#!/usr/bin/env python3
"""Capture a player's rounds with no clicking: the browser drives itself.

capture_shots.py records while a person steps through the holes. This does
the stepping too. The shot tracker on the leaderboard is an Event Centre
page that can be opened straight on any round and hole -- its address
carries the view, team, round and hole -- so this opens it once per hole and
records the same feeds a manual capture would, into the same run folders.

    python auto_capture.py --url <leaderboard URL> --player Rahm --rounds 1,2,3

The event's tracker id and the player's team number are found by opening the
leaderboard and clicking the player, the way a person would; pass --event-id
and --team to skip that. Finishes by running build_shots.py.
"""
from __future__ import annotations

import argparse
import base64
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

import snappy_lite
from capture_shots import ADS, event_slug, slugify, wanted

HERE = Path(__file__).parent
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
TRACKER = ("https://europeantour.apps.srarena.io/golf/5.x/media-shot-tracker/?eventId={event_id}"
           "&operator=europeantour&theme=default&language=en&env=prod"
           "&targetModule=media-shot-tracker&initialContext={context}")


def launch(playwright, headless: bool):
    """Start Chromium, behind the environment's proxy if there is one."""
    options: dict[str, Any] = {"headless": headless}
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        options["proxy"] = {"server": proxy}
    try:
        return playwright.chromium.launch(**options)
    except Exception:
        # A preinstalled browser that does not match this Playwright version.
        for path in sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"), reverse=True):
            try:
                return playwright.chromium.launch(executable_path=path, **options)
            except Exception:
                continue
        raise


def new_context(browser):
    context = browser.new_context(viewport={"width": 1400, "height": 900}, user_agent=UA,
                                  extra_http_headers={"Referer": "https://www.europeantour.com/"})
    context.route(ADS, lambda route: route.abort())
    return context


def find_tracker(browser, url: str, player: str) -> tuple[str, str]:
    """The tracker's event id and the player's team number, from the page.

    Clicking a player on the leaderboard opens the tracker in a frame whose
    address names both.
    """
    context = new_context(browser)
    page = context.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    for selector in ("#onetrust-accept-btn-handler", "button:has-text('Accept All')"):
        try:
            page.click(selector, timeout=5_000)
            break
        except Exception:
            pass
    page.wait_for_timeout(5_000)
    page.get_by_text(player, exact=False).first.click(timeout=15_000)
    for _ in range(30):
        page.wait_for_timeout(1_000)
        for frame in page.frames:
            if "media-shot-tracker" in frame.url and "eventId=" in frame.url:
                query = parse_qs(urlparse(frame.url).query)
                context_json = json.loads(base64.b64decode(query["initialContext"][0]))
                context.close()
                return query["eventId"][0], str(context_json["teamNo"])
    context.close()
    raise RuntimeError(f"Clicked {player} but no shot tracker opened.")


def tracker_url(event_id: str, team: str, round_no: str, hole: int) -> str:
    context = json.dumps({"view": "player-detail-hole", "teamNo": team, "roundNo": str(round_no),
                          "holeNo": str(hole)}, separators=(",", ":"))
    return TRACKER.format(event_id=event_id, context=base64.b64encode(context.encode()).decode())


def capture_round(browser, event: str, url: str, player: str, event_id: str, team: str,
                  round_no: str, holes: list[int]) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_-]+", "-", f"{event}_r{round_no}").strip("-")
    run_dir = HERE / "captured" / f"run_{time.strftime('%Y%m%d_%H%M%S')}_{safe}"
    run_dir.mkdir(parents=True, exist_ok=True)
    round_url = re.sub(r"round=\d+", f"round={round_no}", url)
    (run_dir / "_run_info.json").write_text(json.dumps({
        "event": event, "round": str(round_no), "url": round_url, "player": player,
        "captured": time.strftime("%Y-%m-%d %H:%M:%S"), "method": "auto_capture"}, indent=2),
        encoding="utf-8")

    captured: list[dict[str, Any]] = []
    seen: set[str] = set()
    subscriptions: dict[str, str] = {}
    ws_log = run_dir / "_ws_frames.jsonl"

    def record(source: str, payload: Any, kind: str) -> None:
        body = json.dumps(payload, indent=2)
        fingerprint = hashlib.sha1(body.encode("utf-8")).hexdigest()
        if fingerprint in seen:
            return
        seen.add(fingerprint)
        (run_dir / f"{len(captured):03d}_{slugify(source)}.json").write_text(body, encoding="utf-8")
        captured.append({"url": source, "kind": kind})

    def on_response(response) -> None:
        if wanted(response):
            try:
                record(response.url, response.json(), "http")
            except Exception:
                pass

    def on_websocket(ws) -> None:
        def handle(payload: Any, direction: str) -> None:
            entry: dict[str, Any] = {"direction": direction, "url": ws.url}
            text = payload if isinstance(payload, str) else None
            if isinstance(payload, (bytes, bytearray)):
                raw = bytes(payload)
                entry.update({"bytes": len(raw), "base64": base64.b64encode(raw).decode()})
                text = snappy_lite.decode_text(raw, partial=True)
            if text is None:
                entry["undecodable"] = True
            else:
                entry["text"] = text[:400_000]
                try:
                    parsed = json.loads(text)
                except Exception:
                    parsed = None
                if isinstance(parsed, dict):
                    if direction == "sent" and parsed.get("type") == "start":
                        subscriptions[str(parsed.get("id"))] = parsed.get("operationName", "?")
                    elif direction == "received":
                        operation = subscriptions.get(str(parsed.get("id")))
                        if operation:
                            entry["operation"] = operation
                            parsed["_operation"] = operation
                    record(ws.url, parsed, f"ws-{direction}")
            with open(ws_log, "a", encoding="utf-8") as log:
                log.write(json.dumps(entry) + "\n")

        ws.on("framereceived", lambda payload: handle(payload, "received"))
        ws.on("framesent", lambda payload: handle(payload, "sent"))

    for hole in holes:
        # A fresh page per hole: the tracker subscribes to exactly the round
        # and hole in its address, so nothing from another view leaks in.
        context = new_context(browser)
        page = context.new_page()
        page.on("response", on_response)
        page.on("websocket", on_websocket)
        before = len(captured)
        page.goto(tracker_url(event_id, team, round_no, hole), wait_until="domcontentloaded",
                  timeout=60_000)
        page.wait_for_timeout(7_000)
        try:
            page.get_by_text("AI SHOT COMMENTARY").first.click(timeout=3_000)
            page.wait_for_timeout(2_000)
        except Exception:
            pass
        context.close()
        print(f"   round {round_no} hole {hole:2d}: {len(captured) - before} new payloads", flush=True)

    (run_dir / "_manifest.json").write_text(json.dumps(captured, indent=2), encoding="utf-8")
    return run_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", required=True, help="The event's leaderboard page.")
    parser.add_argument("--player", required=True, help="Player surname, as on the leaderboard.")
    parser.add_argument("--rounds", default="1", help="Comma-separated, e.g. 1,2,3")
    parser.add_argument("--holes", default="1-18", help="e.g. 1-18 or 1,5,9")
    parser.add_argument("--event-id", help="Tracker event id, if already known.")
    parser.add_argument("--team", help="Player's team number at this event, if already known.")
    parser.add_argument("--show", action="store_true", help="Show the browser window.")
    args = parser.parse_args()

    if "-" in args.holes and "," not in args.holes:
        first, last = (int(x) for x in args.holes.split("-"))
        holes = list(range(first, last + 1))
    else:
        holes = [int(x) for x in args.holes.split(",")]
    rounds = [r.strip() for r in args.rounds.split(",") if r.strip()]
    event = event_slug(args.url)

    with sync_playwright() as playwright:
        browser = launch(playwright, headless=not args.show)
        event_id, team = args.event_id, args.team
        if not (event_id and team):
            print(f"Finding {args.player} on the leaderboard...")
            event_id, team = find_tracker(browser, args.url, args.player)
        print(f"{event}: tracker event {event_id}, {args.player} is team {team}\n")
        for round_no in rounds:
            run_dir = capture_round(browser, event, args.url, args.player, event_id, team, round_no, holes)
            print(f"Round {round_no} saved to captured/{run_dir.name}\n")
        browser.close()

    result = subprocess.run([sys.executable, str(HERE / "build_shots.py")], stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, cwd=str(HERE))
    print((result.stdout or "").replace("Press Enter to close...", "").rstrip() or result.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
