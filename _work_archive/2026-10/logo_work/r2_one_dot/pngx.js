// render an SVG to PNG at an exact width, page sized to the SVG's aspect (no grey padding)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [f, out, w] = process.argv.slice(2);
  const s = fs.readFileSync(f, 'utf8');
  const m = s.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  const W = parseInt(w, 10), H = Math.round(W * parseFloat(m[2]) / parseFloat(m[1]));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  await p.setContent(`<body style="margin:0"><img style="display:block;width:${W}px;height:${H}px" src="data:image/svg+xml;base64,${Buffer.from(s).toString('base64')}"></body>`);
  await p.screenshot({ path: out });
  await b.close();
})();
