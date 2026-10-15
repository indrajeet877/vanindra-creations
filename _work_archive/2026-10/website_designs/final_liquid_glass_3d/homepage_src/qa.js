const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const serve = require('./serve'); const Q = __dirname + '/../qa/';
const GL = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'];
const only = process.argv[2];
(async () => {
  const sv = await serve(); const errs = [];
  const run = async (name, opts, fn, args) => {
    if (only && !name.startsWith(only)) return;
    const b = await chromium.launch({ args: args || GL });
    const ctx = await b.newContext(Object.assign({ viewport: { width: 1440, height: 900 } }, opts));
    await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
    const p = await ctx.newPage();
    p.on('pageerror', (e) => errs.push(name + ': ' + e.message));
    p.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') { const t = m.text(); if (!/ERR_|net::|Failed to load/.test(t)) errs.push(name + ' console: ' + t.slice(0, 200)); } });
    try { await fn(p); } catch (e) { errs.push(name + ' script: ' + e.message); }
    await b.close();
  };
  const settle = async (p, ms) => { await p.waitForTimeout(ms || 3200); };
  const shot = (p, n, o) => p.screenshot(Object.assign({ path: Q + n + '.png' }, o || {}));
  // intro + entrance timeline
  
  await run('dark_1440', {}, async (p) => { await p.addInitScript(() => { localStorage.setItem('vanindra_theme', 'dark'); (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now()))); }); await p.goto(sv.url); await settle(p); await shot(p, 'dark_1440_fold'); });
  await run('dark_390', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, async (p) => { await p.addInitScript(() => { localStorage.setItem('vanindra_theme', 'dark'); (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now()))); }); await p.goto(sv.url); await settle(p); await shot(p, 'dark_390_fold'); await p.evaluate(() => window.scrollTo(0, 700)); await p.waitForTimeout(2500); await shot(p, 'dark_390_phone'); });
  await run('hi_390', { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, async (p) => { await p.addInitScript(() => (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now())))); await p.goto(sv.url); await settle(p, 1500); await p.evaluate(() => setLanguageMode('hi')); await p.waitForTimeout(800); await shot(p, 'hi_390_fold'); });
  await run('hi_1440', {}, async (p) => { await p.addInitScript(() => (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now())))); await p.goto(sv.url); await settle(p, 1500); await p.evaluate(() => setLanguageMode('hi')); await p.waitForTimeout(800); await shot(p, 'hi_1440_fold'); });
  await run('w320', { viewport: { width: 320, height: 720 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 }, async (p) => { await p.addInitScript(() => (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now())))); await p.goto(sv.url); await settle(p); await shot(p, 'w320_fold'); await p.evaluate(() => window.scrollTo(0, 640)); await p.waitForTimeout(2600); await shot(p, 'w320_phone'); });
  await run('nowebgl', {}, async (p) => { await p.addInitScript(() => (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now())))); await p.goto(sv.url); await settle(p); await shot(p, 'nowebgl_1440_fold'); }, ['--disable-webgl', '--disable-3d-apis']);
  await run('nojs', { javaScriptEnabled: false }, async (p) => { await p.goto(sv.url); await p.waitForTimeout(1500); await shot(p, 'nojs_1440_fold'); await shot(p, 'nojs_1440_full', { fullPage: true }); });
  await run('rm', { reducedMotion: 'reduce' }, async (p) => { await p.goto(sv.url); await p.waitForTimeout(1500); await shot(p, 'rm_1440_fold'); });
  await run('hover', {}, async (p) => {
    await p.addInitScript(() => (sessionStorage.setItem('vi_intro', '1'), localStorage.setItem('vi_intro', String(Date.now())))); await p.goto(sv.url); await settle(p);
    const box = async (sel) => { const b = await p.locator(sel).first().boundingBox(); return [b.x + b.width / 2, b.y + b.height / 2, b]; };
    let [x, y] = await box('.hero-head .btn-glass'); await p.mouse.move(x - 120, y + 60); await p.mouse.move(x + 20, y + 4, { steps: 12 }); await p.waitForTimeout(900); await shot(p, 'hover_button', { clip: { x: x - 260, y: y - 120, width: 520, height: 240 } });
    [x, y] = await box('.hero-head .btn-primary'); await p.mouse.move(x + 30, y + 5, { steps: 12 }); await p.waitForTimeout(900); await shot(p, 'hover_whatsapp', { clip: { x: x - 220, y: y - 110, width: 520, height: 260 } });
    await p.evaluate(() => document.querySelector('#reels').scrollIntoView({ block: 'center' })); await p.waitForTimeout(1600);
    let b; [x, y, b] = await box('.reel-row .reel:nth-child(2)'); await p.mouse.move(x - 40, y - 60); await p.mouse.move(x, y, { steps: 14 }); await p.waitForTimeout(900); await shot(p, 'hover_reel', { clip: { x: b.x - 120, y: b.y - 40, width: b.width + 240, height: b.height + 80 } });
    await p.evaluate(() => document.querySelector('.marquee').scrollIntoView({ block: 'center' })); await p.waitForTimeout(1200);
    [x, y, b] = await box('.marquee'); await p.mouse.move(x, y + 2, { steps: 8 }); await p.waitForTimeout(800); await shot(p, 'hover_drag', { clip: { x: x - 300, y: y - 120, width: 600, height: 240 } });
    await p.evaluate(() => document.querySelector('#smart-ai-portal').scrollIntoView({ block: 'center' })); await p.waitForTimeout(1500);
    [x, y, b] = await box('#ztName'); await p.mouse.move(x, y, { steps: 8 }); await p.waitForTimeout(600); await shot(p, 'hover_input', { clip: { x: b.x - 40, y: b.y - 60, width: 420, height: 160 } });
    console.log('cursor state over input:', await p.evaluate(() => window.FX && FX.cursorState && FX.cursorState()));
    await p.evaluate(() => document.querySelector('#pricing').scrollIntoView({ block: 'start' })); await p.waitForTimeout(1500);
    [x, y, b] = await box('.plan-pro'); await p.mouse.move(x + 60, y - 80, { steps: 10 }); await p.waitForTimeout(900); await shot(p, 'hover_plan', { clip: { x: b.x - 60, y: b.y - 40, width: b.width + 120, height: b.height + 80 } });
  });
  console.log(errs.length ? errs.join('\n') : 'no errors');
  sv.close();
})();
