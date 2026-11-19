# Player seasons, 2026 (private, internal)

- blades-brown-2026.tgz (pulled 19 Nov 2026, owner "yes pull Blades Brown's season"): all 48 individual stroke-play rounds of his
  2026 PGA TOUR season through Austin (14 events; the Zurich team event is left out). R<event>/raw/66417-<round>.json
  (get_player_shots_compact) + cs<round>.json (field hole averages) for every event; results-2026.json = his results page
  (finish, round scores, money). All 48 round totals match his official scores. Shot detail is missing (finish lies blank) in 6 rounds:
  AmEx R1-R2 (second course) and Puerto Rico R1-R4, so 42 rounds carry full shot detail. Source: pgatour.com via our Parse.bot build
  7f7abae7 (40 new rounds + 10 field files, 50 credits) and rounds already saved in ../pga-2026 (AmEx, Los Cabos).
- blades-brown-2026-kft.tgz (pulled 19 Nov 2026, owner "he should also have Korn Ferry Tour shot tracking stats"): all 68 rounds of his
  2026 Korn Ferry Tour season (18 events, H2026…), H<event>/raw/66417-<round>.json + cs<round>.json + results-2026.json (his KFT results
  page). 66 of 68 round totals match his official scores (H2026125 R2 and H2026171 R4 have a blank 18th in the feed). Shot detail is missing
  in 23 rounds (Bahamas x2, Panama, Astara, Club Car, Tulum, BMW R1): 45 rounds carry full shot detail. 135 credits.
- blades-brown-2026-winners.tgz (19 Nov 2026, owner "compare Blades brown against the winner of every event, hole by hole"): the
  winner's rounds for every Korn Ferry event he played (H2026…/raw, rounds he played; kft-winners.json names them), Mexico (Novak) and
  Austin (Ramey), and Los Cabos runner-up Ben James (he won). The other PGA TOUR winners' rounds are in ../pga-2026-winners-field.
  98 credits.
