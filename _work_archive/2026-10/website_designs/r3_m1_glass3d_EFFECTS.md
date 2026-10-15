# M1 · 3D Glass: effects list

This is the Focus Story page with an FX layer added on top. All content, honesty wording, features and function names are unchanged. Everything new is in two places: `<style id="fx-css">` and the last three `<script>` blocks (Lenis, the glass renderer and the FX layer). Each FX block is feature-checked and wrapped in try/catch, so if any one of them fails the page still works.

- **Size:** `index.html` is 281.6 KB. Inline JS is 89 KB in total (the page's own script plus Lenis at 14 KB plus FX).
- **No three.js.** The glass is a hand-written WebGL1 renderer of about 9 KB.
- **No GSAP.** All motion is CSS or one shared requestAnimationFrame loop.

**Guard flags** used in the "How it degrades" column below:
- *Phone* = width ≤ 768 px or a coarse pointer.
- *RM* = `prefers-reduced-motion: reduce`.
- *no-GL* = WebGL unavailable.
- *soft-GL* = WebGL running on a software rasteriser with no GPU, such as SwiftShader or llvmpipe.

## 1. The 3D glass (lead idea)

| Effect | Where | How it degrades |
|---|---|---|
| **Glass ribbon ring**: a real-time WebGL object made of a rounded-rect ribbon with 1.5 twists (a "Reels loop") that orbits the hero phone. It uses two passes: back-face normals and thickness go to a texture, then front faces are drawn with refraction in and out per colour channel (chromatic dispersion), Fresnel reflection, Beer-law emerald absorption and a pointer-driven specular highlight. It refracts an emerald, gold and ivory studio environment. The half of the ring behind the phone plane is hidden. The half in front is drawn as see-through glass, so the phone stays readable. | Hero, pinned with the phone through the four story scenes | **Phone:** 30 fps cap, no MSAA, fewer triangles, no frames while the finger is scrolling, paused off-screen. Android tilts it with `deviceorientation`. iOS is skipped so no permission prompt appears. **soft-GL:** low resolution and 30 fps; on phones it renders on demand only, for the intro and each step change. **Low-end devices** (deviceMemory ≤ 2, ≤ 2 cores, Save-Data) and **no-GL / JS off:** a pre-rendered WebP still of the ring (19 KB) sits behind the phone. **RM:** a single static frame. A quality governor watches frame times and steps down in this order: 30 fps, then 80 % resolution, then 62 %, then a frozen frame. If the WebGL context is lost, the still comes back. |
| Ring reacts to the cursor and scroll: tilt follows the pointer, the light follows the pointer, and scrolling spins the twist round the ring. | Hero | Phones use device tilt instead. RM: no reaction. |
| Ring changes with the story: each step (Before → Hook → Captions → After) turns the ring to a new pose. "Before" is cool and desaturated with low dispersion; "After" is warm gold. A gold glint runs round the ribbon on every step. | Hero steps and story scenes | Same in every mode where the ring animates. RM: the pose changes without animation. |
| "Glass assembling" intro: the ribbon draws itself round the phone with a tapered tip while it spins and grows thick. | Hero, after the curtain | RM: none, and the ring appears complete. |
| Light aura: soft emerald and gold light behind the ring, with depth parallax opposite to the pointer. | Hero | Static on phones and with RM. |
| Phone in 3D: rotateY per scene plus a small pointer tilt, with a real side edge (box-shadow thickness) that grows as it turns, and a light sweep ("polish") across the screen on every step. | Hero phone | No tilt on phones unless the device is tilted. RM: no sweep and no tilt. |
| Glass ring echo: the same still sits on the corner of the WhatsApp composer card and floats gently. | Final "Slot #03" section | Hidden on phones. RM: static. |

## 2. CSS 3D glass panels

| Effect | Where | How it degrades |
|---|---|---|
| Thickness: a 1.5 px bright under-edge plus a hairline shadow, so every crystal card reads as a glass slab. | All `.cr` cards and plans | Static everywhere. |
| Edge light: a gradient border ring (mask) lit by a gold-to-emerald spotlight that follows the pointer, so card edges near the cursor glint even when the cursor is not over them. | Cards, plans, drawers, team, founder, ROI, AI card, composer | Phones: a fixed top light, plus a short glare where the finger lands. |
| Specular glare: a soft white highlight with a gold and emerald tint at the pointer. | Same | Phones: shown for a moment on tap. |
| 3D tilt: rotation round an axis under the pointer, using the individual `rotate` property. Strength depends on the element: plans 7°, members 4°, Reels 9°, founder 1.6°. Forms are never tilted. | Plans, team, founder, Reels, portal sample | Desktop only. RM: off. |
| "Recommended" plan: a gold glint orbits the card edge. A conic layer rotates with `transform` inside a masked ring. | Pricing | Runs only while on screen. Phones: one orbit when the card appears. RM: off. |
| Tinted glass for the AI and WhatsApp cards over soft emerald and gold light. | AI plan, final CTA | Desktop only, with no backdrop blur (it cost too much while scrolling). |

## 3. Magic cursor (fine pointer only)

| Effect | Where | How it degrades |
|---|---|---|
| A glass lens ring (with backdrop saturate) follows the pointer with lag, plus an exact dot. | Whole page | Off on touch and with RM. The native cursor is always used on inputs, textareas, selects and inside the Reel player. Tab hides the custom cursor so focus rings stay clear. |
| Context states: **Play** (big emerald lens) on Reels; **Chat** (green ring plus a label pill) on every WhatsApp button and link; **Open** on Instagram links; a hover ring on links and buttons; a press squeeze. Labels follow the Hindi toggle (चलाएं / चैट / खोलें). | Reels, CTAs, team, footer | Same as above. |
| Gold-dust trail: tiny gold four-point sparks drawn on a 2D canvas, at most 70. The loop stops when no sparks are alive. | Whole page | Off on touch and with RM. |
| Magnetic buttons: buttons lean toward the pointer using the `translate` property. The Reel play button follows the pointer inside its tile. | All primary, quiet and on-dark buttons, mic, Reel tiles | Desktop only. RM: off. |
| Nav hover pill: a glass pill glides between links (FLIP with transform only). | Top nav | Desktop only. |

## 4. Motion

| Effect | Where | How it degrades |
|---|---|---|
| **Intro curtain**, at most 1.6 s, first visit per session: "VanIndra" letters rise, a gold hairline draws, CREATIONS fades in, a light glint passes, and the curtain lifts. Any key, click, wheel or touch skips it. CSS alone hides it at 1.62 s even if JS fails. | Page load | Skipped with RM, with a URL hash, or on a repeat visit. |
| Hero headline lines rise out of a glass edge, then the original HTML is restored, so the Hindi round trip is exact. | Hero | RM: plain text. |
| Lenis smooth scroll. In-page links glide and respect each target's `scroll-margin-top`; drawers still open. | Desktop | Off on phones and with RM. Stops while the Reel player is open. |
| Reading progress: an emerald-to-gold line along the bottom edge of the nav. | Nav | Everywhere. |
| Depth parallax: section headers drift slowly, and Reel tiles stagger at two depths. | Desktop | Off on phones and with RM. |
| Reels panel rises (scale 0.94 → 1), and the six Reels fan in from a tilted plane one after another, scrubbed by scroll. They stay flat at rest, so static captures look normal. | Reels | Desktop only. |
| Reels 3D coverflow on swipe (rotateY plus scale by distance from centre). | Reels row | Phones only. RM: off. |
| Caustic light drifts inside the dark Reels panel, and tiles "breathe" on hover. | Reels | Caustic runs only while on screen and is static on phones. RM: off. |
| Reveals: fade, rise and a slight scale, with a safety timer that reveals anything the observer missed. | All sections | RM: no reveals. |
| Counters: 50K+, 467+ and 4 count up when seen. They finish instantly if the language changes. | Founder stats | RM: final values only. |
| The ROI outputs pulse gold when a slider moves. | ROI | RM: off. |
| Drawers open with a soft slide, and chips spring on press. | Details, chips | RM: instant. |
| Dark Studio Mode switches with a circular reveal from the pointer (View Transitions). | Theme toggle | Instant where the API is missing and with RM. |

## 5. Magic moments

- **Sparks on WhatsApp actions.** A gold sparkle burst plays at the pointer whenever a WhatsApp action fires (`openElegantWhatsAppDirect`, `sendZeroTouchWhatsApp`).
- **AI plan finished.** When `runZeroTouchBackgroundAI` finishes, a burst plays over the output and a gold glow ring pulses around the plan.
- **Taps and clicks.** Every tap or click draws a gold ripple ring. This includes touch.

## Performance

Tests ran in headless Chromium, which has no GPU: WebGL runs on SwiftShader and compositing is done in software, so this is a worst case. The FPS check scrolls the whole page with `requestAnimationFrame` (a new scroll position every frame) and counts long tasks. Script: `_work/perf.js`.

| Context | Scroll | Idle at the hero |
|---|---|---|
| 390 px phone, DPR 3, CPU ×4 throttled | 58–60 fps; p95 16.8 ms; worst frame 50–67 ms; at most 1 long task (≤ 80 ms) | 59–60 fps |
| Same, the original Focus Story page | 59.8–59.9 fps; worst frame 50–83 ms | |
| Desktop 1440×900 | 59.9 fps; worst frame 33 ms | 48 fps while the software-rendered ring animates (60 on a real GPU) |

- **Phone result:** the FX page is level with the original page.
- **Rules followed:**
  - Motion uses transform and opacity only, including the individual translate, rotate and scale properties.
  - All loops pause off-screen and in hidden tabs.
  - On phones, the computed backdrop-filter count stays within the verify limit; the only blurred elements are the nav and the sticky bar.
  - There is no layout shift, and no horizontal overflow from 320 to 1920 px.

## Verify

`node verify.js m1_glass3d` reports PASS 57, WARN 0, FAIL 0.
