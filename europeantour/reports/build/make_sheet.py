"""Jon Rahm · Abu Dhabi Aldar Championship R1-R3 · Tournament Summary · Raw.

Markup and CSS copied from the gold file (Laurie Canter - LIV Indy Tournament
Summary - Raw.html). Every figure is read from the engine outputs in this
folder (figures.json, raw_out.json) and the official panel/leaderboard pulls;
nothing on the sheet is typed by hand except the prose.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
GOLD = Path("/home/user/rc-greenlight/deliverables/Laurie Canter - LIV Indy Tournament Summary - Raw.html")
OUT = Path(sys.argv[1])

F = json.loads((HERE / "figures.json").read_text())
RAW = json.loads((HERE / "raw_out.json").read_text())
LB = json.loads((HERE.parent / "leaderboard_r3.json").read_text())

MINUS = "−"


def signed(v, dp=2):
    s = f"{abs(v):.{dp}f}"
    return ("+" if v > 0 else MINUS if v < 0 else "") + s if round(v, dp) != 0 else f"{0:.{dp}f}"


def to_par(v):
    return "E" if v == 0 else (f"+{v}" if v > 0 else f"{MINUS}{abs(v)}")


# ---------------------------------------------------------------- standings
players = LB["Players"]
me = next(p for p in players if p["LastName"].upper() == "RAHM")
assert me["PositionDesc"] == "1" and not me["IsTie"], me
second = sorted({p["ScoreToPar"] for p in players if p is not me})[0]
lead = second - me["ScoreToPar"]
field_n = len(players)
rounds = {int(n): r for n, r in F["rounds"].items()}
total = sum(r["score"] for r in rounds.values())
total_par = sum(r["toPar"] for r in rounds.values())
assert total == 198 and total_par == me["ScoreToPar"] == -18, (total, total_par)

# ---------------------------------------------------------------- facets
def frac(s):
    a, b = re.findall(r"\d+", str(s))[:2]
    return int(a), int(b)


def wk(key):
    m = t = 0
    for r in rounds.values():
        a, b = frac(r[key])
        m += a
        t += b
    return m, t


fw_m, fw_t = wk("fw")
gir_m, gir_t = wk("gir")
scr_m, scr_t = wk("scr")
bc_m, bc_t = wk("bc")
gd_m, gd_t = wk("goodDrive")
in6_m, in6_t = wk("inside6")
putts = sum(r["putts"] for r in rounds.values())
three_putts = sum(int(r["threePutts"]) for r in rounds.values())
cfp_m = sum(r["cfp"]["made"] for r in rounds.values())
cfp_t = sum(r["cfp"]["att"] for r in rounds.values())
cfb_m = sum(r["cfbs"]["made"] for r in rounds.values())
cfb_t = sum(r["cfbs"]["att"] for r in rounds.values())
cfb_semi = sum(r["cfbs"]["semiClutch"] for r in rounds.values())
cfb_flag = sum(r["cfbs"]["flagged"] for r in rounds.values())
par5 = [h for r in rounds.values() for h in r["par5"]]
par5_under = sum(1 for h in par5 if h["score"] < 5)
par5_topar = sum(h["score"] - 5 for h in par5)
greens_missed = gir_t - gir_m
best_n = min(rounds, key=lambda n: rounds[n]["score"])

ladder = {}
for n in (1, 2, 3):
    for row in RAW[str(n)]["ladder"]:
        d = ladder.setdefault(row["label"], [0, 0])
        d[0] += row["made"]
        d[1] += row["n"]
LADDER_ORDER = ["under 40", "40–74", "75–100", "101–120", "121–140", "141–160", "161–180", "181–200", "201–220", "220+"]
assert list(ladder) == LADDER_ORDER
assert sum(v[0] for v in ladder.values()) == gir_m, "ladder greens must reconcile to GIR"
in160 = [ladder[k] for k in LADDER_ORDER[:6]]
in160_m, in160_t = sum(v[0] for v in in160), sum(v[1] for v in in160)

# ---------------------------------------------------------------- checks the prose leans on
assert (fw_m, fw_t) == (31, 42) and (gir_m, gir_t) == (46, 54) and (scr_m, scr_t) == (5, 8)
assert (in6_m, in6_t) == (43, 47) and three_putts == 1 and putts == 86 and (bc_m, bc_t) == (21, 46)
assert par5_under == 10 and par5_topar == -11 and len(par5) == 12
assert ladder["141–160"] == [7, 9] and ladder["75–100"] == [4, 4] and ladder["161–180"] == [7, 8]
assert ladder["181–200"] == [6, 7] and ladder["220+"] == [4, 4]
assert max(v[1] for v in ladder.values()) == 9 and [k for k, v in ladder.items() if v[1] - v[0] == 2] == ["141–160"]
for h in ("1", "14", "16"):
    hv = F["holes"][h]
    assert [hv["scores"][str(n)] for n in (1, 2, 3)] == [4, 4, 4] and hv["fld"] < hv["par"], h
assert rounds[2]["level"] == "MEDIUM STRESS" and rounds[1]["level"] == rounds[3]["level"] == "LOW STRESS"
assert rounds[2]["bogeys"] == ["H6", "H9", "H12"] and rounds[3]["bogeys"] == ["H4"] and not rounds[1]["bogeys"]
assert all(r["counts"]["doubles"] == 0 for r in rounds.values())
assert [int(frac(r["gir"])[0]) for r in rounds.values()] == [16, 14, 16]
assert [r["toPar"] for r in rounds.values()] == [-7, -5, -6]

# ---------------------------------------------------------------- pieces
def frow(label, value, color):
    return (f'<div class="frow"><span class="l">{label}</span>'
            f'<span class="v" style="color:var(--{color});">{value}</span></div>')


def frow_small(label, value, color):
    return (f'<div class="frow"><span class="l">{label}</span>'
            f'<span class="v" style="color:var(--{color});font-size:10px;">{value}</span></div>')


def chip(label, value, tone="lime"):
    if tone == "lime":
        bg, ink = "color-mix(in oklch,var(--lime) 30%,#fff)", "var(--g800)"
    else:
        bg, ink = "color-mix(in oklch,var(--g500) 20%,#fff)", "var(--g700)"
    return (f'<div class="bl" style="background:{bg};"><span class="kick" style="color:{ink};font-size:7.5px;">{label}</span>'
            f'<span class="mono" style="font-size:9px;color:{ink};font-weight:700;">{value}</span></div>')


def chip2(label, value):
    """The two-line chip the Raw uses for Clutch Factor Ball Striking (its name is too long for a row)."""
    return ('<div class="bl" style="background:color-mix(in oklch,var(--lime) 30%,#fff);flex-direction:column;align-items:flex-start;gap:1px;">'
            f'<span class="kick" style="color:var(--g800);font-size:7.5px;white-space:normal;line-height:1.15;">{label}</span>'
            f'<span class="mono" style="font-size:9px;color:var(--g800);font-weight:700;">{value}</span></div>')


def band_row(label, made, n):
    dz = ' style="color:var(--bogT);font-weight:700;"' if label == "40–74" else ""
    if n == 0:
        return (f'<div class="pb"><span class="pbl"{dz}>{label}'
                f'<span style="color:var(--ink4);font-weight:400;"> ·0</span></span><div class="pbt"><div style="width:0%;"></div></div>'
                '<span class="pbv" style="color:var(--ink4);">—</span></div>')
    pct = round(100 * made / n)
    if pct >= 75:
        bar, ink = "var(--g500)", "var(--g700)"
    elif pct >= 50:
        bar, ink = "var(--bog)", "var(--bogT)"
    else:
        bar, ink = "var(--red)", "var(--redT)"
    shown = "100" if pct == 100 else f"{pct}%"
    lab_style = ' style="color:var(--bogT);font-weight:700;"' if label == "40–74" else ""
    return (f'<div class="pb"><span class="pbl"{lab_style}>{label}<span style="color:var(--ink4);font-weight:400;"> ·{n}</span></span>'
            f'<div class="pbt"><div style="width:{pct}%;background:{bar};"></div></div><span class="pbv" style="color:{ink};">{shown}</span></div>')


def big(value, unit):
    return ('<div style="display:flex;align-items:baseline;gap:5px;margin-bottom:5px;">'
            f'<span style="font-family:var(--fd);font-weight:800;font-size:27px;color:var(--ink9);line-height:.8;">{value}</span>'
            f'<span class="mono" style="font-size:9px;color:var(--ink5);">{unit}</span></div>')


def card(cap, kick, inner):
    return (f'<div class="fcard"><span class="cap" style="background:var(--{cap});"></span>\n'
            f'      <div class="kick" style="color:var(--ink4);margin-bottom:2px;">{kick}</div>\n      {inner}\n    </div>')


# ---------------------------------------------------------------- header
tile = lambda k, v, sub, vcol, lime=False: (
    f'<div style="text-align:center;background:{"color-mix(in oklch,var(--lime) 16%,transparent)" if lime else "rgba(255,255,255,.05)"};'
    f'border:1px solid {"color-mix(in oklch,var(--lime) 34%,transparent)" if lime else "var(--bi)"};border-radius:9px;padding:6px 12px;">'
    f'<div class="kick" style="color:var({"--g200" if lime else "--g300"});margin-bottom:5px;">{k}</div>'
    f'<div style="font-family:var(--fd);font-weight:800;font-size:21px;color:{vcol};line-height:.85;">{v}</div>'
    f'<div class="mono" style="font-size:9px;color:var(--g200);margin-top:3px;">{sub}</div></div>')

round_line = " · ".join(str(rounds[n]["score"]) for n in (1, 2, 3))
header = f'''  <div style="background:var(--g950);color:#fff;padding:13px 28px 11px;position:relative;overflow:hidden;flex:0 0 auto;">
    <svg viewBox="0 0 816 150" fill="none" aria-hidden="true" class="bleed" style="position:absolute;inset:0;width:100%;height:100%;opacity:.1;pointer-events:none;"><ellipse cx="660" cy="30" rx="360" ry="180" stroke="#5BD891" stroke-width="1"/><ellipse cx="660" cy="30" rx="230" ry="120" stroke="#B4EA32" stroke-width="1"/></svg>
    <div style="position:relative;display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
      <div style="display:flex;align-items:center;gap:11px;">
        <svg width="30" height="30" viewBox="0 0 64 64" fill="none" style="color:var(--g300);"><ellipse cx="30" cy="36" rx="24" ry="18" stroke="currentColor" stroke-width="2.4" opacity=".3"/><ellipse cx="31" cy="35" rx="16.5" ry="12" stroke="currentColor" stroke-width="2.4" opacity=".55"/><ellipse cx="32" cy="34" rx="9" ry="6.5" stroke="currentColor" stroke-width="2.4"/><circle cx="32.5" cy="33.5" r="2.6" fill="currentColor"/><path d="M32.5 33.5 L40 9" stroke="#EAF3DF" stroke-width="2.6" stroke-linecap="round"/><path d="M40 9 L54 13.5 L41.6 18.6 Z" fill="#B4EA32"/></svg>
        <div style="width:max-content;">
          <div style="font-family:var(--fd);font-weight:800;font-size:17px;letter-spacing:-.02em;line-height:.9;"><span style="color:#fff;">RCGreen</span><span style="color:var(--g400);">light</span></div>
          <div class="kick" style="color:var(--g200);margin-top:4px;">Performance <span style="color:var(--lime);margin:0 3px;">·</span> Player Intelligence</div>
        </div>
      </div>
      <div class="kick" style="color:var(--g300);text-align:right;line-height:1.6;">Tournament Summary · Raw<br><span style="color:var(--g200);">Distances in yards · putting in feet</span></div>
    </div>
    <div style="position:relative;display:flex;align-items:flex-end;justify-content:space-between;gap:20px;">
      <div style="width:max-content;">
        <div class="kick" style="color:var(--lime);font-size:9.5px;margin-bottom:6px;white-space:nowrap;">Abu Dhabi Aldar Championship · Yas Links · Thru R3 · Par 72</div>
        <h1 style="font-family:var(--fd);font-weight:800;font-size:36px;line-height:.88;letter-spacing:-.03em;">Jon <span style="color:var(--g400);">Rahm</span></h1>
        <div class="mono" style="font-size:10px;color:var(--g200);margin-top:6px;">{round_line}</div>
      </div>
      <div style="display:flex;gap:7px;flex:0 0 auto;">
        {tile("Total", to_par(total_par), str(total), "var(--lime4)")}
        {tile("Standing", me["PositionDesc"], f"of {field_n}", "#fff")}
        {tile("Lead", str(lead), f"of {to_par(second)}", "var(--lime4)", lime=True)}
      </div>
    </div>
  </div>'''

# ---------------------------------------------------------------- facet cards
ott = card("lime", "Off the Tee",
           big(f"{round(100 * fw_m / fw_t)}%", "fairways")
           + frow("Tee shots FIR", f"{fw_m} / {fw_t}", "g700")
           + frow("Club split", '<span style="font-family:var(--fm);font-weight:500;font-size:9px;color:var(--ink5);">not in feed</span>', "ink5")
           + frow("Good drive", f"{gd_m} / {gd_t}", "g700")
           + frow("Tee avg · par 4/5", f'{round(F["tee"]["avg"])} yd', "ink9")
           + chip("Longest", f'{F["tee"]["longest"]["yd"]} yd · R{F["tee"]["longest"]["r"]} H{F["tee"]["longest"]["h"]}'))

app = card("g500", "Approach · GIR (yd)",
           big(f"{gir_m}/{gir_t}", f"GIR · {round(100 * gir_m / gir_t)}%")
           + "".join(band_row(k, *ladder[k]) for k in LADDER_ORDER)
           + chip("Inside 160", f"{in160_m} of {in160_t}", tone="green"))

best = rounds[best_n]
arg = card("g500", "Around the Green",
           big(f"{scr_m}/{scr_t}", "scrambled")
           + frow("Greens missed", str(greens_missed), "ink9")
           + frow("Par 5s under par", f"{par5_under} / {len(par5)}", "g700")
           + frow("Par 5s", to_par(par5_topar), "g700")
           + frow("Three-putts", str(three_putts), "g700")
           + frow("Best round", f'{best["score"]} ({to_par(best["toPar"])}) · R{best_n}', "g700")
           + chip2("Clutch Factor Ball Striking", f"{cfb_m} of {cfb_t} · {cfb_semi} semi"))

def putt_color(p):
    return "g700" if p <= 28 else "bogT"   # the engine's rule-05 putter line: under 29 low stress, 29-31 neutral

putt = card("lime", "Putting · by round",
            big(str(putts), "putts")
            + "".join(frow_small(f"R{n} · {rounds[n]['score']}",
                                 f"{rounds[n]['putts']} putts · {rounds[n]['inside6'].replace(' ', '')}",
                                 putt_color(rounds[n]["putts"])) for n in (1, 2, 3))
            + frow("Clutch Factor Putting", f"{cfp_m} of {cfp_t}", "g700")
            + chip("Birdie conv", f"{bc_m}/{bc_t} · {round(100 * bc_m / bc_t)}%"))

facets = f'''  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;flex:0 0 auto;">
    {ott}
    {app}
    {arg}
    {putt}
  </div>'''

# ---------------------------------------------------------------- two-panel row
def lvl(n):
    word = rounds[n]["level"].split()[0].capitalize()
    col = "var(--lime4)" if word == "Low" else "var(--bog)"
    return (f'<div><div style="font-family:var(--fd);font-weight:800;font-size:20px;color:#fff;line-height:.8;">{rounds[n]["score"]}</div>'
            f'<div class="kick" style="color:var(--g300);margin-top:4px;">R{n}</div>'
            f'<div class="kick" style="color:{col};font-size:7px;margin-top:2px;">{word}</div></div>')

fr = [round(x, 2) for x in F["fieldRound"]]
beat = [rounds[n]["score"] for n in (1, 2, 3)]
gaps = [f"{fr[i] - beat[i]:.2f}" for i in range(3)]
panel = f'''  <div style="display:flex;gap:8px;margin-top:7px;flex:0 0 auto;">
    <div style="flex:1.35;background:var(--g950);color:#fff;border-radius:12px;padding:9px 14px;display:flex;align-items:center;justify-content:space-between;gap:14px;position:relative;overflow:hidden;">
      <div>
        <div class="kick" style="color:var(--lime4);margin-bottom:4px;">Standing thru R3 · {field_n} in the field</div>
        <div style="font-family:var(--fd);font-weight:800;font-size:16px;line-height:1;">Leads <span style="color:var(--lime4);">by {lead}</span> after 54 holes</div>
        <div class="mono" style="font-size:9px;color:var(--g200);margin-top:5px;">Beat the field's scoring average by {gaps[0]}, {gaps[1]} and {gaps[2]}</div>
      </div>
      <div style="flex:0 0 auto;text-align:center;">
        <div class="kick" style="color:var(--g300);font-size:7px;margin-bottom:5px;">Rule 05 · stress level</div>
        <div style="display:flex;gap:14px;">{lvl(1)}{lvl(2)}{lvl(3)}</div>
      </div>
    </div>
    <div style="flex:1;background:#fff;border:1px solid var(--bs);border-radius:12px;padding:8px 12px;display:flex;flex-direction:column;justify-content:center;gap:5px;">
      <div class="kick" style="color:var(--ink4);">Scoring average by par · three rounds</div>
      <div style="display:flex;gap:7px;">
        {"".join(f'<div style="flex:1;text-align:center;background:color-mix(in oklch,var(--lime) 8%,#fff);border-radius:8px;padding:4px 3px;"><div class="kick" style="color:var(--ink5);font-size:7px;">Par {p} · {F["byPar"][str(p)]["holes"]}</div><div style="font-family:var(--fd);font-weight:800;font-size:18px;color:var(--ink9);line-height:.9;">{F["byPar"][str(p)]["avg"]:.2f}</div><div class="mono" style="font-size:7.5px;color:var(--g700);margin-top:2px;">{to_par(F["byPar"][str(p)]["toPar"])} · {F["byPar"][str(p)]["holes"]} holes</div></div>' for p in (3, 4, 5))}
      </div>
    </div>
  </div>'''
assert gaps == ["5.39", "2.86", "3.71"], gaps

# ---------------------------------------------------------------- SWOT
def quad(cap, kick_col, title, sub, dot, items):
    lis = "".join(f'<li style="--d:var(--{dot});"><b style="color:var(--ink9);">{b}</b>{rest}</li>' for b, rest in items)
    return (f'<div class="swot"><span class="cap" style="position:absolute;top:0;left:0;right:0;height:3px;background:var(--{cap});"></span>'
            f'<div style="display:flex;align-items:baseline;gap:6px;margin:1px 0 2px;"><span class="kick" style="color:var(--{kick_col});font-size:9px;font-weight:700;">{title}</span>'
            f'<span style="font-size:8px;color:var(--ink4);">{sub}</span></div><ul>{lis}</ul></div>')

swot = f'''  <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:7px;flex:0 0 auto;">
    {quad("g500", "g700", "Strengths", "what built the −18", "g600", [
        ("Par 5s at 4.08 — eleven under across twelve.", " Ten of the twelve went under par; the field played them at 4.54."),
        ("46 of 54 greens, never fewer than 14 in a round.", " 161–180 went 7 of 8, 181–200 went 6 of 7 and 220+ went 4 of 4."),
        ("50 of 54 holes at par or better — four bogeys, no double.", " One three-putt in 86 putts."),
    ])}
    {quad("bog", "bogT", "Next to master", "where the shots are", "bog", [
        ("43 of 47 holed inside 6 ft — the house line is 100%.", " The 3-footer missed at R2 H9 made the week’s only three-putt and a bogey."),
        ("5 of 8 scrambled.", " Three missed greens became bogey (R2 H6, R2 H12, R3 H4); chips finished inside 6 ft 7 times in 13."),
        ("141–160 went 7 of 9 —", " the busiest band on the ladder and the only one with two misses."),
    ])}
    {quad("lime", "g800", "Opportunities", "what to build on", "g600", [
        ("Leave 75–100, not 40–74.", " 75–100 went 4 of 4; three leaves landed in 40–74 (R2 H14, R3 H10, R3 H18) and all three still found the green."),
        ("Par 4s hold the room: 3.83 across thirty, the field 3.98.", " H1, H14 and H16 have gone 4-4-4 — the field averages under par on all three."),
        ("Target 16 greens on Sunday.", " R1 and R3 found 16 each and went −7 and −6; R2 found 14."),
    ])}
    {quad("red", "redT", "Threats", "what to navigate", "red", [
        ("A one-shot lead:", " −18 against two players at −17 after 54 holes."),
        ("R2 was the one MEDIUM-stress round,", " floored by three bogeys (H6, H9, H12). R1 and R3 both read LOW."),
        ("Two of the four bogeys began with a missed fairway:", " native area at R2 H6; rough, then a stroke-and-distance penalty, at R2 H12. The other nine missed fairways made par or better."),
    ])}
  </div>'''

# ---------------------------------------------------------------- hole table
def score_cell(score, par):
    d = score - par
    if d <= -2:
        bg, st = "color-mix(in oklch,var(--g500) 34%,transparent)", "font-weight:800;color:var(--g800);"
    elif d == -1:
        bg, st = "color-mix(in oklch,var(--g500) 15%,transparent)", "font-weight:700;color:var(--g700);"
    elif d == 1:
        bg, st = "color-mix(in oklch,var(--bog) 15%,transparent)", "font-weight:700;color:var(--bogT);"
    elif d >= 2:
        bg, st = "color-mix(in oklch,var(--red) 15%,transparent)", "font-weight:700;color:var(--redT);"
    else:
        bg, st = None, "font-weight:500;color:var(--ink5);"
    bgs = f"background:{bg};" if bg else ""
    return f'<div class="c" style="align-self:stretch;align-items:center;{bgs}"><span class="mono" style="{st}">{score}</span></div>'


def bar(diff, scale, track="var(--paper2)", tick="var(--ink4)", tick_op=".55", h="8px", total=False):
    w = abs(diff) * scale
    side = "left" if diff >= 0 else "right"
    col = ("var(--lime)" if total else "var(--g500)") if diff >= 0 else "var(--red)"
    if total:
        ink, fs, wid = "var(--lime4)", "11px", "34px"
    else:
        ink = "var(--ink4)" if abs(diff) < 0.05 else ("var(--g700)" if diff > 0 else "var(--redT)")
        fs, wid = "9.5px", "32px"
    return ('<div style="display:flex;align-items:center;"><div style="display:flex;align-items:center;gap:8px;width:100%;padding-right:6px;">'
            f'<div style="position:relative;flex:1;height:{h};background:{track};border-radius:4px;">'
            f'<div style="position:absolute;left:50%;top:-1px;bottom:-1px;width:1px;background:{tick};opacity:{tick_op};"></div>'
            f'<div style="position:absolute;top:1px;bottom:1px;{side}:50%;width:{w:.1f}%;background:{col};border-radius:3px;"></div></div>'
            f'<span class="mono" style="font-weight:700;font-size:{fs};color:{ink};width:{wid};text-align:right;">{signed(diff)}</span></div></div>')


rows = []
fld_cells = []
for h in range(1, 19):
    v = F["holes"][str(h)]
    par = v["par"]
    sc = [v["scores"][str(n)] for n in (1, 2, 3)]
    avg, fld = v["avg"], v["fld"]
    fld_cells.append(round(fld, 2))
    avg_col = "var(--g700)" if avg < par - 1e-9 else ("var(--bogT)" if avg > par + 1e-9 else "var(--ink7)")
    diff = round(fld, 2) - round(avg, 2)
    rows.append(
        '<div class="hr" style="flex:1;border-bottom:1px solid var(--bs);">'
        f'<span class="mono" style="font-weight:700;color:var(--ink7);">{h}</span><span class="mono" style="color:var(--ink5);">{par}</span>'
        + "".join(score_cell(s, par) for s in sc)
        + f'<div class="c" style="align-self:stretch;align-items:center;"><span class="mono" style="font-family:var(--fd);font-weight:800;font-size:11px;color:{avg_col};">{avg:.2f}</span></div>'
        + f'<div class="c" style="align-self:stretch;align-items:center;"><span class="mono" style="color:var(--ink4);font-size:8.5px;">{fld:.2f}</span></div>'
        + bar(diff, 48) + '</div>')
par_total = sum(F["holes"][str(h)]["par"] for h in range(1, 19))
avg_total = total / 3
fld_total = F["fieldTotal"]
fld_cell_sum = sum(fld_cells)
tot_diff = round(fld_total, 2) - round(avg_total, 2)
tot = ('<div class="hr" style="background:var(--g900);color:var(--g200);flex:0 0 auto;padding-top:4px;padding-bottom:4px;">'
       '<span class="kick" style="font-size:7px;">TOT</span>'
       f'<span class="mono c" style="font-size:9px;font-weight:700;">{par_total}</span>'
       + "".join(f'<span class="mono c" style="font-size:9px;font-weight:700;color:var(--lime4);">{rounds[n]["score"]}</span>' for n in (1, 2, 3))
       + f'<span class="c" style="font-family:var(--fd);font-weight:800;color:var(--lime4);font-size:13px;">{avg_total:.2f}</span>'
       + f'<span class="mono c" style="font-size:10px;font-weight:700;color:var(--g300);">{fld_total:.2f}</span>'
       + bar(tot_diff, 12, track="var(--g800)", tick="var(--g300)", tick_op=".6", h="9px", total=True) + '</div>')
table = f'''  <div style="margin-top:7px;flex:1;display:flex;flex-direction:column;min-height:0;background:#fff;border:1px solid var(--bs);border-radius:12px;overflow:hidden;">
    <div class="hr" style="background:var(--g950);color:var(--g200);flex:0 0 auto;padding-top:3px;padding-bottom:3px;"><span class="kick" style="font-size:7px;">H</span><span class="kick" style="font-size:7px;">PAR</span><span class="kick c" style="font-size:7px;">R1</span><span class="kick c" style="font-size:7px;">R2</span><span class="kick c" style="font-size:7px;">R3</span><span class="kick c" style="font-size:7px;">JR</span><span class="kick c" style="font-size:7px;">FLD</span><span class="kick" style="font-size:7px;padding-left:2px;">Rahm vs field · scoring avg</span></div>
    <div style="flex:1;display:flex;flex-direction:column;min-height:0;overflow:hidden;">
      {"".join(rows)}
    </div>
    {tot}
  </div>'''

# ---------------------------------------------------------------- footnote
foot = (
    "Data = DP World Tour shot-by-shot feed (Event Centre), Rounds 1–3, each reconciled to the official card "
    f"({' / '.join(str(b) for b in beat)} = {total}) — 18 of 18 holes agree in each of the three rounds; par from the course-stats panel · "
    "figures graded through the house engine (the DP World reader, metrics.js, the Raw builder’s facets and ladder, nn-grade) · "
    "<b>R2 H12 is a stroke-and-distance penalty: the feed returns the ball to the tee, a lie the house reader refuses mid-hole, so R2 was "
    "read with that one penalty row allowed to end on the tee;</b> H12 is off the approach ladder as the ladder rule requires (53 of 54 "
    "approaches banded) · <b>no club field in the feed:</b> tee figures cover all 42 par-4/5 tee balls, with no driver / fairway-wood split · "
    "scoring table = his per-hole average across R1–R3 against the field’s, from the course-stats panel’s per-round averages; "
    "<b>vs-field + means he beat the field on that hole</b> and the totals row is the per-round mean, not a week total"
    + (f"; FLD cells are rounded to 2dp and sum to {fld_cell_sum:.2f} against the {fld_total:.2f} printed" if abs(fld_cell_sum - fld_total) >= 0.005 else "")
    + " · standing from the official leaderboard after R3 (70 players) · R1 H11: the feed flagged neither tee ball of a provisional "
    "pair as played; the first ball hit is taken as played, as the commentary confirms · per-round putting row = putts · holed inside 6 ft · "
    "Clutch Factor Putting and Clutch Factor Ball Striking are each the sum of the three rounds’ engine figures · played yardages from the feed’s tee position · no pin sheet on file."
)
footer = f'''  <div style="display:flex;align-items:center;justify-content:space-between;padding:4px 0 5px;gap:10px;flex:0 0 auto;">
    <div class="mono" style="font-size:6.5px;color:var(--ink4);line-height:1.28;">{foot}</div>
    <div class="kick" style="color:var(--ink5);text-align:right;line-height:1.6;flex:0 0 auto;white-space:nowrap;">RC Greenlight · Raw<br>Abu Dhabi · R1–R3</div>
  </div>'''

# ---------------------------------------------------------------- assemble on the gold head
gold = GOLD.read_text(encoding="utf-8")
head = gold[: gold.find("<body")]
head = head.replace("<title>Laurie Canter · LIV Golf Indianapolis · Tournament Summary — RC Greenlight</title>",
                    "<title>Jon Rahm · Abu Dhabi Aldar Championship · R1–R3 Tournament Summary — RC Greenlight</title>")
old_grid = ".hr{display:grid;grid-template-columns:20px 22px 34px 34px 34px 34px 40px 38px 1fr;"
assert old_grid in head
head = head.replace(old_grid, ".hr{display:grid;grid-template-columns:20px 22px 34px 34px 34px 40px 38px 1fr;")
html = (head + '<body>\n<div class="desk">\n<div class="sheet" data-screen-label="JR Abu Dhabi R1-R3 Tournament Summary">\n\n'
        + header + '\n\n  <div style="flex:1;padding:8px 28px 0;display:flex;flex-direction:column;min-height:0;">\n\n'
        + facets + "\n\n" + panel + "\n\n" + swot + "\n\n" + table + "\n\n" + footer
        + "\n\n  </div>\n</div>\n</div>\n</body>\n</html>\n")
OUT.write_text(html, encoding="utf-8")
print("wrote", OUT, len(html), "chars; FLD cell sum", round(fld_cell_sum, 2), "printed", round(fld_total, 2), "tot diff", tot_diff)
