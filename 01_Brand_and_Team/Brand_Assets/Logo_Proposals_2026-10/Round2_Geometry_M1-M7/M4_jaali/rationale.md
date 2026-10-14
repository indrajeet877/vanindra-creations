# The Jaali Stroke — VanIndra Creations (territory: Jaali)

## Concept name
**The Jaali Stroke**

## One-sentence public story
Our V is one point of a Mughal eight-point jaali star: on its own it is our initial, eight of them lock together into the star, and a screen of stars becomes the jaali, the way creators grow stronger together.

## The idea
In Mughal jaali geometry the eight-point star ({8/3}) has a 45-degree point, and that point is a V. When the classic octagon-and-square jaali is drawn with a 67.5-degree contact angle (Hankin's "polygons in contact" method), **every point in the whole screen is the same 45-degree V.** So the mark is not decorated with a jaali. It is the stroke the jaali is made of.
- **Mark:** one V-unit, cut out of the star.
- **Seal:** eight V-units locked into the star (`seal_rosette_on_emerald.svg`).
- **Canvas:** stars on the octagon grid form the full jaali (`pattern_jaali_on_emerald.svg`). It works the way a maison monogram canvas does (a mark plus a proprietary pattern).
- `construction.svg` shows the derivation.

## Construction notes (all from one 22.5-degree grid; generator: `final_build.py`)
- The star is {8/3} with outer radius R = 100 and inner radius ratio cos(67.5°)/cos(45°) = 0.5412. The point angle is 45°.
- The V-unit is a band of thickness t = 9 drawn inside the star outline, kept between the two radii through the notches (247.5° and 292.5°). The angled terminals are therefore the real joints where the next star point would begin.
- A hairline split (0.85) runs on the radius through the tip (270°). **All three cuts in the mark point to the same centre: the centre of the jaali star.** The split also reads as the two halves of one point (Van + Indra), and it suggests a writing nib (scripting).
- The mark's proportion is w/h ≈ 0.66. The counter depth is about 59% of the height.
- Optical corrections: the mark sits 1.2% below geometric centre in the squares, because a V carries its mass high. In the lockup, the points overshoot cap height by 2.8% of mark height and the tip drops below the CREATIONS baseline by the same amount. Mark height is 1.07× the text block.
- **Wordmark:** Marcellus 400, outlined. This flared inscriptional serif suits the carved-stone source and is less worn than Cinzel or Trajan. Spacing is optical: scanline profiles of each letter (depth clamp 0.30 cap) give every pair the same mean white gap of 0.40 cap. Pair corrections are VA −0.07, AN −0.02, RA −0.04 and DR +0.01. CREATIONS is set at 0.31 cap with a 0.98 cap gap, centred, in antique or soft gold.
- **Seal:** eight units with 2.4 radial slits, each carrying the axial split (16 facets).
- **Canvas:** Hankin 4.8.8 with a 67.5° contact angle. Octagon stars are made of 8 units and square stars of 4 units, so every point is the brand V.

## Small-size behaviour
- `mark_small.svg` is a heavier unit (t = 11.5, about 28% bolder). It drops the hairline and is set in antique gold #A8843A, so one favicon works on both light and dark browser chrome. It reads cleanly as a V at 16, 24 and 32 px (see `sizes.png`).
- The full mark's hairline becomes visible from about 90 px up. At the 110–150 px Instagram size it shows as a fine seam, and the V itself never depends on it.
- The seal and the canvas are not for sizes below 64 px.

## Risks / honest weaknesses
- Seen on its own, the mark reads mainly as a refined, sharp V. The jaali story is fully visible only next to the construction, seal or canvas, so the system has to be shown together for the idea to land.
- The territory asked for a jaali motif carving through a bold V. This answer derives the V from the jaali instead. Fully pattern-filled V variants were explored (see `explore.png`) and rejected as ornamental and template-like.
- The split can be read as a pen nib or as two leaves. That is mostly welcome, but it is a known monogram move.
- The seal is an eight-point star. Some viewers may read it as a generic or decorative star, or as Islamic-pattern specific. It works best as a secondary device, not as the profile picture.
- The wordmark is a free font, customised only by spacing. A fully drawn wordmark would raise ownership.
- The horizontal lockup shows V twice (mark plus the wordmark's initial). This is common practice, but some will find it redundant.
- No Devanagari version is supplied. Any Devanagari use (वनिंद्रा) is to be verified by the team.

## Files
`mark.svg`, `mark_small.svg`, `wordmark.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg`, `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`, plus `construction.svg`, `seal_rosette_on_emerald.svg`, `pattern_jaali_on_emerald.svg`, `mark_small_on_emerald.svg`. Renders: `sheet.png`, `sizes.png`, `context.png`, `explore.png`.
