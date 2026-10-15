# Shirorekha, F1: Everything hangs from one line

This is the finalist polish of VanIndra Creations' Shirorekha concept for the team vote. It is built on `r1_shirorekha_final_final` (judges 7.3 / 7.5 / 7.5).

The polish keeps everything the judges said works:
- the one running line;
- the drawn VANINDRA alphabet, and its sturdy and 17 px phone cuts, unchanged;
- the व letter with its point and danda run-on;
- CREATIONS built from the same constructors;
- the 1440 header with the navigation hanging from the page rule;
- the film-credit style Reel tag;
- the gold-hairline global version.

Every must-fix item went through at least three rounds of render, look (zoomed to 16, 24, 32, 40, 48 and 110 px), critique and revise. The studies are in `explore_f1.png`, and the working renders are in `_r5/`.

**Team board:** `board.png`.

## Public story (one sentence)
In Devanagari every letter hangs from one line, the *shirorekha* ("head-line"), and at VanIndra everything we make hangs from its headline too: the first three seconds.

## The idea, as it shows up in the drawing
- **The line is the brand.** VANINDRA hangs from one heavy line. In the full name, CREATIONS hangs from its own hairline at its own cap height, the way separate words each carry their own shirorekha in Devanagari. Both words stand on one baseline. The line also:
  - runs on as the website's page rule, with the navigation hanging from it;
  - steps up from a hairline to the heavy line in the Reel credit.
- **The mark is व, and it reads as a V twice.** The loop hangs from the danda, never from the line, so it reads as व and not प. Both the white counter and the outer silhouette are Vs.
- **One stroke grammar for both scripts:**
  - verticals are dandas;
  - diagonals are leaves: a hairline where they leave the line, full weight at the foot;
  - bowls are k = 0.60 superellipses;
  - C, S and द are drawn with a contrast pen.

## Judges' must-fix items and what was done
J1 = first judge (7.3), J2 = the creator / India judge (7.5), J3 = the US B2B judge (7.5).

### Mark
- **Shoulder heavier than the danda; reads as a Latin "a" under a macron at 40–56 px (J1, J2).**
  - Done:
    - Each side of the loop is now **one smooth cubic**, so there is no knuckle. The loop leaves the danda as a 6.0 hairline, swells to at most **11.9** on the shoulder (was 15.3) and tapers into the point.
    - The **danda (13) is now the heaviest stroke**, followed by the return stroke at 10.5.
    - The counter is larger, so the V dominates.
    - The shoulder is open and round (J1's "graceful"), and the weight tapers toward the hairline (J2).
  - Tested five shoulder variants (`explore_f1.png` §1).
  - The lockup cut follows the same rule: its shoulder is no heavier than its 8.4 danda.
- **mark_small at 16 px not pixel-fitted (J3).**
  - Done: `mark_small.svg` is now **drawn on the 16 px grid**, with its viewBox in pixels. Every straight edge lands on a whole pixel at 16, 32, 48 and 64 px:
    - line: 2 rows;
    - danda: exactly 2 columns;
    - one empty row under the line;
    - loop top: one full row where it leaves the danda.
  - Pixel dump at 16 px: line and danda are 100% ink with no grey edge columns (they were 22–43%). The counter and point survive.
  - `favicon.ico` (16 / 32 / 48, transparent) is built from it.

### Full name and stacked lockup
- **Hairline floats ~0.42 cap above CREATIONS; CREATIONS doesn't hang from a line (J1, J3).**
  - Done: CREATIONS **hangs from its own hairline**. Its caps overlap the line by 45%, so they touch with no gap and no seam. CREATIONS still stands on VANINDRA's baseline, so the old superscript does not come back.
  - Applied in `lockup_horizontal_*`, the header lockup, `global*` and the stacked lockups.
  - Alternatives are shown in `explore_f1.png` §7: the old floating line, a stair step, and CREATIONS standing free.
  - Supporting details:
    - T's crossbar is 1.8× the top stroke so it still reads under its line.
    - CREATIONS stems are 13.5, so the word's ink density matches VANINDRA's (0.291 vs 0.286, measured on global.png).
- **Stacked lockup: CREATIONS floats with no line (J2).** Done: it hangs from its own hairline, centred under VANINDRA.
- **Header full-name lockup gap looks accidental at 28 px (J3).** Done: CREATIONS is hung from its own line. `lockup_horizontal_header.svg` is now **drawn in pixels at a 28 px cap**: the 3 px line, the 2 px CREATIONS hairline and the baseline all land on whole pixels.

### Global avatar
- **The V under a full-bleed bar reads as ▼ / ∇ / dropdown / coat hanger; it is the lone V Round 2 banned (J1, J2, J3).**
  - Done: the V is gone. Following J1's alternative, the global avatar is now **VANINDRA (sturdy cut) hanging from a gold line that runs edge to edge** (`mark_global_on_emerald.svg`, `mark_global_on_ivory.svg`). This is the brand's own idea in a circle, the way luxury houses use their wordmark as an avatar.
  - Before choosing it, I tried J2's "V with the व's DNA" three ways (`explore_f1.png` §2–5):
    - the loop on a danda stub reads as Bengali ব / a "d";
    - a V with a danda stub closes into a shield, like the Pocket app icon;
    - a V hanging by one arm reads as "7".
  - The leaf V without the bleed is still a ∇.
- **Approve the Latin avatar for South India too (J2).** Done: the size rules name it the avatar for USD, South-Indian and pan-India outreach.

### Reel credit
- **EDIT BY too heavy: 2.2 px stems against ~1 px name hairlines (J1).** Done: EDIT BY is redrawn with **1.4 px stems and 1.0 px hairlines** at a 10 px cap.
- **Step from the hairline to the heavy line ~1 px, invisible; V and A hairlines break up over hair (J2, J3).** Done:
  - The step is now a **1.25 px hairline to a 3.0 px heavy line (2.4×)**.
  - VANINDRA is the sturdy cut, so every hairline is ≥ 2.2 px at 540.
  - The credit sits on a calm wall: `reel_tag.png` uses an emerald credit on light footage. `reel_tag_dark.png` shows the ivory credit on dark footage.

### वनिंद्रा
- **Sampled polylines, 414 straight segments (J1).** Done: the contrast pen now fits true cubic Béziers (Schneider least-squares fit, 0.05-unit tolerance).
  - `wordmark_devanagari.svg`: 45 C / 11 L, 2.4 KB (was 15 C / 414 L, 6.7 KB).
  - The same fit applies to the C and S of CREATIONS, so every SVG is now ≤ 4.1 KB.
- **द्र: the rakaar is the largest and lowest shape and reads as an X / λ (J2, J3).** Done: the rakaar is now a **short caret hung from the end of द's tail**:
  - its apex is at the tail;
  - its legs end about 10 units below the baseline (was about 23);
  - it no longer crosses the bowl.
- **न: the teardrop looks like a stray blob (J2).** Done: the न's foot now **grows out of the end of the joining stroke**, through a narrow neck into a weighted foot with a right-turning tail, as in Martel, Noto and Tiro. It was compared with a crescent version (`explore_f1.png` §8).
- **The ि hook vanishes before the न danda at 160 px (J3).** Done: the hook keeps a 5.5-unit width all the way to where it lands, over the centre of the न danda (`_r5/bil160.png`).
- **Still to be verified by the team or a native type reader before any public use.**

### Headers and large sizes
- **The heavy line over all caps comes closest to the "Samarkan" look (J1, J3).**
  - Done: header.png now shows the **India header and the gold-hairline global header side by side** at real size (desktop and phone; new `global_phone_17px.svg`).
  - Decision:
    - the .in site keeps the heavy line, because that is the idea;
    - **outside India, and on any surface wider than about 300 mm, the gold-hairline `global*` files are the default** (J1's rule).
  - The A apexes stay flat-cut into the line, because that is what hanging from the line means.

## Construction (units: VANINDRA cap = 100, from the top of the line to the baseline)
- **Mark, master** (`r5system.MK5`, drawn by `r4mark.va_vloop`):
  - line 9.5; danda 13 at x = 58;
  - the loop leaves the danda at y = 20 as a 6.0 hairline;
  - outer shoulder (0.5, 43), inner shoulder (12, 46.5); maximum loop weight 11.9;
  - point (30, 96); return stroke 10.5, joining at y = 54;
  - four cubics; 386 bytes.
- **mark_small** (`r5small.py`): 16 px grid.
  - line rows 1–2, columns 2–13;
  - danda columns 11–12, rows 1–14;
  - loop top on row 4;
  - return stroke 1.7 px; point on row 14.
- **mark_lockup** (`MKL5`): line 6.2, danda 8.4, loop top 3.4, shoulder ≤ 8.4. Stack it at 1.85× over VANINDRA.
- **VANINDRA:**
  - master: line 8.8, stems 13, hairlines 5.0;
  - sturdy: line 11, stems 16, hairlines 10.2;
  - phone: pixel-fitted at a 17 px cap.

  All three are unchanged.
- **CREATIONS:**
  - set at 0.55 of the cap, on VANINDRA's baseline;
  - its own hairline: 5.0 master / 6.4 sturdy; caps overlap it by 45%;
  - stems 13.5 master / 17 sturdy; T crossbar 1.8× the top stroke.
- **Global:**
  - VANINDRA hangs from a 3.6 gold hairline (6.0 sturdy);
  - CREATIONS hangs from a gold hairline 0.85× as heavy.
- **Global avatar:** sturdy VANINDRA at 86% of the avatar width. The gold line is 2.4% of the side and runs edge to edge. The caps overlap the line by 45%.
- **वनिंद्रा:** see `r5deva.py` (rakaar `rak_l` / `rak_r`, न foot, hook width `hook_w`).
- Everything is parametric. Text is outlined. Shapes are unioned in skia-pathops. Pen outlines are fitted Béziers (`r5fit.py`, `r5pen.py`).

## Size rules (which file at which size)

| Use | File | Size / rule |
|---|---|---|
| Favicon, app icon, any **square** icon (all domains) | `mark_small.svg`, `favicon.ico` | 16–64 px. Pixel-exact at 16 / 32 / 48 / 64. Never above 64 px (it is deliberately heavier). |
| Profile picture (circle crop): **India / Hindi** | `mark_on_emerald.svg` (gold on emerald) or `mark_on_ivory.svg` | One file for every display size. Instagram shows it from 32 px (feed) to 110 px (profile). |
| Profile picture (circle crop): **Global / USD / South India / pan-India outreach** | `mark_global_on_emerald.svg` / `mark_global_on_ivory.svg` | Reads as letters from 40 px. At 32 px it reads as "a word on the line". Never use it as a favicon. Never shorten the line or box it. |
| Website header, **.in** | `wordmark_header.svg` (sturdy, heavy line) | VANINDRA cap 18–40 px. The line may run on as a 1 px page rule, with the navigation hanging from it (header.png). |
| Website header, **.com / outside India** | `global_header.svg` (gold hairline) | Cap 14–40 px. The hairline may run on as the page rule. |
| Phone header | `wordmark_phone_17px.svg` (.in) / `global_phone_17px.svg` (.com) | Native size only (cap 17 px), on whole pixels. For other caps of 12–19 px use the header files. |
| Full name in UI (email signature, invoice, deck footer) | `lockup_horizontal_header.svg` | Drawn in px at a 28 px cap (pixel-exact there). Use at 24–40 px cap. Below 24 px use VANINDRA alone. |
| Print, decks, video end cards, **India** | `wordmark.svg`, `lockup_horizontal_on_*.svg` (master) | Cap ≥ 40 px or ≥ 12 mm, and up to about 300 mm wide. |
| **Outside India, and any surface wider than ~300 mm** (signage, banners, stage) | `global.svg`, `global_on_emerald.svg`, `global_one_colour.svg`, `global_wordmark.svg` | Cap ≥ 28 px. Print-proof the hairline below 30 mm. |
| Formal and vertical uses: cover, letterhead top, merch | `lockup_stacked_on_*.svg` | Width ≥ 220 px / 45 mm. To stack the mark in a new layout, use `mark_lockup.svg`, never mark.svg. |
| Hindi-market extras (optional) | `lockup_bilingual_on_*.svg`, `wordmark_devanagari.svg` | VANINDRA cap ≥ 30 px. **Only after native sign-off.** Never mandatory. |
| Reel / video credit | `reel_tag_emerald.svg` (light footage) / `reel_tag_ivory.svg` (dark footage) | Drawn for 1080 × 1920 at native size (VANINDRA cap 44 px). Left edge on the 60 px safe margin, line top at y ≈ 350 (inside the 3:4 grid crop, which starts at 240). Place it on a calm area, never over hair or pattern. Never start the line at the frame edge. |
| Embroidery, foil, emboss | `wordmark_header.svg`; `mark.svg` / `mark_small.svg` | VANINDRA ≥ 62 mm wide (1 mm stitch). Mark ≥ 25 mm tall (master) or 12–25 mm (small). Never embroider the master wordmark. |

**Clear space:** VANINDRA's cap height on all sides of any lockup, and a quarter of the mark's height around the mark.

**Colour:**
- Use one colour wherever possible: emerald on ivory, or ivory or soft gold on emerald.
- Gold appears only in the India avatar and in the global hairlines.
- No gradients, foil effects, shadows or outlines.

## Using the line (the system)
- The line has two weights only:
  - the heavy line, used only over VANINDRA;
  - the hairline, for everything else.
- Each word hangs from its own line at its own cap height. Smaller words stand on the same baseline.
- The line can run on across a header or a deck title, but it never enters from a frame edge.
- It is never decorated, curved, doubled or turned into a swoosh.

## Honest risks
1. **Native verification is still required.** वनिंद्रा was compared with Martel, Noto Serif and Tiro, but it was drawn by a non-native designer. The proportions of द्र, the length of the ि hook and the position of the anusvara need sign-off before any public use.
2. **The global avatar is a word, not a symbol.** Below 40 px (Instagram feed, comments) it reads as "a word on a gold line", not as letters. That is accepted maison practice, but it is weaker at 32 px than the व.
3. **The व is used as the favicon on every domain, including .com.** A favicon always sits next to the page title, and all three judges called it the strongest small mark. Even so, the profile picture in the USD workspace stays the Latin avatar.
4. **The lighter master loop is thinner at 24–32 px.** For square icons at those sizes, use mark_small, which is heavier and pixel-exact. An Instagram avatar shows one file at every size, so in the feed the loop is light but the counter V and the danda stay clear.
5. **Bengali readers** may read the व as ব (the same historical letter). This is harmless.
6. **Two lines in the full name.** A designer might "fix" CREATIONS by lifting it to the top line, which turns it back into a superscript, or by joining the two lines with a step. Neither is allowed: each word has its own line.
7. **Several cuts need discipline.** The mark has three cuts (master, small, lockup). The name has three (master, sturdy, phone) plus a pixel-exact header lockup and two global cuts. The wrong cut at the wrong size brings back ghost hairlines or a mark that is too heavy. The size table is the rule.
8. **Faux-Devanagari drift.** The heavy line over Latin capitals can still drift toward the restaurant-menu look if anyone adds ornament, foil or 3D. The 300 mm and outside-India rule moves big and international uses to the gold hairline.
9. **Production:** the Béziers are machine-fitted to 0.05 units. A final node cleanup in a vector editor and a print proof of the global hairline below 30 mm are still recommended.

## Files
- **Marks:**
  - mark.svg, mark_small.svg, mark_lockup.svg;
  - mark_on_ivory.svg, mark_on_emerald.svg, mark_one_colour_gold.svg;
  - mark_global_on_emerald.svg, mark_global_on_ivory.svg;
  - favicon.ico.
- **Wordmarks:** wordmark.svg, wordmark_header.svg, wordmark_phone_17px.svg, wordmark_devanagari.svg.
- **Lockups:**
  - lockup_horizontal_on_ivory.svg, lockup_horizontal_on_emerald.svg, lockup_horizontal_header.svg;
  - lockup_stacked_on_ivory.svg, lockup_stacked_on_emerald.svg;
  - lockup_bilingual_on_ivory.svg, lockup_bilingual_on_emerald.svg.
- **Global:** global.svg, global.png, global_on_emerald.svg, global_one_colour.svg, global_wordmark.svg, global_header.svg, global_phone_17px.svg.
- **Reel credit:** reel_tag_emerald.svg, reel_tag_ivory.svg.
- **Renders:**
  - board.png (team board);
  - sheet.png, sizes.png, sizes_global.png;
  - context.png, context_global.png;
  - header.png;
  - reel_tag.png, reel_tag_dark.png;
  - global.png, construction.png;
  - explore_f1.png (this pass's studies);
  - explore.png, explore_final.png (earlier rounds).
- **Generators:**
  - `make_all.sh` runs build3.py, header3.py, reel_tag3.py, extras3.py, construction3.py and board.py.
  - Libraries: r5system.py (every changed parameter), r5small.py, r5deva.py, r5fit.py, r5pen.py, plus r4system / r4mark / r4latin / r3geo / r3latin.
  - Superseded generators are in `_superseded/`. Don't run them, because they rebuild the old design.
