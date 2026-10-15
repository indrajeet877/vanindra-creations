# R3 · The Hinge: VanIndra wordmark

## One-sentence public story
In VanIndra, one stroke belongs to both words: the n of Van is also the I of Indra, so the forest stands in front and the sky rises behind it.

## What you see (no diagram needed)
- A custom, drawn serif wordmark, **VanIndra**. The name itself is the asset; there is no separate symbol in any lockup.
- At the point where Van meets Indra, the n is drawn complete, and its right leg continues upward as the stem of a capital I. The I rises **above every other letter** (I = 784 units; V cap 700, d ascender 724). Indra, the sky, stands over Van, the forest.
- A fine cut that follows the n's shoulder puts the I *behind* the n. Exploration proved this is what makes the word read **VanIndra**: without it, every hinge read "VarIndra" or "Varhdra" (see explore.png).
- On dark grounds the rising I is the only gold element: ivory n, soft-gold I. On light grounds everything is emerald.
- Avatar / favicon: the hinge glyph alone (n + rising I). It is not another V, it is not a VI monogram, and it does not repeat in any lockup.

## Construction notes
- Every letter (V a n d r, the hinge, and C r e a t i o n s) is drawn from cubic béziers and straight segments in `vitype.py`. No font outlines are used. Stock fonts were used only in the first exploration panel (E1–E9) to test structure.
- One system, one contrast. Lowercase stems 82, capital stems 90, hairline 24, arch/bowl tops 29/28, overshoot 11 (1000-unit grid). Bracketed slab feet, sharp wedge heads on lowercase, symmetric bracketed slabs on capitals. The capital-slab head is what makes the hinge I read as a capital and not an l.
- Warmth comes from a teardrop terminal on the a, a beak-cut r, and a slightly oblique stress in the rounds. Restraint comes from flat colour and no ornament, headline bar or flourish.
- Optical spacing was measured, not guessed. Straight-to-straight white space is held at 88–92 units across the word, including the pair right after the hinge.
- **Creations** is drawn in the same system (C with vertical-cut terminals; s with a controlled width profile). It is never tracked, never gold and never Jost. It appears only in the full-name lockups, at the same weight as the name.
- Two optical cuts:
  - **Display** (`wordmark.svg`, lockups): cut = 16 units.
  - **Small** (`wordmark_small.svg`, headers): heavier hairlines (34), wider counters, cut = 46 units, I at 812.
  - `mark_small.svg` is a third, heavier cut (stems 104, cut 52) for favicons only.

## Lockups (no stutter anywhere)
| File | Content | Use |
|---|---|---|
| `wordmark.svg` | VanIndra | primary signature, hero, decks, print |
| `wordmark_small.svg` | VanIndra (small cut) | **website header** (36 px desktop, 26 px phone), email signature, footer |
| `lockup_horizontal_on_ivory/emerald.svg` | VanIndra Creations, one line | full legal / formal name where width allows (not headers) |
| `lockup_stacked_on_ivory/emerald.svg` | VanIndra / Creations as a two-line block (Creations scaled, never letter-spaced) | covers, title slides, packaging, merch |
| `mark*.svg` | hinge glyph | profile picture, favicon, app icon, Reel tag on very small placements |
| `global.svg` | identical to the horizontal lockup, emerald on white | USD / international workspace: the design is already global (Latin only, no Devanagari, no headline bar) |

## Size rules (which file at which size)
| Size of the artwork | Use |
|---|---|
| Wordmark ≥ 64 px tall (≥ 15 mm print) | `wordmark.svg` / lockups (display cut) |
| Wordmark 20–64 px tall | `wordmark_small.svg` (small cut); header 36 px desktop, 26 px phone |
| Wordmark 14–20 px tall | two-colour small cut on emerald only (ivory + soft-gold I) |
| Wordmark < 14 px tall, or mono < 20 px | don't use the wordmark; use the mark or plain text "VanIndra Creations" |
| One-line lockup | ≥ 240 px wide on screen / ≥ 50 mm print, otherwise wordmark only |
| Mark 64 px and up (IG profile 110–320 px, decks) | `mark_on_emerald.svg` (hero), `mark_on_ivory.svg`, `mark.svg` |
| Mark 48 px and below (favicon 16/32/48, small app icons) | `mark_small.svg` (on light) / `mark_small_ivory.svg` (on emerald). Never above 64 px; it is deliberately heavy |
| Reel "Edit by" tag | small-cut wordmark ≈ 24 px tall on a 540 × 960 cover, top-left, inside the playback-safe area; emerald (+ gold I) on light footage, ivory + soft-gold I on dark footage |
| Embroidery / foil | small cut only, wordmark ≥ 30 mm wide, mark ≥ 12 mm |

Colour: emerald `#0B2A20`, ivory `#F6F1E7`, antique gold `#A8843A` (light grounds, one-colour only), soft gold `#D2B26A` (the I on emerald). Gold is never used for anything except the rising I or a full one-colour gold version. Clear space = one x-height on every side.

## How it answers Round 2's failures
- **Decorated V:** the V is just a letter; the idea lives in the name's hinge.
- **Stutter:** no lockup pairs a mark with the wordmark.
- **Tracked Jost CREATIONS:** gone; Creations is drawn in the same system or omitted.
- **Idea only in a diagram:** the rising I is visible at every size where the wordmark is allowed.
- **Small sizes:** dedicated small cut and favicon cut, and the gold I survives down to 14–16 px.
- **Faux-Devanagari:** no headline bar, no Indic-styled Latin.
- **VI / Vi:** there is no monogram.

## Honest risks
1. **The avatar glyph needs context.** Alone, "n + rising I" can read as "nl", "rl" or a mirrored h. It becomes VanIndra's hinge once people have seen the wordmark. The gold-I version on emerald is far clearer than mono; use it as the profile picture.
2. **The mono hinge depends on a hairline cut.** Below about 18 px tall (mono), the cut closes and the word can drift toward "Varlndra/VarIndra". The size rules are not optional, and printers, embroiderers and developers must use the right cut.
3. **The I rising above the capitals could be "corrected" as an error** by a printer or developer. Supply SVG only, never retype the name in a font.
4. **Genre:** a contemporary editorial serif with a ball terminal is in fashion with DTC and beauty brands. The hinge is the ownable part; the surrounding letterforms alone are not unique.
5. **Drawn in code, not by a type foundry.** Curves are clean at every size I tested (up to 4000 px). A professional type designer should still do a final polish of s, e and t before billboard-scale use. Only these 13 letters exist; all other text needs a companion typeface (suggest a quiet sans for UI).
6. **No Devanagari in this direction.** If a bilingual lockup is wanted, वनिंद्रा must be drawn in the same contrast system and **verified by the team** (the द्र conjunct especially). It is not attempted here, to avoid a faux-Devanagari look.
7. **Not yet tested with real readers.** Before approval, show the 24 px header and the 110 px avatar to 10 Indian and 10 overseas people and ask "what does this say?".
8. The one-line "VanIndra Creations" is long (about 8:1). It is for formal uses only, never the header.

## Files
- Deliverables: `mark.svg`, `mark_small.svg` (+ `mark_small_ivory.svg`), `wordmark.svg` (+ `wordmark_small.svg`), `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg`, `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`, `global.svg` / `global.png`.
- Renders: `sheet.png`, `sizes.png` (row 1 `mark_small.svg` on ivory, row 2 `mark_small_ivory.svg` on emerald; two render.js runs stitched), `context.png` (render.js context; emerald bar uses the ivory-ink header file and the ivory bar uses the emerald-ink one, stitched), `reel_tag.png`, `header.png`, `explore.png`, `construction.png`.
- Source: `vitype.py` (type system), `build.py`, `extras.py`, `explore_sheet.py`, `construction.py`, `render_all.sh`.
