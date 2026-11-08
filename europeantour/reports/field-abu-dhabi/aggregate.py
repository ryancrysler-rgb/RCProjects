"""Roll the graded rounds up into the field-study table: winner · top 10 · the rest · whole field."""
import json
import sys
from collections import Counter, defaultdict

rounds = json.load(open(sys.argv[1]))
off = json.load(open(sys.argv[2]))
WINNER = sys.argv[3] if len(sys.argv) > 3 else "493"
res = rounds["results"]

# only players with all four rounds graded go in (the study counts complete weeks)
by_pid = defaultdict(list)
for m in res:
    by_pid[m["pid"]].append(m)
complete = {pid for pid, ms in by_pid.items() if sorted(x["round"] for x in ms) == [1, 2, 3, 4]}
pos = {pid: off["players"][pid].get("posValue") for pid in complete}


def group_of(pid):
    if pid == WINNER:
        return "winner"
    return "top10" if (pos.get(pid) or 99) <= 10 else "rest"


G = {"winner": [], "top10": [], "rest": [], "field": []}
for pid in complete:
    for m in by_pid[pid]:
        G[group_of(pid)].append(m)
        if pid != WINNER:
            G["field"].append(m)


def frac(ms, key, i=0, j=1):
    a = sum(m[key][i] for m in ms)
    b = sum(m[key][j] for m in ms)
    return [a, b]


def ladder_band(ms, label):
    a = b = 0
    for m in ms:
        for lab, made, n in m["ladder"]:
            if lab == label:
                a += made
                b += n
    return [a, b]


def summarize(ms):
    n = len(ms)
    if not n:
        return {}
    lv = Counter(m["level"] for m in ms)
    by_level = defaultdict(list)
    for m in ms:
        by_level[m["level"]].append(m["vsField"])
    rule_state = lambda k: Counter(next((r["state"] for r in m["rules"] if r["n"] == k), None) for m in ms)
    p5_121 = [x for m in ms for x in m["p5third121"]]
    p5_40 = [x for m in ms for x in m["p5third40"]]
    return {
        "rounds": n, "players": len({m["pid"] for m in ms}),
        "scoring": round(sum(m["score"] for m in ms) / n, 2),
        "vsField": round(sum(m["vsField"] for m in ms) / n, 2),
        "in6": frac(ms, "in6"), "in36": frac(ms, "in36"),
        "roundsClean6": [sum(1 for m in ms if m["in6"][0] == m["in6"][1]), n],
        "par5": frac(ms, "par5"),
        "lv24": frac(ms, "lv24"), "three25": frac(ms, "three25"), "p40": frac(ms, "p40"),
        "app40": frac(ms, "app40"),
        "sg6": frac(ms, "sg6"), "bunker6": frac(ms, "bunker6"),
        "chipMissRounds": [sum(m["chipMissRound"] for m in ms), n], "chips": frac(ms, "chips"),
        "dzPerRound": round(sum(m["dz"] for m in ms) / n, 2), "dz": sum(m["dz"] for m in ms),
        "rule3": dict(rule_state(3)), "rule4": dict(rule_state(4)), "rule2": dict(rule_state(2)), "rule1": dict(rule_state(1)),
        "noPenaltyRounds": [sum(1 for m in ms if m["penHoles"] == 0), n],
        "penHolesPerRound": round(sum(m["penHoles"] for m in ms) / n, 2),
        "levels": {k: lv.get(k, 0) for k in ("LOW STRESS", "MEDIUM STRESS", "HIGH STRESS")},
        "vsFieldByLevel": {k: (round(sum(v) / len(v), 2), len(v)) for k, v in by_level.items()},
        "over6": [sum(1 for m in ms if m["after6"] > 0), n],
        "bc": frac(ms, "bc"), "gir": [sum(m["gir"] for m in ms), 18 * n],
        "fw": [sum(m["fw"] for m in ms), sum(m["fwAtt"] for m in ms)],
        "gFw": frac(ms, "gFw"), "gRough": frac(ms, "gRough"),
        "b75": ladder_band(ms, "75–100"), "b4074": ladder_band(ms, "40–74"),
        "resetBad": frac(ms, "resetBad"),
        "bogeysPerRound": round(sum(m["bogeys"] + m["doubles"] for m in ms) / n, 2),
        "doublesPerRound": round(sum(m["doubles"] for m in ms) / n, 2),
        "cfbs": frac(ms, "cfbs"), "cfbsDoubles": sum(m["cfbsDoubles"] for m in ms),
        "cfp": frac(ms, "cfp"), "cfpPerRound": round(sum(m["cfp"][1] for m in ms) / n, 2),
        "cfrStop": frac(ms, "cfr", 0, 2), "cfrAnswer": frac(ms, "cfr", 1, 2),
        "cfdc": frac(ms, "cfdc"),
        "p5third121": [len(p5_121), round(sum(x["toPar"] for x in p5_121) / len(p5_121), 2) if p5_121 else None],
        "p5third40": [len(p5_40), round(sum(x["toPar"] for x in p5_40) / len(p5_40), 2) if p5_40 else None],
        "patched": sorted({(m["name"], m["round"], m["patched"][:90]) for m in ms if m["patched"]}),
    }


out = {"houseRules": rounds["engine"]["houseRules"], "study": rounds["engine"]["study"],
       "complete": len(complete), "groups": {k: summarize(v) for k, v in G.items()},
       "winner": off["players"][WINNER]["name"] if WINNER in off["players"] else None,
       "positions": {off["players"][pid]["name"]: off["players"][pid].get("pos") for pid in complete}}
json.dump(out, open(sys.argv[4] if len(sys.argv) > 4 else "summary.json", "w"), indent=1)
g = out["groups"]
print("players with four graded rounds:", out["complete"], "| winner rounds", g["winner"].get("rounds"), "| top10", g["top10"].get("players"), "| rest", g["rest"].get("players"))
