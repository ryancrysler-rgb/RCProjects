# DP World Tour shot-by-shot scraper

Pulling shot-level data for a player (e.g. Laurie Canter, player id `45`) from
pages like:

```
https://www.europeantour.com/dpworld-tour/amgen-irish-open-2026/leaderboard?round=1
```

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
