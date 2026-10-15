// Stack several PNGs vertically into one image (my own helper for review sheets).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [out, ...files] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 100 }, deviceScaleFactor: 1 });
  await p.setContent('<body style="margin:0;background:#777">' + files.map(f => `<div style="font:13px sans-serif;color:#fff;padding:2px 8px">${f}</div><img style="display:block" src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}">`).join('') + '</body>');
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
