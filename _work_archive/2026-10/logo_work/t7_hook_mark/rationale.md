# Hook + Tick: VanIndra Creations (territory t7, The Hook Mark)

## Concept name
**Hook + Tick**

## One-sentence public story
Our V is cut once: the gold piece above the cut is the hook, the first thing your eye lands on, and what stays below it is a tick, the approval it earns. Every Reel we make works the same way: hook first, then the hold.

## The idea
- **One form, three readings.** At first glance it is a V, the initial of VanIndra. Look again and the emerald part is a complete tick (✓): a short stroke and a long stroke. The gold piece is the hook that sits on top of it. Hook + tick = V.
- **The cut is the studio's real work.** Editing is cutting, and the core service is deciding what to post and what not to post. The mark contains exactly one cut, placed where a creator's idea becomes an approved post.
- **Gold sits where the eye lands first.** Reading starts top-left, so the hook occupies the top-left of the V. That is the "first 3 seconds" position of the mark.
- **Not a letter in a container, not a checkbox icon.** There is no frame, circle or tile around it. In the profile-picture circle it reads as a V first, not as a verified-badge tick.

## Construction (generator: `build.py` + `hookmark.py`; drawing: `construction.svg`)
- Grid: cap height H = 1000, baseline 0.
- **Angle.** Both outer edges run on the diagonals of a 9:16 frame (dx : dy = 9 : 16, which is 29.36° off vertical). The V is literally two Reel diagonals meeting at the baseline.
- **Stroke.** Swiss monoline. The perpendicular stroke is 125 on both arms; the horizontal width is 125 / cos 29.36°.
- **Vertex.** A sharp point at the exact intersection of the outer edges. It overshoots the baseline by 30 (3%), so it optically sits on the baseline next to text.
- **The cut.**
  - One horizontal band, 24 high, through the **left arm only**, centred at **9/16 H**.
  - Below the cut, the tick's two strokes stand **9 : 16**: the short stroke reaches 9/16 H, the long stroke reaches H.
  - Above the cut, the hook is an exact 4-point parallelogram.
- **Geometry check.** Everything is straight lines from exact line intersections, with no Bézier curves anywhere in the mark. The tick is 1 contour and the hook is 1 contour.
- **Optical centring.** In squares and circles the mark is placed halfway between its bounding-box centre and its area centroid, because the V carries its mass at the top.
- **Colour.**
  - On ivory: tick in emerald #0B2A20, hook in antique gold #A8843A.
  - On emerald: tick in ivory #F6F1E7, hook in soft gold #D2B26A.
  - One colour (gold, emerald or ivory): the 24-unit cut alone carries the idea.

## Wordmark
- **VANINDRA** is set in Jost 500 for N, I, D and R. **The V and both A's are redrawn on the brand's 9:16 angle**, with Jost's own stem as the perpendicular stroke. The A's are the V inverted, with a bar at 0.31 cap that is 0.78 stem thick. So the mark's diagonal runs through the whole name.
- **VA is a custom fit.** Its two diagonals are parallel, so the pair nests on a parallel channel whose area equals a normal stem-to-stem gap.
- **Hand-set optical kerning.** Tracking is +0.12 em. Pair adjustments: NI +0.010, IN +0.010, ND +0.004, DR −0.004, RA −0.030 (em). For pairs that touch a redrawn letter: EA −0.012, AT −0.045.
- **CREATIONS** is Jost 400, also with the brand A, tracked +0.30 em, in gold.
  - In the two-line lockups it is set flush left (Swiss) and is 0.37 of the word size.
  - In the stacked lockup it is centred.

## Lockups
- **`lockup_horizontal_on_*` (primary, one line).** Mark at 1.62 × cap height, centred optically on the caps without its overshoot. It is chosen as primary because it stays legible at a 52 px header height (about 16 px caps). A two-line version would shrink CREATIONS to about 5 px.
- **`lockup_horizontal_twoline_on_*` (print and large).** The mark spans exactly from the VANINDRA cap line to the CREATIONS baseline, with its point overshooting.
- **`lockup_stacked_on_*`.** Mark at 2.75 × cap height, centred, with a gap of 0.95 cap.

## Small-size behaviour (`sizes.png`, `context.png`)
- **`mark_small.svg`** is for ≤48 px: stroke 178 (instead of 125) and cut 70 (instead of 24). The cut survives as a visible notch down to 16 px.
  - It is one colour, antique gold, so the same transparent file reads on both ivory and emerald grounds.
  - Tiled versions `mark_small_on_emerald.svg` and `mark_small_on_ivory.svg` are included for favicons and app icons.
- **Profile picture.** `mark_on_emerald.svg` reads clearly at 150, 56 and 32 px. The two-tone split stays visible at 32 px.

## Files
- **Marks:** `mark.svg`, `mark_small.svg`, `mark_small_on_emerald.svg`, `mark_small_on_ivory.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg`, `mark_one_colour_emerald.svg`, `mark_one_colour_ivory.svg`
- **Wordmark and lockups:** `wordmark.svg`, `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_horizontal_twoline_on_*.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`
- **Drawing:** `construction.svg`
- **Renders:** `sheet.png`, `sizes.png`, `context.png`, `explore.png`. The full exploration (53 variations) is in `explore/` and `explore_r1..r8.png`.

All text is outlined paths, and every SVG is under 80 KB.

## Risks (honest)
- **The first read is "a geometric V with a gold piece".** The tick appears on a second look. Without the story, it could be mistaken for a template "V with accent". The idea depends on the hook/tick explanation being told once.
- **Stutter in horizontal lockups.** "V VANINDRA" repeats the V. This is the usual initial-plus-name pattern (as with many maison monograms), but it is noticeable.
- **The wordmark is only partly custom.** Only V and A are drawn; N, I, D, R and the CREATIONS letters are Jost.
- **Contrast.** Antique gold on ivory has modest contrast (about 3.2:1). The hook is an accent, not the legibility carrier.
- **One-colour versions** rely on a 24-unit cut that closes below about 40 px. Use `mark_small` at small sizes.
- **Exploration notes.**
  - A Didone-contrast version was avoided on purpose, because territories t1–t4 already use thick/thin V's.
  - A watch-hands-at-10:10 direction (time, Swiss precision) had the best story but failed at small sizes (2.7:1 aspect) and read as a clock icon.
