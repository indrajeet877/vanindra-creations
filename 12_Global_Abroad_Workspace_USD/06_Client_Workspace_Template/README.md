# Global Client Workspace Template

> Duplicate this structure for every new global client on Day 1 of onboarding (see `05_Delivery_and_Fulfillment/01_Global_Delivery_SOP.md` §2).
> **Text docs** (strategy, scripts, reports, logs) can live in this repo or in the shared drive. **Video files never go in this repo** — they live in the client's cloud folder (Google Drive / Dropbox / Frame.io).
> **Never store passwords, payment details or client bank info anywhere in these folders.**

---

## 1. Folder Name

```
CLIENT_[ShortName]_[CountryCode]_[Plan]
```
Examples: `CLIENT_ACMEPOD_US_Spark` · `CLIENT_HARBOURPHYSIO_AU_Momentum` · `CLIENT_NORTHWIND_UK_FullStudio`

`ShortName` = 4–12 capital letters, no spaces. It's also the prefix for every video filename.

---

## 2. Folder Structure

```
CLIENT_[ShortName]_[CountryCode]_[Plan]/
├── 00_Admin/
│   ├── client_profile.md          ← contacts, time zone, plan, start date, billing date, primary channel
│   ├── agreement_signed.pdf       ← e-signed service agreement
│   ├── invoices/                  ← INV-[number].pdf copies (no bank or card details)
│   ├── intake_form.md             ← answers from the intake form (§3)
│   └── access_log.md              ← what access we hold, granted by whom, when (NO passwords)
├── 01_Brand_Kit/
│   ├── logos/  fonts/  colours.md
│   ├── caption_style.md           ← font, size, colours, highlight style, position
│   ├── intro_outro/               ← if used
│   ├── references_like.md         ← videos they love (links + why)
│   ├── references_dislike.md      ← videos they don't want to look like
│   └── do_not_say.md              ← banned words, claims, topics, competitors not to mention
├── 02_Strategy/
│   ├── kickoff_notes.md
│   ├── content_pillars.md
│   ├── plan_YYYY-MM.md            ← monthly plan (Momentum / Full Studio)
│   ├── hook_bank.md               ← tested and untested hooks, with results
│   └── competitor_notes.md
├── 03_Scripts/
│   └── YYYY-MM/Week_NN_scripts.md
├── 04_Raw_Footage → [link to cloud folder]
│   └── YYYY-MM-DD_[topic]/        ← client uploads here
├── 05_Edits_In_Progress → [cloud]  ← project files (editors only)
├── 06_Review → [review links]      ← one link per batch
├── 07_Final_Delivered → [cloud]
│   └── YYYY-MM/                    ← approved finals + post captions
├── 08_Covers_Thumbnails/
├── 09_Reports/
│   └── report_YYYY-MM.md
└── 10_Feedback_and_Revisions/
    └── revision_log.md
```

**Video filename:** `[SHORTNAME]_[YYYYMMDD]_[NN]_[short-topic]_v[version]_[9x16|4x5].mp4`
→ `ACMEPOD_20261110_03_sleep-myths_v2_9x16.mp4`

**Permissions:** client = upload to `04_Raw_Footage`, view + comment on `06_Review` and `07_Final_Delivered`. Freelance editors = only `01_Brand_Kit`, `04`, `05`, `06` for clients assigned to them.

---

## 3. `00_Admin/client_profile.md` (template)

```markdown
# [Client name] — Client Profile
- Company / brand:
- Primary contact (name, role, email):
- Approver (if different):
- Country / time zone:
- Plan: Pilot / Spark / Momentum / Full Studio / White-label
- Start date: | Billing date: | Prepay: none / quarterly / annual
- Founding client rate: yes / no (ends: )
- Primary channel: email / Slack / WhatsApp (+91 81128 59437)
- Spelling: US / UK
- Platforms: Instagram / TikTok / YouTube Shorts / LinkedIn / Facebook
- Upload cut-off (their time):
- Studio contacts: Smita Yadav (client relations) · Vandana Yadav (creative) · Akarsh Yadav (editing)
```

## 4. `00_Admin/intake_form.md` — Intake Questions (Send via Tally / Google Forms)

**Business**
1. What do you sell, and roughly what does a customer pay?
2. Who is your ideal customer? (role, age range, location, main problem)
3. Where do most new customers find you today?
4. What should a viewer do after watching? (book a call, visit site, DM a keyword, buy, subscribe)

**Content**
5. Links to your accounts on each platform.
6. Your 3 best-performing videos (links) — and why you think they worked.
7. 3 creators / brands whose content you admire (links) — what do you like?
8. 3 things you never want in your videos (style, topics, words).
9. Any claims we must avoid or always phrase a certain way? (health, finance, legal, results)
10. How often can you film, and for how long?
11. Do you have long-form content we can repurpose? (podcast, YouTube, webinars, talks)

**Brand & logistics**
12. Upload your logo, fonts, colours and any intro/outro.
13. US or UK spelling?
14. Who approves videos, and how fast can they usually reply?
15. Which access can you grant? (Meta Business partner, YouTube channel permission, scheduling tool) — **we never need passwords.**
16. Anything else we should know?

## 5. `00_Admin/access_log.md` (template — NO secrets)

```markdown
| Platform | Access type | Granted by | Date granted | Studio user | Date removed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Instagram (Meta Business Suite) | Partner — content | [client] | YYYY-MM-DD | Smita Yadav | |
```

## 6. `02_Strategy/plan_YYYY-MM.md` (template)

```markdown
# [Client] — Content Plan [Month YYYY]
## Focus this month
- Goal:
- Pillars & split: Reach __% · Authority __% · Story/Trust __% · Offer __%
## What to post / what NOT to post this month
| Post | Don't post |
| :--- | :--- |
## Calendar
| # | Week | Pillar | Format | Topic | Hook (on-screen + spoken) | Source (script / repurpose) | Platform(s) | Post date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
## Tests this month
- Test 1: (e.g., question hooks vs. statement hooks on 4 videos)
```

## 7. `03_Scripts/YYYY-MM/Week_NN_scripts.md` (per video)

```markdown
### Video [NN] — [Topic]
- Length target: __ sec | Energy: __ | Cover title (3–5 words): __
- [0:00–0:02 HOOK] Spoken: "…" | On-screen text: "…" | Editor note: …
- [0:02–0:15 SETUP] Spoken: "…" | Editor note: B-roll / graphic
- [0:15–0:45 VALUE] Spoken: "…" (3 crisp points) | Editor note: numbered pop-ups
- [END CTA] Spoken: "…" | Loop / end frame
- Post caption: first line hook / 2–3 short lines / CTA
- Keywords / hashtags:
- Claims to verify with client: …
```

## 8. `09_Reports/report_YYYY-MM.md` (template)

```markdown
# [Client] — Monthly Report, [Month YYYY]
## Delivery
- Videos planned: __ | Delivered: __ | On time: __% | Rolled over: __ (reason)
- Revisions used: __ rounds
## Performance (from platform analytics — no estimates)
| Video | Platform | Views | Avg. watch time / retention | Shares | Saves | Follows | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
## Top 3 and why they worked
## What didn't work and what we'll change
## Tests for next month
## What we need from you
- Footage by: | Approvals by: | Access needed:
```
*(Spark: Delivery section only. Full Studio: add posting log + community notes.)*

## 9. `10_Feedback_and_Revisions/revision_log.md` (template)

```markdown
| Date | Video file | Round | Requested by | Change requested | Revision or new video? | Done (date) | By |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
```

---

## 10. Checklist — New Client Workspace Ready When…
- [ ] Folder created with the exact name format
- [ ] `client_profile.md` filled in
- [ ] Agreement + first invoice saved (no payment details)
- [ ] Cloud folders shared with correct permissions
- [ ] Intake form + brand kit received
- [ ] Access logged (no passwords)
- [ ] Production board created (one card per video)
- [ ] Kickoff notes saved; style test scheduled
