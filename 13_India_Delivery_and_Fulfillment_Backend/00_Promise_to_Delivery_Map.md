# 00 — Promise-to-Delivery Map (Public Website Audit)

> **Purpose:** Every concrete promise, offer or claim on our public pages, with what it takes to actually fulfil it, who owns it, and whether we are ready today.
> **Principle (owner's instruction):** *We do not take money for anything we cannot deliver.* If a row says **Not ready** or **Mock-only**, we either fix the backend first or change the website wording (see `03_Risky_Claims_and_Fixes.md`).
> **Audited:** root `index.html`, `login.html`, `pitch-deck.html`, `thumbnail-studio.html` at commit `0918441` (14 Oct 2026). Line numbers (`L####`) refer to that commit. The copies in `07_Website_and_Client_Portal_Spec/` are mirrors and were not audited separately.
> **Nothing on the website was edited.** All fixes below are recommendations for the owner to approve.

---

## Legend

| Readiness | Meaning |
| :--- | :--- |
| **Ready** | We can deliver this today with the people, tools and documents we already have. |
| **Partly** | Skill/people exist, but a template, tool account, SOP, policy or capacity limit is missing. Deliverable with small fixes. |
| **Not ready** | Nothing in place yet (no tool, no template, no SOP, or capacity does not exist). Do not sell until fixed. |
| **Mock-only** | The page *shows* it working, but it is a front-end demo with fake or browser-only data. Nothing reaches the team. |

**Owners:** **Vandana** = Vandana Yadav (creative QA, scripts, on-camera) · **Smita** = Smita Yadav (WhatsApp desk +91 81128 59437, sales, onboarding, billing, brand deals) · **Akarsh** = Akarsh Yadav (editing, tech, health/food fact-checks) · **Owner** = business owner sign-off on pricing, policy and website copy.

---

## 1. One-Page Verdict: What We Can Sell Today

| Offer | Sell now? | Condition |
| :--- | :--- | :--- |
| Free 15s Sample Edit + 7-Day Plan | **Yes, capped** | Max 10 per week; only for qualified leads (see `01`, Stage 2). |
| 3-Reel Trial (₹2,999) | **Yes** | After payment link, terms and refund policy exist (`04` checklist items P1–P4, L1–L2). Max 2 trials running at once. |
| VanIndra Starter (₹14,999/mo) | **Yes** | Max 2 monthly clients in total until a freelance editor is trained (`02`). |
| VanIndra Pro Growth (₹24,999/mo) | **Yes, max 1** | Only after media-kit template + shoot guide exist. One Pro uses ~83% of current editing capacity. |
| 360° VIP (₹39,999/mo) | **No — not yet** | Publishing access SOP, comment-to-DM tool, brand-representation agreement and a second editor are all missing. Needs ~133–146 team-hours/month (`02`). |
| Brand sponsorship of in-house creators (Vandana Yadav, Smita Yadav) | **Yes, with paperwork** | Media kit, rate card PDF, brand agreement and ASCI disclosure step needed first. |
| D2C UGC Ad Pack (₹19,999 / 3 ads) | **Yes, with brief** | Use a written brief, a usage-rights clause and a 7-working-day timeline (site says 5 days). |
| Comment-to-DM funnels, done-for-you publishing, 5-platform syndication, affiliate auto-DM for clients | **No** | No tool account, no SOP, no tested setup. |
| Client Portal login / live tracking | **No (Mock-only)** | Replace with a per-client Google Sheet tracker until a real portal exists. |

---

## 2. Contact Points & WhatsApp Concierge

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| A1 | "Official WhatsApp Desk: +91 81128 59437 (Smita Yadav)" | `index.html` topbar L1851, header button, hero `#wa-concierge-box` L1936, footer, sticky mobile bar; `login.html`; `pitch-deck.html` | WhatsApp **Business** app on that number with business profile, hours, greeting + away messages, quick replies, labels; a published reply-time promise; linked devices so the team can answer from one number | Smita | **Partly** | The `wa.me/918112859437` links work. No documented business hours, reply SLA, away message or quick replies (pitch-deck slide 7 still asks "What are Smita's official active hours?"). **Fix:** set up per `01` §2 and `04` items A1–A2. |
| A2 | Editable hero message composer ("Edit message below before sending") | `index.html` `#elegantWaMessage` L1945 | Nothing beyond A1 | Smita | **Ready** | — |
| A3 | "Direct WhatsApp Priority Desk with Smita Yadav & Akarsh Yadav"; portal mock tile "WhatsApp Desk — Direct — Smita & Akarsh" | `login.html` L362; `index.html` `#client-portal` L2798 | Akarsh must be reachable *through the official number only* (single-number rule) | Smita, Akarsh | **Partly** | Akarsh has no access to the official number. **Fix:** add Akarsh and Vandana as linked devices on the official WhatsApp Business account and sign messages with their names. |
| A4 | Emails shown: `smitayadav497@gmail.com`, `akarshgkp8756539282@gmail.com` | `index.html` `#our-team` | Monitored inbox, reply SLA, professional signature | Smita, Akarsh | **Partly** | Personal Gmail addresses. **Fix:** commit to a 1-working-day email reply; later move to a studio address on the domain (`04` A5). |
| A5 | "Audio Guide" / "Listen to Founder Audio Overview" / "Listen to Audio Summary" | `index.html` topbar, `#vandana-story`, `#ztOutputPanel` | Browser text-to-speech (`speechSynthesis`, `hi-IN`) | — | **Ready** | Works where the phone has a Hindi voice installed; otherwise falls back to an alert. No backend needed. |
| A6 | English / हिंदी toggle | `index.html` `setLanguageMode()` | — | — | **Ready** | Minor copy bug: Hindi text of the hero reel button says "12 real viral reels" (L2059) while English says 6. |

---

## 3. Free Offers & Lead Capture

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | "we first deliver a **Free 15-Second Sample Re-Edit** of your existing video plus a custom **7-Day Content & Brand Deal Audit** before you pay a rupee" + "24–48h Delivery SLA" | `index.html` Slot #03 L2242, L2255; FAQ 2 L3202; Akarsh card "Request 15s Sample Edit"; AI portal output text | Prospect's video file or Reel link + permission; LLM Prompt #1 (`05_.../02_Master_LLM_Prompt_Pack.md`) ≈ 15 min; Akarsh sample edit 20–30 min; Vandana 5-min check; Smita delivery | Akarsh (edit), Vandana (plan), Smita (send) | **Partly** | Method exists (`04_Outreach_and_Sales_Pipeline/03_Free_Audit_and_Sample_Hook.md`). Missing: weekly cap, qualification filter, permission line, "Brand Deal" part of the audit has no template, no tracker. At ~45 min each, 10 samples/week ≈ 30 h/month — the size of a Starter client. **Fix:** `01` Stage 2 (cap 10/week, 48 working hours). |
| B2 | 9-Step Framework "01 · 7-Day Page Audit — Deep audit of your last 15 posts & retention drop-offs" | `index.html` 9-step section L2831 | Retention drop-offs are only visible in the creator's own Instagram Insights → we need their screenshots | Vandana, Akarsh | **Not ready** | Prompt #1 only uses public observations. **Fix:** ask for 5 Insights screenshots in the intake form (`01` §5.3); or reword to "your last 15 public posts". |
| B3 | "Get Your Free Growth Plan in 5 Seconds!", "100% Automated Voice + Free AI Strategy Desk", "our background AI will instantly generate 3 custom viral Reel scripts and a 7-day roadmap" | `index.html` `#smart-ai-portal` L2850–2852; `runZeroTouchBackgroundAI()` L3445+ | A working AI endpoint, human review before anything is "promised", and lead capture to the team | Akarsh (tech), Smita (follow-up) | **Partly (mock fallback)** | It is real but fragile: it calls the free, keyless `text.pollinations.ai` (no uptime guarantee). If that fails, a **canned template** is shown as if custom (L3504+). The prompt never asks for a 7-day roadmap, so the promised roadmap is not generated. Output is unreviewed (risky for doctor/health niches). **Fix:** reword (see `03`), add the 7-day roadmap to the prompt, label output "AI draft — our team reviews it when you send it on WhatsApp". |
| B4 | Lead capture from the AI form ("Auto-CRM") | `index.html` L3533–3537 (`localStorage 'vanindra_leads_crm'`) | Leads must land in a team-owned sheet | Akarsh (setup), Smita (owner of sheet) | **Mock-only** | Leads are saved **only in the visitor's own browser**. The team receives nothing unless the visitor also taps the WhatsApp button. Name, handle, niche and notes are sent to a third-party AI service without a privacy notice. **Fix:** Google Form or Apps Script → Google Sheet, consent checkbox, privacy policy link (`04` L3, T1). |
| B5 | "Tap to Speak (English / Hindi)" voice input | `index.html` `#btnVoiceMic`, `startHindiVoiceInput()` | Browser speech recognition (Chrome/Android) | — | **Ready** | Not supported on some browsers (iOS Safari varies); fallback alert exists. |
| B6 | "Download Brief (.md)" / "Copy Plan" / "Send to Official WhatsApp Desk" | `index.html` `#ztOutputPanel` | — | — | **Ready** | `.md` is unfamiliar to non-technical users; a `.txt` would open more easily. Minor. |

---

## 4. Packages (`index.html` `#packages`, L3066–3183; `pitch-deck.html` slide 4)

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C1 | **3-Reel Trial Pack ₹2,999 / One-Time:** "7-Day 'What to Post' Strategy Plan · 3 Viral Scripts & 3-Sec Hooks · 3 Studio-Edited High-Retention Reels · Bilingual Captions & 9:16 Reel Covers". Pitch deck adds "Bio & Profile Audit", "WhatsApp Delivery", and Q8 "pehle 7 din" | `index.html` L3125–3128; `pitch-deck.html` slide 4, Q8 | ~14 team-hours incl. free sample (≈8 h Akarsh editing); intake form; payment link; client cover template; terms | Smita (sale), Vandana (plan, scripts, QA), Akarsh (edits, covers) | **Partly** | Delivery skills exist. Missing: payment link, terms, refund policy, intake form, a client-branded cover template (Thumbnail Studio is VanIndra-branded — see H1), a definition of "a Reel" (length, footage). The 7-day promise only works if the client sends footage within 2 days. **Fix:** `01` SLA table; `04` P1–P4, L1–L2, T1–T4. |
| C2 | **VanIndra Starter ₹14,999/month — "3 Reels / Week":** "Full 30-Day Content Calendar · 12 Research-Backed Viral Scripts · 12 High-Retention Studio Edited Reels · Captions, SEO Hashtags & 9:16 Covers". Pitch deck adds "Bio Upgrade + Link Setup", "Client Login + Weekly Sync" | `index.html` L3141–3144; `pitch-deck.html` slide 4 | ~45–49 team-hours/month (≈30 h editing) | Smita, Vandana, Akarsh | **Partly** | Prompt Pack #2–#4 + client template cover strategy, calendar and scripts. Prompt #3 is hard-coded for 20 Reels — adapt it for 12. "Client Login" is mock (E1). **Fix:** use the Google Sheet tracker instead of login; max 2 Starter clients now. |
| C3 | **VanIndra Pro Growth ₹24,999/month — "5 Reels/Wk":** "30-Day Viral Content & Series Calendar · 20 Viral Scripts + Easy Phone Shoot Guide · 20 Studio-Edited Reels + 9:16 Grid Covers · Brand-Ready Bio, Media Kit & Deal Pitching", "supervised by Founder Vandana Yadav". Pitch deck adds "20 Magnific/Studio Covers", "Priority Portal + Founder QA" | `index.html` L3155–3160; `pitch-deck.html` slide 4 | ~79–87 team-hours/month (≈50 h editing); a media-kit template; a shoot guide; a defined pitching scope | Vandana (QA), Smita (bio, media kit, pitching), Akarsh (edits) | **Partly → Not ready for media kit & shoot guide** | No shoot guide exists anywhere in the repo; no media-kit template exists (only mentions in playbooks); "Deal Pitching" has no scope (how many brands, no guarantee). One Pro client consumes ~83% of Akarsh's India editing time. **Fix:** shoot guide is drafted in `01` Stage 7; build media kit (`04` T6); define "up to 20 brand pitches/month, no guarantee of deals". |
| C4 | **VanIndra 360° VIP ₹39,999/month — "Daily Reels":** "100% hands-free daily domination…", "30 Daily Reels (Scripting + Studio Editing) · Done-For-You Publishing & Scheduling · Automated Comment-to-DM Funnel Setup · Dedicated Brand Sponsorship Representation". Pitch deck adds "Shorts Repurpose", "Grid Aesthetic Redesign", "30-Day Multi-Platform Calendar", "VIP Concierge + Auto-Posting" | `index.html` L3171–3176; `pitch-deck.html` slide 3 (tier 4), slide 4 | ~133–146 team-hours/month (≈75 h editing); Meta Business Suite partner access to client's IG/FB; YouTube channel permission; ManyChat (or equal) account on the client's IG; representation agreement + commission terms; 7-day footage buffer | TBD (needs a second editor + coordinator) | **Not ready** | Every VIP-only line is missing a tool, an SOP or capacity. The team cannot staff even one VIP client without a freelancer (`02`). "100% hands-free" is untrue (client still shoots ~30 Reels of raw footage a month). **Fix:** pause VIP sales or change to "Join waitlist"; see `03` C-11. |
| C5 | VIP "Select 360° VIP" button | `index.html` L3179 | Selecting VIP should select VIP | Akarsh | **Bug** | The button calls `selectPackageInForm('VanIndra Pro Growth …')` — it selects **Pro Growth**. VIP is also missing from the AI form dropdown (`#ztPackage` L2900) and the `login.html` plan list. A lead who chose VIP arrives on WhatsApp labelled "Pro Growth". |
| C6 | Prices "₹2,999", "₹14,999 / month" etc. | `index.html` `#packages` | A GST decision: registered or not, inclusive or exclusive | Owner + CA | **Not ready** | No "+ GST" or "incl. GST" anywhere. If we register and prices are GST-inclusive, ~15% of revenue goes to tax. **Fix:** confirm with CA before the first invoice (`04` P5). |
| C7 | Payment & contract terms: "Koi lamba lock-in contract nahi hai. Trial pack (₹2,999) 100% advance UPI/Razorpay … Monthly Retainers mein 50% Onboarding + 50% Mid-Month Milestone" | `pitch-deck.html` slide 5, Q9 (public page) | UPI QR in business name, Razorpay links, written terms | Smita, Owner | **Not ready** | No QR/links exist. The internal rules file (`11_.../03_Client_Login_Data_and_Payment_Gateway_Rules.md`) says the 2nd half is due "Day 15 (after first 10 Reels delivered)", which conflicts with Starter's 12-Reel pace and makes our cash depend on the client's footage timing. **Fix:** date-based second instalment (`01` Stage 4). |

---

## 5. Services Section (`index.html` `#services`, L2635–2722) and 9-Step Framework

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D1 | "Account audit & competitor hook research" | `#services` pillar 1, L2649 | Prompt #1 + manual review of 3–5 competitor pages (≈1 h) | Vandana | **Partly** | No competitor-review template. Add 3 "creators you admire" to the intake form (Prompt #2 already expects it). |
| D2 | "Clear 'What to Post vs. What NOT to Post' filter" | pillar 1 | Prompt #2 + `06_.../01_Onboarding_and_Brand_Voice.md` | Vandana | **Ready** | Template contains family nicknames in fields shared with clients — clean before first use (`04` H1). |
| D3 | "30-Day structured content calendar" | pillar 1; 9-step 03 | Prompt #3 + `02_Monthly_Content_Calendar.md` | Vandana | **Ready** | Prompt #3 produces 20 Reels; adjust count per package (12/20/30). |
| D4 | "Personal brand voice led by Vandana Yadav"; "personally oversees every client's … strategy" | pillar 1; `#our-team` | ~40 min of Vandana's time per Reel (script + QA) | Vandana | **Ready (capacity-limited)** | True only while total load stays under ~45 Reels/month (`02`). |
| D5 | "Word-for-word scripts in Hindi, Hinglish or English"; form option "Regional Dialect / Bilingual (Bhojpuri / Regional Hindi)" | pillar 2 L2662; `#ztLanguage` | Prompt #4 + native proofreading | Vandana | **Ready (EN/Hinglish/Hindi) · Partly (dialects)** | Decide which dialects we truly proofread; list only those. |
| D6 | "Psychological 3-second scroll-stopping hooks" | pillar 2 | Prompt #1/#4 + Vandana's judgement | Vandana | **Ready** | — |
| D7 | "Scientific & fact-checked hooks for Doctors/Health" | pillar 2 L2664 | Fact-check SOP with sources; doctor/client sign-off on every medical statement | Akarsh | **Partly** | No fact-check SOP or source list. Akarsh's B.Voc Food Technology supports food/nutrition topics, not medical advice. **Fix:** `01` §6 QA "health claims" rule; client signs off all medical claims. |
| D8 | "15-minute easy phone shoot guide" (also Pro card "Easy Phone Shoot Guide", 9-step 05) | pillar 2 L2665; L3158; L2834 | A 1-page guide + Hindi voice note | Vandana, Akarsh | **Not ready** | No such document exists. **Fix:** drafted in `01` Stage 7 — turn into a 1-page PDF + voice note. |
| D9 | "Dynamic bilingual captions & B-roll punch-ins", "Sound design, colour grading & pattern interrupts" | pillar 3 L2675–2676 | Editing software licence, licensed SFX/B-roll sources, Hindi caption proofreading | Akarsh | **Partly** | Skill exists. Licences/sources not documented. Note: Instagram **business** accounts (many clinics/shops) have restricted music libraries — use royalty-free music or let creator accounts add trending audio when posting. |
| D10 | "Custom 9:16 Instagram Reel cover thumbnails" | pillar 3 L2677; all package cards | A per-client cover template | Akarsh | **Partly** | `thumbnail-studio.html` works but bakes in the VanIndra crest, "VANINDRA CREATIONS" lockup and our badge — not suitable as a client's cover. **Fix:** one Canva template per client (`04` T5). |
| D11 | "24–48 hour fast turnaround by Akarsh Yadav's editing pod" | pillar 3 L2678; Slot #03 L2255; pitch deck Q10 | Editing hours available when footage arrives | Akarsh | **Partly** | "Pod" = one person today, who also does global lead generation. 48 h holds for the *first Reel* of a batch, not for a 5-Reel batch arriving at once. **Fix:** SLA defined per package in `01` §3 (staggered shoot days). |
| D12 | "Sponsor-ready Instagram bio & highlight covers" | pillar 4 L2688 | Prompt #2 bio options + highlight-cover template | Smita, Akarsh | **Partly** | No highlight-cover template. Canva set needed (`04` T5). |
| D13 | "Professional Creator Media Kit & Rate Card" | pillar 4 L2689; Pro card | Media-kit template fed by the client's Insights (audience, reach, engagement, past brands) | Smita | **Not ready** | No media-kit template exists in the repo. **Fix:** `04` T6. |
| D14 | "Inbound & outbound brand collaboration positioning" | pillar 4 L2690 | Pitch scripts (exist in playbook) + a client representation agreement | Smita | **Partly** | No agreement on who contacts brands on the client's behalf, who invoices, and commission (if any). |
| D15 | "Convert Reel views into WhatsApp customer enquiries" | pillar 5 L2701 | Client's WhatsApp Business link in bio + keyword CTA in scripts + reply templates for the client | Smita | **Not ready** | No SOP. Simple version (no automation): `wa.me` link + "Comment / DM 'PLAN'" CTA — can be delivered once written. |
| D16 | "Automated comment-to-DM keyword funnels"; VIP "Automated Comment-to-DM Funnel Setup" | pillar 5 L2702; L3175 | A Meta-approved automation tool (e.g., ManyChat) connected to the client's IG professional account; flows; testing; monthly monitoring; tool cost (free tier is limited) | Akarsh | **Not ready** | No account, no flow, never tested — not even on our own handles (`11_.../02_Daily_Social_Media…SOP.md` plans it but it isn't live). **Fix:** set up and test on `@vandanay2012` first, then sell. |
| D17 | "Trust-building customer review & showcase Reels" | pillar 5 L2703 | Written consent from the client's customers/patients who appear on camera | Smita | **Partly** | No consent form. For doctors, patient testimonials carry extra professional-conduct rules — client must confirm (see `03`). |
| D18 | "Zero technical knowledge required from you" | pillar 5 | We do all setup | — | **Ready** | Only true if D15/D16 setups are done by us. |
| D19 | "Every video scored against 4 retention rules" | pillar 6 L2714 | A written 4-rule checklist used on every Reel | Vandana, Akarsh | **Not ready** | The 4 rules are not written anywhere (site names only 2). **Fix:** defined in `01` §6. |
| D20 | "Collab-tag flywheel with @vanindracreations" | pillar 6 L2716 | `@vanindracreations` account live; client's written consent to collab-tag | Smita | **Partly** | Account status unknown (SOP says "create today"). Doctors/brands may refuse the tag — make it optional in terms. |
| D21 | "Monthly growth report & strategy review call" | pillar 6 L2717; Smita card "monthly growth reviews"; FAQ 4 | Report template; client Insights access (screenshots or Meta Business Suite partner access); 20–30 min call | Smita (compile), Vandana (insights) | **Not ready** | No report template. **Fix:** outline in `01` Stage 11. Also clarify which packages include the call (site lists it for "everything"). |
| D22 | "Your Only Job: Record raw clips on your phone once a week" / "Every Reel passes a 3-second hook & sponsor-safety check before delivery" | `#client-portal` L2752–2754 | Weekly script pack + shoot guide (D8) + QA checklist (D19) | Vandana, Akarsh | **Partly** | Both depend on D8 and D19. |
| D23 | 9-step 08 "Algorithmic cross-promotion & non-follower reach expansion"; 09 "Convert viral attention into D2C sponsorships & leads" | 9-step L2836–2837 | D14, D15, D20 | Smita | **Partly** | Outcome language — cannot be guaranteed (`03`). |

---

## 6. Client Portal & Tracking (`login.html`, `index.html` `#client-portal`, FAQ 4)

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E1 | "Client Login / Create Account", "Set up your VanIndra Creations portal in 30 seconds" | `login.html` `#loginForm` L384, `#signupForm` L408; header/footer/sticky buttons on `index.html` | Real authentication + a database the team updates | Akarsh | **Mock-only** | `handleLogin()` (L604) **never checks the password** and opens a dashboard for any ID; unknown IDs get a "Pro Growth" dashboard. Sign-ups are stored only in the visitor's browser and never reach the team. Passwords are not even stored. |
| E2 | Dashboard KPIs "85% · 17 of 20 Reels Delivered · 20/20 Scripts Approved · 84.2% Avg 3-Sec Hook Hold · +41% Above Baseline · Brand Deal Media Kit Ready" | `login.html` L466–490; `index.html` portal mock L2771–2799 | Real per-client data | — | **Mock-only** | Every new sign-up sees the **same fake progress** for their own name — a real client could be misled. |
| E3 | "Approve Scripts & Reels in 1 click from your phone"; "aasaan Revision aur Approval button" | `login.html` L359, `approveReel()`; `pitch-deck.html` Q7 | Approval recorded where the team can see it | — | **Mock-only** | Button only changes text on the visitor's screen. |
| E4 | "Submit Raw Video Links directly to your dedicated editing pod" | `login.html` brief form, `submitClientBrief()` | WhatsApp hand-off to official desk | Smita | **Ready** | Opens WhatsApp with the brief — this part genuinely works. |
| E5 | "Zero Black Boxes: Track every script, Reel draft, and monthly growth report live inside your client account"; FAQ 4 "access to your Live Client Portal (`login.html`) where every script, Reel draft, and monthly analytics report is tracked transparently" | `index.html` L2811, L3210 | Same as E1 | Smita, Akarsh | **Mock-only** | **Fix now (₹0):** per-client Google Sheet "Delivery Tracker" + Drive folder, link pinned in the client's WhatsApp group (`01` §8). Relabel the page "Portal preview (demo)" until a real portal exists (`03`). |
| E6 | "Instant Demo Login (Preview Client Dashboard)" with `@vandanay2012` "sample data" | `login.html` L372 | Clear "demo" labelling | — | **Mock-only (labelled)** | Acceptable if the dashboard itself says "Sample data". Today it doesn't once you're inside. |
| E7 | "dedicated WhatsApp Studio Pod with Founder Vandana Yadav, Smita Yadav, and Akarsh Yadav" | `index.html` FAQ 4 L3210 | Client WhatsApp group | Smita | **Partly** | If Vandana's and Akarsh's personal phones join client groups, their numbers become visible to clients — this breaks the single-number rule. **Fix:** create groups from the official number only; team replies via linked devices (`01` Stage 5). |

---

## 7. Brand Sponsorship & Monetization Engine (`index.html` lower `#viral-reels-showcase` block, L2481–2563; `pitch-deck.html` slide 8)

| # | Promise (quoted) | Where | What fulfilment needs | Owner | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F1 | "Brands: Sponsor @vandanay2012 (50K+) & @smitayadav_0901"; "Book Brand Collab on WhatsApp" | `index.html` L2495; `pitch-deck.html` slide 8 | Media kit for each creator (Insights-based), rate-card PDF, brand brief form, brand agreement (deliverables, usage, payment), ASCI disclosure step, invoice, shoot slots in Vandana's week, product-receipt address | Smita (deal), Vandana (on-camera) | **Partly** | WhatsApp CTA works and the rate card exists internally (`03_InHouse_Content_Flywheel/04_…Playbook.md` §4). No media kit, no agreement, no invoice process, no disclosure SOP. |
| F2 | Format 01 "Paid Deal Rate: ₹15,000–₹35,000/Reel" | L2512 | Agreed rate card | Smita, Owner | **Partly** | Conflicts with the hero chip "₹65K/Reel" (L2073) and the internal rate card (₹15,000–₹22,000 for Vandana's dedicated Reel). Ambiguous whether this is our creators' price or what a client will earn. Pick one public rate card. |
| F3 | Format 02 "Comment 'SAREE' for Direct Link — triggers 500+ Explore-boosting comments and 15–25% passive affiliate commissions"; "Wishlink / Hypd / Amazon Storefront Ready" | L2516–2522 | Affiliate accounts approved; comment-to-DM tool live on `@vandanay2012` | Smita, Akarsh | **Not ready** | Registration status unknown; automation not set up (D16). "500+ comments" and "15–25%" are unverified (`03`). |
| F4 | Format 03 dual-generation combo "across 3 accounts — commanding 2x brand sponsorship fees", "Meta Ad Whitelisting" | L2526–2532 | Vandana + Smita shoot together; `@vanindracreations` live; Instagram partnership-ad permission SOP; usage-rights clause | Smita, Vandana | **Partly** | Can be shot today. Whitelisting/partnership-ads permissions not documented; "2x fees" unverified. |
| F5 | Format 04 "Indian Kitchen Food-Tech Truth Bomb … the #1 most forwarded viral format in Indian family WhatsApp groups" | L2536–2542 | Label-reading fact-check with sources; avoid naming/disparaging brands without proof | Akarsh, Vandana | **Partly** | Format is deliverable; the superlative is unverifiable and brand-label content carries disparagement risk (`03`). |
| F6 | Format 05 "3 High-Converting Meta Video Ads in 5 Days … Flat ₹19,999 for 3 Studio UGC Video Ads" (Hindi version adds "doubles the brand's ROAS") | L2546–2552 | Written brief, product shipped to us, 1 shoot day with in-house talent, ~16–18 team-hours, usage-rights term | Smita (brief), Vandana/Smita/Akarsh (talent), Akarsh (edit) | **Partly** | Talent and skills exist. No brief form, no product-logistics step, no usage clause. "5 days" ignores shipping time; Hindi "ROAS doubles" is a performance guarantee. Internal playbook lists the same pack at ₹15,000 (Stream 04) and ₹30,000/₹19,999 (rate card) — prices inconsistent. |
| F7 | Format 06 "Syndicates every Reel across Instagram, Facebook Professional Mode (In-Stream Ad Payouts), YouTube Shorts, and Amazon Influencer Storefronts for 5x revenue" | L2556–2562 | Channel permissions per client, platform eligibility checks, ~10 min per Reel per platform | Akarsh | **Not ready** | Not in any package scope except VIP "Shorts Repurpose" (pitch deck). Monetization depends on each platform's eligibility rules; "5x revenue" unverified. |
| F8 | "Creators: Get These Viral Formats for Your Page" | L2498 | Mapping to a package | Smita | **Partly** | Route to Starter/Pro; formats 02 and 06 cannot be delivered yet. |

---

## 8. Proof Points & Numeric Claims (evidence check)

All of these need a dated screenshot in an "evidence folder" before we keep them. Detailed risk and safer wording: `03_Risky_Claims_and_Fixes.md`.

| # | Claim (quoted) | Where | Evidence in repo? | Readiness |
| :--- | :--- | :--- | :--- | :--- |
| G1 | "84.2% 3-Sec Hook Retention / 3-Sec Hold" ("84%+", "86%+ viewers past the 3-second mark") | `index.html` hero stats L2007, phone dock L2067, founder metrics L2145, vault L2317, portal L2790, JS L2372; `login.html`; pitch deck slide 2 | None (no Insights screenshot, no Reel identified) | **Unverified** |
| G2 | "Before: Raw Clip (4K Views)" vs "After: VanIndra Studio (6.8L Views)" | hero simulator L2028–2029, L2070 | None — no specific Reel named | **Illustrative, presented as real** |
| G3 | "Brand Ready ₹65K/Reel" | phone dock L2073, JS L3606 | None — internal rate card tops out at ₹35,000 | **Unverified / inconsistent** |
| G4 | "0 → 50K+ Live Proven Client Accounts", "LIVE CLIENT PORTFOLIO #01/#02" | hero stats L2011–2012; `#vandana-story` | These are the founder's and a team member's own accounts, not paying clients | **Misleading label** |
| G5 | "@vandanay2012 · 50,000+ Followers · 467+ Posts", "zero paid ads or fake bots" | hero, `#vandana-story`, vault | Public profile (needs dated screenshot); "zero paid ads" needs owner confirmation | **Verifiable** |
| G6 | "100K+ Views" on 4 Vandana Yadav Reels | vault cards | Public view counts (needs dated screenshots) | **Verifiable** |
| G7 | 3 five-star testimonials ("1.4L+ Followers, UP", "1.8L+ Followers, Delhi NCR", "2.1L+ Followers") incl. "our inbound consultation DMs have doubled" | `index.html` `.testimonials-3-col` L2588–2622 | Internal doc `10_Zero_Touch_Automation_Engine/01_…Guide.md` §2 calls them "relatable Indian personas" — i.e., not real clients | **Not genuine — remove** |
| G8 | ROI calculator "Projected Monthly Reach 1.4 Lakh+", "Creator Time Saved 70 Hours/mo", "Estimated Monthly Brand Deal & Business Revenue Potential ₹76,500 – ₹1,41,525 / mo" | `#packages` `.roi-split-card` L3075–3112; `updateROICalc()` | Fixed formulas (reach = followers × 0.48 × Reels/10; revenue = followers/1L × ₹35,000 + Reels × ₹1,200) with no data behind them | **Unsubstantiated projection** |
| G9 | "Just a single brand sponsorship or a handful of inbound client leads easily covers your entire monthly studio retainer" | `#packages` L3071 | None | **Unsubstantiated** |
| G10 | "Scaling 50K to 1M+ Creators" / "Scaling 50K • 100K+ • 200K+ • 500K+ • 1M+ Creators & Brands" | topbar L1845; hero badge | No external clients yet | **Misleading (implies current clients)** |
| G11 | "● 2 New Slots Open" | Slot #03 L2231 | Matches current capacity (`02`) | **OK if kept true** |
| G12 | "80% of trial clients upgrade to ₹14,999 or ₹24,999 within 7 days!" | `pitch-deck.html` slide 4 L578 | No trial clients yet | **Fabricated statistic** |
| G13 | "Hum 80%+ 3-Second Hold Retention … ki 100% guarantee dete hain" | `pitch-deck.html` Q3 L661 | Metric outside our control | **Unsafe guarantee** |
| G14 | "(40%+ reply rate!)", "3.8x Organic Reach", "Smita … Scaled on our 0 → 50K+ trajectory" | `pitch-deck.html` slides 2 & 6 | None | **Unverified** |
| G15 | "Zero — Operations on Your Side"; "100% hands-free"; "Our team handles 100% of your scripts…" | hero stats L2019; VIP L3171; FAQ 1 | Client still shoots and approves | **Overstated** |

---

## 9. Other Public Pages

| # | Promise | Where | Readiness | Gap → Fix |
| :--- | :--- | :--- | :--- | :--- |
| H1 | "Design High-Retention 9:16 Reel Covers in 10 Seconds" → 1080×1920 PNG download | `thumbnail-studio.html` | **Ready (internal tool)** | Works fully in the browser. Brand-locked to VanIndra (crest + lockup), so use it for our own covers, not as a client deliverable. |
| I1 | Pitch deck linked publicly as "📊 Pitch Deck" / "View 100K–1M+ Client Pitch Deck" | `index.html` nav, Slot #03 L2266, footer | **Not ready as a client-facing page** | It is written as internal sales battlecards: "Smita's Pitch Line", "Read these word-for-word", the "Unsolicited Gift" outreach method (downloading a creator's Reel without asking), revenue targets, the fabricated 80% stat. `CLAUDE.md` §3 says internal outreach scripts must not be on public pages. **Fix:** unlink from the public nav or split into a short client deck + an internal deck (`03`). |

---

## 10. Cross-Page Inconsistencies to Resolve Before Selling

| Topic | Versions found | Decide |
| :--- | :--- | :--- |
| 2nd instalment for monthly plans | Pitch deck: "50% Mid-Month Milestone" · internal rules: "Day 15 (after first 10 Reels delivered)" | Date-based (Day 15) or 100% advance — see `01` Stage 4. |
| Brand rate for Vandana Yadav | Hero "₹65K/Reel" · Format 01 "₹15,000–₹35,000" · internal rate card ₹15,000–₹22,000 | One public rate card. |
| UGC Ad Pack | Site "Flat ₹19,999 … in 5 Days" · playbook Stream 04 "₹15,000 for 3 Ad Videos" · rate card ₹30,000 std / ₹19,999 offer | One price, 7 working days after product receipt. |
| VIP inclusions | Site: 4 lines · pitch deck: + Shorts, grid redesign, multi-platform calendar, auto-posting | Publish one inclusion matrix. |
| Free offer name | "7-Day Content Plan", "7-Day Audit", "7-Day Content & Brand Deal Audit", "Free AI Growth Plan" | One name, one deliverable (see `01` Stage 2). |
| Turnaround | "24–48 hour" (services), "24–48h Delivery SLA" (Slot #03), "48-hour first-draft" (pitch deck slide 7, still a question) | Per-package SLA in `01` §3. |
| Revisions | "2 free micro-revisions" (internal rules) · "Revision aur Approval button" (pitch deck Q7) · nothing on index.html | 2 micro-revision rounds per Reel, stated in terms. |
| Number of showcase Reels | English "6", Hindi "12" (L2059) | Fix Hindi copy. |
| "Akarsh Yadav's editing pod" | One editor today | Keep wording only once a second editor is trained. |
