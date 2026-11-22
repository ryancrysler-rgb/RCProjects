# Builds "TeamCH3 TeamFLO - The Crucible 37-Week Practice Plan.pdf" from weeks.json (parse.py) + content.py.
import html, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); from content import MONTHS, FRONT, COMPOSED, CAL, MAJORS, week_date
TMP = os.path.join(ROOT, '.build', 'crucible'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(ROOT, 'pdf', 'Practice Plans', 'TeamCH3 TeamFLO - The Crucible 37-Week Practice Plan.pdf')
A = '../../assets/'
data = json.load(open(os.path.join(HERE, 'weeks.json')))
W = dict(data['weeks']); W.update(COMPOSED)
# weeks that moved for the 2027 major calendar: point their missions at the right block
W['24'] = dict(W['24'], mission=W['24']['mission'].replace("the entire month's training", "everything from Competitive Sharpening"))
W['36'] = dict(W['36'], mission=W['36']['mission'].replace("the entire month's training", "the strokes gained block"))
def cn(k): return CAL[k]
def fmt(d): return d.strftime('%b %-d, %Y')
def remap_from(t):  # last season's week numbers -> this season's calendar weeks
    if t == 'New': return 'New drill'
    return 'From ' + re.sub(r'\b(\d+B?)\b', lambda m: str(CAL.get(m.group(1), m.group(1))) if m.group(1) != '1B' else '1B', t)
e = html.escape

def lab(l):
    l = l.strip(); low = l.lower()
    if low.startswith('optional hiit'): return 'HIIT', 'optional'
    if low.startswith('hiit'): return 'HIIT', l[4:].strip(' ()') or None
    if low == 'the exercise': return 'HIIT', None
    if low.startswith('the task'): return 'Do or Die', None
    if low == 'the question': return 'Question', None
    return l, None

CSS = """
@font-face{font-family:Anton;src:url(%(A)sAnton.ttf)}
@font-face{font-family:B;font-weight:600;src:url(%(A)sBarlow600.ttf)}
@font-face{font-family:B;font-weight:700;src:url(%(A)sBarlow700.ttf)}
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:B;font-weight:600;color:#253746;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;background:#fff;display:flex;flex-direction:column}
.hd{background:#253746;height:.8in;display:flex;align-items:center;justify-content:space-between;padding:0 .5in;border-bottom:5px solid #E04E39;flex:none}
.hd .m{height:40px}.hd .f{height:34px}.hd .t{font:700 12px/1 B;letter-spacing:.28em;color:#F47C67}
.bd{flex:1;padding:.3in .5in .18in;display:flex;flex-direction:column;min-height:0;font-size:var(--fs,12.5px)}
.eb{font:700 12px/1.2 B;letter-spacing:.2em;color:#C9432F;text-transform:uppercase}
h1{font:400 44px/.98 Anton;text-transform:uppercase;margin:6px 0 0;color:#253746}
.wk{display:flex;align-items:flex-end;gap:18px;margin-top:10px}
.wk .num{font:400 76px/.8 Anton;color:#E04E39;flex:none}
.mis{font-size:1.12em;line-height:1.4;color:#33475A;margin-top:10px;border-left:4px solid #253746;padding:2px 0 2px 12px}
.mis b{font-weight:700;color:#253746;letter-spacing:.14em;font-size:.8em;margin-right:6px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;align-content:start}
.sec{grid-column:1/-1;font:400 20px/1 Anton;text-transform:uppercase;color:#253746;border-bottom:2px solid #E04E39;padding:6px 0 5px;margin-top:2px}
.card{background:#F4F6F8;border-radius:4px;padding:10px 12px 9px;display:flex;flex-direction:column;break-inside:avoid}
.card.wide{grid-column:1/-1}
.ct{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.cc{font:700 .78em/1 B;letter-spacing:.18em;color:#C9432F;text-transform:uppercase}
.cc i{font-style:normal;color:#253746;margin-right:7px}
.cf{font:700 .7em/1 B;letter-spacing:.1em;color:#8A99A6;text-transform:uppercase;white-space:nowrap}
.cn{font:400 1.45em/1.05 Anton;text-transform:uppercase;color:#253746;margin:5px 0 6px}
.r{display:grid;grid-template-columns:5.6em 1fr;gap:6px;line-height:1.33;color:#33475A;margin-top:5px}
.r .l{font:700 .7em/1.25 B;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:#253746;border-radius:2px;padding:3px 4px;align-self:start;text-align:center}
.r .l.d{background:#E04E39}.r .l.c{background:#7A8A98}.r .l.q{background:#2E6E5E}.r .l.o{background:#B6C0C8;color:#253746}
.r small{display:block;font-size:.85em;color:#6B7C8A}
.x{line-height:1.33;color:#33475A;margin-top:5px}
.pass{margin-top:auto;padding-top:7px;display:flex;justify-content:flex-end;gap:14px;font:700 .72em/1 B;letter-spacing:.16em;color:#8A99A6;text-transform:uppercase}
.pass span:before{content:'';display:inline-block;width:11px;height:11px;border:1.6px solid #8A99A6;border-radius:2px;margin-right:6px;vertical-align:-2px}
.ft{background:#253746;color:#A6B1BA;font:700 10.5px/1 B;letter-spacing:.2em;padding:11px .5in;display:flex;justify-content:space-between;text-transform:uppercase;flex:none}
.ft b{color:#F47C67}
.cv{background:radial-gradient(ellipse at 40%% 35%%,#2B4152 0%%,#253746 45%%,#16222E 100%%);color:#fff;padding:.9in .8in}
.cv .m{height:80px;align-self:flex-start}
.cv .eb{color:#F47C67;margin-top:.8in;font-size:17px}
.cv h1{color:#fff;font-size:104px;margin-top:14px}
.cv .sub{font:700 30px/1.15 B;color:#F47C67;margin-top:10px}
.cv .ln{font:600 18px/1.5 B;color:#CDD4DA;margin-top:22px;max-width:6.3in}
.cv .rule{width:90px;height:5px;background:#E04E39;margin:30px 0 26px}
.cv .stats{display:flex;gap:34px}.cv .stats div{font:400 46px/1 Anton;color:#fff}.cv .stats span{display:block;font:700 12px/1.4 B;letter-spacing:.2em;color:#A6B1BA;margin-top:6px}
.cv .f{height:56px;margin-top:auto;align-self:flex-end}
.mo{background:#253746;color:#fff;padding:.8in}
.mo .m{height:56px;align-self:flex-start}
.mo .ph{font:700 14px/1 B;letter-spacing:.24em;color:#A6B1BA;text-transform:uppercase;margin-top:1.1in}
.mo .big{font:400 180px/.8 Anton;color:#E04E39;margin-top:22px}
.mo .eb{color:#F47C67;font-size:15px;margin-top:22px}
.mo h1{color:#fff;font-size:64px;margin-top:8px}
.mo .ln{font:600 17px/1.5 B;color:#CDD4DA;margin-top:22px;max-width:6.4in}
.mo ol{list-style:none;margin:28px 0 0;padding:0}
.mo li{display:flex;gap:18px;font:400 24px/1.2 Anton;text-transform:uppercase;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.mo li span{color:#E04E39;width:1.6in;flex:none;font-size:19px;padding-top:3px}
.mo .f{height:46px;margin-top:auto;align-self:flex-end}
.h2{font:400 22px/1 Anton;text-transform:uppercase;color:#253746;margin:16px 0 8px;display:flex;align-items:center;gap:10px}
.h2:after{content:'';flex:1;height:2px;background:#E04E39}
.kv{display:grid;grid-template-columns:1.55in 1fr;gap:6px 14px;line-height:1.4;color:#33475A}
.kv b{color:#253746;font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:.92em}
.flow{display:flex;align-items:center;gap:8px;margin:6px 0 4px}
.flow div{background:#253746;color:#fff;font:700 11px/1.2 B;letter-spacing:.14em;text-transform:uppercase;padding:9px 10px;border-radius:3px;text-align:center;flex:1}
.flow div.o{background:#E04E39}.flow div.g{background:#7A8A98}.flow i{font-style:normal;color:#E04E39;font:400 20px/1 Anton}
.safe{background:#F4F6F8;border-left:5px solid #E04E39;padding:10px 14px;margin-top:14px;line-height:1.4;color:#33475A}
.safe b{color:#C9432F;letter-spacing:.16em;font-size:.85em;margin-right:6px}
table.map{width:100%%;border-collapse:collapse;margin-top:10px}
.map td{padding:4px 6px;border-bottom:1px solid #E1E6EA;vertical-align:top;line-height:1.25}
.map tr.mj td{background:#FCEDEA}.map td span{display:block;font:700 9.5px/1.3 B;letter-spacing:.14em;color:#C9432F;text-transform:uppercase}.map td.dt{white-space:nowrap;color:#7A8A98;font-size:11px;text-align:right}
.major{display:inline-flex;gap:10px;align-items:baseline;background:#E04E39;color:#fff;border-radius:3px;padding:7px 12px;margin-top:10px;font-size:1em;align-self:flex-start}.major b{font:400 17px/1 Anton;text-transform:uppercase;letter-spacing:.02em}
.mo li em{font-style:normal;margin-left:auto;font:700 12px/1 B;letter-spacing:.16em;color:#fff;background:#E04E39;border-radius:2px;padding:6px 8px;align-self:center}
.map td.w{font:400 15px/1.2 Anton;color:#E04E39;width:.55in}
.map tr.mh td{background:#253746;color:#fff;font:700 10.5px/1.2 B;letter-spacing:.16em;text-transform:uppercase;padding:6px 8px;border:0}
.map tr.mh td span{color:#F47C67}
""" % {'A': A}

FIT = """<script>
for(const b of document.querySelectorAll('.bd')){let fs=12.5;b.style.setProperty('--fs',fs+'px');
 const over=()=>b.scrollHeight>b.clientHeight+1||[...b.querySelectorAll('.grid')].some(g=>g.getBoundingClientRect().bottom>b.getBoundingClientRect().bottom-2);
 while(over()&&fs>9){fs-=.25;b.style.setProperty('--fs',fs+'px')}
 if(over())b.closest('.pg').setAttribute('data-overflow',1)}
</script>"""

def header(): return f'<div class="hd"><img class="m" src="{A}mark.png"><div class="t">TEAMCH3 · TEAMFLO · THE CRUCIBLE</div><img class="f" src="{A}flor-white.png"></div>'
def footer(l): return f'<div class="ft"><span>The Crucible · {e(l)}</span><span><b>TEAMCH3</b> · the Floridian</span></div>'
def page(body, label): return f'<div class="pg">{header()}<div class="bd">{body}</div>{footer(label)}</div>'

def card(i, it, wide=False):
    o = [f'<div class="card{" wide" if wide else ""}"><div class="ct"><div class="cc"><i>{i:02d}</i>{e(it["cat"])}</div>']
    if it.get('from'): o.append(f'<div class="cf">{e(remap_from(it["from"]))}</div>')
    o.append(f'</div><div class="cn">{e(it["name"])}</div>')
    for l, t in it['rows']:
        if not l: o.append(f'<div class="x">{e(t)}</div>'); continue
        L, note = lab(l); cls = {'Do or Die': 'd', 'Consequence': 'c', 'Question': 'q', 'Gate': 'c'}.get(L, '')
        if note == 'optional': cls = 'o'; L = 'HIIT opt.'
        extra = f'<small>{e(note)}</small>' if note and note != 'optional' else ''
        o.append(f'<div class="r"><div class="l {cls}">{e(L)}</div><div>{e(t)}{extra}</div></div>')
    for x in it['extra']: o.append(f'<div class="x">{e(x)}</div>')
    o.append('<div class="pass"><span>Passed</span></div></div>')
    return ''.join(o)

def month_of(k):
    for m in MONTHS:
        if k in m['weeks']: return m

def week_pages(k):
    w = W[k]; m = month_of(k); c = cn(k); label = f'Week {c}' + (' (B)' if k == '1B' else '')
    num = '1B' if k == '1B' else f'{c:02d}'
    eb = f'<div class="eb">Month {m["n"]} · {e(m["title"])} · Week of {fmt(week_date(c))}</div>'
    badge = f'<div class="major"><b>{e(MAJORS[c][0])}</b>{e(MAJORS[c][1])}</div>' if c in MAJORS and k != '1B' else ''
    head = (f'{eb}<div class="wk"><div class="num">{num}</div>'
            f'<h1>{e(w["title"])}</h1></div>{badge}<div class="mis"><b>MISSION</b>{e(w["mission"] or "")}</div>')
    # flatten into blocks; max 6 cards per page
    blocks = []
    for s in w['sections']:
        if s['h']: blocks.append(('h', s['h']))
        for it in s['items']: blocks.append(('c', it))
    pages, cur, n, cnt = [], [], 0, 0
    for kind, v in blocks:
        if kind == 'c':
            if cnt == 6: pages.append(cur); cur, cnt = [], 0
            n += 1; cnt += 1; cur.append(('c', v, n))
        else:
            if cnt >= 5: pages.append(cur); cur, cnt = [], 0
            cur.append(('h', v, 0))
    pages.append(cur); html_pages = []
    for pi, pc in enumerate(pages):
        cards = [x for x in pc if x[0] == 'c']; g = []
        for kind, v, i in pc:
            if kind == 'h': g.append(f'<div class="sec">{e(v)}</div>')
            else: g.append(card(i, v, wide=(len(cards) == 1)))
        top = head if pi == 0 else f'{eb}<div class="wk"><div class="num">{num}</div><h1>{e(w["title"])} <span style="color:#7A8A98">(cont.)</span></h1></div>'
        html_pages.append(page(top + f'<div class="grid">{"".join(g)}</div>', label))
    return html_pages

def cover():
    return (f'<div class="pg cv"><img class="m" src="{A}mark.png"><div class="eb">TEAMCH3 · TEAMFLO PRACTICE PLAN</div>'
            '<h1>The Crucible</h1><div class="sub">37-Week Practice Plan · 2026–27 Season</div><div class="ln" style="margin-top:10px;color:#F47C67">October 5, 2026 to U.S. Open week, June 2027. Built around the 2027 Masters, PGA Championship and U.S. Open.</div>'
            f'<div class="ln">{e(FRONT["premise"])}</div><div class="rule"></div>'
            '<div class="stats"><div>37<span>WEEKS</span></div><div>9<span>MONTHS</span></div><div>3<span>PHASES</span></div><div>6+6<span>HIIT + DO OR DIE</span></div></div>'
            f'<img class="f" src="{A}flor-white.png"></div>')

def how():
    b = ['<div class="eb">How it works</div><h1>Make practice harder than the tournament</h1>',
         '<div class="h2">Every rep</div><div class="flow"><div>HIIT · 45–60s</div><i>›</i><div>15s · breathe + routine</div><i>›</i><div class="o">Do or Die shot</div><i>›</i><div class="g">Pass: advance · Fail: reset + consequence</div></div>',
         '<div class="h2">Session architecture</div><div class="kv">' + ''.join(f'<b>{e(a)}</b><div>{e(t)}</div>' for a, t in FRONT['architecture']) + '</div>',
         '<div class="h2">Guiding principles</div><div class="kv">' + ''.join(f'<b>{e(a)}</b><div>{e(t)}</div>' for a, t in FRONT['principles']) + '</div>',
         '<div class="h2">Reset &amp; consequence rules</div><div class="kv">' + ''.join(f'<b>{e(a)}</b><div>{e(t)}</div>' for a, t in FRONT['rules']) + '</div>',
         '<div class="h2">Reading a week</div><div class="kv"><b>HIIT</b><div>The conditioning block you do right before the shot.</div><b>Do or Die</b><div>The golf drill, done with your heart rate up.</div><b>Consequence</b><div>The pass/fail gate and the price of failing it.</div><b>Passed</b><div>Tick the box when you clear the gate. A week is complete when every box is ticked.</div></div>',
         f'<div class="safe"><b>SAFETY</b>{e(FRONT["safety"])}</div>']
    return page(''.join(b), 'How it works')

def season_map():
    cols = []
    for grp in (MONTHS[:5], MONTHS[5:]):
      rows = []
      for m in grp:
        rows.append(f'<tr class="mh"><td colspan="3">Month {m["n"]} · {e(m["title"])}</td></tr>')
        for k in m['weeks']:
            rows.append(f'<tr{" class=mj" if cn(k) in MAJORS and k != "1B" else ""}><td class="w">{k if k == "1B" else cn(k)}</td><td>{e(W[k]["title"])}{"<span>" + e(MAJORS[cn(k)][0]) + "</span>" if cn(k) in MAJORS and k != "1B" else ""}</td><td class="dt">{"" if k == "1B" else week_date(cn(k)).strftime("%b %-d")}</td></tr>')
      cols.append('<table class="map">' + ''.join(rows) + '</table>')
    ph = '<div class="kv" style="margin-top:12px"><b>Phase 1</b><div>The Foundation of Performance · Months 1–3</div><b>Phase 2</b><div>The Strategist &amp; the Shot Maker · Months 4–6</div><b>Phase 3</b><div>The Championship Run · Months 7–9</div></div>'
    return page('<div class="eb">The season</div><h1>37 weeks at a glance</h1>' + ph + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">' + ''.join(cols) + '</div>', 'Season map')

def month_page(m):
    intro = m.get('intro') or data['intros'][m['intro_key']]
    intro = re.sub(r'^We (are now|now) enter(ing)? Month \d+: [^.]*\.\s*', '', intro)
    lis = ''.join(f'<li><span>{"Week 1B" if k == "1B" else "Week " + str(cn(k)) + " · " + week_date(cn(k)).strftime("%b %-d")}</span>{e(W[k]["title"])}{"<em>" + e(MAJORS[cn(k)][0]) + "</em>" if cn(k) in MAJORS and k != "1B" else ""}</li>' for k in m['weeks'])
    return (f'<div class="pg mo"><img class="m" src="{A}mark.png"><div class="ph">{e(m["phase"])}</div><div class="big">{m["n"]:02d}</div>'
            f'<div class="eb">Month {m["n"]}</div><h1>{e(m["title"])}</h1><div class="ln">{e(intro)}</div><ol>{lis}</ol>'
            f'<img class="f" src="{A}flor-white.png"></div>')

pages = [cover(), how(), season_map()]
for m in MONTHS:
    pages.append(month_page(m))
    for k in m['weeks']: pages += week_pages(k)
fn = os.path.join(TMP, 'crucible.html')
open(fn, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}{FIT}</body></html>')
json.dump([[fn, OUT]], open(os.path.join(TMP, 'jobs.json'), 'w'))
print(len(pages), 'pages')
subprocess.run(['node', os.path.join(ROOT, 'render.js'), os.path.join(TMP, 'jobs.json')], check=True)
