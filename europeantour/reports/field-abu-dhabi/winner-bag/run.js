'use strict';
const fs = require('fs'), path = require('path');
const E = '/home/user/rc-greenlight/automation/';
const DPW = require(E + 'dpworld-adapter.js'), SC = require(E + 'shot-csv.js'), M = require(E + 'metrics.js'), NN = require(E + 'nn-grade.js'), HR = require(E + 'house-rules.js');
const BC = require(E + 'bag-clubs.js'), P5 = require(E + 'par5-go.js');
const S = path.join(__dirname, '..');
const text = fs.readFileSync(S + '/fieldrb/SHOT_BY_SHOT_abu-dhabi-field-70-players.csv', 'utf8');
const off = JSON.parse(fs.readFileSync(S + '/rcp/europeantour/reports/build-final/abu_official.json', 'utf8')); const cards = JSON.parse(fs.readFileSync(__dirname + '/cards.json', 'utf8'));
// Jon Rahm's bag: totals from proyardages.pages.dev (Golf Monthly figures; GW/SW/LW marked "Estimated" there)
const bag = { units: 'yd', clubs: [
  ['Driver', 320], ['3W', 282], ['5i', 225], ['6i', 210], ['7i', 195], ['8i', 178], ['9i', 160], ['PW', 143], ['GW', 123], ['SW', 105], ['LW', 84] ]
  .map(([name, total]) => ({ name, total, tee: /Driver|W$/.test(name) }))
  // Golf Monthly carries (no total published): kept as the club's carry, marked so (owner 2026-11-08: "Add Golf Monthly carries")
  .concat([['5W', 256], ['2i', 246], ['4i', 230]].map(([name, carry]) => ({ name, carry, tee: /W$/.test(name), note: 'carry only (Golf Monthly)' }))) };
const pid = '493', name = 'Jon Rahm';
const out = [];
for (const rnd of ['1', '2', '3', '4']) {
  const cardPar = {}, holeLengths = {};
  for (let h = 1; h <= 18; h++) { cardPar[h] = off.holestats[rnd][h].holePar; holeLengths[h] = off.tee[rnd][String(h)]; }
  const r = DPW.readCsv(text, { player: name, playerId: pid, round: rnd, cardPar, cardScores: cards[rnd], holeLengths, holeLengthUnits: 'm' });
  const holes = SC.parse(r.csv).holes;
  const before = NN.grade(holes, { published: HR.NON_NEGOTIABLES, wedgeMaxYd: null });
  const res = BC.apply(holes, bag);
  const after = NN.grade(holes, { published: HR.NON_NEGOTIABLES, wedgeMaxYd: 143 });
  const s = M.summary(holes);
  const tees = holes.filter((h) => +h.par >= 4).map((h) => { const t = h.shots[0]; return { hole: h.hole, par: +h.par, club: t.club, went: t.shotDistance, end: t.endLie }; });
  out.push({ round: +rnd, score: s.card.strokes, bagNote: res.note, rows: res.rows, tees,
    before: before.rules.map((x) => ({ n: x.n, state: x.state, level: x.level || null })),
    after: after.rules.map((x) => ({ n: x.n, state: x.state, level: x.level || null, detail: x.detail || x.why || '' })) });
}
fs.writeFileSync(__dirname + '/rahm.json', JSON.stringify({ bag, deck: P5.deckClub ? P5.deckClub(bag) : null, out }, null, 1));
for (const o of out) {
  console.log('R' + o.round, o.score, '|', o.bagNote);
  console.log('  before', o.before.map((x) => x.n + ':' + (x.level || x.state)).join(' '));
  console.log('  after ', o.after.map((x) => x.n + ':' + (x.level || x.state)).join(' '));
  console.log('  tee   ', o.tees.map((t) => 'H' + t.hole + ' ' + t.club + ' ' + t.went + ' ' + t.end).join(' | '));
  o.after.filter((x) => x.n <= 2).forEach((x) => console.log('  #' + x.n, x.detail.slice(0, 260)));
}
// ---- page 2: Rahm vs the house rules, clubs from his bag
const SR = require(E + 'summary-rules.js'), SLOT = require(E + 'data-slot.js');
const rounds = ['1', '2', '3', '4'].map((rnd) => {
  const cardPar = {}, holeLengths = {};
  for (let h = 1; h <= 18; h++) { cardPar[h] = off.holestats[rnd][h].holePar; holeLengths[h] = off.tee[rnd][String(h)]; }
  const r = DPW.readCsv(text, { player: name, playerId: pid, round: rnd, cardPar, cardScores: cards[rnd], holeLengths, holeLengthUnits: 'm' });
  const holes = SC.parse(r.csv).holes; BC.apply(holes, bag);
  return { n: +rnd, holes, source: 'files', order: null };
});
const P = SR.page(rounds, { units: 'yd', wedgeMaxYd: 143 });
P.notes.push('Clubs are not in the tour shot file: each was read from Jon Rahm’s published stock yardages (totals; gap, sand and lob wedge estimated by the source; 5-wood, 2-iron, 4-iron carry only) by how far the shot went or the distance to the hole — the most likely club, so rules 01 and 02 read Attention, never Broken');
P.notes = P.notes.map((n) => /stored files/.test(n) ? 'R1–R4: read from the DP World Tour shot file by the house reader, every hole adding up to the official card (65, 67, 66, 67 = 265)' : n);
// owner 2026-11-08 ("Lead with the count"): every tee club here is read from the bag, so rule 01 leads as a count and is
// never the "next to master"; the next is the most-flagged rule whose clubs are not guessed.
{
  let lb = 0, lbFw = 0, w = 0, wOn = 0;
  out.forEach((o) => { o.after.forEach((x) => {
    let m = /(\d+) of (\d+) lay-backs missed/.exec(x.detail); if (x.n === 1 && m) { lb += +m[2]; lbFw += +m[2] - +m[1]; }
    m = /Every lay-back \((\d+)\)/.exec(x.detail); if (x.n === 1 && m) { lb += +m[1]; lbFw += +m[1]; }
    m = /(\d+) of (\d+) wedge shots finished off/.exec(x.detail); if (x.n === 2 && m) { w += +m[2]; wOn += +m[2] - +m[1]; }
    m = /All (\d+) wedge shots finished on/.exec(x.detail); if (x.n === 2 && m) { w += +m[1]; wOn += +m[1]; }
  }); });
  const dz = HR.NON_NEGOTIABLES.find((x) => x.key === 'deadzone');
  const flagged = P.groups[0].rules[2].rows[0].cells.map((c, i) => (/attention|broken/.test(c) ? 'R' + (i + 1) : null)).filter(Boolean);
  P.read = { headline: lbFw + ' of ' + lb + ' lay-backs found the fairway and ' + wOn + ' of ' + w + ' wedges the green (clubs read from his bag).',
    next: { n: 3, name: dz.name || 'Never leave 40\u201374 yards', rounds: flagged }, decision: dz.plain.says };
  P.notes = P.notes.map((n) => /^Clubs are not in the tour shot file/.test(n) ? 'Jon Rahm alone (no one else in the field has a bag on file, so rules 01\u201302 are not compared with the field): clubs are not in the tour shot file, so each was read from his published stock yardages (ProYardages totals after Golf Monthly, its GW/SW/LW estimated; Golf Monthly carries for 5-wood, 2-iron, 4-iron) \u2014 the most likely club, so rules 01\u201302 read Attention, never Broken' : n);
  console.log('READ', P.read.headline, '| next', P.read.next.name, P.read.next.rounds.join(','));
}
P.groups.forEach((g) => g.rules.forEach((r) => r.rows.forEach((row) => { if (row.label === 'A driver or fairway wood from a bad lie') row.label = 'Bad lies played with a driver or wood'; })));
fs.writeFileSync(__dirname + '/rahm-page.json', JSON.stringify(P, null, 1));
const tpl = fs.readFileSync(E + 'tournament-summary.template.html', 'utf8');
const sc = [65, 67, 66, 67];
fs.writeFileSync(__dirname + '/rahm.html', SLOT.fill(tpl, { player: 'Jon Rahm', event: 'Abu Dhabi Aldar Championship', rounds: 4, roundNumbers: [1, 2, 3, 4], scores: sc, total: 265, par: 72, facets: {}, holes: [], swot: {}, rulesPage: P }, 'tournament summary'));
console.log('PAGE', P.read.headline, P.read.next ? 'Next: ' + P.read.next.name + ' (' + P.read.next.rounds.join(', ') + ')' : '', '| levels', P.levels.map((x) => x.level).join(' '));
P.groups.forEach((g) => g.rules.forEach((r) => r.rows.forEach((row, i) => console.log((i ? '   ' : r.name.slice(0, 40)).padEnd(41), (row.label || '').slice(0, 44).padEnd(45), JSON.stringify(row.cells || row.why), row.week ? JSON.stringify(row.week) : ''))));
