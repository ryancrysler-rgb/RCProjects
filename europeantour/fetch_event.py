#!/usr/bin/env python3
"""Pull a player's data straight from the DP World Tour's own API.

These endpoints were observed live on the Amgen Irish Open 2026 leaderboard,
so unlike the earlier guesswork they are known-good:

    /api/sportdata/Leaderboard/Strokeplay/{event}/type/load
    /api/sportdata/Scorecard/Strokeplay/Event/{event}/Player/{player}

No browser needed. The leaderboard call also resolves a surname to the
player id their API actually uses, which is not the id shown on the website.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Iterator

import requests

import shotjson

HERE = Path(__file__).parent
BASE = "https://www.europeantour.com/api/sportdata"
DEFAULT_EVENT = "2026135"   # Amgen Irish Open 2026
DEFAULT_SURNAME = "Canter"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.europeantour.com/",
}

ID_KEYS = {"playerid", "id", "playercode", "playernumber"}


def get_json(url: str) -> Any:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def walk_dicts(obj: Any) -> Iterator[dict]:
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk_dicts(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_dicts(item)


def find_players(payload: Any) -> list[dict[str, Any]]:
    """Pull every {id, name} pair out of a leaderboard payload."""
    players: dict[str, dict[str, Any]] = {}
    for record in walk_dicts(payload):
        keys = {shotjson.norm_key(k): k for k in record}
        id_key = next((keys[k] for k in ID_KEYS if k in keys), None)
        name_keys = [orig for norm, orig in keys.items() if "name" in norm]
        if not id_key or not name_keys:
            continue
        identifier = record[id_key]
        if not isinstance(identifier, (str, int)):
            continue
        name = " ".join(
            str(record[k]) for k in name_keys
            if isinstance(record[k], str) and record[k].strip()
        )
        if name:
            players[str(identifier)] = {"id": str(identifier), "name": name}
    return list(players.values())


def write_csv(rows: list[dict], path: Path) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--event", default=DEFAULT_EVENT, help="Event id (Irish Open 2026 = 2026135).")
    parser.add_argument("--surname", default=DEFAULT_SURNAME, help="Player surname to look up.")
    parser.add_argument("--player-id", help="Skip the lookup and use this id directly.")
    args = parser.parse_args()

    print(f"Event {args.event}: fetching the leaderboard...")
    leaderboard = get_json(f"{BASE}/Leaderboard/Strokeplay/{args.event}/type/load")
    (HERE / "leaderboard_raw.json").write_text(json.dumps(leaderboard, indent=2), encoding="utf-8")

    players = find_players(leaderboard)
    print(f"  found {len(players)} players in the field")
    if players:
        write_csv(players, HERE / "players.csv")
        print("  full list -> players.csv")

    player_id = args.player_id
    if not player_id:
        matches = [p for p in players if args.surname.lower() in p["name"].lower()]
        if not matches:
            print(f"\nNo player matching '{args.surname}'. Open players.csv and find the right id,")
            print("then run again with --player-id <id>.")
            return 1
        for match in matches:
            print(f"  match: {match['name']}  ->  id {match['id']}")
        player_id = matches[0]["id"]

    print(f"\nFetching scorecard for player {player_id}...")
    scorecard = get_json(f"{BASE}/Scorecard/Strokeplay/Event/{args.event}/Player/{player_id}")
    raw_path = HERE / f"player_{player_id}_scorecard_raw.json"
    raw_path.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")
    print(f"  raw JSON -> {raw_path.name}")

    score, matched = shotjson.score_payload(scorecard)
    shot_words = {"shots", "shotnumber", "club", "distancetopin", "carry", "lie"}
    has_shots = bool(shot_words & set(matched))
    print(f"  shot-vocabulary score {score}: {matched}")
    print(f"  contains shot-level detail: {'YES' if has_shots else 'no -- hole scores only'}")

    shotjson.MIN_ARRAY_SCORE = 2
    rows = shotjson.to_rows(scorecard)
    if rows:
        csv_path = HERE / f"player_{player_id}_scorecard.csv"
        write_csv(rows, csv_path)
        print(f"\n{len(rows)} rows -> {csv_path.name}")
    else:
        print("\nCouldn't find a table in the scorecard; inspect the raw JSON.")
    return 0


if __name__ == "__main__":
    code = 1
    try:
        code = main()
    except requests.HTTPError as exc:
        print(f"\nThe server refused that request: {exc}")
        print("The event id or player id is probably wrong.")
    except requests.RequestException as exc:
        print(f"\nCouldn't reach the site: {exc}")
    except Exception as exc:
        print(f"\nSomething went wrong: {type(exc).__name__}: {exc}")
    finally:
        input("\nPress Enter to close this window... ")
    raise SystemExit(code)
