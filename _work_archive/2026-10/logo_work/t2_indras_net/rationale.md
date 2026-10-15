# t2: Indra's Net, "One Thread, Many Jewels"

## Public story (one sentence)
Indra's Net is an old image of an endless net with a jewel at every knot, each jewel reflecting all the others. The VanIndra V is cut straight from that net: a strap of jewels and one thread, drawn the way one creator's work, tied to another's, makes both of them shine.

## The idea
- The mark is a high-contrast V with a thick stroke and a thin stroke, like a Didone V. No font was used anywhere in the symbol.
- The thick stroke is a strap of ten stones. Every stone is one cell of a rhombic net.
- The thin stroke is a single thread.
- The net's threads appear twice:
  - in negative, as the light-lines between the stones;
  - in positive, as the V's hairline.
  Every light-line that crosses the strap runs parallel to the thread. The two directions of the net are the two strokes of the letter.
- One stone, the one the thread meets, is gold. This is the knot where two strands meet, the "collab" stone.
- The same net, extended, becomes the brand surface (`pattern_on_*.svg`). The V is not placed on the net; it is a few cells of the net filled in.

## Construction (all geometry is computed: `mark.py`, `build.py`)
- **Grid.** Each point is P(u,v) = u·e1 + v·e2, with e1 = (s·h, h) and e2 = (−s·h, h).
  - s = 0.40 is the tangent of the V's half-angle (21.8°). It is also the ratio of each cell's horizontal half-diagonal to its vertical half-diagonal, so every stone has the same shape as the cell.
  - h = 60 units.
- **Stones.** The cells (i, j) with j ∈ {0,1} and i ∈ [−5, −1] are each inset by g = 4 on all four sides. That leaves light-lines exactly 2g wide, in both directions, everywhere.
- **Thread.**
  - Its width is 12, which is 1.5 light-lines. This keeps it visible at about 40 px.
  - Its outer edge lies on the line u = −g′. That is the same line as the lower facets of the two bottom stones. So the right-hand contour of the V is one straight line from the top of the thread to the vertex (shown in red in `construction.svg`).
  - It stops exactly one light-line (2g) short of the gold stone.
- **Terminals.**
  - The strap's top facets lie along e2, parallel to the thread.
  - The thread's top is cut along e1, parallel to the strap.
  - The thread's peak is solved to sit exactly on the cap line set by the top stone's peak. All terminals are lattice points, so no overshoot fudge is needed.
- **Optical placement.** The mark is centred on a 35/65 blend of its area centroid and its bounding-box centre. This stops the heavy strap from pulling the mark to the left.
- **Wordmark.**
  - VANINDRA is set in Tenor Sans caps, tracked +0.235 em, with hand-set pair corrections: VA −0.085, RA −0.05, AN −0.025, NI and IN +0.01, DR +0.01.
  - CREATIONS is justified to the same width.
  - All text is outlined.
- **Palette.**
  - On ivory: emerald #0B2A20 and antique gold #A8843A.
  - On emerald: ivory #F6F1E7 and soft gold #D2B26A.
  - One-colour versions in gold, emerald and ivory are included. In those, the gold stone simply joins the strap.

## Small-size behaviour
- **`mark_small.svg` (for 48 px and below).** Same lattice and same thread logic, with three changes:
  - The strap's stones merge into one solid stone-shaped strap, four rows long, so the shape is a little wider.
  - The thread is heavier, at 20 units.
  - The junction light-line is kept.
  - `sizes.png` shows it crisp at 16 px on both grounds. It uses the emerald file on ivory and `mark_small_ivory.svg` on emerald. Both rows come from `render.js sizes`, combined with `sizes_combine.js`.
- **The full mark** is used from about 48 px up, including the 110 to 150 px Instagram profile circle (see `context.png`). At those sizes the ten stones and the gold knot all read.
- **Horizontal lockup.** In a 52 px header, CREATIONS shrinks to about 5 px. Below roughly 60 px lockup height, use VANINDRA alone.

## Files
- **Symbol:** `mark.svg`, `mark_small.svg`, `mark_small_ivory.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_{gold,emerald,ivory}.svg`
- **Wordmark and lockups:** `wordmark.svg`, `lockup_horizontal_on_{ivory,emerald}.svg`, `lockup_stacked_on_{ivory,emerald}.svg`
- **System:** `pattern_on_{emerald,ivory}.svg` (a seamless tile), `construction.svg`
- **Renders:**
  - `explore.png`: twelve variations across five exploration rounds. The first raw round is in `explore_round1.png`.
  - `sheet.png`, `sizes.png`, `context.png`
  - Loop sheets are in `review/` and `refine*/`.

## Risks / honest weaknesses
- **Wrong first reads.** The V is asymmetric, with a hairline right stroke. At a glance some people may read it as a tick or check mark, or as a "√".
- **Unwanted associations.** A strap of rhombic stones can suggest argyle, snakeskin or a sports chevron. Restraint matters: one gold stone and generous space.
- **Small master.** It keeps the silhouette but loses the individual jewels. Family resemblance at 16 to 32 px relies on the stone-shaped strap and the separated thread.
- **Wordmark.** It is a carefully spaced typeface, not a custom-drawn one. The justified, tracked-out CREATIONS line is a common luxury convention and echoes Round 1's descriptor treatment.
- **Pattern.** It follows the monogram-canvas convention. On ivory the gold net can tip toward "trellis or fence" if it is printed too dark or too dense.
- **Devanagari.** Not used. Any Devanagari pairing (वनिंद्रा) would need to be drawn and then verified by the team.
