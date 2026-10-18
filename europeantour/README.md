# DP World Tour shot-by-shot scraper

Pulling shot-level data for a player (e.g. Laurie Canter, player id `45`) from
pages like:

```
https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1
```

## Setting up on a PC (no command line)

1. Install **Python** once from <https://www.python.org/downloads/>. On the
   installer's first screen, tick **"Add python.exe to PATH"**.
2. In **GitHub Desktop**, clone `ryancrysler-rgb/RCProjects`. It opens on the right
   branch by default, with all the code and every round captured so far.
3. **Repository -> Show in Explorer**, then open the `europeantour` folder.
4. Double-click **GET SHOT BY SHOT (Windows).bat**. The first time on a new PC it
   sets itself up (a few minutes: a Python environment, its components, and the
   browser it drives); after that it starts straight away.

Each capture asks for the leaderboard URL, the round and the player's surname, opens
the browser, and when you close it builds `SHOT_BY_SHOT_<event>.csv` and checks every
round against the site's own scorecard. **Pull before you start, commit and push
when you finish** -- on whichever PC you are using.

---

## Where the shot-by-shot data actually is (solved)

Not in the DP World Tour's API. Their `/api/sportdata/` endpoints serve hole
scores only. The AI Shot Commentary panel is IMG Arena's Event Centre, and it
streams over a **websocket**:

```
wss://btec-websocket.services.srarena.io/
```

Frames are **Snappy-compressed UTF-16LE JSON** -- not gzip or deflate, which is
why ordinary decoding turns up nothing. `snappy_lite.py` decompresses them in
pure Python, so nothing has to be built or installed.

Two subscriptions carry the round, one hole per frame:

| Subscription | Gives |
|---|---|
| `MapVisualisationSubscribeToMedia3DShots` | `holeNo`, `strokeNo`, `x`/`z`, `surfaceTypeCode`, `distanceToPin`, `shotDistance`, `ballHoled` |
| `ShotFeedSubscribeToGolfTournamentTeamsShotFeed` | `shotNo`, `timestamp`, `eventType`, `holeScore`, `prevSurfaceTypeCode` |

`teamId` is the id the site shows for a player -- Laurie Canter is **45**, which
is a team id, not the `playerId` (840) or the tour's own id (37624). Three
different numbering systems for one golfer.

The event feed carries no hole number, so events are placed on holes by
matching one shot's distances to a position record from the same frame.

**Verified**: 74 shots over 18 holes for Canter, round 1. Holes 1-9 match the
official scorecard stroke for stroke, and hole 1 reproduces the on-screen
commentary exactly -- a 13-footer missed for par leaving eight inches, tapped
in for bogey.

## Getting a round

1. `GET SHOT BY SHOT (Windows).bat` -- a browser opens; click the player, open
   AI SHOT COMMENTARY, step through all 18 holes, then close the window.
2. `BUILD SPREADSHEET (Windows).bat` -- writes `SHOT_BY_SHOT.csv`.

Runs accumulate, so a partial round can be finished later. `decode_ws.py`
re-decodes saved frames without touching the browser.

---

## What the tour site actually serves (confirmed live, Sept 2026)

Captured from the Amgen Irish Open 2026 leaderboard. These are observed, not guessed:

| What | URL |
|---|---|
| Leaderboard | `www.europeantour.com/api/sportdata/Leaderboard/Strokeplay/{event}/type/load` |
| Live polling | `.../Leaderboard/Strokeplay/{event}/type/polling` |
| Scorecard | `www.europeantour.com/api/sportdata/Scorecard/Strokeplay/Event/{event}/Player/{player}` |
| Event status | `www.europeantour.com/api/sportdata/Event/Status/{event}` |

- Irish Open 2026 event id: **2026135**
- Player ids in this API are **not** the ids shown on the site. Laurie Canter is
  `37624` there, not `45`. `fetch_event.py` resolves a surname to the right id.
- Their own API appears to carry **hole-by-hole scores**, not shot-by-shot.
- The **3D shot tracer is a third party**: IMG Arena / SR Arena, on
  `btec-http.services.srarena.io/?hash=...` with course geometry at
  `static.srarena.io/golf/3d/courses/{course}/all_metadata.json`. Shot coordinates
  live there, behind hash-addressed URLs, not in the tour's public API.
- Beware `l10n.frs-prod.imgarena.dev/locales/*/ec-golf.json`. It scores high for
  shot vocabulary because it is the **translation file** listing every UI label
  the app can display. It contains no data. The capture step now filters it out.

---

## The idea

**Don't parse the HTML.** That page is a client-side app — the served HTML
contains no scores at all. Every number you see arrives afterwards as JSON over
XHR, from their feed API (`fdapi.europeantour.com` / `www.europeantour.com/api/sportdata`).

So the reliable route is two steps:

1. **Observe** the API once with a real browser, recording every JSON response
   and ranking them by how much shot-level vocabulary they contain.
2. **Fetch** the winning endpoint directly with plain HTTP for every round and
   player you want. No browser needed after step 1.

Their feed is undocumented and field names drift between seasons, so nothing
here hard-codes a schema — `shotjson.py` finds shot-shaped arrays by vocabulary
and flattens whatever it finds.

## Usage

```bash
pip install -r requirements.txt
playwright install chromium

# 1. discover the endpoints (clicking the player row triggers the shot XHRs)
python capture_api.py \
  --url "https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1" \
  --click-text Canter --har --out captured

# 2. read the ranked list it prints, then pull the shots
python fetch_shots.py --url "<top endpoint from captured/manifest.json>" \
  --player 45 --csv canter_r1.csv

# or parse a body already saved in step 1
python fetch_shots.py --file captured/bodies/000_041_xxx.json --player 45 --csv canter_r1.csv
```

Add `--headed` to `capture_api.py` if nothing is captured — usually a cookie
consent wall or a geo block.

## Output

One row per shot, carrying inherited player/round/hole context:

| RoundNumber | PlayerId | LastName | HoleNumber | Par | ShotNumber | Club | Carry | DistanceToPin | Lie |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 45 | Canter | 1 | 4 | 1 | Driver | 298 | 142 | Fairway |
| 1 | 45 | Canter | 1 | 4 | 2 | 9 Iron | 141 | 11 | Green |

## Files

| File | Purpose |
|---|---|
| `shotjson.py` | Schema-agnostic scoring, shot-array detection, flattening |
| `capture_api.py` | Playwright capture → `manifest.json` ranked by shot-likelihood |
| `fetch_shots.py` | Direct endpoint (or local file) → tidy CSV |

## Caveats

- The candidate URLs in `fetch_shots.py --probe` are **unverified guesses**.
  `europeantour.com` is blocked by the egress policy of the environment this
  was written in, so no endpoint here has been confirmed against the live
  site. Step 1 observes the truth; the guesses are only a fallback grid.
- The parsing pipeline *is* tested, against a synthetic payload matching the
  nested `Rounds → Players → Holes → Shots` shape.
- Shot-level data usually only exists for featured groups/holes, and often
  only during and shortly after play. If a round returns scorecards but no
  shots, that data may simply not be published for that group.
- Check their terms of use before running this at volume, and keep request
  rates sane.
