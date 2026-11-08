const SC = require('/home/user/rc-greenlight/automation/shot-csv.js');
const o = require('./engine_out.json'), raw = require('./raw_out.json'), off = require('../abu_official.json');
const num = (s) => parseFloat(String(s || '').replace(/[^0-9.\-]/g, ''));
const F = { rounds: {}, holes: {} };
const tee = [];
for (const n of [1, 2, 3]) {
  const holes = SC.parse(o[n].csv).holes, s = raw[n].summary, fa = raw[n].facets;
  const r = { score: s.card.strokes, toPar: s.card.toPar, putts: s.putts.value, gir: s.gir.display, fw: s.fairways.display,
    scr: s.scrambling.display, bc: s.birdieConversion.display, counts: s.counts, goodDrive: s.goodDrive.display,
    inside6: (fa.putt.rows.find(x => x[0] === 'Inside 6 ft') || [])[1], onePutts: (fa.putt.rows.find(x => x[0] === 'One-putts') || [])[1],
    threePutts: (fa.putt.rows.find(x => x[0] === 'Three-putts') || [])[1], avg1st: (fa.putt.rows.find(x => x[0] === 'Avg 1st · GIR') || [])[1],
    cfp: s.clutchFactorPutting, cfbs: s.clutchFactorBallStriking, level: raw[n].nn.rules.find(x => x.n === 5).level,
    bogeys: [], birdies: [], par5: [] };
  for (const h of holes) {
    const d = h.score - h.par;
    (F.holes[h.hole] = F.holes[h.hole] || { par: h.par, scores: {}, yards: {} }).scores[n] = h.score;
    F.holes[h.hole].yards[n] = h.yards;
    if (d > 0) r.bogeys.push('H' + h.hole + (d > 1 ? '(+' + d + ')' : ''));
    if (d < 0) r.birdies.push('H' + h.hole + (d < -1 ? '(eagle)' : ''));
    if (h.par === 5) r.par5.push({ hole: h.hole, score: h.score });
    if (h.par >= 4) { const t = h.shots[0]; tee.push({ r: n, h: h.hole, yd: num(t.shotDistance), end: t.endLie }); }
  }
  F.rounds[n] = r;
}
// field per hole: par + mean of the panel's per-round average to par
for (const [h, v] of Object.entries(F.holes)) {
  const fld = [1, 2, 3].map(n => off.holestats[n][h]);
  if (fld.some(x => !x || x.holePar !== v.par)) throw new Error('panel par/field mismatch H' + h);
  v.fieldToPar = [1, 2, 3].map(n => off.holestats[n][h].averageHoleScore);
  v.fld = v.par + v.fieldToPar.reduce((a, b) => a + b, 0) / 3;
  v.avg = (v.scores[1] + v.scores[2] + v.scores[3]) / 3;
  v.diff = v.fld - v.avg;
}
const teeAvg = tee.reduce((a, t) => a + t.yd, 0) / tee.length;
const longest = tee.reduce((a, t) => (t.yd > a.yd ? t : a), { yd: 0 });
F.tee = { n: tee.length, avg: teeAvg, longest, fairways: tee.filter(t => t.end === 'Fairway').length, ends: tee.reduce((m, t) => (m[t.end] = (m[t.end] || 0) + 1, m), {}) };
// scoring average by par
F.byPar = {};
for (const p of [3, 4, 5]) {
  const hs = Object.values(F.holes).filter(v => v.par === p), sc = hs.flatMap(v => [1, 2, 3].map(n => v.scores[n]));
  F.byPar[p] = { holes: sc.length, avg: sc.reduce((a, b) => a + b, 0) / sc.length, toPar: sc.reduce((a, b) => a + b - p, 0),
    field: hs.reduce((a, v) => a + v.fld, 0) / hs.length };
}
F.fieldTotal = Object.values(F.holes).reduce((a, v) => a + v.fld, 0);
F.fieldRound = [1, 2, 3].map(n => Object.values(off.holestats[n]).reduce((a, x) => a + x.holePar + x.averageHoleScore, 0));
require('fs').writeFileSync('figures.json', JSON.stringify(F, null, 1));
console.log(JSON.stringify({ rounds: F.rounds }, null, 0).slice(0, 3000));
console.log('tee', JSON.stringify(F.tee));
console.log('byPar', JSON.stringify(F.byPar));
console.log('field total (sum of 3-rd mean per hole)', F.fieldTotal.toFixed(2), 'per-round field', F.fieldRound.map(x => x.toFixed(2)));
for (const h of Object.keys(F.holes).sort((a, b) => a - b)) { const v = F.holes[h]; console.log('H' + h, 'par', v.par, 'yds', JSON.stringify(v.yards), 'sc', [1,2,3].map(n => v.scores[n]).join('-'), 'avg', v.avg.toFixed(2), 'fld', v.fld.toFixed(2), 'diff', (v.diff >= 0 ? '+' : '') + v.diff.toFixed(2)); }
