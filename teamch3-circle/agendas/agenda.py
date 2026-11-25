# Branded one-page agenda for the CH3 Performance Experience at TeamFLO.
# Usage: python3 agenda.py   (edit EVENT below for each date; output PDF goes in this folder)
import html, json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
A = '../teamflo-games/assets/'; e = html.escape

EVENT = {
    'date': 'Wednesday, December 2, 2026',
    'file': 'CH3 Performance Experience - December 2 2026 - Fitzpatrick and Byer.pdf',
    'coaches': ['Claude Harmon III', 'Ryan Crysler'],
    'players': ['Sean Fitzpatrick', 'Bubba Byer'],
    'blocks': [
        ('9:00', '9:45', 'We Focus On Playing', 'Presentation',
         'How TeamCH3 coaches the game: the Non-Negotiables and the House Rules you will play by today.'),
        ('9:45', '12:30', 'Warmup & Playing Assessment', 'On course',
         'Warm up, then head to the course. The coaches walk with you and assess how you play: decisions, routine, scoring and stats.'),
        ('12:30', '1:30', 'Lunch', 'The Floridian',
         'Return from the course and break for lunch.', 'lunch'),
        ('1:30', '4:30', 'Assessment Review & Total Game Improvement', 'TeamFLO',
         'Review your playing assessment with the coaches, then work on total game improvement: the areas that will lower your scores most.'),
    ],
    'bring': 'Your clubs, golf shoes, your questions, recent round reports and playing stats. Dress for the course.',
}

CSS = f"""
@font-face{{font-family:Anton;src:url({A}Anton.ttf)}}
@font-face{{font-family:B;font-weight:600;src:url({A}Barlow600.ttf)}}
@font-face{{font-family:B;font-weight:700;src:url({A}Barlow700.ttf)}}
@page{{size:8.5in 11in;margin:0}}*{{box-sizing:border-box}}
body{{margin:0;font-family:B;font-weight:600;color:#253746;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;height:11in;display:flex;flex-direction:column;overflow:hidden;background:#fff}}
.top{{background:radial-gradient(ellipse at 30% 20%,#2B4152 0%,#253746 50%,#16222E 100%);color:#fff;padding:.45in .6in .4in;border-bottom:6px solid #E04E39}}
.row{{display:flex;justify-content:space-between;align-items:center}}
.row .m{{height:54px}}.row .f{{height:40px}}
.eb{{font:700 13px/1 B;letter-spacing:.26em;color:#F47C67;text-transform:uppercase;margin-top:26px}}
h1{{font:400 58px/.95 Anton;text-transform:uppercase;margin:8px 0 0}}
.dt{{font:700 19px/1.3 B;color:#CDD4DA;margin-top:10px}}.dt b{{color:#fff}}
.who{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}}
.who div{{background:rgba(255,255,255,.07);border-left:4px solid #E04E39;padding:9px 12px;border-radius:3px}}
.who span{{display:block;font:700 10.5px/1 B;letter-spacing:.24em;color:#A6B1BA;text-transform:uppercase;margin-bottom:6px}}
.who p{{margin:0;font:400 20px/1.15 Anton;text-transform:uppercase;letter-spacing:.01em}}
.bd{{flex:1;padding:.3in .6in .2in;display:flex;flex-direction:column}}
.sh{{font:700 12px/1 B;letter-spacing:.26em;color:#C9432F;text-transform:uppercase;margin-bottom:8px}}
.b{{display:grid;grid-template-columns:1.55in 1fr;gap:16px;padding:34px 0;border-bottom:1px solid #E1E6EA}}
.t{{font:400 24px/1 Anton;color:#E04E39}}.t small{{display:block;font:700 11px/1.2 B;color:#7A8A98;letter-spacing:.12em;margin-top:5px}}
.n{{display:flex;justify-content:space-between;align-items:baseline;gap:10px}}
.n h2{{font:400 24px/1.05 Anton;text-transform:uppercase;margin:0;color:#253746}}
.n span{{font:700 10.5px/1 B;letter-spacing:.16em;text-transform:uppercase;color:#fff;background:#253746;padding:5px 7px;border-radius:2px;white-space:nowrap}}
.d{{font-size:15px;line-height:1.4;color:#33475A;margin-top:4px}}
.b.lunch{{background:#F4F6F8;border-radius:4px;border-bottom:0;margin:4px 0;padding:9px 10px}}.b.lunch .t{{color:#7A8A98}}.b.lunch .n span{{background:#7A8A98}}
.bring{{margin-top:auto;background:#F4F6F8;border-left:5px solid #E04E39;padding:11px 14px;font-size:13.5px;line-height:1.4;color:#33475A}}
.bring b{{color:#C9432F;letter-spacing:.18em;font-size:11px;margin-right:8px}}
.ft{{background:#253746;color:#A6B1BA;font:700 10.5px/1 B;letter-spacing:.2em;padding:12px .6in;display:flex;justify-content:space-between;text-transform:uppercase}}.ft b{{color:#F47C67}}
"""
def to24(t, start):
    h, m = map(int, t.split(':')); return h + (12 if h < 8 else 0), m
def ampm(t):
    h, m = to24(t, True); return f"{h if h <= 12 else h - 12}:{m:02d} {'AM' if h < 12 else 'PM'}"
def dur(a, b):
    (h1, m1), (h2, m2) = to24(a, 1), to24(b, 1); mins = (h2 * 60 + m2) - (h1 * 60 + m1)
    return f'{mins // 60} hr {mins % 60} min'.replace(' 0 min', '') if mins >= 60 else f'{mins} min'
ev = EVENT; rows = []
for blk in ev['blocks']:
    a, b, title, loc, desc = blk[:5]; cls = ' ' + blk[5] if len(blk) > 5 else ''
    rows.append(f'<div class="b{cls}"><div class="t">{ampm(a)}<small>to {ampm(b)} · {dur(a, b)}</small></div>'
                f'<div><div class="n"><h2>{e(title)}</h2><span>{e(loc)}</span></div><div class="d">{e(desc)}</div></div></div>')
page = (f'<div class="pg"><div class="top"><div class="row"><img class="m" src="{A}mark.png"><img class="f" src="{A}flor-white.png"></div>'
        f'<div class="eb">TeamCH3 · TeamFLO at the Floridian</div><h1>CH3 Performance Experience</h1>'
        f'<div class="dt"><b>{e(ev["date"])}</b> · {ampm(ev["blocks"][0][0])} – {ampm(ev["blocks"][-1][1])}</div>'
        f'<div class="who"><div><span>Coaches</span><p>{" · ".join(map(e, ev["coaches"]))}</p></div>'
        f'<div><span>Players</span><p>{" · ".join(map(e, ev["players"]))}</p></div></div></div>'
        f'<div class="bd"><div class="sh">Agenda</div>{"".join(rows)}<div class="bring"><b>BRING</b>{e(ev["bring"])}</div></div>'
        f'<div class="ft"><span>CH3 Performance Experience</span><span><b>TEAMCH3</b> · the Floridian</span></div></div>')
os.makedirs(os.path.join(ROOT, 'teamflo-games', '.build'), exist_ok=True)
fn = os.path.join(HERE, '.agenda.html'); out = os.path.join(HERE, ev['file'])
open(fn, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{page}</body></html>')
jobs = os.path.join(HERE, '.jobs.json'); json.dump([[fn, out]], open(jobs, 'w'))
subprocess.run(['node', os.path.join(ROOT, 'teamflo-games', 'render.js'), jobs], check=True)
print(out)
