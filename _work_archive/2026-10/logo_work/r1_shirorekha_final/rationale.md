# Shirorekha, final: Everything hangs from one line

Round 3 · VanIndra Creations · builds on Round 2's winner T5 Shirorekha

## Public story (one sentence)
In Devanagari every letter hangs from one line, the *shirorekha* ("head-line"), and at VanIndra everything we make hangs from its headline too: the first three seconds.

## The idea, as it shows up in the drawing
- **The line is the brand.** The name hangs from one continuous line. The same line runs on as the rule across a website header (the navigation and the "Book a call" button hang from it), across a deck title, and in from the edge of a Reel cover for the "EDIT BY" credit. Nothing else decorates it. There are no curls, no foil and no ornaments.
- **The mark is व, and its counter is a V.** The avatar is the Devanagari letter **va**, drawn the way it is written. The pen leaves the danda as a hairline, swells into a leaf on the left, comes to a point and returns to the danda. The loop hangs from the danda, and the danda hangs from the line. The white space inside the loop is a clean V. You don't need the construction drawing to see it (construction.png is only supporting material).
- **One stroke grammar for both scripts.** Every vertical is a danda (13 units on a 100-unit cap). Every diagonal or curved stroke is a leaf: a hairline where it leaves the line, full weight at the foot or tip. Bowls are k = 0.60 superellipses. VANINDRA, CREATIONS, EDIT BY and वनिंद्रा are all drawn in this grammar. None of them is typeset.

## Round 2 must-fix list, and what was done
| Judges' must-fix (t5_shirorekha) | Round 3 |
|---|---|
| Mark weight top-right, empty bottom-left, reads as a T or flag in the circle | The bowl is now a leaf-loop whose belly sits on the left (ink is 46% of the bounding box) and the danda is 13. The mark is optically centred: the horizontal centre is blended 45% towards the area centroid (centroid x 41.9 vs box centre 36.8). It fills 54% of the avatar square. |
| Unequal headline overhang (11 left / 7 right), pennant / post-and-beam | The overhangs are 3 and 3, measured from the loop's widest point and the danda. Nothing hangs from the bar on the left any more, so there is no triangle hanging from a beam. |
| White acute sliver where leaf meets bar | Removed by construction: the loop never meets the line. The counter's top-left is a deliberate rounded V corner (M8 in explore_marks.png). |
| Must read as व, not प or ब | A reference study (explore_marks.png, against Martel and Rozha) showed that T5's leaf, hung from the bar, has **प's topology**: in a drawn word it read "पनिंद्रा". In real type, व's loop hangs from the danda and is closed by its own stroke. That is the shape now. There is no inner diagonal, so it can't be ब. A rounded lower third (the judges' fallback) was tested and drifts towards प's U, so it was rejected (M4). |
| N-I-N picket fence, dark clots at N feet | N stems 5.9 → 8.5 (header cut 10.5), N-I and I-N opened 17 → 21 (+24%; header cut 25). The wedge foot was trimmed 16.5 → 13.5, so the diagonal meets the right stem without a clot (checked at 1500 px). |
| Header-size hairlines ghost out | **wordmark_header.svg** is a separate header cut: hairline 5.0 → 7.4, stems 14, wider spacing. It is checked at 28 px and 17 px cap height (header.png). |
| The lone curve (V's leaf) | The leaf is now the grammar, not an exception. It appears in V's left arm, in both A right arms, in the R leg and in the mark. The V leaf was straightened (outer bow 3.5 units). |
| CREATIONS in tracked gold Jost | Removed. CREATIONS is drawn in the same system (danda stems, leaf diagonals, superellipse C/O/S). It hangs from the same line, which steps down to a hairline. The T reads because its own crossbar (6.5 units) is heavier than the hairline (3.6). |
| Horizontal lockup stutters "VI VANINDRA" | **No horizontal lockup contains the mark.** Horizontal = VANINDRA + CREATIONS on one line. The mark appears only as the avatar or favicon, or stacked above the name. |
| Two broken bars of different weight | There is one continuous line everywhere. It is heavy over the name and steps to a hairline over the descriptor. In the global version it is a single uniform gold hairline. |
| Size rules | See below. |
| Samarkan / Indian-restaurant drift | The India master keeps one plain bar of 8.8 and nothing else. The global version replaces the bar with a gold hairline rule, which reads as an editorial masthead, not faux-Devanagari. |
| Redraw वनिंद्रा in the same system, द्र correct | Drawn, not typeset (wordmark_devanagari.svg, lockup_bilingual_*.svg): व is the mark's leaf-loop; ि is a danda plus a tapering leaf hook over न; न has a level hairline from the danda with a hanging leaf; ं is a plain round dot; द्र is a stub flowing into a C-bowl, with द's tail and the rakaar leaving its foot as an inverted V; ा is a danda. **To be verified by the team / a native type reader.** The line is optional and never mandatory. |
| Global version for the USD workspace | **global.svg / global.png**: the same capitals with no headline bar. VANINDRA and CREATIONS hang from one gold hairline (one-colour and on-emerald versions included). global_wordmark.svg is the name only. |

## Construction (units: VANINDRA cap = 100, from the top of the line to the baseline)
- **Mark (master):** line 9.5; danda 13 at x = 58; the loop leaves the danda at y = 20 as a 5.5 hairline; one cubic for the outer edge and one for the counter; tip at (29, 93); the return stroke (10 thick) meets the danda at y = 57; the danda runs on to 100; overhangs 3/3. The whole mark is **two Bézier curves and straight lines** (mark.svg is 345 bytes).
- **mark_small:** line 13.5, danda 16.5, loop top 8.5, return 12.5, a larger counter, overhangs 2/2.
- **Wordmark:** line 8.8; stems 13; hairlines 5.0; N stems 8.5; wedges start at 3.8 and land on 13.5 feet; V overshoots by 1.6; A crossbar at 0.64; overhangs 4/4. The width is 5.96 × the cap height.
- **CREATIONS / EDIT BY:** stems 13, hairlines 7, own top strokes 13. In lockups they are set at 0.50 (header 0.52, Reel tag 0.46) of the VANINDRA cap, hung from a 3.6 hairline.
- Everything is parametric (r3system.py holds every number). Shapes are boolean-unioned in skia-pathops, all text is outlined, and coordinates are rounded to 0.01.

## Size rules (which file at which size)
| Use | File | Size |
|---|---|---|
| Favicon, browser tab, app icons, avatars ≤ 48 px | `mark_small.svg` | 16 to 48 px. **Never above 64 px** (it is deliberately heavier). |
| Instagram / WhatsApp profile picture (110 px circle and up), app splash, social cards | `mark_on_emerald.svg` (gold on emerald) or `mark_on_ivory.svg` | 56 px and up. **Never below 48 px**: the lid and the return stroke thin out. Between 49 and 55 px, use mark_small. |
| Website / app header, email signature, Reel credits | `wordmark_header.svg` (name only) or `lockup_horizontal_header.svg` (full name) | VANINDRA cap 12 to 40 px. Full name only when the cap is ≥ 24 px (CREATIONS ≥ 12 px). Phone header: wordmark_header at a 17 px cap. |
| Print, decks, signage, video end cards | `wordmark.svg`, `lockup_horizontal_on_*.svg` | VANINDRA cap ≥ 40 px. |
| Formal / vertical formats (cover pages, letterhead top, merch) | `lockup_stacked_on_*.svg` | Lockup width ≥ 160 px. |
| Hindi-market extras (optional) | `lockup_bilingual_on_*.svg`, `wordmark_devanagari.svg` | VANINDRA cap ≥ 30 px. Never mandatory: omit for South Indian and international clients. |
| USD workspace, English-speaking markets | `global.svg` (gold hairline), `global_one_colour.svg`, `global_on_emerald.svg`, `global_wordmark.svg`; `global_header.svg` for headers | global.svg: VANINDRA cap ≥ 28 px; global_header.svg: 14 to 28 px cap (at 20 px the master cut's hairlines and gold rule get faint). |
| Reel / video credit | `reel_tag_ivory.svg` / `reel_tag_emerald.svg` | On a 1080 × 1920 cover: VANINDRA cap 40 px, the line entering from the frame edge, inside the 3:4 grid-safe band (below y = 240). |

Clear space: the VANINDRA cap height on all sides of any lockup, and a quarter of the mark's height around the mark. Colour: one colour wherever possible (emerald on ivory, ivory or soft gold on emerald). Gold is used only for the global hairline and the avatar mark on emerald. No gradients, foil, shadows or outlines.

## Using the line (the system)
The line can run on: across a header (header.png), across a deck title, or in from the edge of a Reel cover (reel_tag.png). Titles and labels hang from it, top-aligned. The line has only two weights: the heavy line, which is only ever over VANINDRA, and the hairline, for everything else. It is never decorated, curved, doubled or animated into a swoosh.

## Files
mark.svg, mark_small.svg, wordmark.svg, wordmark_header.svg, wordmark_devanagari.svg, mark_on_ivory.svg, mark_on_emerald.svg, mark_one_colour_gold.svg, lockup_horizontal_on_ivory.svg, lockup_horizontal_on_emerald.svg, lockup_horizontal_header.svg, lockup_stacked_on_ivory.svg, lockup_stacked_on_emerald.svg, lockup_bilingual_on_ivory.svg, lockup_bilingual_on_emerald.svg, global.svg (+ global.png, global_on_emerald.svg, global_one_colour.svg, global_wordmark.svg, global_header.svg), reel_tag_ivory.svg, reel_tag_emerald.svg.
Renders: sheet.png, sizes.png, context.png, explore.png (9 system directions), explore_marks.png (8 mark studies against Martel / Rozha references), construction.png, reel_tag.png, header.png, loops/ (refinement loops 1 to 4).
Generators: r3geo.py, r3mark.py, r3latin.py, r3deva.py, r3system.py, build.py, explore.py, explore_marks.py, reel_tag.py, header.py, construction.py.

## Explored and rejected
- E2 open notch: reads as a glitch. E4 line only over the V: turns the V into a funnel. E9 / M4 rounded lower third: drifts to प.
- M1 to M3 (T5 lineage, notch, gap under the line): all keep प's topology; in a drawn word the first letter read as प.
- M5 straight-lidded loop: correct व, but reads as a pennant. M6 / M7 thin or round loops: weak, or read as a Latin "a".
- Two-tier CREATIONS under a second rule: reads as an underline and adds a second line.

## Honest risks
1. **The V is now quieter.** Hindi readers get an orthographically sound व. Latin readers get the V mainly through the counter and the pointed tip. At 16 to 24 px some will just see "a drawn letter" (or a lowercase a with a macron) rather than a V. Since the mark never appears without the name, this is acceptable, but it is a trade-off made on purpose against Round 2.
2. **Native verification is still required.** The व was checked against Martel, Noto Serif and Rozha, but the drawn वनिंद्रा (द्र proportions, the length of the ि hook, the position of the anusvara) was drawn by a non-native designer. **To be verified by the team** before any public use.
3. **CREATIONS hangs top-aligned.** At a glance it can read as a superscript. The stepped hairline is what explains it, so it must never be deleted. Below a 24 px cap, drop CREATIONS.
4. **Faux-Devanagari drift** remains possible in the India master (a heavy bar over Latin capitals) if someone adds ornaments, foil or 3D. The global hairline version exists for that reason.
5. **Two densities:** the mark is heavy (a display letter) and the wordmark is fine (high contrast). They never sit side by side horizontally, but in the stacked lockup the contrast is visible by design.
6. **Regional readings:** Bengali readers will see ব (ba / va, the same letter family, harmless). South Indian and foreign audiences see a drawn glyph. Hindi-belt connotations are kept optional (no Devanagari line by default).
7. **Production:** the geometry is generated parametrically. A final pass in a vector editor (point placement, a hand-hinted 16 px ICO) and a print proof of the 3.6-unit hairline at small print sizes are recommended.
8. The running line in templates is a usage rule. If designers start putting heavy bars everywhere, the line turns into decoration. The rule is two weights only, and the heavy one is only over the name.
