#!/usr/bin/env python3
"""Capture a whole field: every player, every round, every hole.

    python field_capture.py --event abu-dhabi-aldar-championship-2026 --event-id 1440 \\
        --teams 1-72 --rounds 1-4 --workers 4 --out ../field/abu-dhabi

The tracker numbers its players 1, 2, 3... (its "team" numbers), so the field
is walked by number with no clicking on the leaderboard. Each player-round
opens the tracker on hole 1 and steps through the holes with the tracker's own
next arrow (about 3 seconds a hole), waiting for the holing shot before moving
on. The feeds are written as run folders in <out>/captured, the layout
build_shots.py reads; raw websocket logs are not kept (the decoded payloads
are what the build uses). A number with no player is skipped.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import multiprocessing as mp
import os
import re
import time
from pathlib import Path

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
ADS = re.compile(r"doubleclick|googlesyndication|adservice|safeframe|criteo|teads|prebid|"
                 r"aditude|amazon-adsystem|doubleverify|presage|yellowblue", re.I)
KEEP = ("Media3DShots", "ShotFeed", "Commentary", "GroupScores", "HoleStats", "GolfTournament")


def span(text: str) -> list[int]:
    out = []
    for part in text.split(","):
        a, _, b = part.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def tracker_url(event_id: str, team: int, rnd: int) -> str:
    ctx = json.dumps({"view": "player-detail-hole", "teamNo": str(team), "roundNo": str(rnd), "holeNo": "1"},
                     separators=(",", ":"))
    return (f"https://europeantour.apps.srarena.io/golf/5.x/media-shot-tracker/?eventId={event_id}"
            "&operator=europeantour&theme=default&language=en&env=prod&targetModule=media-shot-tracker"
            "&initialContext=" + base64.b64encode(ctx.encode()).decode())


def worker(jobs, args, log):
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    import snappy_lite
    from playwright.sync_api import sync_playwright

    out = Path(args.out) / "captured"
    with sync_playwright() as pw:
        options = {"headless": True}
        if os.environ.get("HTTPS_PROXY"):
            options["proxy"] = {"server": os.environ["HTTPS_PROXY"]}
        try:
            browser = pw.chromium.launch(**options)
        except Exception:
            import glob
            path = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1]
            browser = pw.chromium.launch(executable_path=path, **options)
        for team, rnd in jobs:
            done = list(out.glob(f"run_*_{args.event}_r{rnd}_t{team:03d}"))
            if done and (done[0] / "_manifest.json").exists():
                continue
            run_dir = out / f"run_{time.strftime('%Y%m%d_%H%M%S')}_{args.event}_r{rnd}_t{team:03d}"
            run_dir.mkdir(parents=True, exist_ok=True)
            seen, files = set(), []
            state = {"player": None, "holed": set(), "holes": set()}

            def record(payload, source):
                body = json.dumps(payload, separators=(",", ":"))
                fp = hashlib.sha1(body.encode()).hexdigest()
                if fp in seen:
                    return
                seen.add(fp)
                name = f"{len(files):04d}_{source}.json"
                (run_dir / name).write_text(body, encoding="utf-8")
                files.append(name)

            def look(payload, source):
                if not isinstance(payload, dict):
                    return
                data = (payload.get("payload") or {}).get("data") or payload.get("data") or {}
                if not isinstance(data, dict) or not any(k in op for op in data for k in KEEP):
                    return
                record(payload, source)
                for op, v in data.items():
                    if "Media3DShots" in op and isinstance(v, list):
                        for r in v:
                            if r.get("teamId") == team:
                                state["holes"].add(r.get("holeNo"))
                                if r.get("ballHoled"):
                                    state["holed"].add(r.get("holeNo"))
                                state["player"] = state["player"] or (r.get("player") or {}).get("displayName")

            def on_response(r):
                if r.request.resource_type in ("xhr", "fetch") and "srarena" in r.url:
                    try:
                        look(r.json(), "http")
                    except Exception:
                        pass

            def on_ws(ws):
                def handle(p):
                    text = p if isinstance(p, str) else snappy_lite.decode_text(bytes(p), partial=True)
                    try:
                        look(json.loads(text), "ws")
                    except Exception:
                        pass
                ws.on("framereceived", handle)

            ctx = browser.new_context(viewport={"width": 1400, "height": 900}, user_agent=UA,
                                      extra_http_headers={"Referer": "https://www.europeantour.com/"})
            ctx.route(ADS, lambda route: route.abort())
            page = ctx.new_page()
            page.on("response", on_response)
            page.on("websocket", on_ws)
            t0 = time.time()
            note = ""
            try:
                page.goto(tracker_url(args.event_id, team, rnd), wait_until="domcontentloaded", timeout=60000)
                end = time.time() + 15
                while 1 not in state["holed"] and time.time() < end:
                    page.wait_for_timeout(200)
                if not state["holes"]:
                    note = "no player at this number"
                else:
                    nxt = page.locator("button").last
                    for hole in range(2, 19):
                        nxt.click(timeout=10000)
                        end = time.time() + 10
                        while hole not in state["holed"] and time.time() < end:
                            page.wait_for_timeout(150)
                        page.wait_for_timeout(350)   # the hole's shot feed and commentary land just after
            except Exception as exc:
                note = f"stopped: {type(exc).__name__}: {str(exc)[:120]}"
            ctx.close()
            (run_dir / "_run_info.json").write_text(json.dumps({
                "event": args.event, "round": str(rnd), "team": team, "player": state["player"],
                "captured": time.strftime("%Y-%m-%d %H:%M:%S"), "method": "field_capture",
                "holes_holed": sorted(h for h in state["holed"] if h)}, indent=1), encoding="utf-8")
            if note == "no player at this number":
                for f in run_dir.iterdir():
                    f.unlink()
                run_dir.rmdir()
            else:
                (run_dir / "_manifest.json").write_text(json.dumps(files), encoding="utf-8")
            with open(log, "a") as fh:
                fh.write(f"team {team:3d} r{rnd}: {state['player'] or '-'} · holed {len(state['holed'])}/18 · "
                         f"{len(files)} payloads · {time.time() - t0:.0f}s {note}\n")
        browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--event", required=True)
    ap.add_argument("--event-id", required=True)
    ap.add_argument("--teams", default="1-72")
    ap.add_argument("--rounds", default="1-4")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    (Path(args.out) / "captured").mkdir(parents=True, exist_ok=True)
    log = str(Path(args.out) / "field_capture.log")
    jobs = [(t, r) for r in span(args.rounds) for t in span(args.teams)]
    chunks = [jobs[i::args.workers] for i in range(args.workers)]
    procs = [mp.Process(target=worker, args=(c, args, log)) for c in chunks]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(open(log).read() if os.path.exists(log) else "no log")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
