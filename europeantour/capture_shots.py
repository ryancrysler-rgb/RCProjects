#!/usr/bin/env python3
"""Record the shot data behind the AI Shot Commentary panel.

You drive, this records. Guessing at button labels from the outside kept
missing the view; you can reach it in seconds. So this opens a browser,
captures every data response and websocket message while you click through
the commentary, and works out what's in them once you close the window.

Runs accumulate. Each run saves into its own folder and the analysis reads
every folder, so covering holes 1-10 now and 11-18 later still produces one
complete spreadsheet.

The commentary lines are rendered from structured records -- the site's own
translation bundle formats them as "Shot {{shotNumber}}" and
"{{distance,metresToYards}}" -- so the feed behind them carries the shot
number, distance and surface as fields, not just prose.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import time
import zlib
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


def collect_payloads(captured_dir: Path) -> list[tuple[str, Any]]:
    """Load every payload from every run, this one and any before it."""
    files = sorted(captured_dir.glob("run_*/*.json"))
    files += sorted((captured_dir / "bodies").glob("*.json"))  # older layout
    payloads = []
    for path in files:
        if path.name.startswith("_"):
            continue
        try:
            payloads.append((path.name, json.loads(path.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return payloads


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--minutes", type=float, default=45.0,
                        help="Safety limit if the window is left open (default 45).")
    args = parser.parse_args()

    out = HERE / "captured"
    run_dir = out / f"run_{time.strftime('%Y%m%d_%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    previous = len(collect_payloads(out))
    if previous:
        print(f"Found {previous} payloads from earlier runs -- this run adds to them.\n")

    captured: list[dict[str, Any]] = []
    seen: set[str] = set()

    def record(url: str, payload: Any, kind: str) -> None:
        # These are GraphQL persisted queries: the hole is in the POST body,
        # not the URL, so every hole comes back from the same address. De-
        # duplicate on content, or holes 2-18 look like repeats and vanish.
        body = json.dumps(payload, indent=2)
        fingerprint = hashlib.sha1(body.encode("utf-8")).hexdigest()
        if fingerprint in seen:
            return
        seen.add(fingerprint)

        (run_dir / f"{len(captured):03d}_{slugify(url)}.json").write_text(body, encoding="utf-8")
        captured.append({"url": url, "kind": kind})
        if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
            print(f"   <- {', '.join(payload['data'].keys())}")

    def on_response(response: Response) -> None:
        if NOISE.search(response.url):
            return
        try:
            payload = response.json()
        except Exception:
            return
        record(response.url, payload, "http")

    ws_log = run_dir / "_ws_frames.jsonl"
    ws_count = [0]

    def decode_frame(payload: Any) -> str | None:
        """Get text out of a frame, compressed or binary though it may be."""
        if isinstance(payload, str):
            return payload
        if not isinstance(payload, (bytes, bytearray)):
            return None
        for attempt in (
            lambda b: b.decode("utf-8"),
            lambda b: zlib.decompress(b).decode("utf-8"),
            lambda b: zlib.decompress(b, -zlib.MAX_WBITS).decode("utf-8"),
            lambda b: gzip.decompress(b).decode("utf-8"),
        ):
            try:
                return attempt(bytes(payload))
            except Exception:
                continue
        return None

    def on_websocket(ws) -> None:
        print(f"   websocket opened: {ws.url[:90]}")

        def handle(payload: Any, direction: str) -> None:
            # Never drop a frame silently: the shot feed streams through here,
            # and an unreadable frame still needs to be visible as evidence.
            ws_count[0] += 1
            text = decode_frame(payload)
            entry: dict[str, Any] = {"direction": direction, "url": ws.url}
            if text is None:
                raw = bytes(payload) if isinstance(payload, (bytes, bytearray)) else b""
                entry.update({"undecodable": True, "bytes": len(raw),
                              "head_hex": raw[:64].hex()})
            else:
                entry["text"] = text[:200_000]
                try:
                    parsed = json.loads(text)
                except Exception:
                    parsed = None
                if parsed is not None:
                    record(ws.url, parsed, f"ws-{direction}")
            with open(ws_log, "a", encoding="utf-8") as handle_:
                handle_.write(json.dumps(entry) + "\n")
            if ws_count[0] % 25 == 0:
                print(f"   ...{ws_count[0]} websocket frames")

        # framesent carries the subscription, which says what to ask for.
        ws.on("framereceived", lambda payload: handle(payload, "received"))
        ws.on("framesent", lambda payload: handle(payload, "sent"))

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
        print("   2. Open the Scorecard, and click hole 1")
        print("   3. Open the AI SHOT COMMENTARY panel -- THIS IS THE ONE")
        print("      THAT MATTERS. Expand it so the lines are visible, and")
        print("      scroll it to the bottom so every shot loads.")
        print("   4. Step through the holes with the > arrow, pausing a")
        print("      moment on each so its shots load")
        print()
        print("  TAKE AS LONG AS YOU LIKE. Nothing is timing you.")
        print("  When you're done -- or want a break -- just CLOSE THE")
        print("  BROWSER WINDOW. Run this again later to add more holes.")
        print("=" * 64 + "\n")

        deadline = time.time() + args.minutes * 60
        while time.time() < deadline and not page.is_closed():
            try:
                page.wait_for_timeout(1_000)
            except Exception:
                break  # window closed mid-wait
        print(f"\nFinished. {len(captured)} new payloads this run.")

        try:
            context.close()
            browser.close()
        except Exception:
            pass

    (run_dir / "_manifest.json").write_text(json.dumps(captured, indent=2), encoding="utf-8")

    payloads = collect_payloads(out)
    print(f"Analysing {len(payloads)} payloads from all runs...")

    shotjson.MIN_ARRAY_SCORE = 2
    shots, commentary = [], []
    for source, payload in payloads:
        for path, records, context_fields in shotjson.find_record_arrays(payload):
            score, fields = find_shots.assess(records)
            if score and len(set(fields) - {"x", "y", "z"}) >= 2:
                shots.append((score, source, records, context_fields, fields))
            score, fields = find_shots.assess_commentary(records)
            if score:
                commentary.append((score, source, records, context_fields, fields))

    def hole_of(row: dict) -> Any:
        for key, value in row.items():
            if shotjson.norm_key(key) in {"holenumber", "holeno", "hole"} and isinstance(value, (int, float)):
                return value
        return None

    def sort_key(row: dict) -> tuple:
        def number(*names):
            for key, value in row.items():
                if shotjson.norm_key(key) in names and isinstance(value, (int, float)):
                    return value
            return 0
        return (number("holenumber", "holeno", "hole"), number("shotnumber", "shotno"))

    wrote = False
    for label, findings, filename in (
        ("shot records", shots, "SHOT_BY_SHOT.csv"),
        ("AI commentary", commentary, "AI_COMMENTARY.csv"),
    ):
        if not findings:
            continue
        # Each hole arrives as its own table, so merge them all rather than
        # keeping only the best-scoring one -- otherwise this is one hole.
        rows, seen_rows = [], set()
        for score, source, records, context_fields, fields in findings:
            for record_ in records:
                row = {**shotjson.flatten(context_fields), **shotjson.flatten(record_)}
                fingerprint = json.dumps(row, sort_keys=True, default=str)
                if fingerprint in seen_rows:
                    continue
                seen_rows.add(fingerprint)
                rows.append(row)

        rows.sort(key=sort_key)
        find_shots.write_csv(rows, HERE / filename)
        holes = sorted({h for h in (hole_of(r) for r in rows) if h is not None})
        print(f"\n{label}: {len(rows)} rows -> {filename}")
        print(f"  fields: {findings[0][4]}")
        if holes:
            print(f"  holes : {', '.join(str(int(h)) for h in holes)}")
            missing = [h for h in range(1, 19) if h not in holes]
            if missing:
                print(f"  MISSING holes {', '.join(str(h) for h in missing)}"
                      f" -- run this again and step through just those.")
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
