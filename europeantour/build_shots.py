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

# The site's own surfaceTypes table names Fairway, Green, Rough, Tee and
# Native Area, and those map cleanly onto these codes. The rest of its list
# (Fringe, Semi Rough, three kinds of bunker, Cart Path, Rock Outline...)
# cannot be told apart from two letters with any confidence -- ORO could be
# Rough or Rock Outline -- so unmapped codes are left raw in lieCode rather
# than guessed at.
SURFACES = {
    "OTB": "Tee",
    "OFW": "Fairway",
    "OGR": "Green",
    "ORO": "Rough",
    "ONA": "Native Area",
}


def surface(code: str | None) -> str:
    return SURFACES.get(code, "") if code else ""


def yards(metres: float | None) -> float | None:
    return round(metres * METRES_TO_YARDS, 1) if isinstance(metres, (int, float)) else None


def load_feeds(captured: Path) -> tuple[list[dict], list[list[dict]]]:
    """Return ball positions, and event frames kept as frames.

    Grouping matters: an event carries no hole number, but every event in one
    frame belongs to the same hole, so one identifiable event dates the rest.
    """
    positions, event_frames = [], []
    for path in sorted(captured.glob("run_*/*.json")):
        if path.name.startswith("_"):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        data = (payload.get("payload") or {}).get("data") or {}
        positions += data.get("subscribeToGolfMedia3DShots") or []
        frame = data.get("subscribeToGolfTournamentTeamsShotFeed") or []
        if frame:
            event_frames.append(frame)
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
        event_key(p.get("strokeNo"), p.get("shotDistance"), p.get("distanceToPin")): p
        for p in positions
    }
    by_hole_shot: dict[tuple, dict] = {}
    unplaced = 0
    for frame in event_frames:
        hole = None
        for event in frame:
            match = positions_by_key.get(
                event_key(event.get("shotNo"), event.get("shotDistance"), event.get("distanceToPin"))
            )
            if match and match.get("holeNo"):
                hole = match["holeNo"]
                break
        if hole is None:
            unplaced += 1
            continue
        for event in frame:
            by_hole_shot.setdefault((hole, event.get("shotNo")), {}).update(event)

    rows, seen = [], set()
    for record in positions:
        stroke = record.get("strokeNo")
        # strokeNo 0 is where the ball started, not a shot that was played.
        if stroke in (None, 0):
            continue
        player = record.get("player") or {}
        event = by_hole_shot.get((record.get("holeNo"), stroke), {})

        row = {
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
        fingerprint = (row["hole"], row["shot"], row["seqNum"])
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        rows.append(row)

    rows.sort(key=lambda r: (r["hole"] or 0, r["shot"] or 0))
    out = HERE / "SHOT_BY_SHOT.csv"
    find_shots.write_csv(rows, out)

    holes = sorted({r["hole"] for r in rows if r["hole"]})
    matched = sum(1 for r in rows if r["eventType"])
    print(f"{len(rows)} shots -> {out.name}")
    print(f"  player : {rows[0]['player']} (team {rows[0]['teamId']})")
    print(f"  holes  : {len(holes)} ({min(holes)}-{max(holes)})")
    print(f"  events : {matched}/{len(rows)} shots matched to the event feed")
    if unplaced:
        print(f"  note   : {unplaced} event frame(s) could not be placed on a hole")
    missing = [h for h in range(1, 19) if h not in holes]
    if missing:
        print(f"  MISSING holes: {missing}")
    try:
        input("\nPress Enter to close... ")
    except EOFError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
