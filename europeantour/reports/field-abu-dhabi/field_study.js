/* Abu Dhabi field vs the house rules (v18.1, Rev 362), every player who finished, every round.
 * The house engine grades each round: dpworld-adapter.readCsv against the official card, metrics.js, nn-grade.js.
 * The measures follow the RC Greenlight tour shot study (tour-benchmarks.js STUDY), so each line can sit beside it.
 * usage: node field_study.js <field csv> <official.json> <engine dir> <out dir> */
'use strict';
const fs = require('fs'), path = require('path');
const [CSV, OFFICIAL, ENGINE, OUT] = process.argv.slice(2);
const A = (f) => require(path.join(ENGINE, f));
const DPW = A('dpworld-adapter.js'), SC = A('shot-csv.js'), M = A('metrics.js'), NN = A('nn-grade.js'), HR = A('house-rules.js'), TB = A('tour-benchmarks.js');
const DPW_P = require('./dpworld-adapter.patched.js');
const RB = A('raw-report-builder.js');
const off = JSON.parse(fs.readFileSync(OFFICIAL, 'utf8'));
const text = fs.readFileSync(CSV, 'utf8');

const isGreen = (l) => /^green$/i.test(String(l || ''));
const isFairway = (l) => /^fairway$/i.test(String(l || ''));
const isRough = (l) => /rough/i.test(String(l || ''));
const leaveOf = (h, i) => { const nx = h.shots[i + 1]; if (!nx) return { ft: 0, yd: 0, holed: true }; return { ft: nx.startFt != null ? nx.startFt : (nx.startYd != null ? nx.startYd * 3 : null), yd: nx.startYd != null ? nx.startYd : (nx.startFt != null ? nx.startFt / 3 : null), lie: nx.startLie, holed: false }; };

// every player id in the sheet, with the name it carries
const rows = text.split('\n'); const head = rows[0].replace(/^﻿/, '').split(',');
const ci = (c) => head.indexOf(c);
const people = {};
const csvSplit = (line) => { const out = []; let cur = '', q = false; for (const ch of line) { if (ch === '"') q = !q; else if (ch === ',' && !q) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; };
rows.slice(1).forEach((l) => { if (!l.trim()) return; const c = csvSplit(l); people[c[ci('playerId')]] = c[ci('player')]; });

const results = [], refused = [];
for (const [pid, name] of Object.entries(people)) {
  const card = off.players[pid];
  if (!card) { refused.push({ pid, name, why: 'no official card' }); continue; }
  for (const rnd of ['1', '2', '3', '4']) {
    const cardScores = card.cards[rnd] || {};
    if (Object.keys(cardScores).length !== 18) { refused.push({ pid, name, rnd, why: 'card not complete' }); continue; }
    if (!off.holestats[rnd] || !off.tee[rnd] || Object.keys(off.holestats[rnd]).length < 18) { refused.push({ pid, name, rnd, why: 'round not captured' }); continue; }
    const cardPar = {}, holeLengths = {};
    for (let h = 1; h <= 18; h++) { cardPar[h] = off.holestats[rnd][h].par; holeLengths[h] = off.tee[rnd][h]; }
    const opts = { player: name, playerId: pid, round: rnd, cardPar, cardScores, holeLengths, holeLengthUnits: 'm' };
    let r, patched = false;
    try { r = DPW.readCsv(text, opts); }
    catch (e) {
      try { r = DPW_P.readCsv(text, opts); patched = (e.problems || [e.message]).join('; '); }
      catch (e2) { refused.push({ pid, name, rnd, why: (e2.problems || [e2.message]).join('; ') }); continue; }
    }
    const holes = SC.parse(r.csv).holes;
    const s = M.summary(holes);
    const nn = NN.grade(holes, { published: HR.NON_NEGOTIABLES, wedgeMaxYd: null });
    const rule = (n) => (nn.rules || []).find((x) => x.n === n) || {};
    const order = (card.order && card.order[rnd]) || Array.from({ length: 18 }, (_, i) => i + 1);
    const byNo = {}; holes.forEach((h) => { byNo[h.hole] = h; });

    const m = { pid, name, round: +rnd, score: s.card.strokes, toPar: s.card.toPar, patched,
      gir: s.gir.made, fw: s.fairways.made, fwAtt: s.fairways.att, putts: s.putts.value,
      birdies: s.counts.birdies + s.counts.eagles, bogeys: s.counts.bogeys, doubles: s.counts.doubles,
      bc: [s.birdieConversion.made, s.birdieConversion.att],
      cfbs: [s.clutchFactorBallStriking.made, s.clutchFactorBallStriking.att], cfbsDoubles: (s.clutchFactorBallStriking.holes || []).filter((x) => x.toPar >= 2).length,
      cfp: [s.clutchFactorPutting.made, s.clutchFactorPutting.att],
      cfr: [s.clutchFactorResponse.stopped, s.clutchFactorResponse.answered, s.clutchFactorResponse.att],
      cfdc: [s.clutchFactorDamageControl.made, s.clutchFactorDamageControl.att],
      level: rule(5).level, rules: (nn.rules || []).map((x) => ({ n: x.n, state: x.state, level: x.level || null, evidence: x.evidence || [] })),
      in6: [0, 0], in36: [0, 0], par5: [0, 0], p40: [0, 0], app40: [0, 0], lv24: [0, 0], three25: [0, 0],
      sg6: [0, 0], bunker6: [0, 0], chipMissRound: 0, chips: [0, 0], dz: 0, dzFaced: [], penHoles: 0,
      gFw: [0, 0], gRough: [0, 0], p5third121: [], p5third40: [], resetBad: [0, 0], first6: null };
    for (const h of holes) {
      const shots = h.shots;
      // putting
      const putts = shots.filter((x) => x.isPutt);
      putts.forEach((x) => { if (x.startFt != null && x.startFt <= 6) { m.in6[1]++; if (x.holed) m.in6[0]++; } if (x.startFt != null && x.startFt >= 3 && x.startFt <= 6) { m.in36[1]++; if (x.holed) m.in36[0]++; } });
      if (putts.length) {
        const f = putts[0];
        if (f.startFt >= 40) { m.p40[1]++; if (putts.length >= 3) m.p40[0]++; }
        if (f.startFt <= 25) { m.three25[1]++; if (putts.length >= 3) m.three25[0]++; }
        if (f.startFt > 24) { m.lv24[1]++; const i = shots.indexOf(f), lv = leaveOf(h, i); if (f.holed || (lv.ft != null && lv.ft <= 0.1 * f.startFt)) m.lv24[0]++; }
      }
      // par 5 on in three or fewer
      if (+h.par === 5) { m.par5[1]++; const k = shots.findIndex((x) => isGreen(x.endLie) || x.holed); if (k >= 0 && k + 1 <= 3) m.par5[0]++; }
      // regulation approach inside 40 ft (finishing on the green, or holed)
      const app = M.regulationApproach(h);
      if (app) { const i = shots.indexOf(app), lv = leaveOf(h, i); m.app40[1]++; if (app.holed || (isGreen(app.endLie) && lv.ft != null && lv.ft <= 40)) m.app40[0]++;
        const st = app.startLie; const hit = app.holed || isGreen(app.endLie);
        if (+h.par >= 4 && app.n >= 2) { if (isFairway(st)) { m.gFw[1]++; if (hit) m.gFw[0]++; } else if (isRough(st)) { m.gRough[1]++; if (hit) m.gRough[0]++; } } }
      // short game: strokes from inside 40 yd off the green (not putts, not tee shots)
      let chipMissed = false;
      shots.forEach((x, i) => {
        if (x.isPutt || x.n === 1 || x.penalty || x.startYd == null || x.startYd > 40) return;
        const lv = leaveOf(h, i), ok6 = x.holed || (isGreen(x.endLie) && lv.ft != null && lv.ft <= 6);
        m.sg6[1]++; if (ok6) m.sg6[0]++;
        if (/bunker/i.test(x.startLie)) { m.bunker6[1]++; if (ok6) m.bunker6[0]++; }
        m.chips[1]++; if (x.holed || isGreen(x.endLie)) m.chips[0]++; else chipMissed = true;
      });
      if (chipMissed) m.chipMissRound = 1;
      // dead zone: a stroke that finished 40–74 yd from the hole, off the green
      shots.forEach((x, i) => { if (x.isPutt || x.holed || x.penalty) return; const lv = leaveOf(h, i); if (lv.yd != null && !isGreen(lv.lie) && lv.yd >= 40 && lv.yd < 75) { m.dz++; m.dzFaced.push('H' + h.hole + ' ' + Math.round(lv.yd)); } });
      // par-5 third shots from 121+ and from inside 40 (lay-up results), scored
      if (+h.par === 5 && shots[2] && !shots[2].isPutt && !shots.slice(0, 2).some((x) => isGreen(x.endLie) || x.holed)) {
        const t = shots[2];
        if (t.startYd >= 121) m.p5third121.push({ lie: t.startLie, toPar: h.score - 5 });
        if (t.startYd < 40) m.p5third40.push({ lie: t.startLie, toPar: h.score - 5 });
      }
      if (shots.some((x) => x.penalty)) m.penHoles++;
    }
    // reset hole: after a bogey or worse, the next hole in playing order
    for (let i = 0; i < order.length - 1; i++) { const a = byNo[order[i]], b = byNo[order[i + 1]]; if (!a || !b) continue; if (a.score > a.par) { m.resetBad[1]++; if (b.score > b.par) m.resetBad[0]++; } }
    // over par after six holes (playing order)
    m.after6 = order.slice(0, 6).reduce((t, h) => t + (byNo[h] ? byNo[h].score - byNo[h].par : 0), 0);
    m.ladder = RB.ladderCounts(holes, 'yd').map((x) => [x.label, x.made, x.n]);
    results.push(m);
  }
}

// field scoring average per round (panel), for "beat the field" by stress level
const fieldRound = {}; for (const r of Object.keys(off.holestats)) fieldRound[r] = Object.values(off.holestats[r]).reduce((t, x) => t + x.par + x.avg, 0);
results.forEach((m) => { m.vsField = +(fieldRound[m.round] - m.score).toFixed(2); });

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, 'rounds.json'), JSON.stringify({ engine: { houseRules: HR.VERSION, study: TB.STUDY.source }, fieldRound, results, refused }, null, 1));
console.log('house rules', HR.VERSION, '| rounds graded', results.length, '| patched reads', results.filter((x) => x.patched).length, '| refused', refused.length);
refused.slice(0, 12).forEach((x) => console.log('  refused', x.name, 'R' + x.rnd, x.why));
