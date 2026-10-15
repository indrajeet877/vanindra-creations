// Render an SVG contact sheet to PNG for visual QA. Usage: node sheet.js <dir> <out.png> [filter]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const dir = process.argv[2], out = process.argv[3], filt = process.argv[4] || '';
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg') && f.includes(filt)).sort();
  const cells = files.map(f => `<figure><div class="c">${fs.readFileSync(path.join(dir, f), 'utf8')}</div><figcaption>${f}</figcaption></figure>`).join('');
  const html = `<html><body style="margin:0;background:#9a9a9a;font:12px sans-serif"><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:10px">${cells}</div>
  <style>figure{margin:0}.c svg{width:100%;height:auto;display:block}figcaption{color:#111;padding:3px 0}</style></body></html>`;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1500, height: 900 } });
  await p.setContent(html); await p.screenshot({ path: out, fullPage: true }); await b.close();
})();
