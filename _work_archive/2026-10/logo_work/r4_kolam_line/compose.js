// Compose context.png (correct ink per ground), header.png, reel_tag.png, and size-rule strip.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const IV = '#F6F1E7', EM = '#0B2A20';
const uri = (f) => 'data:image/svg+xml;base64,' + Buffer.from(fs.readFileSync(f, 'utf8')).toString('base64');
const img = (f) => 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64');
const FONT = '/tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad/logo2/fonts/manrope/';
const ff = (w) => `@font-face{font-family:Manrope;font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(FONT + `manrope-latin-${w}-normal.woff2`).toString('base64')}) format('woff2')}`;
async function shot(html, out, w, h, full = true) {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await p.setContent(`<!doctype html><html><head><style>${ff(400)}${ff(500)}${ff(600)} body{margin:0}</style></head><body>${html}</body></html>`, { waitUntil: 'load' });
  await p.waitForTimeout(150);
  await p.screenshot({ path: out, fullPage: full });
  await b.close();
}
(async () => {
  const mode = process.argv[2];
  if (mode === 'context') {
    const html = `<div style="background:#8f8f8f;padding:20px;display:grid;gap:20px;font:14px sans-serif;width:960px">
      <div style="display:flex;gap:20px;align-items:center;background:#fff;padding:16px;border-radius:8px">
        <div style="width:150px;height:150px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #fff,0 0 0 5px #d62976"><img src="${uri('avatar_on_emerald.svg')}" style="width:100%;height:100%"></div>
        <div style="width:110px;height:110px;border-radius:50%;overflow:hidden"><img src="${uri('avatar_on_emerald.svg')}" style="width:100%;height:100%"></div>
        <div style="width:56px;height:56px;border-radius:50%;overflow:hidden"><img src="${uri('avatar_on_emerald.svg')}" style="width:100%;height:100%"></div>
        <div style="width:32px;height:32px;border-radius:50%;overflow:hidden"><img src="${uri('avatar_small_on_emerald.svg')}" style="width:100%;height:100%"></div>
        <div style="display:flex;align-items:center;gap:8px;background:#f1f3f4;padding:8px 12px;border-radius:8px 8px 0 0"><img src="${uri('favicon.svg')}" width="16" height="16"><span>VanIndra Creations</span></div>
      </div>
      <div style="background:${EM};padding:14px 24px;display:flex;align-items:center;justify-content:space-between"><img src="${uri('lockup_horizontal_ivory_ink.svg')}" style="height:52px"><span style="color:#F6F1E7;opacity:.6">Portfolio · Services · Packages</span></div>
      <div style="background:${IV};padding:14px 24px"><img src="${uri('lockup_horizontal_emerald_ink.svg')}" style="height:52px"></div>
    </div>`;
    await shot(html, 'context.png', 1000, 400);
  } else if (mode === 'header') {
    const nav = (c) => ['Work', 'Services', 'Packages', 'About'].map((t) => `<span style="font:500 15px Manrope;color:${c};letter-spacing:.01em">${t}</span>`).join('');
    const desk = `<div style="width:1440px;height:120px;background:${IV};display:flex;align-items:center;justify-content:space-between;padding:0 64px;box-sizing:border-box;border-bottom:1px solid #e6dfd0">
        <img src="${uri('lockup_horizontal_emerald_ink.svg')}" style="height:44px;display:block">
        <div style="display:flex;align-items:center;gap:36px">${nav(EM)}<span style="font:600 14px Manrope;color:${IV};background:${EM};padding:12px 22px;border-radius:999px">Book a discovery call</span></div></div>`;
    const phone = (scale) => `<div style="width:390px;height:64px;background:${IV};display:flex;align-items:center;justify-content:space-between;padding:0 20px;box-sizing:border-box;border-bottom:1px solid #e6dfd0;transform:scale(${scale});transform-origin:0 0">
        <img src="${uri('lockup_compact_emerald_ink.svg')}" style="height:30px;display:block">
        <svg width="22" height="14" viewBox="0 0 22 14"><rect y="1" width="22" height="1.6" fill="${EM}"/><rect y="11.4" width="22" height="1.6" fill="${EM}"/></svg></div>`;
    const html = `<div style="width:1440px;background:#cfcac0">${desk}
      <div style="display:flex;gap:60px;align-items:flex-start;padding:40px 64px 48px">
        <div><div style="font:500 12px Manrope;color:#444;margin-bottom:8px">Phone header, 390 x 64 (actual size)</div><div style="width:390px;height:64px;box-shadow:0 1px 6px rgba(0,0,0,.15)">${phone(1)}</div></div>
        <div><div style="font:500 12px Manrope;color:#444;margin-bottom:8px">Same phone header at 2x for inspection</div><div style="width:780px;height:128px;box-shadow:0 1px 6px rgba(0,0,0,.15)">${phone(2)}</div></div>
      </div></div>`;
    await shot(html, 'header.png', 1440, 300);
  } else if (mode === 'reel') {
    const html = `<div style="width:540px;height:960px;position:relative;background:url(${img('reel/beach_540.jpg')}) center/cover">
      <img src="${uri('tag_edit_by_emerald.svg')}" style="position:absolute;right:28px;top:778px;height:37px">
    </div>`;
    await shot(html, 'reel_tag.png', 540, 960, false);
  } else if (mode === 'global') {
    const html = `<div style="width:1200px;padding:0;background:#fff"><img src="${uri('global.svg')}" style="width:1200px;display:block"></div>`;
    await shot(html, 'global.png', 1200, 200);
  }
})();
