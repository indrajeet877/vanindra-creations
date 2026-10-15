# Final website: Liquid Glass + 3D glass, magic cursor, cinematic motion (15 Oct 2026)

> **Status:** waiting for the owner's OK. **Not live yet.** The live website is still Focus Story.
> **Private preview, with videos:** https://claude.ai/artifact/MgcLqYnXWBsWhgEpReD1jZ

## What the team asked
- Akarsh (WhatsApp): the Liquid Glass hero ("You just record. We handle everything else.") "made with 3-D glass, a magic cursor and cinematic motion".
- Owner: the client login page "is not looking good", and was never redesigned.

## Files here
| File | What it is |
| :--- | :--- |
| `index.html` | New homepage. Liquid Glass, plus a live WebGL glass ring around the hero phone, the magic cursor (desktop only), the intro, the word-by-word headline and the raw clip "polishing" into the edit. |
| `login.html` | Redesigned "Client portal (preview)": glass sign-in, sample workspace, Reel approvals, "Send a raw video" to WhatsApp. It says plainly that it is a preview, and it has no invented numbers. |
| `thumbnail-studio.html` | Restyled Reel cover studio: 4 looks, 1080×1920 PNG download, and a live mini cover on phones. |
| `screens/` | Preview images and video contact sheets. |

These copies use `../../assets/`, so open them from inside the project folder. All three files are marked `noindex`.

## Checks (15 Oct 2026)
- Homepage `verify.js`: PASS 56 · WARN 1 (mobile height 12,815 px, under the 13,500 budget) · FAIL 0.
- Login + studio `verify_pages.js`: PASS 151 · WARN 0 · FAIL 0.
- `scripts/build_public_site.sh` passes with all three pages swapped in.
- Reviewed by:
  - a design director (6.5 → all 4 blocking fixed);
  - a creator on a mid-range Android in Hindi (7 → 2 fixed);
  - a QA/performance engineer (7.5 → 4 fixed);
  - a design + QA reviewer for the login and studio pages (7.7 → 2 fixed).

## Open points for the owner
1. OK to go live? Going live means copying these three pages to the repo root, fixing the asset paths, removing `noindex`, and updating the `07_Website_and_Client_Portal_Spec/` mirror.
2. The login preview has no password field, because there is no server yet. Is that OK?
3. A native Hindi reader should check the Hindi text, especially the new lines on the login page.
4. The glass speed has not been measured on a real phone or laptop. The sandbox has no GPU.

Sources and notes: `_work_archive/2026-10/website_designs/final_liquid_glass_3d/`.
