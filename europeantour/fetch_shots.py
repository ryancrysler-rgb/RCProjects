#!/usr/bin/env python3
"""Fetch a DP World Tour JSON endpoint and flatten shot data to CSV.

Once capture_api.py has told you which URL carries the shots, you no longer
need a browser -- hit that endpoint directly, for every round and player you
want.

    python fetch_shots.py --url "<endpoint from manifest.json>" --player 45 --csv canter_r1.csv
    python fetch_shots.py --file captured/bodies/000_041_....json --player 45 --csv canter_r1.csv

Or sweep the guessed endpoint patterns first:

    python fetch_shots.py --probe --event 2026014 --player 45 --round 1
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from typing import Any

import requests

import shotjson

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.europeantour.com/",
    "Origin": "https://www.europeantour.com",
}

# UNVERIFIED guesses, kept only as a starting grid for --probe. The feed is
# undocumented; trust whatever capture_api.py actually observes over these.
CANDIDATE_TEMPLATES = [
    "https://fdapi.europeantour.com/api/sportdata/Leaderboard/Strokeplay/{event}",
    "https://fdapi.europeantour.com/api/sportdata/Scorecard/Strokeplay/Event/{event}/Player/{player}",
    "https://fdapi.europeantour.com/api/sportdata/Scorecard/Strokeplay/Event/{event}/Round/{round}/Player/{player}",
    "https://fdapi.europeantour.com/api/sportdata/ShotByShot/Event/{event}/Round/{round}/Player/{player}",
    "https://fdapi.europeantour.com/api/sportdata/Shots/Event/{event}/Round/{round}/Player/{player}",
    "https://www.europeantour.com/api/sportdata/Leaderboard/Strokeplay/{event}",
    "https://www.europeantour.com/api/sportdata/Scorecard/Strokeplay/Event/{event}/Player/{player}",
]


def get_json(session: requests.Session, url: str, timeout: int = 30) -> Any:
    response = session.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.json()


def write_csv(rows: list[dict[str, Any]], path: str) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def probe(session: requests.Session, args: argparse.Namespace) -> int:
    hits = 0
    for template in CANDIDATE_TEMPLATES:
        url = template.format(event=args.event or "", player=args.player or "", round=args.round or "")
        try:
            payload = get_json(session, url)
        except Exception as exc:
            print(f"  miss  {url}\n        {type(exc).__name__}: {exc}"[:220])
            continue
        score, matched = shotjson.score_payload(payload)
        hits += 1
        print(f"  HIT   {url}\n        score={score} keys={matched[:10]}")
    if not hits:
        print("\nNo template worked -- run capture_api.py to observe the real endpoints.")
    return 0 if hits else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", help="Endpoint to fetch (from capture_api.py's manifest).")
    parser.add_argument("--file", help="Parse a local JSON file instead (e.g. a captured body).")
    parser.add_argument("--probe", action="store_true", help="Try the guessed endpoint patterns.")
    parser.add_argument("--event", help="Tournament/event id.")
    parser.add_argument("--player", help="Player id, e.g. 45 for Laurie Canter.")
    parser.add_argument("--round", help="Round number.")
    parser.add_argument("--csv", help="Write flattened shot rows here.")
    parser.add_argument("--raw", help="Write the raw JSON response here.")
    args = parser.parse_args()

    session = requests.Session()

    if args.probe:
        return probe(session, args)

    if not (args.url or args.file):
        parser.error("pass --url, --file, or --probe")

    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            payload = json.load(handle)
    else:
        payload = get_json(session, args.url)
    if args.raw:
        with open(args.raw, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        print(f"raw JSON -> {args.raw}")

    score, matched = shotjson.score_payload(payload)
    print(f"shot-vocabulary score {score}; matched keys: {matched}")

    rows = shotjson.to_rows(payload)
    if not rows:
        print("No shot-shaped arrays found. Inspect the raw JSON, or lower "
              "shotjson.MIN_ARRAY_SCORE.", file=sys.stderr)
        return 1

    if args.player:
        wanted = str(args.player)
        filtered = [
            row for row in rows
            if any("player" in key.lower() and str(value) == wanted for key, value in row.items())
        ]
        if filtered:
            print(f"filtered {len(rows)} -> {len(filtered)} rows for player {wanted}")
            rows = filtered
        else:
            print(f"note: no row carried player id {wanted}; keeping all rows")

    print(f"{len(rows)} rows across {len({row['_source_path'] for row in rows})} array(s)")
    if args.csv:
        write_csv(rows, args.csv)
        print(f"CSV -> {args.csv}")
    else:
        print(json.dumps(rows[:3], indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
