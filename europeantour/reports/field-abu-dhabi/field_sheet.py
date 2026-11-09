"""The field vs the house rules — one sheet, 816×1056, on the house sheet stylesheet (the Raw gold's head).

Every figure is read from summary.json (aggregate.py over the engine-graded rounds). The prose is checked against
the figures by asserts before anything is written. Tour lines are the RC Greenlight tour shot study's own values
(tour-benchmarks.js STUDY, winners · field), printed beside ours and never used to lower a standard.
"""
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).parent
S = json.loads((HERE / sys.argv[1]).read_text())
OUT = Path(sys.argv[2])
GOLD = Path("/home/user/rc-greenlight/deliverables/Laurie Canter - LIV Indy Tournament Summary - Raw.html")
G = S["groups"]
W, T, R, FLD = G["winner"], G["top10"], G["rest"], G["field"]
MINUS = "−"


def two(v):
    return str(Decimal(repr(v)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def pct(f):
    a, b = f
    return None if not b else int(Decimal(repr(100 * a / b)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def pct_s(f):
    p = pct(f)
    return "—" if p is None else f"{p}%"


def frac_s(f):
    return f"{f[0]}/{f[1]}"


def signed(v):
    return ("+" if v > 0 else MINUS if v < 0 else "") + two(abs(v))


def share(g, k):
    return [g["levels"].get(k, 0), sum(g["levels"].values())]


# ---------------------------------------------------------------- checks the prose leans on
assert W["players"] == 1 and T["players"] == 12 and R["players"] == 55 and S["complete"] == 68
assert W["rounds"] == 4 and T["rounds"] == 48 and R["rounds"] == 220
assert pct(T["fw"]) == 66 and pct(R["fw"]) == 66
assert (pct(T["gir"]), pct(R["gir"])) == (85, 77)
assert (pct(T["gFw"]), pct(R["gFw"])) == (92, 85) and W["gFw"] == [42, 43]
assert (pct(T["resetBad"]), pct(R["resetBad"])) == (11, 20) and W["resetBad"] == [0, 5]
assert W["par5"] == [16, 16] and (pct(T["par5"]), pct(R["par5"])) == (91, 86)
assert (round(100 * T["in6"][0] / T["in6"][1], 1), round(100 * R["in6"][0] / R["in6"][1], 1)) == (93.3, 92.6)
assert W["p40"] == [0, 5] and W["over6"] == [0, 4]
assert W["p5third121"][0] == 0 and T["p5third121"] == [21, 0.0] and R["p5third121"] == [99, 0.23]
assert (T["bogeysPerRound"], R["bogeysPerRound"]) == (1.69, 2.72)
assert share(T, "HIGH STRESS") == [13, 48] and share(R, "HIGH STRESS") == [107, 220]
assert FLD["vsFieldByLevel"]["LOW STRESS"][0] == 2.83 and FLD["vsFieldByLevel"]["HIGH STRESS"][0] == -2.0

# ---------------------------------------------------------------- rows
# label, measured as, (rahm, top10, rest) strings, tour, which way is better ('hi' | 'lo' | None), the numbers to tint on
ROWS = []


def row(label, measure, f, tour="", better="hi", kind="pct"):
    if kind == "pct":
        vals = [pct_s(g[f]) for g in (W, T, R)]
        cmp = (pct(T[f]), pct(R[f]))
        thr = 5
    elif kind == "num":
        vals = [two(g[f]) for g in (W, T, R)]
        cmp = (T[f], R[f])
        thr = 0.25
    else:   # a precomputed tuple
        vals, cmp, thr = f
    tint = None
    if better and None not in cmp:
        d = (cmp[0] - cmp[1]) if better == "hi" else (cmp[1] - cmp[0])
        tint = "good" if d >= thr else ("weak" if d <= -thr else None)
    ROWS.append((label, measure, vals, tour, tint))


def head(text):
    ROWS.append((text, None, None, None, None))


head("The five non-negotiables")
row("01 Lay back and you hit the fairway", "Greens from the fairway", "gFw", "82% · 78%")
row("", "Greens from the rough", "gRough", "65% · 52%")
row("02 Wedges always find the green", "Chips and bunker shots on the green", "chips", "")
row("", "Rounds with one off the green", "chipMissRounds", "26% · 40%", "lo")
row("03 Never leave 40–74 yards", "Leaves in 40–74 yd a round", "dzPerRound", "", "lo", "num")
row("", "Greens from 40–74 yd", "b4074", "")
row("04 Carry by 15, or lay back by 15", "Rounds with no penalty stroke", "noPenaltyRounds", "91% · 74%")
row("05 Choose to play stress free", "Rounds graded HIGH stress", ([pct_s(share(g, "HIGH STRESS")) for g in (W, T, R)],
                                                                   (pct(share(T, "HIGH STRESS")), pct(share(R, "HIGH STRESS"))), 5), "", "lo", "raw")
row("", "Over par after six holes", "over6", "9% · 27%", "lo")
head("House rules, ranked (v18.1)")
row("1 Inside 6 feet is sacred", "Holed inside 6 ft", "in6", "")
row("", "Holed from 3–6 ft", "in36", "90% · 84%")
row("2 Every par 5 on the green in three", "Par 5s on the green in 3 or fewer", "par5", "90% · 83%")
row("3 Approach inside 40 feet", "Regulation approaches on the green, under 40 ft", "app40", "")
row("", "Three-putts when the first putt is 40 ft+", "p40", "11% · 15%", "lo")
row("4 Beyond 24 feet, the target is the leave", "First putts of 24 ft+ left within 10%", "lv24", "")
row("5 Short game finishes inside 6 feet", "Chips and bunker shots finishing inside 6 ft", "sg6", "")
row("6 Never escape a bad lie with a driver or fairway wood", "Penalty holes a round (no club in the feed)", "penHolesPerRound", "0.1 · 0.4", "lo", "num")
row("7 Own one band", "Greens from 75–100 yd", "b75", "85% · 79%")
row("8 Birdie conversion", "Birdie or better ÷ greens hit", "bc", "42% · 33%")
row("9 The reset hole", "Bogey or worse after a bogey", "resetBad", "4% · 19%", "lo")
p121 = lambda g: ("none" if not g["p5third121"][0] else (signed(g["p5third121"][1]) if g["p5third121"][1] else "0.00"))
row("10 A par-5 lay-up stays in the fairway, as close as it allows",
    f'Par-5 thirds from 121 yd+, to par ({T["p5third121"][0]} and {R["p5third121"][0]} shots)',
    ([p121(g) for g in (W, T, R)], (T["p5third121"][1], R["p5third121"][1]), 0.15), "F 0.00 fwy", "lo", "raw")
head("House stats and mistakes")
row("Clutch Factor Ball Striking", "Par or better after trouble", "cfbs", "85% · 62%")
row("Clutch Factor Putting", "Par-saving putts from 5 ft+ holed", "cfp", "58% · 45%")
row("Clutch Factor Response", "No bogey in the 3 holes after one", "cfrStop", "81% · 56%")
row("Clutch Factor Damage Control", "Trouble held to bogey or better", "cfdc", "98.5% · 88.5%")
row("Mistakes", "Bogeys or worse a round", "bogeysPerRound", "1.4 · 2.6", "lo", "num")
row("", "Doubles or worse a round", "doublesPerRound", "", "lo", "num")

# ---------------------------------------------------------------- html pieces
TINT = {"good": "background:color-mix(in oklch,var(--g500) 16%,transparent);color:var(--g700);font-weight:700;",
        "weak": "background:color-mix(in oklch,var(--bog) 18%,transparent);color:var(--bogT);font-weight:700;"}

trs = []
for label, measure, vals, tour, tint in ROWS:
    if measure is None:
        trs.append(f'<div class="tr th2"><span class="kick" style="color:var(--g800);font-size:7.5px;font-weight:700;">{label}</span></div>')
        continue
    v = vals
    trs.append(
        '<div class="tr">'
        f'<span class="rl">{label}</span><span class="rm">{measure}</span>'
        f'<span class="rv" style="color:var(--g800);font-weight:700;">{v[0]}</span>'
        f'<span class="rv" style="{TINT.get(tint, "")}">{v[1]}</span>'
        f'<span class="rv">{v[2]}</span>'
        f'<span class="rt">{tour}</span></div>')
table = f'''  <div style="margin-top:7px;flex:1;display:flex;flex-direction:column;min-height:0;background:#fff;border:1px solid var(--bs);border-radius:12px;overflow:hidden;">
    <div class="tr" style="background:var(--g950);color:var(--g200);flex:0 0 auto;padding-top:4px;padding-bottom:4px;">
      <span class="kick" style="font-size:7px;">Rule</span><span class="kick" style="font-size:7px;">Measured as</span>
      <span class="kick rv" style="font-size:7px;color:var(--lime4);">Rahm</span><span class="kick rv" style="font-size:7px;color:var(--g200);">Top 10</span>
      <span class="kick rv" style="font-size:7px;color:var(--g200);">11th on</span><span class="kick rt" style="font-size:7px;color:var(--g200);white-space:nowrap;">Tour W · F</span></div>
    <div style="flex:1;display:flex;flex-direction:column;min-height:0;">
      {"".join(trs)}
    </div>
  </div>'''

# header
tile = lambda k, v, sub, vcol, lime=False: (
    f'<div style="text-align:center;background:{"color-mix(in oklch,var(--lime) 16%,transparent)" if lime else "rgba(255,255,255,.05)"};'
    f'border:1px solid {"color-mix(in oklch,var(--lime) 34%,transparent)" if lime else "var(--bi)"};border-radius:9px;padding:6px 12px;">'
    f'<div class="kick" style="color:var({"--g200" if lime else "--g300"});margin-bottom:5px;">{k}</div>'
    f'<div style="font-family:var(--fd);font-weight:800;font-size:21px;color:{vcol};line-height:.85;">{v}</div>'
    f'<div class="mono" style="font-size:9px;color:var(--g200);margin-top:3px;">{sub}</div></div>')
gold = GOLD.read_text(encoding="utf-8")
lockup_start = gold.index('<div style="display:flex;align-items:center;gap:11px;">')
lockup_end = gold.index('<div class="kick" style="color:var(--g300);text-align:right;line-height:1.6;">Tournament Summary')
lockup = gold[lockup_start:lockup_end]
header = f'''  <div style="background:var(--g950);color:#fff;padding:13px 28px 11px;position:relative;overflow:hidden;flex:0 0 auto;">
    <svg viewBox="0 0 816 150" fill="none" aria-hidden="true" class="bleed" style="position:absolute;inset:0;width:100%;height:100%;opacity:.1;pointer-events:none;"><ellipse cx="660" cy="30" rx="360" ry="180" stroke="#5BD891" stroke-width="1"/><ellipse cx="660" cy="30" rx="230" ry="120" stroke="#B4EA32" stroke-width="1"/></svg>
    <div style="position:relative;display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      {lockup}<div class="kick" style="color:var(--g300);text-align:right;line-height:1.6;">Field Study · Raw<br><span style="color:var(--g200);">Distances in yards · putting in feet</span></div>
    </div>
    <div style="position:relative;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;">
      <div style="width:max-content;">
        <div class="kick" style="color:var(--lime);font-size:9.5px;margin-bottom:6px;white-space:nowrap;">Abu Dhabi Aldar Championship · Yas Links · Final · Par 72</div>
        <h1 style="font-family:var(--fd);font-weight:800;font-size:34px;line-height:.88;letter-spacing:-.03em;">The field vs <span style="color:var(--g400);">the house rules</span></h1>
        <div class="mono" style="font-size:10px;color:var(--g200);margin-top:6px;">{S["complete"]} players · {FLD["rounds"] + W["rounds"]} rounds · house rules v18.1</div>
      </div>
      <div style="display:flex;gap:7px;flex:0 0 auto;">
        {tile("Winner", "−23", "Rahm · 265", "var(--lime4)", lime=True)}
        {tile("Top 10", two(T["scoring"]), "a round · 12", "#fff")}
        {tile("11th on", two(R["scoring"]), "a round · 55", "#fff")}
      </div>
    </div>
  </div>'''

read = f'''  <div style="background:var(--g950);color:#fff;border-radius:12px;padding:10px 14px 9px;flex:0 0 auto;position:relative;overflow:hidden;">
    <div class="kick" style="color:var(--lime4);margin-bottom:4px;">The read</div>
    <div style="font-family:var(--fd);font-weight:800;font-size:15px;line-height:1.12;">The top 10 hit no more fairways than the rest — both 66%. They out-scored them with
      <span style="color:var(--lime4);">greens from the fairway</span> and <span style="color:var(--lime4);">the hole after a bogey</span>.</div>
    <div class="mono" style="font-size:8.6px;color:var(--g200);margin-top:5px;line-height:1.35;">Greens from the fairway {pct_s(T["gFw"])} against {pct_s(R["gFw"])} · bogey or worse after a bogey {pct_s(T["resetBad"])} against {pct_s(R["resetBad"])} ·
      HIGH-stress rounds {pct_s(share(T, "HIGH STRESS"))} against {pct_s(share(R, "HIGH STRESS"))} · holed inside 6 ft {round(100 * T["in6"][0] / T["in6"][1], 1)}% against {round(100 * R["in6"][0] / R["in6"][1], 1)}%: the short putter did not separate them.
      The winner: every par 5 on in three ({frac_s(W["par5"])}), no bogey after a bogey ({frac_s(W["resetBad"])}), never over par after six holes.</div>
    <div style="margin-top:6px;padding-top:5px;border-top:1px solid var(--bi);font-size:10px;color:var(--lime4);font-weight:600;">
      The shots to coach: from the fairway, the green is the target; every par 5 is planned on in three; after a bogey, the fairway club and the middle of the green.</div>
  </div>'''

lv = lambda g, k: share(g, k)
def stress_bar(name, g):
    n = sum(g["levels"].values())
    segs = "".join(f'<div style="width:{100 * g["levels"][k] / n:.1f}%;background:{c};"></div>' for k, c in
                   (("LOW STRESS", "var(--g500)"), ("MEDIUM STRESS", "var(--bog)"), ("HIGH STRESS", "var(--red)")))
    return (f'<div style="display:flex;align-items:center;gap:6px;"><span class="mono" style="font-size:8px;color:var(--ink5);width:44px;">{name}</span>'
            f'<div style="flex:1;height:7px;display:flex;border-radius:3px;overflow:hidden;background:var(--paper2);">{segs}</div>'
            f'<span class="mono" style="font-size:7.5px;color:var(--ink5);width:92px;text-align:right;">{g["levels"]["LOW STRESS"]} · {g["levels"]["MEDIUM STRESS"]} · {g["levels"]["HIGH STRESS"]} of {n}</span></div>')
by = FLD["vsFieldByLevel"]
stress = f'''  <div style="display:flex;gap:8px;margin-top:7px;flex:0 0 auto;">
    <div style="flex:1.25;background:#fff;border:1px solid var(--bs);border-radius:12px;padding:7px 12px;display:flex;flex-direction:column;gap:4px;">
      <div class="kick" style="color:var(--ink4);">Rule 05 · stress level by round · <span style="color:var(--g700);">low</span> · <span style="color:var(--bogT);">medium</span> · <span style="color:var(--redT);">high</span></div>
      {stress_bar("Rahm", W)}{stress_bar("Top 10", T)}{stress_bar("11th on", R)}
    </div>
    <div style="flex:1;background:#fff;border:1px solid var(--bs);border-radius:12px;padding:7px 12px;display:flex;flex-direction:column;justify-content:center;gap:4px;">
      <div class="kick" style="color:var(--ink4);">Strokes against the field's average, by level · the 67 others</div>
      <div style="display:flex;gap:6px;">
        {"".join(f'<div style="flex:1;text-align:center;background:color-mix(in oklch,var(--lime) 8%,#fff);border-radius:8px;padding:3px;"><div class="kick" style="color:var(--ink5);font-size:7px;">{k.split()[0].capitalize()} · {by[k][1]} rds</div><div style="font-family:var(--fd);font-weight:800;font-size:16px;color:{"var(--g700)" if by[k][0] > 0 else "var(--redT)"};line-height:1;">{signed(by[k][0])}</div></div>' for k in ("LOW STRESS", "MEDIUM STRESS", "HIGH STRESS"))}
      </div>
    </div>
  </div>'''

foot = (
    "Data = DP World Tour shot-by-shot feed (Event Centre), every player, every round, every hole: 280 rounds and 19,680 shots, every round reconciled to "
    "its official card on all 18 holes · graded by the RC Greenlight engine at house rules v18.1 (Rev 362: the DP World reader, metrics.js, nn-grade, the "
    "Raw builder’s ladder) · <b>68 players with four graded rounds</b> (Calum Hill R1 and Kristoffer Reitan R4 each have a tee shot with no position, "
    "so neither week is counted) · groups: Rahm · the 12 others who finished T10 or better · the 55 who finished 11th or worse · tint = the top 10 better "
    "(green) or worse (amber) than 11th on by 5 points or more, 0.25 a round on counts · <b>tour column</b> = RC Greenlight tour shot study, 2026 season "
    "(35 winners, 313 others, PGA TOUR), W = winners · F = field, beside ours, never a standard · <b>read by the RC Greenlight reader (Rev 362), no patch:</b> the "
    "feed’s DoubleBogeyOrWorse takes the card’s par; a stroke-and-distance row ends on the tee; a water ball’s drop row is the penalty stroke; a penalty "
    "with no position leaves the ball where it lies (McIlroy R1 H12: his two-shot Rule 8.1b penalty, an 8 on the card); OWA, OBU, ODO, OUK and OTF read Other (owner, "
    "2026-11-08) · a lone ball the feed flags provisional is the ball played · NOT MEASURED (no clubs, pins or hazard lines in the feed): the lay-back itself, "
    "the full-wedge tier of rule 02, rule 04’s margin (penalty-free rounds stand in, as in the tour study), rule 6’s club, front pin (11), the long side / open side (12), The Check, the go line and the short "
    "par 4 (both need clubs) · rule 05 levels are the engine’s, by round, never averaged."
)
footer = f'''  <div style="display:flex;align-items:center;justify-content:space-between;padding:4px 0 5px;gap:10px;flex:0 0 auto;">
    <div class="mono" style="font-size:6.3px;color:var(--ink4);line-height:1.26;">{foot}</div>
    <div class="kick" style="color:var(--ink5);text-align:right;line-height:1.6;flex:0 0 auto;white-space:nowrap;">RC Greenlight · Raw<br>Abu Dhabi · Field study</div>
  </div>'''

head_html = gold[: gold.find("<body")]
head_html = head_html.replace("<title>Laurie Canter · LIV Golf Indianapolis · Tournament Summary — RC Greenlight</title>",
                              "<title>Abu Dhabi · The field vs the house rules — RC Greenlight</title>")
extra = (".tr{display:grid;grid-template-columns:186px 1fr 52px 46px 52px 90px;align-items:center;padding:0 10px;font-size:9px;"
         "line-height:1;flex:1;min-height:0;border-bottom:1px solid color-mix(in oklch,var(--ink9) 7%,transparent);}"
         ".tr.th2{background:var(--paper1);flex:1;}"
         ".tr .rl{font-family:var(--fd);font-weight:700;font-size:9px;line-height:1.02;color:var(--ink9);}"
         ".tr .rm{color:var(--ink7);font-size:9px;}"
         ".tr .rv{font-family:var(--fm);font-size:9.5px;text-align:center;color:var(--ink7);align-self:stretch;display:flex;align-items:center;justify-content:center;}"
         ".tr .rt{font-family:var(--fm);font-size:8.5px;text-align:right;color:var(--ink5);}\n")
head_html = head_html.replace("@media print", extra + "@media print")
html = (head_html + '<body>\n<div class="desk">\n<div class="sheet" data-screen-label="Abu Dhabi field study">\n\n'
        + header + '\n\n  <div style="flex:1;padding:8px 28px 0;display:flex;flex-direction:column;min-height:0;">\n\n'
        + read + "\n\n" + stress + "\n\n" + table + "\n\n" + footer + "\n\n  </div>\n</div>\n</div>\n</body>\n</html>\n")
OUT.write_text(html, encoding="utf-8")
print("wrote", OUT.name, len(html))
