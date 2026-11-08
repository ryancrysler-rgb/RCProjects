# Abu Dhabi field: rounds read with a patched reader, and why

70-player shot file: `europeantour/reports/field-abu-dhabi/SHOT_BY_SHOT_abu-dhabi-field-70-players.csv` (280 rounds, 19,680 shots, every round matching its card; built by build_shots.py with the lone-provisional fix, commit 93277d1).

Engine: Rev 362 at cf44dee (house rules v18.1), standard reader first; the patched copy only when the standard reader refused. 99 rounds patched, 2 not graded.

| Player | Round | Cause | Standard reader said |
|---|---|---|---|
| Matt Wallace | R2 | lie code OWA read as Other | H18 shot 2 ends on lie code OWA, which we have not proven |
| Matt Wallace | R3 | DoubleBogeyOrWorse score word | H15: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Tyrrell Hatton | R1 | DoubleBogeyOrWorse score word | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Jeff Winther | R1 | DoubleBogeyOrWorse score word | H5: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H14: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Jeff Winther | R3 | DoubleBogeyOrWorse score word | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Jeff Winther | R4 | DoubleBogeyOrWorse score word | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Tommy Fleetwood | R3 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Rory McIlroy | R1 | DoubleBogeyOrWorse score word | H12: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Rory McIlroy | R3 | DoubleBogeyOrWorse score word | H10: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Andy Sullivan | R2 | lie code OBU read as Other | H11 shot 1 ends on lie code OBU, which we have not proven |
| Ricardo Gouveia | R2 | DoubleBogeyOrWorse score word | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Ricardo Gouveia | R3 | stroke-and-distance row ends on the tee (OTB) | H11 shot 2 ends on lie code OTB, which we have not proven |
| Ricardo Gouveia | R4 | DoubleBogeyOrWorse score word | H18: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Jorge Campillo | R2 | DoubleBogeyOrWorse score word | H14: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Joost Luiten | R2 | lie code OBU read as Other | H4 shot 1 ends on lie code OBU, which we have not proven |
| Joost Luiten | R4 | DoubleBogeyOrWorse score word | H4: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Richard Sterne | R3 | penalty with no ball position | H12 shot 2 ends on no lie code |
| Aaron Rai | R2 | lie code ODO read as Other | H17 shot 1 ends on lie code ODO, which we have not proven |
| Aaron Rai | R4 | stroke-and-distance row ends on the tee (OTB) | H14 shot 2 ends on lie code OTB, which we have not proven |
| Joakim Lagergren | R1 | DoubleBogeyOrWorse score word | H12: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Joakim Lagergren | R3 | DoubleBogeyOrWorse score word | H3: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Joakim Lagergren | R4 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H12: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Nacho Elvira | R3 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Nacho Elvira | R4 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Julien Guerrier | R1 | DoubleBogeyOrWorse score word | H18: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Scott Jamieson | R1 | DoubleBogeyOrWorse score word | H16: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Scott Jamieson | R2 | lie code ODO/OUK read as Other | H2 shot 1 ends on lie code ODO, which we have not proven; H18 shot 2 ends on lie code OUK, which we have not proven |
| Scott Jamieson | R3 | DoubleBogeyOrWorse score word | H12: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Scott Jamieson | R4 | DoubleBogeyOrWorse score word; stroke-and-distance row ends on the tee (OTB) | H2 shot 2 ends on lie code OTB, which we have not proven; H10: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Grant Forrest | R1 | DoubleBogeyOrWorse score word | H7: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Grant Forrest | R2 | DoubleBogeyOrWorse score word; stroke-and-distance row ends on the tee (OTB); lie code ODO read as Other | H8 shot 1 ends on lie code ODO, which we have not proven; H11 shot 2 ends on lie code OTB, which we have not proven; H13: the score word “DoubleBogeyOrWorse” is |
| Victor Perez | R2 | DoubleBogeyOrWorse score word | H13: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Victor Perez | R4 | DoubleBogeyOrWorse score word | H5: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Shaun Norris | R3 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Shaun Norris | R4 | lie code OWA read as Other | H16 shot 1 ends on lie code OWA, which we have not proven; H18 shot 2 ends on lie code OWA, which we have not proven |
| Patrick Reed | R1 | DoubleBogeyOrWorse score word | H18: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Patrick Reed | R2 | DoubleBogeyOrWorse score word | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Patrick Reed | R4 | DoubleBogeyOrWorse score word | H11: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Jon Rahm | R2 | stroke-and-distance row ends on the tee (OTB) | H12 shot 2 ends on lie code OTB, which we have not proven |
| JC Ritchie | R2 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| JC Ritchie | R4 | DoubleBogeyOrWorse score word | H13: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H15: the score word “DoubleBogeyOrWorse” is not one we read, so the h |
| Antoine Rozner | R2 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Darius Van Driel | R3 | DoubleBogeyOrWorse score word | H5: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Guido Migliozzi | R1 | DoubleBogeyOrWorse score word; lie code OBU read as Other | H7: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H13 shot 1 ends on lie code OBU, which we have not proven |
| Guido Migliozzi | R2 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H5: the score word “DoubleBogeyOrWorse” is not one we read, so the hol |
| Guido Migliozzi | R3 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hol |
| Calum Hill | R3 | DoubleBogeyOrWorse score word | H15: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Alejandro Del Rey | R1 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Alejandro Del Rey | R3 | DoubleBogeyOrWorse score word; stroke-and-distance row ends on the tee (OTB) | H10: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H15 shot 2 ends on lie code OTB, which we have not proven |
| Eugenio Chacarra | R2 | DoubleBogeyOrWorse score word | H14: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Eugenio Chacarra | R4 | DoubleBogeyOrWorse score word | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Thriston Lawrence | R4 | lie code ODO read as Other | H18 shot 3 ends on lie code ODO, which we have not proven |
| Francesco Laporta | R2 | DoubleBogeyOrWorse score word | H14: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Francesco Laporta | R4 | DoubleBogeyOrWorse score word | H13: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Daniel Rodrigues | R3 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H18: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Marcus Armitage | R3 | DoubleBogeyOrWorse score word | H4: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Niklas Nørgaard | R1 | DoubleBogeyOrWorse score word | H4: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Niklas Nørgaard | R2 | DoubleBogeyOrWorse score word | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Niklas Nørgaard | R4 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Hennie du Plessis | R1 | DoubleBogeyOrWorse score word | H18: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Hennie du Plessis | R3 | lie code OBU read as Other | H6 shot 1 ends on lie code OBU, which we have not proven |
| Hennie du Plessis | R4 | lie code OWA read as Other | H8 shot 1 ends on lie code OWA, which we have not proven |
| Ugo Coussaud | R1 | DoubleBogeyOrWorse score word | H12: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Oliver Lindell | R3 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H12: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Manuel Elvira | R1 | lie code ODO read as Other | H1 shot 1 ends on lie code ODO, which we have not proven |
| Manuel Elvira | R4 | DoubleBogeyOrWorse score word | H11: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Nathan Kimsey | R4 | DoubleBogeyOrWorse score word | H13: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Jordan Gumberg | R2 | water drop row typed BallDrop | H17 shot 2 is a drop row (the feed’s penalty shape is not proven); H17: no row for shot 2 (a penalty or a lost row — never guessed) |
| Jordan Gumberg | R4 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H13: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Casey Jarvis | R3 | water drop row typed BallDrop | H8 shot 2 is a drop row (the feed’s penalty shape is not proven); H8: no row for shot 2 (a penalty or a lost row — never guessed) |
| Yurav Premlall | R1 | DoubleBogeyOrWorse score word | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H18: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Yurav Premlall | R2 | DoubleBogeyOrWorse score word; lie code OWA read as Other | H6: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hol |
| Yurav Premlall | R4 | DoubleBogeyOrWorse score word; lie code OTF read as Other | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H15 shot 2 ends on lie code OTF, which we have not proven |
| Michael Hollick | R1 | DoubleBogeyOrWorse score word; lie code OWA read as Other | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H18 shot 2 ends on lie code OWA, which we have not proven |
| Michael Hollick | R3 | DoubleBogeyOrWorse score word | H10: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H13: the score word “DoubleBogeyOrWorse” is not one we read, so the h |
| Michael Hollick | R4 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H13: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Filippo Celli | R1 | lie code OWA read as Other | H14 shot 2 ends on lie code OWA, which we have not proven |
| Filippo Celli | R4 | DoubleBogeyOrWorse score word | H15: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H16: the score word “DoubleBogeyOrWorse” is not one we read, so the h |
| Gregorio De Leo | R3 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| David Puig | R1 | DoubleBogeyOrWorse score word | H4: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| David Puig | R4 | DoubleBogeyOrWorse score word | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Yuto Katsuragawa | R2 | DoubleBogeyOrWorse score word | H17: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Dan Bradbury | R2 | water drop row typed BallDrop | H16 shot 2 is a drop row (the feed’s penalty shape is not proven); H16: no row for shot 2 (a penalty or a lost row — never guessed) |
| Tom Vaillant | R1 | DoubleBogeyOrWorse score word | H3: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Tom Vaillant | R2 | water drop row typed BallDrop | H8 shot 2 is a drop row (the feed’s penalty shape is not proven); H8: no row for shot 2 (a penalty or a lost row — never guessed) |
| Martin Couvra | R4 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H15: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Angel Ayora | R1 | DoubleBogeyOrWorse score word | H2: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Angel Ayora | R2 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Wenyi Ding | R2 | DoubleBogeyOrWorse score word | H18: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Wenyi Ding | R4 | DoubleBogeyOrWorse score word | H9: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Angel Hidalgo | R1 | lie code OWA read as Other | H18 shot 2 ends on lie code OWA, which we have not proven |
| Angel Hidalgo | R2 | lie code ODO read as Other | H6 shot 1 ends on lie code ODO, which we have not proven |
| Joe Dean | R3 | DoubleBogeyOrWorse score word | H2: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H15: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Jacob Skov Olesen | R1 | DoubleBogeyOrWorse score word | H1: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H2: the score word “DoubleBogeyOrWorse” is not one we read, so the hol |
| Jacob Skov Olesen | R4 | DoubleBogeyOrWorse score word | H13: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Davis Bryant | R1 | DoubleBogeyOrWorse score word | H3: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Davis Bryant | R2 | DoubleBogeyOrWorse score word | H10: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Davis Bryant | R3 | DoubleBogeyOrWorse score word | H15: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown |
| Kota Kaneko | R4 | DoubleBogeyOrWorse score word | H8: the score word “DoubleBogeyOrWorse” is not one we read, so the hole’s par is unknown; H12: the score word “DoubleBogeyOrWorse” is not one we read, so the ho |
| Kristoffer Reitan | R4 | not graded | H7 shot 1 ends on no lie code |
| Calum Hill | R1 | not graded | H18 shot 1 ends on no lie code |
