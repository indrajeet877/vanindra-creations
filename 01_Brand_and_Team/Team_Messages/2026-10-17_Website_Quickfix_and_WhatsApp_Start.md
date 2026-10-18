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

## Update, 18 Oct (owner's answers)
- The screen recording shows lag only; the quick fix covers it.
- +91 81128 59437 is the official desk number, not personal; it moves to the WhatsApp Business app.
- Akarsh Yadav's public email removed from the homepage and login page; the build script now blocks those digits.
- Profile picture chosen: the "nI" monogram from the F1 logo (`01_Brand_and_Team/Brand_Assets/Logo_2026-10-18_F1_Matched_Hinge/profile_picture/dp_ivory_640.png`).
- Phone check (390×844, CPU slowed 4×): already 60 fps before and after; endless animations 2 → 0.
- Owner wants bulk work done by Gemini or Grok through a CLI. This session has no API key for either; Grok's API is also blocked by the network here. Prompts for the Mac: `08_Agent_and_LLM_Instructions/07_Gemini_Mac_Task_Prompts_2026-10-17.md`.
