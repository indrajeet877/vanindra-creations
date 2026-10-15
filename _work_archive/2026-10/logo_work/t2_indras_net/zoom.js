// Pixel-zoom helper (my own, not part of the toolkit): renders an SVG at small sizes, then shows them upscaled
// with nearest-neighbour so individual pixels can be inspected.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [svg, out, bg] = process.argv.slice(2);
  const uri = 'data:image/svg+xml;base64,' + Buffer.from(fs.readFileSync(svg, 'utf8')).toString('base64');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 400, height: 100 }, deviceScaleFactor: 1 });
  const sizes = [16, 24, 32, 48];
  await p.setContent(`<body style="margin:0;background:${bg}">` + sizes.map(s => `<img src="${uri}" width="${s}" height="${s}" style="margin:4px">`).join('') + '</body>');
  const shots = [];
  for (let i = 0; i < sizes.length; i++) {
    const el = (await p.$$('img'))[i];
    shots.push((await el.screenshot()).toString('base64'));
  }
  const q = await b.newPage({ viewport: { width: 1200, height: 420 }, deviceScaleFactor: 1 });
  await q.setContent(`<body style="margin:0;background:#888;display:flex;gap:16px;align-items:flex-end;padding:10px">` +
    shots.map((s, i) => `<img src="data:image/png;base64,${s}" style="image-rendering:pixelated;width:${sizes[i] * 8}px;height:${sizes[i] * 8}px">`).join('') + '</body>');
  await q.screenshot({ path: out, fullPage: true });
  await b.close();
})();
