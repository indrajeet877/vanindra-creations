// node pixzoom.js in.png out.png x y w h scale  -> nearest-neighbour zoom of a crop
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [inp, out, x, y, w, h, s] = process.argv.slice(2).map((v, i) => (i < 2 ? v : Number(v)));
  const u = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: w * s, height: h * s } });
  await p.setContent(`<body style="margin:0"><canvas id=c width=${w * s} height=${h * s}></canvas><script>
    const im = new Image(); im.onload = () => { const c = document.getElementById('c').getContext('2d'); c.imageSmoothingEnabled = false;
      c.drawImage(im, ${x}, ${y}, ${w}, ${h}, 0, 0, ${w * s}, ${h * s}); document.title = 'done'; }; im.src = '${u}';</script></body>`);
  await p.waitForFunction(() => document.title === 'done');
  await p.screenshot({ path: out });
  await b.close();
})();
