# Shirorekha, final: Everything hangs from one line (final-final polish)

Round 3 finalist polish for the team vote. VanIndra Creations. It builds on `r1_shirorekha_final` (judges: 7 / 7 / 7). Everything the judges said works has been kept: the one running line, the drawn VANINDRA alphabet, the bilingual line, the 1440 header with the navigation hanging from the rule, the editorial Reel credit and the gold-hairline global version. Every must-fix item below was worked through at least three times (render, look, critique, revise). The loop renders are in `loops2/` and the studies are in `explore_final.png`.

## Public story (one sentence)
In Devanagari every letter hangs from one line, the *shirorekha* ("head-line"), and at VanIndra everything we make hangs from its headline too: the first three seconds.

## The idea, as it shows up in the drawing
- **The line is the brand.** VANINDRA hangs from one heavy line. The same line steps down to a hairline and runs on:
  - over CREATIONS,
  - across a website header as the page rule (the navigation and "Book a call" hang from it),
  - and under "EDIT BY" in a Reel credit, before it steps up again for VANINDRA.

  It is never decorated, curved, doubled or turned into a swoosh.
- **The mark is व, and now it is a V twice.** The loop hangs from the danda, as व does in type, and never from the line, so it can't be read as प. The white counter is a V. In this pass the outside of the loop is also a V. A round shoulder sits under the line. A near-straight left arm runs down to a sharp point, and the return stroke is the V's right arm. The danda runs on below the point, so the shape reads as a letter, not a pennant. `construction.png` shows both Vs, but you can see them without it.
- **One stroke grammar for both scripts.**
  - Verticals are dandas.
  - Diagonals are leaves: a hairline where they leave the line, full weight at the foot.
  - Bowls are k = 0.60 superellipses.
  - C and S are drawn with a contrast pen: full weight when the stroke travels vertically, hairline when it travels along the line.

  VANINDRA, CREATIONS, EDIT BY and वनिंद्रा are all drawn this way. None of them is typeset.

## Round 3 judges' must-fix list, and what was done

| Must-fix (judge) | Done in this pass |
|---|---|
| CREATIONS reads as a superscript ("VANINDRA^CREATIONS"), top-aligned on a hairline step (all three) | **CREATIONS now stands on VANINDRA's baseline** at 0.55 of the cap, under the same line. That is the CD's own alternative. The superscript is gone in `lockup_horizontal_*`, `lockup_horizontal_header.svg`, `global*.svg` and `context.png`. The **recommended website header drops CREATIONS** (India and global judges). The stacked lockup carries it centred under VANINDRA. |
| The heavy bar steps down exactly over the last A's apex, so the A looks clipped (global) | The step now falls in the **middle of the gap between A and C**, never over a letter. It is marked by a gold tick in construction.png. |
| CREATIONS S has a spur or notch at the lower-left terminal (CD, global) | The S has been **redrawn as one continuous contrast-pen stroke** (six G1 cubics, smoothed weight). It has no seams and no spur, and it was checked at 4000 px. The lower bowl is optically larger (spine at 0.49). |
| CREATIONS is a stock condensed grotesque: flat-cut C and S, no contrast, no leaf diagonals (CD, India) | **A, R and N use VANINDRA's own constructors** (leaf right arm on A, leaf leg on R, swelling N diagonal) at reduced contrast. **C and O have real contrast** (full sides, hairline top and bottom). The C is the O ring opened by a radial wedge, so its terminals are angled cuts, not flat verticals. The S uses the same pen. The weight was retuned so that at 0.55 its colour matches VANINDRA. |
| The mark reads as a lowercase "a" with a macron at 16–110 px. The V survives only as the counter (all three) | **The silhouette is now a V.** The round belly has become a shoulder plus a near-straight arm that ends in a sharp point. The point sits at 95 and the danda runs on to 100. The loop still never touches the line. At 16 / 24 / 32 px (sizes.png) the outer shape ends in a point. **Rule:** the व mark is the India and Hindi avatar only. It is never used alone in the USD workspace (see "Global" below). |
| Add a Latin-led avatar for South Indian and global accounts (India), or keep the mark out of USD use (CD, global) | **`mark_global_on_emerald.svg` / `_on_ivory.svg` / `mark_global_small.svg`.** The line runs full-bleed across the avatar, off both edges of the circle crop, and the system's leaf V hangs from it. A V under a short bar was tested and rejected because it reads as a nabla (∇) (`loops2/gav2.png`). |
| Stacked lockup: the mark's danda and bar are about three times the wordmark's weight, giving two densities and two unrelated bars (CD, India) | There is a new **lockup cut of the mark** (`mark_lockup.svg`). At its stacking scale (1.85×) its strokes are within 20–30% of VANINDRA's in absolute terms, down from two to three times:

| Stroke | Lockup mark | VANINDRA |
|---|---|---|
| Line | 11.5 | 8.8 |
| Danda | 15.5 | 13 (I stem) |
| Loop hairline | 6.3 | 5.0 |

The small excess is optical compensation, so the larger glyph has the same density. The two bars now rhyme in weight instead of competing. |
| Phone header at a 17 px cap: V and A hairlines are half-tone single pixels; the N verticals give "VA-IIII-DRA" (CD, global) | There are now **two new cuts.** `wordmark_header.svg` is the sturdy cut: hairline 10.2, stems 16, N stems 12, so 1.7 px at a 17 px cap and 2.9 px at 28 px. `wordmark_phone_17px.svg` is **pixel-fitted** to a 17 px cap: every letter origin, stem and the line sit on whole pixels, the N stems are 2 px, the I / D / R stems 3 px and the hairlines 1.7 px. Checked at 7× (header.png). The N diagonal is now heavier than the N stems, so N reads as N. |
| Hairlines ghost at real size: 28 px desktop header and Reel tag (global) | The desktop header, context.png header bars and the Reel credit all use the sturdy cut. No stroke in them is under 1.5 px. |
| Embroidery: at 70 mm with a 1 mm stitch, both wordmarks lose V and A hairlines; needs a cut with hairlines around 1.6% of the word width (global) | The sturdy cut's hairline is **1.63% of the word width** (10.2 / 626). At 70 mm that is 1.14 mm. Size rule: embroider VANINDRA at 62 mm wide or more. |
| Global version: the caps stand clear of the gold hairline, so "hangs from one line" isn't visible (global) | The caps now **overlap the hairline by 55% of its thickness**, so they touch. The old exact-touch left an anti-alias seam, which is gone (checked at 5×). |
| Reel tag: the hairline bleeds off the frame edge and looks like a crop error (CD, India); EDIT BY is grey, about 9 px, a stock sans, about 3:1 contrast (CD, India) | **The line starts at the E of EDIT BY**, on the safe margin (30 px on 540, 60 px on 1080). EDIT BY stands on the hairline and the line steps up to the heavy bar that VANINDRA hangs from. EDIT BY is **drawn in the system** (credit cut: stems 2.2 px, hairlines 1.6 px at a 10.5 px cap) in **ivory**, and VANINDRA uses the sturdy cut. The credit sits inside the 3:4 grid crop. |
| वनिंद्रा: the न tick is too long and drifts toward त (India); the anusvara floats right of the ि tail (CD, global); द is an open "c" on the ra legs with no entry hook (CD) | **न**: the tick is now a short teardrop, about 0.26 H instead of 0.36 H, in line with Martel and Noto. **ि / ं**: the hook lands on न's danda and the anusvara sits above that danda (over न), as in Martel, Noto and Tiro. **द्र**: द is redrawn as one pen stroke that leaves the line as a danda-weight stub, turns left into a hairline top arm (the entry hook), runs down the heavy left side, round the bottom and up into a terminal at the lower right. The rakaar is a caret hung from that terminal: a leaf leg down-left and a hairline down-right. व is the new mark geometry. Compared side by side with Martel (loops2/deva.png). **Still to be verified by the team / a native type reader before public use.** |

## Construction (units: VANINDRA cap = 100, from the top of the line to the baseline)
- **Mark, master** (`r4mark.va_vloop`, parameters in `r4system.MK`):
  - line 9.5; danda 13 at x = 58;
  - the loop leaves the danda at y = 20 as a 5.5 hairline; outer shoulder at (2, 40); near-straight arm to the point (31, 95); counter shoulder at (17, 43);
  - return stroke 10.5, meeting the danda at y = 54; overhangs 3 / 3;
  - ink is 44% of the box. Four cubics and straight lines, 352 bytes.
- **mark_small**: line 13.5, danda 17, loop top 8.5, return 13, 55% ink.
- **mark_lockup**: line 6.2, danda 8.4, loop top 3.4, return 6.4, drawn to sit at 1.85× over VANINDRA.
- **Wordmark, master**: line 8.8, stems 13, hairlines 5.0, N stems 8.5. Leaf diagonals start at 3.8 and land on 13.5 feet. Width 5.96 × cap. Unchanged from Round 3, because the judges said it works.
- **Sturdy cut**: line 11, stems 16, hairlines and leaf tops 10.2, N stems 12, feet 18.5, wider spacing (N–I 25).
- **Phone cut**: the sturdy cut with stems of 3 px, N stems of 2 px and a 2 px line at a 17 px cap. Letter origins are snapped to the 100/17-unit grid.
- **CREATIONS** (in its own units, then set at 0.55):
  - master: stems 14.5, hairlines 6.2, N stems 9; leaf feet 15;
  - sturdy: stems 18, hairlines 10.5;
  - stands on VANINDRA's baseline; the gap between the words is 36; the step falls at mid-gap.
- **Global**: one hairline of 3.6 (sturdy 6.0) over both words. The caps start 0.45 × hairline below its top, so they overlap it.
- Everything is parametric:
  - `r4system.py` holds every number;
  - shapes are boolean-unioned in skia-pathops;
  - all text is outlined;
  - every SVG is under 14 KB.

## Size rules (which file at which size)

| Use | File | Size |
|---|---|---|
| Favicon, app icon, avatar ≤ 48 px, **India / Hindi audiences** | `mark_small.svg` | 16–48 px. Never above 64 px (it is deliberately heavier). |
| Instagram / WhatsApp profile picture, social cards, **India / Hindi audiences** | `mark_on_emerald.svg` (gold on emerald) or `mark_on_ivory.svg` | 56 px and up. Never below 48 px. Between 49 and 55 px, use mark_small. |
| **Global, USD and South-Indian accounts**: profile picture and favicon | `mark_global_on_emerald.svg` / `mark_global_on_ivory.svg` (≥ 56 px, made for circle crops); `mark_global_small.svg` (16–48 px) | The line always runs full-bleed. Never shorten it to the V's width (that makes a ∇) and never box it. **The व mark is never used alone in the USD workspace.** |
| Website / app header | `wordmark_header.svg` (sturdy cut, VANINDRA only) | VANINDRA cap 18–40 px. The line may run on as a 1 px page rule with the navigation hanging from it (header.png). |
| Phone header | `wordmark_phone_17px.svg` | **Native size only (111 × 19 px, cap 17 px)**, placed on whole pixels. For other caps of 12–19 px use wordmark_header.svg. |
| Full name in UI settings: email signature, invoice, deck footer | `lockup_horizontal_header.svg` (sturdy) | VANINDRA cap ≥ 24 px (CREATIONS cap ≥ 13 px). Below that, VANINDRA alone. |
| Print, decks, signage, video end cards | `wordmark.svg`, `lockup_horizontal_on_*.svg` (master) | VANINDRA cap ≥ 40 px or ≥ 12 mm. Below that, use the sturdy files. |
| Formal and vertical uses: cover page, letterhead top, merch | `lockup_stacked_on_*.svg` | Width ≥ 220 px / 45 mm. To stack the mark over the name in a new layout, use `mark_lockup.svg`, **never** mark.svg. |
| Hindi-market extras (optional) | `lockup_bilingual_on_*.svg`, `wordmark_devanagari.svg` | VANINDRA cap ≥ 30 px. Never mandatory. **Only after native sign-off.** |
| USD workspace, English-speaking markets | `global.svg` (gold hairline), `global_on_emerald.svg`, `global_one_colour.svg`, `global_wordmark.svg`; `global_header.svg` for headers | global.svg: VANINDRA cap ≥ 28 px. global_header.svg: 14–28 px cap. |
| Reel / video credit | `reel_tag_ivory.svg` / `reel_tag_emerald.svg` | Drawn for a 1080 × 1920 cover at native size (VANINDRA cap 42 px). Left edge at the 60 px safe margin, line top at y ≈ 300 (inside the 3:4 grid crop, which starts at y = 240). Ivory on dark footage, emerald on light. Never start the line at the frame edge. |
| Embroidery, foil, emboss | `wordmark_header.svg`; `mark.svg` / `mark_small.svg` | VANINDRA ≥ 62 mm wide (1 mm stitch). Mark ≥ 25 mm tall (master) or 12–25 mm (small). Never embroider the master wordmark (hairline 0.84%). Embroider the full name only at ≥ 180 mm. |

**Clear space:** the VANINDRA cap height on all sides of any lockup, and a quarter of the mark's height around the mark.

**Colour:** use one colour wherever possible (emerald on ivory; ivory or soft gold on emerald). Gold appears only in the avatar on emerald and in the global hairline. No gradients, foil effects, shadows or outlines.

## Using the line (the system)
Titles and labels hang from the line, and anything smaller stands on its baseline under it. The line has two weights only:
- the heavy line, which is only ever over VANINDRA;
- the hairline, for everything else.

The step between them always falls in a gap, never over a letter. The line can run on across a header or a deck title, but it never enters from a frame edge.

## Files
- **Marks:** mark.svg, mark_small.svg, mark_lockup.svg, mark_on_ivory.svg, mark_on_emerald.svg, mark_one_colour_gold.svg, mark_global_on_emerald.svg, mark_global_on_ivory.svg, mark_global_small.svg.
- **Wordmarks:** wordmark.svg, wordmark_header.svg, wordmark_phone_17px.svg, wordmark_devanagari.svg.
- **Lockups:** lockup_horizontal_on_ivory.svg, lockup_horizontal_on_emerald.svg, lockup_horizontal_header.svg, lockup_stacked_on_ivory.svg, lockup_stacked_on_emerald.svg, lockup_bilingual_on_ivory.svg, lockup_bilingual_on_emerald.svg.
- **Global:** global.svg, global.png, global_on_emerald.svg, global_one_colour.svg, global_wordmark.svg, global_header.svg.
- **Reel credit:** reel_tag_ivory.svg, reel_tag_emerald.svg.
- **Renders:**
  - sheet.png, sizes.png, sizes_global.png, context.png, context_global.png, header.png, reel_tag.png, global.png;
  - construction.png (updated);
  - explore_final.png: this pass's studies of the mark, lockups, CREATIONS, stacking, the global avatar, the Reel credit and the Devanagari;
  - explore.png and explore_marks.png (Round 3 history);
  - loops2/ (this pass's loops) and loops/ (Round 3 loops).
- **Generators:** `build2.py` (all SVGs and renders), `header2.py`, `reel_tag2.py`, `construction2.py`. Libraries: `r4system.py`, `r4mark.py`, `r4latin.py`, `r4deva.py`, plus the Round 3 libraries r3geo / r3latin / r3mark. The superseded Round 3 generators are in `_superseded/`; don't run them, because they rebuild the old design.

## Explored and rejected in this pass
- **Mark**: V-silhouette variants A to E and A2 to A5 (loops2/mark1.png, mark2.png). A tip at the baseline loses the danda run-on (the judges' "letter, not pennant"). A bowed arm brings the "a" back. A5 was chosen.
- **Full name**: same cap height in a light weight. It makes a 13:1 strip in which CREATIONS competes with the name. With the line ending at VANINDRA, the system breaks. A larger descriptor (0.62) is too loud. A two-tier version under a second rule reads as an underline (Round 3).
- **C/S**: a pen C with tapered terminals reads as beak-like flicks. A superellipse-arc S has kinks at its joins.
- **Global avatar**: a V under a short bar reads as a nabla. A wordmark disc is illegible at 32 px. VAN / INDRA on two lines splits the name.
- **Reel**: EDIT BY on the bar (compact, but it loses the step).

## Honest risks
1. **Native verification is still required.** वनिंद्रा was compared with Martel, Noto Serif and Tiro, but it was drawn by a non-native designer. The proportions of द्र, the length of the ि hook and the position of the anusvara must be signed off by the team or a native type reader **before any public use**. The bilingual files are optional until then.
2. **Bengali readers**: the new pointed bowl is even closer to Bengali ব (ba / va, the same historical letter). It is harmless but real.
3. **The V is still a drawn letter at favicon size.** The silhouette now ends in a point, but a Latin reader at 16 px sees "a V-shaped glyph with a bar and a stem", not the word VanIndra. That is why the USD and South-Indian accounts use the line + V avatar, and the rule above forbids the व mark alone in the USD workspace.
4. **The global avatar is an initial V.** It is ownable only through the full-bleed line. If someone shortens the line or puts it in a box, it becomes a generic nabla or monogram.
5. **There is a gap between the line and CREATIONS** in the full-name lockups. This is deliberate: CREATIONS stands on the baseline under the same line. Nobody should "fix" it by lifting CREATIONS to the line, because that brings back the superscript.
6. **Six cuts need discipline.** The mark has three cuts (master, small, lockup) and the name has three (master, sturdy, phone). The wrong cut at the wrong size brings back ghost hairlines or a mark that is too heavy. The size table is the rule.
7. **Faux-Devanagari drift** remains possible in the India master (a heavy bar over Latin capitals) if someone adds ornaments, foil or 3D. The global hairline version exists for that reason.
8. **The recommended web header omits CREATIONS.** The full name lives in the page title, the footer and `lockup_horizontal_header.svg`.
9. **Production:**
   - The geometry is generated parametrically.
   - The S and C of CREATIONS and the द are sampled pen outlines (smooth at display sizes, but node-heavy).
   - A final vector-editor pass is recommended: node cleanup, a hand-hinted 16 px ICO and a print proof of the 3.6-unit global hairline below 30 mm.
