#!/usr/bin/env python3
"""Open the Shot Tracker and capture the shot feed behind it.

The leaderboard page never loads shot data -- it only appears once the IMG
Arena "Event Centre" opens a player's Shots view. That widget lives in an
iframe and talks GraphQL to btec-http.services.srarena.io using persisted
queries addressed by a numeric hash, so the URL for shots simply does not
exist until something asks for it.

This drives the page to that view and records what comes back.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, Response, sync_playwright

import find_shots
import shotjson

HERE = Path(__file__).parent
DEFAULT_URL = (
    "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1"
)

# Labels the Event Centre uses for the views that load shot data, taken from
# its own translation bundle.
SHOT_VIEWS = ["Shots", "Shot Tracker", "Play by play", "Play By Play", "Tracker", "3D", "Hole"]


def slugify(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", url.split("?")[0])[-70:].strip("_")


def try_click(page: Page, text: str, timeout: int = 5_000) -> bool:
    """Click matching text anywhere on the page, including inside iframes."""
    for frame in page.frames:
        try:
            frame.get_by_text(text, exact=False).first.click(timeout=timeout)
            print(f"    clicked {text!r}" + ("" if frame is page.main_frame else " (in iframe)"))
            return True
        except Exception:
            continue
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--surname", default="Canter")
    parser.add_argument("--headless", action="store_true", help="Hide the browser window.")
    args = parser.parse_args()

    out = HERE / "captured"
    bodies = out / "bodies"
    bodies.mkdir(parents=True, exist_ok=True)

    captured: list[dict[str, Any]] = []
    seen: set[str] = set()

    def on_response(response: Response) -> None:
        url = response.url
        if url in seen or not re.search(r"srarena|imgarena|sportdata|graphql", url, re.I):
            return
        if re.search(r"/locales?/|l10n", url, re.I):
            return
        try:
            payload = response.json()
        except Exception:
            return
        seen.add(url)
        name = f"{len(captured):03d}_{slugify(url)}.json"
        (bodies / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        captured.append({
            "url": url,
            "method": response.request.method,
            "status": response.status,
            "body_file": str(bodies / name),
        })
        operations = list(payload.get("data", {}).keys()) if isinstance(payload, dict) else []
        if operations:
            print(f"    <- {', '.join(operations)}")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=args.headless)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.on("response", on_response)

        print("Opening the leaderboard...")
        page.goto(args.url, wait_until="domcontentloaded", timeout=60_000)
        for selector in ("#onetrust-accept-btn-handler", "button:has-text('Accept All')"):
            try:
                page.click(selector, timeout=5_000)
                print("  accepted cookies")
                break
            except Exception:
                pass
        page.wait_for_timeout(6_000)

        print(f"\nOpening {args.surname}'s player view...")
        if not try_click(page, args.surname, timeout=15_000):
            print(f"  couldn't find a row for {args.surname} -- is that player in this event?")
        page.wait_for_timeout(8_000)

        print("\nLooking for the shot views...")
        for label in SHOT_VIEWS:
            if try_click(page, label):
                page.wait_for_timeout(7_000)

        print("\nSettling...")
        page.wait_for_timeout(6_000)
        context.close()
        browser.close()

    (out / "manifest.json").write_text(json.dumps(captured, indent=2), encoding="utf-8")
    print(f"\nCaptured {len(captured)} data responses.")

    shotjson.MIN_ARRAY_SCORE = 2
    findings = []
    for item in captured:
        payload = json.loads(Path(item["body_file"]).read_text(encoding="utf-8"))
        for path, records, context_fields in shotjson.find_record_arrays(payload):
            score, fields = find_shots.assess(records)
            if score:
                findings.append((score, item["url"], path, records, context_fields, fields))
    findings.sort(key=lambda f: f[0], reverse=True)

    real = [f for f in findings if len(set(f[5]) - {"x", "y", "z"}) >= 2]
    if not real:
        print("\nStill no per-shot records. The Shots view may not have opened,")
        print("or this event doesn't publish shot tracking for that player.")
        print("Run SEND DATA TO CLAUDE and push, and Claude can look at what arrived.")
        input("\nPress Enter to close... ")
        return 1

    score, url, path, records, context_fields, fields = real[0]
    rows = [
        {**shotjson.flatten(context_fields), **shotjson.flatten(record)}
        for record in records
    ]
    find_shots.write_csv(rows, HERE / "SHOT_BY_SHOT.csv")
    print(f"\nSHOT BY SHOT FOUND: {len(rows)} rows -> SHOT_BY_SHOT.csv")
    print(f"  from   : {url}")
    print(f"  fields : {fields}")
    input("\nPress Enter to close... ")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"\nSomething went wrong: {type(exc).__name__}: {exc}")
        input("\nPress Enter to close... ")
        raise SystemExit(1)
