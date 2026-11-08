#!/usr/bin/env python3
"""Write one player's rounds as a plain text file, hole by hole.

    python shot_text.py --event abu-dhabi-aldar-championship-2026 --player Puig

Reads SHOT_BY_SHOT_<event>.csv (built by build_shots.py) for the shots and
the commentary, and the captured run folders for what the spreadsheet does not
carry: each hole's par (the official scorecard) and its played length (the
tee position the feed records before the first shot). Writes
reports/<Player> - <event> - shot by shot.txt.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
YD = 1.0936132983377078
WORDS = {-3: "Albatross", -2: "Eagle", -1: "Birdie", 0: "Par", 1: "Bogey", 2: "Double bogey", 3: "Triple bogey"}


def feed(payload, name):
    data = (payload.get("payload") or {}).get("data") or payload.get("data") or {}
    for key, value in data.items():
        if key.endswith(name):
            return value
    return None


def course_facts(event: str, player_id: str):
    """Par and played length per (round, hole), from the captured payloads."""
    par, length = {}, {}
    for run in sorted((HERE / "captured").glob(f"run_*_{event}_r*")):
        info = json.loads((run / "_run_info.json").read_text(encoding="utf-8"))
        rnd = str(info.get("round"))
        for path in sorted(run.glob("[0-9]*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            shots = feed(payload, "GolfMedia3DShots")
            for rec in shots if isinstance(shots, list) else []:
                if str((rec.get("player") or {}).get("id")) == player_id and rec.get("strokeNo") == 0:
                    length[(rnd, rec["holeNo"])] = rec["distanceToPin"] * YD
            groups = feed(payload, "GolfTournamentGroupScores")
            for group in groups if isinstance(groups, list) else []:
                if not any(str(p.get("id")) == player_id for p in group.get("players") or []):
                    continue
                for score in group.get("roundScores") or []:
                    for hole in score.get("holes") or []:
                        if hole.get("holePar"):
                            par[(str(score.get("roundNo")), hole["holeNumber"])] = hole["holePar"]
    return par, length


def yd(v):
    return f"{float(v):.0f} yd"


def ft(v_yd):
    f = float(v_yd) * 3
    if f < 1:
        return f"{f * 12:.0f} in"
    return f"{f:.1f} ft" if f < 10 else f"{f:.0f} ft"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--event", required=True)
    ap.add_argument("--player", required=True, help="Surname (or full name) as in the spreadsheet.")
    args = ap.parse_args()

    sheet = HERE / f"SHOT_BY_SHOT_{args.event}.csv"
    rows = [r for r in csv.DictReader(open(sheet, encoding="utf-8-sig"))
            if args.player.lower() in (r.get("player") or "").lower()]
    if not rows:
        raise SystemExit(f"No shots for {args.player} in {sheet.name}")
    name, player_id = rows[0]["player"], rows[0]["playerId"]
    par, length = course_facts(args.event, player_id)
    title = args.event.replace("-", " ").upper()

    rounds = sorted({r["round"] for r in rows}, key=int)
    totals = []
    body = []
    for rnd in rounds:
        rr = [r for r in rows if r["round"] == rnd]
        holes = sorted({int(r["hole"]) for r in rr})
        rpar = sum(par.get((rnd, h), 0) for h in holes)
        totals.append((len(rr), len(rr) - rpar if len(holes) == 18 and rpar else None))
        head = f"ROUND {rnd} · {len(rr)}" + (f" ({len(rr) - rpar:+d})" if len(holes) == 18 and rpar else f" through {len(holes)} holes")
        body += ["=" * 72, head, "=" * 72]
        for h in holes:
            hs = sorted([r for r in rr if int(r["hole"]) == h], key=lambda r: int(r["shot"]))
            hp, hl, sc = par.get((rnd, h)), length.get((rnd, h)), len(hs)
            result = f"{sc}" + (f" ({WORDS.get(sc - hp, f'{sc - hp:+d}')})" if hp else "")
            body.append(f"\nHole {h} · Par {hp or '?'} · " + (f"{hl:.0f} yd · " if hl else "") + result)
            lie, togo = "Tee", hl
            for r in hs:
                n = r["shot"]
                if r["eventType"] == "Penalty":
                    where = r["lieAfterShot"] or "drop"
                    extra = f" ({float(r['distanceToPin_yds']):.0f} yd)" if r["distanceToPin_yds"] else ""
                    body.append(f"  {n}. Penalty stroke - ball back to the {where.lower()}{extra}")
                    lie = where
                    if r["distanceToPin_yds"]:
                        togo = float(r["distanceToPin_yds"])
                else:
                    putt = lie == "Green"
                    start = (ft(togo) if putt else yd(togo)) if togo is not None else "?"
                    what = "Putt" if putt else ("Tee shot" if lie == "Tee" else f"From {lie.lower()}")
                    if (r["ballHoled"] or "").lower() == "true":
                        body.append(f"  {n}. {what} from {start} - HOLED" if putt else f"  {n}. {what} ({start}) - HOLED")
                    else:
                        left = float(r["distanceToPin_yds"]) if r["distanceToPin_yds"] else None
                        end = r["lieAfterShot"] or "?"
                        lefts = "?" if left is None else (ft(left) if end == "Green" or left < 4 else yd(left))
                        body.append(f"  {n}. {what} from {start} -> {lefts}" if putt else f"  {n}. {what} ({start}) -> {end}, {lefts} left")
                        lie, togo = end, left
                if r.get("commentary"):
                    body.append(f"       \"{r['commentary']}\"")
                if r.get("note"):
                    body.append(f"       [note: {r['note']}]")
        body.append("")

    scores = " · ".join(str(s) for s, _ in totals)
    complete = [tp for _, tp in totals if tp is not None]
    total_line = f"Shot by shot, Round{'s' if len(rounds) > 1 else ''} {', '.join(rounds)} · {scores}"
    if len(complete) == len(totals):
        total_line += f" = {sum(s for s, _ in totals)} ({sum(complete):+d})"
    out = [f"{name.upper()} · {title}", total_line,
           "Source: DP World Tour shot tracker; par from the official scorecard.",
           "Each line: where the shot was played from (and how far from the hole) -> where it finished.",
           "Yards off the green, feet on it. The quoted line under each shot is the site's AI commentary.", ""] + body
    target = HERE / "reports" / f"{name} - {args.event} - shot by shot.txt"
    target.parent.mkdir(exist_ok=True)
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{target.relative_to(HERE)}: {len(out)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
