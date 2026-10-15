// Combine two render.js `sizes` outputs: the ivory row of the first (emerald small mark) and the emerald row of
// the second (ivory small mark), so one image shows the small master on both grounds. Own helper, toolkit untouched.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [out, a, b] = process.argv.slice(2);
  const src = (f) => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
  const br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 520, height: 336 }, deviceScaleFactor: 1 });
  await p.setContent(`<body style="margin:0">
    <div style="width:520px;height:168px;overflow:hidden"><img src="${src(a)}" style="display:block"></div>
    <div style="width:520px;height:168px;overflow:hidden"><img src="${src(b)}" style="display:block;margin-top:-168px"></div></body>`);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: 520, height: 336 } });
  await br.close();
})();
