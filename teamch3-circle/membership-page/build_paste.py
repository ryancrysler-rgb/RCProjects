# Build the paste-ready TeamCH3 membership page from the design template.
# Usage: python3 -I build_paste.py <template.html> <out.html>
import re, sys, json, html as H
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

SRC, OUT = sys.argv[1], sys.argv[2]
CDN = 'https://assets-v2.circle.so/'
SLOT_IMG = {  # empty photo slot in the design -> Circle-hosted photo, alt text
    'junior-paddock': (CDN + '9g9ln04ugcei0s8xtoifxqjongil', 'Junior players watching a drive at a CH3 academy'),
    'acad-dubai': (CDN + 't98g54q9wn7fv6pwnojxz8yxklv3', 'The CH3 Dubai coaching team with their CH3 bags',
                   'display:block;width:100%;height:100%;object-fit:cover;object-position:50% 72%', ''),
    'acad-thailand': (CDN + 'hs1g84s02j12eyoqpd9pria5k4yl', 'The CH3 Thailand coaching team outside the CH3 Thailand studio',
                      'display:block;width:100%;height:100%;object-fit:cover;object-position:50% 45%', ''),
    # tall photo: crop to the tree line and the group walking up the fairway
    'acad-teamflo': (CDN + 'v1yjaub5tpp51xgs9socyx90h3wg', 'TeamFLO players walking up a Florida fairway with their bags',
                     'display:block;width:100%;height:100%;object-fit:cover;object-position:50% 44%', ''),
    # tall photo: keep the coach in the upper half, above the cue text
    'session-cam': (CDN + '7j18iax3nfe4yh5w5pa6k9qt4n59', 'A CH3 coach on the putting green, with players behind',
                    'display:block;width:100%;height:100%;object-fit:cover;object-position:50% 62%', ''),
    # Claude stands on the left of this photo, so it fills the right half of the hero, clear of the headline
    'hero-claude': (CDN + 'l3mre63766j0kdqifdxoftjpkw12', 'Claude Harmon III range-side at a tour event',
                    'position:absolute;top:0;right:0;width:min(908px,64%);height:auto;'
                    '-webkit-mask-image:linear-gradient(to right,transparent 0%,#000 32%),linear-gradient(to bottom,#000 55%,transparent 100%);'
                    '-webkit-mask-composite:source-in;mask-image:linear-gradient(to right,transparent 0%,#000 32%),linear-gradient(to bottom,#000 55%,transparent 100%);'
                    'mask-composite:intersect', 'ch3-hero-photo'),
}
IMG = {  # design asset uuid -> Circle-hosted copy
    '724528f7-5b9d-45d3-b948-7dd4cceefc0c': CDN + 'h51u9b15jxu0kv0zg3a0pmizefyp',  # CH3 mark, white (no tagline)
    '530230c8-ce0d-4e54-9948-c5e0ce21f727': CDN + 'rrxvgyqulo15uln4o8y0t7bqi3f5',  # CH3 mark, dark (no tagline)
    'fa1e6f77-8a0a-4443-887e-3b9e06bba26d': CDN + 'vyw1wxcti53ypjnr5pcyiofi7nn2',  # TeamFLO logo
    'fa46084f-77e4-47ae-a937-5dc68a3f796b': CDN + '0ystuo9hiylgxum4vl9qbfyy0t07',  # CH3 Dubai logo
    '00cae2d0-8c2a-4858-93aa-a3c112368ba0': CDN + 'ivgpm0bzd85mu5xrqougzj7v5s67',  # CH3 Thailand logo
    'b539c284-f97e-47c0-84cd-5835b49df570': CDN + 'l8a3ec8pkhpblfiksomztbdim55k',  # Son of a Butch studio
    'c7b5244b-de71-4c97-92ac-40d0afaf1a74': CDN + 'j9aqy8fmz9qv6ld9yl66z2es3mmn',  # Global Basecamp (live Circle view)
}
LOGIN = 'https://ch3.circle.so/sign_in'

t = open(SRC, encoding='utf-8').read()
t = t[:t.find('<script type="text/x-dc"')]

# ---- copy updates: the decisions made after the design (pricing, tiers, basecamps, feed) ----
EDITS = [
    ('Full access for 4 weeks, then from $50/month.', '4 weeks free, then from $49/month.'),
    ('Then $50/month. Cancel any time.', 'Then $49/month. Cancel any time.'),
    ('Every player from every CH3 academy is on board, alongside the Son of a Butch community. Everyone shares the Global Basecamp. Each academy also has its own home basecamp: your coaches, your squad, your range. Pick the one that feels like home.',
     'Every player from every CH3 academy is on board, alongside the Son of a Butch community. Everyone shares the Global Basecamp. Each academy also has its own home basecamp: your coaches, your squad, your range. You join the one closest to where you live, and it’s where you train with us in person.'),
    ('PREMIER + ELITE MEMBERS', 'JUNIOR, PREMIER + ELITE'),
    ('Stories from the coaches, swing videos with the Foresight numbers on screen, and the conversation. Switch between the Global Basecamp and your home basecamp in one tap.',
     'Featured posts from Claude and the coaches, the live calendar and the conversation. Switch between the Global Basecamp and your home basecamp in one click.'),
    ('teamch3.com/basecamp', 'ch3.circle.so/c/global'),
    ('Coach stories', 'Featured from the coaches'),
    ('Claude, Ryan and your academy coaches. Live sessions ring orange.', 'The best posts from Claude, Ryan and every academy, at the top of the Global Basecamp.'),
    ('Data on the swing', 'Your data, coached'),
    ('Foresight numbers sit right on the video. Post your own.', 'Send your golf data to RC Greenlight, or ask a coach, straight from the feed.'),
    ('Every membership starts with 4 weeks of full access. Choose where you land after that.',
     'Every membership except Elite starts with 4 weeks free. Cancel before day 28 and pay nothing.'),
    ('Prices in USD, billed monthly. Not at a CH3 academy? You’re welcomed into the closest home basecamp: North America → TeamFLO, Europe → CH3 Dubai, Asia → CH3 Thailand. Elite is limited and by application.',
     'Prices in USD, billed monthly, or pay for the year and get 12 months for the price of 10. Your home basecamp is the academy closest to where you live: the Americas → TeamFLO, Europe, the Middle East and Africa → CH3 Dubai, Asia and the Pacific → CH3 Thailand. Elite is limited, by application, with no free trial.'),
    ('alt="TeamCH3 Global Basecamp feed"', 'alt="The TeamCH3 Global Basecamp in Circle"'),
    # After the Pod is now exclusive access to live podcast recordings with CH3 and special guests
    ('|</span> AFTER THE POD', '|</span> LIVE RECORDING'),
    ('LIVE Q&amp;A WITH CLAUDE <span', 'CH3 + SPECIAL GUEST <span'),
    ('<span>AFTER THE POD</span>', '<span>LIVE RECORDING</span>'),
    ('Live Q&amp;A with Claude</div>', 'In the studio with CH3</div>'),
    ('Straight after the next Son of a Butch drop. Bring a question. Get it answered on air.',
     'Exclusive access to the next Son of a Butch recording, live, with CH3 and a special guest.'),
    ('The episode ends. The mic stays on. Every drop is followed by a live behind-the-scenes Q&amp;A with Claude, open to the whole podcast community.',
     'Pull up a chair in the studio. Every member gets exclusive access to live Son of a Butch recordings with CH3 and special guests.'),
    ('AFTER THE POD IN', 'LIVE RECORDING IN'),
    ('>After the Pod<', '>Live recordings<'),
    ('A live Q&amp;A after every Son of a Butch episode.', 'Exclusive access to live Son of a Butch recordings with special guests.'),
    # No TeamCH3 phone app: TeamCH3 is on the web
    ("Now it's on your phone.", "Now it's yours."),
    ('INSIDE THE APP', 'INSIDE TEAMCH3'),
    ('One tap, two feeds', 'One click, two feeds'),
    # Basecamp codes, as in the community sidebar (the Paddock codes are gone)
    ('>P1</span>HOME BASECAMP · UAE + EUROPE', '>DU</span>HOME BASECAMP · UAE + EUROPE'),
    ('>P2</span>HOME BASECAMP · THAILAND + ASIA', '>TH</span>HOME BASECAMP · THAILAND + ASIA'),
    ('>P3</span>HOME BASECAMP · FLORIDA + NORTH AMERICA', '>FL</span>HOME BASECAMP · FLORIDA + NORTH AMERICA'),
    ('>POD</span>OPEN COMMUNITY · GLOBAL', '>SB</span>OPEN COMMUNITY · GLOBAL'),
    ('>JR</span>GLOBAL JUNIOR BASECAMP · ALL ACADEMIES', '>JB</span>GLOBAL JUNIOR BASECAMP · ALL ACADEMIES'),
    ('height:96px;width:auto;margin-left:-14px', 'height:96px;width:auto;margin-left:-2px'),  # the new mark has no padding to offset
]
# Dubai and Thailand cards: swap the "Head Coach · Academy Coach" placeholders for the head coach, laid out like TeamFLO's
COACH = ('<span style="display:flex;align-items:center;gap:8px;font:400 17px/1 \'Barlow Condensed\'">'
         '<span style="width:22px;height:22px;border-radius:11px;background:%s;flex:none"></span>%s <b style="font-weight:700;text-transform:uppercase">%s</b></span>')
COACH_LABEL = '<span style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.1em;color:%s;align-self:center">%s</span>'
for dot, first, last, label, color in [('#253746', 'Mike', 'Bolt', 'HEAD COACH · CH3 DUBAI', '#fff'),
                                       ('#E04E39', 'Joe', 'Marshall', 'HEAD COACH · CH3 THAILAND', '#A6B1BA')]:
    EDITS.append((COACH % (dot, 'Head', 'Coach') + COACH % (dot, 'Academy', 'Coach'),
                  COACH % (dot, first, last) + COACH_LABEL % (color, label)))
for a, b in EDITS:
    a2 = a.replace('’', "'") if a.replace('’', "'") in t else a
    n = t.count(a2)
    assert n >= 1, 'edit not found: ' + a[:60]
    t = t.replace(a2, b)

class Raw(str):
    """A value that is inserted as HTML, not text."""

def raw(s): return Raw(s)
def span(key, text, extra=''): return raw('<span data-ch3="%s"%s>%s</span>' % (key, extra, H.escape(str(text))))

# ---- data (static snapshot of the design's renderVals, with the updates above) ----
SHOTS = [
    ('7-IRON', '175', 89.6, 123.4, 16.8, 7020, 178, -2, 'Hold the finish. Let the ball tell you.'),
    ('7-IRON', '175', 89.9, 124.1, 16.4, 6890, 179, 1, 'Same again. Pick a smaller target.'),
    ('7-IRON', '165', 86.2, 118.0, 17.9, 7410, 166, -1, 'Three-quarter. Flight it under the wind.'),
    ('7-IRON', '165', 86.5, 118.6, 17.2, 7280, 167, 3, 'Start line first. Curve second.'),
    ('DRIVER', 'FWY', 117.8, 173.9, 11.6, 2480, 289, -6, 'Tee it higher. Hit up on it.'),
    ('DRIVER', 'FWY', 118.4, 175.2, 12.4, 2310, 294, 4, 'That one plays. Full routine on the next.'),
    ('DRIVER', 'FWY', 118.1, 174.6, 12.1, 2390, 292, -2, 'Commit. Pick the line and go.'),
    ('WEDGE', '95', 76.3, 94.8, 29.4, 9850, 96, 0, 'Last ball like it is the 72nd hole.'),
]
CUR = 2  # the still the page shows before any script runs
def dot_pos(sh):
    club, target, carry, off = sh[0], sh[1], sh[6], sh[7]
    rel = carry - 291 if club == 'DRIVER' else carry - 95 if club == 'WEDGE' else carry - int(target) - 2
    return 50 + off * 4.5, 50 - rel * 9
def dot_html(i, last):
    x, y = dot_pos(SHOTS[i])
    st = ('position:absolute;left:%s%%;top:%s%%;width:%dpx;height:%dpx;border-radius:8px;background:%s;opacity:%s;border:%s;transform:translate(-50%%,-50%%)'
          % (round(x, 2), round(y, 2), 16 if last else 10, 16 if last else 10, '#E04E39' if last else '#fff', 1 if last else .55, '2px solid #fff' if last else 'none'))
    return '<span data-ch3-dot="%d" style="%s"></span>' % (i, st)

LIVEDOT = raw('<span class="ch3-pulse" style="width:10px;height:10px;border-radius:5px;background:#fff;box-shadow:0 0 0 3px rgba(255,255,255,.3);display:inline-block;flex:none"></span>')
def bars():
    out = []
    for i, w in enumerate([150, 96, 52, 24]):
        bg = '#E04E39' if i == 0 else 'rgba(224,78,57,%s)' % round(0.75 - i * 0.2, 2)
        out.append('<span class="ch3-bar" style="display:block;height:7px;width:%dpx;background:%s;transform-origin:left;animation-delay:%ss"></span>' % (w, bg, round(i * 0.12, 2)))
    return raw(''.join(out))
TICKER_ITEMS = ['LIVE PODCAST RECORDINGS · CH3 + SPECIAL GUESTS', 'NEW: CAM SMITH RANGE SESSION ON FORESIGHT', 'WEEKLY LIVE WEBINARS WITH THE CH3 COACHES',
                'ON TOUR WITH CLAUDE · BEHIND THE ROPES', 'CH3 DUBAI · CH3 THAILAND · TEAMFLO', 'START 4 WEEKS FREE']
def ticker():
    items = ''.join('<span style="display:inline-flex;align-items:center;gap:28px;padding-right:28px;font:600 17px/1 \'Barlow Condensed\';letter-spacing:.14em;white-space:nowrap">%s<span style="width:8px;height:8px;background:#253746;display:inline-block;transform:rotate(45deg)"></span></span>' % H.escape(s) for s in TICKER_ITEMS * 2)
    return raw('<div class="ch3-marquee" style="display:flex;width:max-content">%s</div>' % items)

ELITE_LEFT = 8  # no Elite members yet
FEATS = ['Son of a Butch community', 'Live podcast recordings', 'Global feed', 'Live webinars + course archive', 'Academy home basecamp',
         'On tour with Claude + Coaches’ Room', 'Global Junior Basecamp', 'Direct access to Claude + Ryan']
def tier(pos, flag, name, pitch, price, note, cta, yes, primary, key):
    return {'pos': pos, 'flag': flag, 'name': name, 'pitch': pitch, 'price': price, 'note': note, 'cta': cta,
            'primary': primary, 'secondary': not primary, 'key': key,
            'feats': [{'t': f, 'yes': bool(y), 'no': not y} for f, y in zip(FEATS, yes)]}

ctx = {
    'epNum': '24',
    'myTime': span('tz', '--:--', ' data-tz="local"'), 'dubaiTime': span('tz', '--:--', ' data-tz="Asia/Dubai"'),
    'thaiTime': span('tz', '--:--', ' data-tz="Asia/Bangkok"'), 'floTime': span('tz', '--:--', ' data-tz="America/New_York"'),
    'countShort': span('cd-short', '--:--:--'),
    'lightsLabel': raw('<span style="position:relative;display:inline-block"><span class="ch3-label-a">TEAMCH3 · THE BASECAMP IS OPEN</span>'
                       '<span class="ch3-label-b" style="position:absolute;left:0;top:0;white-space:nowrap">LIGHTS OUT — AND AWAY WE GO</span></span>'),
    'lights': [{'on': False, 'off': True} for _ in range(5)],
    'countdown': [{'v': span('cd-' + k, '--'), 'l': l} for k, l in (('d', 'DAYS'), ('h', 'HRS'), ('m', 'MIN'), ('s', 'SEC'))],
    'liveDot': LIVEDOT, 'ticker': ticker(), 'bars': bars(),
    'offerings': [
        {'n': '01', 'tier': 'PREMIER +', 'title': 'Live webinars', 'hook': 'On the calendar. On the clock.', 'body': 'Scheduled sessions with Claude and the CH3 coaches every week. Ask live, get answered on air.', 'cta': 'SEE THE SCHEDULE'},
        {'n': '02', 'tier': 'PREMIER +', 'title': 'Course archive', 'hook': 'The whole playbook, on demand.', 'body': 'Every course, drill and breakdown we have filmed. Start anywhere. Pick up where you left off.', 'cta': 'BROWSE COURSES'},
        {'n': '03', 'tier': 'ALL TIERS', 'title': 'Live recordings', 'hook': 'Pull up a chair in the studio.', 'body': 'Exclusive access to live Son of a Butch recordings with CH3 and special guests. Watch it happen before it drops.', 'cta': raw('NEXT ONE IN <span data-ch3="cd-hm">--:--</span>')},
        {'n': '04', 'tier': 'PREMIER +', 'title': 'On tour with Claude', 'hook': 'Range-side. Week in, week out.', 'body': 'Behind-the-scenes coaching from tour events and from home. The sessions, the data and the thinking.', 'cta': 'GO INSIDE THE ROPES'},
        {'n': '05', 'tier': 'PREMIER +', 'title': "The Coaches' Room", 'hook': 'Every CH3 coach. One room.', 'body': 'Behind the scenes with the coaches from Dubai, Thailand and TeamFLO: how they diagnose, plan and run a lesson.', 'cta': 'MEET THE COACHES'},
    ],
    'shotNum': span('shot-num', CUR + 1), 'shotTotal': str(len(SHOTS)),
    'cur': {'club': span('club', SHOTS[CUR][0]), 'target': span('target', SHOTS[CUR][1]), 'cue': span('cue', SHOTS[CUR][8])},
    'readouts': [
        {'l': 'CLUB SPEED', 'v': span('ro-cs', '%.1f' % SHOTS[CUR][2]), 'u': 'MPH'},
        {'l': 'BALL SPEED', 'v': span('ro-bs', '%.1f' % SHOTS[CUR][3]), 'u': 'MPH'},
        {'l': 'LAUNCH', 'v': span('ro-la', '%.1f' % SHOTS[CUR][4]), 'u': '°'},
        {'l': 'SPIN', 'v': span('ro-sp', '{:,}'.format(SHOTS[CUR][5])), 'u': 'RPM'},
        {'l': 'CARRY', 'v': span('ro-carry', SHOTS[CUR][6]), 'u': 'YDS'},
    ],
    'progressEl': raw('<div data-ch3="progress" style="height:4px;background:#E04E39;width:16.67%;transition:width .4s linear"></div>'),
    'playLabel': span('play-label', 'PAUSE'),
    'dotEls': raw('<span data-ch3="dots">%s</span>' % ''.join(dot_html(i, i == CUR) for i in range(CUR + 1))),
    'shots': [{'n': str(i + 1), 'club': s[0], 'carry': '%dY' % s[6], 'off': ('R' if s[7] > 0 else 'L' if s[7] < 0 else '') + str(abs(s[7])),
               'active': False, 'inactive': True} for i, s in enumerate(SHOTS)],
    'podPerks': [
        {'n': '1', 't': 'Live recordings.', 'd': 'Watch CH3 and the guest record the episode, before it drops.'},
        {'n': '2', 't': 'Episode threads.', 'd': 'Talk it through with the rest of the community.'},
        {'n': '3', 't': 'The global feed.', 'd': 'What Claude, the coaches and the academies are posting, in one place.'},
        {'n': '4', 't': 'Ask the next guest.', 'd': 'Submit questions before we record.'},
    ],
    'regions': [],  # rebuilt below as a CSS-only picker
    'eliteLeft': str(ELITE_LEFT),
    'seatBar': raw(''.join('<span style="flex:1;height:10px;background:%s"></span>' % ('rgba(255,255,255,.3)' if i < 8 - ELITE_LEFT else '#fff') for i in range(8))),
    'tiers': [
        tier('SB', '4 WEEKS FREE', 'Pod Community', 'For Son of a Butch listeners who want the room behind the mic.', '$49',
             'Free for 4 weeks, then $49/month.', 'START FREE', [1, 1, 1, 0, 0, 0, 0, 0], False, 'pod'),
        tier('JB', 'JUNIORS', 'Junior Basecamp', 'Everything in Premier, plus the Global Junior Basecamp: juniors from every CH3 academy in one place.', '$69',
             'Ages 13–19. Premier access at a junior price.', 'JOIN THE JUNIOR BASECAMP', [1, 1, 1, 1, 1, 1, 1, 0], False, 'junior'),
        tier('PS', 'MOST POPULAR', 'Premier', 'The full basecamp. Your home basecamp, or the one closest to you, plus everything global.', '$99',
             'Includes your academy’s home basecamp.', 'GO PREMIER', [1, 1, 1, 1, 1, 1, 0, 0], True, 'premier'),
        tier('EB', 'LIMITED · BY APPLICATION', 'Elite', 'A direct line to Claude Harmon III and Ryan Crysler, Head Coach of TeamFLO and RC Greenlight.', '$999',
             'Limited spots. %d of 8 remaining.' % ELITE_LEFT, 'APPLY FOR ELITE', [1, 1, 1, 1, 1, 1, 0, 1], False, 'elite'),
    ],
}

# ---- template renderer ----
EXPR = re.compile(r'\{\{\s*([\w.]+)\s*\}\}')
def lookup(path, c):
    v = c
    for part in path.split('.'):
        v = v[part] if isinstance(v, dict) else getattr(v, part)
    return v

soup = BeautifulSoup(t, 'html.parser')
root = soup.find('x-dc').find('div', recursive=False)
out = BeautifulSoup('', 'html.parser')
hover_rules, hover_ids = [], {}

def frag(html_str):
    return list(BeautifulSoup(html_str, 'html.parser').contents)

def render(node, c):
    if isinstance(node, Comment):
        return []
    if isinstance(node, NavigableString):
        s = str(node)
        if '{{' not in s:
            return [NavigableString(s)]
        res, pos = [], 0
        for m in EXPR.finditer(s):
            if m.start() > pos: res.append(NavigableString(s[pos:m.start()]))
            v = lookup(m.group(1), c)
            res.extend(frag(v) if isinstance(v, Raw) else [NavigableString(str(v))])
            pos = m.end()
        if pos < len(s): res.append(NavigableString(s[pos:]))
        return res
    name = node.name
    if name == 'sc-for':
        lst = lookup(EXPR.search(node['list']).group(1), c)
        res = []
        for item in lst:
            c2 = dict(c); c2[node['as']] = item
            for ch in node.children: res.extend(render(ch, c2))
        return res
    if name == 'sc-if':
        if lookup(EXPR.search(node['value']).group(1), c):
            return [r for ch in node.children for r in render(ch, c)]
        return []
    if name == 'image-slot':
        if node.get('id') in SLOT_IMG:
            src, alt, *extra = SLOT_IMG[node['id']]
            style, cls = extra if extra else ('display:block;width:100%;height:100%;object-fit:cover', '')
            return frag('<img%s src="%s" alt="%s" style="%s">' % (' class="%s"' % cls if cls else '', src, H.escape(alt), style))
        if node.get('src'):
            return frag('<img src="%s" alt="" style="display:block;width:100%%;height:100%%;object-fit:cover">' % IMG[node['src']])
        return frag('<div class="ch3-slot" data-slot="%s" style="box-sizing:border-box;width:100%%;height:100%%;min-height:inherit;display:flex;align-items:center;justify-content:center;text-align:center;padding:16px;border:1px dashed currentColor;opacity:.5;font:400 15px/1.3 \'Barlow Condensed\',sans-serif">Photo: %s</div>'
                    % (node.get('id', ''), H.escape(node.get('placeholder', ''))))
    el = out.new_tag(name)
    for k, v in node.attrs.items():
        if k in ('sc-camel-on-click', 'data-screen-label') or k.startswith('hint-'):
            continue
        if k == 'style-hover':
            if v not in hover_ids:
                hover_ids[v] = 'ch3-hv%d' % (len(hover_ids) + 1)
                decl = ';'.join(d.strip() + ' !important' for d in v.split(';') if d.strip())
                hover_rules.append('#ch3-site .%s:hover{%s}' % (hover_ids[v], decl))
            el['class'] = (el.get('class', []) + [hover_ids[v]])
            continue
        if k == 'src' and v in IMG:
            v = IMG[v]
        el[k] = v
    for ch in node.children:
        for r in render(ch, c): el.append(r)
    return [el]

page = render(root, ctx)[0]
page['id'] = 'ch3-site'

def find_style(tag, needle, nth=0):
    hits = [e for e in page.find_all(tag) if needle in e.get('style', '')]
    assert hits, 'not found: %s %s' % (tag, needle)
    return hits[nth]
def add_class(e, *cls):
    e['class'] = e.get('class', []) + list(cls)

# ---- lights: animate with CSS instead of React state ----
hero_lamps = [e for e in page.find_all('div') if 'width:44px;height:96px' in e.get('style', '')]
assert len(hero_lamps) == 5
for i, d in enumerate(hero_lamps):
    for s in d.find_all('span'): add_class(s, 'ch3-lamp', 'ch3-lamp%d' % i)
final_lamps = [e for e in page.find_all('span') if 'width:30px;height:30px;border-radius:15px' in e.get('style', '')]
assert len(final_lamps) == 5
for i, s in enumerate(final_lamps): add_class(s, 'ch3-lamp', 'ch3-lamp-light', 'ch3-lamp%d' % i)

# ---- range session: rows become buttons the optional script can drive ----
rows = [b for b in page.find_all('button') if 'grid-template-columns:30px 1fr 60px 60px' in b.get('style', '')]
assert len(rows) == 8
for i, b in enumerate(rows):
    b['type'] = 'button'; b['data-ch3-shot'] = str(i); add_class(b, 'ch3-shot')
    if i == CUR: add_class(b, 'is-active')
play = [b for b in page.find_all('button') if b.find(attrs={'data-ch3': 'play-label'})]
assert len(play) == 1
play[0]['type'] = 'button'; play[0]['data-ch3'] = 'play'

# ---- region picker: CSS-only (radio + labels), defaults to the Americas ----
old = find_style('div', 'grid-template-columns:minmax(0,1.1fr) minmax(0,2fr)')
REG = [('am', 'THE AMERICAS', 'TeamFLO'), ('eu', 'EUROPE · MIDDLE EAST · AFRICA', 'CH3 Dubai'), ('as', 'ASIA · PACIFIC', 'CH3 Thailand')]
radios = ''.join('<input type="radio" name="ch3-region" id="ch3-reg-%s" class="ch3-radio"%s>' % (k, ' checked' if i == 0 else '') for i, (k, _, _) in enumerate(REG))
labels = ''.join(
    '<label for="ch3-reg-%s" class="ch3-reg ch3-reg-%s">'
    '<span class="ch3-reg-where" style="font:600 13px/1.2 \'Barlow Condensed\';letter-spacing:.14em">%s</span>'
    '<span class="ch3-reg-arrow" style="font:400 18px/1 Anton,sans-serif">↓</span>'
    '<span style="font:400 28px/1 Anton,sans-serif;text-transform:uppercase">%s</span>'
    '<span class="ch3-reg-on" style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.12em">YOUR HOME BASECAMP ✓</span>'
    '<span class="ch3-reg-off" style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.12em">SELECT</span>'
    '</label>' % (k, k, H.escape(w), H.escape(a)) for k, w, a in REG)
new = frag(
    '<div class="ch3-region-box" style="margin-top:20px;background:#253746;color:#fff;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,2fr);gap:0">'
    '<div class="ch3-region-intro" style="padding:28px;border-right:1px solid #384B5B">'
    '<div style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.14em;color:#F47C67">WHERE DO YOU LIVE?</div>'
    '<div style="font:400 32px/1 Anton,sans-serif;text-transform:uppercase;margin-top:10px">There’s a basecamp near you.</div>'
    '<div style="font:400 17px/1.35 \'Barlow Condensed\';color:#CDD4DA;margin-top:10px">Junior, Premier and Elite members join the home basecamp closest to where they live.</div>'
    '</div><div class="ch3-region-pick">%s<div class="ch3-regions" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));height:100%%">%s</div></div></div>' % (radios, labels))
old.replace_with(*new)

# ---- links ----
for a in page.find_all('a'):
    txt = a.get_text(strip=True).upper()
    if txt in ('LOG IN',):
        a['href'] = LOGIN
for a in page.find_all('a'):
    if a.get_text(strip=True) == 'Log in': a['href'] = LOGIN
cards = page.find_all('div', style=lambda s: s and s.startswith('position:relative;display:flex;flex-direction:column;background:#fff;color:#253746;overflow:hidden'))
assert len(cards) == 4
for card, tr in zip(cards, ctx['tiers']):
    a = card.find_all('a')[-1]
    a['href'] = '#tiers'; a['data-checkout'] = tr['key']
elite = [a for a in page.find_all('a') if a.get_text(strip=True) == 'APPLY FOR ELITE' and a.get('href') == '#']
for a in elite: a['href'] = '#tiers'; a['data-checkout'] = 'elite'

# ---- responsive hooks (the design is desktop-first) ----
def hook(tag, needle, cls, nth=None):
    hits = [e for e in page.find_all(tag) if needle in e.get('style', '')]
    assert hits, 'hook not found: ' + needle
    for e in (hits if nth is None else [hits[nth]]): add_class(e, cls)
hook('header', 'position:sticky;top:0', 'ch3-nav')
hook('nav', 'display:flex;gap:26px', 'ch3-navlinks')
hook('div', 'position:sticky;top:72px', 'ch3-strip')
hook('div', 'grid-template-rows:auto auto;grid-auto-flow:column', 'ch3-clocks')
hook('div', 'padding:96px 40px 150px', 'ch3-hero-grid')
hook('section', 'padding:110px 40px', 'ch3-sec')
hook('section', 'padding:120px 40px', 'ch3-sec')
hook('div', 'grid-template-columns:repeat(auto-fit,minmax(380px,1fr))', 'ch3-pod-grid')
hook('div', 'grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr))', 'ch3-session-grid')
hook('div', 'grid-template-columns:repeat(5,minmax(0,1fr));gap:2px', 'ch3-readouts')
hook('div', 'position:relative;min-height:560px', 'ch3-video')
hook('div', 'grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr))', 'ch3-academies')
hook('div', 'grid-template-columns:minmax(0,1fr) 260px', 'ch3-feed-grid')
hook('div', 'grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)', 'ch3-elite')
hook('div', 'grid-template-columns:minmax(0,2fr) repeat(3,minmax(0,1fr))', 'ch3-footer-grid')
hook('div', 'grid-template-columns:repeat(4,minmax(0,1fr));gap:2px', 'ch3-count')
for a in page.find_all('a'):
    if 'min-height:420px' in a.get('style', ''): add_class(a, 'ch3-offer')
hook('div', 'position:relative;min-height:300px;margin:22px 22px 22px 0', 'ch3-junior-photo')
hook('footer', 'padding:56px 40px 40px', 'ch3-foot')

# ---- pinned bars: nav + live strip in one wrapper, CSS sticky with a script fallback for builder hosts ----
nav_el = page.find('header', class_='ch3-nav'); strip_el = page.find('div', class_='ch3-strip')
assert 'position:sticky;top:0;z-index:30;' in nav_el['style'] and 'position:sticky;top:72px;z-index:29;' in strip_el['style']
nav_el['style'] = nav_el['style'].replace('position:sticky;top:0;z-index:30;', 'position:relative;')
strip_el['style'] = strip_el['style'].replace('position:sticky;top:72px;z-index:29;', 'position:relative;')
mark = out.new_tag('div'); mark['class'] = ['ch3-bars-mark']
bars_el = out.new_tag('div'); bars_el['class'] = ['ch3-bars']
nav_el.insert_before(mark); mark.insert_after(bars_el)
bars_el.append(nav_el.extract()); bars_el.append(strip_el.extract())

# ---- CSS ----
lamp_css = []
for i in range(5):
    on, off = (i + 1) / 12 * 100, 9 / 12 * 100
    lamp_css.append('@keyframes ch3lamp%d{0%%,%.2f%%{background:var(--ch3-off);box-shadow:none}%.2f%%,%.2f%%{background:#E04E39;box-shadow:0 0 var(--ch3-glow) #E04E39}%.2f%%,100%%{background:var(--ch3-off);box-shadow:none}}'
                    % (i, on - .01, on, off - .01, off))
    lamp_css.append('#ch3-site .ch3-lamp%d{animation:ch3lamp%d 5.4s infinite}' % (i, i))
CSS = r'''
#ch3-site{font-size:16px;line-height:normal;-webkit-text-size-adjust:100%;text-align:left;overflow-x:clip}
#ch3-site,#ch3-site *,#ch3-site *::before,#ch3-site *::after{box-sizing:content-box}
#ch3-site a{color:#C9432F;text-decoration:none}#ch3-site a:hover{color:#B33826}
#ch3-site img{max-width:none}
#ch3-site button{font-family:inherit;margin:0;-webkit-appearance:none;appearance:none}
#ch3-site [class*="ch3-hv"]{transition:background-color .18s,color .18s,transform .2s,box-shadow .2s}
@keyframes ch3bar{0%{transform:scaleX(0);opacity:0}25%{transform:scaleX(1);opacity:1}80%{opacity:1}100%{transform:scaleX(1);opacity:0}}
@keyframes ch3marquee{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes ch3pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes ch3pop{0%{transform:translate(-50%,-50%) scale(0)}70%{transform:translate(-50%,-50%) scale(1.5)}100%{transform:translate(-50%,-50%) scale(1)}}
@keyframes ch3labela{0%,74.99%{opacity:1}75%,100%{opacity:0}}
@keyframes ch3labelb{0%,74.99%{opacity:0}75%,100%{opacity:1}}
#ch3-site .ch3-bar{animation:ch3bar 1.8s cubic-bezier(.2,.8,.2,1) infinite}
#ch3-site .ch3-marquee{animation:ch3marquee 40s linear infinite}
#ch3-site .ch3-pulse{animation:ch3pulse 1.2s ease-in-out infinite}
#ch3-site .ch3-label-a{animation:ch3labela 5.4s infinite}
#ch3-site .ch3-label-b{animation:ch3labelb 5.4s infinite;opacity:0}
#ch3-site .ch3-bars-mark{height:0}
#ch3-site .ch3-bars{position:sticky;top:0;z-index:40}
#ch3-site .ch3-bars.is-js{position:relative;will-change:transform}
#ch3-site .ch3-lamp{--ch3-off:#1E2D3A;--ch3-glow:18px}
#ch3-site .ch3-lamp-light{--ch3-off:#E8ECEF;--ch3-glow:14px}
''' + '\n'.join(lamp_css) + r'''
#ch3-site .ch3-shot.is-active{background:#C9432F!important;color:#fff!important;font-weight:600!important;border-bottom-color:transparent!important}
#ch3-site .ch3-shot.is-active span:first-child{color:#fff!important}
#ch3-site [data-ch3-dot]:last-child{animation:ch3pop .5s cubic-bezier(.2,.8,.2,1)}
#ch3-site .ch3-radio{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px;margin:0}
#ch3-site .ch3-reg{display:flex;flex-direction:column;gap:8px;padding:28px 22px;cursor:pointer;color:#fff;background:transparent;border-left:1px solid #384B5B;transition:background-color .18s}
#ch3-site .ch3-reg:first-child{border-left:none}
#ch3-site .ch3-reg:hover{background:#1E2D3A}
#ch3-site .ch3-reg .ch3-reg-where,#ch3-site .ch3-reg .ch3-reg-off{color:#A6B1BA}
#ch3-site .ch3-reg .ch3-reg-arrow{color:#F47C67}
#ch3-site .ch3-reg .ch3-reg-on{display:none}
#ch3-reg-am:checked~.ch3-regions .ch3-reg-am,#ch3-reg-eu:checked~.ch3-regions .ch3-reg-eu,#ch3-reg-as:checked~.ch3-regions .ch3-reg-as{background:#C9432F}
#ch3-reg-am:checked~.ch3-regions .ch3-reg-am *,#ch3-reg-eu:checked~.ch3-regions .ch3-reg-eu *,#ch3-reg-as:checked~.ch3-regions .ch3-reg-as *{color:#fff}
#ch3-reg-am:checked~.ch3-regions .ch3-reg-am .ch3-reg-on,#ch3-reg-eu:checked~.ch3-regions .ch3-reg-eu .ch3-reg-on,#ch3-reg-as:checked~.ch3-regions .ch3-reg-as .ch3-reg-on{display:block}
#ch3-reg-am:checked~.ch3-regions .ch3-reg-am .ch3-reg-off,#ch3-reg-eu:checked~.ch3-regions .ch3-reg-eu .ch3-reg-off,#ch3-reg-as:checked~.ch3-regions .ch3-reg-as .ch3-reg-off{display:none}
#ch3-site .ch3-radio:focus-visible~.ch3-regions{outline:2px solid #F47C67;outline-offset:2px}
/* photo slots still waiting for a photo: no placeholder caption on the live page */
#ch3-site .ch3-slot{font-size:0!important;border:0!important;opacity:1!important;background:rgba(128,128,128,.12)}
#ch3-site .ch3-slot[data-slot="hero-claude"],#ch3-site .ch3-slot[data-slot="session-cam"]{display:none!important}
@media (max-width:1100px){
#ch3-site .ch3-navlinks{display:none!important}
#ch3-site .ch3-clocks{display:none!important}
}
@media (max-width:860px){
#ch3-site .ch3-nav{padding:0 16px!important;gap:12px!important}
#ch3-site .ch3-nav img{height:40px!important}
#ch3-site .ch3-strip{padding:10px 16px!important}
#ch3-site .ch3-sec{padding:72px 16px!important}
#ch3-site .ch3-hero-grid{grid-template-columns:minmax(0,1fr)!important;padding:56px 16px 120px!important;gap:36px!important}
#ch3-site .ch3-pod-grid,#ch3-site .ch3-feed-grid,#ch3-site .ch3-elite,#ch3-site .ch3-region-box{grid-template-columns:minmax(0,1fr)!important;gap:28px!important}
#ch3-site .ch3-region-box,#ch3-site .ch3-elite{gap:0!important}
#ch3-site .ch3-region-intro{border-right:none!important;border-bottom:1px solid #384B5B}
#ch3-site .ch3-regions{grid-template-columns:minmax(0,1fr)!important}
#ch3-site .ch3-reg{border-left:none;border-top:1px solid #384B5B}
#ch3-site .ch3-reg:first-child{border-top:none}
#ch3-site .ch3-academies{grid-template-columns:minmax(0,1fr)!important}
#ch3-site .ch3-junior-photo{margin:0 22px 22px!important;min-height:220px!important}
#ch3-site .ch3-readouts{grid-template-columns:repeat(3,minmax(0,1fr))!important}
#ch3-site .ch3-video{min-height:620px!important}
#ch3-site .ch3-offer{min-height:0!important}
#ch3-site .ch3-footer-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important}
#ch3-site .ch3-footer-grid>div:first-child{grid-column:1/-1}
#ch3-site .ch3-foot{padding:48px 16px 32px!important}
#ch3-site h1,#ch3-site h2{overflow-wrap:anywhere}
#ch3-site .ch3-slot[data-slot="hero-claude"],#ch3-site .ch3-slot[data-slot="session-cam"]{display:none!important}
#ch3-site .ch3-hero-photo{width:100%!important;opacity:.35}
}
@media (max-width:520px){
#ch3-site .ch3-nav a[href="#tiers"]{padding:12px 12px!important;font-size:14px!important}
#ch3-site .ch3-count>div>div:first-child{font-size:30px!important}
}
@media (prefers-reduced-motion:reduce){#ch3-site *{animation:none!important;transition:none!important}#ch3-site .ch3-label-b{display:none}}
''' + '\n'.join(hover_rules)

JS = r'''
(function(){
var root=document.getElementById('ch3-site');if(!root)return;
function q(s){return root.querySelectorAll(s)}
function p(n){return (n<10?'0':'')+n}
function nextLive(now){var t=new Date(Date.UTC(now.getUTCFullYear(),now.getUTCMonth(),now.getUTCDate(),15,0,0));t.setUTCDate(t.getUTCDate()+((4-t.getUTCDay()+7)%7));if(t<=now)t.setUTCDate(t.getUTCDate()+7);return Math.max(0,Math.floor((t-now)/1000))}
function tick(){var now=new Date();
 q('[data-ch3="tz"]').forEach(function(e){var z=e.getAttribute('data-tz');try{e.textContent=now.toLocaleTimeString('en-GB',z==='local'?{hour:'2-digit',minute:'2-digit'}:{timeZone:z,hour:'2-digit',minute:'2-digit'})}catch(err){}});
 var s=nextLive(now),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),x=s%60;
 var v={'cd-d':p(d),'cd-h':p(h),'cd-m':p(m),'cd-s':p(x),'cd-short':(d?d+'D ':'')+p(h)+':'+p(m)+':'+p(x),'cd-hm':p(h)+':'+p(m)};
 Object.keys(v).forEach(function(k){q('[data-ch3="'+k+'"]').forEach(function(e){e.textContent=v[k]})});}
tick();setInterval(tick,1000);
var S=SHOTS_JSON,cur=CUR_JSON,sub=0,playing=true;
function pos(sh){var rel=sh[0]==='DRIVER'?sh[6]-291:sh[0]==='WEDGE'?sh[6]-95:sh[6]-Number(sh[1])-2;return[(50+sh[7]*4.5)+'%',(50-rel*9)+'%']}
function set(k,t){q('[data-ch3="'+k+'"]').forEach(function(e){e.textContent=t})}
function show(i){cur=i;sub=0;var sh=S[i];
 set('shot-num',i+1);set('club',sh[0]);set('target',sh[1]);set('cue',sh[8]);
 set('ro-cs',sh[2].toFixed(1));set('ro-bs',sh[3].toFixed(1));set('ro-la',sh[4].toFixed(1));set('ro-sp',sh[5].toLocaleString('en-US'));set('ro-carry',sh[6]);
 q('.ch3-shot').forEach(function(b,j){b.classList.toggle('is-active',j===i)});
 var box=root.querySelector('[data-ch3="dots"]');if(box){var h='';for(var j=0;j<=i;j++){var L=j===i,xy=pos(S[j]);h+='<span data-ch3-dot="'+j+'" style="position:absolute;left:'+xy[0]+';top:'+xy[1]+';width:'+(L?16:10)+'px;height:'+(L?16:10)+'px;border-radius:8px;background:'+(L?'#E04E39':'#fff')+';opacity:'+(L?1:.55)+';border:'+(L?'2px solid #fff':'none')+';transform:translate(-50%,-50%)"></span>'}box.innerHTML=h}
 bar();}
function bar(){var b=root.querySelector('[data-ch3="progress"]');if(b)b.style.width=((sub+1)/6*100)+'%'}
q('.ch3-shot').forEach(function(b){b.addEventListener('click',function(){show(Number(b.getAttribute('data-ch3-shot')))})});
var pb=root.querySelector('[data-ch3="play"]');if(pb)pb.addEventListener('click',function(){playing=!playing;set('play-label',playing?'PAUSE':'PLAY')});
var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;if(still){playing=false;set('play-label','PLAY')}
setInterval(function(){if(!playing)return;sub++;if(sub>=6){show((cur+1)%S.length)}else bar()},500);
var bars=root.querySelector('.ch3-bars'),mark=root.querySelector('.ch3-bars-mark');
if(bars&&mark){
 var frame=null,pdoc=null;
 try{if(window.self!==window.top&&window.frameElement){frame=window.frameElement;pdoc=frame.ownerDocument}}catch(e){frame=null;pdoc=null}
 function findScroller(el,doc){var w=doc.defaultView||window;for(var n=el&&el.parentElement;n&&n!==doc.body&&n!==doc.documentElement;n=n.parentElement){if(/(auto|scroll|overlay)/.test(w.getComputedStyle(n).overflowY)&&n.scrollHeight>n.clientHeight+1)return n}return null}
 var mode=frame?'js':'auto',sc;
 function edge(){if(sc===undefined)sc=frame?findScroller(frame,pdoc):findScroller(root,document);var vt=sc?sc.getBoundingClientRect().top:0;
  if(frame){var fr=frame.getBoundingClientRect(),k=(fr.height/(frame.offsetHeight||fr.height))||1;return Math.max(0,(vt-fr.top)/k)}return vt}
 function place(){if(mode==='sticky')return;var nat=mark.getBoundingClientRect().top,e=edge(),y=e-nat;
  if(mode==='auto'){if(y<=20)return;if(Math.abs(bars.getBoundingClientRect().top-e)<2){mode='sticky';return}mode='js';bars.classList.add('is-js')}
  var max=root.getBoundingClientRect().bottom-nat-bars.offsetHeight;y=Math.max(0,Math.min(y,max));bars.style.transform=y?'translateY('+y+'px)':''}
 if(frame)bars.classList.add('is-js');
 var o={passive:true,capture:true};document.addEventListener('scroll',place,o);window.addEventListener('resize',function(){sc=undefined;place()});
 if(pdoc){pdoc.addEventListener('scroll',place,o);try{pdoc.defaultView.addEventListener('resize',function(){sc=undefined;place()})}catch(e){}}
 place();
}
})();
'''.replace('SHOTS_JSON', json.dumps([list(s) for s in SHOTS])).replace('CUR_JSON', str(CUR))

head = ('<!-- TeamCH3 membership page · for Circle\'s website builder · built Oct 15 2026 from "TeamCH3_Membership_Site_1.html".\n'
        'Paste everything into one custom HTML / code block. Images are hosted on Circle (assets-v2.circle.so).\n'
        'Buttons marked data-checkout="pod|junior|premier|elite" still point to #tiers: swap in the checkout links once the paywalls exist. -->\n')
fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@400;600;700&display=swap">\n'
html_out = head + fonts + '<style>' + re.sub(r'\n+', '\n', CSS).strip() + '</style>\n' + str(page) + '\n<script>' + JS.strip() + '</script>\n'
assert '{{' not in html_out, 'unrendered expression left'
assert 'sc-' not in re.sub(r'data-[\w-]+', '', html_out).replace('desc-', ''), 'directive left'
open(OUT, 'w', encoding='utf-8').write(html_out)
print('wrote', OUT, len(html_out), 'bytes;', len(hover_rules), 'hover rules')
