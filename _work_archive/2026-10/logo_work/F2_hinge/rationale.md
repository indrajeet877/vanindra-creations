# F2 · The Hinge (finalist polish): one stroke, two words

## One-sentence public story
VanIndra joins two old words, *van* (the forest) and *Indra* (the sky and its rain), and the logo writes them with one shared gold stroke, the forest and the rain that makes it grow.

For Hindi audiences, add this line only after the team has verified the Devanagari: in **वनिंद्रा** the same join is one sign, **नि**, and its gold **ि** stands on the same vertical as the gold stroke in the Latin name.

Tell the story as forest and sky only. Never explain the name any other way.

## What the system is
| Part | What it is | Where it lives |
|---|---|---|
| **Signature** (primary logo) | The staircase. *Van* is on line 1 and *Indra* on line 2. The n's right leg drops into the I. | Website header, decks, print, Reel credit |
| **Symbol** | The hinge on its own: the n of Van and the I of Indra sharing one stroke. | Profile picture, favicon, app icon, merchandise |
| **Wordmark** | One line, *VanIndra*. The n and I stand apart, the I is at cap height and in gold. | Anywhere that can only take one line |
| **Lockups** | Signature + *Creations* (horizontal and stacked), plus bilingual (one line over वनिंद्रा) | Letterhead, covers, Hindi-first material |
| **Global** | The horizontal lockup on white, Latin only | USD / international workspace |

**Gold marks the shared stroke, and only that.** In the signature and symbol, the gold is the n's right leg from half the x-height down, the shared slab and the I. These are one piece. The colour break on the leg is cut at the system's knife angle (20°). In the one-line wordmark the gold is the I. In Devanagari it is the ि.

## What changed after the final judges (F2)
1. **The join is now one stroke, not a post in a collar.** In R3 the colour changed on top of the slab, so gold brackets flared round an emerald stem. Now the gold starts on the n's leg, so the leg, the slab (the n's foot and the I's head at once) and the I are one gold piece. Gold no longer picks out "Indra": the stroke belongs to both words.
2. **A real symbol, drawn from the hinge.** The R3 favicon (a stock-looking Didone V) and the R3 avatar (the staircase set small) are both retired. The new symbol is the hinge itself. The **icon cut** (stem 116, arch top 58, slab 38) is for the profile picture, favicon and app icon. In the circle the n's x-height is 40 % of the diameter, and the gold pin runs off the bottom edge as it continues into Indra. It reads at 110, 48, 40, 32 and 24 px (`loops2/zoom_3x.png`, `sizes_mark.png`), and it survives in a 16 px browser tab.
3. **d redrawn.** It is now as wide as the n (420, was 356). The counter is one oval: outer and inner contours are ellipses, with thin joins at 0.86 and 0.78 of the x-height. There is no flat wall and no corner or spur at the bottom left.
4. **One-line I at cap height (700), level with the V** (it was 724, about 3 % above). The change is in `wordmark`, `wordmark_small` and `wordmark_mono`. Only the staircase keeps the ascender-tall I.
5. **Staircase I-to-n gap opened** from 24 to 36 units (the same as the d-to-r gap), so the feet no longer fuse in small headers.
6. ***Creations* lightened.** It now has about 10 % optical compensation at 58 % size: stem 86, C ring 90 (was 106), hairline 29. The e's eye is opened (bar lower and thinner) and the s spine is 10 % lighter. It is no longer darker than the name it qualifies.
7. **Bilingual lockup rebuilt.** The gold I and the gold ि now share one vertical axis, so the gold reads as one line through both scripts. The Devanagari is drawn in a lighter cut: a danda equals the Latin stem, and the headline height equals the Latin cap height (700).
8. **Devanagari redrawn** (still **to be verified by the team**):
   - The ि hook is one smooth pen stroke with no kink, and it lands on the shirorekha, as written.
   - द्र hangs 84 units below the baseline (was 150). Its tail and rakar are shorter and lighter.
9. **Photo contrast rule.** On photographs the Reel credit is always one colour: all ivory on dark footage and all emerald on light footage. Gold is used only on flat brand grounds.
10. **Craft bug fixed.** The R3 staircase was clipping the right half of the left foot on Van's n. It is now whole.

## Construction notes (construction.png)
- Every Latin and Devanagari glyph is drawn from cubic béziers, straight segments and pen-expanded spines in `vitype.py` and `deva.py`. No font outlines appear in any deliverable. Manrope is used only for UI labels in the mocks and boards; it is not part of the identity.
- **Grid** (1000 units): x-height 490, cap 700, ascender 724, overshoot 11. Staircase line spacing L = 724 − 21 = 703, so the I is exactly ascender-tall.
- **Optical cuts:**

  | Cut | Use | Stem | Hairline / arch top |
  |---|---|---|---|
  | display | 64 px and up, print | 82 | 24 |
  | small | headers, Reel credit, email | 90 | 34 |
  | icon | avatar, favicon, app icon | 116 | arch top 58 |
  | Creations | descriptor at 58 % size | 86 | 29 |

- **Terminals:** every free stroke end is the same knife cut rising at 20° (a, r, s, C, e, t, y, and the Devanagari dandas and hooks).
- **Palette:**

  | Colour | Hex | Contrast |
  |---|---|---|
  | emerald | `#0B2A20` | 13.6 : 1 on ivory |
  | ivory | `#F6F1E7` | |
  | antique gold | `#A8843A` | 3.1 : 1 on ivory, 3.5 : 1 on white; used for strokes only, never for text |
  | soft gold | `#D2B26A` | 7.6 : 1 on emerald |

  One-colour versions are all emerald, all antique gold, and all ivory on emerald.

## Files
| File | What | Use |
|---|---|---|
| `staircase.svg`, `staircase_on_emerald.svg`, `staircase_one_colour_{emerald,gold,ivory}.svg` | Signature, display cut | Hero, print, merchandise, decks |
| `header_staircase_{emerald,ivory}.svg` (+ `_mono_`) | Signature, small cut, tight crop | **Website header**, footer, **email signature** |
| `mark.svg`, `mark_one_colour_{emerald,gold,ivory}.svg` | Symbol, full I, small cut | Symbol at 64 px and up, stamps, foil |
| `mark_on_emerald.svg` / `mark_on_ivory.svg` | Symbol, icon cut, pin bleeding off the edge, made for a circle crop | **Instagram / WhatsApp / YouTube / LinkedIn profile picture** (emerald is the hero) |
| `mark_small.svg` / `mark_small_ivory.svg` | Symbol, icon cut, short pin with its foot, transparent | Anything 48 px and below on a flat ground |
| `mark_small_tile.svg` | Symbol, icon cut, on an emerald tile | **Favicon** (16/32/48), apple-touch-icon 180, PWA 512 |
| `wordmark.svg` / `wordmark_mono.svg` / `wordmark_small.svg` | One line, gold I at cap height | One-line places only |
| `lockup_horizontal_on_{ivory,emerald}.svg` | Van / Indra Creations | Letterhead, wide spaces |
| `lockup_stacked_on_{ivory,emerald}.svg` | Van / Indra / Creations | Covers, title slides, packaging |
| `lockup_bilingual_on_{ivory,emerald}.svg`, `wordmark_devanagari.svg` | With वनिंद्रा | Hindi-first India material, **after the team verifies the Devanagari** |
| `reel_tag_ivory.svg` / `reel_tag_emerald.svg` | "edit by" + signature, one colour | Reel cover credit |
| `global.svg` / `global.png` | Horizontal lockup on white, Latin only | USD workspace |
| `board.png` | Team presentation board | Tomorrow's vote |

## Size rules (which file at which size)
| Size / place | Use |
|---|---|
| Signature **40–63 px tall** on screen (cap 19 px and up) | `header_staircase_*.svg` (small cut). Desktop header: 64 px tall. Phone header: 44 px tall in a 64 px bar |
| Signature **64 px tall and up**, or **40 mm wide and up** in print | `staircase*.svg` and the lockups (display cut) |
| **Below 40 px tall** | Don't shrink the signature. Use the symbol, or `wordmark_small.svg` if the name must be spelled |
| Horizontal lockup | 200 px wide and up on screen, 60 mm in print. Below that, use the signature alone |
| Stacked lockup | 160 px wide and up on screen, 45 mm in print |
| Bilingual lockup | 280 px wide and up on screen, 80 mm in print. Only after the Devanagari is verified |
| One line only | 14–63 px tall: `wordmark_small.svg`. 64 px and up: `wordmark.svg`. Under 14 px: plain text "VanIndra Creations" |
| **Profile picture** | `mark_on_emerald.svg` everywhere. Instagram uses one image at every size, and this one reads from 320 px down to 24 px |
| **48 px and below** (favicon, small app icons, map pins) | `mark_small_tile.svg` on unknown grounds; `mark_small.svg` / `_ivory` on flat ivory or emerald |
| Symbol 64 px and up | `mark.svg`, or a one-colour version |
| **Email signature** | `header_staircase_emerald.svg` at 48 px tall (not the one-line wordmark) |
| **Reel credit** | `reel_tag_ivory.svg` on dark footage, `reel_tag_emerald.svg` on light footage. 64 px tall on a 540 × 960 cover (128 px on 1080 × 1920), 30 px from the left and 150 px from the top. This keeps it inside the 3:4 profile-grid crop (y 120–840) and clear of the caption overlay. **Never gold on a photo** |
| **Embroidery** (1 mm test: render at 10 px/mm, open with a 1 mm disk) | Caps, sleeves, pockets: `mark_small` one colour, **20 mm tall or more**. At 20 mm only the serif tips round off (`loops2/emb/diff.png`). Signature small cut: **90 mm wide or more**. Never embroider the Creations lockups below 250 mm wide. Ask the digitiser to keep strokes at 1 mm or more |
| Foil / emboss | Signature 30 mm wide or more; symbol 12 mm tall or more |
| Offset / digital print | Signature 25 mm wide or more |

**Clear space:** one x-height of the artwork on every side.

**Never:**
- retype the name in a font;
- put the signature on one line;
- move the gold off the shared stroke;
- use gold on a photograph;
- use antique gold for text.

## Honest risks
1. **The name split needs the owner's conscious sign-off.** The signature sets *Van* over *Indra*. With gold now on the shared stroke rather than on Indra's I, and the story told as forest + sky, the emphasis is on the join rather than on a second name. Even so, a two-line, two-capital name invites "what is Indra?". To an English reader, "Van" on its own line can also read as the vehicle. If the owner is uncomfortable, the fallback is the one-line wordmark as the primary logo, with the symbol as the avatar.
2. **The symbol is a lowercase n with a long leg.** Some people will read it as the Greek η (eta). It is not a V or an I, so nobody will "spell" the brand from the avatar alone. It is recognised by its shape and its gold. Instagram shows the handle next to it.
3. **The one-line wordmark carries no ligature.** Only the gold I marks the join. Because of that, the rules send the email signature, invoices and deck footers to the signature (it works from 40 px tall). The one-line version is for places that genuinely can't take two lines. A shared-foot one-line version was tried and misread as "VanLndra", so it was rejected (`explore.png`, row 4).
4. **Antique gold on ivory is only 3.1 : 1.** It is fine as a stroke, but at the 44 px phone header the gold is visibly lighter than the emerald. If it looks weak in a particular build, use `header_staircase_mono_emerald.svg`.
5. **Devanagari** was drawn in code by a non-native designer, using the anatomy of Tiro and Noto Serif as reference. **Verify before any use**, especially:
   - the conjunct द्र (drop, tail and rakar);
   - where the ि hook lands;
   - the bindu position;
   - the knife-cut danda feet.

   The spelling is **वनिंद्रा** in every file.
6. **Drawn in code, not by a foundry.** The curves are clean at the sizes tested (up to 1600 px wide). A type designer should polish the s, the a terminal and the Devanagari before billboard use. Only these glyphs exist: V a n d r I C e t i o s b y, and वनिंद्रा.
7. **The step can be "corrected"** by a developer or printer into one line, or retyped in a font. Supply only the SVGs.
8. **Genre.** It is still a high-contrast editorial serif. The ownable parts are the staircase, the gold shared stroke and the symbol crop, not the letters on their own.
9. **Not tested with real readers yet.** Before approval, run a 5-second test with 10 Indian and 10 overseas people. Show them the 44 px phone header and the 40 px avatar, and ask "what does this say?" and "what does this remind you of?".

## Final judges' must-fix items: what happened
| Must-fix | Status |
|---|---|
| Favicon is a stock Didone V (judges 1, 2, 3) | **Fixed.** The small mark is the hinge, in a heavier icon cut |
| Avatar is the name set small and turns to texture at 32–40 px (1, 2, 3) | **Fixed.** A drawn avatar from the hinge, legible at 24 px |
| d is narrow, with a slot counter and a corner/spur (1, 2) | **Fixed** |
| One-line I sits above the cap line (1) | **Fixed** |
| Staircase I-n feet fuse (1) | **Fixed** (gap 36) |
| *Creations* about 40 % too heavy (1) | **Fixed** (about +10 %) |
| The join reads as a post in a gold collar (1, 3) | **Fixed.** The gold is carried up into the n's leg |
| Gold disappears on warm photos (2) | **Fixed.** Photos are one colour only, plus a contrast rule |
| Bilingual golds misaligned; Hindi line louder (2) | **Fixed** |
| Devanagari ि kink; द्र oversized (2, 3) | **Redrawn.** Native sign-off is still required |
| One-line wordmark has no hinge (3) | **Partly.** Usage rules move the one-line contexts to the signature; see risk 3 |
| Embroidery falls back to the generic V (3) | **Fixed.** Small merchandise uses the hinge symbol at 20 mm or more |
| Name split / "who is Indra?" (1, 2, 3) | **Mitigated, not removed.** The story is now forest + sky and the gold sits on the shared stroke. The owner must sign off (risk 1) |
