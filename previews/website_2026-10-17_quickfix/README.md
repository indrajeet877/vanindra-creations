# Quick-fix preview of the live homepage (17 Oct 2026)

> **Status:** preview only. Not live. The live site is still the 16 Oct version until the owner says OK and this branch is merged to main.
> **Noindex:** the page is marked `noindex`; the folder is excluded from GitHub Pages in `_config.yml`.

## What changed (from Akarsh Yadav's feedback: laggy scroll, exaggerated pointer, cursor not moving freely)
- **Scroll:** smooth-scroll library removed (native trackpad scrolling). Background blobs, the chips and the marquee no longer animate forever; the marquee runs only while on screen. Full-page grain layer no longer uses a blend mode. Scroll-linked parallax, hero drift and panel scale switched off. Desktop WebGL orbit capped at 30 fps and reads layout only when the canvas changes.
- **Blur:** blurred panels cut from 8 to 3 on a desktop screen (nav, segment pill, and the rare modal). Other glass is a solid translucent fill with the same rim light.
- **Pointer:** magnetic pull on buttons off; card tilt cut from 4° to about 1°; phone tilt cut from 8°/6° to 2°/1.5° and only with a mouse; glare only on the hovered card; gold trail reduced to a few sparks on fast moves.
- **Cursor:** the small dot follows the pointer 1:1. The ring follows faster (about 20 ms lag, down from 42 ms) and only nudges towards buttons. The native cursor comes back when the pointer leaves the page or enters a text field. A stuck press or drag state now clears on cancel, on window blur, and when the drag capture is lost.
- **Copy:** the unconfirmed "First edit within 48 working hours" line is replaced with "We confirm your first-edit time on WhatsApp once we have seen your footage." (the team has not confirmed the 48-hour promise).

## Measured (headless Chromium, no GPU, 1440×900)
| | Before (16 Oct) | After |
| :--- | :--- | :--- |
| Blurred panels in view | 8 | 3 |
| Infinite animations running | 8 | 0 |
| Running animations (total) | 21 | 1 |
| Frame time while scrolling, WebGL off (median / slow frames over 50 ms, 2 runs) | 50 ms / 28–41 | 16.7 ms / 0–7 |
| Frame time while scrolling, WebGL on (median / p95) | 167–216 ms / 416–583 ms | 33–50 ms / 267–283 ms |
| Console errors | 0 | 0 |

The WebGL-on numbers are from a machine with no graphics card, where the glass ring is drawn in software. Real laptops are expected to be much faster; this has to be confirmed on the Windows laptop.

## Still to check before going live
1. Akarsh's screen recording (1.2 MB) — send the file so the cursor can be compared frame by frame.
2. Mobile: the same check at 390×844 (not measured in this round).
3. Owner OK, then merge to main and check the GitHub Pages build.
