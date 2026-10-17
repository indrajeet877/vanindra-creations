# Gemini CLI prompts for the owner's Mac (17 Oct 2026)

> Run these in Gemini CLI (Argon High) from the project folder: `cd "/Users/vanindra/Downloads/Influencer  Agency"` then `gemini`. Gemini reads GEMINI.md and AGENTS.md first, so the golden rules apply.
> **Rule for every prompt:** report only. Do not edit, commit or push. Paste the report back to Claude.

## Prompt 1: golden-rule scan before any merge
```
Read GEMINI.md and AGENTS.md. Then scan these files for the following, and report file and line for every hit. Do not edit anything.
Files: index.html, login.html, thumbnail-studio.html, previews/website_2026-10-17_quickfix/index.html, 07_Website_and_Client_Portal_Spec/index.html, 07_Website_and_Client_Portal_Spec/login.html.
Look for: "Guggy", "Sahil", "Indrajeet" (any case); any phone number other than 8112859437 / 81128 59437; any wa.me link not ending in 918112859437; "github.io" anywhere in visible text; "7-day audit" or "7 day audit"; "guarantee" not preceded by "no" or "not"; "Most popular"; any link to pitch-deck.html; "preview" appearing more than once in visible text on index.html.
Output: a table with columns File | Line | Text | Rule. Then one line: CLEAN or N issues.
```

## Prompt 2: check the WhatsApp drafts against the confirmed-promises list
```
Read 04_Outreach_and_Sales_Pipeline/07_WhatsApp_Business_Setup_and_Daily_Routine.md, section 6 (promises) and section 2 (quick replies).
For each quick reply and the greeting, list any sentence that promises a time, a count, a price, a guarantee or a result that section 6 does not allow.
Also check that no quick reply contains a link other than wa.me/918112859437 or a placeholder.
Output: a list of problem sentences with their location, or "No problems found". Do not edit.
```

## Prompt 3: Hinglish check (native review)
```
Read 04_Outreach_and_Sales_Pipeline/07_WhatsApp_Business_Setup_and_Daily_Routine.md, section 2.
Check each Hinglish message for: gender-neutral wording (no "chahta/chahti" and no gendered "karenge/karungi" that assumes the reader's gender), spelling in Roman Hindi, and tone (polite, not pushy).
Suggest a replacement only where a line is unclear or gendered. Keep the same meaning and length.
Output: a table of line | problem | suggested change. Do not edit.
```

## Note
Gemini's output is a draft for Claude to review. Anything that goes to a client, on a public page or into a WhatsApp profile still needs the owner's OK.
