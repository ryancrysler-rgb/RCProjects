#!/usr/bin/env python3
"""Turn captured websocket frames into a shot-by-shot spreadsheet.

Two subscriptions carry the data and each holds half the picture:

  subscribeToGolfMedia3DShots         ball positions -- hole, stroke, x/z,
                                      surface, distance to pin
  subscribeToGolfTournamentTeamsShotFeed
                                      the event feed -- shot number, time,
                                      surface moved from, hole score

The event feed carries no hole number (each frame covers one hole), so the
positions lead and events are joined onto them by stroke number and the
distances, which both feeds report identically.
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

import find_shots

HERE = Path(__file__).parent

METRES_TO_YARDS = 1.0936132983377078

# Confirmed against what the site displays for these shots. The codes are not
# simple abbreviations of the display names -- OST reads as Rough, not
# anything starting "ST" -- so the rest stay raw in the lieCode columns until
# each is checked on the site. Guessing here would quietly corrupt the lie,
# which is the column most worth trusting.
SURFACES = {
    "OTB": "Tee",
    "OFW": "Fairway",
    "OGR": "Green",
    "OST": "Rough",       # confirmed: hole 1 tee shot
}


def surface(code: str | None) -> str:
    return SURFACES.get(code, "") if code else ""


def yards(metres: float | None) -> float | None:
    return round(metres * METRES_TO_YARDS, 1) if isinstance(metres, (int, float)) else None


def run_round(run_dir: Path) -> str:
    """Which round a capture folder holds, recorded when it was captured."""
    info = run_dir / "_run_info.json"
    if info.exists():
        try:
            return str(json.loads(info.read_text(encoding="utf-8")).get("round") or "?")
        except Exception:
            pass
    return "?"


def load_feeds(captured: Path) -> tuple[list[dict], list[tuple[str, list[dict]]]]:
    """Return ball positions and event frames, each tagged with its round.

    Grouping matters twice over: an event carries no hole number, but every
    event in one frame shares a hole; and no record carries a round at all,
    so the round comes from the folder it was captured into.
    """
    positions, event_frames = [], []
    for run_dir in sorted(captured.glob("run_*")):
        if not run_dir.is_dir():
            continue
        round_no = run_round(run_dir)
        for path in sorted(run_dir.glob("*.json")):
            if path.name.startswith("_"):
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(payload, dict):
                continue
            data = (payload.get("payload") or {}).get("data") or {}
            for record in data.get("subscribeToGolfMedia3DShots") or []:
                positions.append({**record, "_round": round_no})
            frame = data.get("subscribeToGolfTournamentTeamsShotFeed") or []
            if frame:
                event_frames.append((round_no, frame))
    return positions, event_frames


def event_key(shot_no, shot_distance, distance_to_pin) -> tuple:
    """Join key shared by both feeds: stroke number plus its two distances."""
    def near(value):
        return round(value, 4) if isinstance(value, (int, float)) else None
    return (shot_no, near(shot_distance), near(distance_to_pin))


def main() -> int:
    positions, event_frames = load_feeds(HERE / "captured")
    if not positions:
        print("No 3D shot records found. Run GET SHOT BY SHOT first.")
        try:
            input("\nPress Enter to close... ")
        except EOFError:
            pass
        return 1

    # Work out each event frame's hole by matching one of its shots to a
    # position record, then key every event in that frame by (hole, shot).
    positions_by_key = {
        (p["_round"], *event_key(p.get("strokeNo"), p.get("shotDistance"), p.get("distanceToPin"))): p
        for p in positions
    }
    by_hole_shot: dict[tuple, dict] = {}
    unplaced = 0
    for round_no, frame in event_frames:
        hole = None
        for event in frame:
            match = positions_by_key.get(
                (round_no, *event_key(event.get("shotNo"), event.get("shotDistance"), event.get("distanceToPin")))
            )
            if match and match.get("holeNo"):
                hole = match["holeNo"]
                break
        if hole is None:
            unplaced += 1
            continue
        for event in frame:
            by_hole_shot.setdefault((round_no, hole, event.get("shotNo")), {}).update(event)

    rows, seen = [], set()
    for record in positions:
        stroke = record.get("strokeNo")
        # strokeNo 0 is where the ball started, not a shot that was played.
        if stroke in (None, 0):
            continue
        player = record.get("player") or {}
        event = by_hole_shot.get((record["_round"], record.get("holeNo"), stroke), {})

        row = {
            "round": record["_round"],
            "player": player.get("displayName"),
            "playerId": player.get("id"),
            "teamId": record.get("teamId"),
            "hole": record.get("holeNo"),
            "shot": stroke,
            "shotDistance_yds": yards(record.get("shotDistance")),
            "distanceToPin_yds": yards(record.get("distanceToPin")),
            "shotDistance_m": round(record.get("shotDistance"), 2) if isinstance(record.get("shotDistance"), (int, float)) else None,
            "distanceToPin_m": round(record.get("distanceToPin"), 2) if isinstance(record.get("distanceToPin"), (int, float)) else None,
            "lieAfterShot": surface(record.get("surfaceTypeCode")),
            "lieAfterShotCode": record.get("surfaceTypeCode"),
            "lieBeforeShot": surface(event.get("prevSurfaceTypeCode")),
            "lieBeforeShotCode": event.get("prevSurfaceTypeCode"),
            "ballHoled": record.get("ballHoled"),
            "eventType": event.get("eventType"),
            "holeScore": event.get("holeScore"),
            "timestamp": event.get("timestamp"),
            "isProvisional": record.get("isProvisional"),
            "isBallDrop": record.get("isBallDrop"),
            "x": record.get("x"),
            "z": record.get("z"),
            "seqNum": record.get("seqNum"),
        }
        fingerprint = (row["round"], row["hole"], row["shot"], row["seqNum"])
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        rows.append(row)

    rows.sort(key=lambda r: (r["round"], r["hole"] or 0, r["shot"] or 0))
    out = HERE / "SHOT_BY_SHOT.csv"
    find_shots.write_csv(rows, out)

    matched = sum(1 for r in rows if r["eventType"])
    print(f"{len(rows)} shots -> {out.name}")
    print(f"  player : {rows[0]['player']} (team {rows[0]['teamId']})")
    print(f"  events : {matched}/{len(rows)} shots matched to the event feed")
    if unplaced:
        print(f"  note   : {unplaced} event frame(s) could not be placed on a hole")

    for round_no in sorted({r["round"] for r in rows}):
        in_round = [r for r in rows if r["round"] == round_no]
        holes = sorted({r["hole"] for r in in_round if r["hole"]})
        missing = [h for h in range(1, 19) if h not in holes]
        line = f"  round {round_no}: {len(in_round):3d} shots, {len(holes)} holes"
        print(line + (f"  MISSING {missing}" if missing else ""))
    try:
        input("\nPress Enter to close... ")
    except EOFError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
