#!/usr/bin/env python3
"""Discover the JSON API behind a DP World Tour leaderboard page.

The leaderboard HTML ships no scores -- it is a client-side app that pulls
everything over XHR. So instead of parsing HTML, drive a real browser, record
every JSON response, and rank them by how much shot-level data they hold.

    python capture_api.py \
        --url "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1" \
        --click-text Canter --out captured
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from playwright.sync_api import Response, sync_playwright

import shotjson

INTERESTING_URL = re.compile(r"(api|feed|fdapi|sportdata|srarena|imgarena|graphql|\.json)", re.I)

# Consent banners, ad tech and analytics. None of it is golf.
NOISE_HOSTS = (
    "onetrust.com", "doubleverify.com", "gigya.com", "prebid.cloud", "aditude.io",
    "circlelevel.com", "googletagmanager.com", "google-analytics.com", "permutive",
    "chartbeat", "segment.io", "sentry.io", "adservice", "geolocation", "geo-location",
)

# Localisation bundles list every UI label the app can render -- including
# "shotNumber" and "distanceToPin" -- so they score high while containing no
# data whatsoever. Exclude them or they drown out the real feed.
NOISE_PATH = re.compile(r"/locales?/|l10n|/consent/|scripttemplates|translation", re.I)


def is_noise(url: str) -> bool:
    return any(host in url for host in NOISE_HOSTS) or bool(NOISE_PATH.search(url))


def slugify(url: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", url.split("?")[0])[-90:].strip("_")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", required=True, help="Leaderboard page to load.")
    parser.add_argument("--out", default="captured", help="Output directory.")
    parser.add_argument(
        "--click-text",
        action="append",
        default=[],
        help="Text to click after load (repeatable) -- e.g. a player surname, "
             "to trigger the scorecard/shot XHRs. Failures are non-fatal.",
    )
    parser.add_argument("--headed", action="store_true", help="Show the browser window.")
    parser.add_argument("--wait", type=int, default=8000, help="Settle time in ms after each action.")
    parser.add_argument("--har", action="store_true", help="Also record a full HAR of the session.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = Path(args.out)
    bodies = out / "bodies"
    bodies.mkdir(parents=True, exist_ok=True)

    captured: list[dict[str, Any]] = []
    seen: set[str] = set()

    def on_response(response: Response) -> None:
        url = response.url
        if url in seen:
            return
        if is_noise(url):
            return
        content_type = (response.headers or {}).get("content-type", "")
        if "json" not in content_type.lower() and not INTERESTING_URL.search(url):
            return
        try:
            payload = response.json()
        except Exception:
            return
        seen.add(url)

        score, matched = shotjson.score_payload(payload)
        arrays = [(path, len(rows)) for path, rows in shotjson.find_record_arrays(payload)]
        name = f"{len(captured):03d}_{score:03d}_{slugify(url)}.json"
        (bodies / name).write_text(json.dumps(payload, indent=2)[:20_000_000], encoding="utf-8")
        captured.append(
            {
                "url": url,
                "status": response.status,
                "method": response.request.method,
                "score": score,
                "matched_keys": matched,
                "record_arrays": arrays,
                "body_file": str(bodies / name),
            }
        )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headed)
        context_args: dict[str, Any] = {
            "user_agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        }
        if args.har:
            context_args["record_har_path"] = str(out / "session.har")
        context = browser.new_context(**context_args)
        page = context.new_page()
        page.on("response", on_response)

        print(f"loading {args.url}", file=sys.stderr)
        page.goto(args.url, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(args.wait)

        for text in args.click_text:
            try:
                print(f"clicking {text!r}", file=sys.stderr)
                page.get_by_text(text, exact=False).first.click(timeout=10_000)
                page.wait_for_timeout(args.wait)
            except Exception as exc:  # the row may be laid out differently
                print(f"  could not click {text!r}: {type(exc).__name__}", file=sys.stderr)

        context.close()
        browser.close()

    captured.sort(key=lambda item: item["score"], reverse=True)
    (out / "manifest.json").write_text(json.dumps(captured, indent=2), encoding="utf-8")

    print(f"\ncaptured {len(captured)} JSON responses -> {out}/manifest.json")
    print("\nmost shot-like endpoints:")
    for item in captured[:12]:
        print(f"  [{item['score']:3d}] {item['url'][:130]}")
        if item["record_arrays"]:
            preview = ", ".join(f"{path} ({count} rows)" for path, count in item["record_arrays"][:3])
            print(f"        arrays: {preview}")
    if not captured:
        print("  none -- try --headed to check for a consent wall or geo block.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
