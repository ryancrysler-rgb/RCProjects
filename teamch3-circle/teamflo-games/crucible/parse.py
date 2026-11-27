# Parses the Crucible Blueprint Google Docs (exported as text into src/) into weeks.json.
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, 'src')

def clean(t):
    t = t.replace('﻿', '').replace(' ', ' ')
    # stray citation markers left by the AI tool the docs came from, e.g. "advises1111." / "changes13." / "round"2222."
    t = re.sub(r'(?<=[a-z])\d{1,4}(?=[\s.,;:!?)]|$)', '', t)
    t = re.sub(r'(?<=[a-z]["”])\d{1,4}(?=[\s.,;:!?)]|$)', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def read(name): return open(os.path.join(SRC, name), encoding='utf-8-sig').read().replace('\ufeff', '')

def split_weeks(text):
    """Return {week: block_text} for 'Crucible Blueprint: Week N - ...' headers in a month doc."""
    parts = re.split(r'(?m)^\s*(?=Crucible Blueprint:\s*Week \d+)', text)
    out = {}
    for p in parts:
        m = re.match(r'Crucible Blueprint:\s*Week (\d+)', p.strip())
        if m: out[int(m.group(1))] = p
    return out

def intro(text):
    """Month intro paragraph that sits above the first week header."""
    first = re.split(r'(?m)^\s*(?:Crucible Blueprint|Mission:)', text)[0]
    return clean(first.replace('_', ' ')).removeprefix('Of course. ')

LABELS = {'"do or die" drill': 'Do or Die', 'do or die drill': 'Do or Die', 'consequence': 'Consequence',
          'conditioning': 'Conditioning', 'execution': 'Execution', 'gate': 'Gate'}

def parse_block(text):
    lines = text.splitlines(); title = None; mission = None; sections = [{'h': None, 'items': []}]
    cur = None
    for raw in lines:
        s = raw.strip()
        if not s or set(s) <= {'_'}: continue
        if title is None and re.match(r'(Crucible Blueprint|Crucible Week)', s): title = s; continue
        m = re.match(r'Mission:\s*(.*)', s)
        if m: mission = clean(m.group(1)); continue
        if mission is None: continue  # intro chatter before the mission line
        m = re.match(r'(\d+)\.\s+(.*)', s)
        if m:
            head = clean(m.group(2)); cat, _, name = head.partition(':')
            if not name: cat, name = '', head
            cur = {'cat': clean(cat), 'name': clean(name), 'rows': [], 'extra': []}
            sections[-1]['items'].append(cur); continue
        m = re.match(r'[*•]\s+(.*)', s)
        if m:
            b = clean(m.group(1)); lab, sep, rest = b.partition(':')
            if cur is None:
                cur = {'cat': '', 'name': '', 'rows': [], 'extra': []}; sections[-1]['items'].append(cur)
            if sep and len(lab) <= 32:
                cur['rows'].append([LABELS.get(lab.strip().lower(), lab.strip()), rest.strip()])
            else:
                cur['rows'].append(['', b])
            continue
        # anything else: a short line after drills = section heading, otherwise extra text
        if len(s) < 40:
            sections.append({'h': clean(s).rstrip(':'), 'items': []}); cur = None
        elif cur: cur['extra'].append(clean(s))
    sections = [x for x in sections if x['items']]
    return title, mission, sections

WEEKS = {}
def add(n, text, title=None, src=''):
    t, mission, secs = parse_block(text)
    if title is None:
        m = re.search(r'Week \d+\s*(?:\(B\))?\s*[-–:]\s*(.*)', t or '')
        title = clean(m.group(1)) if m else ''
    WEEKS[str(n)] = {'n': n, 'title': title, 'mission': mission, 'sections': secs, 'src': src}

# Weekly docs actually used last season take priority over the month drafts.
single = {1: 'w01.txt', 2: 'w02.txt', 3: 'w03.txt', 4: 'w04.txt', 5: 'w05.txt', 6: 'w06.txt', 7: 'w07.txt', 9: 'w09.txt',
          10: 'w10.txt', 11: 'w11.txt', 12: 'w12.txt', 13: 'w13.txt', 14: 'w14.txt', 15: 'w15.txt', 16: 'w16.txt',
          17: 'w17.txt', 18: 'w18.txt', 19: 'w19.txt', 20: 'w20.txt', 21: 'w21.txt', 22: 'w22.txt', 23: 'w23.txt'}
FIXED_TITLES = {3: 'Pressure Inoculation', 4: 'Solidifying Control', 18: 'Mastering the Curves: Part 1', 19: 'Mastering the Curves: Part 2'}
for n, f in single.items(): add(n, read(f), FIXED_TITLES.get(n), f)
add('1B', read('w01b.txt'), 'The Gauntlet', 'w01b.txt')
m2 = split_weeks(read('m2.txt')); add(8, m2[8], src='m2.txt')
m6 = split_weeks(read('m6_w21-24.txt')); add(24, m6[24], src='m6_w21-24.txt')
m7 = split_weeks(read('m7_w25-28.txt'))
for n in (25, 26, 27, 28): add(n, m7[n], src='m7_w25-28.txt')
m9 = split_weeks(read('m9_w33-37.txt'))
for n in (33, 34, 35, 36): add(n, m9[n], src='m9_w33-37.txt')

INTROS = {'2': intro(read('m2.txt')), '3': intro(read('w09.txt')), '6': intro(read('m6_w21-24.txt')),
          '7': intro(read('m7_w25-28.txt')), '9': intro(read('m9_w33-37.txt'))}

# Master doc: core philosophy section and per-week KPI gates.
master = read('master.txt')
kpi = {}
for m in re.finditer(r'\n\s*Week (\d+)\s*\n\s*(.+?)\n\s*(.+?)\n', master):
    kpi[m.group(1)] = clean(m.group(3))
json.dump({'weeks': WEEKS, 'intros': INTROS, 'kpi': kpi}, open(os.path.join(HERE, 'weeks.json'), 'w'), indent=1, ensure_ascii=False)
for k, w in WEEKS.items():
    print(k, '|', w['title'], '|', [len(s['items']) for s in w['sections']], [s['h'] for s in w['sections']], '| kpi:', kpi.get(str(k), '-')[:60])
