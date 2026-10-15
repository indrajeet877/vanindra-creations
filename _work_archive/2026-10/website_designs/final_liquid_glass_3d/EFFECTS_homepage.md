# Final homepage · Liquid Glass + 3D glass, magic cursor, cinematic motion

This is the team's **Liquid Glass** page (`base_liquid_glass/index.html`) with one FX layer on top. The ivory glass look, layout, copy, honesty wording, prices, every `data-hi` string and every function name are unchanged. A "Review fixes" section at the end lists what changed after the three reviews (creative director, Android/Hindi creator, QA/performance).

The FX layer is made of these parts:
- `<style id="fx-css">` at the end of `<head>`.
- A tiny boot script in `<head>` that decides, before first paint, whether the intro plays.
- The intro markup as the first child of `<body>` (desktop only; phones remove it).
- Two boxes inside the hero phone: `.gl3d-back` (behind the phone) and `.gl3d` (in front of it, holding the canvas).
- `<style id="fx-stills">` at the end of `<body>`: the pre-rendered stills of the glass (back half and front half, light and dark).
- Two scripts before `</body>`: Lenis, then the glass renderer and the FX layer.

Sources are in `_work/` (`fx.css`, `fx.js`, `glass.js`, `boot.html`, `intro.html`, `still2.js` for the stills). `_work/build.py` assembles the page from the base and asserts every injection point. The pre-review version is kept in `_work/pre_review/`.

**Size and libraries**
- `index.html` is 406,845 bytes (144 KB gzipped).
- Inline JS is 110 KB: the base script, Lenis (MIT) and the glass renderer plus the FX layer. There is no GSAP and no three.js.
- The four stills are WebP with lossy alpha, 12–17 KB each, and sit at the end of `<body>`, off the render-blocking `<head>`.

**Guards:**
- Every block runs inside `safe()` (try/catch) and checks its features first.
- All animation runs through one shared `requestAnimationFrame` loop. It sleeps when nothing moves, stops in hidden tabs, and each effect uses IntersectionObserver to stop off-screen. Pointer handlers queue nothing while the tab is hidden.
- Motion uses `transform` and `opacity` only. The one exception is the base page's existing filter transition on the phone image.

**Legend:** *Phone* = ≤ 768 px or a coarse pointer · *RM* = `prefers-reduced-motion: reduce` · *RT* = `prefers-reduced-transparency: reduce` · *no-GL* = WebGL unavailable, software-only or refused · *JS off* = JavaScript disabled.

## 1. 3D glass

| Effect | Where | Phone | RM | no-GL / JS off |
|---|---|---|---|---|
| **Glass orbit.** A real-time WebGL ring of clear glass orbits the hero phone (pitched about 49°, centred at 30 % of the phone height). Its far half passes **behind** the phone and its near half passes **in front of** the lower screen, below the face, over the caption area. One canvas does both: the shader cuts the far half out exactly where the phone's rounded rectangle is. The ribbon has one twist that slowly drifts, so it reads as live on a still screen. The material is clear glass: refraction in and out (IOR 1.33) with a ~1.5 px dispersion split, light emerald absorption, a thin Fresnel rim and a pointer-driven specular light. The body is only partly opaque (and only 10–24 % over the phone screen), so the real page and the real screen show through it. | Hero | Narrower (fits the screen) and a little lower, so the near half stays under the face. Rendered at min(DPR, 2) with MSAA, at most 30 fps, on demand only, never while a finger scrolls, one clean frame after a scroll settles, immediate redraw after a resize. Created only after the visitor scrolls to the phone, or after 3 s of idle, never in the middle of a tap; never with Save-Data or ≤ 3 GB memory. Android tilt moves it. | One static frame. | The identical pre-rendered still (back half behind the phone, front half in front) shows instead. With JS on, the live canvas cross-fades over it. |
| Orbit reacts. Yaw and pitch follow the pointer (±0.2 / ±0.1 rad), scrolling tips it back and rolls the twist. Before/After changes the light: the raw clip and "Before" are cool and desaturated, "After" is warm gold, with a gold glint running round the ring on every change. | Hero | Device tilt instead of the pointer. | Static. | — |
| **Software WebGL is refused.** The context is requested with `failIfMajorPerformanceCaveat`, and a SwiftShader / llvmpipe / software renderer is dropped at once (`WEBGL_lose_context`), so those visitors get the still and no multi-second freeze. | | | | |
| Quality governor. On a slow GPU it lowers the frame rate first (30, then 24 fps), then the resolution, never below 1 canvas pixel per CSS pixel, then freezes the last frame. | | Same. | | |
| Context loss and restore. On `webglcontextlost` the still returns; on `webglcontextrestored` the renderer is rebuilt and the live glass comes back. | | | | |
| **Glass with true thickness.** Every glass panel in `main` gets a crisp 1.5 px under-lip, a hairline shadow and an inner light. | Cards, plans, composer, AI card, ROI, portal, FAQ | Same (static). | Same. | Same (CSS only). |
| **Edge light + glare** that follow the pointer, and a **gentle 3D tilt** (up to 4° on plans, 2.5° on team cards). | Desktop | Off. | Off. | Off. |

## 2. Magic cursor (fine pointers only)

| Effect | Notes |
|---|---|
| **A quiet default lens**: 20 px, transparent, a 1 px white rim with an ink hairline and a 6 px ink dot at the exact hotspot. Gold appears only on hover (links) and on press. It trails the pointer by about 40 ms and squishes on press. | `pointer-events:none`, no backdrop filter. |
| **Context states.** *Morph*: the lens wraps buttons, nav links, chips, language and theme toggles (gold hairline). Buttons that already say WhatsApp get the wrap with a **green** rim and stay magnetic. *Chat / चैट*: a small speech bubble only for WhatsApp links that show just the number; it sits 14 px after the link, vertically centred, so it never covers text. *Play / चलाएं* on Reels. *Drag / खींचें* on the niches band (draggable with inertia). *Native*: over inputs, selects, the Reel player **and over body text** the lens steps aside and the native caret or I-beam is shown. Headlines keep the plain lens (no fake caret). | Labels are CSS `content:` from a data attribute, so they never enter `innerText`; they switch with the Hindi toggle. |
| **Keyboard mode.** Tab (or Enter / Space on a focused control) hides the lens. It stays hidden while the page scrolls under a parked mouse (synthetic hovers are ignored) and only returns on a real mouse move, so it never competes with the focus ring. | |
| Magnetic primary buttons, a faint gold-dust trail (≤ 14 compositor-only sparks), a gold click ripple. Phones get a gold tap ripple instead of a cursor. | Off with RM and on coarse pointers. |

## 3. Cinematic motion

| Effect | Where | Phone | RM | JS off |
|---|---|---|---|---|
| **Intro** (desktop, at most once a day, stored in `localStorage` with a timestamp; never for deep links, Save-Data or connections slower than 4G). "VanIndra" rises over three ivory glass panes that slide together, a gold hairline draws, CREATIONS fades in. Then only the mark flies into the nav: CREATIONS, the line and the panes leave in the first 200 ms, the ivory veil fades on its own (420 ms), and in the last 100 ms of the 560 ms flight the nav wordmark fades in exactly where the mark lands. Every fade starts from the opacity on screen, so nothing can flash back. A CSS fail-safe at 2.2 s clears it if JS never runs. Never blocks input; any key, click, wheel or touch skips it. | Page load | **No splash.** A 420 ms gold shimmer runs across the nav wordmark over a hero that is already painted. | None. | None. |
| **Hero entrance** starts with the veil (or at once without an intro). Words rise .42 em and fade in, 720 ms, 55 ms apart; "everything else." lands as one unit 140 ms after the last word; the lede at +180 ms, CTAs at +260 ms, the phone at +320 ms. Done within about 1.1 s. Words are split on spaces only (Hindi is never broken) and the split is undone afterwards and before any language switch. | Hero | 20 % shorter. | Static. | Static. |
| **Before → After polish.** The phone first shows the raw clip, then polishes into the finished edit with a 700 ms light sweep, the hook dropping in, the chips popping and the glass warming to gold. Desktop: 450 ms after the phone starts rising. Phones: 350 ms after it is 40 % in view. **The raw look is never on screen for more than 1.2 s**, and scrolling away finishes it at once. Visual only: the page text never changes. | Hero phone | On view. | Shown finished. | Shown finished. |
| **Reels coverflow** (desktop): the hovered Reel lifts 8 px, scales 1.04 and breathes (1.0 → 1.015, 2.4 s); its neighbours turn ±10° and step back 40 px. Transform only. | Reels | Off. | No breathing. | — |
| Depth parallax, dark panels opening from 95.5 % with a sweep of light, the nav turning to dark glass over the emerald panels (its WhatsApp button turns to the ivory pill there), counters on the two dated stats only, Lenis smooth scroll (desktop), a scroll progress hairline, and a circular reveal for Dark Studio Mode. | | Light sweep and dark nav only; native scroll. | Dark nav only. | — |

## 4. Magic moments

- **WhatsApp sent.** A soft gold sparkle at the pointer (or the focused button), plus an 8 ms haptic tick on Android. Every message still goes to wa.me/918112859437 only.
- **AI plan finished.** A burst over the plan and a gold ring pulse.

## 5. Phones and accessibility

- Phones: no splash, no WebGL until the visitor reaches the phone, no cursor, no Lenis, no parallax, no heading split.
- **Blur budget:** on phones only the nav and the sticky bar keep a live `backdrop-filter` (2 elements), and **RT removes those too** (fixed: it used to be overridden on coarse pointers).
- **Hindi is remembered** between visits (`localStorage 'vanindra_lang'`, applied before the hero is split). English stays the default for new visitors.
- Tap targets ≥ 44 px (the wordmark links now have `min-height:44px`). The pricing carousel moves one card per swipe (`scroll-snap-stop:always`). The footer Gmail address wraps inside its column and the contact column is full width under 420 px.
- Visible focus everywhere; form fields now get a 2 px emerald outline on `:focus-visible`. The cursor never hides focus, the caret or text selection. All new layers are `aria-hidden`.

## 6. QA (this sandbox has no GPU)

`node verify.js final_home`: **PASS 56 / WARN 1 / FAIL 0** (the WARN is the mobile height note, 12,815 px, under the 13,500 budget).

Screenshots in `qa/` (dark 1440/390, Hindi 390/1440, 320 px, no-WebGL, JS off, reduced motion, hover states) and the check outputs in `_work/rv/` (intro sheets `intro_sheet_n.png` and `intro_sheet_slow*.png` at 6× CPU throttle, orbit poses `hero_*.png`, cursor states `cur_*.png`, `nav_on_dark.png`, `nav_1130_hi.png`, `foot360_hi.png`).

## 7. Performance

Headless Chromium, SwiftShader (no GPU), shared 4-core VM. Treat these as worst cases.

**Phones (soft WebGL is refused, so this is what a GPU-less visitor gets):**

| | Final | Before the review | Base |
|---|---|---|---|
| First visit, hero fully readable (390 / 360, 4G, CPU ×4, reviewer's `load_clean.js`) | **1.37 s / 1.35 s** | 3.85 s / 4.02 s | 2.32 s / 2.26 s |
| Touch-fling scroll, CPU ×4 (reviewer's `scroll.js`), avg fps / p95 / worst | **38.5 / 66.7 ms / 383 ms** (390), **44.6 / 50 ms / 400 ms** (360) | 31.2 / 100 ms / 1,083 ms | 26.2 / 133 ms / 733 ms |
| Scripted scroll, DPR 3, CPU ×4 (`perf.js`) | 59.8 fps, worst 33 ms, 0 long tasks | 57.5 fps | 58.2 fps |
| Same with the live glass forced on | 54.4 fps, 1 long task (80 ms) | | |

First contentful paint is about 2.2 s against the base's 1.7 s in the same throttled setup (a larger page); there is no layout shift (CLS 0).

**Desktop hero, 1440×900:** without the glass (software GL refused) 13.4 fps idle and 9.6 fps with the pointer moving, against the base's 13.8 / 13.3 fps; the difference is the panel glare repainting blurred glass in software. With the live glass forced on: 11 / 7 fps. On a real GPU the glass is two passes of about 9 k triangles and should hold 60 fps; **this still needs a check on a real mid-range laptop and Android phone.**

**Long tasks at load (desktop, SwiftShader):** the parse (138–146 ms) plus one **612 ms** task about 3 s after load while Chrome creates the WebGL context that is then refused (before the review: 1.8–5.1 s). With `--disable-webgl` only the parse remains.

**Loops pause:** hero off-screen 0 glass frames in 2 s and the loop stopped; hidden tab 0 frames, loop stopped, 0 rAF calls queued by 80 pointer moves. Phones: 0 glass frames in 3 s of idle after the phone came into view.

**Jump scroll** (bottom, top, middle, top; 1.6 s after each): 0 hidden elements in view at every stop, desktop and mobile, with and without the live glass; stats always end on "50K+ 467+ 4".

**Recordings** (the live glass is forced on for capture, `window.__fxForceGL`, because this sandbox has no GPU; real visitors never set it):
- `desktop.mp4`: 22.6 s, 1440×900. The sandbox's blank first 2.8 s are cut. 0–4.2 s real time (intro, entrance, glass), then hover, cursor states and Before/After at 1.5×, then the full scroll at 4.5×.
- `mobile.mp4`: 23 s, 390×844, real time (first 1.5 s of blank paint cut). Shimmer, phone with the orbit, tap ripple, full scroll.
- Software rendering makes the glass slower and a little softer than on a device.

## 8. Review fixes

**Blocking, all fixed**
1. *Intro veil flashed back on slow paints.* Fades now start from the on-screen opacity (Web Animations), the fail-safe moved to 2.2 s, and a late skip after the fail-safe just removes the layer. Checked at 1× and 6× CPU throttle: no flash.
2. *Wordmark never landed; two logos at once.* The veil is a separate layer; only the mark travels; the nav wordmark is hidden during the intro and cross-fades in during the last 100 ms of the flight (`intro_sheet_n.png`).
3. *3D glass mostly below the fold.* Re-posed as an orbit round the phone: at 1440×900 the far arc, both lobes and the glass round the phone are on the first screen; the near arc passes in front of the lower screen below the face (`hero_1440x900_live.png`, `hero_1440x1250_live.png`, 1280×720, 1920×1080).
4. *Low-resolution, aliased rim.* Canvas at min(DPR, 2) on all devices (phones 886 px for 443 CSS px), MSAA on, and the governor never drops below 1 canvas px per CSS px.
5. *Phone intro cost (+1.6 s).* No splash on phones, Save-Data or slow connections; a 420 ms shimmer instead; "seen" stored for 24 h in `localStorage` (Instagram in-app opens no longer replay it). Hero readable at 1.37 s instead of 3.85 s.
6. *Footer Gmail cut off at 360 px Hindi.* Columns get `min-width:0`, links wrap, the contact column is full width under 420 px; the address now ends at x = 230 in a 360 px viewport (EN and हि).
7. *RT ignored on phones.* The phone blur rule is scoped to `prefers-reduced-transparency: no-preference`, and RT clears everything; the reviewer's `t_rtbase.js` now returns `[]` for both pages.
8. *Cursor came back during keyboard navigation.* Keyboard mode ignores synthetic hovers and the scroll re-resolve until a real mouse move. Reviewer's `t_kbd2.js`: lens visible on **0 of 70** Tab stops (was 9).
9. *Software WebGL froze the page 1.8–5.1 s.* Software renderers are refused before any shader is compiled; one 612 ms context-creation task remains (see §7).
10. *Condensed nav wrapped its labels.* Labels never wrap and the pill widens to 1,180 px; all links are one line at 1,130–1,920 px in EN and हि.

**Polish applied:** clear-glass material (IOR 1.33, lighter absorption, thin rim, page visible through it); quiet 20 px default cursor; heading caret dropped; WhatsApp bubble only on number-only links and placed after the link; faster Before→After (≤ 1.2 s raw, 700 ms sweep); light Reels coverflow with breathing; ivory glass panes in the intro; ivory nav WhatsApp pill over dark panels; scroll-end and resize redraws on phones; `scroll-snap-stop` on plans (swipes now go 0 → 313 → 625 px, one card each, instead of skipping the Rs 2,999 trial); `webglcontextrestored`; no rAF while hidden; shorter phone demand windows; stills moved off the `<head>`; form focus outlines; 44 px wordmark; Hindi remembered; touch-fling numbers reported; haptic tick on WhatsApp send.

**Skipped, and why**
- *Auto-defaulting to Hindi when `navigator.language` is `hi`*: the golden rules say English by default; only a visitor's own choice is remembered.
- *Dropping the blur on the small hero chips (`.kchip`, `.fan-note`)*: the chips floating over the glass orbit are part of the Liquid Glass look the team picked; desktop stays well inside the blur rules.
- *Analytic `fwidth` edge AA*: MSAA plus full-resolution rendering fixes the stair-steps without the WebGL1 derivatives extension.
- *Moving the stills to `assets/`*: the public build ships HTML + images from the repo, which this job may not touch; they moved to the end of `<body>` instead.
- *Wow ideas not built*: the ring as the intro, a drag scrubber for Before/After, the in-phone "message sent" notification (it would add new page text that needs Hindi copy), and a gold focus ring for keyboard users. Good candidates for a next round.
