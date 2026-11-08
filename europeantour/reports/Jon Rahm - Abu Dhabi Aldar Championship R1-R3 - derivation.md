# Jon Rahm · Abu Dhabi Aldar Championship R1–R3 · Tournament Summary · Raw — derivation and disclosures

Deliverable: `Jon Rahm - Abu Dhabi Aldar Championship R1-R3 - Tournament Summary - Raw.html` (this folder).
Gold standard copied: `deliverables/Laurie Canter - LIV Indy Tournament Summary - Raw.html` (RC Greenlight repo,
the four-round Tournament Summary standard, 2026-08-23). Markup and CSS are the gold file's; only the content and the
hole table's column count (three rounds, not four) differ.

## Source and reconciliation

- DP World Tour Event Centre (Sportradar) shot feed, tracker event 1440, Jon Rahm (player 493, team 45 at this event),
  captured hole by hole with `auto_capture.py`; spreadsheet `SHOT_BY_SHOT_abu-dhabi-aldar-championship-2026.csv`.
- Rounds reconciled to the official group scorecards: **65 / 67 / 66 = 198 (−18)**, 18 of 18 holes agree in each round.
- Par per hole from the course-stats panel (`getGolfHoleStats.holePar`), passed to the house reader as the scorecard, which
  checks par and score per hole (`cardPar`, `cardScores`). Par 72.
- Standing from the official leaderboard (`/api/sportdata/Leaderboard/Strokeplay/2026142`, updated
  2026-11-07 13:14 UTC): **1st, not tied, −18; next best −17 (two players); 70 players, no cut.** Nobody else is named
  on the sheet.
- Field per hole: the panel's `averageHoleScore` (field average to par) for each of R1, R2, R3. FLD = par + the mean of
  the three. FLD cells are printed at 2dp and sum to the printed 69.98 exactly. Per-round field averages
  (sum over holes): R1 70.39 · R2 69.86 · R3 69.71, so he beat them by 5.39 · 2.86 · 3.71.

## The engine

Every figure is computed by the RC Greenlight engine (repo `rc-greenlight`, commit ac95b66), not by hand:
`dpworld-adapter.readCsv` (the tour reader) → `shot-csv.parse` → `metrics.summary`, `raw-report-builder.assembleFacets`
and `ladderCounts` (the published ten-band ladder, regulation approach), `nn-grade.grade` (the five non-negotiables and
the Rule 05 level).

**R2 needed one change to the reader, made in a scratch copy only (the repo is untouched):** R2 H12 is a
stroke-and-distance penalty — tee shot to the rough (331 yd), a penalty row with the ball back on the tee
(`OTB`, 478 yd from the hole), a re-tee to the fairway, a 173-yd approach to 2 ft, holed for 5 (bogey; the official card
agrees). The reader refuses `OTB` as the end lie of any non-final row, so the whole round was refused. The scratch copy
allows `OTB` on a penalty row only. Nothing else was changed. Consequences, all as the house rules already prescribe:
H12 has no clean regulation approach, so it is **off the approach ladder** (53 of 54 approaches banded; ladder greens
reconcile to GIR 46); the hole counts for Clutch Factor Ball Striking as a penalty hole (semi-clutch, bogey).
**Owner call:** whether the reader should accept this shape (a rev in the RC Greenlight repo). The re-teed shot is
classed `Approach` from 478 yd by the reader's category rule; it is excluded from the ladder by the penalty rule, so it
does not reach any printed figure.

**R1 H11 provisional:** two balls off the tee, the feed flagged neither as played (`isProvisionalSelected` false on
both; `provisionalIndex` 2 and 1). The first ball hit (seqNum 162, rough, 331 yd) is kept — a provisional only counts
once put in play — and the site's commentary confirms it ("finds the rough with a 331-yard drive... leaving 234 yards").
Our spreadsheet marks that ball played (note column says so), which is what lets the house reader read the round.

## Units and yardage

Yards, putting in feet. The feed is metric; the reader converts from the metre columns. Hole lengths passed to the
reader are the **played** tee-to-pin distance from each round's tee record (`strokeNo` 0), never the card.

## Definitions the sheet prints

- **Off the Tee** — `Tee shots FIR 31 / 42` (par-4/5 tee balls ending in the fairway; the reader's own word "Fairway" only).
  **No club field in the feed**: the gold's mandatory Driver FIR / FWY wood + Iron FIR split cannot be built, so the card
  prints `Club split · not in feed`, and Rule 01 (lay back → fairway) is NOT MEASURED. `Good drive 38 / 42` is
  `metrics.goodDrive`. `Tee avg · par 4/5 299 yd` = mean travel of all 42 par-4/5 tee balls (not "driver avg").
  `Longest 338 yd · R2 H2` = the week maximum over the same 42.
- **Approach · GIR** — 46 of 54. Ten bands, regulation approach (stroke par−2 or the stroke that reached the green), start
  distance in yards: under 40 6/6 · 40–74 3/3 · 75–100 4/4 · 101–120 0/1 · 121–140 5/6 · 141–160 7/9 · 161–180 7/8 ·
  181–200 6/7 · 201–220 4/5 · 220+ 4/4. `Inside 160` = band-chart sum of the first six bands, 25 of 29.
- **Around the Green** — scrambling 5/8 (missed greens: R1 H10, H16 · R2 H4, H6, H12, H13 · R3 H4, H6; bogeys from R2 H6,
  R2 H12, R3 H4). `Par 5s under par 10 / 12` (birdie or better: the R3 H11 eagle is one of them, so the row does not say
  "birdies"). `Par 5s −11`. `Three-putts 1` (R2 H9: 30.1 ft → 3.1 ft → 1 ft). `Best round 65 (−7) · R1`.
  **Clutch Factor Ball Striking 1 of 3 · 2 semi**: R1 H2 clutch (tee ball in a fairway bunker, birdie); R2 H6 semi
  (recovery, bogey); R2 H12 semi (penalty, bogey); R3 none. Sum of the three rounds' engine figures.
- **Putting · by round** — 86 putts. Each row = putts · holed inside 6 ft (R1 28 · 15/17, R2 28 · 14/15, R3 30 · 14/15;
  week 43/47). Row ink follows the engine's Rule 05 putter line (under 29 green; 29–31 neutral band amber).
  **Clutch Factor Putting 2 of 4** (R1 H16 5.5 ft made; R2 H4 10.5 ft made, one missed; R3 one missed). Birdie conversion
  21/46 (46%) = birdie or better ÷ greens in regulation.
- **Rule 05 level, one per round (never a week average):** R1 LOW · R2 MEDIUM (floored by three bogeys: H6, H9, H12) ·
  R3 LOW — the engine's `level`, all four measures graded each round. Shown in the dark panel because the gold's
  "vs the champion" panel has no champion mid-event (see deviations).
- Other non-negotiables, for the record (not printed on a summary): Rule 01 and 02 NOT MEASURED every round (no club
  field; no wedge ceiling on file). Rule 03 KEPT R1, ATTENTION R2 (H14, faced 67 yd) and R3 (H10 55 yd, H18 54 yd).
  Rule 04 KEPT R1/R3, ATTENTION R2 (H12).
- Inside 6 ft misses: R1 H3 5.0 ft, R1 H8 5.7 ft, R2 H9 3.1 ft (the bogey), R3 H14 5.5 ft.

## Deviations from the gold, and why

1. **Mid-event, not final.** Kick says `Thru R3`; tiles are Total / **Standing** (1 of 70) / **Lead** (1, of −17) in the
   gold's Total / Finish / Back positions — Lead is the lime-filled one, as Back is.
2. **No champion yet, and he is the leader**, so the gold's "vs the champion" panel becomes **Standing thru R3**: lead,
   the per-round margin over the field's scoring average, and the three Rule 05 levels (the precedent for a partial
   event is `Avery Schneider - GPro Tour Huntsville R1-R2 - Tournament Summary.html`'s "Round by round" panel).
3. **Both Clutch Factors are printed** (Ball Striking as the ARG chip, Putting as a Putting-card row) because all three
   rounds carry them through the same engine; the gold omitted Clutch Factor Putting only because it was on file for two
   of four rounds. `Best round` moved from the ARG chip to an ARG row to make room.
4. **Off the Tee** cannot carry the club split (no club field), as above.
5. Hole table has three round columns.

## Claim checks run before shipping

- House claim lint (`automation/claim-lint.js`) on the rendered sheet: first run blocked `term.clutch` (a plural
  "Clutch Factors" in the footnote) and asked to verify one scope ("every round") — both reworded; second run clear,
  58 sentences.
- Every SWOT figure is asserted in the generator against the engine output: 31/42, 46/54, 5/8, 43/47, one three-putt,
  86 putts, 21/46; par 5s 10 of 12 under par and −11 (field 4.54); 141–160 7 of 9 and the only band with two misses and
  the most attempts; 75–100 4/4; 161–180 7/8, 181–200 6/7, 220+ 4/4; H1, H14, H16 4-4-4 with the field under par on each;
  levels LOW/MEDIUM/LOW; bogeys R2 H6/H9/H12 and R3 H4; no doubles; GIR 16/14/16 with −7/−5/−6.
- "The other nine missed fairways made par or better": 11 par-4/5 tee balls missed the fairway; R2 H6 (native area) and
  R2 H12 (rough, then the penalty) made bogey; the other nine made par or better.
- No other player named anywhere on the sheet. No superlative without an assert behind it.

## Fit

816×1056, sheet scroll 0 on both axes, no element past a paper edge, no sideways overflow anywhere, 20 table rows
(header, 18 holes, totals) with no row clip (minimum row 13px), identical standalone and inside an iframe. The 1–3px
vertical ink overflow on the big figures is the gold's own `line-height:.8–.9` display type.
