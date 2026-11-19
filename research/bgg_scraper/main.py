import html
import json
import re
import time
import xml.etree.ElementTree as ET
import os
from asyncio import wait
from dotenv import load_dotenv
import requests


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

def pobierz_gry():
    load_dotenv()
    url = "https://boardgamegeek.com/xmlapi2/thing"
    headers = {"Authorization": f"Bearer {os.getenv("BGG_API_KEY")}", }

    start_time = time.perf_counter()
    os.makedirs("games", exist_ok=True)

    try:
        ilosc_gier = 30
        ids = []
        rozmiar_paczki = 10
        for i in range(1, ilosc_gier + 1):
            ids.append(f"{i}")
            if len(ids) == rozmiar_paczki or i == ilosc_gier:
                params = {"id": ",".join(ids), "stats": "1", "versions": "1", "videos": "1", "type": 'boardgame'}

                time.sleep(5)
                response = requests.get(url, headers=headers, params=params)

                print("Response: ", response.status_code)

                print("--- Wczytywanie i parsowanie ---")
                root = ET.fromstring(response.text)
                for item in root.findall("item"):
                    parsed_game = parse_bgg_item(item)

                    safe_title = re.sub(r'[\\/*?:"<>|]', "", parsed_game["title"]).replace(" ", "_").lower()
                    filename = f"{parsed_game['bgg_id']}_{safe_title}"

                    with open(f"games/{filename}.json", "w", encoding="utf-8") as f:
                        json.dump(parsed_game, f, indent=2, ensure_ascii=False)

                    print(f"[SUKCES] Zapisano: {filename}.json")
                ids = []

        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Czas wykonania: {total_time:.2f} sekund")
    except Exception as ex:
        print(f"Coś poszło nie tak: {ex}")

def pobierz_rozgrywki():
    load_dotenv()
    url = "https://boardgamegeek.com/xmlapi2/plays"
    headers = {"Authorization": f"Bearer {os.getenv("BGG_API_KEY")}", }

    start_time = time.perf_counter()
    os.makedirs("plays", exist_ok=True)

    try:
        ilosc_stron = 10
        for strona in range(1, ilosc_stron + 1):
            params = {"id": 13, "subtype": "boardgame", "page": strona}

            time.sleep(2)

            while True:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    break
                elif response.status_code == 202:
                    print(f"Strona {strona}: BGG kolejkuje (202). Trzeba ponowić zapytanie")
                    time.sleep(5)
                else:
                    response.raise_for_status()

            with open(f"plays/13_strona_{strona}.xml", "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[SUKCES] Zapisano: 13_strona_{strona}.xml")
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Czas wykonania: {total_time:.2f} sekund")
    except Exception as ex:
        print(f"Coś poszło nie tak: {ex}")        

if __name__ == "__main__":
    pobierz_rozgrywki()