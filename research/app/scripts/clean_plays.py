import os
import time
import asyncio
from pathlib import Path
import xml.etree.ElementTree as ET
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.game import Game

CACHE_DIR = Path(__file__).resolve().parents[1] / "bgg_cache"
RAW_PLAYS_DIR = CACHE_DIR / "plays"
CLEAN_PLAYS_DIR = CACHE_DIR / "bgg_plays"


def pobierz_rozgrywki_bgg(bgg_id: int, ilosc_stron: int = 10) -> list[Path]:
    load_dotenv()
    RAW_PLAYS_DIR.mkdir(parents=True, exist_ok=True)
    pobrane_pliki = []

    url = "https://boardgamegeek.com/xmlapi2/plays"
    headers = {"User-Agent": "MeepleOS/1.0"}
    api_key = os.getenv("BGG_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print(f"\n[BGG DOWNLOAD] Sprawdzanie rozgrywek dla gry ID: {bgg_id} (strony 1-{ilosc_stron})...")

    for strona in range(1, ilosc_stron + 1):
        plik = RAW_PLAYS_DIR / f"{bgg_id}_strona_{strona}.xml"
        if plik.exists():
            print(f"[CACHE] Plik {plik.name} już istnieje. Pomijam pobieranie.")
            pobrane_pliki.append(plik)
            continue

        print(f"[{strona}/{ilosc_stron}] Pobieram z BGG (ID: {bgg_id}, strona: {strona})...")
        params = {"id": bgg_id, "subtype": "boardgame", "page": strona}
        time.sleep(2)

        while True:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                break
            elif response.status_code == 202:
                print(f"[BGG 202] BGG kolejkuje zapytanie dla strony {strona}. Czekam 4s...")
                time.sleep(4)
            else:
                response.raise_for_status()

        with open(plik, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"[POBRANO] Zapisano surowy XML: {plik.name}")
        pobrane_pliki.append(plik)

    return pobrane_pliki


async def load_games_metadata() -> dict[int, dict]:
    async with AsyncSessionLocal() as session:
        query = select(
            Game.bgg_id,
            Game.title,
            Game.weight,
            Game.text_heaviness,
            Game.optimal_playtime,
            Game.min_playtime,
            Game.max_playtime,
            Game.min_player,
            Game.max_player,
        )
        result = await session.execute(query)
        games_dict = {}
        for row in result.all():
            base_time = row.optimal_playtime
            if not base_time or base_time <= 0:
                min_p = row.min_playtime or 0
                max_p = row.max_playtime or 0
                base_time = (min_p + max_p) // 2 if (min_p + max_p) > 0 else None

            games_dict[row.bgg_id] = {
                "title": row.title,
                "weight": float(row.weight) if row.weight is not None else None,
                "text_heaviness": row.text_heaviness,
                "base_time": base_time,
                "min_player": row.min_player,
                "max_player": row.max_player,
            }
        print(f"[BAZA] Załadowano metadane dla {len(games_dict)} gier do pamięci.")
        return games_dict


def parsuj_i_oczysc_rozgrywki(xml_files: list[Path], games_meta: dict[int, dict]) -> pd.DataFrame:
    stats = {
        "total_parsed": 0,
        "rejected_incomplete": 0,
        "rejected_zero_length": 0,
        "rejected_outliers": 0,
        "rejected_players_count": 0,
        "accepted": 0,
    }

    cleaned_rows = []

    for file_path in xml_files:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except Exception as e:
            print(f"[OSTRZEŻENIE] Błąd czytania {file_path.name}: {e}")
            continue

        for play in root.findall("play"):
            stats["total_parsed"] += 1

            if play.get("incomplete") != "0":
                stats["rejected_incomplete"] += 1
                continue

            length_str = play.get("length", "0")
            try:
                real_length = int(length_str)
            except ValueError:
                real_length = 0

            if real_length == 0:
                stats["rejected_zero_length"] += 1
                continue

            if real_length < 15 or real_length > 360:
                stats["rejected_outliers"] += 1
                continue

            item = play.find("item")
            if item is None:
                continue

            try:
                bgg_id = int(item.get("objectid"))
            except (ValueError, TypeError):
                continue

            game = games_meta.get(bgg_id)

            players_elems = play.findall("./players/player")
            players_count = len(players_elems)

            min_pl = game["min_player"] or 1
            max_pl = game["max_player"] or 99

            if not (min_pl <= players_count <= max_pl):
                stats["rejected_players_count"] += 1
                continue

            weight = game["weight"]
            text_heaviness = game["text_heaviness"]
            base_time = game["base_time"]

            paralysis_ratio = round(real_length / base_time, 4)

            cleaned_rows.append({
                "play_id": play.get("id"),
                "date": play.get("date"),
                "bgg_id": bgg_id,
                "game_title": game["title"],
                "weight": weight,
                "players_count": players_count,
                "text_heaviness": text_heaviness,
                "base_time": base_time,
                "real_length": real_length,
                "paralysis_ratio": paralysis_ratio,
            })
            stats["accepted"] += 1

    print("\n" + "=" * 55)
    print("           RAPORT CZYSZCZENIA DANYCH         ")
    print("=" * 55)
    print(f"Łącznie sparsowanych partii:          {stats['total_parsed']}")
    print(f"├── 1. Odrzucono (nieukończone):       {stats['rejected_incomplete']}")
    print(f"├── 2. Odrzucono (czas = 0):           {stats['rejected_zero_length']}")
    print(f"├── 3. Odrzucono (outliery <15/>360):  {stats['rejected_outliers']}")
    print(f"├── 4. Odrzucono (błędna l. graczy):   {stats['rejected_players_count']}")
    print("-" * 55)
    print(f"ZAAKCEPTOWANE REKORDY TRENINGOWE:     {stats['accepted']}")
    print("=" * 55 + "\n")

    return pd.DataFrame(cleaned_rows)


async def main(bgg_ids: list[int] = [13], ilosc_stron: int = 10):
    CLEAN_PLAYS_DIR.mkdir(parents=True, exist_ok=True)

    wszystkie_pliki = []
    for g_id in bgg_ids:
        pliki_gry = pobierz_rozgrywki_bgg(bgg_id=g_id, ilosc_stron=ilosc_stron)
        wszystkie_pliki.extend(pliki_gry)

    games_meta = await load_games_metadata()

    df = parsuj_i_oczysc_rozgrywki(wszystkie_pliki, games_meta)

    if not df.empty:
        output_csv = CLEAN_PLAYS_DIR / "training_plays.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8")
        print(f"[SUKCES] Zapisano wyczyszczony dataset do: {output_csv}")
    else:
        print("[OSTRZEŻENIE] Brak rekordów spełniających kryteria filtrów.")


if __name__ == "__main__":
    pobierz_rozgrywki_bgg(203417, 30)
    asyncio.run(main(bgg_ids=[203417], ilosc_stron=30))
