# Shirorekha: The Headline

**Territory:** t5 Shirorekha · VanIndra Creations, an India-to-world identity

## Public story (one sentence)
In Devanagari every letter hangs from one line, the *shirorekha* (literally "head-line"). The VanIndra wordmark hangs its English letters from that same line, because at VanIndra every piece of content hangs from the headline: the first three seconds.

## The idea
- **Wordmark.** "VANINDRA" is set in custom-drawn capitals that hang from a continuous shirorekha. It reads as English straight away, but its rhythm (tops fused into one line, weight gathering at the feet) is Devanagari.
- **Stroke logic.** Every diagonal leaves the headline as a hairline and gains weight as it falls, so the A's right arm, the N's diagonal and the R's leg are all straight wedges that start thin under the line and finish at full weight on the baseline. Verticals are full-weight *dandas*. The V's thick stroke is the one exception. It is drawn as a single **leaf**, thin at the line, swelling and ending in a point. It is the signature stroke and a quiet nod to *Van* (forest).
- **Monogram (व / V).** The same leaf, a hairline return stroke, a danda and a headline together form the Devanagari letter **व** (va). Read in Latin, the leaf and the hairline make a **V**, and the danda adds an **I** (VanIndra's V·I). It is one glyph in two scripts under one headline. It sits in no container: the headline belongs to the letter.
- **Optional bilingual line.** VANINDRA and **वनिंद्रा** hang from one shirorekha of identical weight (lockup_bilingual_*). The Devanagari is set in Tiro Devanagari Hindi, and its own headline band is replaced by the identity's 8.8-unit line so that both scripts share exactly one line. **The Devanagari spelling and rendering are to be verified by the team.**

## Construction (every value is in units of a 100-unit letter body; see construction.png)
**Wordmark.** Cap body H = 100, measured from the top of the headline to the baseline. Headline 8.8 (0.63 × stem). Stems 14. Hairlines 4.0. Wedges start at 3.6 and end with a 16.5 foot (1.18 × stem). N verticals 5.9. Bowls of D and R are superellipses (k = 0.60), with a thick side of 1.10 and 1.02 × stem. A crossbar at 0.66 H. The V point overshoots the baseline by 1.6. The headline overhangs 10 at the left and 5 at the right. Spacing was set by eye and fixed per pair: VA −9, AN 9, NI 17, IN 17, ND 16, DR 13.5, RA 6.

**Mark.** Headline 9.6, danda 14.5 at x = 62–76.5, hairline 5.0. The leaf is two quadratic Béziers: the outer edge runs from (0,0) to the tip at (37, 90) and bows outward by 12; the inner edge bows inward by 15 and starts 4.5 wide under the headline. The hairline rises from the tip at the V's mirrored angle and joins the danda at y = 50. The headline overhangs 11 at the left and 7 at the right. The tip sits at 90, above the danda foot at 100, as in a real व bowl.

All curves are exact quadratic or elliptical segments, with no hand-placed béziers. All shapes are boolean unions made in skia-pathops, and all text is outlined. In the squares, the mark is centred optically: the horizontal position blends the bbox centre with the area centroid at 0.6, because the danda carries the weight.

**Descriptor.** CREATIONS is set in Jost 500, tracked +0.44 em, in antique gold on light grounds and soft gold on emerald.

## Lockups
- **Horizontal.** Mark and wordmark hang from **one top line**. CREATIONS stands on the danda's baseline, so the top and bottom of the lockup are both shared lines. The wordmark cap body is 0.58 × the mark height.
- **Stacked.** The mark is 2.0 × the wordmark cap height and optically centred, with CREATIONS centred below.
- **Colour.** On ivory: the mark and wordmark are emerald and CREATIONS is antique gold. On emerald: the mark is soft gold, the wordmark is ivory and CREATIONS is soft gold. Every element also works in a single colour (emerald, ivory or gold).

## Small-size behaviour
- **mark_small.svg** is a separate cut for 48 px and below. The headline is 13, the danda 18, the hairline 8.5, the leaf fuller, and the overhangs shorter, so the counter stays open. It fills about 94% of its square. At 16 px it still shows headline, V and danda as separate strokes (see sizes.png, pixel-checked). At 24 and 32 px it is crisp.
- **The full mark** is for 56 px and up. It is used for the 110 px Instagram circle (context.png) at about 54% of the square, where it reads clearly.
- **The wordmark** needs a cap height of about 14 px or more. Below that the A and V hairlines thin out, so use the mark alone.

## Explored and rejected (explore.png, explore_marks.png, loop sheets)
- **Blocky "VI" stencils (M, N series).** Heavy and generic.
- **Straight-wedge mark (F series).** Clunky as a standalone symbol and pennant-like.
- **Two-stroke sweep into the danda (G series).** Rejected because it reads as **प (pa)**, not व.
- **Bindu over the mark (वं).** Dropped: वं stands alone as a bija-mantra syllable (religious connotation, the same territory as Om), and a dot above a V also echoed Round 1's diamond.
- **Lowercase "vanindra" with the i-dot as a bindu.** Charming, but it drifts toward faux-Hindi display type and loses the VanIndra casing.
- **Kalam chisel feet.** These read as faux-3D shadows.

## Risks / watch-outs
- Latin readers will see "VI". That is VanIndra's initials, but some may read it as the Roman numeral VI. The horizontal lockup therefore says "VI VANINDRA".
- The व reading is stylised: a pointed bowl rather than a round one. Native readers should confirm that it reads as व at a glance.
- A headline over Latin capitals has cheap precedents in "faux-Devanagari" fonts. This identity stays restrained: no ornaments, no curls, and only one line. Keep it that way in use (no flourishes, no gradients, no gold foil "3D" effects).
- The lockup_bilingual Devanagari is typeset (Tiro Devanagari Hindi, OFL) and is **to be verified by the team**.
