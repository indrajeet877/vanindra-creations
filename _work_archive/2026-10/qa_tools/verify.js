// Full acceptance check for a candidate homepage.
// Usage: node verify.js <dir-with-index.html>
// Checks: golden rules (names, phone numbers), WhatsApp targets, required features/functions,
// Hindi toggle round trip, no horizontal overflow 320-1920, page errors, broken local links/images,
// tap-target sizes on mobile, required links to the other public pages.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const dir = path.resolve(process.argv[2]);
const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
const fails = []; const warns = []; const ok = [];
const check = (cond, msg, warnOnly) => { if (cond) ok.push(msg); else (warnOnly ? warns : fails).push(msg); };

// ---------- static checks ----------
check(!/guggy|sahil|indrajeet/i.test(html), 'no nicknames / background names in source');
const nums = [...html.matchAll(/(?:\+?\d[\d\s-]{8,}\d)/g)].map((m) => m[0].replace(/\D/g, '')).filter((d) => d.length >= 10).map((d) => d.slice(-10));
const badNums = [...new Set(nums.filter((d) => !/^(8112859437|8756539282)$/.test(d) && /^[6-9]/.test(d)))];
check(badNums.length === 0, 'only the official phone number appears' + (badNums.length ? ' (found: ' + badNums.join(', ') + ')' : ''));
const wa = [...html.matchAll(/(?:wa\.me|api\.whatsapp\.com\/send\?phone=)\/?(\d+)/g)].map((m) => m[1]);
const waConst = (html.match(/WHATSAPP_NUMBER\s*=\s*['"`](\d+)['"`]/) || [])[1];
check(wa.every((n) => n === '918112859437') && (wa.length > 0 || waConst === '918112859437') && (!waConst || waConst === '918112859437'), `every WhatsApp link goes to 918112859437 (${wa.length} literal links, constant ${waConst || 'none'})`);
for (const f of ['playVandanaViralReel', 'closeVandanaViralReel', 'setLanguageMode', 'updateROICalc', 'openElegantWhatsAppDirect', 'sendCustomHeroWhatsApp', 'switchPhoneSimulation', 'sendZeroTouchWhatsApp', 'downloadZeroTouchFile', 'startHindiVoiceInput', 'selectPackageInForm'])
  check(new RegExp('function\\s+' + f + '\\b|' + f + '\\s*=\\s*(async\\s*)?(function|\\()').test(html), `function ${f} defined`, ['openElegantWhatsAppDirect', 'selectPackageInForm', 'sendCustomHeroWhatsApp'].includes(f));
check(/pollinations/.test(html), 'AI plan uses pollinations API');
for (const l of ['login.html', 'thumbnail-studio.html']) check(html.includes(l), `links to ${l}`);
check(!/href=["']pitch-deck\.html/.test(html), 'no public link to the internal pitch-deck playbook');
const bf = (html.match(/backdrop-filter\s*:/g) || []).length;
check(true, `backdrop-filter rules in CSS: ${bf}`);
for (const h of ['@vandanay2012', '@smitayadav_0901', '@yadavakarsh_07', 'smitayadav497@gmail.com', 'Vandana Yadav', 'Smita Yadav', 'Akarsh Yadav', 'Gargi', 'Allahabad'])
  check(html.includes(h), `mentions ${h}`);
// Akarsh Yadav's email contains his private mobile digits: removed from public pages on 18 Oct 2026 and must stay off.
check(!html.includes('akarshgkp8756539282'), "Akarsh Yadav's private email is not on the page");
for (const p of ['2,999', '14,999', '24,999', '39,999']) check(html.includes(p), `price ₹${p} present`);
for (const r of ['DZSZW2ey529', 'Ddl3VLbu4P5', 'Dds1foTyrQm', 'DSZ8VilkrA8', 'DedHDrLgY43', 'Da0lVfrAa47']) check(html.includes(r), `reel ${r} present`);
check(!/★★★★★|5-star|five-star/i.test(html), 'no fake 5-star testimonial markup', true);
const gl = [...html.matchAll(/[^.<>]{0,50}guarantee[^.<>]{0,50}/gi)].map((m) => m[0].trim()).filter((t) => !/\b(no|not|never|don't|do not|isn't|cannot|can't|without|nobody|honest)\b|\?/i.test(t));
check(gl.length === 0, 'no un-negated "guarantee" wording' + (gl.length ? ': ' + gl.slice(0, 4).join(' || ') : ''), true);
const dataHi = (html.match(/data-hi=/g) || []).length;
check(dataHi >= 150, `data-hi translations: ${dataHi}`, true);
check(!/crest|v-wing/i.test(html.replace(/<!--[\s\S]*?-->/g, '')), 'no crest logo image', true);

// ---------- browser checks ----------
const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.js': 'text/javascript', '.css': 'text/css', '.ico': 'image/x-icon' };
const missing = new Set();
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(dir, p);
  fs.readFile(f, (e, d) => { if (e) { missing.add(p); res.writeHead(404); return res.end('nf'); } res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
}).listen(0, async () => {
  const port = server.address().port; const url = `http://127.0.0.1:${port}/index.html`;
  const b = await chromium.launch(); const errors = [];
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  await ctx.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  await p.goto(url, { waitUntil: 'load' }); await p.waitForTimeout(800);

  // overflow sweep
  const bad = [];
  for (let w = 1920; w >= 320; w -= 20) {
    await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(25);
    const r = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
    if (r[0] > r[1]) bad.push(`${w}px (scrollWidth ${r[0]})`);
  }
  check(bad.length === 0, 'no horizontal overflow 320-1920' + (bad.length ? ': ' + bad.slice(0, 6).join(', ') : ''));

  // Hindi round trip
  await p.setViewportSize({ width: 1440, height: 900 });
  const t0 = await p.evaluate(() => document.body.innerText);
  const hasToggle = await p.evaluate(() => typeof setLanguageMode === 'function');
  if (hasToggle) {
    await p.evaluate(() => setLanguageMode('hi')); await p.waitForTimeout(150);
    const tHi = await p.evaluate(() => document.body.innerText);
    const devanagari = (tHi.match(/[ऀ-ॿ]/g) || []).length;
    check(devanagari > 500, `Hindi mode shows Devanagari text (${devanagari} chars)`);
    await p.evaluate(() => setLanguageMode('en')); await p.waitForTimeout(150);
    const t1 = await p.evaluate(() => document.body.innerText);
    check(t0 === t1, 'English -> Hindi -> English round trip restores the page exactly');
  } else fails.push('setLanguageMode not callable');

  // WhatsApp links at runtime
  const waRuntime = await p.evaluate(() => [...document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]')].map((a) => a.getAttribute('href')));
  check(waRuntime.every((h) => /918112859437/.test(h)), `runtime WhatsApp anchors all target the official number (${waRuntime.length})`);

  // WhatsApp functions open the official number
  const opened = await p.evaluate(() => { const urls = []; const o = window.open; window.open = (u) => { urls.push(String(u)); return null; }; const la = window.location; for (const f of ['openElegantWhatsAppDirect', 'sendCustomHeroWhatsApp', 'sendZeroTouchWhatsApp']) { try { if (typeof window[f] === 'function') window[f](); } catch (e) { urls.push('ERR ' + f + ': ' + e.message); } } window.open = o; return urls; });
  check(opened.length > 0 && opened.every((u) => /918112859437/.test(u)), 'WhatsApp functions open wa.me/918112859437: ' + JSON.stringify(opened.map((u) => u.slice(0, 60))), true);

  // broken images
  const brokenImgs = await p.evaluate(() => [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && !/^https?:/.test(i.getAttribute('src') || '') ).map((i) => i.getAttribute('src')));
  check(brokenImgs.length === 0, 'no broken local images' + (brokenImgs.length ? ': ' + brokenImgs.join(', ') : ''));

  // reel player
  const reel = await p.evaluate(() => { try { playVandanaViralReel('DZSZW2ey529'); const m = [...document.querySelectorAll('iframe')].find((f) => /instagram\.com\/(reel|p)\/DZSZW2ey529/.test(f.src)); const okk = !!m; closeVandanaViralReel(); return okk; } catch (e) { return 'err ' + e.message; } });
  check(reel === true, 'Reel player opens an Instagram embed iframe and closes' + (reel !== true ? ` (${reel})` : ''));

  // ROI calculator reacts
  const roi = await p.evaluate(() => { try { const r = [...document.querySelectorAll('input[type=range]')]; if (!r.length) return 'no range inputs'; const before = document.body.innerText; r[0].value = r[0].max; r[0].dispatchEvent(new Event('input', { bubbles: true })); return document.body.innerText !== before; } catch (e) { return 'err ' + e.message; } });
  check(roi === true, 'ROI calculator updates when slider moves' + (roi !== true ? ` (${roi})` : ''));

  // mobile: sticky bar and tap targets
  const m = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await m.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => r.abort());
  const mp = await m.newPage(); mp.on('pageerror', (e) => errors.push('mobile pageerror: ' + e.message));
  await mp.goto(url, { waitUntil: 'load' }); await mp.waitForTimeout(600);
  await mp.evaluate(() => window.scrollTo({ top: 1500, behavior: 'instant' })); await mp.waitForTimeout(400);
  const sticky = await mp.evaluate(() => [...document.querySelectorAll('a,button')].filter((e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.bottom > innerHeight - 120 && r.top < innerHeight && r.height > 0 && cs.visibility !== 'hidden' && /whatsapp|ai plan|plan/i.test(e.innerText); }).map((e) => e.innerText.trim()));
  check(sticky.length >= 2, 'mobile sticky bar with WhatsApp + AI plan: ' + JSON.stringify(sticky));
  const small = await mp.evaluate(() => [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter((e) => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none') return false; if (e.closest('p,li') && e.tagName === 'A' && getComputedStyle(e).display === 'inline') return false; return r.height < 40 || r.width < 40; }).map((e) => `${e.tagName}:${(e.innerText || e.getAttribute('aria-label') || e.name || '').trim().slice(0, 24)} ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`));
  check(small.length <= 8, `mobile tap targets under 40px: ${small.length}` + (small.length ? ' e.g. ' + small.slice(0, 8).join(' | ') : ''), true);
  const blurN = await mp.evaluate(() => [...document.querySelectorAll('*')].filter((e) => { const cs = getComputedStyle(e); const v = cs.backdropFilter || cs.webkitBackdropFilter || ''; return v && v !== 'none' && cs.display !== 'none' && cs.visibility !== 'hidden'; }).length);
  check(blurN <= 8, `mobile elements with backdrop-filter: ${blurN} (max 8)`);
  const mh = await mp.evaluate(() => document.body.scrollHeight);
  check(mh <= 12000, `mobile page height ${mh}px`, true);

  check(errors.length === 0, 'no page errors' + (errors.length ? ': ' + errors.slice(0, 5).join(' | ') : ''));
  const miss = [...missing].filter((x) => !/favicon/.test(x));
  check(miss.length === 0, 'no missing local files requested' + (miss.length ? ': ' + miss.join(', ') : ''));

  console.log(`PASS ${ok.length}  WARN ${warns.length}  FAIL ${fails.length}`);
  if (warns.length) console.log('WARN:\n  ' + warns.join('\n  '));
  if (fails.length) console.log('FAIL:\n  ' + fails.join('\n  '));
  await b.close(); server.close(); process.exit(fails.length ? 1 : 0);
});
