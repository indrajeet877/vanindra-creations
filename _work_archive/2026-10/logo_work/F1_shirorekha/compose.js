// Composite two renders: rows above `split` from A, rows below from B. Usage: node compose.js A.png B.png split out.png
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [a, b, split, out] = process.argv.slice(2);
  const ua = 'data:image/png;base64,' + fs.readFileSync(a).toString('base64');
  const ub = 'data:image/png;base64,' + fs.readFileSync(b).toString('base64');
  const br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 400, height: 300 }, deviceScaleFactor: 1 });
  await p.setContent(`<!doctype html><body style="margin:0"><div id=w style="position:relative;display:inline-block">
    <img id=b src="${ub}" style="display:block"><img src="${ua}" style="position:absolute;left:0;top:0;clip-path:inset(0 0 calc(100% - ${split}px) 0)"></div></body>`, { waitUntil: 'load' });
  const el = await p.$('#w');
  await el.screenshot({ path: out });
  await br.close();
})();
