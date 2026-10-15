// Render SVG logos to PNG for visual review.
// Usage:
//   node render.js png <file.svg> <out.png> [widthPx]            -> one PNG at width (default 1024)
//   node render.js sheet <out.png> <a.svg> <b.svg> ...            -> contact sheet, each on its own ground
//   node render.js sizes <out.png> <icon.svg>                      -> the icon at 16/24/32/48/64/128 px on ivory + emerald
//   node render.js context <out.png> <icon.svg> <horizontal.svg>  -> icon as Instagram DP (circle crop), browser tab, website header bar
// Each SVG should carry its own background rect when the ground matters.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const IVORY = '#F6F1E7', EMERALD = '#0B2A20';
const read = (f) => fs.readFileSync(f, 'utf8');
const uri = (f) => 'data:image/svg+xml;base64,' + Buffer.from(read(f)).toString('base64');

async function shot(html, out, width) {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width, height: 400 }, deviceScaleFactor: 1 });
  await p.setContent(`<!doctype html><html><body style="margin:0;background:#8f8f8f">${html}</body></html>`, { waitUntil: 'load' });
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
}

(async () => {
  const [mode, ...a] = process.argv.slice(2);
  if (mode === 'png') {
    const [file, out, w] = a;
    const width = parseInt(w || '1024', 10);
    await shot(`<img src="${uri(file)}" style="width:${width}px;display:block">`, out, width);
  } else if (mode === 'sheet') {
    const [out, ...files] = a;
    const cells = files.map((f) => `<figure style="margin:0"><img src="${uri(f)}" style="width:100%;display:block;background:#fff"><figcaption style="font:12px sans-serif;padding:4px 0;color:#111">${path.basename(f)}</figcaption></figure>`).join('');
    await shot(`<div style="display:grid;grid-template-columns:repeat(${Math.min(3, files.length)},1fr);gap:12px;padding:12px">${cells}</div>`, out, 1500);
  } else if (mode === 'sizes') {
    const [out, icon] = a;
    const row = (bg) => `<div style="display:flex;gap:24px;align-items:flex-end;padding:20px;background:${bg}">` +
      [16, 24, 32, 48, 64, 128].map((s) => `<img src="${uri(icon)}" width="${s}" height="${s}">`).join('') + '</div>';
    await shot(row(IVORY) + row(EMERALD), out, 520);
  } else if (mode === 'context') {
    const [out, icon, horiz] = a;
    const html = `<div style="padding:20px;display:grid;gap:20px;font:14px sans-serif">
      <div style="display:flex;gap:20px;align-items:center;background:#fff;padding:16px;border-radius:8px">
        <div style="width:150px;height:150px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #fff,0 0 0 5px #d62976"><img src="${uri(icon)}" style="width:100%;height:100%"></div>
        <div style="width:56px;height:56px;border-radius:50%;overflow:hidden"><img src="${uri(icon)}" style="width:100%;height:100%"></div>
        <div style="width:32px;height:32px;border-radius:50%;overflow:hidden"><img src="${uri(icon)}" style="width:100%;height:100%"></div>
        <div style="display:flex;align-items:center;gap:8px;background:#f1f3f4;padding:8px 12px;border-radius:8px 8px 0 0"><img src="${uri(icon)}" width="16" height="16"><span>VanIndra Creations</span></div>
      </div>
      <div style="background:${EMERALD};padding:14px 24px;display:flex;align-items:center;justify-content:space-between"><img src="${uri(horiz)}" style="height:52px"><span style="color:#F6F1E7;opacity:.6">Portfolio · Services · Packages</span></div>
      <div style="background:${IVORY};padding:14px 24px"><img src="${uri(horiz)}" style="height:52px"></div>
    </div>`;
    await shot(html, out, 1000);
  } else {
    console.error('modes: png | sheet | sizes | context');
    process.exit(1);
  }
})();
