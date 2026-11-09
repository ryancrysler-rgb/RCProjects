/* Rule 02, literal, for the Abu Dhabi field: every shot from 150 yd in, off the green, on the green or holed. Added to the stored
 * rounds.json (every other measure untouched). Cards from the feed's own score words placed by the course par (as for the winner). */
'use strict';
const fs = require('fs'), E = '/home/user/rc-greenlight/automation/';
const DPW = require(E + 'dpworld-adapter.js'), SC = require(E + 'shot-csv.js');
const text = fs.readFileSync(__dirname + '/SHOT_BY_SHOT_abu-dhabi-field-70-players.csv', 'utf8');
const off = JSON.parse(fs.readFileSync(__dirname + '/../rcp/europeantour/reports/build-final/abu_official.json'));
const R = JSON.parse(fs.readFileSync(__dirname + '/rounds.json'));
const isGreen = (l) => /^green$/i.test(String(l || ''));
const W = { EagleOrBetter: -2, Eagle: -2, Birdie: -1, Par: 0, Bogey: 1, DoubleBogeyOrWorse: null };
const lines = text.split('\n'); const head = lines[0].replace(/^﻿/, '').split(',');
const csvSplit = (line) => { const out = []; let cur = '', q = false; for (const ch of line) { if (ch === '"') q = !q; else if (ch === ',' && !q) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; };
const ci = (c) => head.indexOf(c);
const cards = {};
lines.slice(1).forEach((l) => { if (!l.trim()) return; const c = csvSplit(l); if (c[ci('eventType')] !== 'BallHoled') return;
  const k = c[ci('playerId')] + '|' + c[ci('round')], hole = c[ci('hole')];
  (cards[k] = cards[k] || {})[hole] = +c[ci('shot')]; });
let done = 0, failed = [];
for (const m of R.results) {
  const rnd = String(m.round), cardPar = {}, holeLengths = {};
  for (let h = 1; h <= 18; h++) { cardPar[h] = off.holestats[rnd][h].holePar; holeLengths[h] = off.tee[rnd][String(h)]; }
  try {
    const r = DPW.readCsv(text, { player: m.name, playerId: m.pid, round: rnd, cardPar, cardScores: cards[m.pid + '|' + rnd], holeLengths, holeLengthUnits: 'm' });
    const holes = SC.parse(r.csv).holes;
    const sc = holes.reduce((t, h) => t + h.score, 0);
    if (sc !== m.score) { failed.push(m.name + ' R' + rnd + ' ' + sc + '≠' + m.score); continue; }
    m.w150 = [0, 0]; m.w150f = [0, 0]; m.w150Miss = 0;
    holes.forEach((h) => h.shots.forEach((x) => {
      if (x.isPutt || x.penalty || x.startYd == null || x.startYd > 150 || isGreen(x.startLie)) return;
      const on = x.holed || isGreen(x.endLie);
      m.w150[1]++; if (on) m.w150[0]++; else m.w150Miss = 1;
      if (x.startYd >= 40) { m.w150f[1]++; if (on) m.w150f[0]++; }
    }));
    done++;
  } catch (e) { failed.push(m.name + ' R' + rnd + ': ' + ((e.problems || [e.message]).join('; ')).slice(0, 80)); }
}
fs.writeFileSync(__dirname + '/rounds.json', JSON.stringify(R, null, 1));
console.log('rounds with the literal count', done, 'of', R.results.length, '| not read', failed.length); failed.slice(0, 8).forEach((x) => console.log('  ' + x));
