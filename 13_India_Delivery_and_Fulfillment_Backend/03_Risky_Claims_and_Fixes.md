# 03 — Risky Claims & Suggested Fixes

> **What this is:** Claims on our public pages that could mislead a client, are hard to prove, or describe features that are mock-only — with safer wording. These are **recommendations for the owner to approve**; no HTML was changed.
> **Why it matters:** the owner's rule is "we don't take money for something we can't deliver". A client who pays because of a number we can't show, or a portal that doesn't exist, is exactly that risk. One unhappy 100K+ creator can also cost us far more in reputation than the sale was worth.
> **Legal note:** the points below are general, plain-language flags, not legal advice. Please **confirm** with a lawyer / CA before relying on them.

---

## 1. General Rules We Should Follow (India, general — confirm)

| Area | Plain-language rule of thumb | What it means for us |
| :--- | :--- | :--- |
| **ASCI Code (advertising self-regulation)** | Claims must be truthful and backed by evidence; testimonials must be genuine and documented; comparisons and claims about other brands must be fair. | Every number on the site needs a dated proof (§4). Persona testimonials must go. |
| **ASCI influencer guidelines** | Paid/gifted/affiliate content needs a clear upfront disclosure label; people giving health or financial information are expected to state relevant qualifications (confirm the current text). | Built into the QA checklist (`01` §6). Applies to brand deals for our in-house creators and to clients' sponsored Reels. |
| **Consumer Protection Act 2019 + CCPA guidelines on misleading advertisements & endorsements (2022)** | Ads must not mislead; endorsements should reflect genuine, current experience; guarantees must be honoured. | Avoid guarantees on views/retention/revenue; don't present illustrations as real results. |
| **CCPA guidelines on dark patterns (2023)** | "False urgency" (fake scarcity/countdowns) is listed as a dark pattern. | "2 New Slots Open" is fine only while it is literally true. |
| **Digital Personal Data Protection Act 2023 (and its Rules)** | Collecting personal data (name, phone, email) needs a clear notice of purpose, consent, and a way to withdraw/delete. | Website forms, the AI generator and the login page collect personal data with no privacy notice. |
| **Health content** | Health claims need evidence; doctors have their own professional rules on self-promotion and patient testimonials. | Doctor/clinic clients must approve every health claim and patient appearance in writing (`01` Stage 6, `04` L7). |
| **Copyright / consent** | Re-using someone else's video needs their permission. | Free samples only on videos the creator sends us (`01` T-04). |

---

## 2. Claims to Fix — by Severity

**Severity:** **High** = fix before taking any paid client · **Medium** = fix within 30 days · **Low** = tidy-up.

### 2.1 High

| # | Claim (quoted) | Where | Why it's risky | Suggested safer wording |
| :--- | :--- | :--- | :--- | :--- |
| R1 | Three ★★★★★ testimonials: "I had 1.4L followers … Vandana Ma'am and Akarsh's editing pod turn them into high-retention Reels" — "Regional Creator & Vlogger (1.4L+ Followers, UP)"; "our inbound consultation DMs have doubled" — "Health & Nutrition Specialist (1.8L+ Followers, Delhi NCR)"; "we started closing paid retainers monthly" — "Fashion & Lifestyle Creator (2.1L+ Followers)" | `index.html` `.testimonials-3-col` L2588–2622 | Our own internal doc (`10_Zero_Touch_Automation_Engine/01_Free_APIs_and_Zero_Work_Automation_Guide.md` §2) describes these as "relatable Indian personas" — they are not real clients. Fabricated testimonials are the clearest misleading-advertising risk and destroy trust if a prospect asks to speak to them. | **Remove the section now.** Replace with: *"Our first client stories will appear here — with their permission — as they complete their trials. Until then, judge us by our live in-house accounts and a free 15-second sample of your own video."* When real: full name or handle (with written consent), date, and a screenshot-backed result. |
| R2 | "84.2%" 3-Sec Hook Retention / 3-Sec Hold; "84%+ 3-Sec Hold"; "+41% Lift"; "holds 86%+ viewers past the 3-second mark" | `index.html` hero stats L2007, phone KPI dock L2067, founder metrics L2145, vault L2317, portal mock L2790–2791, reel note L2372; `login.html`; `pitch-deck.html` slide 2 | No screenshot or named Reel in the repo backs it. Presented as a general studio result. | Keep only with proof: *"84% of viewers watched past 3 seconds on 'Ye 5 mins kaam karte hi…' (Instagram Insights, [Month Year])."* Otherwise remove the percentage and say *"Hook-first editing designed to stop the scroll in the first 3 seconds."* |
| R3 | Hero simulator "Before: Raw Clip (4K Views)" / "After: VanIndra Studio (6.8L Views)", "6.8L+ Views", "68% viewers swiped away", "21.4%" | `index.html` `.sim-toggle-pill` L2028–2029, `#chipViews` L2070, `switchPhoneSimulation()` | No real Reel is named; it reads as a real before/after client result. | Add a visible label: *"Illustration — not a client result."* Or use one real Reel with its real numbers and date. |
| R4 | "💰 Brand Ready ₹65K/Reel" | `index.html` `#chipSponsor` L2073, JS L3606 | No basis — our own internal rate card tops out at ₹35,000 (combo Reel). Implies clients will earn ₹65K per Reel. | Remove the amount: *"💰 Brand-ready profile"*. |
| R5 | ROI calculator: "Estimated Monthly Brand Deal & Business Revenue Potential ₹76,500 – ₹1,41,525 / mo"; "Projected Monthly Reach 1.4 Lakh+"; "Creator Time Saved 70 Hours/mo — 100% editing handled by our pod" | `index.html` `.roi-split-card` L3075–3112, `updateROICalc()` | Fixed formulas with no data (revenue = followers ÷ 1 lakh × ₹35,000 + Reels × ₹1,200). An earnings projection on a sales page is easy to read as a promise. | Remove the revenue output, or label the whole widget: *"Illustrative only. Real results depend on your niche, audience, consistency and brand demand — we don't promise reach or income."* Rename "Time Saved" to *"Editing time you hand over to us (approx.)"*. |
| R6 | Client portal: "Track every script, Reel draft, and monthly growth report live inside your client account"; FAQ 4 "access to your Live Client Portal (`login.html`) where every script, Reel draft, and monthly analytics report is tracked transparently"; "Client Login / Create Account"; dashboard "85% · 17 of 20 Reels Delivered · 84.2%" | `index.html` `#client-portal` L2811, FAQ L3210, header/footer/sticky buttons; `login.html` | **Mock-only.** Any ID logs in, passwords are ignored, sign-ups never reach us, and every new account sees the same fake progress for their own name. A paying client would discover this on day one. | Header button: *"Client Portal (preview)"*. Login page banner: *"Preview only. Paying clients get a private tracker (shared Google Sheet) and a WhatsApp group on day one."* FAQ 4: *"You get a private WhatsApp group with our official studio desk and a shared tracker where every script, Reel draft and monthly report is listed."* Remove the sign-up form until a real backend exists. |
| R7 | AI form collects name, handle, WhatsApp number and goals; sends name/handle/niche/notes to a third-party AI service; stores leads in the browser as "Auto-CRM" | `index.html` `#zeroTouchForm`, L3492, L3533–3537; `login.html` sign-up | Personal data collected with no privacy notice or consent; leads don't reach us at all (lost sales). | Under the button: *"We use a third-party AI service to draft your plan — please don't enter sensitive personal information. By continuing you agree to our [Privacy Policy]."* + consent checkbox; send leads to a team Google Sheet (`04` W3). |
| R8 | VIP "100% hands-free daily domination", "Done-For-You Publishing & Scheduling", "Automated Comment-to-DM Funnel Setup", "Dedicated Brand Sponsorship Representation" | `index.html` VIP card L3171–3176 | Not deliverable today (`00` C4, `02`). The client still records ~30 Reels of footage a month, so "100% hands-free" is untrue. | Change the button to *"Join the VIP waitlist"* and add *"Opening [month] — limited to 1 client."* When live: *"Daily Reels with done-for-you scheduling — you record about 1 hour a week, we handle scripting, editing and posting."* |
| R9 | Hindi copy of Format 05: "जो ब्रांड का ROAS दोगुना करती हैं" ("doubles the brand's ROAS"); English "3 High-Converting Meta Video Ads" | `index.html` L2546–2549 | A performance guarantee to brands that we cannot control (and only visible in Hindi mode). | EN: *"3 ad-ready video variations with 3 different hooks, so you can test what converts."* HI: *"3 अलग-अलग हुक वाले 3 ऐड वीडियो — ताकि आप टेस्ट कर सकें कि क्या सबसे अच्छा चलता है।"* |
| R10 | Pitch deck: "80% of trial clients upgrade to ₹14,999 or ₹24,999 within 7 days!" and Q3 "Hum 80%+ 3-Second Hold Retention … ki 100% guarantee dete hain" | `pitch-deck.html` slide 4 L578, slide 5 Q3 L661 (publicly linked) | We have no trial clients yet; a retention guarantee depends on the creator's delivery, topic and the algorithm. | Remove the 80% line. Q3 answer: *"Hum views ya followers ki guarantee nahi dete — koi imaandar agency nahi de sakti. Hum guarantee dete hain deliverables aur deadlines ki: har Reel 4 retention rules pass karegi aur time par milegi."* |

### 2.2 Medium

| # | Claim (quoted) | Where | Why it's risky | Suggested safer wording |
| :--- | :--- | :--- | :--- | :--- |
| R11 | "LIVE CLIENT PORTFOLIO #01 / #02"; "0 → 50K+ Live Proven Client Accounts"; topbar "Live Client Portfolios @vandanay2012 & @smitayadav_0901" | `index.html` hero stats L2011–2012, `#vandana-story` cards, topbar L1841–1845; pitch deck slide 2 | These are the founder's and a team member's own accounts, not paying clients. Calling them "clients" overstates our track record. | *"Our in-house creator accounts"* · *"In-house Portfolio #01 — Founder Vandana Yadav"* · hero stat: *"50K+ — Founder's organic Instagram community (as of [Month Year])"*. |
| R12 | "Scaling 50K to 1M+ Creators" / "Scaling 50K • 100K+ • 200K+ • 500K+ • 1M+ Creators & Brands" | topbar L1845, hero badge | Implies we currently work with 1M+ creators. | *"Built for 50K to 1M+ creators & brands."* |
| R13 | "Just a single brand sponsorship or a handful of inbound client leads easily covers your entire monthly studio retainer." | `index.html` `#packages` L3071 | Unsupported earnings promise. | *"For many creators, one paid collaboration a month can offset the cost — but results vary and we don't guarantee deals."* |
| R14 | "Zero — Operations on Your Side"; FAQ 1 "Our team handles 100% of your scripts…"; "Your Only Job: Record raw clips … once a week" | hero stats L2019; FAQ L3198; `#client-portal` L2752 | The client still records, uploads and approves. | *"Minimal effort on your side — about 30–60 minutes a week to record. We handle scripts, editing, captions and covers."* |
| R15 | "Get Your Free Growth Plan in 5 Seconds!", "100% Automated", "instantly generate 3 custom viral Reel scripts and a 7-day roadmap" | `#smart-ai-portal` L2850–2852 | The free API can be slow or down; on failure a canned template is shown as if custom; the prompt doesn't generate a 7-day roadmap. | *"Get a free AI-drafted starter plan in about a minute. Send it to us on WhatsApp and our team will review it with you."* (and add the 7-day roadmap to the prompt). |
| R16 | "24–48 hour fast turnaround by Akarsh Yadav's editing pod"; "24–48h Delivery SLA" | `#services` L2678; Slot #03 L2255 | One editor today; a 5-Reel batch cannot all arrive in 48 h. "Pod" implies a team. | *"First edit within 48 working hours of receiving your footage; full weekly batch in 3–4 working days. Edited by Akarsh Yadav."* (Say "editing team" once a second editor is trained.) |
| R17 | Services pillar 5: "Automated comment-to-DM keyword funnels" and Format 02 "Comment 'SAREE' … triggers 500+ Explore-boosting comments and 15–25% passive affiliate commissions … Wishlink / Hypd / Amazon Storefront Ready" | `#services` L2702; L2516–2522 | Not set up or tested even on our own accounts; numbers unverified; commission rates vary by platform/brand. | Pillar 5: *"Comment-to-DM keyword funnels (coming soon)"* until tested. Format 02: *"Comment-keyword lookbooks that drive comments and affiliate link clicks (commission rates vary by platform and brand)."* |
| R18 | "commanding 2x brand sponsorship fees"; "for 5x revenue"; "the #1 most forwarded viral format in Indian family WhatsApp groups"; "Hooks 100K+ viewers in the first 4 seconds"; "Paid Deal Rate: ₹15,000–₹35,000/Reel" | `index.html` L2510–2562 | Unverifiable superlatives and multipliers; the rate range is ambiguous (our creators' price vs. what a client will earn). | *"Combo Reels across multiple accounts can command a higher fee"* · *"Repurpose one Reel across platforms (subject to each platform's eligibility rules)"* · *"A highly shareable format with Indian family audiences"* · *"Opens with a relatable comedy hook in the first 3–4 seconds"* · move rates into one *"Brand rate card for our in-house creators — on request"*. |
| R19 | Format 04 "expose everyday grocery & nutrition labels" | `index.html` L2536–2542 | Naming and criticising brands can raise disparagement complaints if any claim is wrong. | Keep the format but add an internal rule: read the label on camera, cite the source for any health statement, no insulting language, legal check before naming a brand. Public copy: *"Explain everyday food labels in simple Hindi — fact-checked."* |
| R20 | Pitch deck is publicly linked (nav "📊 Pitch Deck", Slot #03 button, footer) but contains internal battlecards: "Smita's Pitch Line", "Read these word-for-word", "(40%+ reply rate!)", "3.8x Organic Reach", the "Unsolicited Gift" method ("Download 1 recent low-view Reel from a 100K–500K creator. Akarsh re-edits …") | `pitch-deck.html` slides 2–8 | Prospects can read our sales psychology; unverified stats; re-editing someone's Reel without asking raises consent/copyright and platform-terms issues; `CLAUDE.md` §3 says internal outreach scripts must not be on public pages. | Remove the public links or split into (a) a short client deck — who we are, packages, process, FAQ — and (b) an internal deck kept out of the published site. Change the outreach method to *"re-edit only with the creator's permission"*. |
| R21 | Prices shown with no GST mention | `index.html` `#packages`; AI form; `login.html` | If we must charge GST later, clients may feel misled; if inclusive, margins collapse (`02` §6.2). | After CA confirmation: *"Prices exclusive of GST, if applicable."* |
| R22 | "Professional Creator Media Kit & Rate Card", "Brand-Ready Bio, Media Kit & Deal Pitching", "Inbound & outbound brand collaboration positioning" | `#services` L2688–2690; Pro card L3160 | Media kit template doesn't exist; pitching scope is open-ended and could be read as a promise of deals. | *"Media kit and rate card, plus up to 20 brand pitches a month on your behalf (we don't guarantee deals)."* |

### 2.3 Low

| # | Claim (quoted) | Where | Why it's risky | Suggested safer wording |
| :--- | :--- | :--- | :--- | :--- |
| R23 | "Scaled from 0 to 50,000+ organic followers across 467+ tested posts with zero paid ads"; "Built across 467+ tested posts with zero paid ads or fake bots" | `#vandana-story` L2140, vault L2314 | Fine if true — but follower counts change and "zero paid ads" needs owner confirmation. | Add a date: *"50,000+ followers (Oct 2026)"*; keep "zero paid ads" only if confirmed. |
| R24 | "🔥 100K+ Views" badges on 4 Reels | vault cards | Verifiable, but needs a dated screenshot in case a client asks. | Keep; store proof (§4). |
| R25 | "● 2 New Slots Open" | Slot #03 L2231 | Matches real capacity today (`02` §4.2). Becomes "false urgency" if left up when we are full or if it never changes. | Update monthly: *"[n] slots open for [Month]"* or *"Waitlist open"*. |
| R26 | FAQ 3 "Every view, share, follower, and brand inquiry is generated organically…" | `index.html` L3206 | Sound policy, but reads as a result promise. | *"We never buy followers, bots or engagement. Growth comes from your content, hooks and collaborations — we can't promise specific numbers."* |
| R27 | "Every video scored against 4 retention rules" | `#services` L2714 | True only once the checklist is in use. | Keep after adopting `01` §6. |
| R28 | Hindi hero button "वंदना की 12 असली वायरल रील्स देखें" vs. English "6 Flagship Viral Reels" | `index.html` L2059 | Inconsistent claim between languages. | Hindi: *"▶ वंदना की 6 चुनिंदा वायरल रील्स देखें ↓"*. |
| R29 | "Personally oversees every client's 'What to Post vs. What NOT to Post' strategy" (Vandana Yadav) | `index.html` `#our-team` L2966 | True at today's scale; not at 80+ Reels/month (`02` §5.4). | Keep; revisit when adding a script assistant. |

---

## 3. Features That Are Mock-Only (summary)

| Feature on the site | What actually happens | Minimum honest fix |
| :--- | :--- | :--- |
| Client Login / Create Account (`login.html`) | Any ID works, password ignored, data stays in the visitor's browser | Label "preview"; real tracker via Google Sheet; remove sign-up |
| Dashboard numbers (85%, 17/20, 84.2%, +41%) | Same hard-coded numbers for everyone | Label "Sample data" inside the dashboard |
| 1-click Approve buttons | Change text on screen only | Approvals by WhatsApp reply / tracker comment |
| "Auto-CRM" for AI-form leads | Saved only in the visitor's browser | Google Sheet capture + consent |
| AI plan "in 5 seconds" | Free third-party API; canned fallback on failure | Reword (R15), add roadmap to prompt, review by team |

---

## 4. Evidence Locker (for claims we keep)

Create a Drive folder `Evidence_Public_Claims/` (internal). For each claim we keep, store a dated screenshot and the page section it supports. Review every quarter and before any website update.

| Claim | Evidence needed | Owner |
| :--- | :--- | :--- |
| @vandanay2012 follower and post count | Profile screenshot with date | Vandana |
| 4 Reels "100K+ views" | Screenshot of each Reel's view count with date | Vandana |
| Any 3-second / retention figure | Instagram Insights screenshot for the named Reel (skip-rate or equivalent data where shown) | Vandana |
| "Zero paid ads" | Owner confirmation + Meta ads history check | Vandana / Owner |
| Any client result or testimonial | Written consent + screenshot + date | Smita |
| Brand rate card figures | Past paid deal invoices or agreed rate card | Smita |
