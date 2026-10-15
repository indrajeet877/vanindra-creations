// Acceptance check for login.html (client portal preview) and thumbnail-studio.html (cover studio).
// Usage: node verify_pages.js [dir]   (dir defaults to this file's folder)
// Blocks all non-local network. Checks golden rules (static HTML + rendered text), function names,
// demo login -> dashboard -> approve -> logout, signup + login + saved-session auto-open,
// submitClientBrief -> wa.me/918112859437, photo upload -> render -> PNG download 1080x1920,
// overflow 320/390/768/1024/1440/1920 in both themes and languages, Hindi round trip,
// mobile tap targets / blur budget, focus ring, cursor rules, reduced motion and no-JS fallbacks.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2] || __dirname);
const PHOTO = '/home/user/vanindra-creations/assets/portfolio/reel_DZSZW2ey529.jpg';
const fails = [], warns = [], ok = [];
const check = (cond, msg, warnOnly) => { if (cond) ok.push(msg); else (warnOnly ? warns : fails).push(msg); };
// names that must never appear (built from pieces so this script never spells them either)
const BANNED = new RegExp(['gug' + 'gy', 'sa' + 'hil', 'indra' + 'jeet'].join('|'), 'i');
const PAGES = { login: 'login.html', studio: 'thumbnail-studio.html' };
// <wbr> (soft line-break hints inside long emails) is markup, not text: strip it before the text checks
const src = {}; for (const k in PAGES) src[k] = fs.readFileSync(path.join(dir, PAGES[k]), 'utf8').replace(/<wbr>/g, '');

/* ---------------- static checks ---------------- */
for (const [k, html] of Object.entries(src)) {
  const P = `[${k}]`;
  check(!BANNED.test(html), `${P} no nicknames / background names anywhere in the source`);
  const nums = [...html.matchAll(/(?:\+?\d[\d\s-]{8,}\d)/g)].map((m) => m[0].replace(/\D/g, '')).filter((d) => d.length >= 10).map((d) => d.slice(-10));
  const bad = [...new Set(nums.filter((d) => d !== '8112859437' && /^[6-9]/.test(d)))];
  const emailOnly = bad.every((d) => d === '8756539282') && (html.match(/8756539282/g) || []).length === (html.match(/akarshgkp8756539282@gmail\.com/g) || []).length;
  check(bad.length === 0 || emailOnly, `${P} only the official phone number +91 81128 59437 appears` + (bad.length && !emailOnly ? ' (found ' + bad.join(', ') + ')' : ''));
  const wa = [...html.matchAll(/(?:wa\.me|api\.whatsapp\.com\/send\?phone=)\/?(\d+)/g)].map((m) => m[1]);
  check(wa.length > 0 && wa.every((n) => n === '918112859437'), `${P} every WhatsApp link goes to wa.me/918112859437 (${wa.length})`);
  check(!/7[- ]day (free )?audit|free 7/i.test(html), `${P} no "Free 7-day audit" wording`);
  check(!/84\.2|above baseline|hook hold/i.test(html), `${P} no invented performance numbers`);
  check(!/pitch-deck/i.test(html), `${P} no pitch-deck link`);
  check(!/★★★★★|5-star|testimonial/i.test(html), `${P} no testimonials / star ratings`);
  const g = [...html.matchAll(/[^.<>]{0,60}guarantee[^.<>]{0,60}/gi)].map((m) => m[0]).filter((t) => !/\b(no|not|never|don't)\b/i.test(t));
  check(g.length === 0, `${P} no un-negated guarantee wording` + (g.length ? ': ' + g[0] : ''));
  check(!/<script[^>]+src=/i.test(html), `${P} no external scripts (everything inline)`);
  check(!/three(\.module)?(\.min)?\.js|THREE\./.test(html), `${P} three.js not used`);
  check(!/<img[^>]+(logo|crest)/i.test(html), `${P} text wordmark only (no logo image)`);
  const js = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].reduce((a, m) => a + m[1].length, 0);
  check(js <= 120 * 1024, `${P} inline JS ${(js / 1024).toFixed(1)} KB (max 120 KB)`);
  const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || '', desc = (html.match(/<meta name="description" content="([^"]+)"/) || [])[1] || '';
  check(title.length > 20 && /VanIndra/.test(title) && desc.length > 80, `${P} descriptive title + meta description ("${title}")`);
  check(/vanindra_theme/.test(html) && /dark-studio/.test(html), `${P} shared dark-mode key + body.dark-studio`);
  check((html.match(/data-hi=/g) || []).length >= 40, `${P} data-hi translations: ${(html.match(/data-hi=/g) || []).length}`);
  for (const id of ['icon-instagram', 'icon-whatsapp', 'icon-gmail']) check(html.includes(`id="${id}"`), `${P} official ${id} SVG present`);
  for (const h of ['@vandanay2012', '@smitayadav_0901', '@yadavakarsh_07', '+91 81128 59437', 'smitayadav497@gmail.com', 'Vandana Yadav']) check(html.includes(h), `${P} mentions ${h}`);
}
{
  const L = src.login, P = '[login]';
  for (const f of ['approveReel', 'demoLogin', 'handleLogin', 'handleSignup', 'logoutClient', 'openDashboardForUser', 'submitClientBrief', 'switchAuthTab', 'setLanguageMode', 'toggleSurfaceTheme'])
    check(new RegExp('function\\s+' + f + '\\s*\\(').test(L), `${P} function ${f} defined`);
  for (const key of ['vanindra_active_client', 'vanindra_client_accounts']) check(L.includes(`'${key}'`), `${P} localStorage key ${key}`);
  for (const t of ['Free page audit + a 15-second sample edit', '₹2,999', '₹14,999', '₹24,999', '12 Reels/month', '20 Reels/month', 'Recommended', 'by application', 'Sample workspace — illustration, not a client result', 'only in this browser', 'thumbnail-studio.html', 'index.html', 'Akarsh Yadav', 'Smita Yadav', 'akarshgkp8756539282@gmail.com'])
    check(L.includes(t), `${P} contains "${t}"`);
  check(!/vip[^<]{0,80}₹39,999[^<]{0,40}(pay|buy|checkout)/i.test(L), `${P} VIP is not sold here (application / waitlist only)`);
  const S = src.studio, Q = '[studio]';
  for (const f of ['clearPhoto', 'downloadThumbnail', 'handleImageUpload', 'renderThumbnail', 'setLanguageMode', 'toggleSurfaceTheme'])
    check(new RegExp('function\\s+' + f + '\\s*\\(').test(S), `${Q} function ${f} defined`);
  check(/<canvas id="thumbCanvas" width="1080" height="1920"/.test(S), `${Q} canvas output size 1080×1920 unchanged`);
  check(S.includes("'VanIndra_Creations_Reel_Cover_1080x1920.png'"), `${Q} PNG filename unchanged`);
  for (const l of ['index.html', 'login.html']) check(S.includes(`href="${l}"`), `${Q} links to ${l}`);
}

/* ---------------- browser checks ---------------- */
const types = { '.html': 'text/html', '.jpg': 'image/jpeg', '.png': 'image/png', '.svg': 'image/svg+xml', '.js': 'text/javascript' };
const missing = new Set();
const server = http.createServer((q, s) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  fs.readFile(path.join(dir, p), (e, d) => { if (e) { if (!/favicon|index\.html/.test(p)) missing.add(p); s.writeHead(404); return s.end(); } s.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' }); s.end(d); });
}).listen(0, async () => {
  const base = `http://127.0.0.1:${server.address().port}/`;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const errors = [], foreign = new Set();
  const ctxFor = async (opts = {}) => {
    const c = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true, ...opts });
    await c.route(/^https?:\/\/(?!127\.0\.0\.1)/, (r) => { const u = r.request().url(); if (!/fonts\.(googleapis|gstatic)\.com/.test(u)) foreign.add(u.slice(0, 80)); return r.abort(); });
    return c;
  };
  const open = async (c, page, tag) => {
    const p = await c.newPage();
    p.on('pageerror', (e) => errors.push(`${tag} pageerror: ${e.message}`));
    p.on('console', (m) => { if (m.type() === 'error' && !/ERR_|net::|Failed to load resource/i.test(m.text())) errors.push(`${tag} console: ${m.text().slice(0, 140)}`); });
    await p.goto(base + page, { waitUntil: 'load' }); await p.waitForTimeout(700);
    return p;
  };
  const textScan = async (p, tag) => {
    const t = await p.evaluate(() => document.body.innerText);
    check(!BANNED.test(t), `${tag} rendered text has no banned names`);
    const nums = [...t.matchAll(/(?:\+?\d[\d\s-]{8,}\d)/g)].map((m) => m[0].replace(/\D/g, '').slice(-10)).filter((d) => d.length === 10 && /^[6-9]/.test(d) && d !== '8112859437' && d !== '8756539282');
    check(nums.length === 0, `${tag} rendered text shows no other phone number`);
    const waR = await p.evaluate(() => [...document.querySelectorAll('a[href*="wa.me"],a[href*="whatsapp.com"]')].map((a) => a.getAttribute('href')));
    check(waR.every((h) => /^https:\/\/wa\.me\/918112859437/.test(h)), `${tag} runtime WhatsApp anchors all go to wa.me/918112859437 (${waR.length})`);
    const logos = await p.evaluate(() => {
      const miss = [];
      document.querySelectorAll('a[href*="instagram.com"]').forEach((a) => { if (!a.querySelector('use[href="#icon-instagram"]')) miss.push('IG ' + a.textContent.trim()); });
      document.querySelectorAll('a[href^="mailto:"]').forEach((a) => { if (!a.querySelector('use[href="#icon-gmail"]')) miss.push('mail ' + a.textContent.trim()); });
      document.querySelectorAll('a[href*="wa.me"]').forEach((a) => { if (!a.querySelector('use[href="#icon-whatsapp"]')) miss.push('wa ' + a.textContent.trim()); });
      return miss;
    });
    check(logos.length === 0, `${tag} official app logo next to every handle, phone and email link` + (logos.length ? ': ' + logos.join(' | ') : ''));
  };
  const roundTrip = async (p, tag) => {
    const t0 = await p.evaluate(() => document.body.innerText);
    await p.evaluate(() => setLanguageMode('hi')); await p.waitForTimeout(120);
    const th = await p.evaluate(() => document.body.innerText);
    const dev = (th.match(/[ऀ-ॿ]/g) || []).length;
    await p.evaluate(() => setLanguageMode('en')); await p.waitForTimeout(120);
    const t1 = await p.evaluate(() => document.body.innerText);
    check(dev > 300 && t0 === t1, `${tag} Hindi toggle shows Devanagari (${dev} chars) and round-trips exactly back to English`);
  };
  const overflow = async (p, tag, setup) => {
    const bad = [];
    for (const dark of [false, true]) for (const lang of ['en', 'hi']) {
      await p.evaluate(([dk, lg]) => { document.body.classList.toggle('dark-studio', dk); setLanguageMode(lg); }, [dark, lang]);
      for (const w of [1920, 1440, 1024, 768, 390, 320]) {
        await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(60);
        const r = await p.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
        if (r[0] > r[1]) bad.push(`${w}px ${dark ? 'dark' : 'light'} ${lang} (+${r[0] - r[1]})`);
      }
    }
    await p.evaluate(() => { document.body.classList.remove('dark-studio'); setLanguageMode('en'); });
    await p.setViewportSize({ width: 1440, height: 900 });
    check(bad.length === 0, `${tag} no horizontal overflow at 320/390/768/1024/1440/1920, light+dark, EN+HI` + (bad.length ? ': ' + bad.slice(0, 6).join(', ') : ''));
  };
  // every visible nav control must sit fully inside the glass pill (tablet widths clipped it before)
  const navFit = async (p, tag) => {
    const bad = [];
    for (const lang of ['en', 'hi']) {
      await p.evaluate((lg) => setLanguageMode(lg), lang);
      for (const w of [320, 360, 390, 721, 769, 800, 810, 820, 834, 900, 1024, 1080, 1180, 1280, 1440]) {
        await p.setViewportSize({ width: w, height: 900 }); await p.waitForTimeout(50);
        const r = await p.evaluate(() => {
          const nav = document.querySelector('.nav').getBoundingClientRect(), out = [];
          document.querySelectorAll('.nav a, .nav button, .nav .lang, .nav .crumb').forEach((e) => {
            const cs = getComputedStyle(e), b = e.getBoundingClientRect();
            if (cs.display === 'none' || cs.visibility === 'hidden' || e.closest('[hidden]') || !b.width) return;
            if (b.left < nav.left - 0.5 || b.right > nav.right + 0.5) out.push((e.id || e.className.split(' ')[0]) + ' ' + Math.round(b.right) + '>' + Math.round(nav.right));
            // text that breaks onto a second line (a 40 px button can hide a 2-line label, so count line boxes)
            const tops = new Set(); const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
            for (let n = tw.nextNode(); n; n = tw.nextNode()) { if (!n.textContent.trim() || getComputedStyle(n.parentElement).position === 'absolute') continue; const rg = document.createRange(); rg.selectNodeContents(n); for (const q of rg.getClientRects()) if (q.width > 1) tops.add(Math.round(q.top / 6)); }
            if (tops.size > 1 && !e.classList.contains('wm')) out.push((e.id || e.className.split(' ')[0]) + ' text wraps');
          });
          return out;
        });
        if (r.length) bad.push(`${w}px ${lang}: ${r.join(', ')}`);
      }
    }
    await p.evaluate(() => setLanguageMode('en')); await p.setViewportSize({ width: 1440, height: 900 });
    check(bad.length === 0, `${tag} every nav control fits inside the nav pill (no wrap) at 320–1440 px incl. iPad 769/800/810/820/834, EN+HI` + (bad.length ? ': ' + bad.slice(0, 4).join(' | ') : ''));
  };
  const mobileAudit = async (p, tag) => {
    const small = await p.evaluate(() => [...document.querySelectorAll('a,button,input,select,textarea,[role=tab],[role=radio]')].filter((e) => {
      const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      if (!r.width || !r.height || cs.visibility === 'hidden' || cs.display === 'none' || e.closest('[hidden]') || e.getAttribute('aria-hidden') === 'true' || e.tabIndex < 0) return false;
      if (e.tagName === 'A' && cs.display === 'inline' && e.closest('p,li')) return false;
      return r.height < 43.5 || r.width < 43.5;
    }).map((e) => `${e.tagName}#${e.id || ''}:${(e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 20)} ${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`));
    check(small.length === 0, `${tag} phone tap targets ≥ 44 px` + (small.length ? ': ' + small.slice(0, 6).join(' | ') : ''));
    const blur = await p.evaluate(() => [...document.querySelectorAll('*')].filter((e) => { const cs = getComputedStyle(e); const v = cs.backdropFilter || cs.webkitBackdropFilter || ''; return v && v !== 'none' && cs.display !== 'none' && !e.closest('[hidden]'); }).length);
    check(blur <= 8, `${tag} elements with backdrop-filter on phone: ${blur} (max 8)`);
    const cur = await p.evaluate(() => document.documentElement.classList.contains('mc-on') || !!document.querySelector('.mc-lens'));
    check(!cur, `${tag} no custom cursor on touch`);
  };

  /* ===== LOGIN: desktop ===== */
  {
    const c = await ctxFor(); const p = await open(c, PAGES.login, 'login');
    const fns = await p.evaluate(() => ['approveReel', 'demoLogin', 'handleLogin', 'handleSignup', 'logoutClient', 'openDashboardForUser', 'submitClientBrief', 'switchAuthTab'].filter((f) => typeof window[f] !== 'function'));
    check(fns.length === 0, '[login] all 8 portal functions callable' + (fns.length ? ' (missing ' + fns + ')' : ''));
    check(await p.isVisible('#authCard') && !(await p.isVisible('#dashboardSection')), '[login] auth view shows the sign-in panel; dashboard hidden');
    await textScan(p, '[login auth]');
    await roundTrip(p, '[login auth]');
    // tabs
    await p.click('#tabSignupBtn'); await p.waitForTimeout(200);
    const tabs1 = await p.evaluate(() => [!document.getElementById('signupForm').hidden, document.getElementById('loginForm').hidden, document.getElementById('tabSignupBtn').getAttribute('aria-selected')]);
    await p.click('#tabLoginBtn'); await p.waitForTimeout(200);
    const tabs2 = await p.evaluate(() => [!document.getElementById('loginForm').hidden, document.getElementById('signupForm').hidden]);
    check(tabs1[0] && tabs1[1] && tabs1[2] === 'true' && tabs2[0] && tabs2[1], '[login] Log in / Create account tabs switch forms');
    const plans = await p.evaluate(() => [...document.querySelectorAll('#regPlan option')].map((o) => o.textContent));
    check(plans.length === 5 && /Free page audit \+ a 15-second sample edit/.test(plans[0]) && plans.some((t) => /Starter.*12 Reels.*14,999/.test(t)) && plans.some((t) => /Pro Growth.*20 Reels.*24,999.*Recommended/.test(t)) && plans.some((t) => /Trial.*2,999/.test(t)) && plans.some((t) => /VIP.*by application/.test(t)), '[login] plan dropdown matches homepage plans + free offer: ' + JSON.stringify(plans));
    // cursor + focus (fine pointer)
    await p.mouse.move(300, 300, { steps: 4 }); await p.mouse.move(700, 420, { steps: 6 }); await p.waitForTimeout(200);
    check(await p.evaluate(() => document.documentElement.classList.contains('mc-on')), '[login] glass-lens cursor runs on fine pointers');
    const inp = await p.$('#loginId'); const bb = await inp.boundingBox();
    await p.mouse.move(bb.x + 40, bb.y + bb.height / 2, { steps: 5 }); await p.waitForTimeout(250);
    const nat = await p.evaluate(() => [document.querySelector('.mc-layer').dataset.s, getComputedStyle(document.getElementById('loginId')).cursor]);
    check(nat[0] === 'native' && nat[1] !== 'none', `[login] inputs keep the native caret (lens state ${nat[0]}, cursor ${nat[1]})`);
    await p.keyboard.press('Tab'); await p.keyboard.press('Tab'); await p.waitForTimeout(150);
    const foc = await p.evaluate(() => { const e = document.activeElement, cs = getComputedStyle(e); return [e.tagName + '#' + e.id, cs.outlineStyle, cs.outlineWidth, document.querySelector('.mc-layer').dataset.s, cs.boxShadow.slice(0, 40)]; });
    check(((foc[1] !== 'none' && parseFloat(foc[2]) >= 2) || /rgba\(14, 107, 78/.test(foc[4])) && foc[3] === 'out', `[login] keyboard focus ring visible and the lens steps aside (${foc.join(' ')})`);
    // demo -> dashboard -> approve -> round trip -> logout
    await p.click('#btnDemo'); await p.waitForTimeout(1500);
    const d1 = await p.evaluate(() => [document.getElementById('authSection').hidden, !document.getElementById('dashboardSection').hidden, !!localStorage.getItem('vanindra_active_client'), document.getElementById('dashWelcomeName').innerText, document.body.innerText.includes('Sample workspace — illustration, not a client result')]);
    check(d1[0] && d1[1] && d1[2] && /Welcome, Sample Creator/.test(d1[3]) && d1[4], '[login] demo login opens the labelled sample dashboard: ' + d1[3]);
    await textScan(p, '[login dash]');
    const dtext = await p.evaluate(() => document.body.innerText);
    check(!/\d+(\.\d+)?\s?%/.test(dtext), '[login dash] no percentage performance claims on the dashboard');
    await p.click('button[onclick*="stReel18"]'); await p.waitForTimeout(300);
    const ap = await p.evaluate(() => { const b = document.querySelector('button[onclick*="stReel18"]'); const s = document.getElementById('stReel18'); return [s.textContent.trim(), s.className, b.disabled, b.textContent.trim()]; });
    check(ap[0] === 'Approved ✓' && /st-ready/.test(ap[1]) && ap[2] && ap[3] === 'Approved', '[login] Approve marks the Reel approved and disables the button: ' + JSON.stringify(ap));
    await roundTrip(p, '[login dash, after approve]');
    // brief -> WhatsApp
    const url = await p.evaluate(() => { let u = null; const o = window.open; window.open = (x) => { u = String(x); return null; }; document.getElementById('briefTopic').value = 'drive.google.com/test-clip'; document.getElementById('briefNotes').value = 'Hindi captions'; document.querySelector('form.brief button[type=submit]').click(); window.open = o; return u; });
    check(!!url && url.startsWith('https://wa.me/918112859437?text=') && decodeURIComponent(url).includes('drive.google.com/test-clip') && decodeURIComponent(url).includes('Hindi captions'), '[login] submitClientBrief opens wa.me/918112859437 with the brief: ' + (url || 'none').slice(0, 70));
    await overflow(p, '[login dash]');
    await navFit(p, '[login dash]');
    await p.evaluate(() => logoutClient()); await p.waitForTimeout(300);
    const lo = await p.evaluate(() => [!document.getElementById('authSection').hidden, document.getElementById('dashboardSection').hidden, localStorage.getItem('vanindra_active_client')]);
    check(lo[0] && lo[1] && lo[2] === null, '[login] logout returns to sign-in and clears the saved session');
    await overflow(p, '[login auth]');
    await navFit(p, '[login auth]');
    // signup -> logout -> login by handle -> reload auto-opens
    await p.evaluate(() => localStorage.removeItem('vanindra_client_accounts'));
    await p.click('#tabSignupBtn');
    await p.fill('#regName', 'Dr. Test Sharma'); await p.fill('#regHandle', 'drtest_wellness'); await p.fill('#regPhone', '+91 90000 00000'); await p.fill('#regEmail', 'test@example.com');
    await p.selectOption('#regPlan', { index: 2 });
    await p.click('#signupForm button[type=submit]'); await p.waitForTimeout(600);
    const su = await p.evaluate(() => [document.getElementById('dashUserName').textContent, document.getElementById('dashUserHandle').textContent, document.getElementById('dashPlanName').textContent, JSON.parse(localStorage.getItem('vanindra_client_accounts') || '[]').length, document.getElementById('delivList').innerText]);
    check(su[0] === 'Dr. Test Sharma' && su[1] === '@drtest_wellness' && /Starter/.test(su[2]) && su[3] === 1 && /of 12/.test(su[4]), '[login] signup saves the account and opens a Starter workspace: ' + su.slice(0, 3).join(' / '));
    await p.evaluate(() => logoutClient());
    await p.fill('#loginId', '@drtest_wellness'); await p.click('#loginForm button[type=submit]'); await p.waitForTimeout(400);
    check(await p.evaluate(() => document.getElementById('dashUserName').textContent === 'Dr. Test Sharma'), '[login] login with the saved handle finds the account');
    await p.reload({ waitUntil: 'load' }); await p.waitForTimeout(500);
    check(await p.evaluate(() => !document.getElementById('dashboardSection').hidden && document.getElementById('dashUserName').textContent === 'Dr. Test Sharma'), '[login] saved session auto-opens on reload');
    await p.evaluate(() => logoutClient());
    await p.fill('#loginId', 'unknown@gmail.com'); await p.click('#loginForm button[type=submit]'); await p.waitForTimeout(300);
    check(await p.evaluate(() => document.getElementById('dashUserName').textContent === 'unknown' && document.getElementById('toast').classList.contains('on')), '[login] unknown login opens a sample workspace and says so');
    // theme persistence (shared key)
    await p.evaluate(() => toggleSurfaceTheme()); await p.waitForTimeout(900);
    const th = await p.evaluate(() => [document.body.classList.contains('dark-studio'), localStorage.getItem('vanindra_theme')]);
    check(th[0] && th[1] === 'dark', '[login] Dark Studio Mode toggles and saves vanindra_theme ' + JSON.stringify(th));
    await c.close();
    // dark preference set elsewhere (homepage) is honoured
    const c2 = await ctxFor(); await c2.addInitScript(() => { try { if (!sessionStorage.getItem('x')) { localStorage.setItem('vanindra_theme', 'dark'); sessionStorage.setItem('x', 1); } } catch (e) {} });
    const p2 = await open(c2, PAGES.login, 'login-dark');
    check(await p2.evaluate(() => document.body.classList.contains('dark-studio')), '[login] honours vanindra_theme=dark from the homepage');
    await c2.close();
  }
  /* ===== LOGIN: phone ===== */
  {
    const c = await ctxFor({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const p = await open(c, PAGES.login, 'login-mobile');
    await p.touchscreen.tap(200, 400); await p.waitForTimeout(100);
    await mobileAudit(p, '[login auth 390]');
    check(await p.evaluate(() => { const a = document.querySelector('.nav a.nav-wa'); if (!a) return false; const r = a.getBoundingClientRect(); return r.width >= 44 && r.height >= 44 && /wa\.me\/918112859437/.test(a.href) && !!a.querySelector('use[href="#icon-whatsapp"]'); }), '[login 390] phone nav keeps a 44 px WhatsApp button with the official logo');
    await p.evaluate(() => demoLogin()); await p.waitForTimeout(1300);
    await mobileAudit(p, '[login dash 390]');
    await c.close();
  }
  /* ===== LOGIN: reduced motion + no JS ===== */
  {
    const c = await ctxFor({ reducedMotion: 'reduce' }); const p = await open(c, PAGES.login, 'login-rm');
    await p.mouse.move(400, 400, { steps: 5 }); await p.waitForTimeout(400);
    const rm = await p.evaluate(() => [document.documentElement.classList.contains('mc-on'), !!document.querySelector('.mc-fx'), Math.min(...[...document.querySelectorAll('.en,.en-3d')].filter((e) => e.offsetParent).map((e) => +getComputedStyle(e).opacity)), getComputedStyle(document.querySelector('.orb')).animationName]);
    check(!rm[0] && !rm[1] && rm[2] === 1 && rm[3] === 'none', `[login] reduced motion: no cursor/trail, content fully visible, orb still (${JSON.stringify(rm)})`);
    await c.close();
    const c3 = await ctxFor({ javaScriptEnabled: false }); const p3 = await open(c3, PAGES.login, 'login-nojs');
    const nj = await p3.evaluate(() => { const card = document.getElementById('authCard'); const r = card.getBoundingClientRect(); const wa = [...card.querySelectorAll('a[href*="wa.me"]')].filter((a) => a.getBoundingClientRect().height > 0); return [r.height > 200, wa.length, document.getElementById('dashboardSection').hidden, getComputedStyle(document.querySelector('.auth-forms')).display, +getComputedStyle(card.closest('.card-en')).opacity]; });
    check(nj[0] && nj[1] >= 1 && nj[2] && nj[3] === 'none' && nj[4] === 1, `[login] no-JS: sign-in panel visible with a WhatsApp link, dead forms hidden (${JSON.stringify(nj)})`);
    await c3.close();
  }

  /* ===== STUDIO ===== */
  {
    const c = await ctxFor(); const p = await open(c, PAGES.studio, 'studio');
    const fns = await p.evaluate(() => ['clearPhoto', 'downloadThumbnail', 'handleImageUpload', 'renderThumbnail'].filter((f) => typeof window[f] !== 'function'));
    check(fns.length === 0, '[studio] 4 studio functions callable');
    await textScan(p, '[studio]');
    await roundTrip(p, '[studio]');
    const blank = await p.evaluate(() => document.getElementById('thumbCanvas').toDataURL().length);
    await p.setInputFiles('#bgUpload', PHOTO);
    await p.waitForFunction(() => window.uploadedImg && uploadedImg.complete, null, { timeout: 5000 }).catch(() => {});
    await p.waitForTimeout(300);
    const withPhoto = await p.evaluate(() => [!!window.uploadedImg, document.getElementById('thumbCanvas').toDataURL().length, document.getElementById('dropTitle').textContent]);
    check(withPhoto[0] && withPhoto[1] !== blank, `[studio] photo upload renders into the canvas (${withPhoto[2]})`);
    await p.fill('#hookLine1', 'STOP POSTING THIS'); await p.fill('#hookLine2', 'do this instead');
    const themes = await p.evaluate(() => { const out = []; for (const b of document.querySelectorAll('.swatch')) { b.click(); out.push([document.getElementById('themeSelect').value, b.getAttribute('aria-checked')]); } return out; });
    check(themes.length === 4 && themes.every((t) => t[1] === 'true') && new Set(themes.map((t) => t[0])).size === 4, '[studio] 4 look swatches drive the theme: ' + themes.map((t) => t[0]).join(', '));
    const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#btnDownload')]);
    const out = path.join(dir, 'qa', '_verify_download.png'); await dl.saveAs(out);
    const buf = fs.readFileSync(out);
    const isPng = buf.slice(1, 4).toString() === 'PNG', w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
    check(isPng && w === 1080 && h === 1920 && dl.suggestedFilename() === 'VanIndra_Creations_Reel_Cover_1080x1920.png', `[studio] download produces ${dl.suggestedFilename()} PNG ${w}×${h}`);
    await p.click('#btnClearPhoto'); await p.waitForTimeout(150);
    check(await p.evaluate(() => uploadedImg === null && document.getElementById('bgUpload').value === ''), '[studio] Clear photo resets the photo');
    await p.mouse.move(200, 200, { steps: 4 }); await p.mouse.move(600, 500, { steps: 4 });
    const fi = await p.$('#topBadge'); const fb = await fi.boundingBox(); await p.mouse.move(fb.x + 30, fb.y + 10, { steps: 4 }); await p.waitForTimeout(200);
    check(await p.evaluate(() => document.querySelector('.mc-layer').dataset.s === 'native' && getComputedStyle(document.getElementById('topBadge')).cursor !== 'none'), '[studio] text inputs keep the native caret under the custom cursor');
    await overflow(p, '[studio]');
    await navFit(p, '[studio]');
    await c.close();
    const cm = await ctxFor({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const pm = await open(cm, PAGES.studio, 'studio-mobile');
    await mobileAudit(pm, '[studio 390]');
    const ord = await pm.evaluate(() => [document.getElementById('hookLine1').getBoundingClientRect().top + scrollY, document.getElementById('thumbCanvas').getBoundingClientRect().top + scrollY]);
    check(ord[0] < ord[1], `[studio 390] controls come before the full preview (hook y=${Math.round(ord[0])}, canvas y=${Math.round(ord[1])})`);
    await pm.evaluate(() => document.getElementById('hookLine1').scrollIntoView({ block: 'center' }));
    await pm.tap('#hookLine1'); await pm.waitForTimeout(700);
    await pm.keyboard.type('NEW HOOK', { delay: 20 }); await pm.waitForTimeout(500);
    const dk = await pm.evaluate(() => {
      const d = document.getElementById('pvDock'), r = d.getBoundingClientRect(), cs = getComputedStyle(d), h = document.getElementById('hookLine1').getBoundingClientRect();
      const px = document.getElementById('dockCanvas').getContext('2d').getImageData(100, 120, 1, 1).data;
      const over = !(h.right < r.left || h.left > r.right || h.bottom < r.top || h.top > r.bottom);
      return [d.classList.contains('on'), cs.visibility, +cs.opacity, Math.round(r.top), Math.round(r.bottom), innerHeight, px[3], over, Math.round(r.width), Math.round(r.height)];
    });
    check(dk[0] && dk[1] === 'visible' && dk[2] > 0.9 && dk[4] <= dk[5] && dk[3] > 60 && dk[6] > 0 && !dk[7] && dk[8] >= 44 && dk[9] >= 44, `[studio 390] while typing a hook, the mini live cover is pinned on screen, drawn, and does not cover the field (${JSON.stringify(dk)})`);
    await pm.tap('#pvDock'); await pm.waitForTimeout(1200);
    const dk2 = await pm.evaluate(() => { const r = document.getElementById('thumbCanvas').getBoundingClientRect(), b = document.getElementById('btnDownload').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom), Math.round(b.bottom), innerHeight, document.getElementById('pvDock').classList.contains('on'), document.activeElement && document.activeElement.id]; });
    check(dk2[0] >= 0 && dk2[0] < dk2[3] && dk2[4] === false && dk2[5] === 'btnDownload', `[studio 390] tapping the mini cover brings the full preview into view and focuses Download (${JSON.stringify(dk2)})`);
    await cm.close();
    const cr = await ctxFor({ reducedMotion: 'reduce' }); const pr = await open(cr, PAGES.studio, 'studio-rm');
    await pr.mouse.move(500, 500, { steps: 4 });
    check(await pr.evaluate(() => !document.documentElement.classList.contains('mc-on') && Math.min(...[...document.querySelectorAll('.en,.en-3d')].map((e) => +getComputedStyle(e).opacity)) === 1), '[studio] reduced motion: no custom cursor, everything visible');
    await cr.close();
    const cn = await ctxFor({ javaScriptEnabled: false }); const pn = await open(cn, PAGES.studio, 'studio-nojs');
    const nj = await pn.evaluate(() => [document.body.innerText.includes('The cover studio needs JavaScript'), getComputedStyle(document.querySelector('.studio-app')).display, !!document.querySelector('.nojs-card a[href*="wa.me/918112859437"]')]);
    check(nj[0] && nj[1] === 'none' && nj[2], '[studio] no-JS shows a clear message + WhatsApp link instead of a dead app');
    await cn.close();
  }

  check(errors.length === 0, 'no page errors or console errors' + (errors.length ? ': ' + errors.slice(0, 5).join(' | ') : ''));
  check(foreign.size === 0, 'no network requests except Google Fonts' + (foreign.size ? ': ' + [...foreign].join(', ') : ''));
  check(missing.size === 0, 'no missing local files' + (missing.size ? ': ' + [...missing].join(', ') : ''));
  try { fs.unlinkSync(path.join(dir, 'qa', '_verify_download.png')); } catch (e) {}
  console.log(`PASS ${ok.length}  WARN ${warns.length}  FAIL ${fails.length}`);
  if (warns.length) console.log('WARN:\n  ' + warns.join('\n  '));
  if (fails.length) console.log('FAIL:\n  ' + fails.join('\n  '));
  if (process.env.VERBOSE) console.log('PASS:\n  ' + ok.join('\n  '));
  await b.close(); server.close(); process.exit(fails.length ? 1 : 0);
});
