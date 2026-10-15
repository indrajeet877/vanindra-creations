// One Dot presentation renders: reel_tag | header | sizes | zoom
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const D = __dirname;
const uri = (f) => 'data:image/svg+xml;base64,' + Buffer.from(fs.readFileSync(path.join(D, f), 'utf8')).toString('base64');
const img = (f) => 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64');
const FONT = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/fonts/manrope/manrope-latin-500-normal.woff2';
const fontcss = `@font-face{font-family:UI;src:url(data:font/woff2;base64,${fs.readFileSync(FONT).toString('base64')}) format('woff2');font-weight:500}`;
const IV = '#F6F1E7', EM = '#0B2A20';

async function shot(html, out, w, h, scale = 1) {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  await p.setContent(`<!doctype html><html><head><style>${fontcss}*{box-sizing:border-box}body{margin:0}</style></head><body>${html}</body></html>`, { waitUntil: 'load' });
  await p.screenshot({ path: path.join(D, out), fullPage: false });
  await b.close();
}

(async () => {
  const mode = process.argv[2];
  if (mode === 'reel_tag') {
    const photo = process.argv[3] || '/home/user/vanindra-creations/assets/portfolio/reel_DZSZW2ey529.jpg';
    // 540x960 cover; the credit sits top-left inside the 3:4 grid-safe zone (120 px in from top/bottom)
    const html = `<div style="position:relative;width:540px;height:960px;overflow:hidden;background:#000">
      <img src="${img(photo)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
      <div style="position:absolute;left:0;top:136px;background:${EM};padding:12px 16px 12px 20px;display:flex;align-items:center">
        <img src="${uri('parts/edit_by_ivory.svg')}" style="height:21px;display:block">
      </div>
    </div>`;
    await shot(html, 'reel_tag.png', 540, 960);
  } else if (mode === 'header') {
    const nav = (c, gap, size) => ['Work', 'Services', 'Pricing', 'About'].map((t) => `<span style="font:500 ${size}px UI;color:${c};letter-spacing:.01em">${t}</span>`).join(`<span style="width:${gap}px;display:inline-block"></span>`);
    const html = `<div style="width:1440px;background:#cfcfcf;padding:0 0 40px 0">
      <div style="width:1440px;height:120px;background:${IV};display:flex;align-items:center;justify-content:space-between;padding:0 64px;border-bottom:1px solid #e4dccb">
        <img src="${uri('parts/wordmark_emerald.svg')}" style="height:46px;display:block">
        <div style="display:flex;align-items:center">${nav(EM, 36, 16)}<span style="width:40px;display:inline-block"></span>
          <span style="font:500 15px UI;color:${IV};background:${EM};padding:13px 22px;border-radius:999px">Book a discovery call</span></div>
      </div>
      <div style="display:flex;gap:40px;padding:40px 64px 0 64px;align-items:flex-start">
        <div style="width:390px;height:64px;background:${IV};display:flex;align-items:center;justify-content:space-between;padding:0 20px;border:1px solid #e4dccb">
          <img src="${uri('parts/wordmark_emerald.svg')}" style="height:28px;display:block">
          <div style="width:22px;height:14px;display:flex;flex-direction:column;justify-content:space-between"><i style="display:block;height:2px;background:${EM}"></i><i style="display:block;height:2px;background:${EM}"></i></div>
        </div>
        <div style="font:500 13px UI;color:#444;line-height:1.6;padding-top:6px">Top: 1440 × 120 desktop header (wordmark at 46 px, x-height ≈ 25 px).<br>Left: 390 × 64 phone header (wordmark at 28 px, x-height ≈ 15 px).<br>Recommended header lockup: the wordmark alone; the full name sits in the page title and footer.</div>
      </div>
    </div>`;
    await shot(html, 'header.png', 1440, 304);
  } else if (mode === 'sizes') {
    const row = (bg, f) => `<div style="display:flex;gap:24px;align-items:flex-end;padding:20px;background:${bg}">` +
      [16, 24, 32, 48, 64, 128].map((s) => `<img src="${uri(f)}" width="${s}" height="${s}">`).join('') + '</div>';
    await shot(`<div style="width:520px">${row(IV, 'mark_small.svg')}${row(EM, 'parts/mark_small_ivory.svg')}</div>`, 'sizes.png', 520, 336);
  } else if (mode === 'zoom') {
    // render the small mark at true 16/24/32/48 px on both grounds, then let CSS upscale x8 with pixelation
    const b = await chromium.launch();
    const p = await b.newPage({ viewport: { width: 200, height: 60 }, deviceScaleFactor: 1 });
    const outs = [];
    for (const [bg, f, tag] of [[IV, 'mark_small.svg', 'iv'], [EM, 'parts/mark_small_ivory.svg', 'em']]) {
      for (const s of [16, 24, 32, 48]) {
        await p.setViewportSize({ width: s, height: s });
        await p.setContent(`<body style="margin:0;background:${bg}"><img src="${uri(f)}" width="${s}" height="${s}" style="display:block"></body>`);
        const o = path.join(D, `work/z_${tag}_${s}.png`);
        await p.screenshot({ path: o });
        outs.push([o, s]);
      }
    }
    await b.close();
    const html = `<div style="background:#888;padding:16px;display:flex;flex-wrap:wrap;gap:16px;width:1180px">` +
      outs.map(([o, s]) => `<img src="data:image/png;base64,${fs.readFileSync(o).toString('base64')}" style="width:${s * 6}px;height:${s * 6}px;image-rendering:pixelated">`).join('') + '</div>';
    await shot(html, 'work/zoom.png', 1212, 720);
  }
})();
