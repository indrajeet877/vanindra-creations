# Kolam Line — VanIndra Creations, Round 3

## One-sentence public story
Like the kolam drawn at doorsteps across India every morning, our mark is one unbroken line woven around a grid of dots, so every creator stays connected to the next, with one gold jewel held at the centre.

## What you see (no diagram needed)
- **One closed line.** You can trace it with a finger and never lift it. It draws the whole V: down the left side, round the point, up the right side, across into the crotch, round the centre dot and back.
- **Pulli (kolam dots).** Four dots sit inside the line, the way rice-flour dots sit inside a kolam. Three are drawn in the line's own colour and sized to its weight. Only the centre one is gold.
- **The sikku move.** The two inner strands cross once at a right angle and tie a loop round the centre pulli. That loop-round-a-dot crossing is the most recognisable gesture of a sikku kolam, and it is what makes this a kolam and not a decorated letter.
- **Meaning.** One line connects every point, like creators lifting each other through collabs (Indra's Net). The one gold jewel is the client held at the centre. It is pan-Indian, not Hindi-belt: kolam is drawn from Tamil Nadu to Maharashtra and needs no script at all.

## Construction (mark)
- **Grid and visit order.** The mark sits on a 3x3 pulli grid. The line visits four pulli: L (-1,1), R (1,1), C (0,0) and B (0,-1), in the order L, B, R, C, all counter-clockwise.
- **Arcs.** There is one radius, r = 0.30 grid units, for every arc. Each arc is a true circular arc concentric with its pulli: the line keeps one distance from every dot, as a kolam does.
- **Tangents.** Every straight run is a common tangent of two pulli circles, so every join is tangent (G1) by construction (`kolam.py`).
- **Outer edges.** They are the L-B and B-R tangents, on the 2:1 knight's-move diagonal, giving a V opening of 53.13°.
- **Inner strands.** They are the R-C and C-L tangents at exactly 45°. They cross at exactly 90° at (0, r·√2).
- **Arc spans.** The top caps are 161.57°, the point is 126.87° and the loop is exactly 270°. These angles follow from the grid alone; the radius does not change them.
- **Size and weights.** The bounding box is exactly square, 2 + 2r + w in both directions, which suits round avatars. The master stroke is w = 0.13 and the pulli radius 0.08, so the dots match the line weight, as in real rice-flour kolam.
- **Small cut.** `mark_small.svg` is the same topology with r = 0.32, w = 0.26 and no pulli.
- **How it was chosen.** I enumerated 125 symmetric, non-degenerate closed lines on V-shaped pulli sets (`kenum.py`, `kenum2.py`). They were filtered for retracing, lines passing through dots, and V silhouette; 12 are shown in `explore.png`. Rope-style sikku V's read as antlers or a goblet; this topology is the only clean V.

## Construction (wordmark)
- **Lettering.** Lowercase monoline drawn on the same rule as the mark: straight lines and true circular arcs, tangent joins, one stroke weight (`letters.py`). It is not a font.
- **Shared features with the mark.**
  - The v and y diagonals use the mark's own 2:1 slope.
  - The n arches are true semicircles flowing into both stems. Each n is one stroke turning round an invisible pulli.
  - The s spine is the crossing tangent between two circles: the kolam figure-eight, cut open.
  - The i-dot is a pulli.
- **Metrics.** x-height 100, stroke 8, ascender 146. The "creations" stroke is 6 (0.75 of the name). Spacing uses per-glyph side bearings plus a measured optical gap between the kolam V and the "a" of "anindra".
- **"Creations".** It is drawn in the same system, never tracked caps.

## Lockups and the no-stutter rule
- **Rule.** The kolam V never sits next to a word starting with V: **it is the V of the name.** `lockup_horizontal_*` reads "Vanindra creations", `lockup_compact_*` reads "Vanindra", and `lockup_stacked_*` uses a drop-cap kolam V spanning "anindra / creations".
- **Where the mark appears alone.** Avatars, the favicon and the reel credit only.
- **Global (USD workspace).** `global.svg` / `global.png` are identical to the horizontal lockup, on white. The design has no script dependency or headline bar, so it is already global.

## Size rules (which file at which size)
| Use | File | Size |
|---|---|---|
| Favicon, app icon under 48 px, 32 px story ring | `favicon.svg` / `mark_small.svg` (`mark_small_ivory.svg` on dark) | 16–40 px. Never use above 48 px (it looks heavy). |
| Instagram / WhatsApp profile picture (110 px and up) | `avatar_on_emerald.svg` | 56 px and up |
| Mark alone, print, covers, merch | `mark.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_*` | 48 px and up (pulli resolve from 48 px) |
| Desktop website header | `lockup_horizontal_emerald_ink.svg` on ivory (`..._ivory_ink` on emerald) | kolam V 36–48 px tall (header.png uses 44 px) |
| Phone header, tight spaces | `lockup_compact_emerald_ink.svg` | kolam V 22–30 px tall (header.png uses 30 px) |
| Square / poster / deck title | `lockup_stacked_on_*` | 160 px wide and up |
| Reel "Edit by" credit | `tag_edit_by_emerald.svg` (light footage) / `tag_edit_by_ivory.svg` (dark footage) | kolam V at least 20 px on a 540 x 960 cover; inside the 3:4 grid-safe zone |
| Wordmark without symbol (body copy, credits lists) | `wordmark.svg` | x-height 10 px and up |

**Colour:**
- On ivory: emerald line and letters, with an antique-gold jewel.
- On emerald: ivory line and letters, with a soft-gold jewel.
- Gold is only ever the jewel, never text.
- One-colour versions (emerald, ivory, gold) exist for embroidery, foil and stamps.

**Clear space:** at least the height of one pulli loop (0.6 r of the mark) on all sides. The lockup SVGs already carry 0.55x the V height of padding.

## Honest risks
1. **Pareidolia.** Two dots at the top of a downward-pointing outline can read as eyes, with the loop as a nose (a fox face). The pulli were drawn at line weight and coloured the same as the line, with gold only at the centre, to suppress this. But someone will see it. Test with 10 people.
2. **Heart / pendant reading.** The wide 53° V with round top caps, plus the loop, can read as a heart at 16–24 px, or as a V-neck pendant. The deep notch to the crossing keeps the V reading in my tests, but the pendant reading is real. It suits jewellery and saree partners, and is less neutral for doctors.
3. **Still a V.** It is not a decorated V: the V is the path of one kolam line. But the round's brief warned against lone V's, and a judge may still file it under "V marks".
4. **Kolam literacy.** Only 4 of the 9 grid pulli appear. Indian viewers should read kolam from the dot-in-loop and the crossing; viewers abroad will see an elegant one-line V. The idea survives without the story, but the word "kolam" does not.
5. **Wordmark genre.** The custom lowercase is constructed, not a font. It still sits in the geometric monoline family (Futura / Century Gothic light) and could be called generic. Its ownable traits are the 2:1 diagonals, the semicircle arches, the pulli i-dot and the kolam initial.
6. **Casing.** The logo reads "Vanindra creations". The camel-case capital I of "VanIndra" is not expressed, because a capital I between two n's reads as "l". The team must accept lowercase in the logo while writing "VanIndra Creations" in text.
7. **Detail at small lockup sizes.** Below a 22 px V height, the kolam initial's loop and pulli become specks. There, use the compact lockup at minimum size or the wordmark.
8. **Thin strokes under compression.** "edit by" and "creations" are lighter. On heavily compressed Reels, export the credit at least 20 px tall.
9. **Cultural note.** Kolam is an everyday threshold art, and in many households it is also part of morning ritual. It is widely used in secular design, and the mark uses no deity, lotus or ritual motif, but Tamil team members or clients should be comfortable with it.
10. **Devanagari.** This direction deliberately has no Devanagari line. If a bilingual lockup is wanted, it must be drawn in this monoline system and verified by native readers. It has not been drawn.

## Files
`mark.svg`, `mark_small.svg` (+ `_ivory`), `wordmark.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg` (+ `_emerald`, `_ivory`), `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`, `lockup_compact_on_*.svg`, `*_ink.svg` (transparent), `avatar_on_emerald.svg`, `favicon.svg`, `tag_edit_by_*.svg`, `global.svg`, `construction.svg`.
Renders: `sheet.png`, `sizes.png`, `context.png`, `explore.png`, `reel_tag.png`, `header.png`, `global.png`, `construction.png`.
Generators: `kolam.py` (arc/tangent engine), `mark.py`, `letters.py`, `lockup.py`, `build.py` (all deliverables), `compose.js` (context/header/reel), `kenum*.py` (enumeration), `pixzoom.js` (pixel checks).
