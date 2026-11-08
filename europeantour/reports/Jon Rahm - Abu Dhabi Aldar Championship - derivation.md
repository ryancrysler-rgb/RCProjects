# Jon Rahm · Abu Dhabi Aldar Championship (final) · Tournament Summary · Raw — derivation and disclosures

Deliverable: `Jon Rahm - Abu Dhabi Aldar Championship - Tournament Summary - Raw.html` (supersedes the R1–R3 sheet).
Gold standard copied: `deliverables/Laurie Canter - LIV Indy Tournament Summary - Raw.html` — the four-round set, so the
hole table is the gold's own grid (four round columns). Build record: `build-final/`.

## Source and reconciliation

- DP World Tour Event Centre shot feed (tracker event 1440), Jon Rahm (player 493, team 45), all four rounds captured hole
  by hole; spreadsheet `SHOT_BY_SHOT_abu-dhabi-aldar-championship-2026.csv`.
- Reconciled to the official cards: **65 / 67 / 66 / 67 = 265 (−23)**, 18 of 18 holes agree in each of the four rounds.
- Par per hole from the course-stats panel (`getGolfHoleStats.holePar`), checked hole by hole by the house reader.
- Finish from the official final leaderboard (updated 2026-11-08 13:00 UTC): **1st, −23, won by 2 (next best −21);
  70 players, all finished.** No other player is named on the sheet.
- Field per hole: the panel's `averageHoleScore` for each round; FLD = par + the mean of the four. FLD cells (2dp) sum to
  the printed 70.26. Per-round field averages: 70.39 · 69.86 · 69.71 · 71.11 — he beat them by 5.39 · 2.86 · 3.71 · 4.11.

## The engine — house rules v18.1

Graded with the RC Greenlight engine at **Rev 362 (house rules v18.1, 2026-11-09)**, the latest rulebook, from the RC
Greenlight session's branch `claude/exciting-bardeen-faa85u` (commit cf44dee; not yet merged, ships Monday 9 Nov). The R1–R3
sheet was graded at Rev 361; every figure here was re-run on Rev 362.

**R2 H12** (stroke-and-distance: the feed returns the ball to the tee, `OTB`) is read with one change in a scratch copy of
the reader: a penalty row may end on the tee. Nothing else changed; R1, R3 and R4 read through the standard reader. H12 is
off the approach ladder by the ladder rule (71 of 72 approaches banded; ladder greens reconcile to GIR 62).

## Definitions the sheet prints

- **Off the Tee** — 43/56 fairways (77%; by round 71 · 71 · 79 · 86%). No club field: the gold's driver / fairway-wood split
  cannot be built (`Club split · not in feed`), Rule 01 NOT MEASURED. Good drive 51/56 (`metrics.goodDrive`). Tee avg 300 yd
  over all 56 par-4/5 tee balls. Longest 348 yd · R4 H2 (the week maximum over the same 56).
- **Approach · GIR** — 62/72. Ladder: under 40 8/8 · 40–74 5/5 · 75–100 4/4 · 101–120 0/1 · 121–140 8/9 · 141–160 11/14 ·
  161–180 7/8 · 181–200 10/12 · 201–220 4/5 · 220+ 5/5. Inside 160 = 36 of 41 (band-chart sum).
- **Around the Green** — scrambling 6/10 (missed greens R1 H10, H16 · R2 H4, H6, H12, H13 · R3 H4, H6 · R4 H3, H17; bogeys
  from R2 H6, R2 H12, R3 H4, R4 H3). Par 5s under par 11/16 (the R3 H11 eagle among them). Par 5s −12. Three-putts 1 (R2 H9).
  Best round 65 (−7) · R1. **Clutch Factor Ball Striking 1 of 4 · 3 semi** (R1 H2 clutch; R2 H6, R2 H12, R4 H3 semi).
- **Putting · by round** — 116 putts; rows = putts · holed inside 6 ft (28 · 15/17, 28 · 14/15, 30 · 14/15, 30 · 16/16;
  week 59/63). **Clutch Factor Putting 2 of 5.** Birdie conversion 27/62 (44%).
- **Rule 05 level per round:** LOW · MEDIUM (floored by three bogeys) · LOW · LOW — the engine's level, four measures each.
- Other non-negotiables for the record: Rule 01/02 NOT MEASURED every round; Rule 03 KEPT R1, ATTENTION R2 (H14 67 yd),
  R3 (H10 55, H18 54), R4 (H10 65, H18 48); Rule 04 ATTENTION R2 (H12), KEPT otherwise.

## The dead-zone exception (owner's form answer 2026-11-08: "Note the exception")

Opportunities keeps "Leave 75–100, not 40–74" and adds the written exception: his own 40–74 band went **5 of 5** (R2 H14,
R3 H10, R3 H18, R4 H10, R4 H18), which meets non-negotiable 3's written exception (`house-rules.js` NN3: a 40–74 leave is
allowed when the player's own band covering it reads ≥90%). The next band (75–100) is also 4 of 4, so it qualifies on the
≥90% test, not on "higher than the next band". Applying it is the coach's call, as the policy says; the sheet says so.

## Deviations from the gold

1. **He is the champion**, so "vs the champion" becomes **Champion · won by 2**, carrying the margin over the field's
   scoring average each round and the four Rule 05 levels (one per round, never a week average). The third header tile is
   **Won by** (the mirror of the gold's Back).
2. Both Clutch Factors printed (all four rounds through one engine); Best round moved to an ARG row.
3. Off the Tee cannot carry the club split.

## Checks

- Generator asserts every SWOT figure against the engine output (fairways, greens, putts, scrambling, inside 6 ft incl. R4
  16/16, birdie conversion, par-5 counts incl. Sunday 5-5-4-5, the ladder bands named, H14/H16 4-4-4-4 against a field under
  par, the levels, every bogey, no doubles, GIR and to-par by round, fairways by round).
- "Three of the five bogeys began with a missed fairway": 13 par-4/5 tee balls missed; R2 H6 (native area), R2 H12 (rough,
  then the penalty), R4 H3 (fairway bunker) made bogey; the other ten made par or better.
- Averages print half-up from one helper, so the par-4 tile and the SWOT both read 3.78 (151 over 40 = 3.775).
- House claim lint clear (one scope "verify" answered by printing the four per-round fairway rates).
- Fit: 816×1056, no overflow either axis, nothing past a paper edge, no row clip (minimum 13px), same in an iframe.
