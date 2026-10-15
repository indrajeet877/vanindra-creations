// node pixzoom.js out.png a.svg b.svg ... : renders each at 16/24/32/48 px (ivory ground, emerald ink) and on emerald (ivory ink),
// then shows them x6 nearest-neighbour so real pixels can be inspected.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const [out, ...files] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 1 });
  const sizes = [16, 24, 32, 48];
  let rows = '';
  for (const f of files) {
    let svg = fs.readFileSync(f, 'utf8');
    const inv = svg.replace(/#0B2A20/g, '#F6F1E7');
    let cells = '';
    for (const [s, bg] of [[svg, '#F6F1E7'], [inv, '#0B2A20']]) {
      for (const px of sizes) {
        const html = `<body style="margin:0;background:${bg}"><img src="data:image/svg+xml;base64,${Buffer.from(s).toString('base64')}" width="${px}" height="${px}" style="display:block"></body>`;
        await p.setViewportSize({ width: px, height: px });
        await p.setContent(html);
        const buf = await p.screenshot({ clip: { x: 0, y: 0, width: px, height: px } });
        cells += `<img src="data:image/png;base64,${buf.toString('base64')}" style="width:${px * 6}px;height:${px * 6}px;image-rendering:pixelated;margin:6px;vertical-align:bottom">`;
      }
    }
    rows += `<div style="display:flex;align-items:flex-end;gap:4px;padding:6px;font:14px sans-serif"><span style="width:40px">${path.basename(f, '.svg')}</span>${cells}</div>`;
  }
  await p.setViewportSize({ width: 2000, height: 400 });
  await p.setContent(`<body style="margin:0;background:#999">${rows}</body>`);
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
