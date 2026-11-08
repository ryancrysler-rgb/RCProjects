"""Official facts for the field study, read from the field capture's run folders.

Writes official.json: every player's card (all rounds), finish, playing order of
holes per round (from the commentary feed's holeOrder), the course-stats panel
(par and field average per round/hole) and each hole's played length per round
(the median tee position across the field, metres).
"""
import json
import statistics
import sys
from pathlib import Path

cap = Path(sys.argv[1])
out = Path(sys.argv[2])
players, holestats, tees = {}, {}, {}


def feeds(payload):
    data = (payload.get("payload") or {}).get("data") or payload.get("data") or {}
    return data.items() if isinstance(data, dict) else []


for run in sorted(cap.glob("run_*")):
    info_path = run / "_run_info.json"
    if not info_path.exists() or not (run / "_manifest.json").exists():
        continue
    info = json.loads(info_path.read_text())
    rnd, team = str(info["round"]), info.get("team")
    for path in sorted(run.glob("[0-9]*.json")):
        try:
            payload = json.loads(path.read_text())
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        for op, v in feeds(payload):
            if op.endswith("GroupScores") and isinstance(v, list):
                for g in v:
                    for pl in g.get("players") or []:
                        pid = str(pl.get("id"))
                        rec = players.setdefault(pid, {"name": f"{pl.get('firstName', '')} {pl.get('lastName', '')}".strip(),
                                                       "team": g.get("teamId"), "cards": {}, "order": {}})
                        rec["toPar"] = (g.get("toPar") or {}).get("value", rec.get("toPar"))
                        tp = g.get("tournamentPosition") or {}
                        if tp.get("displayValue"):
                            rec["pos"], rec["posValue"] = tp["displayValue"], tp.get("value")
                        rec["status"] = g.get("status", rec.get("status"))
                        for rs in g.get("roundScores") or []:
                            holes = {str(h["holeNumber"]): h.get("holeStrokes") for h in rs.get("holes") or [] if h.get("holeStrokes")}
                            cur = rec["cards"].get(str(rs.get("roundNo")), {})
                            if len(holes) >= len(cur):
                                rec["cards"][str(rs.get("roundNo"))] = holes
            elif op.endswith("HoleStats") and isinstance(v, dict):
                holestats.setdefault(str(v.get("roundNo")), {})[str(v.get("holeNo"))] = {"par": v.get("holePar"), "avg": v.get("averageHoleScore")}
            elif op.endswith("GolfMedia3DShots") and isinstance(v, list):
                for r in v:
                    if r.get("strokeNo") == 0 and isinstance(r.get("distanceToPin"), (int, float)):
                        tees.setdefault(rnd, {}).setdefault(str(r.get("holeNo")), []).append(r["distanceToPin"])
            elif op.endswith("GolfCommentary") and isinstance(v, dict):
                order = sorted((h.get("holeOrder"), h.get("holeNo")) for h in v.get("holes") or [] if h.get("holeOrder") is not None)
                pids = {str(s.get("playerId")) for h in v.get("holes") or [] for s in h.get("shots") or [] if s.get("playerId")}
                if len(order) == 18 and len(pids) == 1:
                    pid = pids.pop()
                    players.setdefault(pid, {"name": None, "team": team, "cards": {}, "order": {}})["order"][str(v.get("roundNo"))] = [h for _, h in order]

json.dump({"players": players, "holestats": holestats,
           "tee": {r: {h: statistics.median(v) for h, v in hs.items()} for r, hs in tees.items()}},
          open(out, "w"), indent=1)
done = [p for p in players.values() if all(len(p["cards"].get(str(r), {})) == 18 for r in range(1, 5))]
print(f"{len(players)} players on cards, {len(done)} with four complete rounds; panel rounds "
      f"{ {r: len(v) for r, v in holestats.items()} }; tee lengths { {r: len(v) for r, v in tees.items()} }")
