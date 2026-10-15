// Screenshot a page directory for design review.
// Usage: node shoot.js <dir-with-index.html> <outPrefix>
// Produces: <outPrefix>_desktop_fold.png (1440x900), <outPrefix>_desktop_full.png (1440 wide, full page, scaled),
//           <outPrefix>_mobile_fold.png (390x844), <outPrefix>_mobile_full.png, and prints overflow + console errors.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const dir = path.resolve(process.argv[2]); const out = process.argv[3];
const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.js': 'text/javascript', '.css': 'text/css' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(dir, p);
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end('nf'); } res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
}).listen(0, async () => {
  const port = server.address().port; const url = `http://127.0.0.1:${port}/index.html`;
  const b = await chromium.launch(); const errors = [];
  for (const [name, vp] of [['desktop', { width: 1440, height: 900 }], ['mobile', { width: 390, height: 844 }]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    p.on('pageerror', (e) => errors.push(`${name} pageerror: ${e.message}`));
    p.on('console', (m) => { if (m.type() === 'error' && !/fonts|googleapis|gstatic|instagram|pollinations|ERR_|net::/i.test(m.text())) errors.push(`${name} console: ${m.text().slice(0, 160)}`); });
    await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 60)); } window.scrollTo({ top: 0, behavior: 'instant' }); });
    await p.waitForTimeout(800);
    await p.screenshot({ path: `${out}_${name}_fold.png` });
    await p.screenshot({ path: `${out}_${name}_full.png`, fullPage: true });
    const ov = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth, document.body.scrollHeight]);
    console.log(`${name}: scrollWidth=${ov[0]} clientWidth=${ov[1]} pageHeight=${ov[2]}${ov[0] > ov[1] ? '  <-- HORIZONTAL OVERFLOW' : ''}`);
    await ctx.close();
  }
  console.log(errors.length ? errors.join('\n') : 'no page errors');
  await b.close(); server.close();
});
