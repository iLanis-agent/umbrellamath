const E = require('./engine.js');
const cases = require('./expected.json');
const fns = { coverPlan: E.coverPlan, dryPlan: E.dryPlan, yearPlan: E.yearPlan };
const renders = {
  coverPlan: (r, a) => E.renderCover(r, a[0]),
  dryPlan: (r, a) => E.renderDry(r, a[2]),
  yearPlan: (r, a) => E.renderYear(r, a[0])
};
let checks = 0, failed = 0;
for (const c of cases) {
  const got = fns[c.fn](...c.args);
  for (const k of Object.keys(c.result)) {
    checks++;
    if (got[k] !== c.result[k]) { failed++; console.log('FAIL', c.fn, c.args, k, 'expected', c.result[k], 'got', got[k]); }
  }
  if (c.render !== undefined) {
    checks++;
    const g = renders[c.fn](got, c.args);
    if (g !== c.render) { failed++; console.log('FAIL render', c.fn, c.args, '\n exp:', c.render, '\n got:', g); }
  }
}
console.log(cases.length + ' cases, ' + checks + ' checks ' + (failed ? failed + ' FAILED' : 'green'));
process.exit(failed ? 1 : 0);
