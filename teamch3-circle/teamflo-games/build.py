# Builds the TeamCH3 TeamFLO games and drills PDFs from games.py.  Run: python3 build.py  (needs Playwright via node)
import html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from games import C, SINGLES, PACKS
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'pdf'); TMP = os.path.join(HERE, '.build')
e = html.escape
CSS = """
@font-face{font-family:Anton;src:url(../assets/Anton.ttf)}
@font-face{font-family:B;font-weight:600;src:url(../assets/Barlow600.ttf)}
@font-face{font-family:B;font-weight:700;src:url(../assets/Barlow700.ttf)}
@page{size:8.5in 11in;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:B;font-weight:600;color:#253746;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:8.5in;height:11in;position:relative;overflow:hidden;page-break-after:always;background:#fff;display:flex;flex-direction:column}
.hd{background:#253746;height:1.05in;display:flex;align-items:center;justify-content:space-between;padding:0 .55in;border-bottom:6px solid #E04E39;flex:none}
.hd .m{height:52px}.hd .f{height:44px}.hd .t{font:700 15px/1 B;letter-spacing:.28em;color:#F47C67}
.bd{flex:1;padding:.42in .6in .2in;display:flex;flex-direction:column;min-height:0}
.eb{font:700 16px/1.2 B;letter-spacing:.2em;color:#C9432F;text-transform:uppercase}
h1{font:400 64px/.95 Anton;text-transform:uppercase;margin:10px 0 0;color:#253746}
.sub{font:700 24px/1.2 B;color:#536676;margin-top:10px}
.meta{font:700 14px/1 B;letter-spacing:.16em;color:#7A8A98;text-transform:uppercase;margin-top:12px}
.rule{width:90px;height:5px;background:#E04E39;margin:22px 0 20px;flex:none}
.body{font-size:var(--fs,19px);line-height:1.45;color:#33475A}.body p{margin:0 0 .7em}
.img{margin:6px 0 14px;text-align:center}.img img{max-width:100%;max-height:var(--ih,3.4in);border-radius:4px}
.low{margin-top:auto;display:grid;grid-template-columns:1.25fr 1fr;gap:16px;padding-top:12px}
.low.one{grid-template-columns:1fr}
.box{background:#F2F4F6;border-left:5px solid #E04E39;padding:14px 16px;border-radius:3px}
.box.adv{border-left-color:#253746}
.bl{font:700 13px/1 B;letter-spacing:.22em;color:#C9432F;text-transform:uppercase;margin-bottom:8px}
.box.adv .bl{color:#253746}
.bt{font-size:16.5px;line-height:1.4;color:#33475A;white-space:pre-line}
.col{display:flex;flex-direction:column;gap:12px}
.notes{flex:1;min-height:0;margin-top:10px;display:flex;flex-direction:column}.notes .bl{color:#7A8A98;margin-bottom:0}.notes .ln2{flex:1;background:repeating-linear-gradient(to bottom,transparent 0,transparent 33px,#D5DCE2 33px,#D5DCE2 34px)}
.note{font:700 14px/1 B;letter-spacing:.24em;color:#C9432F;text-transform:uppercase;margin-top:14px}
.ft{background:#253746;color:#A6B1BA;font:700 12px/1 B;letter-spacing:.2em;padding:13px .6in;display:flex;justify-content:space-between;text-transform:uppercase;flex:none}
.ft b{color:#F47C67}
.cv{background:radial-gradient(ellipse at 40% 35%,#2B4152 0%,#253746 45%,#16222E 100%);color:#fff;padding:.9in .8in;justify-content:flex-start}
.cv .m{height:80px;align-self:flex-start}
.cv .eb{color:#F47C67;margin-top:.7in;font-size:18px}
.cv h1{color:#fff;font-size:96px;margin-top:14px}
.cv .sub{color:#F47C67;font-size:30px}
.cv .ln{font:600 19px/1.45 B;color:#CDD4DA;margin-top:14px;max-width:6.4in}
.cv .rule{margin:30px 0 24px}
.cv ol{margin:0;padding:0;list-style:none;counter-reset:n}
.cv li{counter-increment:n;font:400 30px/1.25 Anton;text-transform:uppercase;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.14);display:flex;gap:18px}
.cv li:before{content:counter(n,decimal-leading-zero);color:#E04E39;font-size:22px;padding-top:6px}
.cv .f{height:56px;margin-top:auto;align-self:flex-end}
"""
FIT = """<script>
document.querySelectorAll('.pg.card').forEach(pg=>{const b=pg.querySelector('.bd');let fs=19,ih=3.4;const n=pg.querySelector('.notes');if(n&&n.getBoundingClientRect().height<90)n.remove();
 const over=()=>b.scrollHeight>b.clientHeight+1;
 while(over()&&fs>13){fs-=.5;b.style.setProperty('--fs',fs+'px');if(ih>2)ih-=.15;b.style.setProperty('--ih',ih+'in')}
 if(over())pg.setAttribute('data-overflow','1')});
document.querySelectorAll('.cv').forEach(pg=>{let s=30;const l=[...pg.querySelectorAll('li')];
 while(pg.scrollHeight>pg.clientHeight+1&&s>18){s-=1;l.forEach(x=>x.style.fontSize=s+'px')}});
</script>"""
def header():
    return '<div class="hd"><img class="m" src="../assets/mark.png"><div class="t">TEAMCH3 · TEAMFLO</div><img class="f" src="../assets/flor-white.png"></div>'
def footer(label):
    return f'<div class="ft"><span>TeamFLO · the CH3 academy at the Floridian</span><span><b>TEAMCH3</b> · {e(label)}</span></div>'
def card_html(k, label):
    c = C[k]; o = ['<div class="pg card">', header(), '<div class="bd">']
    o.append(f'<div class="eb">{e(c["eyebrow"])}</div><h1>{e(c["title"])}</h1>')
    if c['sub']: o.append(f'<div class="sub">{e(c["sub"])}</div>')
    if c['meta']: o.append(f'<div class="meta">{e(c["meta"])}</div>')
    o.append('<div class="rule"></div><div class="body">' + ''.join(f'<p>{e(p)}</p>' for p in c['body']) + '</div>')
    if c['img']: o.append(f'<div class="img"><img src="../assets/{c["img"]}"></div>')
    o.append('<div class="notes"><div class="bl">Notes and scores</div><div class="ln2"></div></div>')
    boxes = ''.join(f'<div class="box"><div class="bl">{e(l)}</div><div class="bt">{e(t)}</div></div>' for l, t in c['boxes'])
    adv = f'<div class="box adv"><div class="bl">Doc\'s advice</div><div class="bt">{e(c["advice"])}</div></div>' if c['advice'] else ''
    if adv or boxes:
        cls = 'low' if adv and boxes else 'low one'
        o.append(f'<div class="{cls}">{adv}' + (f'<div class="col">{boxes}</div>' if boxes else '') + '</div>')
    if c['note']: o.append(f'<div class="note">{e(c["note"])}</div>')
    o.append('</div>' + footer(label) + '</div>')
    return ''.join(o)
def cover_html(title, sub, lines, keys):
    o = ['<div class="pg cv"><img class="m" src="../assets/mark.png"><div class="eb">TEAMCH3 · TEAMFLO</div>', f'<h1>{e(title)}</h1>']
    if sub: o.append(f'<div class="sub">{e(sub)}</div>')
    for l in lines or []: o.append(f'<div class="ln">{e(l)}</div>')
    o.append('<div class="rule"></div><ol>' + ''.join(f'<li>{e(C[k]["title"])}</li>' for k in keys) + '</ol>')
    o.append('<img class="f" src="../assets/flor-white.png"></div>')
    return ''.join(o)
def slug(s): return re.sub(r'[^A-Za-z0-9 ,\'&+.-]', '', s).strip()
jobs = []
os.makedirs(TMP, exist_ok=True)
def doc(folder, name, pages):
    fn = os.path.join(TMP, f'{len(jobs):03d}.html')
    open(fn, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}{FIT}</body></html>')
    out = os.path.join(OUT, folder, f'TeamCH3 TeamFLO - {slug(name)}.pdf'); os.makedirs(os.path.dirname(out), exist_ok=True)
    jobs.append([fn, out])
for folder, keys in SINGLES:
    for k in keys: doc(os.path.join('Games and drills', folder), C[k]['title'] if not C[k]['eyebrow'].startswith('Harmon Match ·') else f'Harmon Match {C[k]["eyebrow"].split("·")[1].strip()} - {C[k]["title"]}', [card_html(k, folder)])
for folder, title, sub, lines, keys in PACKS:
    doc(folder, title, [cover_html(title, sub, lines, keys)] + [card_html(k, title) for k in keys])
# one combined playbook of every unique card
allk = list(dict.fromkeys([k for _, ks in SINGLES for k in ks] + [k for p in PACKS for k in p[4]]))
doc('', 'Complete Playbook', [cover_html('The Playbook', 'Every TeamFLO game and drill.', None, [])] + [card_html(k, 'Playbook') for k in allk])
json.dump(jobs, open(os.path.join(TMP, 'jobs.json'), 'w'))
subprocess.run(['node', os.path.join(HERE, 'render.js'), os.path.join(TMP, 'jobs.json')], check=True)
