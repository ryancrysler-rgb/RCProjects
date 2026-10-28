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
    # tall photo: keep Claude in the upper half, above the cue text
    'session-cam': (CDN + '7j18iax3nfe4yh5w5pa6k9qt4n59', 'Claude Harmon III on the putting green, with players behind',
                    'display:block;width:100%;height:100%;object-fit:cover;object-position:50% 62%', ''),
    # Claude stands on the left of this photo, so it fills the right half of the hero, clear of the headline
    # the cap's P and side logo are replaced by the CH3 mark (brand/Claude range-side (CH3 cap).jpg)
    'hero-claude': (CDN + 'd85q2vrd3kilwhzo17w9x39764zx', 'Claude Harmon III range-side at a tour event, in a CH3 cap',
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
    'c7b5244b-de71-4c97-92ac-40d0afaf1a74': CDN + '3hy9hkputoabzbwq6hcweyd3sw24',  # a Premier · CH3 Dubai test member's Feed (live Circle view, Oct 27)
}
LOGIN = 'https://ch3.circle.so/sign_in'

# ---- beta: membership is by invitation until the paywalls (Stripe) are live ----
# At launch: BETA = False, and put each paywall's checkout link in CHECKOUT. Every join button then reads
# "START 2 WEEKS FREE" and goes to its checkout.
BETA = True
CTA = 'REQUEST AN INVITE' if BETA else 'START 2 WEEKS FREE'
INVITE_EMAIL = 'rcrysler@floridian.cc'
CHECKOUT = {'pod': '#tiers', 'junior': '#tiers', 'premier': '#tiers', 'elite': '#tiers'}
MEMBERSHIP_NAMES = {'pod': 'Pod Community', 'junior': 'Junior Basecamp', 'premier': 'Premier', 'elite': 'Elite'}
def invite_url(key=None):
    from urllib.parse import quote
    if key == 'elite':
        subj, body = 'TeamCH3 Elite application', ('Hi TeamCH3,\n\nI would like to apply for Elite.\n\nName:\nHome city:\n'
                                                   'My game (handicap, recent results):\nMy goals this season:\nMy schedule:\n')
    else:
        what = MEMBERSHIP_NAMES.get(key, 'Pod Community, Junior Basecamp or Premier')
        subj = 'TeamCH3 invite request' + (' · ' + MEMBERSHIP_NAMES[key] if key else '')
        body = ('Hi TeamCH3,\n\nI would like an invite to TeamCH3.\n\nName:\nHome city:\nMembership: %s\n'
                'Junior (13 to 19) or adult:\n' % what)
    return 'mailto:%s?subject=%s&body=%s' % (INVITE_EMAIL, quote(subj), quote(body))
def join_url(key=None):
    return invite_url(key) if BETA or key == 'elite' else CHECKOUT[key or 'premier']

# ---- the live calendar (UTC), copied from the Circle events; the countdowns run off it. Refresh before each paste. ----
# (start, minutes, kind, short title for the strip, card title, card line, is a live podcast recording)
EVENTS = [
    ('2026-10-28T16:00:00Z', 120, 'LIVE RECORDING', 'CLAUDE + CAM SMITH', 'Son of a Butch Live',
     'Claude with Cam Smith and Ryan Crysler, recorded live for members.', True),
    ('2026-10-28T23:00:00Z', 60, 'BASECAMP SPOTLIGHT', 'INSIDE CH3 DUBAI', 'Inside CH3 Dubai',
     'Claude and Head Coach Mike Bolt on what the Dubai squad is working on.', False),
    ('2026-11-05T00:00:00Z', 60, 'BASECAMP SPOTLIGHT', 'INSIDE CH3 THAILAND', 'Inside CH3 Thailand',
     'Claude and Head Coach Joe Marshall on course strategy and how the squad trains.', False),
    ('2026-11-12T00:00:00Z', 60, 'BASECAMP SPOTLIGHT', 'INSIDE TEAMFLO', 'Inside TeamFLO',
     'Claude and Head Coach Ryan Crysler on turning round data into decisions.', False),
    ('2026-11-19T00:00:00Z', 60, 'JUNIOR NIGHT', 'JUNIORS + PARENTS', 'Junior night with Claude',
     'Claude on the pre-round routine, with questions from juniors in every basecamp.', False),
]
NO_EVENT = ('', 0, 'COMING UP', 'NEW DATES SOON', 'Next live session', 'New dates are announced in the community.', False)
def next_event(rec=False):
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    for e in EVENTS:
        start = datetime.fromisoformat(e[0].replace('Z', '+00:00'))
        if start + timedelta(minutes=e[1]) > now and (e[6] or not rec):
            return e
    return None

t = open(SRC, encoding='utf-8').read()
t = t[:t.find('<script type="text/x-dc"')]

# ---- copy updates: the decisions made after the design (pricing, tiers, basecamps, feed) ----
EDITS = [
    ('Full access for 4 weeks, then from $50/month.', '2 weeks free, then from $49/month.'),
    # the free trial is 2 weeks (14 days), not the design's 4 weeks
    ('Cancel any time before day 28 and pay nothing.', 'Cancel any time before day 14 and pay nothing.'),
    ('ALL TIERS · 4 WEEKS FREE', 'ALL TIERS · 2 WEEKS FREE'),
    ('GET IN THE FEED — 4 WEEKS FREE', 'GET IN THE FEED — 2 WEEKS FREE'),
    ('JOIN THE POD COMMUNITY — 4 WEEKS FREE', 'JOIN THE POD COMMUNITY — 2 WEEKS FREE'),
    ('START 4 WEEKS FREE', 'START 2 WEEKS FREE'),
    ('Your 4 weeks start now.', 'Your 2 weeks start now.'),
    ('Then $50/month. Cancel any time.', 'Then $49/month. Cancel any time.'),
    ('Every player from every CH3 academy is on board, alongside the Son of a Butch community. Everyone shares the Global Basecamp. Each academy also has its own home basecamp: your coaches, your squad, your range. Pick the one that feels like home.',
     'Every player from every CH3 academy is on board, alongside the Son of a Butch community. Everyone shares the Global Basecamp. Each academy also has its own home basecamp: your coaches, your squad, your range. You join the one closest to where you live, and it’s where you train with us in person.'),
    ('PREMIER + ELITE MEMBERS', 'JUNIOR, PREMIER + ELITE'),
    ('Stories from the coaches, swing videos with the Foresight numbers on screen, and the conversation. Switch between the Global Basecamp and your home basecamp in one tap.',
     'Featured posts from Claude and the coaches, the live calendar and the conversation. Switch between the Global Basecamp and your home basecamp in one click.'),
    ('teamch3.com/basecamp', 'ch3.circle.so/feed'),
    ('Coach stories', 'Featured from the coaches'),
    ('Claude, Ryan and your academy coaches. Live sessions ring orange.', 'The best posts from Claude, Ryan and every academy, at the top of the Global Basecamp.'),
    ('Data on the swing', 'Your data, coached'),
    ('Foresight numbers sit right on the video. Post your own.', 'Send your golf data to RC Greenlight, or ask a coach, straight from the feed.'),
    ('Every membership starts with 4 weeks of full access. Choose where you land after that.',
     'Every membership except Elite starts with 2 weeks free. Cancel before day 14 and pay nothing.'),
    ('Prices in USD, billed monthly. Not at a CH3 academy? You’re welcomed into the closest home basecamp: North America → TeamFLO, Europe → CH3 Dubai, Asia → CH3 Thailand. Elite is limited and by application.',
     'Prices in USD, billed monthly, or pay for the year and get 12 months for the price of 10. Your home basecamp is the academy closest to where you live: the Americas → TeamFLO, Europe, the Middle East and Africa → CH3 Dubai, Asia and the Pacific → CH3 Thailand. Elite is limited, by application, with no free trial.'),
    ('alt="TeamCH3 Global Basecamp feed"', 'alt="A TeamCH3 member\'s feed in Circle, with the Global, CH3 Dubai and Son Of A Butch basecamps"'),
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
    # What's Inside cards: the tag ("JUNIOR · PREMIER · ELITE") gets its own line above the number, so it never wraps
    ('<div style="display:flex;justify-content:space-between;align-items:center"><span style="font:400 56px/1 Anton,sans-serif;color:#E04E39">{{ o.n }}</span>'
     '<span style="font:600 12px/1 \'Barlow Condensed\';letter-spacing:.12em;color:#fff;background:#C9432F;padding:6px 8px;border-radius:2px">{{ o.tier }}</span></div>',
     '<div style="display:flex;flex-direction:column-reverse;align-items:flex-start;gap:14px"><span style="font:400 56px/1 Anton,sans-serif;color:#E04E39">{{ o.n }}</span>'
     '<span style="font:600 12px/1 \'Barlow Condensed\';letter-spacing:.12em;color:#fff;background:#C9432F;padding:6px 8px;border-radius:2px;white-space:nowrap">{{ o.tier }}</span></div>'),
    # no course archive in TeamCH3: on-demand sessions live in Premier Sessions
    (' The full course archive.', ''),
    # hero line: play better golf first, then Claude live (Ryan, Oct 27)
    ('Claude Harmon III on tour and at home. Exclusive access to live Son of a Butch recordings with special guests. The coaches from Dubai, Thailand and TeamFLO. One membership.',
     'Play better golf with Claude and the CH3 coaches from Dubai, Thailand and TeamFLO, wherever you live. Then go live with Claude: Son of a Butch recordings and his updates from tour. One membership.'),
    ('<a href="#grid" style="color:#A6B1BA">Course archive</a>', '<a href="#grid" style="color:#A6B1BA">Premier Sessions</a>'),
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
EDITS += [
    # the live strip, the hero card and the pod card follow the real calendar (EVENTS), not a weekly guess
    ('EP {{ epNum }} <span style="color:#536676">|</span> LIVE RECORDING</span>', 'NEXT LIVE <span style="color:#536676">|</span> {{ evKind }}</span>'),
    ('CH3 + SPECIAL GUEST <span', '{{ evShort }} <span'),
    ('<span>LIVE RECORDING</span>', '<span>{{ evKind }}</span>'),
    ('In the studio with CH3</div>', '{{ evTitle }}</div>'),
    ('Exclusive access to the next Son of a Butch recording, live, with CH3 and a special guest.', '{{ evBlurb }}'),
    ('LIVE RECORDING IN</div><div style="font:400 30px/1 Anton,sans-serif;font-variant-numeric:tabular-nums;margin-top:6px">{{ countShort }}',
     'NEXT RECORDING</div><div style="font:400 30px/1 Anton,sans-serif;font-variant-numeric:tabular-nums;margin-top:6px">{{ recShort }}'),
    ('Next live session in {{ countShort }}.', 'Next live session: {{ countShort }}'),
    # pricing: the annual price on every card, and Elite as a fixed eight seats
    ('<div style="font:600 15px/1.3 \'Barlow Condensed\';color:#C9432F;margin-top:8px">{{ t.note }}</div>',
     '<div style="font:600 15px/1.3 \'Barlow Condensed\';color:#C9432F;margin-top:8px">{{ t.note }}</div>'
     '<div style="font:600 15px/1.3 \'Barlow Condensed\';color:#536676;margin-top:4px">{{ t.annual }}</div>'),
    ('OF 8<br>SPOTS LEFT', 'SEATS<br>IN TOTAL'),
    # Elite: private coaching, not just a chat (Ryan, Oct 28)
    ('Direct access to Claude Harmon III and Ryan Crysler, Head Coach of TeamFLO and RC Greenlight. Applications are reviewed by the coaching team.',
     'Private coaching with Claude Harmon III and Ryan Crysler. The Elite Basecamp for exclusive conferences with the 8 members. RC Greenlight Data Services on your rounds. Plus the Son of a Butch Podcast and your home academy basecamp. Applications are reviewed by the coaching team.'),
    # SEO: the H1 says what this is, in words people search for
    ('<span style="color:#E04E39">Every week.</span></h1>',
     '<span style="color:#E04E39">Every week.</span><span class="ch3-h1-sub" style="display:block;margin-top:22px;font:600 20px/1.3 \'Barlow Condensed\';'
     'letter-spacing:.1em;color:#A6B1BA">Online golf coaching from Claude Harmon III and the CH3 academies in Dubai, Thailand and Florida</span></h1>'),
]
if BETA:
    EDITS += [
        ('2 weeks free, then from $49/month. Renews automatically. Cancel any time before day 14 and pay nothing.',
         'Now in beta with the CH3 academies: membership is by invitation. At launch, 2 weeks free, then from $49/month.'),
        ('Every membership except Elite starts with 2 weeks free. Cancel before day 14 and pay nothing.',
         'TeamCH3 is in beta with the CH3 academies, so membership is by invitation for now. At launch, every membership except Elite starts with 2 weeks free.'),
        ('Then $49/month. Cancel any time.', 'In beta, by invitation. From $49/month at launch.'),
        ('Your 2 weeks start now.', 'Your basecamp is waiting.'),
        ('ALL TIERS · 2 WEEKS FREE', 'ALL TIERS · NOW IN BETA'),
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
                'ON TOUR WITH CLAUDE · BEHIND THE ROPES', 'CH3 DUBAI · CH3 THAILAND · TEAMFLO', 'NOW IN BETA · REQUEST AN INVITE' if BETA else 'START 2 WEEKS FREE']
def ticker():
    items = ''.join('<span style="display:inline-flex;align-items:center;gap:28px;padding-right:28px;font:600 17px/1 \'Barlow Condensed\';letter-spacing:.14em;white-space:nowrap">%s<span style="width:8px;height:8px;background:#253746;display:inline-block;transform:rotate(45deg)"></span></span>' % H.escape(s) for s in TICKER_ITEMS * 2)
    return raw('<div class="ch3-marquee" style="display:flex;width:max-content">%s</div>' % items)

ELITE_LEFT = 8  # no Elite members yet
FEATS = ['Son of a Butch community', 'Live podcast recordings', 'Global feed + Claude’s tour updates', 'Live webinars + Premier Sessions', 'Academy home basecamp',
         'Basecamp Spotlights', 'Global Junior Basecamp', 'Private coaching with Claude + Ryan',
         'Elite Basecamp: conferences with the 8 members', 'RC Greenlight Data Services']
def tier(pos, flag, name, pitch, price, note, cta, yes, primary, key):
    return {'pos': pos, 'flag': flag, 'name': name, 'pitch': pitch, 'price': price, 'note': note, 'cta': cta,
            'primary': primary, 'secondary': not primary, 'key': key,
            'feats': [{'t': f, 'yes': bool(y), 'no': not y} for f, y in zip(FEATS, yes)]}

_ev = next_event() or NO_EVENT
_rec = next_event(rec=True)
REC_DEFAULT = 'SOON' if not _rec else '--:--:--'
ctx = {
    'evKind': span('ev-kind', _ev[2]), 'evShort': span('ev-short', _ev[3]), 'evTitle': span('ev-title', _ev[4]),
    'evBlurb': span('ev-blurb', _ev[5]), 'recShort': span('rec-short', REC_DEFAULT),
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
        # first the golf (Junior, Premier, Elite): the coaches' minds, lessons from every academy, a day inside each academy
        {'n': '01', 'tier': 'JUNIOR · PREMIER · ELITE', 'title': 'Live webinars', 'hook': "Inside the coaches' minds.", 'body': 'Webinars with the CH3 coaches for Premier members at every academy and the Junior Basecamp: how they think, plan and fix a game.', 'cta': 'SEE THE SCHEDULE'},
        {'n': '02', 'tier': 'JUNIOR · PREMIER · ELITE', 'title': 'Premier Sessions', 'hook': 'Lessons from every academy.', 'body': 'Watch the CH3 coaches teach at CH3 Dubai, CH3 Thailand and TeamFLO, live and on demand. The first sessions are on the way.', 'cta': 'OPENING SOON'},
        # the coaches' own space (the Coaches' Basecamp) stays coaches-only; members get a look inside each academy instead
        {'n': '03', 'tier': 'JUNIOR · PREMIER · ELITE', 'title': 'Basecamp Spotlights', 'hook': 'A day inside each academy.', 'body': "The daily practice schedule, the coaching insights and what it's like to train at CH3 Dubai, CH3 Thailand and TeamFLO.", 'cta': 'SEE THE NEXT ONE'},
        # then the cherry on top, for every membership: Claude live with the podcast, and his updates from tour (posted in the Global Basecamp)
        {'n': '04', 'tier': 'ALL TIERS', 'title': 'Live with Claude', 'hook': 'On air with CH3.', 'body': 'Watch Son of a Butch record live with Claude and special guests, and get your questions answered on air.', 'cta': raw('NEXT ONE · ' + span('rec-short', REC_DEFAULT))},
        {'n': '05', 'tier': 'ALL TIERS', 'title': 'On tour with Claude', 'hook': 'Updates from tour events.', 'body': "What Claude is seeing range-side at tour events, and what it means for your game.", 'cta': 'GO INSIDE THE ROPES'},
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
        tier('SB', '2 WEEKS FREE', 'Pod Community', 'For Son of a Butch listeners who want the room behind the mic.', '$49',
             'Free for 2 weeks, then $49/month.', 'START FREE', [1, 1, 1, 0, 0, 0, 0, 0, 0, 0], False, 'pod'),
        tier('JB', 'JUNIORS', 'Junior Basecamp', 'Everything in Premier, plus the Global Junior Basecamp: juniors from every CH3 academy in one place.', '$69',
             'Ages 13–19. Premier access at a junior price.', 'JOIN THE JUNIOR BASECAMP', [1, 1, 1, 1, 1, 1, 1, 0, 0, 0], False, 'junior'),
        tier('PS', 'MOST POPULAR', 'Premier', 'The full basecamp. Your home basecamp, or the one closest to you, plus everything global.', '$99',
             'Includes your academy’s home basecamp.', 'GO PREMIER', [1, 1, 1, 1, 1, 1, 0, 0, 0, 0], True, 'premier'),
        tier('EB', 'LIMITED · BY APPLICATION', 'Elite', 'Private coaching with Claude Harmon III and Ryan Crysler, plus RC Greenlight Data Services. Eight members, by application.', '$999',
             'Limited to 8 members.', 'APPLY FOR ELITE', [1, 1, 1, 1, 1, 1, 0, 1, 1, 1], False, 'elite'),
    ],
}

# three cards side by side (Pod, Premier, Elite); the Junior Basecamp gets its own bar under them
JUNIOR_TIER = [tr for tr in ctx['tiers'] if tr['key'] == 'junior'][0]
ctx['tiers'] = [tr for tr in ctx['tiers'] if tr['key'] != 'junior']
ANNUAL = {'pod': 'or $490/year · 2 months free', 'premier': 'or $990/year · 2 months free', 'elite': 'or $9,990/year · 2 months free'}
for tr in ctx['tiers']:
    tr['annual'] = ANNUAL[tr['key']]

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
    '<span style="font:400 40px/1 Anton,sans-serif;text-transform:uppercase">%s</span>'
    '<span class="ch3-reg-on" style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.12em">YOUR HOME BASECAMP ✓</span>'
    '<span class="ch3-reg-off" style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.12em">SELECT</span>'
    '</label>' % (k, k, H.escape(w), H.escape(a)) for k, w, a in REG)
new = frag(
    '<div class="ch3-region-box" style="grid-column:1/-1;border-radius:8px;overflow:hidden;background:#253746;color:#fff;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:0">'
    '<div class="ch3-region-intro" style="padding:30px 28px;border-right:1px solid #384B5B">'
    '<div style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.14em;color:#F47C67">WHERE DO YOU LIVE?</div>'
    '<div style="font:400 44px/1 Anton,sans-serif;text-transform:uppercase;margin-top:12px">There’s a basecamp near you.</div>'
    '<div style="font:400 19px/1.35 \'Barlow Condensed\';color:#CDD4DA;margin-top:14px">Junior, Premier and Elite members join the home basecamp closest to where they live.</div>'
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
assert len(cards) == len(ctx['tiers'])
for card, tr in zip(cards, ctx['tiers']):
    a = card.find_all('a')[-1]
    a['href'] = '#tiers'; a['data-checkout'] = tr['key']
elite = [a for a in page.find_all('a') if a.get_text(strip=True) == 'APPLY FOR ELITE' and a.get('href') == '#']
for a in elite: a['href'] = '#tiers'; a['data-checkout'] = 'elite'

# ---- sales pass (Oct 28): one way to join, the coaches up front, how it works, FAQ, and a clearer order ----
def node(html_str):
    return frag(html_str)[0]
BTN = ("font:700 19px/1 'Barlow Condensed';letter-spacing:.08em;color:#fff;background:#E04E39;padding:20px 30px;border-radius:2px;"
       "display:inline-block")
def cta_html(key=None, label=None, extra=''):
    return '<a class="ch3-join ch3-cta" href="%s" style="%s%s">%s</a>' % (H.escape(join_url(key)), BTN, extra, H.escape(label or CTA))

# every "join" button: one wording, and in beta a pre-filled invite email (Elite: an application)
JOIN_TEXT = {'START 2 WEEKS FREE': None, 'SAVE MY SEAT — FREE': None, 'GET IN THE FEED — 2 WEEKS FREE': None,
             'UNLOCK THE FULL SESSION — PREMIER': 'premier', 'JOIN THE POD COMMUNITY — 2 WEEKS FREE': 'pod',
             'START FREE': 'pod', 'GO PREMIER': 'premier'}
joined = 0
for a in page.find_all('a'):
    label = a.get_text(strip=True)
    if label in JOIN_TEXT:
        a.string = CTA
        a['href'] = join_url(JOIN_TEXT[label]); add_class(a, 'ch3-join'); joined += 1
    elif label == 'APPLY FOR ELITE':
        a['href'] = join_url('elite'); add_class(a, 'ch3-join'); joined += 1
assert joined >= 11, joined
# the Junior Basecamp banner in the academies section is one big link
jb = [a for a in page.find_all('a') if 'JOIN THE JUNIOR BASECAMP' in a.get_text(' ', strip=True)]
assert len(jb) == 1
jb[0]['href'] = join_url('junior')

# sections by name
site_sections = {s.get('id'): s for s in page.find_all('section') if s.get('id')}
hero = [s for s in page.find_all('section') if s.find('h1')][0]; hero['id'] = 'top'
final = [s for s in page.find_all('section') if 'Lights out.' in s.get_text()][0]; final['id'] = 'join'
footer = page.find('footer')

# the coaches, up front
COACHES = [('CH3', 'Claude Harmon III', 'HEAD COACH · TEAMCH3'), ('DU', 'Mike Bolt', 'HEAD COACH · CH3 DUBAI'),
           ('TH', 'Joe Marshall', 'HEAD COACH · CH3 THAILAND'), ('FL', 'Ryan Crysler', 'HEAD COACH · TEAMFLO + RC GREENLIGHT')]
coaches = node(
    '<section id="coaches" style="background:#253746;color:#fff;padding:40px 40px 44px">'
    '<div style="max-width:1280px;margin:0 auto">'
    '<div style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.18em;color:#F47C67">YOUR COACHES · THREE ACADEMIES · ONE TEAM</div>'
    '<div class="ch3-coach-grid" style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:3px;margin-top:18px">%s</div>'
    '</div></section>' % ''.join(
        '<div style="display:flex;gap:14px;align-items:center;background:#1E2D3A;padding:18px 20px">'
        '<span style="flex:none;width:50px;height:50px;border-radius:25px;border:2px solid #E04E39;display:flex;align-items:center;justify-content:center;'
        'font:400 17px/1 Anton,sans-serif;color:#F47C67">%s</span>'
        '<div><div style="font:400 24px/1 Anton,sans-serif;text-transform:uppercase">%s</div>'
        '<div style="font:600 13px/1.25 \'Barlow Condensed\';letter-spacing:.1em;color:#A6B1BA;margin-top:6px">%s</div></div></div>'
        % (code, H.escape(name), H.escape(role)) for code, name, role in COACHES))

# how it works, in three steps
STEPS = [('01', 'Pick your academy', 'Your home basecamp is the CH3 academy closest to where you live: TeamFLO for the Americas, '
          'CH3 Dubai for Europe, the Middle East and Africa, CH3 Thailand for Asia and the Pacific.'),
         ('02', 'Request your invite', 'TeamCH3 is in beta with the CH3 academies. Tell us your name, home city and membership, '
          'and we’ll send your invite.') if BETA else
         ('02', 'Start 2 weeks free', 'Full access for 14 days. Cancel before day 14 and you pay nothing.'),
         ('03', 'Train with the coaches', 'Bring your questions, round reports and playing stats to the coaches, join the webinars '
          'and Basecamp Spotlights, and go live with Claude.')]
how = node(
    '<section id="how" style="background:#F2F4F6;color:#253746;padding:90px 40px">'
    '<div style="max-width:1280px;margin:0 auto">'
    '<div style="font:600 15px/1 \'Barlow Condensed\';letter-spacing:.18em;color:#C9432F">HOW IT WORKS</div>'
    '<h2 style="margin:14px 0 0;font:400 clamp(44px,5.4vw,76px)/.92 Anton,sans-serif;text-transform:uppercase">Three steps to your basecamp.</h2>'
    '<div class="ch3-how-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:3px;margin-top:40px">%s</div>'
    '<div style="display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:32px">%s'
    '<span style="font:400 17px/1.3 \'Barlow Condensed\';color:#536676">%s</span></div>'
    '</div></section>' % (
        ''.join('<div style="background:#fff;padding:28px 24px 32px;border-top:4px solid #E04E39">'
                '<div style="font:400 56px/1 Anton,sans-serif;color:#E04E39">%s</div>'
                '<div style="font:400 32px/1 Anton,sans-serif;text-transform:uppercase;margin-top:14px">%s</div>'
                '<div style="font:400 18px/1.4 \'Barlow Condensed\';color:#536676;margin-top:12px">%s</div></div>'
                % (n, H.escape(t), H.escape(d)) for n, t, d in STEPS),
        cta_html(),
        'No email app? Write to %s.' % INVITE_EMAIL if BETA else '2 weeks free, then from $49/month. Cancel any time before day 14.'))

# Junior Basecamp: its own bar under the three membership cards
grid = find_style('div', 'grid-template-columns:repeat(auto-fit,minmax(270px,1fr))')
grid.insert_after(node(
    '<div class="ch3-junior-bar" style="margin-top:3px;background:#C9432F;color:#fff;display:grid;grid-template-columns:minmax(0,1fr) auto;'
    'gap:24px;align-items:center;padding:26px 28px">'
    '<div><div style="font:600 13px/1 \'Barlow Condensed\';letter-spacing:.14em;color:#FFD9D1">JUNIORS 13–19 · PARENTS JOIN FREE</div>'
    '<div style="font:400 34px/1 Anton,sans-serif;text-transform:uppercase;margin-top:10px">Junior Basecamp · $69/month</div>'
    '<div style="font:400 18px/1.35 \'Barlow Condensed\';margin-top:8px;max-width:720px">Everything in Premier, plus the juniors-only '
    'Junior Basecamp with the CH3 coaches from every academy. Or $690/year, 2 months free.</div></div>'
    '%s</div>' % cta_html('junior', extra=';background:#253746;white-space:nowrap')))

# FAQ (the same questions go into the page's structured data for search)
FAQ = [
    ('Do I need to live near a CH3 academy?',
     'No. TeamCH3 is online. You join the home basecamp closest to where you live (TeamFLO for the Americas, CH3 Dubai for Europe, '
     'the Middle East and Africa, CH3 Thailand for Asia and the Pacific) and train with its coaches from wherever you are.'),
    ('How do I join during the beta?',
     'TeamCH3 is in beta with the CH3 academies, so membership is by invitation for now. Request an invite, or email %s with your name, '
     'home city and the membership you want, and we’ll send it.' % INVITE_EMAIL) if BETA else
    ('How does the free trial work?',
     'Every membership except Elite starts with 2 weeks free. Cancel before day 14 and you pay nothing. After that it renews monthly, or yearly if you chose annual.'),
    ('What does it cost?',
     'Pod Community is $49 a month, Junior Basecamp $69, Premier $99 and Elite $999. Pay for the year and you get 12 months for the price of 10. '
     'Every membership except Elite starts with 2 weeks free.'),
    ('What’s the difference between Premier and Elite?',
     'Premier is the full basecamp: your home academy, the live webinars, Basecamp Spotlights, Premier Sessions and everything global. '
     'Elite adds private coaching with Claude Harmon III and Ryan Crysler, the Elite Basecamp for exclusive conferences with the 8 members, '
     'and RC Greenlight Data Services. It’s by application, with no free trial.'),
    ('What do juniors get, and how are they kept safe?',
     'Juniors aged 13 to 19 get everything in Premier plus the Junior Basecamp, a juniors-only feed with the CH3 coaches from every academy. '
     'Adult members can’t see or join the junior spaces, members can’t send private messages, and a parent or guardian joins the Parents space free.'),
    ('What do I need to bring?',
     'Your questions, plus any round reports or playing stats you have. We coach how you play the game, so start with your last round. '
     'Not tracking your rounds yet? The coaches will help you get set up. You don’t need a launch monitor.'),
    ('Where do I watch the live sessions?',
     'Inside TeamCH3, in your web browser. RSVP to a session and you’ll get a reminder before it starts.'),
    ('Can I cancel any time?',
     'Yes. Cancel whenever you like, and if you cancel during your 2 free weeks you pay nothing.'),
]
faq = node(
    '<section id="faq" style="background:#fff;color:#253746;padding:110px 40px">'
    '<div class="ch3-faq-grid" style="max-width:1280px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:56px">'
    '<div><div style="font:600 15px/1 \'Barlow Condensed\';letter-spacing:.18em;color:#C9432F">FAQ</div>'
    '<h2 style="margin:14px 0 0;font:400 clamp(44px,5.4vw,76px)/.92 Anton,sans-serif;text-transform:uppercase">Questions before you join.</h2>'
    '<p style="margin:18px 0 28px;font:400 20px/1.35 \'Barlow Condensed\';color:#536676">Still not sure? Email %s and a TeamCH3 admin will help.</p>%s</div>'
    '<div>%s</div></div></section>' % (
        INVITE_EMAIL, cta_html(),
        ''.join('<details class="ch3-faq"><summary>%s</summary><p>%s</p></details>' % (H.escape(q), H.escape(a)) for q, a in FAQ)))

# the order: golf first, then Claude, then the decision
order = [hero, coaches, how, site_sections['grid'], site_sections['session'], site_sections['basecamp'],
         site_sections['feed-preview'], site_sections['pod'], site_sections['tiers'], faq, final, footer]
for el in order:
    if el.parent is not None: el.extract()
for el in order:
    page.append(el)

# nav follows the page, and gets an FAQ link; footer too
nav = find_style('nav', 'display:flex;gap:26px')
links = {a['href']: a for a in nav.find_all('a')}
nav.clear()
for href in ('#grid', '#session', '#basecamp', '#pod', '#tiers'):
    nav.append(links[href])
faq_link = node(str(links['#tiers']).replace('#tiers', '#faq').replace('MEMBERSHIP', 'FAQ'))
nav.append(faq_link)
mem_col = [d for d in footer.find_all('div') if d.find('span', string='MEMBERSHIP')][0]
log_in = [a for a in mem_col.find_all('a') if a.get_text(strip=True) == 'Log in'][0]
premier = [a for a in mem_col.find_all('a') if a.get_text(strip=True) == 'Premier'][0]
premier.insert_after(node('<a href="#tiers" style="color:#A6B1BA">Junior Basecamp</a>'))
log_in.insert_before(node('<a href="#faq" style="color:#A6B1BA">FAQ</a>'))
log_in.insert_before(node('<a href="%s" style="color:#A6B1BA">%s</a>' % (H.escape(join_url()), 'Request an invite' if BETA else 'Start 2 weeks free')))

# structured data for search: who we are, and the FAQ
LD = json.dumps({'@context': 'https://schema.org', '@graph': [
    {'@type': 'Organization', 'name': 'TeamCH3', 'url': 'https://ch3.circle.so/', 'logo': CDN + 'rrxvgyqulo15uln4o8y0t7bqi3f5',
     'description': 'Online golf coaching from Claude Harmon III and the CH3 academies in Dubai, Thailand and Florida.'},
    {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
]}, ensure_ascii=False)

SALES_CSS = r'''
#ch3-site .ch3-faq{border-top:1px solid #CDD4DA}
#ch3-site .ch3-faq:last-child{border-bottom:1px solid #CDD4DA}
#ch3-site .ch3-faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 0;font:400 26px/1.05 Anton,sans-serif;text-transform:uppercase;color:#253746}
#ch3-site .ch3-faq summary::-webkit-details-marker{display:none}
#ch3-site .ch3-faq summary::after{content:"+";flex:none;font:400 30px/1 Anton,sans-serif;color:#E04E39}
#ch3-site .ch3-faq[open] summary::after{content:"–"}
#ch3-site .ch3-faq summary:focus-visible{outline:2px solid #E04E39;outline-offset:4px}
#ch3-site .ch3-faq p{margin:0 0 22px;font:400 19px/1.45 'Barlow Condensed';color:#536676;max-width:720px}
#ch3-site a.ch3-cta:hover{background:#C9432F!important;color:#fff!important}
#ch3-site .ch3-junior-bar a.ch3-cta:hover{background:#111A22!important}
@media (max-width:1100px){
#ch3-site .ch3-coach-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
}
@media (max-width:860px){
#ch3-site #coaches{padding:32px 16px!important}
#ch3-site #how{padding:72px 16px!important}
#ch3-site #faq{padding:72px 16px!important}
#ch3-site .ch3-how-grid,#ch3-site .ch3-faq-grid{grid-template-columns:minmax(0,1fr)!important;gap:28px!important}
#ch3-site .ch3-how-grid{gap:3px!important}
#ch3-site .ch3-junior-bar{grid-template-columns:minmax(0,1fr)!important}
#ch3-site .ch3-h1-sub{font-size:17px!important}
}
@media (max-width:520px){
#ch3-site .ch3-coach-grid{grid-template-columns:minmax(0,1fr)!important}
#ch3-site .ch3-faq summary{font-size:22px}
}
'''

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
#ch3-site .ch3-reg{display:flex;flex-direction:column;gap:10px;padding:30px 28px;cursor:pointer;color:#fff;background:transparent;border-left:1px solid #384B5B;transition:background-color .18s}
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
#ch3-site .ch3-nav a.ch3-join{padding:12px 12px!important;font-size:14px!important}
#ch3-site .ch3-count>div>div:first-child{font-size:30px!important}
}
@media (prefers-reduced-motion:reduce){#ch3-site *{animation:none!important;transition:none!important}#ch3-site .ch3-label-b{display:none}}
''' + '\n'.join(hover_rules)

JS = r'''
(function(){
var root=document.getElementById('ch3-site');if(!root)return;
function q(s){return root.querySelectorAll(s)}
function p(n){return (n<10?'0':'')+n}
var EV=EVENTS_JSON;
function nextEv(now,rec){for(var i=0;i<EV.length;i++){var e=EV[i],a=Date.parse(e[0]),b=a+e[1]*60000;if(b>now&&(e[6]||!rec))return{e:e,s:Math.max(0,Math.floor((a-now)/1000)),live:a<=now}}return null}
function parts(s){var d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60),x=s%60;return{d:p(d),h:p(h),m:p(m),s:p(x),short:(d?d+'D ':'')+p(h)+':'+p(m)+':'+p(x)}}
function tick(){var now=new Date();
 q('[data-ch3="tz"]').forEach(function(e){var z=e.getAttribute('data-tz');try{e.textContent=now.toLocaleTimeString('en-GB',z==='local'?{hour:'2-digit',minute:'2-digit'}:{timeZone:z,hour:'2-digit',minute:'2-digit'})}catch(err){}});
 var n=nextEv(now.getTime(),false),r=nextEv(now.getTime(),true),v,t;
 if(n){t=parts(n.s);v={'cd-d':t.d,'cd-h':t.h,'cd-m':t.m,'cd-s':t.s,'cd-short':n.live?'LIVE NOW':t.short,'ev-kind':n.e[2],'ev-short':n.e[3],'ev-title':n.e[4],'ev-blurb':n.e[5]}}
 else v={'cd-d':'--','cd-h':'--','cd-m':'--','cd-s':'--','cd-short':'SOON','ev-kind':'COMING UP','ev-short':'NEW DATES SOON','ev-title':'Next live session','ev-blurb':'New dates are announced in the community.'};
 v['rec-short']=r?(r.live?'LIVE NOW':parts(r.s).short):'SOON';
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
'''.replace('EVENTS_JSON', json.dumps([list(e) for e in EVENTS])).replace('SHOTS_JSON', json.dumps([list(s) for s in SHOTS])).replace('CUR_JSON', str(CUR))

head = ('<!-- TeamCH3 membership page · for Circle\'s website builder · built Oct 15 2026 from "TeamCH3_Membership_Site_1.html".\n'
        'Paste everything into one custom HTML / code block. Images are hosted on Circle (assets-v2.circle.so).\n'
        'Buttons marked data-checkout="pod|junior|premier|elite" still point to #tiers: swap in the checkout links once the paywalls exist. -->\n')
fonts = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@400;600;700&display=swap">\n'
html_out = (head + fonts + '<style>' + re.sub(r'\n+', '\n', CSS + SALES_CSS).strip() + '</style>\n' + str(page)
            + '\n<script type="application/ld+json">' + LD + '</script>\n<script>' + JS.strip() + '</script>\n')
assert '{{' not in html_out, 'unrendered expression left'
assert 'sc-' not in re.sub(r'data-[\w-]+', '', html_out).replace('desc-', ''), 'directive left'
open(OUT, 'w', encoding='utf-8').write(html_out)
print('wrote', OUT, len(html_out), 'bytes;', len(hover_rules), 'hover rules')
