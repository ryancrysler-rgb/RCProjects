#!/usr/bin/env python3
"""Search everything already captured for genuine shot-by-shot data.

Answers one question: of the payloads on this machine, which -- if any --
actually contain per-shot records, as opposed to hole scores or UI labels?

Run it after START HERE has captured a session. Nothing is downloaded.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import shotjson

HERE = Path(__file__).parent

# Fields that only exist once you are describing an individual shot. Hole
# scores never carry these.
SHOT_ONLY = {
    "shotnumber", "strokenumber", "club", "clubused", "distancetopin",
    "distancetohole", "carry", "lie", "surface", "trajectory", "ballposition",
    "ballspeed", "launchangle", "spin", "apex", "fromlocation", "tolocation",
}
COORDS = {"x", "y", "z", "latitude", "longitude"}


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def assess(rows: list[dict]) -> tuple[int, list[str]]:
    """Score a candidate table, demanding real values rather than labels.

    Localisation bundles contain every shot field name in the app mapped to
    display text, so a key-name match alone proves nothing -- the values have
    to be numbers or short codes.
    """
    keys = {shotjson.norm_key(k): k for row in rows for k in row}
    shot_keys = sorted(set(keys) & SHOT_ONLY)
    coord_keys = sorted(set(keys) & COORDS)

    has_values = any(
        is_number(row[keys[k]])
        for k in shot_keys + coord_keys
        for row in rows
        if keys[k] in row
    )
    if not has_values:
        return 0, []

    score = len(shot_keys) * 3 + (2 if len(coord_keys) >= 2 else 0)
    if len(rows) >= 3:
        score += 1
    return score, shot_keys + coord_keys


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
    manifest_path = HERE / "captured" / "manifest.json"
    if not manifest_path.exists():
        print("Nothing captured yet -- run START HERE (Windows).bat first.")
        input("\nPress Enter to close... ")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(f"Searching {len(manifest)} captured payloads for per-shot records...\n")

    shotjson.MIN_ARRAY_SCORE = 2
    findings = []
    for item in manifest:
        body = Path(item.get("body_file", ""))
        if not body.exists():
            continue
        try:
            payload = json.loads(body.read_text(encoding="utf-8"))
        except Exception:
            continue
        for path, records, context in shotjson.find_record_arrays(payload):
            score, matched = assess(records)
            if score:
                findings.append({
                    "score": score, "url": item.get("url", ""), "file": body.name,
                    "json_path": path, "rows": records, "context": context,
                    "fields": matched,
                })

    findings.sort(key=lambda f: f["score"], reverse=True)

    if not findings:
        print("No shot-by-shot data in anything captured.")
        print("\nThe tour's own API publishes hole scores. Shot tracking on that site")
        print("comes from IMG Arena (srarena.io), and it is not in what was captured.")
        input("\nPress Enter to close... ")
        return 1

    print(f"Found {len(findings)} candidate table(s):\n")
    for index, finding in enumerate(findings[:10], start=1):
        print(f"{index}. score {finding['score']} - {len(finding['rows'])} rows")
        print(f"   from  : {finding['url'][:120]}")
        print(f"   file  : captured\\bodies\\{finding['file']}")
        print(f"   fields: {finding['fields']}")
        print()

    for index, finding in enumerate(findings[:3], start=1):
        rows = [
            {**shotjson.flatten(finding["context"]), **shotjson.flatten(record)}
            for record in finding["rows"]
        ]
        out = HERE / f"SHOT_DATA_{index}.csv"
        write_csv(rows, out)
        print(f"Wrote {out.name} ({len(rows)} rows)")

    print("\nOpen SHOT_DATA_1.csv first -- that's the strongest match.")
    input("\nPress Enter to close... ")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
