const path = require('path');
const A = (f) => require(path.join('/home/user/rc-greenlight-rev362/automation', f));
const SC = A('shot-csv.js'), RB = A('raw-report-builder.js'), M = A('metrics.js'), NN = A('nn-grade.js'), HR = A('house-rules.js');
const o = require('./engine_out.json');
const res = {};
for (const n of [1, 2, 3, 4]) {
  const holes = SC.parse(o[n].csv).holes;
  const summary = M.summary(holes);
  const facets = RB.assembleFacets(holes, summary, {});
  const ladder = RB.ladderCounts(holes, 'yd');
  const nn = NN.grade(holes, { published: HR.NON_NEGOTIABLES, wedgeMaxYd: null });
  res[n] = { facets, ladder, nn, summary };
  console.log('==== R' + n);
  console.log('facets:', JSON.stringify(facets).slice(0, 3000));
  console.log('ladder:', JSON.stringify(ladder.map(r => r.label + ' ' + r.made + '/' + r.n)));
  console.log('nn:', JSON.stringify((nn.rules || []).map(r => ({ n: r.n, state: r.state, level: r.level, cause: r.cause, credit: r.credit, measuresGraded: r.measuresGraded, evidence: r.evidence || r.detail || r.note }))).slice(0, 2500));
}
require('fs').writeFileSync('raw_out.json', JSON.stringify(res, null, 1));
