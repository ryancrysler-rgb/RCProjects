#!/usr/bin/env python3
"""One-shot runner: capture the API, find the shots, write a CSV.

Written for people who don't live in a terminal -- it asks a couple of
questions with sensible defaults, then does everything else itself.

It always leaves DIAGNOSTICS.txt behind, whether it succeeded or not, so a
failed run can still be diagnosed by someone else.
"""
from __future__ import annotations

import csv
import datetime
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import shotjson

HERE = Path(__file__).parent
DEFAULT_URL = "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1"
DEFAULT_PLAYER = "45"
DEFAULT_NAME = "Canter"

diagnostics: list[str] = []


def log(line: str = "", quiet: bool = False) -> None:
    """Record a line for DIAGNOSTICS.txt, and normally show it too."""
    diagnostics.append(line)
    if not quiet:
        print(line)


def write_diagnostics() -> Path:
    path = HERE / "DIAGNOSTICS.txt"
    header = [
        "DP World Tour scraper - diagnostics",
        f"when   : {datetime.datetime.now():%Y-%m-%d %H:%M:%S}",
        f"python : {sys.version.split()[0]} on {sys.platform}",
        "-" * 62,
    ]
    path.write_text("\n".join(header + diagnostics), encoding="utf-8")
    return path


def ask(question: str, default: str) -> str:
    answer = input(f"{question}\n  [Enter for: {default}]\n> ").strip()
    return answer or default


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


def load_body(item: dict) -> Any:
    try:
        return json.loads(Path(item["body_file"]).read_text(encoding="utf-8"))
    except Exception:
        return None


def extract_rows(manifest: list[dict]) -> tuple[list[dict], dict | None]:
    """Find the best shot table, relaxing the threshold if the strict pass fails."""
    for threshold in (shotjson.MIN_ARRAY_SCORE, 2):
        shotjson.MIN_ARRAY_SCORE = threshold
        for item in manifest[:60]:
            payload = load_body(item)
            if payload is None:
                continue
            rows = shotjson.to_rows(payload)
            if rows:
                if threshold != 6:
                    log(f"(nothing matched strictly; found this at a relaxed threshold of {threshold})")
                return rows, item
    return [], None


def summarise_capture(manifest: list[dict]) -> None:
    """Record every endpoint seen, so a failed run is still diagnosable."""
    log()
    log(f"Captured {len(manifest)} JSON responses. Top 25 by shot-likelihood:", quiet=True)
    for item in manifest[:25]:
        log(f"  [{item.get('score', 0):3d}] {item.get('url', '')[:150]}", quiet=True)
        if item.get("matched_keys"):
            log(f"        keys  : {item['matched_keys'][:14]}", quiet=True)
        if item.get("record_arrays"):
            arrays = ", ".join(f"{p} ({n})" for p, n in item["record_arrays"][:4])
            log(f"        arrays: {arrays}", quiet=True)


def main() -> int:
    print("=" * 62)
    print("  DP World Tour - shot by shot scraper")
    print("=" * 62)
    print()

    url = ask("Which leaderboard page?", DEFAULT_URL)
    name = ask("Player surname (used to click their row)?", DEFAULT_NAME)
    player = ask("Player id (for filtering)?", DEFAULT_PLAYER)
    log(f"url    : {url}", quiet=True)
    log(f"player : {name} / id {player}", quiet=True)

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
    log(f"capture exit code: {result.returncode}", quiet=True)

    manifest_path = out / "manifest.json"
    if not manifest_path.exists():
        log("\nNo JSON was captured at all -- the page never loaded its data.")
        log("Usually a cookie wall that wasn't accepted, or the site blocked the browser.")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    summarise_capture(manifest)

    rows, best = extract_rows(manifest)
    if not rows:
        log("\nCaptured traffic, but nothing shot-shaped in it.")
        log("The endpoint list is saved in DIAGNOSTICS.txt -- send that back to Claude.")
        return 1

    log()
    log("=" * 62)
    log(f"Best endpoint (score {best.get('score', 0)}):")
    log(f"  {best.get('url', '')}")

    all_csv = HERE / "all_shots.csv"
    write_csv(rows, all_csv)
    log(f"\nAll players : {len(rows):5d} rows -> {all_csv.name}")

    wanted = str(player)
    mine = [
        row for row in rows
        if any("player" in key.lower() and str(value) == wanted for key, value in row.items())
    ]
    if mine:
        player_csv = HERE / f"player_{wanted}_shots.csv"
        write_csv(mine, player_csv)
        log(f"Player {wanted:<4}: {len(mine):5d} rows -> {player_csv.name}")
    else:
        log(f"Player {wanted}: no row carried that id -- use all_shots.csv and filter by name.")

    log(f"\nSaved in: {HERE}")
    log("Open the CSV in Excel. Done.")
    log("=" * 62)
    return 0


if __name__ == "__main__":
    code = 1
    try:
        code = main()
    except KeyboardInterrupt:
        log("\nCancelled by user.")
    except Exception as exc:
        log(f"\nSomething went wrong: {type(exc).__name__}: {exc}")
        import traceback
        log(traceback.format_exc(), quiet=True)
    finally:
        path = write_diagnostics()
        print("\n" + "=" * 62)
        print(f"A report of this run was saved to:\n  {path}")
        if code != 0:
            print("\nSend that file back to Claude and it can tell you what happened.")
        print("=" * 62)
        input("\nPress Enter to close this window... ")
    raise SystemExit(code)
