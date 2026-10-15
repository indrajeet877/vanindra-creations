# The Emerald Cut — VanIndra Creations

## Public story (one sentence)
A V cut from a 9:16 emerald (the shape of every Reel we make): two stones, one broad and one hairline, set together at a single culet. We cut content the way a lapidary cuts an emerald, with precision, clarity and nothing wasted.

## What the mark is
- **Two stones, one V.** The broad stroke and the hairline stroke are two separate step-cut stones mitred on one hairline seam that runs from the crotch to the culet. The thick/thin contrast is Didone stress (thick stroke on the left, like a classical V), so it reads first as a refined letter and second as a jewel.
- **The emerald is in the geometry, not around the letter.** The V is a window cut from a true emerald-cut girdle on a 9:16 Reel grid (see `construction.svg`):
  - The V's two outer top corners are the girdle's own 45° corner cuts (C = 10% of the width, the same on both stones).
  - The outer edges run as pavilion lines from the girdle's top corners to the culet on the girdle's bottom edge.
  - The hairline mitre is the only internal facet line.
  - There is no container. The octagon exists only as the cutting grid.

## Construction notes
- Grid: W = 90 × H = 160 units (exactly 9:16). The outer edges run from (0,0) and (90,0) to the culet at (45,160).
- Strokes: perpendicular widths are 30 (broad) and 12 (hairline), a ratio of about 2.5:1.
- Corner cuts: 45°, 9 units on both stones. These lie on the girdle chamfer lines x + y = 9 and x − y = 81.
- Mitre: crotch → culet, 1.7 units wide. The seam starts inside the open counter, so the counter flows into the hairline with no shelves. The hairline stone tapers out just before the culet, so the broad stone forms the point, as in a cut Didone V.
- Everything is straight lines computed in `emv2.py` (exact line intersections; no hand-drawn curves). The whole mark is two polygons with 5 vertices each.
- Optical: in every square or circle the mark is centred halfway between its bounding box and its area centroid, because the left-heavy V otherwise sits visibly left. In the horizontal lockup the text block is lifted slightly against the pointed culet.
- Wordmark: VANINDRA is set in Bodoni Moda (variable, opsz 14 / wght 480). Its stress matches the mark's. It is custom spaced pair by pair from outline gaps, not font advances. Every acute vertex is cut flat like a culet: the V base, the A apexes, and the N joints trimmed to cap height and baseline. CREATIONS is set in Jost 400 at 0.40 em tracking, 29% of the cap height, in antique gold. All type is outlined.
- Colour: on ivory, emerald `#0B2A20` with antique gold `#A8843A`. On emerald, soft gold `#D2B26A` with ivory `#F6F1E7`. The mark also works in one colour (`mark_one_colour_gold.svg`) and in any of emerald, ivory or gold.

## Small-size behaviour
- `mark_small.svg` is the same silhouette, solid with no seam. The hairline is thickened from 12 to 15 units, the corner cuts are 10, and the culet is blunted by 3 units so the tip survives rasterising. It is shown in antique gold so `sizes.png` proves it on both ivory and emerald; on light grounds use `mark_small_emerald.svg`.
- It reads as a V at 16, 24 and 32 px. The 45° corners become visible from about 32 px, and the hairline seam from about 64 px; below that the mark simply becomes a strong Didone V, which is the intended degradation.
- Instagram DP: the soft-gold V on an emerald circle is clear at 150, 56 and 32 px. Favicon: `icon_small_on_emerald.svg` fills the tile.

## Exploration (see explore.png and explore_r1..r5.png)
I tried 36 variations in 5 rounds, plus 11 refinement loops. Rejected, with reasons:
- V wedges inside the octagon (01, 02, 04, 08) read as a tuxedo lapel or V-neck.
- The stepped tunnel (03, 17) reads as a lamp or shell, and the V is weak.
- The octagon with a V incision or channel (16, 22, 33, 34) is the knocked-out-letter-in-a-container move. 33 also reads as a phone notch.
- Step-cut V-stones (06, 15, 20, 30) read as an inline neon V, a lanyard or a paperclip.
- The opened emerald (10–13, 19, 28) reads as two crystal bars or a shirt collar.
- Faceted Didone stones with a table rim (r1, r2) read as a beveled 3D crystal or a pencil. This was the key learning: an emerald cut drawn naively is a beveled rectangle, the same sin as the old crest.
- The window cut from the facet diagram (r3–r5) read as crystal shards, a dog-eared collar, or a pencil tip. The geometry survived as the construction.

## Risks (honest)
- At a glance, this is a beautifully cut Didone V. The emerald reading depends on the 45° girdle corners, the two-stone mitre and the construction story. People will not see a gem unless they are shown the construction.
- The octagonal gem silhouette named in the territory is used as the cutting grid, not shown. Every version that showed the octagon became a letter-in-a-container, a lapel, or a bevel.
- The wordmark is only lightly customised (culet cuts plus optical spacing). It is in the same genre as round 1's maison wordmark, although set and spaced far better.
- A tall pointed V can read as a pen nib or arrowhead to some viewers. The narrow 9:16 V leaves side space in square and circle avatars.
- Use the Devanagari name (वनिंद्रा) only after the team verifies it; it is not used here.
