// stack PNGs vertically with labels: node stack.js out.png a.png b.png ...
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [out, ...files] = process.argv.slice(2);
  const html = files.map(f => `<div style="font:12px sans-serif;margin:4px 0">${f}</div><img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}">`).join('');
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 600, height: 200 } });
  await p.setContent(`<body style="margin:8px;background:#ccc">${html}</body>`); await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
