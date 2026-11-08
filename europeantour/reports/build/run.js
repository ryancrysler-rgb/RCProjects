const fs = require('fs'), path = require('path');
const A = (f) => require(path.join('/home/user/rc-greenlight/automation', f));
const DPW_STD = A('dpworld-adapter.js'), DPW_P = require('./dpworld-adapter.patched.js');
const SC = A('shot-csv.js'), M = A('metrics.js');
const off = JSON.parse(fs.readFileSync('../abu_official.json', 'utf8'));
const text = fs.readFileSync('/home/user/RCProjects/europeantour/SHOT_BY_SHOT_abu-dhabi-aldar-championship-2026.csv', 'utf8');
const out = {};
for (const n of [1, 2, 3]) {
  const cardPar = {}, cardScores = {}, holeLengths = {};
  for (const [h, st] of Object.entries(off.holestats[n])) cardPar[h] = st.holePar;
  for (const [h, v] of Object.entries(off.groups['493'].rounds[n])) cardScores[h] = v[0];
  for (const [h, m] of Object.entries(off.tee[n])) holeLengths[h] = m;
  const opts = { player: 'Jon Rahm', round: n, cardPar, cardScores, holeLengths, holeLengthUnits: 'm' };
  let r, patched = false;
  try { r = DPW_STD.readCsv(text, opts); } catch (e) { console.log('R' + n + ' standard reader refused:', e.problems); r = DPW_P.readCsv(text, opts); patched = true; }
  const pm = SC.parse(r.csv).holes;
  const s = M.summary(pm);
  out[n] = { card: r.card, notes: r.notes, patched, csv: r.csv, summary: s };
  console.log('R' + n, JSON.stringify(r.card), patched ? '(patched reader)' : '', '\n  notes:', JSON.stringify(r.notes));
}
fs.writeFileSync('engine_out.json', JSON.stringify(out, null, 1));
