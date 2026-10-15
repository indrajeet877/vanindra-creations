# M2 · Magic Cursor: effect list

Direction: **the cursor is a small lens of real glass.** It refracts what it touches, changes shape for each kind of control, and leaves a little gold dust behind it. On phones, the same glass answers taps, tilt and scroll.

Everything sits on top of Focus Story (`base_focus_story.html`). Content, honesty wording, features and function names are unchanged.

The layer is about 40 KB of JS and 22 KB of CSS, plus Lenis (14 KB, MIT). There is no WebGL and no three.js. Refraction comes from an SVG displacement filter used as a `backdrop-filter`, which Chromium supports; every other browser gets frosted glass instead.

## How each effect degrades

**Legend**

- **Touch:** coarse pointer and most phones.
- **RM:** `prefers-reduced-motion: reduce`.
- **No refraction:** Safari, Firefox, or `prefers-reduced-transparency`.
- **No JS:** JavaScript is off.
- **Never in text:** labels come from CSS `content:` or `attr()`, so they never reach `innerText`, and the Hindi round trip stays exact.

### Intro and hero

**1. Intro**

- **What and where:** the boot script at the top of `<body>`. The letters of "VanIndra" resolve from blur, a gold hairline draws under them, and a glass lens sweeps across and magnifies the wordmark. Then the curtain lifts. It finishes in 1.52 s.
- **Skipping:** any pointer, key, wheel or touch input skips it. It plays once per session and is skipped for deep links (`#hash`). The text is drawn with CSS, never in the page text.
- **Touch:** smaller lens, no blur on the letters.
- **RM:** not shown.
- **No refraction:** the lens is a frosted glass ring.
- **No JS:** not shown.

**2. Hero headline**

- **What and where:** the words of the headline rise out of soft focus as the curtain lifts.
- **Safety:** if the layer script fails, the headline still appears after 2 s (CSS fallback).
- **Touch:** rise without blur.
- **RM:** static.
- **No JS:** static (the base CSS fade).

**3. Hero light pool**

- **What and where:** a soft emerald and gold aura in the hero follows the pointer slowly.
- **Touch, RM, No JS:** none.

**4. Hero phone as 3D glass**

- **What and where:** at rest the phone is turned slightly toward the headline. It tilts toward the pointer (up to about 10°), and a glare moves across its glass.
- **Touch:** the phone rolls a little as it scrolls past. On Android it also follows the gyroscope; iOS is never asked for permission.
- **RM, No JS:** flat.

**5. Polishing sheen**

- **What and where:** a light sweep crosses the phone screen and the phone gives a small 3D turn on every Before/Hook/Captions/After change. While the visitor reads the hero, the glass catches the light every 7 s.
- **Touch:** sweep only.
- **RM, No JS:** none.

**6. Liquid-glass Before/After thumb**

- **What and where:** the sliding thumb of the step control is a drop of glass. It gently magnifies the active label and bends text at its rim as it slides.
- **Fallback:** without refraction, the base thumb sits behind the labels.

### The cursor (desktop and other fine pointers only)

**7. Glass-lens cursor**

- **What and where:** a 30 px lens with a 1 px specular rim, a warm gold underside and a 5 px hotspot dot.
- **Motion:** it follows the pointer on a spring, stretches with speed, and squishes when pressed.
- **Native cursor:** stays visible until the first mouse move, and comes back over inputs, textareas, selects, the range slider, the consent checkbox and the Instagram iframe.
- **Safety:** it never takes pointer events, so clicking always works.
- **Touch, RM, No JS:** the native cursor is used.
- **No refraction:** frosted lens.

**8. Cursor states.** The lens changes shape depending on what it is over:

| State | Where | What it does |
| --- | --- | --- |
| Loupe | the hero phone, the founder photo, the team photos, the client-portal preview | 82 px magnifier with chromatic dispersion |
| Play / चलाएं | Reel covers | 90 px lens that magnifies the cover |
| Drag / खींचें | the Reels strip | arrows appear, and the label stays while dragging |
| Chat / चैट | every WhatsApp action | the lens becomes a dark emerald speech bubble with the WhatsApp glyph, beside the pointer so it never covers the label |
| Morph | nav links, buttons, chips, the step control, contact rows, the "+" on the drawers, footer links, the language switch and the theme toggle | the glass wraps the control, iPad style, with a gold hairline |
| Text | big headlines | a slim gold caret |

The labels switch to Hindi together with the page.

**9. Magnetic controls**

- **What and where:** buttons, icon buttons, chips, the drawer "+", nav links, the strip arrows and the wordmark lean toward the pointer (up to 12 px) and spring back. A soft light follows the pointer across the surface of each button.
- **Touch, RM:** off. Instead, touch gets the press states in item 18.

**10. Gold-dust trail**

- **What and where:** one canvas, drawn only while the pointer moves fast. Particles twinkle and drift down.
- **Dark areas:** on the dark Reels band and in Dark Studio Mode the gold glows additively.
- **Cost when idle:** the canvas is hidden (`display:none`).
- **Touch, RM, No JS:** none.

**11. Click ripple**

- **What and where:** a gold and white glass ring at the click point.
- **Touch:** the same ring appears on tap.
- **RM:** none.

**12. Edge light**

- **What and where:** the glass panels light up along their rim near the pointer: crystal cards, pricing plans, the client portal, the nav pill and Reel tiles. Each panel gets a 1.6 px ring child; only its transform and opacity change.
- **Touch:** instead, a gold line draws along the top edge of each glass panel once, as the panel arrives (compositor-only).
- **RM:** none.

**13. Reel previews that follow the pointer**

- **What and where:** a fan of Reel covers follows the pointer and tilts with its speed. It appears on the @vandanay2012 and @smitayadav_0901 links (founder, team, footer, Reels footer), on the nav "Reels" link and on "Watch 6 real Reels". Near the top of the screen it drops below the pointer.
- **Touch, RM, No JS:** none; the links work as before.

### Reels and other magic moments

**14. Reels film strip**

- **Desktop:** the six covers become a larger strip with faded edges.
  - You can drag it with the mouse (with inertia), or scroll it sideways with a trackpad or Shift + wheel.
  - Hovering a cover dims the other five, and the hovered tile leans in 3D.
  - A gold rail and prev/next buttons (44 px or more) work with the keyboard. A click is never swallowed unless you actually dragged.
- **Touch:** native swipe, plus the rail and the arrows.
- **No JS:** a plain scrollable row.

**15. Sparkle bursts**

- **What and where:** gold stars burst and a ring expands on every WhatsApp action, with a bigger burst on "Send on WhatsApp" and "Send to WhatsApp desk".
- **AI plan:** when the plan is ready, two bursts fire and a light sweeps across the result card.
- **Touch:** same.
- **RM, No JS:** none.

**16. Dark Studio Mode reveal**

- **What and where:** a circle of the new theme opens from the sun/moon toggle (View Transitions). `toggleSurfaceTheme` is kept and wrapped.
- **Fallback:** the instant switch, on RM or in browsers without View Transitions.

### Scrolling and reveals

**17. Scroll reveals**

- **What and where:** glass panels settle into place. The big two-tone statements rise word by word, and the founder stats count up and end on their exact original text.
- **Safety:** reveals only arm after the first scroll, and a backup check reveals anything already on screen. Nothing waits invisible.
- **Touch:** same, lighter (2D only).
- **RM:** static.
- **No JS:** static.

**18. Haptic-feeling press states (touch)**

- Buttons, chips, steps, contact rows and the mobile bar press down to about 95% and spring back.
- A 7 ms vibrate tick fires on primary taps (Android); WhatsApp taps get a double tick.
- The blue tap flash is replaced by the ripple.

**19. Scroll progress**

- **What and where:** a gold thread under the nav pill. The page height is cached, so there is no layout read per scroll.

**20. Smooth wheel scrolling (Lenis)**

- **What and where:** desktop with a fine pointer only.
  - Anchors respect `scroll-margin`, and the matching drawer still opens.
  - Scrolling pauses while the Reel player is open.
  - Textareas, selects and the AI plan output scroll natively.
  - Lenis runs first in every frame, before any layout read.
- **Touch, RM, No JS:** native scrolling.

**21. "Stage opens"**

- **What and where:** the dark Reels band scales up from 95.5% as it arrives. This is a CSS scroll-driven animation (Chromium 115+), desktop only.
- **Fallback:** static.

## Performance

**Desktop.** Loops sleep when nothing moves. All animation loops pause when off-screen or when the tab is hidden. Motion uses `transform` and `opacity` only. Compositor layers are only promoted while an element is active, and the headline animations are released once they have played.

- Compositor layers on desktop: **58 for M2 vs 48 for the base page.**

**Mobile.** Measured at 390 px with 4x CPU throttling (CDP `Emulation.setCPUThrottlingRate 4`), using requestAnimationFrame frame times while scrolling the whole page:

| | Average fps | p95 frame | Worst frame | Frames over 50 ms |
| --- | --- | --- | --- | --- |
| M2 | **57.4** | 16.8 ms | 33 ms | 0 |
| Base page | 59.2 | 16.8 ms | 67 ms | 1 |

**Backdrop filters on mobile:** at most 4 (the nav, the mobile bar and the glass step thumb, plus the intro lens while it runs). The limit is 8.

**Accessibility.** Focus rings are untouched. The custom cursor never hides focus or text selection. Every new button is at least 44 px and has an `aria-label`.
