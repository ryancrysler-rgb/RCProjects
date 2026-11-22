# Builds the TeamCH3 TeamFLO practice plans (rebranded Golf Blueprint plans) from blueprint/plans.json.
import html, json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'pdf', 'Practice Plans'); TMP = os.path.join(ROOT, '.build', 'plans'); os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
src = open(os.path.join(ROOT, 'build.py')).read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1).replace('../assets/', '../../assets/')
FIT = re.search(r'FIT = """(.*?)"""', src, re.S).group(1)
e = html.escape
NAMES = {'IntentionalPractice': 'Intentional Practice 1', 'Intentional3': 'Intentional Practice 3', 'IntentionalFail': 'Intentional Fail',
         'Approach': 'Approach', 'DistanceControl': 'Distance Control', 'DrivingSpecificBlueprint': 'Driving',
         'HabitsAndProcess': 'Habits and Process', 'Process2': 'Process 2', 'ProcessAllAreasBlueprint': 'Process - All Areas',
         'ProcessAllAspects': 'Process - All Aspects', 'Reflection': 'Reflection 1', 'Reflection2': 'Reflection 2', 'Session1': 'Session 1'}
CREDIT = 'Practice plan by Nico Darras and Kevin Moore, © 2021'
FIX = [('committted', 'committed'), ('judgement', 'judgment')]
def fx(t):
    t = re.sub(r'\s*\(\d+ min\.\)\s*$', '', t)
    for a, b in FIX: t = t.replace(a, b)
    return t
EXTRA = """
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{font:700 13px/1 B;letter-spacing:.12em;text-transform:uppercase;background:#F2F4F6;color:#253746;padding:8px 10px;border-radius:3px}
.chip b{color:#C9432F;font-weight:700;margin-right:6px}
.chip.on{background:#253746;color:#fff}.chip.on b{color:#F47C67}
.cv .ses{margin-top:18px}.cv .sh{font:400 30px/1 Anton;text-transform:uppercase;display:flex;gap:14px;align-items:baseline}
.cv .sh span{font:700 15px/1 B;letter-spacing:.2em;color:#F47C67}
.cv .sl{font:600 16px/1.5 B;color:#CDD4DA;margin-top:6px}
.cv .cr{font:600 12px/1.3 B;color:#7A8A98;letter-spacing:.06em;margin-top:14px}
"""
def header():
    return '<div class="hd"><img class="m" src="../../assets/mark.png"><div class="t">TEAMCH3 · TEAMFLO</div><img class="f" src="../../assets/flor-white.png"></div>'
def footer(label):
    return f'<div class="ft"><span>TeamFLO practice plan · {e(label)}</span><span><b>TEAMCH3</b> · the Floridian</span></div>'
def cover(name, p):
    o = ['<div class="pg cv"><img class="m" src="../../assets/mark.png"><div class="eb">TEAMCH3 · TEAMFLO PRACTICE PLAN</div>', f'<h1>{e(name)}</h1>',
         f'<div class="ln">{e(fx(p["intro"]))}</div><div class="rule"></div>']
    for s in p['sessions']:
        o.append(f'<div class="ses"><div class="sh">Session {s["n"]} <span>{e(s["mins"].strip("()").upper())}</span></div><div class="sl">{e(" · ".join(s["cards"]))}</div></div>')
    o.append(f'<div class="cr">{e(CREDIT)}</div><img class="f" src="../../assets/flor-white.png"></div>')
    return ''.join(o)
def card(c, sess, name):
    f = c['fields']
    o = ['<div class="pg card">', header(), '<div class="bd">',
         f'<div class="eb">Session {sess["n"]} · {e(sess["mins"].strip("()"))} · {e(f["Skillset"])}</div><h1>{e(c["title"])}</h1>']
    chips = [('Type', f['Type']), ('Location', f['Location']), ('Pressure', 'Simulate' if f['Simulate pressure'] == 'Yes' else 'No'), ('Launch monitor', f['Launch monitor'])]
    o.append('<div class="chips">' + ''.join(f'<div class="chip{" on" if l == "Pressure" and v == "Simulate" else ""}"><b>{e(l)}</b>{e(v)}</div>' for l, v in chips) + '</div>')
    o.append('<div class="rule"></div><div class="bl" style="font:700 13px/1 B;letter-spacing:.22em;color:#C9432F">DESCRIPTION</div><div class="body" style="margin-top:8px">' + ''.join(f'<p>{e(fx(x))}</p>' for x in c['description']) + '</div>')
    o.append('<div class="notes"><div class="bl">Notes and scores</div><div class="ln2"></div></div>')
    adv = '<br><br>'.join(e(fx(x)) for x in c['advice']); trk = '<br><br>'.join(e(fx(x)) for x in c['tracking'])
    o.append(f'<div class="low"><div class="box adv"><div class="bl">Advice</div><div class="bt" style="white-space:normal">{adv}</div></div><div class="col"><div class="box"><div class="bl">Tracking</div><div class="bt" style="white-space:normal">{trk}</div></div></div></div>')
    o.append('</div>' + footer(name) + '</div>')
    return ''.join(o)
plans = json.load(open(os.path.join(HERE, 'plans.json'))); jobs = []
for key, name in NAMES.items():
    p = plans[key]; pages = [cover(name, p)]; i = 0
    for s in p['sessions']:
        for _ in s['cards']: pages.append(card(p['cards'][i], s, name)); i += 1
    fn = os.path.join(TMP, key + '.html')
    open(fn, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}{EXTRA}</style></head><body>{"".join(pages)}{FIT}</body></html>')
    jobs.append([fn, os.path.join(OUT, f'TeamCH3 TeamFLO Practice Plan - {name}.pdf')])
json.dump(jobs, open(os.path.join(TMP, 'jobs.json'), 'w'))
subprocess.run(['node', os.path.join(ROOT, 'render.js'), os.path.join(TMP, 'jobs.json')], check=True)
