# Website quick fix and WhatsApp start (17 Oct 2026)

> Internal. Built from Akarsh Yadav's WhatsApp feedback (screenshots, 16 Oct evening) and the owner's instructions.

## Akarsh Yadav's feedback (as sent)
1. "I've checked the website, and honestly, it feels quite laggy when scrolling."
2. "Also, the pointer effect sometimes feels exaggerated."
3. "See, the cursor is not moving freely." (screen recording, 1.2 MB, Windows laptop; not in the cloud session, so the owner needs to send the file)

## What was fixed (branch `claude/stoic-tesla-l103vu`, not live yet)
- Scroll: smooth-scroll library removed; ambient background motion stopped; blurred panels cut from 8 to 3; scroll-linked parallax off. Frame time while scrolling (no graphics card): median 50 ms → 16.7 ms.
- Pointer: magnetic pull off; card tilt and phone tilt cut hard; glare only on the hovered card; gold trail reduced.
- Cursor: the small dot follows the pointer exactly; the ring follows faster and only nudges towards buttons; the native cursor comes back over text fields and when the pointer leaves the page; stuck press and drag states clear.
- Copy: the unconfirmed "First edit within 48 working hours" line is replaced with a neutral line.
- Full details and measurements: `previews/website_2026-10-17_quickfix/README.md`.

## Reply to send to Akarsh Yadav (owner's voice, Hinglish, draft)
> Akarsh, thanks, teeno points note kar liye: scroll ka lag, pointer effect ka zyada hona, aur cursor ka ruk-ruk ke chalna. Fix kar diya hai. Preview yahan dekh lo (laptop pe, aur phone pe bhi): https://claude.ai/artifact/GmaBWkmKyFXVrxgk5cpXYV
> Ek kaam: apni screen recording wali video yahin bhej do, taaki hum frame-by-frame check kar sakein ki cursor kab atakta hai.

## Open before going live
1. The owner says OK. Then the branch is merged to main, and GitHub Pages rebuilds.
2. Mobile check at 390×844 (not measured yet).
3. Akarsh's video, to confirm the cursor fix on the same case.
4. Akarsh's public email digits (see `04_Outreach_and_Sales_Pipeline/07_WhatsApp_Business_Setup_and_Daily_Routine.md`, section 5).

## WhatsApp start
Plan and drafts: `04_Outreach_and_Sales_Pipeline/07_WhatsApp_Business_Setup_and_Daily_Routine.md`. Free app, Rs 0, one official number, daily routine by person.
Gemini prompts for the owner's Mac: `08_Agent_and_LLM_Instructions/07_Gemini_Mac_Task_Prompts_2026-10-17.md`.

## Still with the 10x rebuild and the logo
- Logo: the final round (polish and judging) did not finish because of the session limit. No logo is final, so the profile picture is blank until the owner decides.
- 10x rebuild: waits for the logo decision. It is not part of today's fix.
