# R3 · The Hinge (final): VanIndra, one stroke for two words

## One-sentence public story
VanIndra is one name made of two words, and the logo shows the join: the n that ends **Van** runs straight down into the **I** that begins **Indra**, so one stroke belongs to both.

Second line, for Hindi audiences (Devanagari to be verified by the team): Hindi writes the same join as one sign, **नि**. The i-sign is a stem with an arch over the n, so the gold **I** in English is the gold **ि** in **वनिंद्रा**.

## What changed after the judges' round
Three things were kept: the drawn serif, "Creations" drawn in the same system, and the restraint with gold. The hinge also stays, but it was rebuilt so that it can be read at the sizes the brand is actually used.

1. **The hinge is now a staircase.** *Van* is on line 1 and *Indra* on line 2. The n's right leg drops straight into the I, and the slab where they meet is the n's foot and the I's head at once (one slab, two serifs). The old version hid most of the I behind the n's shoulder. Here nothing is hidden: both letters are whole, so there is no cut to close up and no tick that reads as an apostrophe. Line spacing = ascender 724 − slab 21 = 703, so the I is exactly the height of the ascender (no longer the 784 that looked pasted in).
2. **The one-line hinge is retired** (explore.png, studies 1–2: it read "Van'ndra" at every size once the I was lowered). The one-line wordmark now sets n and I side by side. The I is at ascender height and in gold, which marks the join. This version is for places that can only take one line.
3. **Avatar:** the staircase in a circle names the brand at 150, 110 and 56 px. The favicon is the V of the wordmark, a heavier cut used only at 48 px and below, where two words cannot survive.
4. **Terminals:** every free stroke end is now the same straight knife cut, rising about 20° (a, r, s, C, e, t, y). There are no ball terminals, no beak r, no flag on the t and no slab-ended s. The I's slab extension was cut from 37 to 31 units so it matches the feet.
5. **India:** **वनिंद्रा** is drawn in the same pen and shown in a bilingual lockup. Dandas and falling strokes are heavy; rising strokes and the shirorekha are light; ends are knife cuts. **Not Tiro pasted in, and to be verified by the team** (especially द्र, the drop, the height of the ि hook and the position of the bindu).
6. **Reel credit:** the words "edit by" are drawn in the system (new glyphs b and y). The credit is ivory with a soft-gold I on dark footage and all emerald on light footage, because gold disappears against a light wall.
7. **Stacked lockup:** Creations is at 58 % of the name's cap height and right-aligned under Indra. The *ns* pair was opened (kern −4 → +14).

## Construction notes (construction.png)
- Every Latin and Devanagari glyph is drawn from cubic béziers, straight segments and pen-expanded spines in `vitype.py` / `deva.py`. No font outlines appear in any deliverable. UI labels in the header mock use Manrope; they are not part of the identity.
- 1000-unit grid: x-height 490, cap 700, ascender 724. Lowercase stem 82, capital stem 90, hairline 24, arch tops 29, overshoot 11. Feet are bracketed slabs, lowercase heads are sharp wedges, and capitals take symmetric slabs.
- **Optical cuts:** *display* (`staircase.svg`, lockups) has hairline 24 / stem 82. *Small* (`mark*.svg`, `header_staircase_*.svg`, Reel credit, `wordmark_small.svg`) has hairline 34 / stem 90. The *favicon V* has a hairline of about half the stem.
- Colour rule: gold is only ever the I (in Devanagari, the ि). Emerald + antique gold `#A8843A` on ivory or white; ivory + soft gold `#D2B26A` on emerald. On photographs, use one colour (emerald on light footage, ivory on dark; the soft-gold I may stay on dark, calm footage). One-colour versions: all emerald, all ivory, all antique gold.

## Files
| File | What | Use |
|---|---|---|
| `mark.svg` | staircase, small cut, emerald + gold I, transparent | avatar artwork, decks |
| `mark_on_emerald.svg` / `mark_on_ivory.svg` | staircase in a square, fitted inside a circle crop | **Instagram / WhatsApp profile picture** (emerald is the hero) |
| `mark_one_colour_gold.svg`, `mark_one_colour_emerald.svg` | one-colour staircase | foil, stamps, single-colour print |
| `mark_small.svg` / `mark_small_ivory.svg` / `mark_small_tile.svg` | the wordmark's V, favicon cut | favicon, app icon, anything at 48 px and below |
| `staircase.svg` | staircase, display cut | hero, print, merchandise |
| `header_staircase_emerald.svg` / `_ivory.svg` (+ `_mono_`) | staircase, small cut, tight crop | **website header**, footers, email signature |
| `lockup_horizontal_on_ivory/emerald.svg` | Van / Indra Creations (Creations on line 2) | full name in wide spaces, letterhead, decks |
| `lockup_stacked_on_ivory/emerald.svg` | Van / Indra / Creations, right-aligned | covers, title slides, packaging |
| `lockup_bilingual_on_ivory/emerald.svg` | VanIndra over वनिंद्रा | Hindi-first India material (**after the team verifies the Devanagari**) |
| `wordmark.svg` / `wordmark_mono.svg` | one line, n and I apart, gold I | one-line places 64 px and taller |
| `wordmark_small.svg` | the same in the small cut | one-line places 14–63 px tall |
| `wordmark_devanagari.svg` | वनिंद्रा alone | to be verified by the team |
| `reel_tag_ivory.svg` / `reel_tag_emerald.svg` | "edit by" + staircase | Reel cover credit |
| `global.svg` / `global.png` | horizontal lockup on white, Latin only | USD / international workspace |

## Size rules (which file at which size)
| Artwork size | Use |
|---|---|
| Staircase **40 px tall or more** on screen (cap 19 px and up) | `header_staircase_*.svg` (small cut). Desktop header 64 px tall, phone header 44 px tall in a 64 px bar |
| Staircase **64 px tall or more**, or 40 mm wide or more in print | `staircase.svg` / lockups (display cut) |
| Horizontal lockup | 200 px wide or more on screen / 60 mm in print; below that, staircase alone |
| Stacked lockup | 160 px wide or more on screen / 45 mm in print; below that, staircase alone |
| One line only, 14–63 px tall | `wordmark_small.svg`; 64 px and up `wordmark.svg`; under 14 px, set "VanIndra Creations" as plain text |
| Profile picture | `mark_on_emerald.svg`. It reads at 320, 150, 110 and 56 px. At Instagram's 32 px comment avatar it becomes a texture (accepted; see risks) |
| 48 px and below (favicon 16/32/48, small app icons, map pins) | `mark_small*.svg` (the V). Never use it above 64 px as the main logo |
| Reel credit | `reel_tag_*.svg` at 64 px tall on a 540 × 960 cover (128 px on 1080 × 1920), 30 px from the left and 150 px from the top. That keeps it inside the 3:4 profile-grid crop (y 120–840) and clear of the caption overlay |
| **Embroidery** (1 mm test: render at 10 px/mm, open with a 1 mm disk) | Staircase small cut **≥ 90 mm wide** (≈ 41 mm tall): only serif tips round off. At 60 mm, the V's hairline arm and the arch tops vanish. Caps, sleeves and anything narrower: the V **≥ 12 mm tall**. Never embroider the Creations lockups below 250 mm wide (Creations hairline ≈ 20 units). Ask the digitiser to keep the hairlines at 1 mm or more |
| Foil / emboss | staircase ≥ 30 mm wide (hairline ≥ 0.3 mm) |
| Offset / digital print | staircase ≥ 25 mm wide |

Clear space = one x-height of the artwork on every side. Never retype the name in a font, never put the staircase on one line, and never move the gold off the I.

## Honest risks
1. **A two-line signature is unusual.** Some places only take one line. There, the one-line wordmark carries no ligature, only the gold I, so the idea is weaker. The staircase is also wider than a stacked block (about 2.2 : 1).
2. **The avatar at Instagram's 32–40 px sizes** (comments, story rings) is a texture, not text. It is recognised by colour and shape there. The V can't be swapped in automatically, because Instagram uses one image at every size.
3. **The favicon is a plain V**, the most default move in the book. It is accepted only at 48 px and below, where nothing with two words survives.
4. **Devanagari** was drawn in code by a non-native designer, with the Tiro anatomy as reference. **Verify before any use**: the conjunct द्र (drop, tail and rakaar), the ि hook height, the bindu, and that the dandas' knife-cut feet don't read as damage. The spelling is **वनिंद्रा** in every file.
5. **The step can be "corrected"** by a developer or printer into one line, or retyped in a font. Supply SVGs only.
6. **Genre.** It is still a high-contrast editorial serif. The knife cuts, the staircase and the Devanagari move it away from the ball-terminal DTC-beauty look, but the ownable parts are the staircase and the gold I, not the letters on their own.
7. **Drawn in code, not by a foundry.** The curves are clean at the sizes tested (up to 1600 px wide). A type designer should polish s, the a terminal and the Devanagari before billboard use. Only these glyphs exist: V a n d r I C e t i o s b y and वनिंद्रा.
8. **Embroidery minimums are large** (90 mm), so small merchandise uses the V.
9. **Not tested with real readers yet.** Before approval, run a 5-second test: show the 44 px phone header and the 110 px avatar to 10 Indian and 10 overseas people and ask "what does this say?".

## Judges' must-fix items → what happened
- Header and Reel misreads ("Van'ndra", "Varlndra"): **fixed.** The header and the Reel credit use the staircase, where both letters stay whole (header.png, reel_tag.png, explore.png study 1). The one-line hinge is retired.
- Avatar reads as a mirrored h, "nl" or "rl": **fixed.** The staircase avatar names the brand; the V is used only at 48 px and below.
- Hairline cut closes at 16–32 px / one colour: **fixed by removal.** No part of the system depends on a cut any more.
- The I at 784 looks pasted, and its slab is wider than the other serifs: **fixed.** The I is exactly ascender-tall (724) and its slab extension matches the feet (31).
- Ball a, beak r, t flag, slab-ended s, mixed terminals: **fixed.** One knife cut everywhere.
- Stacked lockup has two equal words; tight *ns*: **fixed.** Creations at 58 %, *ns* opened.
- No Indian root, no Devanagari, wrong spelling: **fixed** with a drawn वनिंद्रा, the bilingual lockup and the नि story (to be verified by the team). Spelling is वनिंद्रा everywhere.
- "Edit by" in a stock grotesk; gold disappears on light footage: **fixed.** The credit is drawn in the system, all emerald on light footage, with gold only on dark footage.
- Embroidery rule wrong by more than 2×: **fixed.** The rule was recalculated from a 1 mm test.
- Genre: **partly fixed** (see risk 6).
