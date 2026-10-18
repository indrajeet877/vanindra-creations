# F1 "Matched hinge" · VanIndra wordmark (built from c3 "Emerald and Gold Leaf")

**Idea.** One word, two materials, one hinge. "Van" (the forest) is a humanist italic in solid forest-ink
emerald; "Indra" (the sky king) is a Didone cut in emerald glass with its capital I alone in antique gold.
The two are not merely different: their stems are measured and matched (V and d within 3 %), and the n's
foot and tail are re-drawn as a gold hinge that physically runs into the I's stem, whose left foot serif
is deleted so the stroke arrives clean. The eye reads the stroke turning gold as it rises: **VanIndra**.

## What changed since c3 (every final-round finding, resolved)
| Finding | Done |
|---|---|
| Heavy Van + faint ndra; two words | Van dropped from Cormorant 700 to **650**, ndra raised from Bodoni 500/opsz 36 to **600/opsz 18**. Measured: V thick stroke 15.6 u, d stem 16.0 u (2.9 % apart), I stem 17.5 u, hairlines 2.2 u (1.7 px at 480 px). Nav cut: Van 700 + Bodoni 640/opsz 11 (V 16.8, d 17.1, 2.1 %) |
| Join was a sliver short of the stem, colliding with the I's left foot serif | **Real ligature.** The I's left foot serif is deleted (top serif kept so the I still reads as I). Indra is placed so the n's tail enters the stem by 3.5 u (OVERLAP). The n's foot is cut with a pen-lift line rising at 22°, so gold starts where the stroke turns to rise (≈ 0.2 cap back from the stem) and the whole tail + the foot's underside is gold. The tail is re-drawn as a ribbon that keeps the font's thickness at the foot and stops tapering at 4.6 u (5.8 u nav), so the hook survives at 28 px. The gold is ONE path (n-foot ∩ cut ∪ hinge ∪ custom I), built with boolean ops, so flat/white files are identical geometry in one colour |
| Hairlines cannot carry glass; gold-lit bottom rim = underline by the side door | opsz-36 cut retired. Gold rim deleted; bottom serifs are letter colour with only a deep-emerald shadow rim at 42 % |
| Washed-out glass on ivory, near-white top stop | Base stops **#2E9670 → #1C7A58 → #0B4A36** at 0.97 alpha (no white stop). Measured mean of the glass letter pixels on #FAF8F3: **4.25:1** |
| Satin ribbon / Canva gold effect (diagonal band + gold rim + bulge + dispersion) | All removed. Glass = base + ONE hard-edged specular plane at a fixed angle per word (gradient with a crisp 0.2 % stop) + a soft inner light pooled at the top of each bowl (per-glyph blurred ellipse, clipped) + a crisp top-left rim that fades out after the top-left quarter + contact shadow. No feSpecularLighting, no feTurbulence, no colour-split stroke |
| Gold I too pale on ivory | Antique range **#C9A646 → #B9953B → #8F6B16 → #6E5010** with a 1 u #6E5010 edge. Measured I-stem mean RGB (146,112,30): **4.34:1** on ivory. On deep ground champagne (7.3:1); `logo_mid.svg` uses a lighter champagne (3.54:1 on #0E6B4E) |
| ndra vanishes on mid emerald | `logo_mid.svg`: mint glass #CDF5E2 → #93E2BE → #5CC79A, ivory Van. Measured **3.63:1** on #0E6B4E (worst decile 3.07:1) |
| r's floating bead | Bodoni 600/opsz 18 connects the ball with a 2.8 u hairline; it no longer floats |
| Mark reads "nl"; favicon a blob; thin box outline | `mark.svg` = the hinge monogram (n + gold hinge-I, right serifs kept) for 48 px up; `mark_tile.svg` = solid gold Bodoni I on an emerald disc for 16–32 px avatars; `favicon_32.svg` = gold I on an emerald rounded square, drawn on whole pixels at 16 px, **no outline** |
| Three typefaces, wedding register | Jost dropped. CREATIONS is **Bodoni Moda small caps** (wght 600 / opsz 11, +0.26 em). Two families total; gold only on the I and the hinge (≈ 8 % of the mark) |
| ndra too far from the I | The n of Indra pulled 2.5 u towards the I (IN_PULL), tracking +1.8 % elsewhere |
| Display cut below 48 px; lockups | Hero cut (opsz 18) is used only at ≥ 160 px wide. Everything ≤ 48 px (`logo_nav*`, `mark*`, flat/white) is the sturdy cut (opsz 11). Lockups are display files: use at ≥ 160 px wide |

## Type and colour
| Part | Face | Colour |
|---|---|---|
| Van | Cormorant Garamond Italic wght 650 (700 in nav), slant reduced 2.5°, outlined | #0F5C44 → #0A3A2B (ivory) · ivory #FAF8F3 → #E8E2D2 (dark, mid) · nav ink #0A1E17 |
| ndra | Bodoni Moda wght 600 / opsz 18 (640 / opsz 11 in nav), outlined | glass #2E9670 → #1C7A58 → #0B4A36 (ivory) · #7FD9AE → #36A97E → #157A57 (deep) · #CDF5E2 → #93E2BE → #5CC79A (mid) · nav flat #0E6B4E |
| I + hinge | Bodoni Moda I (left foot serif removed) + the n's foot/tail ribbon | antique #C9A646 → #8F6B16 → #6E5010, 1 u #6E5010 edge (ivory) · champagne #F6EBC6 → #C9A646 → #8E6A14 (deep) · nav flat #8A6612 (4.96:1) |
| CREATIONS | Bodoni Moda small caps 600 / opsz 11, +0.26 em | ink #0A1E17 at 82 % (ivory) · ivory at 90 % (dark) |

## Files
- `logo.svg` primary (ivory, glass, CREATIONS). `logo_on_dark.svg` for #09241B. `logo_mid.svg` for #0E6B4E.
- `logo_flat.svg` one colour #0E6B4E, `logo_white.svg` one colour #FAF8F3 (sturdy cut, no effects).
- `wordmark.svg`, `wordmark_on_dark.svg` hero wordmark without CREATIONS; letter art grouped `#lg-ndra`, `#lg-van`, `#lg-i` for the website animation.
- `logo_nav.svg` (ivory nav: ink Van, emerald ndra, antique gold I; no gradients, no filters), `logo_nav_on_dark.svg` (gradients + two masks, no filters), `logo_nav_flat.svg`, `logo_nav_white.svg`: sturdy cut, 24–48 px tall, same `lg-*` groups in the first two.
- `lockup_horizontal.svg` (+`_on_dark`) CREATIONS right-aligned; `lockup_stacked.svg` (+`_on_dark`) CREATIONS centred.
- `mark.svg` hinge monogram (48 px up; antique gold on ivory), `mark_flat.svg`, `mark_white.svg`. `mark_tile.svg` gold I on an emerald disc (avatars 16 px up).
- `favicon_32.svg` 32-unit grid; `favicon.ico` 16 + 32 + 48 (PNG entries, transparent corners).
- `og_logo_1200x630.png` share image. `sheet.png`, `in_use.png`, `join_closeup.png` (4×: ivory, deep, mid) previews.
- `build/` regenerates everything: `./all.sh` (build.py → sheet.py → Playwright → ico.py); `report.py` prints the measurements; `join.py`, `small.py` the inspection renders. `fonts/` has the three variable fonts used.

## Size rules
| Size | File |
|---|---|
| hero, print, ≥ 160 px wide | `logo.svg` / `logo_on_dark.svg` / `logo_mid.svg` / `wordmark*.svg` / lockups |
| nav 24–48 px tall | `logo_nav*.svg` only (the glass files never below 48 px) |
| avatar / app icon 16 px up | `mark_tile.svg` |
| tab icon | `favicon.ico` / `favicon_32.svg` |
| monogram 48 px up | `mark.svg` |
| one colour, embroidery, stamp | `logo_flat.svg` / `logo_white.svg` |

## Measurements (build/report.py)
- Hero stems (cap = 100 u): V 15.6 u vs d 16.0 u → **2.9 %**; I 17.5; Van n 11.8/12.6; Indra n 14.6/15.9. Sturdy: V 16.8 vs d 17.1 → 2.1 %.
- Hairlines: 2.16 u = 1.7 px at 480 px wide; nav cut 3.23 u = 0.7 px at 28 px, 1.0 px at 40 px.
- Gold I on #FAF8F3: 4.34:1 (stem pixel mean). ndra on #FAF8F3: 4.25:1 (letter-pixel mean; 4.36 across all four letters). ndra on #0E6B4E (`logo_mid.svg`): 3.63:1, worst decile 3.07:1. Gold I on #0E6B4E: 3.54:1. Nav flat: gold 4.96:1, emerald 6.12:1.
- 28 px: rendered and inspected at 4× (build/render/small_x4.png): the word reads VanIndra, the gold foot shows as a 2 px hook under the n, hairlines hold at 0.7 px with anti-aliasing.

## Live glass plan (website)
**Default (every browser, no WebGL, no backdrop-filter):** inline `wordmark.svg` once (≈ 11 KB). Its three groups
(`#lg-van`, `#lg-i`, `#lg-ndra`) are animated with CSS `transform` and `opacity` only (entrance: van slides in, the
hinge-I drops 6 px and settles, ndra fades up 120 ms later). A moving light is added as ONE extra element inside
the ndra clip: a `<radialGradient>`-filled rect whose gradient `cx`/`cy` attributes are set from a single
`pointermove` listener throttled to `requestAnimationFrame` (on touch it idles on a slow 12 s CSS keyframe of a
CSS custom property that drives `cx` via JS, never a SMIL or gradientTransform animation). Nothing with a filter
is ever animated; `feGaussianBlur` on the pooled light paints once. `prefers-reduced-motion` stops the light.
**Not used by default:** `backdrop-filter` (an opt-in class `.vi-refract` adds a masked `backdrop-filter: blur(6px)`
layer only on desktop Chromium/Safari when the hero ring is present, and the page works identically without it).
**Never:** animate `gradientTransform` (Safari/Firefox repaint cost and SMIL inconsistencies), animate any filter,
scale the glass file below 48 px, or put champagne gold on ivory (ivory nav uses antique #8A6612).
**Optional WebGL pass:** same rule as the hero ring: when WebGL exists, one quad behind the SVG uses the ndra alpha
as a texture for a moving Fresnel light; the SVG stays on top for crisp edges, and GPU-less phones see the static logo.

## Open points (honest)
- The hinge enters the stem low (0.08–0.13 cap): a true cursive join, but at 28 px it reads as a gold foot touching
  the I rather than a sweeping hook. A taller hook would need the stem's bottom-left to flare, which read as a boot.
- The hinge monogram `mark.svg` still depends on the I's right serifs to say "I"; below 48 px use `mark_tile.svg`.
- The 1 u dark edge on the gold I is visible as an outline at 1400 px and above; drop `stroke-opacity` to 0.6 for print.
- The ivory glass is translucent by stops and the pooled light, not by alpha inside the bowls (0.97 everywhere): the
  engineer's 0.82 would have cost the ≥ 3:1 the Indian pair asked for; I kept contrast.
