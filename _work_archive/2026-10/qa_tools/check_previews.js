const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const root = '/home/user/vanindra-creations';
const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml' };
const missing = [];
const server = http.createServer((req, res) => { const p = decodeURIComponent(req.url.split('?')[0]); const f = path.join(root, p);
  fs.readFile(f, (e, d) => { if (e) { missing.push(p); res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(d); }); }).listen(0, async () => {
  const port = server.address().port; const b = await chromium.launch();
  for (const v of ['v1_crystal', 'v2_prism', 'v3_vision', 'v4_focus']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
    const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(e.message));
    await p.goto(`http://127.0.0.1:${port}/previews/website_2026-10-15/${v}.html`, { waitUntil: 'load' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } });
    await p.waitForTimeout(500);
    const r = await p.evaluate(() => ({ broken: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')), imgs: document.images.length, login: [...document.querySelectorAll('a[href*="login.html"]')].map(a => a.href).slice(0, 1) }));
    console.log(v, JSON.stringify(r), errs.length ? 'ERR ' + errs.join('|') : 'no errors');
    await ctx.close();
  }
  console.log('missing:', [...new Set(missing)].join(', ') || 'none');
  await b.close(); server.close();
});
