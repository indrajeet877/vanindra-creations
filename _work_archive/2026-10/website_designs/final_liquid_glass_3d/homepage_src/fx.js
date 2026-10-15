/* =========================================================
   FX LAYER · glass halo, glass thickness, magic cursor, cinematic motion.
   Every block is feature-checked and wrapped in try/catch: the page works without any of it.
   One shared requestAnimationFrame loop; it sleeps when nothing moves, off-screen or in a hidden tab.
   prefers-reduced-motion: no intro, no smooth scroll, no parallax, no cursor, no trail.
   ========================================================= */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement, body = doc.body, W = window;
  var mm = function (q) { return !!(W.matchMedia && W.matchMedia(q).matches); };
  var RM = mm('(prefers-reduced-motion: reduce)');
  var FINE = mm('(hover: hover) and (pointer: fine)');
  var PHONE = mm('(max-width: 768px)') || mm('(pointer: coarse)');
  var DESKQ = W.matchMedia ? W.matchMedia('(min-width: 900px)') : { matches: true };
  var DESK_FX = FINE && !PHONE && !RM;
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var now = function () { return W.performance ? performance.now() : Date.now(); };
  var canAnim = !!(W.Element && Element.prototype.animate);
  var FX = W.FX = { lang: 'en', ptr: { x: innerWidth / 2, y: innerHeight * 0.4, nx: 0, ny: 0, t: 0 }, tilt: { x: 0, y: 0 } };
  function safe(name, fn) { try { fn(); } catch (e) { try { console.warn('[fx] ' + name + ' off: ' + (e && e.message)); } catch (_) {} } }
  var $$ = function (s, c) { return [].slice.call((c || doc).querySelectorAll(s)); };

  /* ---------- one rAF loop; each ticker returns true while it still needs frames ---------- */
  var tickers = [], running = false;
  function loop(t) {
    if (doc.hidden) { running = false; return; }
    var more = false;
    for (var i = 0; i < tickers.length; i++) { try { if (tickers[i](t)) more = true; } catch (e) { tickers.splice(i--, 1); } }
    if (more) requestAnimationFrame(loop); else running = false;
  }
  function kick() { if (!running && !doc.hidden) { running = true; requestAnimationFrame(loop); } }
  FX.kick = kick;
  FX.running = function () { return running; };
  doc.addEventListener('visibilitychange', function () { if (!doc.hidden) kick(); });

  W.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'touch' || doc.hidden) return;
    var p = FX.ptr; p.x = e.clientX; p.y = e.clientY; p.t = now();
    p.nx = clamp((p.x / innerWidth) * 2 - 1, -1, 1); p.ny = clamp((p.y / innerHeight) * 2 - 1, -1, 1);
    kick();
  }, { passive: true });
  W.addEventListener('pointerdown', function (e) { FX.ptr.x = e.clientX; FX.ptr.y = e.clientY; FX.ptr.t = now(); }, { passive: true, capture: true });

  /* ---------- 1. ripples + sparkle bursts (all devices; none with reduced motion) ---------- */
  safe('sparks', function () {
    var live = 0;
    FX.ripple = function (x, y) {
      if (RM || live > 4 || !canAnim) return;
      var r = doc.createElement('span'); r.className = 'fx-ripple'; r.setAttribute('aria-hidden', 'true'); r.style.left = x + 'px'; r.style.top = y + 'px'; body.appendChild(r); live++;
      var a = r.animate([{ transform: 'scale(.12)', opacity: 0.95 }, { transform: 'scale(1)', opacity: 0 }], { duration: 620, easing: 'cubic-bezier(.16,1,.3,1)' });
      a.onfinish = function () { live--; r.remove(); };
    };
    FX.burst = function (x, y, n) {
      if (RM || !canAnim) return;
      if (!(x > 0 && y > 0)) { x = innerWidth / 2; y = innerHeight / 2; }
      n = Math.min(n || 16, PHONE ? 12 : 22);
      for (var i = 0; i < n; i++) (function (i) {
        var s = doc.createElement('span'); s.className = 'fx-spark'; s.setAttribute('aria-hidden', 'true'); s.style.left = x + 'px'; s.style.top = y + 'px'; body.appendChild(s);
        var a = (i / n) * Math.PI * 2 + Math.random() * 0.5, d = 38 + Math.random() * 70, sz = 0.55 + Math.random() * 1.05;
        var an = s.animate([{ transform: 'translate(0,0) scale(' + sz.toFixed(2) + ') rotate(0deg)', opacity: 1 }, { transform: 'translate(' + (Math.cos(a) * d).toFixed(1) + 'px,' + (Math.sin(a) * d + 18).toFixed(1) + 'px) scale(0) rotate(' + (Math.random() * 180 - 90).toFixed(0) + 'deg)', opacity: 0 }], { duration: 780 + Math.random() * 420, easing: 'cubic-bezier(.2,.7,.2,1)' });
        an.onfinish = function () { s.remove(); };
      })(i);
    };
    // where did the action come from? the pointer if it was just used, else the focused control
    FX.here = function () {
      var p = FX.ptr; if (now() - p.t < 1500) return [p.x, p.y];
      var a = doc.activeElement; if (a && a !== body && a.getBoundingClientRect) { var r = a.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }
      return [innerWidth / 2, innerHeight / 2];
    };
    // touch: a soft gold ring where you tap
    if (!FINE) doc.addEventListener('click', function (e) { if ((e.clientX || e.clientY) && e.pointerType !== 'mouse') FX.ripple(e.clientX, e.clientY); }, { passive: true, capture: true });
  });

  /* ---------- 2. hooks into the page's own functions (names and behaviour kept) ---------- */
  safe('hooks', function () {
    var slm = W.setLanguageMode;
    if (typeof slm === 'function') W.setLanguageMode = function (lang) {
      try { if (FX.unsplitAll) FX.unsplitAll(); if (FX.finishCounters) FX.finishCounters(); } catch (e) {}
      var r = slm.apply(this, arguments);
      FX.lang = lang === 'hi' ? 'hi' : 'en';
      try { localStorage.setItem('vanindra_lang', FX.lang); } catch (e) {}
      try { if (FX.onLang) FX.onLang(); } catch (e) {}
      return r;
    };
    var tst = W.toggleSurfaceTheme;
    if (typeof tst === 'function') W.toggleSurfaceTheme = function () {
      var self = this, args = arguments;
      var done = function () { try { if (FX.onTheme) FX.onTheme(); } catch (e) {} };
      if (RM || !doc.startViewTransition) { var r0 = tst.apply(self, args); done(); return r0; }
      var h = FX.here(), x = h[0], y = h[1];
      var vt = doc.startViewTransition(function () { tst.apply(self, args); done(); });
      vt.ready.then(function () {
        var rad = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
        root.animate({ clipPath: ['circle(0px at ' + x + 'px ' + y + 'px)', 'circle(' + rad + 'px at ' + x + 'px ' + y + 'px)'] }, { duration: 700, easing: 'cubic-bezier(.65,0,.35,1)', pseudoElement: '::view-transition-new(root)' });
      }).catch(function () {});
    };
    // magic moment: a soft gold sparkle whenever a WhatsApp message is sent
    ['openElegantWhatsAppDirect', 'sendZeroTouchWhatsApp'].forEach(function (name) {
      var f = W[name]; if (typeof f !== 'function') return;
      W[name] = function () { try { var h = FX.here(); FX.burst(h[0], h[1], 18); if (!RM && navigator.vibrate) navigator.vibrate(8); } catch (e) {} return f.apply(this, arguments); };
    });
    // magic moment: the AI plan finishes
    var ai = W.runZeroTouchBackgroundAI;
    if (typeof ai === 'function') W.runZeroTouchBackgroundAI = function () {
      var p = ai.apply(this, arguments);
      Promise.resolve(p).then(function () {
        var o = doc.getElementById('ztOutputPanel'); if (!o || !o.classList.contains('active')) return;
        setTimeout(function () { var r = o.getBoundingClientRect(); FX.burst(r.left + r.width / 2, clamp(r.top + 40, 40, innerHeight - 40), 24); o.classList.remove('fx-glow'); void o.offsetWidth; o.classList.add('fx-glow'); }, 450);
      }).catch(function () {});
      return p;
    };
    // the hero phone polishes with a light sweep on every Before/After change
    var sps = W.switchPhoneSimulation;
    if (typeof sps === 'function') W.switchPhoneSimulation = function (mode) {
      var prev = W.currentPhoneMode, r = sps.apply(this, arguments);
      try { if (FX.onMode) FX.onMode(mode, prev); } catch (e) {}
      return r;
    };
    var pv = W.playVandanaViralReel, cv = W.closeVandanaViralReel;
    if (typeof pv === 'function') W.playVandanaViralReel = function () { if (FX.lenis) FX.lenis.stop(); return pv.apply(this, arguments); };
    if (typeof cv === 'function') W.closeVandanaViralReel = function () { if (FX.lenis) FX.lenis.start(); return cv.apply(this, arguments); };
  });
  // a Hindi reader's choice is remembered between visits (English stays the default for everyone else)
  safe('lang', function () { var l = null; try { l = localStorage.getItem('vanindra_lang'); } catch (e) {} if (l === 'hi' && typeof W.setLanguageMode === 'function') W.setLanguageMode('hi'); });
  // the seg buttons call switchPhoneSimulation through their inline handlers, which look up the global, so the hook above catches them

  /* ---------- 3. Lenis smooth scroll (desktop, fine pointer) ---------- */
  safe('lenis', function () {
    if (!DESK_FX || !W.Lenis) return;
    var lenis = new W.Lenis({ lerp: 0.1, smoothWheel: true, wheelMultiplier: 1, prevent: function (n) { return !!(n.closest && n.closest('.ai-pre, .player, textarea, select, .nav-sheet')); } });
    FX.lenis = lenis;
    doc.addEventListener('click', function (e) {
      var a = e.target && e.target.closest && e.target.closest('a[href^="#"]'); if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var id = a.getAttribute('href'); if (!id || id.length < 2) return;
      var el = doc.getElementById(id.slice(1)); if (!el) return;
      e.preventDefault();
      try { history.pushState(null, '', id); } catch (er) {}
      requestAnimationFrame(function () { var sm = parseFloat(getComputedStyle(el).scrollMarginTop) || 0; var y = el.getBoundingClientRect().top + (W.scrollY || 0); lenis.scrollTo(Math.max(0, y - sm), { duration: 1.2 }); kick(); });
    });
    var idle = 0;
    tickers.push(function (t) { lenis.raf(t); if (lenis.isScrolling) idle = 0; else idle++; return idle < 30; });
    ['wheel', 'keydown', 'pointerdown', 'scroll'].forEach(function (ev) { W.addEventListener(ev, kick, { passive: true }); });
    kick();
  });

  /* ---------- 4. intro (desktop): the veil fades on its own while the wordmark flies into the nav and lands there ---------- */
  var INTRO = root.classList.contains('intro-on') && !RM;
  var entered = false;
  FX.enter = function () { if (entered) return; entered = true; if (FX._enter) FX._enter(); };
  safe('intro', function () {
    // phones: the gold shimmer over the nav wordmark ends by itself; tidy the class away
    if (root.classList.contains('wm-shimmer')) setTimeout(function () { root.classList.remove('wm-shimmer'); }, 900);
    var el = doc.getElementById('vcIntro'); if (!el) return;
    if (!INTRO) { el.parentNode.removeChild(el); return; }
    try { localStorage.setItem('vi_intro', String(Date.now())); } catch (e) {}
    var veil = el.querySelector('.intro-veil'), mark = el.querySelector('.intro-wm'), navWm = doc.querySelector('.nav .wm');
    var gone = false, timers = [], E = 'cubic-bezier(.4,0,.2,1)';
    var navAnim = null;
    var end = function () { if (gone === 'done') return; gone = 'done'; timers.forEach(clearTimeout); if (el.parentNode) el.parentNode.removeChild(el); root.classList.remove('intro-on'); if (navAnim) try { navAnim.cancel(); } catch (e) {} FX.introDone = true; FX.enter(); };
    // fade from whatever opacity is showing now (never restart from 1, so the veil can never flash back)
    var fade = function (node, ms, delay) { if (!node || !canAnim) return; var o = getComputedStyle(node).opacity; node.animate([{ opacity: o }, { opacity: 0 }], { duration: ms, delay: delay || 0, easing: E, fill: 'forwards' }); };
    var evs = ['pointerdown', 'keydown', 'wheel', 'touchstart'];
    var skip = function () {
      if (gone) return; gone = true; timers.forEach(clearTimeout); evs.forEach(function (ev) { W.removeEventListener(ev, skip, true); });
      if (parseFloat(getComputedStyle(el).opacity) < 0.98 || !canAnim) return end();
      FX.enter(); fade(el, 200); if (navWm && canAnim) navAnim = navWm.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, easing: E, fill: 'forwards' });
      timers.push(setTimeout(end, 210));
    };
    evs.forEach(function (ev) { W.addEventListener(ev, skip, { capture: true, passive: true }); });
    // the timeline starts at the first rendered frame (not at script time), so a slow first paint never skips the wordmark
    var at = function (fn, ms) { requestAnimationFrame(function () { requestAnimationFrame(function () { timers.push(setTimeout(fn, ms)); }); }); };
    at(function () {
      if (gone) return; gone = 'flying';
      if (parseFloat(getComputedStyle(el).opacity) < 0.98 || !canAnim || !mark || !navWm) return end(); // the CSS fail-safe already took it
      var a = mark.getBoundingClientRect(), b = (navWm.querySelector('.wm-name') || navWm).getBoundingClientRect(), s = b.height / a.height;
      var dx = (b.left + b.width / 2) - (a.left + a.width / 2), dy = (b.top + b.height / 2) - (a.top + a.height / 2);
      // only the mark travels: CREATIONS, the hairline and the panes leave in the first 200 ms
      [].forEach.call(el.querySelectorAll('.intro-line,.intro-sub,.intro-panes,.intro-glint'), function (x) { fade(x, 200); });
      mark.animate([{ transform: 'none' }, { transform: 'translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px) scale(' + s.toFixed(3) + ')' }], { duration: 560, easing: 'cubic-bezier(.7,0,.2,1)', fill: 'forwards' });
      FX.enter();                      // the hero entrance is set up first (its hidden start states apply at once) ...
      fade(veil, 420, 120);            // ... then the ivory veil leaves on its own
      // the last 100 ms of the flight: the nav wordmark fades in exactly where the mark lands, the mark fades out
      timers.push(setTimeout(function () {
        if (gone === 'done') return;
        fade(mark, 100);
        navAnim = navWm.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 100, easing: 'linear', fill: 'forwards' });
      }, 460));
      timers.push(setTimeout(end, 580));
    }, 720);
    setTimeout(function () { if (!FX.introDone) end(); }, 2600); // belt and braces
  });

  /* ---------- word splitting (word level only, so Devanagari is never broken), always reverted ---------- */
  var splits = [];
  function splitWords(el, emUnit) {
    if (!el || el._fxOrig != null) return [];
    var orig = el.innerHTML, words = [];
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var parts = ch.nodeValue.split(/(\s+)/); if (parts.length < 2 && !ch.nodeValue.trim()) return;
          var frag = doc.createDocumentFragment();
          parts.forEach(function (p) { if (!p) return; if (/^\s+$/.test(p)) frag.appendChild(doc.createTextNode(p)); else { var s = doc.createElement('span'); s.className = 'fxw'; s.textContent = p; frag.appendChild(s); words.push(s); } });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1 && ch.tagName !== 'BR') {
          var cs = getComputedStyle(ch);
          if ((emUnit && ch.tagName === 'EM') || /text/.test(cs.backgroundClip || cs.webkitBackgroundClip || '') || ch.tagName === 'MARK') { var wr = doc.createElement('span'); wr.className = 'fxw' + (emUnit && ch.tagName === 'EM' ? ' fx-unit' : ''); node.replaceChild(wr, ch); wr.appendChild(ch); words.push(wr); }
          else walk(ch);
        }
      });
    })(el);
    words.forEach(function (w, i) { w.style.setProperty('--i', i); });
    el._fxOrig = orig; splits.push(el);
    return words;
  }
  function unsplit(el) {
    if (!el || el._fxOrig == null) return;
    el.innerHTML = el._fxOrig; el._fxOrig = null; el.classList.remove('fx-split');
    var i = splits.indexOf(el); if (i >= 0) splits.splice(i, 1);
  }
  FX.unsplitAll = function () { splits.slice().forEach(unsplit); };

  /* ---------- 5. hero entrance + the raw clip polishing into the finished edit ---------- */
  FX.t0 = INTRO ? 0.84 : 0.06;
  safe('hero', function () {
    var hero = doc.getElementById('hero'); if (!hero) return;
    var stage = doc.getElementById('heroStage'), phone = doc.getElementById('phoneBody'), pw = doc.getElementById('iphone3D');
    var screen = doc.getElementById('phoneScreen');
    if (screen) { var sh = doc.createElement('i'); sh.className = 'fx-sheen'; sh.setAttribute('aria-hidden', 'true'); screen.appendChild(sh); }
    FX.polish = function () { if (!phone || RM) return; phone.classList.remove('fx-polish'); void phone.offsetWidth; phone.classList.add('fx-polish'); };
    var ease = 'cubic-bezier(.16,1,.3,1)', K = PHONE ? 0.8 : 1; // phones: a shorter entrance
    var inView = function (el) { var r = el.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; };
    var anim = function (el, from, delay, dur) { if (!el || !canAnim || !inView(el)) return null; return el.animate([from, { opacity: 1, transform: 'none' }], { duration: (dur || 800) * K, delay: delay * K, easing: ease, fill: 'backwards' }); };
    var h1 = doc.getElementById('heroMainTitle'), ws = [];
    // split now (before first paint), animate when the entrance starts; until then the words are simply visible
    if (!RM && canAnim && h1 && inView(h1)) ws = splitWords(h1, FX.lang !== 'hi');
    var entranceAt = 0;
    FX._enter = function () {
      entranceAt = now();
      if (RM || !canAnim) return;
      anim(hero.querySelector('.eyebrow'), { opacity: 0.001, transform: 'translate3d(0,10px,0)' }, 0, 700);
      if (ws.length) {
        // per word: rise .42em and fade in, 720 ms, 55 ms apart; "everything else." lands as one unit 140 ms after the last word
        var last = null, n = ws.length, d = 0;
        ws.forEach(function (w, i) { d = w.classList.contains('fx-unit') ? (i - 1) * 55 + 140 : i * 55; last = w.animate([{ opacity: 0.001, transform: 'translate3d(0,.42em,0)' }, { opacity: 1, transform: 'none' }], { duration: 720 * K, delay: d * K, easing: ease, fill: 'backwards' }); });
        var fin = function () { unsplit(h1); };
        if (last) last.onfinish = fin;
        setTimeout(fin, 2200);
      }
      anim(doc.getElementById('heroSubTitle'), { opacity: 0.001, transform: 'translate3d(0,14px,0)' }, 180, 760);
      $$('.hero-head .cta-row > *').forEach(function (b, i) { anim(b, { opacity: 0.001, transform: 'translate3d(0,16px,0) scale(.97)' }, 260 + i * 40, 720); });
      anim(hero.querySelector('.hero-head .micro'), { opacity: 0.001, transform: 'translate3d(0,8px,0)' }, 340, 680);
      anim(hero.querySelector('.seg'), { opacity: 0.001, transform: 'translate3d(0,12px,0)' }, 300, 720);
      anim(pw, { opacity: 0.001, transform: 'perspective(1400px) translate3d(0,70px,-60px) rotateX(12deg)' }, 320, 900);
      anim(hero.querySelector('.concierge'), { opacity: 0.001, transform: 'translate3d(-22px,20px,0)' }, 380, 820);
      anim(hero.querySelector('.changes'), { opacity: 0.001, transform: 'translate3d(22px,20px,0)' }, 420, 820);
      if (FX.onEnter) FX.onEnter();
    };
    if (!INTRO) FX.enter(); else setTimeout(FX.enter, 2400); // safety: the entrance always starts
    // raw clip -> polished edit, once (a visual demo; the page text never changes). The raw look is never on screen for more than 1.2 s.
    if (!stage || RM || stage.dataset.mode !== 'after' || !('IntersectionObserver' in W)) return;
    stage.classList.add('fx-raw');
    var done = false, cap = 0, tmr = 0;
    FX.finishRaw = function (animate) {
      if (done) return; done = true; clearTimeout(tmr); clearTimeout(cap); io.disconnect();
      stage.classList.remove('fx-raw');
      if (animate) { FX.polish(); if (FX.halo) FX.halo.sweep(); }
      if (FX.halo) FX.halo.mode();
    };
    var play = function (ms) { if (!done && !tmr) tmr = setTimeout(function () { FX.finishRaw(true); }, ms); };
    // desktop: the phone is on the first screen, so it polishes 450 ms after the phone starts rising
    FX.onEnter = function () { if (!PHONE && inView(pw)) play(320 + 450); };
    if (entered) FX.onEnter();
    var io = new IntersectionObserver(function (en) {
      var e = en[0];
      if (e.isIntersecting) {
        if (!cap) cap = setTimeout(function () { FX.finishRaw(true); }, 1200);
        if (e.intersectionRatio >= 0.4 && entranceAt) play(PHONE ? 350 : 450);
      } else if (cap && !done) FX.finishRaw(false); // scrolled away before the demo played: show the finished edit, never leave it raw
    }, { threshold: [0, 0.4] });
    io.observe(pw || stage);
  });
  FX.onMode = function (mode, prev) {
    if (FX.finishRaw) FX.finishRaw(false);
    if (mode !== prev) { if (FX.polish) FX.polish(); if (FX.halo) FX.halo.sweep(); }
    if (FX.halo) FX.halo.mode();
  };

  /* ---------- 6. the 3D glass orbit round the phone (WebGL) ---------- */
  safe('halo', function () {
    var box = doc.querySelector('.gl3d'), back = doc.querySelector('.gl3d-back'), cv = box && box.querySelector('canvas'), pw = doc.getElementById('iphone3D'), phone = doc.getElementById('phoneBody');
    var stage = doc.getElementById('heroStage'), hero = doc.getElementById('hero');
    if (!cv || !pw || typeof createGlassHalo !== 'function' || typeof fitGlassPose !== 'function' || !W.WebGLRenderingContext) return;
    // W.__fxForceGL is only set by our own capture scripts (this sandbox has no GPU); real visitors never set it
    var FORCE = W.__fxForceGL === true, nav = navigator, conn = nav.connection || {};
    if (!FORCE && ((nav.deviceMemory && nav.deviceMemory <= 3) || (nav.hardwareConcurrency && nav.hardwareConcurrency <= 2) || conn.saveData === true)) return; // the still stays
    var P0 = 0.85, fit = fitGlassPose(P0), DPR = Math.min(W.devicePixelRatio || 1, 2);
    var g = null, gl = null, soft = false, started = false, near = false, loaded = doc.readyState === 'complete';
    var visible = false, dead = false, scale = 1, cap = PHONE ? 33 : 0, frozen = false, level = 0;
    var cur = { yaw: 0, pitch: P0, warm: 1, disp: 1, lx: -0.35, ly: 0.62, dark: 0 }, tgt = { warm: 1, disp: 1 };
    var frames = 0, last = 0, phase = 0, lastScroll = 0, sweepT = -1, prevDraw = 0, samples = [], demandUntil = 0, lastScrollAt = 0, heroH = 900, liveAt = 0, S = null;
    var userScrolled = false, lastTouch = 0, phR = null, idleOK = false;
    function want(ms) { demandUntil = Math.max(demandUntil, now() + ms); kick(); }
    function readMode() { var raw = stage && stage.classList.contains('fx-raw'), m = W.currentPhoneMode; tgt.warm = raw ? 0.15 : m === 'before' ? 0.22 : 1; tgt.disp = raw || m === 'before' ? 0.45 : 1; }
    var setOn = function (on) { box.classList.toggle('on', on); if (back) back.classList.toggle('on', on); };
    FX.halo = {
      mode: function () { readMode(); want(PHONE ? 1800 : 2200); if (g && (RM || frozen)) draw(now()); },
      sweep: function () { sweepT = now(); want(1800); },
      kick: function () { want(PHONE ? 600 : 1200); }
    };
    FX.haloInfo = function () { return { frames: frames, started: started, soft: soft, forced: FORCE, level: level, scale: scale, cap: cap, frozen: frozen, px: g ? g.size() : [0, 0], css: [box.clientWidth, box.clientHeight], visible: visible, dead: dead }; };
    // the canvas follows its CSS box (CSS sizes and places the orbit, so the no-JS still sits in the same place)
    function size() {
      var w = box.clientWidth, h = box.clientHeight; if (!w || !h) return;
      if (g && g.resize(w * DPR * scale, h * DPR * scale)) { phR = null; if (!dead) draw(now()); } // a resize clears the canvas: redraw at once
    }
    // the phone's rounded rect in canvas pixels (bottom-left origin), so the far half of the orbit passes behind it
    function phoneRect() {
      if (!phone || !g) return;
      var b = box.getBoundingClientRect(), r = phone.getBoundingClientRect(), sz = g.size(), kx = sz[0] / (b.width || 1), ky = sz[1] / (b.height || 1);
      var rad = (parseFloat(getComputedStyle(phone).borderTopLeftRadius) || 40) * kx;
      S.ph = [(r.left - b.left - 0.5) * kx, (b.bottom - r.bottom - 0.5) * ky, (r.right - b.left + 0.5) * kx, (b.bottom - r.top + 0.5) * ky]; S.phr = rad;
      phR = true;
    }
    var STEPS;
    function setLevel(l) { level = l; var st = STEPS[l - 1]; if (!st) return; if (st[0] === 'cap') cap = st[1]; else if (st[0] === 'scale') scale = Math.max(st[1], 1 / DPR); else frozen = true; size(); }
    function draw(t) {
      if (dead || !g) return;
      var dt = last ? Math.min((t - last) / 1000, 0.1) : 0.016; last = t;
      var k = 1 - Math.exp(-dt * 3), p = FX.ptr, tl = FX.tilt, sc = W.scrollY || 0;
      var hp = clamp(sc / Math.max(1, heroH), 0, 1);
      var sx = RM ? 0 : (PHONE ? tl.x * 0.3 : p.nx * 0.2), sy = RM ? 0 : (PHONE ? tl.y * 0.16 : p.ny * 0.1);
      cur.yaw += (sx - cur.yaw) * k; cur.pitch += (P0 + sy + (RM ? 0 : hp * 0.2) - cur.pitch) * k;
      cur.warm += (tgt.warm - cur.warm) * k * 0.9; cur.disp += (tgt.disp - cur.disp) * k;
      cur.lx += ((-0.35 + (PHONE ? tl.x : p.nx) * 0.9) - cur.lx) * k; cur.ly += ((0.62 - (PHONE ? tl.y : p.ny) * 0.6) - cur.ly) * k;
      cur.dark = body.classList.contains('dark-studio') ? 1 : 0;
      if (!RM) phase += dt * 0.16 + (sc - lastScroll) * 0.0016;
      lastScroll = sc;
      if (!PHONE || !phR) phoneRect();
      S.yaw = cur.yaw; S.pitch = cur.pitch; S.warm = cur.warm; S.disp = cur.disp; S.lx = cur.lx; S.ly = cur.ly; S.dark = cur.dark; S.phase = phase;
      S.sweep = sweepT > 0 && t - sweepT < 1600 ? -0.15 + (t - sweepT) / 1600 * 1.4 : -1;
      g.render(); frames++;
      if (!box.classList.contains('on')) setOn(true);
      if (back) back.style.setProperty('--cx', (cur.yaw * -60).toFixed(1));
      if (phone && !RM && !PHONE) phone.style.setProperty('--pe', clamp(-p.nx * 4, -5, 5).toFixed(2));
    }
    function tick(t) {
      if (dead || frozen || RM || !visible || !g) return false;
      var active = !PHONE || t < demandUntil;
      if (soft && !PHONE && t > demandUntil && t - Math.max(FX.ptr.t, lastScrollAt, sweepT, liveAt) > 8000) active = false; // software GL rests when idle
      if (!active) { prevDraw = 0; return false; }
      if (PHONE && t - lastScrollAt < 160) { prevDraw = 0; return true; } // no frames while a finger scrolls
      if (cap && t - prevDraw < cap - 3) return true;
      if (prevDraw && t - prevDraw < 250) samples.push(t - prevDraw);
      prevDraw = t; draw(t);
      if (samples.length >= 40) { samples.sort(function (a, b) { return a - b; }); var med = samples[20], budget = cap || 16.7; samples.length = 0; if (med > budget * 1.5 && level < STEPS.length) setLevel(level + 1); }
      return true;
    }
    function build() {
      g = createGlassHalo(cv, { gl: gl, nu: soft || PHONE ? 144 : 192, nv: soft || PHONE ? 20 : 24 });
      if (!g) return false;
      S = g.S; S.foc = fit.foc; S.sh = fit.sh; S.pitch = P0; S.occ = 0;
      heroH = hero ? hero.offsetHeight : 900; lastScroll = W.scrollY || 0; size(); readMode(); cur.warm = tgt.warm; cur.disp = tgt.disp;
      return true;
    }
    // one WebGL context, created after load in idle time and only near the viewport, so it never competes with the first paint or the intro.
    // Software WebGL (no GPU) is refused, so those visitors keep the identical pre-rendered still with no freeze.
    function start() {
      if (started || !loaded || !near) return;
      if (PHONE) {
        if (!idleOK && !(visible && userScrolled)) return; // phones: only once the visitor scrolls to the phone, or after 3 s of idle
        if (now() - lastTouch < 350) { setTimeout(start, 400); return; } // never in the middle of a tap
      }
      started = true;
      var ric = W.requestIdleCallback || function (f) { return setTimeout(f, 200); };
      ric(function () {
        try {
          gl = cv.getContext('webgl', { alpha: true, premultipliedAlpha: true, antialias: true, depth: true, stencil: false, powerPreference: 'default', failIfMajorPerformanceCaveat: !FORCE });
          if (!gl) return;
          try { var ex = gl.getExtension('WEBGL_debug_renderer_info'); soft = /swiftshader|llvmpipe|softpipe|software|basic render/i.test(String(gl.getParameter(ex ? ex.UNMASKED_RENDERER_WEBGL : gl.RENDERER))); } catch (e) {}
          if (soft && !FORCE) { dead = true; try { var lc = gl.getExtension('WEBGL_lose_context'); if (lc) lc.loseContext(); } catch (e) {} return; }
          if (soft) cap = 33;
          // the governor lowers the frame rate first, then the resolution (never below 1 canvas px per CSS px), then freezes
          STEPS = PHONE ? [['cap', 42], ['scale', 0.75], ['freeze']] : [['cap', 33], ['cap', 42], ['scale', 0.75], ['freeze']];
          if (!build()) return;
          cv.addEventListener('webglcontextlost', function (e) { e.preventDefault(); dead = true; setOn(false); }, false);
          cv.addEventListener('webglcontextrestored', function () { try { if (build()) { dead = false; want(1200); } } catch (er) { dead = true; setOn(false); } }, false);
          liveAt = now();
          if (RM) { draw(now()); return; }
          tickers.push(tick); if (!PHONE) { sweepT = now(); want(2400); } else want(600);
          if (PHONE && 'DeviceOrientationEvent' in W && typeof DeviceOrientationEvent.requestPermission !== 'function') {
            W.addEventListener('deviceorientation', function (e) { if (e.gamma == null) return; var tx = clamp(e.gamma / 30, -1, 1), ty = clamp(((e.beta || 45) - 45) / 30, -1, 1); if (Math.abs(tx - FX.tilt.x) + Math.abs(ty - FX.tilt.y) > 0.03) { FX.tilt.x = tx; FX.tilt.y = ty; if (visible) want(500); } }, { passive: true });
          }
        } catch (e) { dead = true; setOn(false); try { console.warn('[fx] halo off: ' + e.message); } catch (_) {} }
      }, { timeout: 1500 });
    }
    FX.onTheme = function () { want(1500); if (g && (RM || frozen)) draw(now()); };
    W.addEventListener('resize', function () { heroH = hero ? hero.offsetHeight : heroH; size(); phR = null; if (g && !dead) draw(now()); want(600); });
    var se = 0;
    W.addEventListener('scroll', function () {
      lastScrollAt = now();
      if (visible) { if (PHONE) want(700); else kick(); }
      // and one clean frame once the scroll settles (phones draw nothing while a finger moves)
      clearTimeout(se); se = setTimeout(function () { if (visible && g && !dead) { phR = null; draw(now()); } }, 180);
    }, { passive: true });
    W.addEventListener('scroll', function us() { if (W.scrollY > 4) { userScrolled = true; W.removeEventListener('scroll', us); start(); } }, { passive: true });
    ['touchstart', 'pointerdown'].forEach(function (ev) { W.addEventListener(ev, function () { lastTouch = now(); }, { passive: true, capture: true }); });
    // desktop: after the raw-to-polished demo has played; phones: as soon as the phone is near and the visitor is there (see start)
    var delay = PHONE ? 250 : (INTRO ? 2300 : 2000);
    var arm = function () {
      if (INTRO && !FX.introDone) { setTimeout(arm, 250); return; }
      setTimeout(function () { loaded = true; start(); }, INTRO ? Math.max(250, delay - 1300) : delay);
      if (PHONE) setTimeout(function () { idleOK = true; start(); }, (FX.t0 + 1.1) * 1000 + 3000);
    };
    if (!loaded) W.addEventListener('load', arm); else { loaded = false; arm(); }
    if ('IntersectionObserver' in W) new IntersectionObserver(function (en) {
      visible = en[0].isIntersecting; prevDraw = 0; last = 0;
      if (visible || en[0].boundingClientRect.top < innerHeight + 400) { near = true; start(); }
      if (visible) want(PHONE ? 600 : 2000);
    }, { rootMargin: '400px 0px' }).observe(box);
    else { near = visible = true; start(); }
  });

  /* ---------- 7. magic cursor: glass lens with context states, gold dust, click ripple (fine pointers) ---------- */
  safe('cursor', function () {
    if (!DESK_FX) return;
    var c = doc.createElement('div'); c.className = 'cur'; c.setAttribute('aria-hidden', 'true'); c.dataset.s = 'out';
    c.innerHTML = '<div class="cur-lens"><span class="cur-label"></span></div><div class="cur-dot"></div>';
    body.appendChild(c); root.classList.add('has-cur');
    var lens = c.querySelector('.cur-lens'), label = c.querySelector('.cur-label'), dot = c.querySelector('.cur-dot');
    var LBL = { play: ['Play', 'चलाएं'], drag: ['Drag', 'खींचें'], chat: ['Chat', 'चैट'] };
    var SIZE = { idle: [20, 20, '999px'], link: [40, 40, '999px'], play: [92, 92, '999px'], drag: [92, 92, '999px'], chat: [92, 38, '8px 19px 19px 19px'], native: [20, 20, '999px'], out: [20, 20, '999px'] };
    var WA = '[onclick*="WhatsApp"],a[href*="wa.me"],.btn-wa';
    var MORPH = '.btn,.nav-links a,.lang button,.icon-btn,.chip,.seg button,.crow,.nav-login,.player-x,.tab,.link-arrow,.wm,.reel-ig,.site-foot li a,.mic-btn,summary';
    var MAG = '.btn-primary,.btn-gold,.btn-glass.btn-lg,.btn-dark-glass.btn-lg,.nav-wa,.mic-btn';
    var ptr = { x: -200, y: -200 }, lx = -200, ly = -200, vx = 0, vy = 0, lastMove = 0, moved = 0, started = false, inside = false, kbd = false;
    var state = 'out', curEl = null, cfg = null, press = 1, pressV = 0, pressT = 1, alive = 0, lastDust = 0;
    var magEl = null, magBase = null, magSY = 0, mx = 0, my = 0, magFixed = false;
    var isHi = function () { return W.currentLangMode === 'hi'; };
    function resolve(t) {
      if (!t || t.nodeType !== 1) return { s: 'idle' };
      if (t.closest('input,textarea,select,iframe,[contenteditable],.player')) return { s: 'native' };
      // body text keeps the native I-beam, so a selection starts exactly where it looks like it will
      if (t.closest('p,figcaption,blockquote,dd,.ai-pre') && !t.closest('a,button,label,[role=button],.marquee,.reel,.screen')) return { s: 'native' };
      var dark = !!t.closest('.panel,.plan-pro,.ai-out,.mbar') || body.classList.contains('dark-studio'), info;
      var wa = t.closest(WA);
      // a button that already says WhatsApp gets the wrap (with a green rim); the "Chat" bubble only explains links that show just a number
      if (wa && /whatsapp|व्हाट्सऐप/i.test(wa.textContent || '')) { var rw = wa.getBoundingClientRect(); info = { s: 'morph', el: wa, wa: true, mag: wa.matches(MAG) || wa.matches('.btn-wa.btn-lg') ? wa : null, pad: 5 }; if (rw.width > 420 || rw.height > 90) info = { s: 'link', el: wa }; }
      else if (wa) info = { s: 'chat', el: wa };
      else if (t.closest('.reel') && !t.closest('.reel-ig')) info = { s: 'play', el: t.closest('.reel') };
      else if (t.closest('.marquee')) info = { s: 'drag', el: t.closest('.marquee') };
      else {
        var m = t.closest(MORPH);
        if (m) { var r = m.getBoundingClientRect(); info = r.width > 420 || r.height > 90 ? { s: 'link', el: m } : { s: 'morph', el: m, mag: m.matches(MAG) ? m : null, pad: m.matches('.btn') ? 5 : 4 }; }
        else if (t.closest('a,button,label,[role=button]')) info = { s: 'link', el: t.closest('a,button,label,[role=button]') };
        else info = { s: 'idle' };
      }
      info.dark = dark;
      return info;
    }
    function baseRect(el) {
      if (el === magEl && magBase) { var dy = magFixed ? 0 : (W.scrollY || 0) - magSY; return { left: magBase.left, top: magBase.top - dy, width: magBase.width, height: magBase.height }; }
      return el.getBoundingClientRect();
    }
    function grab(el) { magEl = el; mx = my = 0; el.style.translate = ''; magBase = el.getBoundingClientRect(); magFixed = !!el.closest('.nav-shell,.mbar'); magSY = W.scrollY || 0; el.classList.add('fx-mag'); }
    function release() { var el = magEl; magEl = null; magBase = null; if (!el) return; el.classList.remove('fx-mag'); el.style.translate = ''; }
    function setState(info) {
      var same = info.s === state && info.el === curEl; cfg = info; curEl = info.el || null;
      c.classList.toggle('dark', !!info.dark); c.classList.toggle('wa', !!info.wa);
      if (magEl && magEl !== info.mag) release();
      if (info.mag && magEl !== info.mag) grab(info.mag);
      if (same) return;
      state = info.s; c.dataset.s = state;
      var z = SIZE[state] || SIZE.idle, w = z[0], h = z[1], r = z[2];
      if (state === 'morph' && curEl) { var rr = baseRect(curEl), br = parseFloat(getComputedStyle(curEl).borderTopLeftRadius) || 0; w = rr.width + info.pad * 2; h = rr.height + info.pad * 2; r = br >= 200 ? '999px' : Math.max(10, br + info.pad) + 'px'; }
      lens.style.width = w + 'px'; lens.style.height = h + 'px'; lens.style.borderRadius = r;
      label.dataset.t = LBL[state] ? LBL[state][isHi() ? 1 : 0] : '';
    }
    FX.onLang = function () { label.dataset.t = LBL[state] ? LBL[state][isHi() ? 1 : 0] : ''; };
    FX.cursorState = function () { return state; };
    doc.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      var t = e.timeStamp || now(), dt = Math.max(4, t - lastMove);
      if (started) { var nvx = (e.clientX - ptr.x) / dt, nvy = (e.clientY - ptr.y) / dt; vx = vx * 0.5 + nvx * 0.5; vy = vy * 0.5 + nvy * 0.5; moved += Math.hypot(e.clientX - ptr.x, e.clientY - ptr.y); }
      if (kbd) { if (!(e.movementX || e.movementY)) return; kbd = false; setState(resolve(e.target)); }
      ptr.x = e.clientX; ptr.y = e.clientY; lastMove = t; inside = true;
      if (!started) { started = true; lx = ptr.x; ly = ptr.y; root.classList.add('cur-live'); setState(resolve(e.target)); }
      else if (state === 'out') setState(resolve(e.target));
      kick();
    }, { passive: true });
    doc.addEventListener('pointerover', function (e) { if (e.pointerType === 'touch' || !started || kbd) return; setState(resolve(e.target)); }, { passive: true });
    doc.addEventListener('pointerout', function (e) { if (!e.relatedTarget && e.pointerType !== 'touch') { inside = false; setState({ s: 'out' }); kick(); } }, { passive: true });
    W.addEventListener('blur', function () { inside = false; if (started) setState({ s: 'out' }); });
    // keyboard users: the custom cursor steps aside so focus rings are never covered
    W.addEventListener('keydown', function (e) { if ((e.key === 'Tab' || ((e.key === 'Enter' || e.key === ' ') && doc.activeElement !== body)) && started) { kbd = true; inside = false; setState({ s: 'out' }); kick(); } });
    FX.cursorKbd = function () { return kbd; };
    doc.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'touch') return;
      if (kbd) { kbd = false; inside = true; setState(resolve(e.target)); }
      pressT = state === 'morph' ? 0.94 : 0.82; c.classList.add('down');
      if (state !== 'native' && FX.ripple) FX.ripple(e.clientX, e.clientY);
      if (state !== 'native') for (var i = 0; i < 5; i++) spawn(e.clientX, e.clientY, (Math.random() - 0.5) * 2.4, (Math.random() - 0.5) * 2.4);
      kick();
    }, { passive: true });
    doc.addEventListener('pointerup', function () { pressT = 1; c.classList.remove('down'); kick(); }, { passive: true });
    var sp = false;
    W.addEventListener('scroll', function () { if (sp || !started || !inside || kbd) return; sp = true; setTimeout(function () { sp = false; var el = doc.elementFromPoint(ptr.x, ptr.y); if (el) setState(resolve(el)); kick(); }, 120); }, { passive: true });
    // gold dust: a few tiny compositor-only sparks (transform + opacity), never a full-screen canvas
    function spawn(x, y, svx, svy) {
      if (alive > 14 || !canAnim) return; alive++;
      var d = doc.createElement('i'), h = Math.random(), sz = 0.5 + Math.random() * 0.75, dx = svx * 26 + (Math.random() - 0.5) * 18, dy = svy * 26 + 14 + Math.random() * 22;
      d.className = 'cur-dust' + (h > 0.66 ? ' l' : h > 0.33 ? ' m' : ''); d.style.left = (x + (Math.random() - 0.5) * 6).toFixed(1) + 'px'; d.style.top = (y + (Math.random() - 0.5) * 6).toFixed(1) + 'px'; c.appendChild(d);
      var a = d.animate([{ transform: 'translate(0,0) scale(' + sz.toFixed(2) + ') rotate(0deg)', opacity: 0.9 }, { transform: 'translate(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px) scale(0) rotate(' + (Math.random() * 120 - 60).toFixed(0) + 'deg)', opacity: 0 }], { duration: 650 + Math.random() * 500, easing: 'cubic-bezier(.2,.7,.2,1)' });
      a.onfinish = function () { alive--; d.remove(); };
    }
    var lt = 0;
    tickers.push(function (t) {
      var dt = clamp(t - lt || 16, 1, 50), f = dt / 16.67; lt = t;
      var busy = t - lastMove < 260, s = state;
      var mRect = magEl ? baseRect(magEl) : null;
      if (magEl && mRect) {
        var cx = mRect.left + mRect.width / 2, cy = mRect.top + mRect.height / 2;
        var tx0 = clamp((ptr.x - cx) * 0.2, -10, 10), ty0 = clamp((ptr.y - cy) * 0.26, -7, 7);
        if (Math.abs(tx0 - mx) > 0.05 || Math.abs(ty0 - my) > 0.05) { mx = tx0; my = ty0; magEl.style.translate = mx.toFixed(2) + 'px ' + my.toFixed(2) + 'px'; }
      }
      var tx = ptr.x, ty = ptr.y, k = 1 - Math.exp(-dt * 0.024);
      if (s === 'morph' && curEl) {
        var r = curEl === magEl ? mRect : curEl.getBoundingClientRect(), isM = curEl === magEl;
        var ccx = r.left + r.width / 2 + (isM ? mx : 0), ccy = r.top + r.height / 2 + (isM ? my : 0);
        tx = ccx + (ptr.x - ccx) * 0.08; ty = ccy + (ptr.y - ccy) * 0.08; k = 1 - Math.exp(-dt * 0.02);
      } else if (s === 'chat' && curEl) { var cr = curEl.getBoundingClientRect(); tx = Math.min(cr.right + 14 + 46, innerWidth - 50); ty = cr.top + cr.height / 2; k = 1 - Math.exp(-dt * 0.02); } // the bubble sits just after the link, never over its text
      lx += (tx - lx) * k; ly += (ty - ly) * k;
      if (Math.abs(tx - lx) > 0.15 || Math.abs(ty - ly) > 0.15) busy = true;
      if (t - lastMove > 40) { vx *= Math.pow(0.8, f); vy *= Math.pow(0.8, f); }
      var speed = Math.hypot(vx, vy); if (speed > 0.01) busy = true;
      pressV += (pressT - press) * 0.32 * f; pressV *= Math.pow(0.6, f); press += pressV * f;
      if (Math.abs(pressT - press) > 0.002 || Math.abs(pressV) > 0.002) busy = true;
      var tf = 'translate3d(' + lx.toFixed(2) + 'px,' + ly.toFixed(2) + 'px,0)';
      if (s === 'idle' || s === 'play' || s === 'drag' || s === 'link') { var st = clamp(speed * 0.05, 0, 0.22), a = Math.atan2(vy, vx) * 57.2958; tf += ' rotate(' + a.toFixed(1) + 'deg) scale(' + (1 + st).toFixed(3) + ',' + (1 - st * 0.5).toFixed(3) + ') rotate(' + (-a).toFixed(1) + 'deg)'; }
      lens.style.transform = tf + ' scale(' + press.toFixed(3) + ')';
      dot.style.transform = 'translate3d(' + ptr.x.toFixed(1) + 'px,' + ptr.y.toFixed(1) + 'px,0)';
      // a very subtle gold dust, only when the pointer moves quickly
      if (inside && s !== 'native' && s !== 'out' && speed > 0.45 && moved > 16 && t - lastDust > 34) { moved = 0; lastDust = t; spawn(ptr.x, ptr.y, -vx * 0.6, -vy * 0.6); }
      else if (moved > 60) moved = 0;
      return busy;
    });
  });

  /* ---------- 8. glass panels: edge light + glare that follow the pointer, gentle 3D tilt (desktop) ---------- */
  safe('panels', function () {
    if (!DESK_FX) return;
    var all = $$('main .glass:not(.kchip):not(.seg):not(.fan-note), .plan-pro');
    var TILT = { 'plan': 4, 'plan-pro': 4, 't-person': 2.5 };
    var tiltOf = function (el) { for (var k in TILT) if (el.classList.contains(k)) return TILT[k]; return 0; };
    var vis = new Set(), rects = new Map(), dirty = true, hover = null;
    if ('IntersectionObserver' in W) {
      var io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) vis.add(e.target); else { vis.delete(e.target); e.target.classList.remove('fx-on'); } }); dirty = true; });
      all.forEach(function (el) { io.observe(el); });
    } else all.forEach(function (el) { vis.add(el); });
    W.addEventListener('scroll', function () { dirty = true; }, { passive: true });
    W.addEventListener('resize', function () { dirty = true; });
    var rect = function (el) { if (dirty) { rects.clear(); dirty = false; } var r = rects.get(el); if (!r) { r = el.getBoundingClientRect(); rects.set(el, r); } return r; };
    var pending = false, px = 0, py = 0;
    W.addEventListener('pointermove', function (e) { if (e.pointerType === 'touch' || doc.hidden) return; px = e.clientX; py = e.clientY; if (!pending) { pending = true; requestAnimationFrame(frame); } }, { passive: true });
    function frame() {
      pending = false; var over = null;
      vis.forEach(function (el) {
        var r = rect(el), inside = px >= r.left && px <= r.right && py >= r.top && py <= r.bottom;
        if (px > r.left - 300 && px < r.right + 300 && py > r.top - 300 && py < r.bottom + 300) { el.style.setProperty('--mx', (px - r.left).toFixed(0) + 'px'); el.style.setProperty('--my', (py - r.top).toFixed(0) + 'px'); }
        el.classList.toggle('fx-on', inside);
        if (inside && (!over || el.contains(over) === false)) over = el;
      });
      if (hover && hover !== over) { hover.style.rotate = ''; hover.classList.remove('fx-tilt'); }
      hover = over;
      if (over) { var m = tiltOf(over); if (m && !over.closest('form')) { var r = rect(over), nx = ((px - r.left) / r.width) * 2 - 1, ny = ((py - r.top) / r.height) * 2 - 1; over.classList.add('fx-tilt'); over.style.rotate = (-ny).toFixed(3) + ' ' + nx.toFixed(3) + ' 0 ' + (m * Math.min(1, Math.hypot(nx, ny))).toFixed(2) + 'deg'; } }
    }
    doc.addEventListener('pointerout', function (e) { if (!e.relatedTarget && hover) { hover.style.rotate = ''; hover.classList.remove('fx-tilt', 'fx-on'); hover = null; } });
  });

  /* ---------- 9. scroll: progress line, depth parallax, hero depth, the dark panels open with light ---------- */
  safe('scroll', function () {
    var navEl = doc.querySelector('.nav'), prog = null;
    if (navEl) { prog = doc.createElement('span'); prog.className = 'nav-prog'; prog.setAttribute('aria-hidden', 'true'); navEl.appendChild(prog); }
    var heroHead = doc.querySelector('.hero-head'), stageC = doc.querySelector('#hero .stage'), hero = doc.getElementById('hero');
    var panels = $$('.panel'), reels = $$('.reel-row .reel');
    var useFx = function () { return DESK_FX && DESKQ.matches; };
    var par = [];
    function measure() {
      par = [];
      if (!useFx()) return;
      $$('main .head').forEach(function (el) { el.style.translate = ''; var r = el.getBoundingClientRect(); par.push({ el: el, top: r.top + W.scrollY, h: r.height, k: -0.04 }); });
      reels.forEach(function (el, i) { el.style.translate = ''; var r = el.getBoundingClientRect(); par.push({ el: el, top: r.top + W.scrollY, h: r.height, k: i % 2 ? 0.035 : -0.025 }); });
    }
    var lastY = -1, lastH = 0, need = true;
    function update() {
      var y = W.scrollY || 0, vh = innerHeight, H = root.scrollHeight - vh;
      if (y === lastY && H === lastH) return;
      lastY = y; lastH = H;
      if (prog) prog.style.transform = 'scaleX(' + clamp(H > 0 ? y / H : 0, 0, 1).toFixed(4) + ')';
      if (!useFx()) return;
      for (var i = 0; i < par.length; i++) { var p = par[i], c = p.top - y + p.h / 2 - vh / 2; if (Math.abs(c) > vh * 1.4) continue; p.el.style.translate = '0 ' + (c * p.k).toFixed(1) + 'px'; }
      // hero depth: the headline drifts up a little faster than the stage
      if (hero && y < hero.offsetHeight + vh) { var hp = clamp(y / Math.max(1, hero.offsetHeight), 0, 1); if (heroHead) heroHead.style.translate = '0 ' + (-y * 0.14).toFixed(1) + 'px'; if (stageC) stageC.style.translate = '0 ' + (-y * 0.04).toFixed(1) + 'px'; }
      // the dark panels open from 95.5% as they arrive
      panels.forEach(function (pn) { var r = pn.getBoundingClientRect(); if (r.top > vh * 1.1 || r.bottom < 0) { if (pn.style.scale) pn.style.scale = ''; return; } var tt = clamp((vh - r.top) / (vh * 0.7), 0, 1), e = 1 - Math.pow(1 - tt, 3); pn.style.scale = (0.955 + 0.045 * e).toFixed(4); });
    }
    measure();
    setTimeout(function () { measure(); lastY = -1; need = true; kick(); }, 1400);
    W.addEventListener('load', function () { measure(); lastY = -1; need = true; kick(); });
    W.addEventListener('resize', function () { if (!useFx()) { par.forEach(function (p) { p.el.style.translate = ''; }); panels.forEach(function (p) { p.style.scale = ''; }); if (heroHead) heroHead.style.translate = ''; if (stageC) stageC.style.translate = ''; } measure(); lastY = -1; need = true; kick(); });
    W.addEventListener('scroll', function () { need = true; kick(); }, { passive: true });
    tickers.push(function () { if (need) { need = false; update(); } return false; });
    kick();
    // the nav turns to dark glass while it floats over an emerald panel
    var shell = doc.getElementById('stickySiteHeader');
    if (shell && 'IntersectionObserver' in W) {
      var over = new Set();
      var nio = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) over.add(e.target); else over.delete(e.target); }); shell.classList.toggle('on-dark', over.size > 0); }, { rootMargin: '-40px 0px -' + Math.max(0, innerHeight - 80) + 'px 0px' });
      panels.forEach(function (pn) { nio.observe(pn); });
    }
    // the dark panels catch a sweep of light once as they arrive (all devices)
    if (!RM && 'IntersectionObserver' in W) {
      var pio = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('fx-lit'); pio.unobserve(e.target); } }); }, { threshold: 0.25 });
      panels.forEach(function (pn) { var s = doc.createElement('i'); s.className = 'fx-sweep'; s.setAttribute('aria-hidden', 'true'); pn.insertBefore(s, pn.firstChild); pio.observe(pn); });
    }
  });

  /* ---------- 10. reveals: headings rise word by word, dated stats count up; nothing is ever left hidden ---------- */
  safe('reveals', function () {
    if (RM || !('IntersectionObserver' in W)) return;
    var jobs = [];
    FX.finishCounters = function () { jobs.forEach(function (j) { j.done = true; j.el.textContent = j.fin; }); jobs = []; };
    var arm = function () {
      W.removeEventListener('scroll', arm);
      var vh = innerHeight, below = function (el) { return el.getBoundingClientRect().top > vh * 0.98; };
      // headings (desktop): split at arm time, reverted as soon as the words have landed
      if (DESK_FX) $$('main .head h2.rv:not(.in), main h2.h2.rv:not(.in), .final-inner h2.rv:not(.in)').forEach(function (h) {
        if (!below(h)) return;
        var ws = splitWords(h); if (!ws.length) return; h.classList.add('fx-split');
        var mo = new MutationObserver(function () { if (h.classList.contains('in')) { mo.disconnect(); setTimeout(function () { if (h.classList.contains('in')) unsplit(h); }, 1300 + ws.length * 42); } });
        mo.observe(h, { attributes: true, attributeFilter: ['class'] });
      });
      // counters: only the real, dated stats (e.g. "50K+ · Oct 2026")
      $$('.stat').forEach(function (st) {
        var b = st.querySelector('b'), lab = st.querySelector('span'); if (!b || !lab || !/20\d\d/.test(lab.textContent) || !below(b)) return;
        var fin = b.textContent, m = fin.match(/^(\d+)(.*)$/); if (!m) return;
        var job = { el: b, fin: fin, done: false }; jobs.push(job);
        var to = +m[1], suf = m[2];
        var io = new IntersectionObserver(function (en) {
          if (!en[0].isIntersecting) return; io.disconnect(); if (job.done) return;
          var s0 = now();
          (function step() { if (job.done) return; var f = clamp((now() - s0) / 1400, 0, 1), v = Math.round(to * (1 - Math.pow(2, -10 * f))); b.textContent = (f >= 1 ? fin : v + suf); if (f < 1) requestAnimationFrame(step); else { job.done = true; b.textContent = fin; } })();
        }, { threshold: 0.6 });
        io.observe(b);
        job.io = io;
      });
      // safety net: anything that scrolled past without being seen (a fast jump) is finished at once
      var sweep = function () { var lim = innerHeight; jobs.forEach(function (j) { if (!j.done && j.el.getBoundingClientRect().top < lim * 0.4) { j.done = true; if (j.io) j.io.disconnect(); j.el.textContent = j.fin; } }); };
      var te = 0; W.addEventListener('scroll', function () { clearTimeout(te); te = setTimeout(sweep, 200); }, { passive: true });
    };
    W.addEventListener('scroll', arm, { passive: true });
  });

  /* ---------- 11. the niches band can be dragged (fine pointers) ---------- */
  safe('marquee', function () {
    if (!DESK_FX) return;
    var mq = doc.querySelector('.marquee'), tr = mq && mq.querySelector('.mq-track'); if (!tr) return;
    mq.classList.add('fx-drag-on');
    var off = 0, down = false, sx = 0, so = 0, v = 0, lx = 0, lt = 0, raf = 0;
    var wrap = function (x) { var half = tr.scrollWidth / 2 + 5; if (!half) return x; x = x % half; if (x > 0) x -= half; return x; };
    var set = function () { tr.style.translate = off.toFixed(1) + 'px 0'; };
    mq.addEventListener('dragstart', function (e) { e.preventDefault(); });
    mq.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse' || e.button !== 0) return; down = true; sx = e.clientX; so = off; v = 0; lx = e.clientX; lt = e.timeStamp; cancelAnimationFrame(raf); mq.classList.add('fx-dragging'); try { mq.setPointerCapture(e.pointerId); } catch (er) {} });
    mq.addEventListener('pointermove', function (e) { if (!down) return; off = wrap(so + e.clientX - sx); set(); var dt = Math.max(1, e.timeStamp - lt); v = v * 0.4 + ((e.clientX - lx) / dt) * 0.6; lx = e.clientX; lt = e.timeStamp; });
    var end = function () { if (!down) return; down = false; var last = now(); var coast = function () { var t = now(), dt = Math.min(40, t - last); last = t; off = wrap(off + v * dt); set(); v *= Math.pow(0.94, dt / 16.7); if (Math.abs(v) > 0.02) raf = requestAnimationFrame(coast); else mq.classList.remove('fx-dragging'); }; raf = requestAnimationFrame(coast); };
    mq.addEventListener('pointerup', end); mq.addEventListener('pointercancel', end);
  });

  /* ---------- 12. ROI outputs pulse gold when a slider moves ---------- */
  safe('roi', function () {
    if (RM || !canAnim) return;
    var outs = $$('#outViews, #outHours');
    ['rngFollowers', 'rngReels'].forEach(function (id) {
      var el = doc.getElementById(id); if (!el) return;
      el.addEventListener('input', function () { outs.forEach(function (o) { o.animate([{ transform: 'translateY(5px)', opacity: 0.4 }, { transform: 'none', opacity: 1 }], { duration: 420, easing: 'cubic-bezier(.16,1,.3,1)' }); }); });
    });
  });
})();
