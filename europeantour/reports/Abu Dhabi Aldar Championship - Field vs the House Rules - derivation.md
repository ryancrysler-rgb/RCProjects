# Abu Dhabi Aldar Championship · The field vs the house rules · derivation and disclosures

Deliverable: `Abu Dhabi Aldar Championship - Field vs the House Rules - Raw.html` (one sheet, 816×1056, on the house
sheet stylesheet — the head of `Laurie Canter - LIV Indy Tournament Summary - Raw.html`). There is no gold standard for a
field study; the anatomy borrows the Raw family's header, a THE READ panel (the arc's), and a rule table. Build record:
`field-abu-dhabi/` (scripts, the graded rounds, the roll-up, the field spreadsheet gzipped).

## Source and reconciliation

- DP World Tour Event Centre (tracker event 1440). Every player (tracker numbers 1–80 walked; 70 players found, numbers
  38 and 71–80 empty), every round, every hole, captured with `field_capture.py` (tracker opened on hole 1 of each round,
  then the tracker's own next arrow; no 3D rendering). One round (Van Driel R1) was pulled hole by hole with
  `auto_capture.py` because one hole never reported a holed ball in the fast capture.
- **280 rounds, 19,680 shots; every round matches its official card on all 18 holes**; every shot matched to the event feed.
- Par and field averages from the course-stats panel per round; played hole lengths = the median tee position across the
  field per round. Finishes from the group scorecards (tournamentPosition), which agree with the official leaderboard.

## The engine — house rules v18.1

Every round graded by the RC Greenlight engine at **Rev 362 (house rules v18.1)**: `dpworld-adapter.readCsv` against the
card (par, score per hole, hole lengths) → `shot-csv.parse` → `metrics.summary`, `nn-grade.grade`,
`raw-report-builder.ladderCounts`. Rule names and the rank order are the engine's (`HOUSE_RULES_RANKED`).

**278 of 280 rounds graded.** Calum Hill R1 (H18) and Kristoffer Reitan R4 (H7) each have a tee shot the feed counted with
no ball position at all; grading them would mean guessing, so they are left out, and so are those two players' weeks
(the study counts complete weeks): **68 players, 272 rounds** in the table.

**99 rounds read with a patched copy of the reader** (the RC Greenlight repo is untouched; the patches are listed so the
owner can decide whether the reader should learn them):
1. The score word `DoubleBogeyOrWorse` takes the card's par (the reader knows `EagleOrBetter` this way; it refused the
   double-bogey word) — 97 rounds, the main cause.
2. A stroke-and-distance penalty row may end on the tee (`OTB`) — 6 rounds (Rahm R2 H12 among them).
3. A water ball's drop row typed `BallDrop` (not `Penalty`), numbered in sequence with no travel and matching the card, is
   the penalty stroke — 4 rounds.
4. A penalty stroke the feed counted with no ball position leaves the ball where it was — 1 round.
5. Lie codes read as **Other**: `OWA` (water; owner ruling 2026-10-31), and on the `OTH` ruling ("Other can be ruled outside
   of fairway"): `OBU` (the commentary says "bushes" 3 times in 4), `ODO` ("dirt", 4 of 4), `OUK` and `OTF` (no consistent
   meaning) — 20 strokes in all.
Also in our own spreadsheet build: a lone ball the feed flags provisional (and never marks selected) is the ball played —
the hole still matches the card with it counted (31 rounds were refused before this).

## Groups

Rahm (winner, 1 player, 4 rounds) · the 12 others who finished T10 or better (48 rounds) · the 55 who finished 11th or worse
(220 rounds). Tint = the top 10 better (green) or worse (amber) than 11th-on by 5 points or more on rates, 0.25 a round on
counts, 0.15 a hole on to-par.

## Measures (as the tour shot study counts them, where it has a line)

- 01: greens in regulation from the fairway / from the rough (the regulation approach's start lie, par 4/5). The lay-back
  itself is NOT MEASURED (no club).
- 02: rounds in which a chip, pitch or bunker shot (a stroke from 40 yd or less off the green) finished off the green.
- 03: strokes that finished 40–74 yd from the hole off the green, a round; greens from 40–74 yd (ladder).
- 04: rounds with no penalty stroke (the tour study's proxy; no hazard lines in the feed).
- 05: the engine's level per round; over par after the first six holes played (playing order from the commentary feed).
- 1: putts from 6 ft or less holed; 3–6 ft holed (the tour line's band).
- 2: par 5s on the green in 3 or fewer.
- 3: regulation approaches finishing on the green under 40 ft (or holed); three-putts when the first putt was 40 ft+.
- 4: first putts of 24 ft+ finishing within 10% of the start (or holed).
- 5: chips, pitches and bunker shots (≤40 yd, off the green) finishing inside 6 ft (or holed).
- 6: penalty holes a round (the tour study's recovery line); the club rule itself is NOT MEASURED.
- 7: greens from 75–100 yd (the study's own-band line). 8: birdie or better ÷ greens hit. 9: bogey or worse on the next
  hole played after a bogey or worse. 10: par-5 third shots from 121 yd+, score to par (no third shot when the green was
  reached in two).
- Clutch Factor Ball Striking / Putting / Response / Damage Control: `metrics.js` definitions, summed over rounds.

## The read, checked

Asserted in the generator against the roll-up: fairways 66% for both the top 10 and 11th-on; greens 85% vs 77%; greens from
the fairway 92% vs 85%; bogey-after-bogey 11% vs 20%; HIGH-stress rounds 13/48 (27%) vs 107/220 (49%); holed from 6 ft or
less 93.3% vs 92.6%; Rahm 16/16 par 5s on in three, 0/5 bogey-after-bogey, 0/5 three-putts from 40 ft+, 0/4 rounds over par
after six holes; field strokes against the field average by level: LOW +2.83, MEDIUM +0.97, HIGH −2.00.

## Claim lint and fit

- House claim lint: one BLOCK remains, `claim.spanImplied` on **"3 Approach inside 40 feet" — the rule's published name**
  (`HOUSE_RULES_RANKED` rank 3). The lint exempts "inside 6 feet" as a published standard but predates the v17 rule; renaming
  a published rule would break the "names come from the engine" rule, so the name is kept and the gap is flagged for the RC
  Greenlight session (add "inside 40 feet" to the lint's published-standard exemption). Every other line is clear; the
  "inside 6 ft" wording is the house phrase the lint recognises.
- Fit: 816×1056, no overflow either axis, nothing past a paper edge, 30 table rows with no clip (minimum 16px), same in an
  iframe.

## Not measured

The lay-back (01), the full-wedge tier of 02, 04's margin itself (penalty-free rounds stand in), rule 6's club, front pin
(11) and the long side / open side (12) (no pin sheet or positions), The Check (needs each player's plan), the par-5 go line
and the short par 4 (need the bag).
