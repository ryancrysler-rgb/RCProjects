/* Page 2 (the player vs the house rules) for a winner whose clubs are read from a published bag — the owner's rulings of
 * 2026-11-08/09, applied in one place for every such page (Rahm, Blades Brown, the WWT field report's page 2):
 *   LITERAL (owner: "The rule is on the green all shots so we need literal interpretation of our rules" · form: "Broken"):
 *     rule 01 — every lay-back tee shot (a par-4/5 tee club that is not the driver) finds the fairway; one miss = Broken.
 *     rule 02 — every wedge shot (PW/GW/SW/LW, full or greenside, lay-up wedges from beyond the wedge ceiling excluded as the
 *               engine does) finishes on the green or in the hole; one miss = Broken. Clubs read from the bag still grade this way.
 *   WORDING (form: "Wedge shots on the green"): rule 02 leads with the combined count, the split underneath.
 *   LEAD WITH THE COUNT (owner 2026-11-08): the read leads with the counts; a rule graded on read clubs is never "next to master".
 *   PLAIN LABELS: "Bad lies played with a driver or wood", "Birdie or better, of greens hit". */
'use strict';
const E = '/home/user/rc-greenlight/automation/';
const NN = require(E + 'nn-grade.js'), HR = require(E + 'house-rules.js');
const frac = (a) => a[0] + '/' + a[1];
function rate(label, per) {
  const week = per.reduce((t, x) => [t[0] + x[0], t[1] + x[1]], [0, 0]);
  return { kind: 'rate', label, good: true, cells: per.map((x) => (x[1] ? frac(x) : '—')), week, weekPct: week[1] ? Math.round(100 * week[0] / week[1]) : null };
}
function fix(P, rounds, wedgeMaxYd) {
  const lay = [], wAll = [], wFull = [], wG = [], g1 = [], g2 = [];
  rounds.forEach((r) => {
    let l = [0, 0];
    r.holes.forEach((h) => { if (+h.par < 4) return; const t = h.shots[0]; if (!t || t.club === 'Driver' || !t.club) return; l[1]++; if (/^fairway$/i.test(t.endLie)) l[0]++; });
    const W = NN.wedgeShots(r.holes, { wedgeMaxYd }).items;
    const on = (it) => it.onGreen || !!it.sh.holed;
    const a = [W.filter(on).length, W.length], f = W.filter((it) => it.tier === 'f'), g = W.filter((it) => it.tier === 'g');
    lay.push(l); wAll.push(a); wFull.push([f.filter(on).length, f.length]); wG.push([g.filter(on).length, g.length]);
    g1.push(l[1] ? (l[0] === l[1] ? 'kept' : 'broken') : 'kept');
    g2.push(a[1] ? (a[0] === a[1] ? 'kept' : 'broken') : 'kept');
  });
  const nn = P.groups[0].rules;
  const r1 = nn.find((r) => r.n === 1), r2 = nn.find((r) => r.n === 2);
  r1.rows[0].cells = g1;
  r1.rows.splice(1, 0, rate('Lay-back tee shots in the fairway', lay));
  r2.rows = [{ kind: 'state', label: 'The grade', cells: g2 },
    rate('Wedge shots on the green', wAll), rate('Full wedges (40 yd+)', wFull), rate('Chips, pitches and bunker shots', wG)];
  // STRICT, LITERAL (owner 2026-11-09): only each rule's own measure; a stand-in row comes out; what the file cannot measure says so
  const NA = (label, why) => ({ kind: 'na', label, why });
  r1.rows = r1.rows.filter((row) => !/^Greens from the (fairway|rough)$/.test(row.label));
  const r3 = nn.find((r) => r.n === 3); r3.rows = r3.rows.filter((row) => !/^Greens from 40/.test(row.label));
  const r4 = nn.find((r) => r.n === 4); r4.rows = [r4.rows[0].kind === 'state' ? NA('Carries and lay-backs by 15 yards', 'not measured \u00b7 no hazard lines in the files') : r4.rows[0]];
  const r5 = nn.find((r) => r.n === 5); r5.rows = r5.rows.filter((row) => !/after six/.test(row.label));
  const ranked = P.groups[1].rules;
  const h3 = ranked.find((r) => /^3 /.test(r.name)); if (h3) h3.rows = h3.rows.filter((row) => !/^Three-putts/.test(row.label));
  const h7 = ranked.find((r) => /^7 /.test(r.name)); if (h7) h7.rows = [NA('The one band to work on', 'not measured \u00b7 a practice rule')];
  const h4 = ranked.find((r) => /^4 /.test(r.name));
  if (h4) { // "From 24 feet and out": first putts of 24 ft or more, left within a tenth (or holed)
    const per = rounds.map((r) => { let x = [0, 0]; r.holes.forEach((h) => { const p = h.shots.filter((y) => y.isPutt); if (!p.length) return; const f = p[0];
      if (f.startFt == null || f.startFt < 24) return; x[1]++; const nx = h.shots[h.shots.indexOf(f) + 1]; const ft = nx ? (nx.startFt != null ? nx.startFt : (nx.startYd != null ? nx.startYd * 3 : null)) : 0;
      if (f.holed || (ft != null && ft <= 0.1 * f.startFt)) x[0]++; }); return x; });
    h4.rows = [rate('First putts from 24 ft and out, left within 10%', per)];
  }
  P.groups.forEach((gr) => gr.rules.forEach((r) => r.rows.forEach((row) => {
    if (row.label === 'A driver or fairway wood from a bad lie') row.label = 'Bad lies played with a driver or wood';
    if (/^Birdie or better ÷ greens hit$/.test(row.label)) row.label = 'Birdie or better, of greens hit';
  })));
  // the tallies the read uses, re-counted from the literal grades
  const gi = (n) => P.graded.find((g) => g.n === n);
  [[1, g1], [2, g2]].forEach(([n, g]) => { const x = gi(n); x.graded = g.length; x.kept = g.filter((s) => s === 'kept').length; x.flagged = g.map((s, i) => (s === 'kept' ? null : 'R' + rounds[i].n)).filter(Boolean); });
  const sum = (arr) => arr.reduce((t, x) => [t[0] + x[0], t[1] + x[1]], [0, 0]);
  const L = sum(lay), WA = sum(wAll);
  const next = P.graded.filter((g) => g.n >= 3 && g.n <= 4 && g.flagged.length).sort((a, b) => b.flagged.length - a.flagged.length || a.n - b.n)[0];
  const nr = next ? HR.NON_NEGOTIABLES.find((x) => x.name === next.name) : null;
  P.read = { headline: 'Lay-backs ' + L[0] + ' of ' + L[1] + ' in the fairway; wedge shots ' + WA[0] + ' of ' + WA[1] + ' on the green (clubs read from the bag).',
    next: next ? { n: next.n, name: next.name, rounds: next.flagged } : null, decision: nr ? nr.plain.says : null };
  return { lay: L, wedges: WA, full: sum(wFull), green: sum(wG), g1, g2 };
}
module.exports = { fix };
