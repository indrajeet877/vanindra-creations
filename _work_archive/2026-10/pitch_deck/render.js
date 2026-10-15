// Render the VanIndra pitch deck: slide PNGs (EN + HI), PDFs (EN + HI), phone + desktop viewer shots, overflow checks.
// Usage: node render.js [--pdf] [--quick]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const DECK = path.resolve(__dirname, '..');
const WORK = __dirname;
const args = process.argv.slice(2);
const WANT_PDF = args.includes('--pdf');
const types = { '.html': 'text/html; charset=utf-8', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.js': 'text/javascript', '.css': 'text/css', '.pdf': 'application/pdf' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'pitch-deck.html';
  const f = path.join(DECK, p);
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); return res.end('nf'); } res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
});

async function settle(page) {
  await page.evaluate(async () => { await document.fonts.ready; await Promise.all(Array.from(document.images).map((im) => im.complete ? 0 : new Promise((r) => { im.onload = im.onerror = r; }))); });
  await page.waitForTimeout(400);
}

async function overflowReport(page, tag) {
  return page.evaluate((tag) => {
    const out = [];
    document.querySelectorAll('.slide').forEach((s, i) => {
      const sr = s.getBoundingClientRect();
      s.querySelectorAll('*').forEach((el) => {
        if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
        const r = el.getBoundingClientRect();
        if (!r.width || !r.height) return;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none') return;
        if (el.closest('.screen')) return; // phone internals are clipped by design
        if (el.closest('.cv-media')) return;
        if (r.right > sr.right + 1 || r.bottom > sr.bottom + 1 || r.left < sr.left - 1) {
          out.push(`${tag} slide ${i + 1}: <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className}"> out of slide by R${Math.round(r.right - sr.right)} B${Math.round(r.bottom - sr.bottom)} L${Math.round(sr.left - r.left)}`);
        }
        // text clipped inside its own box
        if ((el.scrollWidth > el.clientWidth + 2) && cs.overflow !== 'visible' && !el.classList.contains('tt') && el.clientWidth > 0) {
          out.push(`${tag} slide ${i + 1}: <${el.tagName.toLowerCase()} class="${el.className}"> h-clipped ${el.scrollWidth}>${el.clientWidth}`);
        }
      });
      // safe-zone check: content too close to the bottom edge
      let maxB = 0; s.querySelectorAll('p,h1,h2,h3,li,span,b,small,img,.cr,.plan,.node,.lk').forEach((el) => { const r = el.getBoundingClientRect(); if (r.height && !el.closest('.screen')) maxB = Math.max(maxB, r.bottom - sr.top); });
      if (maxB > 1080 - 40) out.push(`${tag} slide ${i + 1}: content reaches y=${Math.round(maxB)} (safe bottom 1040)`);
    });
    return out;
  }, tag);
}

server.listen(0, async () => {
  const port = server.address().port; const url = `http://127.0.0.1:${port}/pitch-deck.html`;
  const browser = await chromium.launch();
  const errors = [];
  const report = [];
  fs.mkdirSync(path.join(DECK, 'slides'), { recursive: true });
  fs.mkdirSync(path.join(WORK, 'hi'), { recursive: true });
  fs.mkdirSync(path.join(WORK, 'shots'), { recursive: true });

  // ---- slide PNGs + PDFs (print geometry) ----
  for (const lang of ['en', 'hi']) {
    const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(`${lang} pageerror: ${e.message}`));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(`${lang} console: ${m.text().slice(0, 200)}`); });
    page.on('requestfailed', (r) => errors.push(`${lang} requestfailed: ${r.url().slice(0, 120)}`));
    await page.goto(url, { waitUntil: 'networkidle' });
    if (lang === 'hi') await page.evaluate(() => setLanguageMode('hi'));
    await page.emulateMedia({ media: 'print' });
    await settle(page);
    report.push(...await overflowReport(page, lang.toUpperCase()));
    const n = await page.locator('.slide').count();
    for (let i = 0; i < n; i++) {
      const out = lang === 'en' ? path.join(DECK, 'slides', `${String(i + 1).padStart(2, '0')}.png`) : path.join(WORK, 'hi', `${String(i + 1).padStart(2, '0')}.png`);
      await page.locator('.slide').nth(i).screenshot({ path: out });
    }
    if (WANT_PDF) {
      const pdfPath = path.join(DECK, lang === 'en' ? 'VanIndra_Pitch_Deck_EN.pdf' : 'VanIndra_Pitch_Deck_HI.pdf');
      await page.pdf({ path: pdfPath, width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    }
    await ctx.close();
  }

  // ---- phone PDFs (WhatsApp version): 390 px responsive layout, one page per slide (named @page sizes) ----
  if (WANT_PDF) {
    for (const lang of ['en', 'hi']) {
      const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
      const page = await ctx.newPage();
      page.on('pageerror', (e) => errors.push(`phonepdf ${lang} pageerror: ${e.message}`));
      // smaller copies of the portfolio images keep the phone PDF light (work/phoneimg, max 480 px wide)
      await page.route('**/assets/portfolio/*.jpg', (route) => {
        const f = path.join(WORK, 'phoneimg', path.basename(new URL(route.request().url()).pathname));
        return fs.existsSync(f) ? route.fulfill({ path: f, contentType: 'image/jpeg' }) : route.continue();
      });
      await page.goto(url, { waitUntil: 'networkidle' });
      if (lang === 'hi') await page.evaluate(() => setLanguageMode('hi'));
      await page.evaluate(() => document.documentElement.classList.add('pdfphone'));
      await page.emulateMedia({ media: 'screen' });
      await settle(page);
      const hs = await page.evaluate(() => {
        const ss = Array.from(document.querySelectorAll('.slide'));
        const hs = ss.map((s) => Math.ceil(s.getBoundingClientRect().height));
        const st = document.createElement('style');
        st.textContent = hs.map((h, i) => `@page p${i + 1}{size:390px ${h}px;margin:0}`).join('\n') + '\n' +
          ss.map((s, i) => `#${s.id}{page:p${i + 1};break-after:page;break-inside:avoid}`).join('\n') + `\n#${ss[ss.length - 1].id}{break-after:auto}`;
        document.head.appendChild(st);
        return hs;
      });
      const out = path.join(DECK, lang === 'en' ? 'VanIndra_Pitch_Deck_Phone_EN.pdf' : 'VanIndra_Pitch_Deck_Phone_Hinglish.pdf');
      await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
      report.push(`phone pdf ${lang}: ${hs.length} slides, heights ${hs.join(',')}, ${Math.round(fs.statSync(out).size / 1024)} KB`);
      await ctx.close();
    }
  }

  // ---- desktop viewer (deck mode) ----
  {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(`viewer pageerror: ${e.message}`));
    await page.goto(url + '#1', { waitUntil: 'networkidle' }); await settle(page);
    await page.screenshot({ path: path.join(WORK, 'shots', 'viewer_1440_s1.png') });
    await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowRight'); await page.waitForTimeout(600);
    await page.screenshot({ path: path.join(WORK, 'shots', 'viewer_1440_s3.png') });
    const st = await page.evaluate(() => ({ cur: document.querySelector('.slide.active').id, hash: location.hash, count: document.getElementById('uiCount').textContent, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
    report.push('viewer state after 2x ArrowRight: ' + JSON.stringify(st));
    await page.setViewportSize({ width: 1280, height: 1000 }); await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(WORK, 'shots', 'viewer_1280x1000.png') });
    await ctx.close();
  }

  // ---- phone (scroll mode) ----
  for (const lang of ['en', 'hi']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    page.on('pageerror', (e) => errors.push(`phone pageerror: ${e.message}`));
    await page.goto(url, { waitUntil: 'networkidle' });
    if (lang === 'hi') await page.evaluate(() => setLanguageMode('hi'));
    await settle(page);
    const ov = await page.evaluate(() => {
      const bad = [];
      const W = document.documentElement.clientWidth;
      document.querySelectorAll('.slide *').forEach((el) => { const r = el.getBoundingClientRect(); if (r.width && (r.right > W + 1 || r.left < -1) && !el.closest('.screen') && !el.closest('svg')) bad.push(`${el.tagName}.${el.className && el.className.baseVal === undefined ? el.className : ''} R${Math.round(r.right)}`); });
      return { sw: document.documentElement.scrollWidth, cw: W, h: document.documentElement.scrollHeight, bad: bad.slice(0, 12) };
    });
    report.push(`phone ${lang}: scrollWidth=${ov.sw} clientWidth=${ov.cw} height=${ov.h} ${ov.bad.length ? 'OVERFLOW: ' + ov.bad.join(', ') : 'no overflow'}`);
    await page.screenshot({ path: path.join(WORK, 'shots', `phone_${lang}_full.png`), fullPage: true });
    await page.screenshot({ path: path.join(WORK, 'shots', `phone_${lang}_fold.png`) });
    await ctx.close();
  }

  await browser.close(); server.close();
  console.log(report.length ? report.join('\n') : 'no layout issues');
  console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'no page errors');
});
