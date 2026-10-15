const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const serve = require('./serve');
(async () => {
  const sv = await serve(); const res = {};
  for (const [name, opts] of [['desktop', { viewport: { width: 1440, height: 900 } }], ['mobile', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }]]) {
    const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
    const ctx = await b.newContext(opts); await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
    const p = await ctx.newPage(); if (process.argv[2] === 'force') await p.addInitScript(() => { window.__fxForceGL = true; }); await p.goto(sv.url, { waitUntil: 'load' }); await p.waitForTimeout(1500);
    const check = () => p.evaluate(() => {
      const bad = []; const vh = innerHeight;
      document.querySelectorAll('main *, footer *').forEach((e) => { const r = e.getBoundingClientRect(); if (r.bottom < 0 || r.top > vh || !r.width) return; if (e.closest('[hidden],.player,.nav-sheet,#ztOutputPanel,[aria-hidden=true]')) return; let op = 1, n = e; while (n && n !== document.body) { op *= parseFloat(getComputedStyle(n).opacity); n = n.parentElement; } if (op < 0.95 && (e.innerText || '').trim()) bad.push(e.tagName + '.' + String(e.className).slice(0, 30) + ' op=' + op.toFixed(2)); });
      return { y: Math.round(scrollY), hiddenInView: bad.length, sample: bad.slice(0, 5), stats: [...document.querySelectorAll('.stat b')].map((x) => x.textContent).join(' '), splitLeft: document.querySelectorAll('.fxw').length };
    });
    res[name] = [];
    for (const target of ['bottom', 'top', 'mid', 'top']) {
      await p.evaluate((t) => { const H = document.documentElement.scrollHeight; window.scrollTo({ top: t === 'bottom' ? H : t === 'mid' ? H * 0.45 : 0, behavior: 'instant' }); }, target);
      await p.waitForTimeout(1600); res[name].push(Object.assign({ target }, await check()));
    }
    await b.close();
  }
  console.log(JSON.stringify(res, null, 1)); sv.close();
})();
