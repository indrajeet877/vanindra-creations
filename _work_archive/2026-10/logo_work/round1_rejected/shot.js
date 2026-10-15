const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const html = require('fs').readFileSync(process.argv[2], 'utf8');
  const doc = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>${html}</body></html>`;
  for (const [n, vp, scheme] of [['desk', { width: 1280, height: 900 }, 'light'], ['mob', { width: 390, height: 844 }, 'dark']]) {
    const p = await b.newPage({ viewport: vp, colorScheme: scheme });
    await p.setContent(doc, { waitUntil: 'load' });
    await p.waitForTimeout(400);
    const ov = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
    console.log(n, 'scrollW/clientW', ov);
    await p.screenshot({ path: process.argv[3] + `_${n}.png`, fullPage: true });
  }
  await b.close();
})();
