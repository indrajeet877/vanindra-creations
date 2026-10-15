# VanIndra Creations — "The Threaded VI" (Territory: Maison Monogram)

## Public story (one sentence)
The two capitals of the name, the V of *Van* (forest) and the I of *Indra* (sky), are threaded through one another, so neither can be pulled away from the other.

## The idea
VanIndra is written with two capitals, and the monogram is exactly those two letters. A small-capital **I** is threaded through the **V**'s hairline arm. Its head sits inside the V's counter and its foot stands outside. Where they cross, the hairline passes *over* the I's stem: the stem is cut by two hairline gaps and the hairline runs unbroken across it. That single over/under makes the two letters topologically linked, like two links of a chain. The idea is weaving rather than a container, a frame or a decoration.

## Construction (all computed in `build.py`, cap height H = 1000)
- **V (Didone):** outer half-widths 520/520 at the cap line, giving symmetric outer arms at 27.1°. The thick arm is 186 wide horizontally (about 166 perpendicular), the hairline 31. The vertex overshoots the baseline by 16 (1.6 %). Unbracketed-style hairline serifs are 23 thick, slightly thinner than the diagonal hairline because horizontals read heavier. Small concave brackets (quadratic fillets, 24 × 40) sit where serifs meet strokes.
- **I (small capital):** stem 150, which is lighter than the V's thick arm because the I is the secondary letter. Serifs overhang 56 and are 23 thick, with 22 × 36 brackets.
- **Placement is solved, not eyeballed.** The I lives in a slanted channel between the V's point and the hairline. Its centre `d` is set so the foot-serif corner clears the V's outer edge by **58 units, measured perpendicular**. Its height is then solved so the head-serif corner clears the hairline's inner edge by **44 perpendicular**. Result: I centre x = 216, I height = 842 (0.84 H). The hairline crosses the stem between y = 260 and 613, roughly the middle of the I.
- **Interlace:** the I is cut by the hairline dilated by 18 units (perpendicular, mitred). Thin passes over thick, so the hairline is never interrupted. The earlier explorations proved that thick-over-thin at this angle hides about 38 % of the hairline.
- **Rules derived during exploration and obeyed:**
  - The I is never centred, because a centred I makes a trident or psi shape (which reads as a trishul or the Ukrainian trident).
  - No horizontal crosses the I's stem, because that makes a cross.
  - The I's head is kept below the cap line, so it never reads as a third prong.
- **Wordmark:** "VanIndra" in Bodoni Moda at **opsz 11** (not 96). At opsz 11 the hairline is 0.027 cap, matching the monogram's contrast and staying intact at header sizes. Weight 500, tracking −0.012 em, plus hand-set optical kerning per pair: Va −0.050, an −0.006, nI +0.010, In +0.006, nd −0.008, dr −0.002, ra −0.028. The camel-case capital I is kept deliberately: it is the monogram's I. "CREATIONS" is set in Jost 400 at 0.275 of the word size, tracked +0.30 em, in antique gold (soft gold on emerald).
- **Lockups:** in the horizontal lockup, the mark is 1.16 × the text-block height and optically centred on it, with a gap of 0.40 × the mark's width. In the stacked lockup, the mark is 0.44 × the wordmark's width, with a gap of 0.30 × the mark's height. Clear space around any lockup is at least the I's head-serif width × 2.
- **Palette:**
  - Emerald #0B2A20 with ivory #F6F1E7.
  - On ivory: emerald, with antique gold #A8843A for CREATIONS.
  - On emerald: soft gold #D2B26A and ivory.
  - Every file also works in one colour, as `mark_one_colour_gold.svg` and `lockup_horizontal_one_colour_gold.svg` show.
- **Monogram canvas (`pattern_canvas.svg`):** an upright half-drop lattice in soft gold on emerald, for packaging, slide backgrounds and Reel end-cards.

## Small-size behaviour
- `mark_small.svg` is a separate cut, built with the same equations. The changes:
  - The V is wider (575/575).
  - The hairline is 74 (2.4× the master's).
  - The gap is 52.
  - The I's serifs are slab-short (30), and brackets are removed.
- The channel solver keeps the I at 0.88 H, so the I never rises above the V.
- It is drawn in antique gold so it reads on both ivory and emerald.
- At 16 px it reads as a V with a stem. From 24 px the threaded hairline is visible.
- The master mark (`mark_on_emerald.svg`) holds as a 110–150 px Instagram profile picture in a circle crop.
- For favicons, use `mark_small`, never the master: the master's 31-unit hairline is under 0.5 px at 16 px.

## Risks / honest notes
- "VI" can be read as the Roman numeral six when it's seen without the wordmark. The overlap and stagger reduce this, but they don't remove it.
- The letterforms are Didone in spirit, so a viewer may call the V and I "Bodoni-like". What's ownable is the threading geometry and the solved placement, not exotic letter shapes.
- The two long acute wedges either side of the crossing are fine at screen sizes. For foil or emboss below 12 mm, use `mark_small`.
- The wordmark uses Bodoni Moda (OFL) glyphs with custom spacing. Its glyphs are not redrawn, apart from the spacing.
- Any Devanagari use of the name (वनिंद्रा) must be verified by the team. None is used here.
