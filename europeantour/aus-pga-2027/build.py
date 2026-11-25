"""Cam Smith · Australian PGA · one round, graded FROM THE SCORECARD (no shot tracker at this event), against the house rules
where a card can measure them, and against every player who had finished the round when he finished (owner 2026-11-25: "we are
the source. Let's build a report with everything we can get for Cam including versus the field with his score card" · "compare to
as many players as possible that are finished when he finishes").
usage: build.py DATADIR ROUND OUT.html"""
import json, sys, html, datetime

d, RND, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lb = json.load(open(f"{d}/leaderboard.json"))
cards = {int(k): v for k, v in json.load(open(f"{d}/scorecards.json")).items() if v}
PAR = [4, 4, 4, 4, 4, 4, 3, 5, 3, 4, 5, 4, 4, 5, 3, 4, 5, 3]   # the site's Par row (front 35, back 37, 72); checked below
try:
    row = json.load(open(f"{d}/par_row.json")).get("text", "")
    nums = [int(x) for x in row.split() if x.isdigit()][:20]
    site = nums[0:9] + nums[10:19]
    if len(site) == 18 and site != PAR: raise SystemExit("PAR ROW DISAGREES: " + row)
except FileNotFoundError:
    pass
assert sum(PAR) == 72

def holes(pid):
    c = cards.get(pid)
    if not c: return None
    r = next((r for r in c["Rounds"] if r["RoundNo"] == RND), None)
    if not r: return None
    s = [h["Strokes"] for h in sorted(r["Holes"], key=lambda h: h["HoleNo"])]
    return s if len(s) == 18 and all(x and x > 0 for x in s) else None

players = {p["PlayerId"]: p for p in lb["Players"]}
cam = [p for p in lb["Players"] if p["LastName"].upper() == "SMITH" and p["FirstName"].lower().startswith("cam")]
assert len(cam) == 1, "Cameron Smith not on the leaderboard"
cam = cam[0]; CID = cam["PlayerId"]
C = holes(CID)
if C is None: raise SystemExit("Cam's card is not complete for round %d" % RND)
# the card's own total and the leaderboard agree
rc = next(r for r in cards[CID]["Rounds"] if r["RoundNo"] == RND)
if rc.get("Strokes") and rc["Strokes"] != sum(C): raise SystemExit("card total %s != holes %d" % (rc["Strokes"], sum(C)))
# ScoreClass check: every finished card's classes agree with PAR (catches a wrong par row)
bad = 0
for pid, c in cards.items():
    r = next((r for r in c["Rounds"] if r["RoundNo"] == RND), None)
    for h in (r or {}).get("Holes", []):
        sc = (h.get("ScoreClass") or "").lower(); n = h["Strokes"]; p = PAR[h["HoleNo"] - 1]
        if not n: continue
        want = {"birdie": p - 1, "bogey": p + 1, "par": p, "eagle": p - 2, "double-bogey": p + 2}.get(sc)
        if want is not None and want != n: bad += 1
if bad: raise SystemExit("%d holes disagree with the par row" % bad)

field = {pid: holes(pid) for pid in cards if pid != CID}
field = {pid: s for pid, s in field.items() if s}
N = len(field)
assert N >= 10, "only %d finished players" % N
avg = [sum(s[i] for s in field.values()) / N for i in range(18)]
first_tee = bool(cam.get("FirstTee", True))
# the leader among the finished players (lowest round), first by the leaderboard's order on a tie; none when Cam leads
lowest = min(sum(x) for x in field.values())
LEAD = None
if lowest < sum(C):
    for p in sorted(lb["Players"], key=lambda p: p.get("SortOrder") or 999):
        if p["PlayerId"] in field and sum(field[p["PlayerId"]]) == lowest:
            LEAD = (p["FirstName"].title() + " " + p["LastName"].title(), field[p["PlayerId"]]); break
order = list(range(18)) if first_tee else list(range(9, 18)) + list(range(9))

def tp(x): return "E" if x == 0 else ("%+d" % x)
def tpf(x):
    if abs(x) < 0.05: return "E"
    return ("%+.1f" % x)
def vs(x):   # golf sign: + = better than the field
    return ("+%.2f" % x) if x > 0.004 else ("−%.2f" % -x if x < -0.004 else "0.00")

to_par = sum(C) - 72
diff = [avg[i] - C[i] for i in range(18)]
won = sum(1 for x in diff if x > 1e-9); lost = sum(1 for x in diff if x < -1e-9)
strokes_vs = sum(diff)
field_avg_score = sum(sum(s) for s in field.values()) / N
rank_better = sum(1 for s in field.values() if sum(s) < sum(C))
rank_tied = sum(1 for s in field.values() if sum(s) == sum(C))
pos = cam.get("PositionDesc") or ""

def bytype(p):
    ix = [i for i in range(18) if PAR[i] == p]
    me = sum(C[i] - PAR[i] for i in ix); fl = sum(avg[i] - PAR[i] for i in ix)
    return len(ix), me, fl
types = {p: bytype(p) for p in (3, 4, 5)}

seq = [order[k:k + 6] for k in (0, 6, 12)]
stretches = []
for s in seq:
    me = sum(C[i] - PAR[i] for i in s); fl = sum(avg[i] - PAR[i] for i in s)
    stretches.append((s[0] + 1, s[-1] + 1, me, fl))

birdies = sum(1 for i in range(18) if C[i] < PAR[i]); bogeys = sum(1 for i in range(18) if C[i] > PAR[i])
doubles = sum(1 for i in range(18) if C[i] >= PAR[i] + 2)
f_bird = sum(sum(1 for i in range(18) if s[i] < PAR[i]) for s in field.values()) / N
f_bog = sum(sum(1 for i in range(18) if s[i] > PAR[i]) for s in field.values()) / N
stress = "HIGH" if doubles >= 2 else ("MEDIUM" if doubles >= 1 or bogeys >= 3 else "LOW")
resets = [(order[k], order[k + 1]) for k in range(17) if C[order[k]] > PAR[order[k]]]
reset_kept = sum(1 for a, b in resets if C[b] <= PAR[b])
par5 = [(i + 1, C[i], avg[i]) for i in range(18) if PAR[i] == 5]
hard = sorted(range(18), key=lambda i: avg[i] - PAR[i], reverse=True)[:3]
easy = sorted(range(18), key=lambda i: avg[i] - PAR[i])[:3]
best = sorted(range(18), key=lambda i: diff[i], reverse=True)[:3]
worst = sorted(range(18), key=lambda i: diff[i])[:3]

def cls(n, p):
    return "eag" if n <= p - 2 else "bir" if n == p - 1 else "par" if n == p else "bog" if n == p + 1 else "dbl"

def card_rows(rng, label):
    cells_h = "".join(f"<th>{i+1}</th>" for i in rng)
    cells_p = "".join(f"<td>{PAR[i]}</td>" for i in rng)
    cells_c = "".join(f'<td><span class="sc {cls(C[i],PAR[i])}">{C[i]}</span></td>' for i in rng)
    cells_f = "".join(f"<td>{avg[i]:.2f}</td>" for i in rng)
    cells_v = "".join(f'<td class="{"pos" if diff[i]>0 else "neg" if diff[i]<0 else ""}">{vs(diff[i])}</td>' for i in rng)
    tot = lambda a: sum(a[i] for i in rng)
    return (f"<tr class='hd'><th>{label}</th>{cells_h}<th>Tot</th></tr>"
            f"<tr><th>Par</th>{cells_p}<td><b>{tot(PAR)}</b></td></tr>"
            f"<tr class='cam'><th>Cam</th>{cells_c}<td><b>{tot(C)}</b></td></tr>"
            + (f"<tr><th>Leader</th>" + "".join(f'<td><span class="sc {cls(LEAD[1][i],PAR[i])}">{LEAD[1][i]}</span></td>' for i in rng) + f"<td><b>{sum(LEAD[1][i] for i in rng)}</b></td></tr>" if LEAD else "") +
            f"<tr><th>Field avg</th>{cells_f}<td><b>{tot(avg):.1f}</b></td></tr>"
            f"<tr><th>vs field</th>{cells_v}<td><b>{vs(sum(diff[i] for i in rng))}</b></td></tr>")

kept = lambda ok: '<span class="pill ok">Kept</span>' if ok else '<span class="pill no">Not kept</span>'
reading = '<span class="pill rd">Reading</span>'
nm = lambda why: f'<span class="nm">{html.escape(why)}</span>'

strong = max(types.items(), key=lambda kv: kv[1][2] - kv[1][1])
next_up = min(types.items(), key=lambda kv: kv[1][2] - kv[1][1])
st_ok = [s for s in stretches if s[2] <= 0]

LOCK = """<div class="lock" style="--lk:1.15">
  <svg class="mark" viewBox="0 0 64 64" fill="none" aria-hidden="true">
    <ellipse cx="30" cy="36" rx="24" ry="18" stroke="currentColor" stroke-width="2.4" opacity=".3"></ellipse>
    <ellipse cx="31" cy="35" rx="16.5" ry="12" stroke="currentColor" stroke-width="2.4" opacity=".55"></ellipse>
    <ellipse cx="32" cy="34" rx="9" ry="6.5" stroke="currentColor" stroke-width="2.4"></ellipse>
    <circle cx="32.5" cy="33.5" r="2.6" fill="currentColor"></circle>
    <path d="M32.5 33.5 L40 9" stroke="#EAF3DF" stroke-width="2.6" stroke-linecap="round"></path>
    <path d="M40 9 L54 13.5 L41.6 18.6 Z" fill="#B4EA32"></path>
  </svg>
  <div>
    <div class="wm">RCGreen<b>light</b></div>
    <div class="desc">Every number ends with a choice</div>
  </div>
</div>"""

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime("%a %d %b %Y, %-I:%M %p ET")
H = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Cam Smith · Aussie PGA R{RND}</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,600;0,800;1,800&family=Hanken+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{{--g950:#0E2018;--g900:#163024;--g800:#1B5238;--g700:#1E7048;--g600:#2A9460;--g400:#5BD891;--g300:#97E9BB;--g200:#C5F2D7;--lime:#B4EA32;
--paper:#FBF9F3;--paper2:#E9E2D1;--ink9:#101914;--ink7:#33433B;--ink5:#5F6E64;--bogT:#9A5B12;--redT:#A3262A;
--fd:"Archivo",system-ui,sans-serif;--fs:"Hanken Grotesk",system-ui,sans-serif;--fm:"JetBrains Mono",ui-monospace,monospace}}
@page{{size:8.5in 11in;margin:0}}
html,body{{margin:0;background:var(--paper);color:var(--ink9);font-family:var(--fs)}}
section{{width:8.5in;height:11in;box-sizing:border-box;position:relative;overflow:hidden;page-break-after:always;background:var(--paper)}}
.top{{background:var(--g950);color:#fff;padding:22px 34px 18px;display:flex;justify-content:space-between;align-items:center}}
.lock{{--lk:1;display:flex;align-items:center;gap:calc(13px * var(--lk));flex:0 0 auto}}
.lock .mark{{width:calc(38px * var(--lk));height:calc(38px * var(--lk));flex:0 0 auto;color:var(--g300,#97E9BB)}}
.lock .wm{{font-family:var(--fd,"Archivo",sans-serif);font-weight:800;font-size:calc(20px * var(--lk));letter-spacing:-.02em;line-height:.92;color:#fff}}
.lock .wm b{{color:var(--g400,#5BD891);font-weight:800}}
.lock .desc{{font-family:var(--fm,"JetBrains Mono",monospace);font-size:calc(8px * var(--lk));letter-spacing:.18em;text-transform:uppercase;color:var(--g200,#C5F2D7);margin-top:calc(6px * var(--lk));padding-top:calc(6px * var(--lk));border-top:1px solid rgba(255,255,255,.16)}}
.lock .desc .s{{color:var(--lime,#B4EA32);margin:0 calc(4px * var(--lk))}}
.ttl{{text-align:right}} .ttl .k{{font-family:var(--fm);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--g300)}}
.ttl h1{{font-family:var(--fd);font-style:italic;font-weight:800;font-size:30px;margin:4px 0 0;letter-spacing:-.01em;color:#fff}}
.body{{padding:20px 34px}}
.hero{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}}
.tile{{background:#fff;border:1px solid var(--paper2);padding:10px 12px}}
.tile .l{{font-family:var(--fm);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink5)}}
.tile .v{{font-family:var(--fd);font-weight:800;font-size:28px;color:var(--g900);margin-top:2px}}
.tile .s{{font-size:11.5px;color:var(--ink7)}}
h2{{font-family:var(--fd);font-style:italic;font-weight:800;font-size:17px;margin:14px 0 6px;color:var(--g900)}}
table.card{{width:100%;border-collapse:collapse;font-family:var(--fm);font-size:11px;margin-bottom:8px}}
table.card th,table.card td{{border:1px solid var(--paper2);padding:3px 2px;text-align:center}}
table.card tr.hd th{{background:var(--g900);color:#fff}} table.card th:first-child{{text-align:left;padding-left:6px;width:62px;color:var(--ink7);background:#fff}}
table.card tr.hd th:first-child{{background:var(--g900);color:#fff}}
.sc{{display:inline-block;min-width:18px;padding:1px 2px;font-weight:600}}
.sc.bir{{border-radius:50%;border:1.6px solid var(--g700);color:var(--g700)}} .sc.eag{{border-radius:50%;border:3px double var(--g700);color:var(--g700)}}
.sc.bog{{border:1.6px solid var(--bogT);color:var(--bogT)}} .sc.dbl{{border:3px double var(--redT);color:var(--redT)}}
td.pos{{color:var(--g700);font-weight:600}} td.neg{{color:var(--redT);font-weight:600}}
table.g{{width:100%;border-collapse:collapse;font-size:12.5px}} table.g td,table.g th{{border-bottom:1px dashed var(--paper2);padding:6px 4px;text-align:left;vertical-align:top}}
table.g th{{font-family:var(--fm);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink5);font-weight:500}}
.pill{{display:inline-block;font-family:var(--fm);font-size:10px;padding:2px 7px;transform:skewX(-10deg);font-weight:600}}
.pill.ok{{background:var(--g200);color:var(--g900)}} .pill.no{{background:#F6DADA;color:var(--redT)}} .pill.rd{{background:var(--paper2);color:var(--ink7)}}
.nm{{font-size:11.5px;color:var(--ink5)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.note{{font-size:11px;color:var(--ink5);line-height:1.45}}
.call{{background:var(--g950);color:#fff;padding:12px 16px;margin-top:12px}} .call b{{color:var(--lime)}} .call p{{margin:4px 0;font-size:13px;line-height:1.45}}
.foot{{position:absolute;left:34px;right:34px;bottom:26px;font-family:var(--fm);font-size:9px;color:var(--ink5);letter-spacing:.06em}}
</style></head><body>
<section>
<div class="top">{LOCK}<div class="ttl"><div class="k">Australian PGA · Round {RND} · Raw, from the card</div><h1>Cameron Smith</h1></div></div>
<div class="body">
<div class="hero">
 <div class="tile"><div class="l">Score</div><div class="v">{sum(C)} <span style="font-size:18px">({tp(to_par)})</span></div><div class="s">started on the {"1st" if first_tee else "10th"}</div></div>
 <div class="tile"><div class="l">vs the field</div><div class="v">{vs(strokes_vs).replace("+","+") }</div><div class="s">strokes vs the {N} who had finished (avg {field_avg_score:.2f})</div></div>
 <div class="tile"><div class="l">Holes won – lost</div><div class="v">{won}–{lost}</div><div class="s">beat / lost to the field's average on the hole</div></div>
 <div class="tile"><div class="l">Place when he finished</div><div class="v">{html.escape(str(pos)) or "—"}</div><div class="s">{rank_better} of {N} finished players lower, {rank_tied} level</div></div>
</div>
<h2>The card against the field</h2>
<table class="card">{card_rows(range(0,9),"Hole")}</table>
<table class="card">{card_rows(range(9,18),"Hole")}</table>
<div class="note">{("Leader = " + html.escape(LEAD[0]) + ", " + str(sum(LEAD[1])) + " (" + tp(sum(LEAD[1])-72) + "), the low round among the finished players; Cam " + ("%d" % (sum(C)-sum(LEAD[1]))) + " behind. ") if LEAD else "Cam holds the low round among the finished players. "}Field average = every player who had finished round {RND} when Cam finished ({N} players). vs field: + = better than the field's average on that hole (golf sign).</div>
<div class="two">
<div><h2>By par</h2><table class="g"><tr><th>Holes</th><th>Cam</th><th>Field</th><th>vs field</th></tr>
{"".join(f"<tr><td>Par {p}s ({n})</td><td>{tp(me)}</td><td>{tpf(fl)}</td><td>{vs(fl-me)}</td></tr>" for p,(n,me,fl) in types.items())}
</table></div>
<div><h2>Every six holes, in playing order</h2><table class="g"><tr><th>Stretch</th><th>Cam</th><th>Field</th><th>Level or better</th></tr>
{"".join(f"<tr><td>Holes {a}–{b}</td><td>{tp(me)}</td><td>{tpf(fl)}</td><td>{kept(me<=0)}</td></tr>" for a,b,me,fl in stretches)}
</table></div>
</div>
<div class="two">
<div><h2>Where he gained on the field</h2><table class="g">{"".join(f"<tr><td>Hole {i+1} (par {PAR[i]})</td><td>{C[i]}</td><td>field {avg[i]:.2f}</td><td>{vs(diff[i])}</td></tr>" for i in best)}</table></div>
<div><h2>Where the field gained on him</h2><table class="g">{"".join(f"<tr><td>Hole {i+1} (par {PAR[i]})</td><td>{C[i]}</td><td>field {avg[i]:.2f}</td><td>{vs(diff[i])}</td></tr>" for i in worst)}</table></div>
</div>
<div class="call"><p><b>The round in one line.</b> {tp(to_par)}, {vs(strokes_vs)} strokes on the field, {won} holes won and {lost} lost. Strongest: the par {strong[0]}s ({vs(strong[1][2]-strong[1][1])} on the field). Next to master: the par {next_up[0]}s ({vs(next_up[1][2]-next_up[1][1])}).</p></div>
</div>
<div class="foot">No shot tracker at this event: graded from the official hole-by-hole card. Independent analysis by RC Greenlight · built {now}</div>
</section>
<section>
<div class="top">{LOCK}<div class="ttl"><div class="k">Australian PGA · Round {RND} · Page 2</div><h1>Cam vs the house rules</h1></div></div>
<div class="body">
<div class="note" style="margin-bottom:6px">Every rule a scorecard can measure is graded literally. A rule that needs the shots reads "no shot data this week".</div>
<h2>The five non-negotiables</h2>
<table class="g"><tr><th>Rule</th><th>Grade</th><th>From the card</th></tr>
<tr><td>5 · Choose to play stress free</td><td><span class="pill {"ok" if stress=="LOW" else "rd" if stress=="MEDIUM" else "no"}">{stress}</span></td><td>{doubles} double{"s" if doubles!=1 else ""} or worse, {bogeys} bogey{"s" if bogeys!=1 else ""} or worse · every six holes level or better: {len(st_ok)} of 3 · <span class="nm">the four shot measures and three-putts need shot data</span></td></tr>
<tr><td>4 · Carry by 15, or lay back by 15</td><td>{reading}</td><td>penalty strokes on the card: {cards[CID].get("TotalPenalty", 0) or 0} <span class="nm">(the rule's stand-in; hazard lines need the shots)</span></td></tr>
<tr><td colspan="3" class="nm">Need the shots (no shot data this week): 1 · Lay back and you hit the fairway · 2 · Wedges always find the green · 3 · Never leave 40–74 yards (37–68 m)</td></tr>
</table>
<h2>The house rules, by rank</h2>
<table class="g"><tr><th>Rule</th><th>Grade</th><th>From the card</th></tr>
<tr><td>2 · Every par 5 on the green in three</td><td>{reading}</td><td>par 5s: {", ".join(f"hole {h} {s} (field {a:.2f})" for h,s,a in par5)} · {nm("on the green in three needs the shots")}</td></tr>
<tr><td>5 · Take the bogey before the double</td><td>{kept(doubles==0)}</td><td>doubles or worse: {doubles} · {nm("the bad-lie club needs the shots")}</td></tr>
<tr><td>7 · Birdie conversion</td><td>{reading}</td><td>{birdies} birdie{"s" if birdies!=1 else ""} or better (field {f_bird:.1f}) · {nm("the rate needs greens hit")}</td></tr>
<tr><td>9 · The reset hole</td><td>{kept(reset_kept==len(resets)) if resets else '<span class="pill ok">No bogey to reset</span>'}</td><td>{f"par or better on {reset_kept} of {len(resets)} holes after a bogey" if resets else "no bogey on the card"}</td></tr>
<tr><td colspan="3" class="nm">Need the shots (no shot data this week): 1 · Inside 6 feet is sacred · 3 · Approach inside 40 feet · 4 · Beyond 24 feet, the target is the leave · 6 · Short game finishes inside 6 feet · 8 · Long par 4s: bogey is the enemy (hole lengths are not on the card) · 10 · A par-5 lay-up stays in the fairway · 11 · Miss on the long side / open side</td></tr>
</table>
<div class="two">
<div><h2>The field's hardest holes</h2><table class="g">{"".join(f"<tr><td>Hole {i+1} (par {PAR[i]})</td><td>field {tpf(avg[i]-PAR[i])}</td><td>Cam {tp(C[i]-PAR[i])}</td></tr>" for i in hard)}</table></div>
<div><h2>The field's easiest holes</h2><table class="g">{"".join(f"<tr><td>Hole {i+1} (par {PAR[i]})</td><td>field {tpf(avg[i]-PAR[i])}</td><td>Cam {tp(C[i]-PAR[i])}</td></tr>" for i in easy)}</table></div>
</div>
<div class="two"><div><h2>Birdies and bogeys</h2><table class="g"><tr><td>Birdies or better</td><td>Cam {birdies}</td><td>field {f_bird:.1f}</td></tr><tr><td>Bogeys or worse</td><td>Cam {bogeys}</td><td>field {f_bog:.1f}</td></tr></table></div><div></div></div>
</div>
<div class="foot">Bag on file: the Cam Smith yardage sheet (total metres); not used this round (no shots). Independent analysis by RC Greenlight.</div>
</section></body></html>"""
H = H.replace("3 · Never leave 40–74 metres' worth (37–68 m)", "3 · Never leave 40–74 yards (37–68 m)")
open(OUT, "w").write(H)
print("built", OUT, "| Cam", sum(C), tp(to_par), "| field", N, "| vs", round(strokes_vs, 2), "| W-L", won, lost, "| stress", stress)
