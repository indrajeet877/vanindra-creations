# VanIndra homepage: "Blow their clients' minds" (3D glass, magic cursor, motion)

SCRATCH = /tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad
W = SCRATCH/web3

## What the owner said (15 Oct 2026, after "Focus Story" went live)
> "I don't like it. So many things — create 3D glass, stylish, elegant. Add features in the cursor, also some magic effects, add some motion effects too, lots of things you can think of. Create the best stylish on top of it. Make it blow their clients' mind."

## The job
Build **on top of the live Focus Story page** (`W/base_focus_story.html`, the current `index.html`; LOOK at `SCRATCH/web2/v4_focus/preview.png` and its screenshots). Keep its structure, content, honesty and every feature. Then make it an **award-level, jaw-dropping, premium experience**: real 3D glass, a magical cursor, cinematic motion, and delightful micro-interactions. Think Awwwards Site of the Day, Apple product pages, Linear, Stripe, Lusion, Active Theory and visionOS.

It must stay **elegant**, not gimmicky. One strong idea per moment, smooth 60 fps, calm typography, and lots of space. The audience is premium Indian creators with 1 lakh+ followers, doctors, coaches and D2C brands. The page should make them feel "this studio is world class".

## Ideas to draw from (pick, combine, invent; don't do everything at once)
- **3D glass:**
  - A real-time WebGL glass object that refracts the brand light: an emerald/gold/ivory environment, chromatic dispersion, Fresnel edges, caustics.
  - For example: a glass prism or monolith behind the hero phone, a glass "lens" that the phone sits in, or glass panels with true thickness.
  - It reacts to the cursor, to scroll, and to device tilt on phones.
  - CSS 3D glass cards with thickness, edge highlights and a specular glare that follows the pointer.
- **Magic cursor (desktop and fine pointers only):**
  - A custom glass-lens cursor that refracts or magnifies what is under it.
  - Context states: "Play" on Reels, "Drag" on carousels, "Chat" on WhatsApp buttons, and a text caret on inputs.
  - Magnetic buttons, a subtle gold-dust sparkle trail, a click ripple, and a spotlight that lights glass edges.
  - On touch devices: tap ripples and gyroscope tilt instead. Never hide the native cursor on inputs, and never break clicking.
- **Motion:**
  - An intro reveal: a wordmark draw and glass assembling, short (≤ 1.6 s) and skippable.
  - Split-text headline reveals and scroll-choreographed scenes (the pinned phone rotating in 3D through raw clip → hook → captions → ready).
  - Depth parallax, a light sweep across glass, number counters, a 3D Reels carousel or coverflow, section-to-section colour and light transitions, a smooth scroll feel, and a scroll progress indicator.
  - Hover micro-interactions everywhere.
- **Magic moments:** for example, a soft gold sparkle burst when a WhatsApp message is sent or the AI plan finishes; Reels that "breathe" on hover; the before/after phone "polishing" with a light sweep.

## Libraries
- Self-contained is preferred: everything inline in `index.html`.
- These vendor files are available locally in `W/vendor/`:
  - `gsap.min.js` 72 KB, `ScrollTrigger.min.js` 44 KB, `SplitText.min.js` 7 KB, `Observer.min.js`, `Flip.min.js`, `CustomEase.min.js`
  - `lenis.min.js` 14 KB
  - `three.module.min.js` 339 KB
- GSAP is free for commercial use under its standard license; keep its license comment.
- **Inline** any vendor script you use (copy its contents into a `<script>` in `index.html`), because the public build only ships HTML and images, and CDNs are blocked in this sandbox.
- Do **not** inline three.js. It is too heavy for Indian 4G phones. Write your own small WebGL shader (raymarched or fragment-shader glass, a few KB) or use CSS 3D.
- **Budget:** at most 200 KB of total JS inline (about 70 KB gzipped). The whole `index.html` should stay under about 550 KB.

## Hard rules (unchanged)
- All content, honesty wording and features of Focus Story stay:
  - the WhatsApp concierge (wa.me/918112859437 only) and the Hindi `data-hi` toggle with an exact round trip;
  - Dark Studio Mode, the Before/After phone, Vandana Yadav's 6 Reels with the inline player, the AI plan (pollinations + fallback, WhatsApp send, download, voice mic), pricing, ROI, team with official app logos, FAQ, mobile sticky bar, and links to `login.html` and `thumbnail-studio.html`.
  - Keep every JS function name listed in `SCRATCH/web2/FINAL_SPEC.md` section E.
- Golden rules:
  - Never write Guggy, Sahil or Indrajeet.
  - The only phone number is +91 81128 59437.
  - No guarantees, illustrations labelled, text wordmark only (the logo is not approved yet), and no pitch-deck link.
- **Progressive enhancement:**
  - With JS effects off, WebGL unavailable, or any effect throwing an error, the page still works and looks good.
  - All effects are wrapped in try/catch and feature checks.
  - Content is never left invisible: no opacity:0 waiting for an observer without a fallback timer.
- **`prefers-reduced-motion`:** no smooth scroll, no parallax, no cursor trail and no intro. Simple fades only.
- **Performance:**
  - 60 fps on desktop, with no jank on a mid-range Android.
  - On phones (≤ 768 px or coarse pointer), run a lighter set: no WebGL, or a low-resolution WebGL capped at 30 fps and paused off-screen.
  - Pause every animation loop when off-screen or when the tab is hidden.
  - Use `transform`/`opacity` only for motion.
  - Keep `backdrop-filter` to ≤ 8 elements on mobile.
  - No layout shift.
- Accessibility: keyboard focus visible, the custom cursor never hides focus or text selection, and contrast ≥ 4.5:1.
- `node W/verify.js <your folder>` must report FAIL 0. It blocks external network and checks the rules, round trip, overflow 320–1920 px and features.

## Deliverables (in W/<id>/, with `assets` symlinked to /home/user/vanindra-creations/assets)
1. `index.html`
2. Screenshots via `node W/shoot.js W/<id> W/<id>/shot`, plus your own: dark mode, Hindi, and 320 px.
3. **Motion recordings**, because motion can't be judged from stills:
   - Use Playwright `recordVideo` (Chromium is pre-installed; `require('/opt/node22/lib/node_modules/playwright')`).
   - `desktop.mp4`: 1440×900, about 25 s. Load the page, let the intro play, move the mouse across the hero and over buttons and Reels (to show the cursor effects), click a Before/After step, then scroll smoothly through the whole page.
   - `mobile.mp4`: 390×844 with `isMobile` and `hasTouch`, about 20 s, scrolling through.
   - Convert with `ffmpeg` to H.264 mp4: `-c:v libx264 -pix_fmt yuv420p -crf 26 -movflags +faststart`, at most about 12 MB each.
   - Also extract a 12-frame contact sheet of each video (`frames_desktop.png`, `frames_mobile.png`) so reviewers can see the motion.
4. `preview.png`: a desktop fold plus a mobile fold, side by side.
5. `EFFECTS.md`: a list of every effect, where it is, and how it degrades (mobile, reduced motion, no WebGL).
