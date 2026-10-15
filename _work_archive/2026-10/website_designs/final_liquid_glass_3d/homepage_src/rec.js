const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const serve = require('./serve'); const fs = require('fs');
const which = process.argv[2] || 'desktop';
(async () => {
  const sv = await serve();
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const D = which === 'desktop';
  const vp = D ? { width: 1440, height: 900 } : { width: 390, height: 844 };
  const ctx = await b.newContext(Object.assign({ viewport: vp, recordVideo: { dir: __dirname + '/vid_' + which, size: vp } }, D ? {} : { isMobile: true, hasTouch: true, deviceScaleFactor: 2 }));
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
  const p = await ctx.newPage();
  // this sandbox has no GPU: the capture forces the live WebGL glass (real visitors on software WebGL get the identical still)
  await p.addInitScript(() => { window.__fxForceGL = true; });
  const T = Date.now(); const log = (m) => console.log(((Date.now() - T) / 1000).toFixed(1) + 's ' + m);
  await p.goto(sv.url, { waitUntil: 'commit' });
  if (D) {
    await p.waitForTimeout(3200); log('entrance done');
    // glide over the hero glass
    await p.mouse.move(720, 700); 
    for (const [x, y] of [[520, 640], [470, 800], [640, 860], [880, 860], [1040, 780], [990, 620], [750, 600]]) await p.mouse.move(x, y, { steps: 5 });
    log('glass');
    const c = async (sel) => { const bb = await p.locator(sel).first().boundingBox(); return [bb.x + bb.width / 2, bb.y + bb.height / 2]; };
    let [x, y] = await c('.hero-head .btn-glass'); await p.mouse.move(x, y, { steps: 6 }); await p.waitForTimeout(900);
    [x, y] = await c('.hero-head .btn-primary'); await p.mouse.move(x + 20, y, { steps: 6 }); await p.waitForTimeout(1100);
    log('buttons');
    [x, y] = await c('#btnModeBefore'); await p.mouse.move(x, y, { steps: 5 }); await p.waitForTimeout(250); await p.mouse.click(x, y); await p.waitForTimeout(1300);
    [x, y] = await c('#btnModeAfter'); await p.mouse.move(x, y, { steps: 4 }); await p.waitForTimeout(250); await p.mouse.click(x, y); await p.waitForTimeout(1300);
    log('before/after');
    await p.mouse.move(720, 450, { steps: 4 });
    const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    const wheelTo = async (target, step) => { const sy = await p.evaluate(() => scrollY); const n = Math.ceil((target - sy) / step); for (let i = 0; i < n; i++) { await p.mouse.wheel(0, step); await p.waitForTimeout(40); } await p.waitForTimeout(600); };
    const reelsTop = await p.evaluate(() => document.querySelector('#reels').getBoundingClientRect().top + scrollY - 60);
    await wheelTo(reelsTop, 200); await p.waitForTimeout(900);
    log('reels');
    [x, y] = await c('.reel-row .reel:nth-child(3)'); await p.mouse.move(x - 160, y, { steps: 4 }); await p.mouse.move(x, y - 20, { steps: 6 }); await p.waitForTimeout(1100);
    const bb = await p.locator('.reel-row .reel:nth-child(5)').boundingBox(); await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2, { steps: 6 }); await p.waitForTimeout(500);
    await p.mouse.move(720, 450, { steps: 3 });
    await wheelTo(H, 240); await p.waitForTimeout(1200);
    // finale: the WhatsApp button in the final panel
    [x, y] = await c('.final-inner .btn-wa'); await p.mouse.move(x, y, { steps: 6 }); await p.waitForTimeout(1200);
    log('end');
  } else {
    await p.waitForTimeout(3000); log('entrance');
    const H = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
    const touchScroll = async (dy, ms) => { const steps = Math.round(ms / 50); for (let i = 0; i < steps; i++) { await p.evaluate((d) => window.scrollBy(0, d), dy / steps); await p.waitForTimeout(50); } };
    await touchScroll(700, 1400); await p.waitForTimeout(2600); log('phone');
    // a tap ripple on an empty area of the concierge card
    const bb = await p.locator('.concierge .cc-head').boundingBox(); await p.touchscreen.tap(bb.x + bb.width - 30, bb.y + 20); await p.waitForTimeout(900);
    await touchScroll(1300, 1800); await p.waitForTimeout(500);
    const rest = H - (await p.evaluate(() => scrollY));
    await touchScroll(rest, 9500); await p.waitForTimeout(800); log('end');
  }
  const v = p.video(); await ctx.close(); const path = await v.path(); fs.renameSync(path, __dirname + '/raw_' + which + '.webm');
  await b.close(); sv.close();
})();
