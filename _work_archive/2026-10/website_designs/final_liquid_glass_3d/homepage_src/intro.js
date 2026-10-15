const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const serve = require('./serve'); const Q = __dirname + '/../qa/';
(async () => {
  const sv = await serve();
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
  const p = await ctx.newPage();
  await p.goto(sv.url, { waitUntil: 'commit' });
  const out = [];
  for (let i = 0; i < 9; i++) { const t = await p.evaluate(() => Math.round(performance.now())).catch(() => -1); const f = Q + 'introT_' + i + '.png'; await p.screenshot({ path: f }); out.push(t); await p.waitForTimeout(120); }
  console.log(out.join(' '));
  await b.close(); sv.close();
})();
