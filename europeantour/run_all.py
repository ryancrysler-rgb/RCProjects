#!/usr/bin/env python3
"""One-shot runner: capture the API, find the shots, write a CSV.

Written for people who don't live in a terminal -- it asks a couple of
questions with sensible defaults, then does everything else itself.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import shotjson

HERE = Path(__file__).parent
DEFAULT_URL = "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1"
DEFAULT_PLAYER = "45"
DEFAULT_NAME = "Canter"


def ask(question: str, default: str) -> str:
    answer = input(f"{question}\n  [Enter for: {default}]\n> ").strip()
    return answer or default


def main() -> int:
    print("=" * 62)
    print("  DP World Tour - shot by shot scraper")
    print("=" * 62)
    print()

    url = ask("Which leaderboard page?", DEFAULT_URL)
    name = ask("Player surname (used to click their row)?", DEFAULT_NAME)
    player = ask("Player id (for filtering)?", DEFAULT_PLAYER)

    print("\n" + "-" * 62)
    print("A browser window will open. You do NOT need to do anything except:")
    print("  * accept the cookie banner if one appears")
    print("  * then just watch -- it closes itself after about a minute")
    print("-" * 62 + "\n")
    input("Press Enter to start... ")

    out = HERE / "captured"
    result = subprocess.run(
        [
            sys.executable, str(HERE / "capture_api.py"),
            "--url", url,
            "--click-text", name,
            "--headed", "--har",
            "--wait", "12000",
            "--out", str(out),
        ],
        cwd=str(HERE),
    )
    if result.returncode != 0:
        print("\nThe capture step failed -- see the error above.")
        return 1

    manifest_path = out / "manifest.json"
    if not manifest_path.exists():
        print("\nNothing was captured. The page may have been blocked.")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidates = [item for item in manifest if item.get("record_arrays")]
    if not candidates:
        print("\nCaptured traffic, but nothing shot-shaped in it.")
        print(f"Send the whole '{out.name}' folder back to Claude and it can dig deeper.")
        return 1

    best = candidates[0]
    print("\n" + "=" * 62)
    print(f"Best endpoint (score {best['score']}):\n  {best['url']}")

    payload = json.loads(Path(best["body_file"]).read_text(encoding="utf-8"))
    rows = shotjson.to_rows(payload)

    all_csv = HERE / "all_shots.csv"
    write_csv(rows, all_csv)
    print(f"\nAll players : {len(rows):5d} rows -> {all_csv.name}")

    wanted = str(player)
    mine = [
        row for row in rows
        if any("player" in key.lower() and str(value) == wanted for key, value in row.items())
    ]
    if mine:
        player_csv = HERE / f"player_{wanted}_shots.csv"
        write_csv(mine, player_csv)
        print(f"Player {wanted:<4}: {len(mine):5d} rows -> {player_csv.name}")
    else:
        print(f"Player {wanted}: no rows carried that id -- use all_shots.csv and filter by name.")

    print("\nOpen the CSV in Excel. Done.")
    print("=" * 62)
    return 0


def write_csv(rows: list[dict], path: Path) -> None:
    import csv

    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
    except Exception as exc:  # keep the window open so the error is readable
        print(f"\nSomething went wrong: {type(exc).__name__}: {exc}")
        input("\nPress Enter to close... ")
        raise SystemExit(1)
