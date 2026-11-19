import csv
from pathlib import Path
import html
import json
import re
import time
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
import requests
from app.core.database import AsyncSessionLocal
from sqlalchemy import select
from app.models.game import Game, Mechanic, Category
import asyncio

def get_top_bgg_ids(csv_path: Path, limit: int = 1000) -> list[int]:
    ranked_games = []
    with open (csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            id_tekst = row.get("id_bgg", "").strip()
            rank_tekst = row.get("rank", "").strip()
            if id_tekst and rank_tekst:
                try:
                    id_liczba = int(id_tekst)
                    rank_liczba = float(rank_tekst)
                    if rank_liczba > 0:
                        ranked_games.append((id_liczba, rank_liczba))
                except ValueError:
                    continue

    ranked_games.sort(key=lambda x: x[1])
    return [game_id for game_id, rank in ranked_games[:limit]]

def clean_text(text):
    if text:
        text = html.unescape(text)
        return re.sub(r'\s+', ' ', text).strip()
    return None


def safe_int(val, default=None):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def safe_float(val, default=None, ndigits=2):
    try:
        res = float(val)
        return round(res, ndigits) if ndigits is not None else res
    except (ValueError, TypeError):
        return default


def parse_bgg_item(item):
    bgg_id = safe_int(item.get("id"))

    primary_name_elem = item.find("./name[@type='primary']")
    title = clean_text(primary_name_elem.get("value")) if primary_name_elem is not None else None

    polish_title = None
    versions_node = item.find("versions")
    if versions_node is not None:
        for version in versions_node.findall("item"):
            lang_link = version.find("./link[@type='language'][@value='Polish']")
            if lang_link is not None:
                canon = version.find("canonicalname")
                if canon is not None and canon.get("value"):
                    polish_title = clean_text(canon.get("value"))
                    break

    if not polish_title:
        for alt_name in item.findall("./name[@type='alternate']"):
            val = alt_name.get("value", "")
            if "Catan" in val and any(pl_char in val for pl_char in ["Osadnicy", "planszowa"]):
                polish_title = clean_text(val)
                break



    min_player_elem = item.find("minplayers")
    min_player = safe_int(min_player_elem.get("value")) if min_player_elem is not None else None

    publisher_elem = item.find("./link[@type='boardgamepublisher']")
    publisher = clean_text(publisher_elem.get("value")) if publisher_elem is not None else None

    designer_elem = item.find("./link[@type='boardgamedesigner']")
    designer = clean_text(designer_elem.get("value")) if designer_elem is not None else None

    max_player_elem = item.find("maxplayers")
    max_player = safe_int(max_player_elem.get("value")) if max_player_elem is not None else None

    optimal_player = None
    poll_summary = item.find("./poll-summary[@name='suggested_numplayers']")
    if poll_summary is not None:
        best_with = poll_summary.find("./result[@name='bestwith']")
        if best_with is not None:
            match = re.search(r'\d+', best_with.get("value", ""))
            if match:
                optimal_player = safe_int(match.group(0))

    min_pt_elem = item.find("minplaytime")
    min_playtime = safe_int(min_pt_elem.get("value")) if min_pt_elem is not None else None

    max_pt_elem = item.find("maxplaytime")
    max_playtime = safe_int(max_pt_elem.get("value")) if max_pt_elem is not None else None

    opt_pt_elem = item.find("playingtime")
    optimal_playtime = safe_int(opt_pt_elem.get("value")) if opt_pt_elem is not None else None

    year_elem = item.find("yearpublished")
    year_published = safe_int(year_elem.get("value")) if year_elem is not None else None

    desc_elem = item.find("description")
    description = clean_text(desc_elem.text) if desc_elem is not None else None

    min_age_elem = item.find("minage")
    min_age = safe_int(min_age_elem.get("value")) if min_age_elem is not None else None

    community_min_age = None
    age_pool = item.find("./poll[@name='suggested_playerage']")
    if age_pool is not None:
        best_age = None
        max_votes = -1
        for res in age_pool.findall("./results/result"):
            votes = safe_int(res.get("numvotes"), 0)
            val_match = re.search(r'\d+', res.get("value", ""))
            age = safe_int(val_match.group(0)) if val_match else None
            if votes > max_votes and age is not None:
                max_votes = votes
                best_age = age
        if max_votes > 0:
            community_min_age  = best_age

    community_players_min = None
    community_players_max = None
    players_pool = item.find("./poll-summary[@name='suggested_numplayers']")
    if players_pool is not None:
        rec_res = players_pool.find("./result[@name='recommmendedwith']")
        if rec_res is not None:
            tekst = rec_res.get("value")
            bufor = re.findall(r'\d+', tekst)
            if len(bufor) >= 2:
                community_players_min = safe_int(bufor[0])
                community_players_max = safe_int(bufor[1])
            elif len(bufor) == 1:
                community_players_min = safe_int(bufor[0])
                community_players_max = safe_int(bufor[0])
    if community_players_min is None:
        community_players_min = min_player
        community_players_max = max_player

    img_elem = item.find("image")
    image_url = clean_text(img_elem.text) if img_elem is not None else None

    thumb_elem = item.find("thumbnail")
    thumbnail_url = clean_text(thumb_elem.text) if thumb_elem is not None else None

    text_heaviness = None
    lang_poll = item.find("./poll[@name='language_dependence']")
    if lang_poll is not None:
        best_level = None
        max_votes = -1
        for res in lang_poll.findall("./results/result"):
            votes = safe_int(res.get("numvotes"), 0)
            level = safe_int(res.get("level"))
            if votes > max_votes and level is not None:
                max_votes = votes
                best_level = level
        if max_votes > 0:
            text_heaviness = best_level

    is_expansion = (item.get("type") == "boardgameexpansion")
    parent_bgg_id = None
    if is_expansion:
        for link in item.findall("./link[@type='boardgameexpansion'][@inbound='true']"):
            parent_bgg_id = safe_int(link.get("id"))
            break

    tutorial_video_url_pl = None
    tutorial_video_url_eng = None
    videos_node = item.find("videos")
    if videos_node is not None:
        for vid in videos_node.findall("video"):
            if vid.get("category") == "instructional":
                lang = vid.get("language")
                link = vid.get("link")
                if lang == "Polish" and not tutorial_video_url_pl:
                    tutorial_video_url_pl = link
                elif lang == "English" and not tutorial_video_url_eng:
                    tutorial_video_url_eng = link

    weight = None
    bayes_avg = None
    stddev = None
    users_rated = None
    bgg_rank = None

    ratings = item.find("./statistics/ratings")
    if ratings is not None:
        w_val = safe_float(ratings.find("averageweight").get("value")) if ratings.find("averageweight") is not None else None
        weight = w_val if (w_val is not None and w_val > 0.0) else None

        b_val = safe_float(ratings.find("bayesaverage").get("value")) if ratings.find("bayesaverage") is not None else None
        bayes_avg = b_val if (b_val is not None and b_val > 0.0) else None

        stddev = safe_float(ratings.find("stddev").get("value")) if ratings.find("stddev") is not None else None
        users_rated = safe_int(ratings.find("usersrated").get("value")) if ratings.find("usersrated") is not None else None

        rank_elem = ratings.find("./ranks/rank[@type='subtype'][@name='boardgame']")
        if rank_elem is not None:
            bgg_rank = safe_int(rank_elem.get("value"))

    mechanics = []
    for mech in item.findall("./link[@type='boardgamemechanic']"):
        mechanics.append({
            "bgg_id": safe_int(mech.get("id")),
            "name": clean_text(mech.get("value"))
        })

    categories = []
    for cat in item.findall("./link[@type='boardgamecategory']"):
        categories.append({
            "bgg_id": safe_int(cat.get("id")),
            "name": clean_text(cat.get("value"))
        })

    game_data = {
        "bgg_id": bgg_id,
        "title": title,
        "polish_title": polish_title,
        "parent_bgg_id": parent_bgg_id,
        "is_expansion": is_expansion,
        "text_heaviness": text_heaviness,
        "tutorial_video_url_pl": tutorial_video_url_pl,
        "tutorial_video_url_eng": tutorial_video_url_eng,
        "publisher": publisher,
        "designer": designer,
        "min_player": min_player,
        "max_player": max_player,
        "optimal_player": optimal_player,
        "community_players_min": community_players_min,
        "community_players_max": community_players_max,
        "min_age": min_age,
        "community_min_age": community_min_age,
        "min_playtime": min_playtime,
        "max_playtime": max_playtime,
        "optimal_playtime": optimal_playtime,
        "weight": weight,
        "bayes_avg": bayes_avg,
        "stddev": stddev,
        "bgg_rank": bgg_rank,
        "users_rated": users_rated,
        "year_published": year_published,
        "image_url": image_url,
        "thumbnail_url": thumbnail_url,
        "description": description,
        "mechanics": mechanics,
        "categories": categories
    }

    return game_data

def pobierz_gry(top_ids, rozmiar_paczki):
    ilosc_gier = len(top_ids)
    sciezka_cache = Path(__file__).resolve().parent / "bgg_cache" / f"top{ilosc_gier}_games.json"
    if sciezka_cache.exists():
        print(f"[CACHE] Plik {sciezka_cache} już istnieje! Pomijam pobieranie z sieci.")
        with open(sciezka_cache, "r", encoding="utf-8") as f:
            return json.load(f)

    load_dotenv()
    url = "https://boardgamegeek.com/xmlapi2/thing"
    headers = {"Authorization": f"Bearer {os.getenv("BGG_API_KEY")}", }

    start_time = time.perf_counter()
    os.makedirs("games", exist_ok=True)

    try:
        wszystkie_gry = []
        lacznie_paczek = (len(top_ids) + rozmiar_paczki - 1) // rozmiar_paczki
        for i in range(0, len(top_ids), rozmiar_paczki):
            idx = (i // rozmiar_paczki) + 1

            paczka = top_ids[i: i + rozmiar_paczki]
            ids_param = ",".join(str(g_id) for g_id in paczka)
            params = {"id": ids_param, "stats": "1", "versions": "1", "videos": "1", "type": "boardgame"}
            print(f"[{idx}/{lacznie_paczek}] Pobieram paczkę gier: {ids_param}")
            time.sleep(4)
            response = requests.get(url, headers=headers, params=params)
            print("Response: ", response.status_code)
            print("--- Wczytywanie i parsowanie ---")
            root = ET.fromstring(response.text)
            for item in root.findall("item"):
                parsed_game = parse_bgg_item(item)
                wszystkie_gry.append(parsed_game)
                print(f"[PARSER] Pobrano: {parsed_game['title']} (ID: {parsed_game['bgg_id']})")

        sciezka_cache = Path(__file__).resolve().parent / "bgg_cache" / f"top{ilosc_gier}_games.json"
        sciezka_cache.parent.mkdir(parents=True, exist_ok=True)

        with open(sciezka_cache, "w", encoding="utf-8") as f:
            json.dump(wszystkie_gry, f, indent=2, ensure_ascii=False)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Czas wykonania: {total_time:.2f} sekund")
        print(f"[ZAPISANO] Zapisano zbiorczy plik cache: {sciezka_cache}")
        return wszystkie_gry

    except Exception as ex:
        print(f"Coś poszło nie tak: {ex}")

async def seed_database(games_data: list[dict]):
    async with AsyncSessionLocal() as session:
        result_m = await session.execute(select(Mechanic))
        existing_mechanics: dict[int, Mechanic] = {m.bgg_id: m for m in result_m.scalars().all()}

        result_c = await session.execute(select(Category))
        existing_categories: dict[int, Category] = {c.bgg_id: c for c in result_c.scalars().all()}

        result_g = await session.execute(select(Game.bgg_id))
        existing_game_ids: set[int] = set(result_g.scalars().all())

        print(f"[BAZA] W bazie jest już: {len(existing_game_ids)} gier, {len(existing_mechanics)} mechanik, {len(existing_categories)} kategorii.")

        nowe_gry_count = 0

        for g in games_data:
            bgg_id = g["bgg_id"]
            if bgg_id in existing_game_ids:
                continue

            mechaniki_dla_gry = []
            for m_data in g.get("mechanics", []):
                m_id = m_data["bgg_id"]
                if m_id not in existing_mechanics:
                    nowa_m = Mechanic(bgg_id=m_id, name=m_data["name"])
                    session.add(nowa_m)
                    existing_mechanics[m_id] = nowa_m
                mechaniki_dla_gry.append(existing_mechanics[m_id])

            kategorie_dla_gry = []
            for c_data in g.get("categories", []):
                c_id = c_data["bgg_id"]
                if c_id not in existing_categories:
                    nowa_c = Category(bgg_id=c_id, name=c_data["name"])
                    session.add(nowa_c)
                    existing_categories[c_id] = nowa_c
                kategorie_dla_gry.append(existing_categories[c_id])

            nowa_gra = Game(
                bgg_id=bgg_id,
                title=g["title"],
                polish_title=g.get("polish_title"),
                is_expansion=g.get("is_expansion", False),
                text_heaviness=g.get("text_heaviness"),
                tutorial_video_url_pl=g.get("tutorial_video_url_pl"),
                tutorial_video_url_eng=g.get("tutorial_video_url_eng"),
                publisher=g.get("publisher"),
                designer=g.get("designer"),
                min_player=g.get("min_player"),
                max_player=g.get("max_player"),
                optimal_player=g.get("optimal_player"),
                community_players_min=g.get("community_players_min"),
                community_players_max=g.get("community_players_max"),
                min_age=g.get("min_age"),
                community_min_age=g.get("community_min_age"),
                min_playtime=g.get("min_playtime"),
                max_playtime=g.get("max_playtime"),
                optimal_playtime=g.get("optimal_playtime"),
                weight=g.get("weight"),
                bayes_avg=g.get("bayes_avg"),
                stddev=g.get("stddev"),
                bgg_rank=g.get("bgg_rank"),
                users_rated=g.get("users_rated"),
                year_published=g.get("year_published"),
                image_url=g.get("image_url"),
                thumbnail_url=g.get("thumbnail_url"),
                description=g.get("description"),
                mechanics=mechaniki_dla_gry,
                categories=kategorie_dla_gry
            )

            session.add(nowa_gra)
            existing_game_ids.add(bgg_id)
            nowe_gry_count += 1

        await session.commit()
        print(f"[SUKCES] Zapisano do bazy {nowe_gry_count} nowych gier!")

if __name__ == "__main__":
    sciezka_csv = Path(__file__).resolve().parents[3] / "dane_kaggle" / "game.csv"
    top_ids = get_top_bgg_ids(sciezka_csv, limit=1000)
    rozmiar_paczki = 20
    gry = pobierz_gry(top_ids, rozmiar_paczki)
    asyncio.run(seed_database(gry))