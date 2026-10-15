# Canopy Signature — VanIndra Creations (territory: Founder Signature)

## Public story (one sentence)
One unbroken pen stroke joins *Van* and *Indra*: the hairline that rises out of the V becomes the canopy over the name — the sky over the forest — and comes down as the I.

## The idea
- **Wordmark:** a drawn signature, "VanIndra", in a high-contrast pointed-pen script. Its one controlled swash is the **canopy**: the V's hairline doesn't stop at the top of the letter. It keeps rising, runs over "an" as a single hairline and turns down into the shaded I. So the two halves of the name are signed in a single gesture.
- **Mark:** the same gesture with "an" taken out. It's a V–I ligature: shaded V arm, hairline rising, a short canopy turn, shaded I. The mark and the wordmark call the same construction functions, so the mark really is cut from the signature, not drawn separately. At 16 px it reads as a bold V; from about 32 px the I shows.
- **CREATIONS:** Jost 400 in caps, tracked +0.44 em, with optical pair kerning (A–T −0.06 em, I–O/O–N −0.015 em). It's set flush right under the signature, like a title under a name.

## Construction notes
- **Not a font.** Every stroke is a centre-line skeleton built from a grid in an upright design space: x-height X = 100, caps 252, d ascender 212, stem unit U = 70.
  - Underturn radius 12, overturn radius 11.
  - Bowls are true ellipses (rx 31, ry 50). Connectives are computed as the internal tangent line between the underturn and overturn circles.
  - Arcs use exact Bézier handles, h = r·4/3·tan(φ/4). Nothing is eyeballed.
  - The whole skeleton is then sheared to a single 18° slant, so every stem, bowl axis and connective shares one angle.
- **Pen logic.** A simulated pointed nib:
  - The pen only shades when moving down the slant axis; every upstroke and the whole canopy are hairlines by rule.
  - Pressure changes use C1-continuous profiles: ramps go soft start → straight → soft finish, tapers go soft shoulder → straight wedge to a point. So there are no corners, "necks" or bulbs.
  - Ball terminals (the V's entry and the r) are blended into the stroke (w = √(w² + bump²)), giving a filleted drop instead of a stuck-on dot.
- **Outline.** The outline is the exact envelope of the moving round nib (including dr/ds), curve-fitted to clean cubics (Schneider) and unioned with pathops. All text is outlined; every file is under 30 KB.
- **Joins.**
  - The n→d connective runs up the inside of the d's bowl, so it is hidden in the shade instead of slicing through the counter.
  - The I's foot loop crosses back over its own stem on a rising curve and flows into the n. This is the classic roundhand capital I.
  - Stems end on the baseline at full pressure, with the round end sitting exactly on the line.
- **Optical sizes of one pen** (hair / shade, on the 252-unit cap):
  - wordmark: 5 / 18
  - mark: 7 / 26
  - mark_small: 19 / 45, with the entry hook removed and a wider turn so the counter stays open.

## Colour
- On ivory: emerald `#0B2A20` signature and mark, antique gold `#A8843A` CREATIONS and rule.
- On emerald: ivory `#F6F1E7` signature, soft gold `#D2B26A` mark, CREATIONS and rule.
- `mark_small` is antique gold so the transparent favicon holds on both light and dark grounds (about 3.1:1 on ivory, 4.3:1 on emerald).
- Everything is flat and works in one colour.

## Small-size behaviour
- `mark_small.svg` stays a legible "VI" at 16, 24 and 32 px on both ivory and emerald (see sizes.png): the two shaded strokes carry the read.
- In the 110 px Instagram circle the display mark fills about 60 % of the circle and sits inside the circle-safe area.
- The hairline canopy is decorative below about 40 px wordmark height. At small sizes the wordmark still reads, from the shaded strokes and the I's loop.
- For browser favicons, use `mark_small_on_emerald.svg` (supplied) rather than the display mark.

## Risks and caveats
- **"VI" ligature:** some may read it as the Roman numeral six. It's mitigated by always pairing it with the signature in launch material.
- **Script capital I:** the roundhand I with a foot loop is standard but can be misread as a J by people unfamiliar with scripts. This is why the I keeps its loop in the wordmark (the tapered version read as "/" or "l" in testing).
- **The canopy is a strong gesture.** It could feel decorative if misused (for example, recoloured or stretched). Never distort the canopy, and never set the signature smaller than about 24 px x-height on screen without the mark.
- **This is a designed brand signature, not Vandana Yadav's personal autograph.** It should not be used on documents as her legal signature.
- **No Devanagari version yet.** A वनिंद्रा companion would need to be drawn separately, and verified by the team.

## Files
- **Marks:** `mark.svg`, `mark_small.svg`, `mark_on_ivory.svg`, `mark_on_emerald.svg`, `mark_one_colour_gold.svg`, plus extra `mark_small_on_emerald.svg` and `mark_small_on_ivory.svg`
- **Wordmark:** `wordmark.svg`
- **Lockups:** `lockup_horizontal_on_ivory.svg`, `lockup_horizontal_on_emerald.svg`, `lockup_stacked_on_ivory.svg`, `lockup_stacked_on_emerald.svg`
- **Renders:** `sheet.png`, `sizes.png`, `context.png`, `explore.png`
- **Generator:**
  - `build.py` — deliverables
  - `sig.py` — final construction
  - `word2.py`, `mono.py`, `geo.py` — lettering, monogram and geometry helpers
  - `pen.py` — pen engine
