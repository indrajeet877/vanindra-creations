# VanIndra Creations — Round 3 — "One Dot" (bilingual wordmark)

## Public story (one sentence)
One gold dot sits exactly where Van (forest) becomes Indra (sky), and it lands in the same place whether the name is written in English or in Hindi, because everything we make is built around one point: where your audience looks first.

## The idea, in the drawing
- The identity is the name, not a symbol. `vanindra` (Latin lowercase) and `वनिंद्रा` (Devanagari) are drawn as one lettering system.
- In both scripts there is exactly one dot, and it sits over "ni": the i-dot in `vanindra`, the anusvara in `वनिंद्रा`. Both dots belong to Indra (the i of *indra*; the nasal of *इंद्र*), so the dot marks the seam where Van ends and Indra begins.
- That dot is the only gold in the whole identity. It is the focus point, the first three seconds.
- Every Latin top is flat on the x-height, so the letters hang from an invisible line. In the Devanagari that same line is drawn as the shirorekha. The one-line bilingual lockup shows this directly: the Hindi headline continues the Latin x-height, and both dots float at the same height. In the stacked bilingual lockup the two dots fall on one vertical axis, and the `a` bowl sits directly above the `व` bowl.
- No V, no container, no ornament, no headline bar over the Latin.

## Construction (all parametric, `od.py` + `system.py`, booleans in skia-pathops)
- Units: Latin x-height X = 500. Stem S = 96. Thin T = 48 (contrast 0.5). Rounds are 1.05 S.
- Flat tops, round bottoms. Squircle bowls use k = 0.70 on top and 0.56 at the bottom, with a 9-unit overshoot below. The a, d and व bowls join their stem with a flat top.
- One arch. It leaves the stem with a square shoulder and lands with a round one (apex at 0.56). The same arch makes n, r, the Devanagari i-matra (kamaan) and the न shoulder.
- One bowl: a = d = व.
- One pair of diagonals: the v (down-right heavy, down-left light), mirrored as the inverted-v legs of द्र.
- One dot: a circle 140 units across (1.46 S). It sits 60 units above the line in both scripts, and its top lands exactly on the d ascender (700).
- Devanagari: headline top H = 550 (1.1 X), headline 58, dandas = S. Words are set on a continuous shirorekha with a 34-unit left overhang. In every lockup the Devanagari is set at the same scale as the Latin.
- The descriptor `creations` is drawn in the same system: book weight (S 74) in the stacked lockup, light weight (S 58) in the horizontal lockup. Its i-dot is always ink, never gold. No tracked capitals anywhere.
- The `ni` mark is the wordmark's own n and i, set a little tighter (1.6 × the side bearing) so the pair reads as one unit.
- Small cut (`mark_small`, `wordmark_small`): S 108, T 68, dot 160, wider spacing.

## Size rules (which file at which size)
| Use | File | Rule |
|---|---|---|
| Website header, desktop | `header_wordmark_on_ivory.svg` / `parts/wordmark_*.svg` | Wordmark alone, 36–56 px tall (x-height 20–30 px). See `header.png`. |
| Website header, phone | same | 24–32 px tall. Below 160 px wide, switch to `wordmark_small.svg`. |
| Full name (decks, invoices, footer) | `lockup_horizontal_*.svg` / `global.svg` | At least 240 px wide on screen and 60 mm in print. The light `creations` must not go smaller. |
| Square / portrait formats | `lockup_stacked_*.svg` | At least 140 px wide. |
| India-facing (Hindi audiences) | `lockup_bilingual_*.svg` (stacked), `lockup_bilingual_line_on_ivory.svg` (one line) | At least 220 px wide, with the Devanagari headline at least 12 px tall. Optional, never mandatory. |
| Instagram profile (110 px), app icon, ≥ 96 px | `mark_on_emerald.svg` | The master `ni`. |
| Round avatars 32–64 px (comments, stories ring) | `mark_small_avatar_on_emerald.svg` | Circle-safe small cut. |
| Favicon 16 / 24 / 32 / 48 px | `mark_small_on_emerald.svg` (or `mark_small.svg` on light) | Never use `mark_small` above 64 px. Never use the master `mark` below 96 px. |
| Hindi-only campaigns | `mark_hindi_on_emerald.svg` (`निं`) | Alternate avatar only. Same dot, same place. |
| Reel credit | `parts/edit_by_ivory.svg` on an emerald tab | Credit text at least 40 px tall on a 1080-wide cover, on a flush-left tab inside the 3:4 grid-safe zone (top-left, about 270 px down). See `reel_tag.png`. |
| Embroidery, foil, deboss | `wordmark_small.svg`, `mark_small.svg` | Wordmark at least 70 mm wide (hairline ≥ 1 mm). Below that, use the `ni` small cut. |
| Abroad / USD workspace | `global.svg` | Latin only. Identical to the horizontal lockup, because the system is global by default. |

Clear space: 0.6 × the x-height around the wordmark and the lockups (built into the files). For the `ni` mark the square box is the clear space.

## Colour rules
- On ivory: emerald `#0B2A20` letters and an antique-gold `#A8843A` dot. On emerald: ivory `#F6F1E7` letters and a soft-gold `#D2B26A` dot.
- The dot is the only gold. Never colour any other letter, and never colour the `creations` i-dot gold.
- One colour (all emerald, all ivory or all gold) is allowed. The dot then takes the letter colour (`mark_one_colour_gold.svg`).
- Flat colour only: no glow, halo, gradient or foil effect on the dot.

## Lockup rules (Round 2 failures, checked)
- No stutter. The `ni` mark is never placed beside the wordmark. Horizontal = wordmark (+ `creations`).
- No tracked Jost CREATIONS. `creations` is drawn in the same system or left out. The primary is `vanindra` alone.
- No decorated V. There is no V symbol at all.
- The idea is in the drawing. The dot sits on one axis or one height in both scripts, and the flat top line is visible without a diagram (see `construction.png` for the details only).
- Small sizes: `ni` holds at 16 px (pixel zoom checked at 16/24/32/48 on both grounds).
- No faux-Devanagari: there is no bar over the Latin. The Devanagari is drawn letter by letter, not set in Tiro, and it is optional.

## Small-size behaviour
At 16 px `ni` is about 7 px of n, a 1.5 px i and a 3 px gold dot. It stays legible and the dot is still visible, and it is clearest on emerald. At 24–48 px the square shoulder and the hairline arch begin to show. Below about 14 px x-height the master wordmark's hairlines (0.5 S) thin out, so `wordmark_small` takes over.

## Risks (honest)
1. `ni` is not the initials. Some Hindi/Hinglish readers know "ni" as chat slang for *nahi* ("no"). Recognition depends on people having seen the wordmark. Always pair the avatar with the @vanindracreations name. The `निं` alternate and the full wordmark are fallbacks.
2. A coloured i-dot is a familiar logo device. Ownability rests on the custom letters and the bilingual match, so never put the gold dot over a stock font.
3. The Devanagari was drawn by a non-native designer. **It must be verified by the team** (ideally a native type designer) before any public use: the द्र conjunct (inverted-v ra legs), the न shoulder, the closed व bowl (so it does not read as ब or प), and the i-matra's reach and anusvara placement.
4. A gold dot over Devanagari can be read as a "bindu" with spiritual meaning. It is the anusvara, an ordinary spelling mark (as in हिंदी), over निं, not the वं syllable. Never call it a bindu, never give it a glow, and never use the dot alone over व.
5. Antique gold on ivory is about 3.2:1 contrast. At 32 px and below on light grounds the dot weakens, so favicons and avatars use the emerald ground.
6. The stacked bilingual lockup is set on the dot axis, so the Hindi line is indented and some viewers may read it as off-centre. Use the one-line bilingual lockup for centred layouts.
7. The lowercase wordmark drops the camel-case "VanIndra". In running text, keep "VanIndra Creations".
8. A gold dot alone on an emerald circle can recall a flag (a disc on green). Never use the dot without its letters.
9. Hairlines at 0.5 S suit screens. Print, embroidery and foil below 70 mm must use the small cut.
10. The light `creations` in the horizontal lockup is thin below about 240 px wide. Use the wordmark alone there.

## Files
Required: `mark.svg`, `mark_small.svg`, `wordmark.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg`, `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`, `sheet.png`, `sizes.png`, `context.png`, `explore.png`, `reel_tag.png`, `header.png`, `global.svg`, `global.png`.
Extras: `lockup_bilingual_on_ivory.svg`, `lockup_bilingual_on_emerald.svg`, `lockup_bilingual_line_on_ivory.svg`, `wordmark_hindi.svg`, `mark_hindi_on_emerald.svg`, `wordmark_small.svg`, `wordmark_on_emerald.svg`, `mark_small_on_emerald.svg`, `mark_small_avatar_on_emerald.svg`, `header_wordmark_on_ivory.svg`, `construction.png`, `parts/` (transparent pieces for the mocks).
Sources: `od.py` (engine), `system.py` (parameters), `build.py`, `construction.py`, `explore.py`, `present.js`, `ctx.js`, `pngx.js`, `render_all.sh`.
