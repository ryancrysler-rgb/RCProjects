#!/usr/bin/env python3
"""Record the shot data behind the AI Shot Commentary panel.

You drive, this records. Guessing at button labels from the outside kept
missing the view; you can reach it in seconds. So this opens a browser,
captures every data response and websocket message while you click through
to the commentary, and works out what's in them once you close the window.

The commentary lines are rendered from structured records -- the site's own
translation bundle formats them as "Shot {{shotNumber}}" and
"{{distance,metresToYards}}" -- so the feed behind them carries the shot
number, distance and surface as fields, not just prose.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

from playwright.sync_api import Response, sync_playwright

import find_shots
import shotjson

HERE = Path(__file__).parent
DEFAULT_URL = (
    "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1"
)

NOISE = re.compile(
    r"onetrust|doubleverify|doubleclick|googlesyndication|googletagmanager|"
    r"google-analytics|adservice|safeframe|criteo|teads|prebid|aditude|"
    r"amazon-adsystem|/locales?/|l10n|sentry|chartbeat|permutive",
    re.I,
)


def slugify(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", url.split("?")[0])[-70:].strip("_")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--minutes", type=float, default=5.0, help="Give up after this long.")
    args = parser.parse_args()

    out = HERE / "captured"
    bodies = out / "bodies"
    bodies.mkdir(parents=True, exist_ok=True)

    captured: list[dict[str, Any]] = []
    ws_frames: list[dict[str, Any]] = []
    seen: set[str] = set()

    def record(url: str, payload: Any, kind: str) -> None:
        name = f"{len(captured):03d}_{slugify(url)}.json"
        (bodies / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        captured.append({"url": url, "kind": kind, "body_file": str(bodies / name)})
        if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
            print(f"   <- {', '.join(payload['data'].keys())}")

    def on_response(response: Response) -> None:
        url = response.url
        if url in seen or NOISE.search(url):
            return
        try:
            payload = response.json()
        except Exception:
            return
        seen.add(url)
        record(url, payload, "http")

    def on_websocket(ws) -> None:
        print(f"   websocket opened: {ws.url[:90]}")

        def on_frame(payload) -> None:
            if isinstance(payload, bytes):
                return
            try:
                parsed = json.loads(payload)
            except Exception:
                return
            ws_frames.append({"url": ws.url, "payload": parsed})

        ws.on("framereceived", on_frame)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1500, "height": 950},
        )
        page = context.new_page()
        page.on("response", on_response)
        page.on("websocket", on_websocket)

        page.goto(args.url, wait_until="domcontentloaded", timeout=60_000)
        for selector in ("#onetrust-accept-btn-handler", "button:has-text('Accept All')"):
            try:
                page.click(selector, timeout=5_000)
                break
            except Exception:
                pass

        print("\n" + "=" * 64)
        print("  YOUR TURN -- in the browser window that just opened:")
        print()
        print("   1. Click on Laurie Canter")
        print("   2. Open the Scorecard, and click a hole")
        print("   3. Open the AI SHOT COMMENTARY panel")
        print("   4. Click through a few holes so it loads more shots")
        print()
        print("  Then CLOSE THE BROWSER WINDOW. Everything gets saved.")
        print("=" * 64 + "\n")

        deadline = time.time() + args.minutes * 60
        last_report = 0
        while time.time() < deadline:
            if page.is_closed():
                break
            try:
                page.wait_for_timeout(1_000)
            except Exception:
                break  # window closed mid-wait
            if len(captured) != last_report:
                last_report = len(captured)
        print(f"\nFinished. {len(captured)} data responses, {len(ws_frames)} websocket messages.")

        try:
            context.close()
            browser.close()
        except Exception:
            pass

    if ws_frames:
        (out / "websocket_frames.json").write_text(json.dumps(ws_frames, indent=2), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(captured, indent=2), encoding="utf-8")

    payloads = [(item["url"], json.loads(Path(item["body_file"]).read_text(encoding="utf-8")))
                for item in captured]
    payloads += [(frame["url"], frame["payload"]) for frame in ws_frames]

    shotjson.MIN_ARRAY_SCORE = 2
    shots, commentary = [], []
    for url, payload in payloads:
        for path, records, context_fields in shotjson.find_record_arrays(payload):
            score, fields = find_shots.assess(records)
            if score and len(set(fields) - {"x", "y", "z"}) >= 2:
                shots.append((score, url, records, context_fields, fields))
            score, fields = find_shots.assess_commentary(records)
            if score:
                commentary.append((score, url, records, context_fields, fields))

    wrote = False
    for label, findings, filename in (
        ("shot records", shots, "SHOT_BY_SHOT.csv"),
        ("AI commentary", commentary, "AI_COMMENTARY.csv"),
    ):
        if not findings:
            continue
        findings.sort(key=lambda f: f[0], reverse=True)
        score, url, records, context_fields, fields = findings[0]
        rows = [
            {**shotjson.flatten(context_fields), **shotjson.flatten(record)}
            for record in records
        ]
        find_shots.write_csv(rows, HERE / filename)
        print(f"\n{label}: {len(rows)} rows -> {filename}")
        print(f"  from   : {url[:110]}")
        print(f"  fields : {fields}")
        wrote = True

    if not wrote:
        print("\nNothing shot-shaped arrived. Run SEND DATA TO CLAUDE and push --")
        print("Claude can then read exactly what the commentary panel requested.")
    input("\nPress Enter to close... ")
    return 0 if wrote else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"\nSomething went wrong: {type(exc).__name__}: {exc}")
        input("\nPress Enter to close... ")
        raise SystemExit(1)
