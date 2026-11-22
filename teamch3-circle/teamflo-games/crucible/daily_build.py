# Builds "TeamCH3 TeamFLO - Daily Crucible Training Plan (37 Weeks).pdf" from src/daily.txt
# (Drive doc "37-Week Golf Practice & Daily Crucible Training Plan"). Same look as the Crucible PDF.
import html, json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
TMP = os.path.join(ROOT, '.build', 'crucible'); os.makedirs(TMP, exist_ok=True)
OUT = os.path.join(ROOT, 'pdf', 'Practice Plans', 'TeamCH3 TeamFLO - Daily Crucible Training Plan (37 Weeks).pdf')
A = '../../assets/'; e = html.escape
import sys; sys.path.insert(0, HERE); from content import MAJORS, week_date
fmt = lambda d: d.strftime('%b %-d, %Y')
bsrc = open(os.path.join(HERE, 'build.py')).read()
CSS = eval(re.search(r'CSS = (""".*?""" % \{\'A\': A\})', bsrc, re.S).group(1))
FIT = eval(re.search(r'FIT = (""".*?""")', bsrc, re.S).group(1)).replace('let fs=12.5', 'let fs=15.5')
text = open(os.path.join(HERE, 'src', 'daily.txt'), encoding='utf-8-sig').read()
cl = lambda t: re.sub(r'\s+', ' ', t.replace(' ', ' ')).strip()

DAYS = [('Technical & Launch Monitor', 'Bio-feedback, video, face control, path shaping, launch optimization.'),
        ('Speed, Strike & Wedge Matrix', 'Speed protocols, centered strike, distance matrix work.'),
        ('Short Game & Crucible Scrambling', 'Up-and-downs, bunkers, putting ladders under physical stress.'),
        ('On-Course Chaos & Playcalls', 'Course strategy, forced awkward lies, wind and elevation.'),
        ('Tournament Sim & Conditioning', 'High-pressure simulated scoring with the heart rate up.'),
        ('Benchmark & Analytics', 'Standardized testing: TrackMan Combine, wedge test, Clippd review.'),
        ('Recovery, Mobility & Reset', 'Mobility, soft tissue work, mental audit.')]
SHORT = ['Technical', 'Speed & wedges', 'Short game', 'On-course', 'Tournament sim', 'Benchmark', 'Recovery']
PHASE_INFO = {  # from the doc's Program Phase Matrix
    1: ('Biomechanical baseline, launch monitor alignment, core speed mechanics', 'Baseline cardio metrics; post-set putting drills (Zone 1 HR)', 'Face/path delta < 2.0°, smash 1.48+, TrackMan Combine baseline'),
    2: ('Speed gains, stock wedge yardage mapping (4 distances per wedge)', 'Assault bike sprints into 70–110 yd wedge precision (Zone 3 HR)', 'Wedge dispersion radius < 12 ft; +3–5 mph clubhead speed'),
    3: ('Scrambling, tight-lie control, bunker play, pressure putting', 'Burpees and push-ups into 6-ft pressure putts; execute at 140+ BPM', 'Up-and-down > 65% from 30 yards; 3-putt < 2.0%'),
    4: ('Environmental adaptability, non-standard lies, course management', 'Full Crucible circuits (bike + push-ups) before simulated holes', 'Clippd Off-the-Tee quality > 80; Tee-to-Green SG positive'),
    5: ('18-hole simulated rounds, strict scoring rules, penalty stress', '30-second sprint intervals between simulated shots on a clock', 'Tournament scoring average in line with handicap index'),
    6: ('Fine-tuning, speed maintenance, mental readiness, load reduction', 'Low-volume, high-intensity neural priming; mobility focus', '90%+ target proximity accuracy; zero fatigue markers')}

phases, cur_p, cur_w = [], None, None
for line in text.splitlines():
    s = line.strip()
    m = re.match(r'Phase (\d): (.+?) \(Weeks (\d+)[–-](\d+)\)', s)
    if m: cur_p = {'n': int(m.group(1)), 'title': m.group(2), 'range': f'Weeks {m.group(3)}–{m.group(4)}', 'weeks': []}; phases.append(cur_p); continue
    m = re.match(r'Week (\d+): (.+)', s)
    if m and cur_p: cur_w = {'n': int(m.group(1)), 'title': cl(m.group(2)), 'obj': '', 'days': []}; cur_p['weeks'].append(cur_w); continue
    m = re.match(r'Weekly Objective: (.+)', s)
    if m and cur_w: cur_w['obj'] = cl(m.group(1)); continue
    m = re.match(r'\* Day (\d): (.+)', s)
    if m and cur_w: cur_w['days'].append(cl(m.group(2)))
assert sum(len(p['weeks']) for p in phases) == 37 and all(len(w['days']) == 7 for p in phases for w in p['weeks'])

EXTRA = """
.obj{background:#253746;color:#fff;border-radius:4px;padding:12px 16px;margin-top:14px;font-size:1.1em;line-height:1.4}
.obj b{color:#F47C67;font-weight:700;letter-spacing:.16em;font-size:.78em;display:block;margin-bottom:4px}
.days{margin-top:14px;display:flex;flex-direction:column;gap:8px}
.day{display:grid;grid-template-columns:1.45in 1fr auto;gap:14px;background:#F4F6F8;border-radius:4px;padding:11px 14px;align-items:start}
.day.r{background:#EEF2F0}
.dn{font:400 2em/.9 Anton;color:#E04E39}.dn small{display:block;font:700 .62em/1.25 B;letter-spacing:.12em;color:#536676;text-transform:uppercase;margin-top:6px}
.dt{line-height:1.45;color:#33475A;font-size:1.08em}
.ck{font:700 .72em/1 B;letter-spacing:.16em;color:#8A99A6;text-transform:uppercase;white-space:nowrap;padding-top:4px}
.ck:before{content:'';display:inline-block;width:11px;height:11px;border:1.6px solid #8A99A6;border-radius:2px;margin-right:6px;vertical-align:-2px}
.notes2{flex:1;min-height:0;margin-top:12px;display:flex;flex-direction:column}.notes2 .bl{font:700 11px/1 B;letter-spacing:.22em;color:#7A8A98;text-transform:uppercase}
.notes2 .ln2{flex:1;background:repeating-linear-gradient(to bottom,transparent 0,transparent 27px,#D5DCE2 27px,#D5DCE2 28px)}
table.pm{width:100%;border-collapse:collapse;margin-top:6px;font-size:.95em}
.pm td,.pm th{padding:6px 7px;border-bottom:1px solid #E1E6EA;vertical-align:top;text-align:left;line-height:1.3;color:#33475A}
.pm th{background:#253746;color:#fff;font:700 10px/1.2 B;letter-spacing:.16em;text-transform:uppercase}
.pm td.p{font:400 15px/1.15 Anton;color:#253746;text-transform:uppercase;width:1.35in}.pm td.p span{display:block;font:700 10px/1.3 B;color:#C9432F;letter-spacing:.12em;margin-top:3px}
"""
LBL = 'DAILY CRUCIBLE TRAINING PLAN'
def header(): return f'<div class="hd"><img class="m" src="{A}mark.png"><div class="t">TEAMCH3 · TEAMFLO · DAILY TRAINING</div><img class="f" src="{A}flor-white.png"></div>'
def footer(l): return f'<div class="ft"><span>Daily Crucible Training Plan · {e(l)}</span><span><b>TEAMCH3</b> · the Floridian</span></div>'
def page(body, label): return f'<div class="pg">{header()}<div class="bd">{body}</div>{footer(label)}</div>'

def cover():
    return (f'<div class="pg cv"><img class="m" src="{A}mark.png"><div class="eb">TEAMCH3 · TEAMFLO PRACTICE PLAN</div>'
            '<h1 style="font-size:92px">Daily Crucible Training</h1><div class="sub">37 Weeks · 7 Days a Week · 6 Phases</div><div class="ln" style="margin-top:10px;color:#F47C67">2026–27 season: October 5, 2026 to U.S. Open week, June 2027. Masters week is Week 27, PGA Championship week is Week 33 and U.S. Open week is Week 37.</div>'
            '<div class="ln">A day-by-day player development plan built on launch monitor numbers (TrackMan, GCQuad, Swing Catalyst), round analytics (Clippd, Arccos Strokes Gained) and high-heart-rate Crucible stress training.</div><div class="rule"></div>'
            '<div class="stats"><div>37<span>WEEKS</span></div><div>259<span>SESSIONS</span></div><div>6<span>PHASES</span></div></div>'
            f'<img class="f" src="{A}flor-white.png"></div>')

def overview():
    rows = ''.join(f'<tr><td class="p">{e(p["title"])}<span>{e(p["range"])}</span></td><td>{e(PHASE_INFO[p["n"]][0])}</td><td>{e(PHASE_INFO[p["n"]][1])}</td><td>{e(PHASE_INFO[p["n"]][2])}</td></tr>' for p in phases)
    days = ''.join(f'<b>Day {i + 1} · {e(t)}</b><div>{e(d)}</div>' for i, (t, d) in enumerate(DAYS))
    b = ('<div class="eb">How it works</div><h1>GolfChaos: Managed</h1>'
         '<div class="mis"><b>DOCTRINE</b>Golf performance breaks down when physical exertion, competitive stress and environmental chaos disrupt your mechanics. Pair elite mechanics with high-heart-rate conditioning (assault bike sprints, burpees, push-ups) before the shot, and you learn to perform under competitive pressure.</div>'
         '<div class="h2">The six phases</div><table class="pm"><tr><th>Phase</th><th>Focus</th><th>Pressure &amp; conditioning</th><th>Benchmarks</th></tr>' + rows + '</table>'
         '<div class="h2">The weekly rhythm</div><div class="kv" style="grid-template-columns:2.6in 1fr">' + days + '</div>'
         '<div class="safe"><b>SAFETY</b>Coaches set every load and every rep count. Juniors use bodyweight or light options for any loaded exercise, and anyone can swap an exercise for a safe alternative. Hydrate between blocks.</div>')
    return page(b, 'How it works')

def phase_page(p):
    lis = ''.join(f'<li><span>Week {w["n"]} · {week_date(w["n"]).strftime("%b %-d")}</span>{e(w["title"])}{"<em>" + e(MAJORS[w["n"]][0]) + "</em>" if w["n"] in MAJORS else ""}</li>' for w in p['weeks'])
    f, c, k = PHASE_INFO[p['n']]
    return (f'<div class="pg mo"><img class="m" src="{A}mark.png"><div class="ph">{e(p["range"])}</div><div class="big">{p["n"]:02d}</div>'
            f'<div class="eb">Phase {p["n"]}</div><h1>{e(p["title"])}</h1><div class="ln"><b style="color:#F47C67">FOCUS</b> {e(f)}<br><b style="color:#F47C67">BENCHMARKS</b> {e(k)}</div><ol>{lis}</ol>'
            f'<img class="f" src="{A}flor-white.png"></div>')

def week_page(p, w):
    ds = ''.join(f'<div class="day{" r" if i == 6 else ""}"><div class="dn">DAY {i + 1}<small>{e(SHORT[i])}</small></div><div class="dt">{e(t)}</div><div class="ck">Done</div></div>' for i, t in enumerate(w['days']))
    badge = f'<div class="major"><b>{e(MAJORS[w["n"]][0])}</b>{e(MAJORS[w["n"]][1])}</div>' if w['n'] in MAJORS else ''
    b = (f'<div class="eb">Phase {p["n"]} · {e(p["title"])} · Week of {fmt(week_date(w["n"]))}</div><div class="wk"><div class="num">{w["n"]:02d}</div><h1>{e(w["title"])}</h1></div>{badge}'
         f'<div class="obj"><b>WEEKLY OBJECTIVE</b>{e(w["obj"])}</div><div class="days">{ds}</div>'
         '<div class="notes2"><div class="bl">Numbers and notes</div><div class="ln2"></div></div>')
    return page(b, f'Week {w["n"]}')

pages = [cover(), overview()]
for p in phases:
    pages.append(phase_page(p)); pages += [week_page(p, w) for w in p['weeks']]
fn = os.path.join(TMP, 'daily.html')
open(fn, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{EXTRA}</style></head><body>{"".join(pages)}{FIT}</body></html>')
json.dump([[fn, OUT]], open(os.path.join(TMP, 'jobs_daily.json'), 'w'))
print(len(pages), 'pages')
subprocess.run(['node', os.path.join(ROOT, 'render.js'), os.path.join(TMP, 'jobs_daily.json')], check=True)
