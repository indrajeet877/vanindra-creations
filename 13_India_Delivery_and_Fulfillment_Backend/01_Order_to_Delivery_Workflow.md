# 01 — Order-to-Delivery Workflow (India Clients)

> **What this is:** The end-to-end path from a stranger's first WhatsApp message to a renewed monthly client — who does what, how fast, with copy-paste messages in **English** and **Roman Hinglish**.
> **Built from:** the public promises in `00_Promise_to_Delivery_Map.md`, the prompt pipeline in `05_Content_Factory_and_LLM_Prompts/`, the client folder in `06_Client_Workspace_Template/`, and the payment notes in `11_Magnific_AI_and_Social_Automation/03_Client_Login_Data_and_Payment_Gateway_Rules.md`.
> **Status:** Draft operating procedure for owner approval. Anything marked **(confirm)** needs an owner, CA or lawyer decision before use.

---

## 0. Golden Rules for Every Client-Facing Message, File and Form

1. Use official full names only: **Vandana Yadav**, **Smita Yadav**, **Akarsh Yadav**. Never family nicknames.
2. Only these three people appear in anything a client sees. No other team member is named.
3. Only one WhatsApp number is ever shown or used with clients: **+91 81128 59437** (official desk, Smita Yadav).
4. Client WhatsApp groups are created **from the official number**. Vandana Yadav and Akarsh Yadav reply as **linked devices on the official WhatsApp Business account**, signing their name — their personal numbers never join client groups.
5. Never promise views, followers, deals or a retention percentage. Promise **deliverables and deadlines** only.
6. Before sending any template, replace every `[bracket]`. Read it once on a phone screen.

**Standard sign-offs**
- Smita: `— Smita Yadav, VanIndra Creations · WhatsApp +91 81128 59437`
- Akarsh (via official desk): `— Akarsh Yadav, Editing Lead · VanIndra Creations`
- Vandana (via official desk): `— Vandana Yadav, Founder · VanIndra Creations`

---

## 1. Flow at a Glance

```
[1] First WhatsApp message ──► [2] Free 15s sample + 1-page plan (qualified leads, max 10/week)
                                        │
                                        ▼
[3] 15-min discovery call ──► CAPACITY CHECK (capacity board) ──► no room? → waitlist / later start date
                                        │ room
                                        ▼
[4] Written proposal ──► payment (UPI / Razorpay / bank) ──► receipt / invoice
                                        │
                                        ▼
[5] Onboarding: WhatsApp group (official number) + Drive folder + intake form + tracker sheet
                                        │
                                        ▼
[6] Brand bible + calendar + weekly script pack ──► client approves (24 h)
                                        │
                                        ▼
[7] Shoot guide ──► client records (15–30 min) ──► uploads to Drive
                                        │
                                        ▼
[8] Edit (first cut ≤ 48 working hours) ──► [QA: 4 retention rules + safety]
                                        │
                                        ▼
[9] Client review ──► up to 2 micro-revision rounds ──► approved
                                        │
                                        ▼
[10] Final files + posting kit (or scheduled publishing for VIP, when enabled)
                                        │
                                        ▼
[11] Monthly report + review call ──► [12] Renewal / upgrade / pause / exit
```

---

## 2. Who Does What (RACI-lite)

| Stage | Does the work | Approves / QA | Tool / file | Output |
| :--- | :--- | :--- | :--- | :--- |
| 1 First contact | Smita | — | WhatsApp Business (labels, quick replies) | Lead logged in Lead Sheet |
| 2 Free sample + plan | Akarsh (15s edit), Vandana (plan via Prompt #1) | Vandana | Prompt #1, editing app, `04_Outreach_and_Sales_Pipeline/Prospect_Audits/` | Sample MP4 + 1-page plan |
| 3 Discovery call | Smita (lead), Vandana (joins Pro/VIP calls) | — | Google Meet / WhatsApp call, Capacity Board | Agreed package + start date |
| 4 Proposal + payment | Smita | Owner (non-standard deals) | Proposal template, UPI QR / Razorpay link | Payment logged, receipt sent |
| 5 Onboarding | Smita | — | Drive template, intake Google Form, Delivery Tracker | Group, folder, form, tracker live |
| 6 Strategy + scripts | Vandana (Prompts #2–#4 + rewrite), Akarsh (health/food fact-check) | Vandana | `06_Client_Workspace_Template/` files | Brand bible, calendar, weekly script pack |
| 7 Shoot guide | Smita sends | — | Shoot guide (Stage 7 below) | Raw footage in Drive |
| 8 Edit | Akarsh (later + freelancers) | Vandana (QA) | Editing app, cover template, QA checklist §6 | First cut + cover |
| 9 Review / revisions | Akarsh | Client | Tracker, WhatsApp | Approved Reel |
| 10 Delivery / publishing | Smita (posting kit); VIP publishing owner **TBD** | Vandana | Drive `06_Final…`, Meta Business Suite (VIP only) | Final files / scheduled post |
| 11 Monthly report | Smita (compile), Vandana (insights) | Vandana | Report template (Stage 11) | 1-page report + call |
| 12 Renewal | Smita | Owner (discounts) | Payment log | Renewed / paused / closed |

---

## 3. Service Levels by Package

**Working hours (confirm):** Monday–Saturday, 10:00 AM – 7:00 PM IST, excluding national holidays. "Working day" (wd) and "working hours" (wh) count only these.
**Footage clock:** editing deadlines start when *complete, usable* footage for that Reel is in the Drive folder.
**Batch rule:** shoot days are staggered between clients (e.g., Client A footage Monday, Client B Thursday) so one editor can hold the 48-hour first-cut promise.

| Step | Free sample | 3-Reel Trial ₹2,999 | Starter ₹14,999 | Pro Growth ₹24,999 | 360° VIP ₹39,999 (paused — see `00`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| First WhatsApp reply | ≤ 3 wh | ≤ 3 wh | ≤ 3 wh | ≤ 2 wh | ≤ 1 wh |
| Discovery call offered | within 2 wd | within 2 wd | within 2 wd | within 2 wd | within 1 wd |
| Kick-off after payment (group + Drive + form) | — | same wd if paid by 4 PM | same | same | same |
| Strategy document | 1-page plan with sample | 7-day plan ≤ 2 wd after intake form | Brand bible + 30-day calendar ≤ 3 wd after intake | ≤ 3 wd | ≤ 4 wd |
| Script packs | 3 hook ideas | 3 scripts with the plan | 3 scripts/week, sent Friday for next week | 5 scripts/week, sent Friday | 7 scripts/week, sent Thursday |
| Client approval window | — | 24 h | 24 h | 24 h | 24 h |
| First cut | 15s sample ≤ 2 wd after we get the video | 1st Reel ≤ 48 wh; all 3 ≤ 3 wd | 1st Reel ≤ 48 wh; weekly batch (3) ≤ 3 wd | 1st Reel ≤ 48 wh; weekly batch (5) ≤ 4 wd | 1 Reel/day from a 7-Reel footage buffer |
| Revisions | 1 small change | 2 micro rounds per Reel, ≤ 1 wd each | same | same | same |
| Final files | — | ≤ 1 wd after approval | same | same | scheduled per calendar |
| Reporting | — | Wrap-up note ≤ 2 wd after last Reel | Monthly report by wd 3 + 20-min call | Report + 30-min call | Report + 30-min call + weekly snapshot |
| Brand work | — | — | Bio upgrade + link setup (once) | Brand-ready bio + media kit (once) + up to 20 brand pitches/month, no guarantee of deals | Representation (scope + commission to be defined) |

**Micro-revision** = text/caption change, hook banner wording, music/voice level, trim or reorder existing shots, cover text. **Not a revision** (= a new Reel): new footage, new concept, a different script, a full style change.

**Website wording to match this (recommendation):** "First edit within 48 working hours of receiving your footage; full weekly batch within 3–4 working days."

---

## 4. Stage-by-Stage Detail and Message Templates

Templates are numbered T-01 to T-28. Each has an English and a Roman Hinglish version — send the one the client writes in.

### Stage 1 — First WhatsApp Message

**Setup (once, Smita):** WhatsApp Business on +91 81128 59437 → business profile (name *VanIndra Creations*, category, hours, website, email), greeting message, away message, quick replies (`/hi`, `/sample`, `/plans`, `/pay`, `/welcome` …), labels: `New lead` · `Qualified` · `Sample sent` · `Call booked` · `Proposal sent` · `Paid` · `Active client` · `Renewal due` · `Brand enquiry` · `Not a fit`. Add Vandana Yadav and Akarsh Yadav as linked devices.

**Log every lead** in the Lead Sheet (columns in §8) the same day, even if they came from the website AI form (the form does not save leads for us today — see `00` B4).

**T-01 Greeting (automatic)**
- EN: *Hello! Thank you for reaching VanIndra Creations. I'm Smita Yadav from the studio team. To help you quickly, please share: 1) your Instagram handle, 2) follower count, 3) your niche or business, 4) what you need most — scripts, editing, brand deals or customer enquiries. We reply within 3 working hours (Mon–Sat, 10 AM–7 PM).*
- Hinglish: *Namaste! VanIndra Creations se judne ke liye dhanyavaad. Main Smita Yadav, studio team se. Jaldi madad ke liye please bhejiye: 1) Instagram handle, 2) followers, 3) aapka niche ya business, 4) sabse zyada kis cheez ki zarurat hai — scripts, editing, brand deals ya customer enquiries. Hum Mon–Sat, 10 AM–7 PM mein 3 working ghante ke andar reply karte hain.*

**T-02 Away message (automatic, outside hours)**
- EN: *Thanks for your message! Our studio desk is closed right now (hours: Mon–Sat, 10 AM–7 PM). We'll reply by 11 AM on the next working day. — VanIndra Creations*
- Hinglish: *Message ke liye shukriya! Abhi studio desk band hai (Mon–Sat, 10 AM–7 PM). Hum agle working day 11 AM tak reply kar denge. — VanIndra Creations*

**T-03 Qualification + plans overview (manual, `/plans`)**
- EN: *Thank you, [Name]! Here's how we work: we write your scripts and hooks, you record raw clips on your phone (about 15–30 minutes a week), and we edit, add captions and covers. Plans: 3-Reel Trial ₹2,999 (one-time) · Starter ₹14,999/month (12 Reels) · Pro Growth ₹24,999/month (20 Reels + bio, media kit and brand pitching). Prices [are exclusive of GST / include GST — confirm]. Before you decide, we can make a free 15-second sample edit of one of your videos. Shall we?*
- Hinglish: *Shukriya [Name] ji! Hamara tareeka simple hai: scripts aur hooks hum likhte hain, aap phone par raw clips record karte hain (hafte mein lagbhag 15–30 minute), aur editing, captions aur covers hum karte hain. Plans: 3-Reel Trial ₹2,999 (ek baar) · Starter ₹14,999/mahina (12 Reels) · Pro Growth ₹24,999/mahina (20 Reels + bio, media kit aur brand pitching). Prices [GST alag / GST shamil — confirm]. Decide karne se pehle hum aapke ek video ka free 15-second sample edit bana sakte hain. Bhejein?*

---

### Stage 2 — Free 15s Sample + 1-Page Plan

**Who qualifies (to protect editing time):** Instagram creators/businesses with roughly 50K+ followers *or* a clinic/coaching/business with a real budget; clear interest in Trial/Starter/Pro; we have done fewer than 10 samples this week (fewer than 5 once 2 monthly clients are active — see `02` A6). Others get T-06 (polite plans + waitlist).

**Steps**
1. Smita sends T-04 and logs the lead as `Qualified`.
2. Client sends one video (original file, or as WhatsApp **Document** to avoid compression) + their handle.
3. Vandana runs Prompt #1 (`05_Content_Factory_and_LLM_Prompts/02_Master_LLM_Prompt_Pack.md`), rewrites it in our voice, saves to `04_Outreach_and_Sales_Pipeline/Prospect_Audits/Audit_[@handle].md` (≈15 min).
4. Akarsh edits the first 15 seconds (≈20–30 min): hook banner, captions, 1–2 B-roll/zoom cuts, SFX. Small "Sample — VanIndra Creations" mark in a corner.
5. Vandana 5-minute check → Smita sends T-05 within 2 working days. Label `Sample sent`.
6. No reply in 3 days → one follow-up; no reply in 7 days → close as `Lost`.

**T-04 Sample request (with permission)**
- EN: *Great! Please send one recent video you'd like improved — the original file, or attach it as a "Document" on WhatsApp so the quality stays sharp. By sending it, you allow us to re-edit 15 seconds as a private sample for you only. We won't post it anywhere without your written OK. You'll get it within 2 working days.*
- Hinglish: *Badhiya! Apna ek recent video bhejiye jise aap better dekhna chahte hain — original file, ya WhatsApp par "Document" ki tarah attach karein taaki quality kharab na ho. Video bhejkar aap humein uske 15 second ka private sample edit banane ki permission dete hain — sirf aapke liye. Aapki likhit permission ke bina hum ise kahin post nahi karenge. 2 working days mein mil jaayega.*

**T-05 Sample + plan delivery**
- EN: *[Name], here's your free 15-second sample and a 1-page plan for @[handle]: [Drive link]. The plan covers what to post vs. what to stop, and 3 hook ideas for your niche. If you like the direction, let's do a 15-minute call to choose a plan — does [Day, Time] or [Day, Time] work?*
- Hinglish: *[Name] ji, ye raha aapka free 15-second sample aur @[handle] ke liye 1-page plan: [Drive link]. Isme kya post karein vs. kya band karein, aur aapke niche ke 3 hook ideas hain. Agar direction pasand aaye, toh 15 minute ki call karte hain plan choose karne ke liye — [Day, Time] ya [Day, Time] theek rahega?*

**T-06 Not a fit right now / capacity full (honest)**
- EN: *Thank you so much, [Name]. We keep only a few clients at a time so every Reel gets proper attention, and our slots for [month] are full. I've added you to the waitlist for [date]. If you'd like, you can start with the 3-Reel Trial on that date.*
- Hinglish: *Bahut shukriya [Name] ji. Hum ek time par kam clients lete hain taaki har Reel par poora dhyaan de sakein, aur [month] ke slots full hain. Maine aapko [date] ki waitlist mein add kar diya hai. Chahein toh us date se 3-Reel Trial se shuru kar sakte hain.*

---

### Stage 3 — Discovery Call (15 minutes)

**Before the call (Smita, 5 min):** open the Lead Sheet row, the sample, and the **Capacity Board** (§8). Write down the earliest start date we can honestly meet.

**Agenda**
1. (2 min) Their goal in one sentence; followers, average views, who shoots.
2. (4 min) Walk through the sample: what changed and why.
3. (4 min) How it works week by week: script pack Friday → they shoot → first cut in 48 working hours → 2 small revision rounds → final files.
4. (3 min) Recommend one plan. Say clearly what is **not** included and that we don't guarantee views, followers or deals.
5. (2 min) Agree start date (from the Capacity Board) and payment method. Send T-08 within 2 working hours.

**Capacity gate (non-negotiable):** if committed editing for the start month + this client exceeds ~45 hours on the Capacity Board (75% of current capacity, see `02`), offer a later start date. **We never take payment for a start date we cannot meet.**

**T-07 Call confirmation**
- EN: *Confirmed: 15-minute call on [Day, Date] at [Time] on [Google Meet link / WhatsApp call]. Smita Yadav from VanIndra Creations will call you.*
- Hinglish: *Confirm: [Day, Date] ko [Time] par 15 minute ki call, [Google Meet link / WhatsApp call] par. VanIndra Creations se Smita Yadav aapko call karengi.*

---

### Stage 4 — Proposal → Payment → Receipt

**Payment methods (Smita):**
1. **UPI QR / UPI ID in the business name** — no fee. A current account in the business's name is recommended so clients see "VanIndra Creations", not a personal name (confirm with bank/CA).
2. **Razorpay Payment Link** — cards, UPI, net banking; transaction fee applies (roughly 2% — check current pricing). Activation needs KYC and policy pages on the website (terms, privacy, refund, contact).
3. **Bank transfer (NEFT/IMPS)** — share account details only after the client confirms the proposal.

**Payment terms (recommendation, owner to confirm):**
- Trial ₹2,999: 100% before work starts.
- Monthly plans: **Option A (recommended for the first 5 clients):** 100% in advance per 30-day cycle. **Option B:** 50% before kick-off + 50% on **Day 15 of the cycle** — tied to the date, *not* to "10 Reels delivered", because delivery depends on the client's footage.
- No production (beyond the free sample) before the first payment clears.

**GST (confirm with CA before the first invoice):** whether to register now, whether prices are shown inclusive or exclusive of GST, the right service code, and how to handle TDS if a business client deducts it. Until registered, do not show GST on receipts.

**Refunds (draft — owner + lawyer to confirm, then publish as a policy):**
- Trial: full refund if requested before we send the 7-day plan; after that, refund for any of the 3 Reels we fail to deliver within 14 days of receiving usable footage.
- Monthly: any Reel we cannot deliver because of **our** capacity → refund or credit at the plan's per-Reel value (Starter/Pro ₹1,250, VIP ₹1,333). Reels not made because footage didn't arrive → roll over up to 7 days into the next cycle after 2 reminders, then lapse.
- Cancel any time before Day 25 → no renewal. Delivered work in the current cycle is not refunded.

**T-08 Proposal (after call)**
- EN: *Thank you for the call, [Name]! Summary of what we agreed:*
  *• Plan: [Plan name] — [₹ amount] [one-time / per 30-day cycle] [GST note]*
  *• Included: [list from package card]*
  *• Not included: guaranteed views, followers or brand deals; paid ads spend; new footage shoots by our team*
  *• Start date: [date] · Script pack every [Friday] · First cut within 48 working hours of footage · 2 small revision rounds per Reel*
  *• Payment: [100% advance / 50% now + 50% on Day 15]*
  *• Terms & refund policy: [link]*
  *Reply "CONFIRM" and I'll send the payment link.*
- Hinglish: *Call ke liye shukriya [Name] ji! Jo tay hua uska summary:*
  *• Plan: [Plan name] — [₹ amount] [ek baar / har 30 din] [GST note]*
  *• Shamil: [package card list]*
  *• Shamil nahi: views, followers ya brand deals ki guarantee; ads ka kharcha; hamari team ka on-location shoot*
  *• Start date: [date] · Har [Friday] script pack · Footage milne ke 48 working ghante mein pehla edit · Har Reel par 2 chhote revision rounds*
  *• Payment: [100% advance / 50% abhi + 50% Day 15 par]*
  *• Terms aur refund policy: [link]*
  *"CONFIRM" likh dijiye, main payment link bhej deti hoon.*

**T-09 Payment request**
- EN: *Here are the payment options for [Plan] — ₹[amount]: UPI: [UPI ID] (QR attached) · Card/UPI/Net banking: [Razorpay link] · Bank transfer: details on request. Please share the screenshot or UTR number after paying. Your kick-off is booked for [date].*
- Hinglish: *[Plan] ke liye ₹[amount] ka payment yahan kar sakte hain: UPI: [UPI ID] (QR attached) · Card/UPI/Net banking: [Razorpay link] · Bank transfer: details maangne par. Payment ke baad screenshot ya UTR number bhej dijiye. Aapka kick-off [date] ko booked hai.*

**T-10 Payment received**
- EN: *Payment of ₹[amount] received — thank you! Receipt/invoice no. [#] attached. Next: I'm creating your private WhatsApp group and Drive folder now.*
- Hinglish: *₹[amount] ka payment mil gaya — dhanyavaad! Receipt/invoice no. [#] attached hai. Ab main aapka private WhatsApp group aur Drive folder bana rahi hoon.*

Log every payment in the Payment Log (§8) the same day.

---

### Stage 5 — Onboarding (same working day as payment)

**5.1 WhatsApp group (Smita)**
- Name: `VanIndra × [Client Name]`. Created **from +91 81128 59437**. Members: client (+ their assistant if they want). Team replies through linked devices — no personal team numbers in the group.
- Group description (pin): Drive link · Delivery Tracker link · Studio hours · "First cut within 48 working hours of footage" · "Reply APPROVED to approve a Reel".

**5.2 Google Drive folder (Smita)** — owned by a studio Google account (not a personal one), copied from `06_Client_Workspace_Template/_TEMPLATE_Influencer_Name_100K/`, renamed `[ClientName]_@handle`. The template only has folders 01–03; add the rest:

```
[ClientName]_@handle/
├── 00_Admin_INTERNAL/                 (agreement, invoices, intake responses — never shared)
├── 01_Onboarding_and_Brand_Voice/     (template file 01 — remove internal nickname fields before sharing)
├── 02_Monthly_Content_Calendar/       (template file 02)
├── 03_Scripts_and_Hooks/              (weekly packs — client: Commenter)
├── 04_Raw_Footage_Upload/             (client: Editor)
├── 05_Edits_for_Review/               (client: Viewer)
├── 06_Final_Approved_Reels_and_Covers/(client: Viewer)
├── 07_Monthly_Reports/                (client: Viewer)
└── 08_Brand_Deals/                    (Pro/VIP only — media kit, pitches)
```

**5.3 Intake form (Google Form, client fills within 2 working days)**
- *Basics:* full name/brand · Instagram handle · other platforms · city · WhatsApp · email · plan bought · account type (Creator or Business — affects music) · language to speak in · caption language and script (Roman Hinglish / Devanagari / English / bilingual).
- *Performance:* followers · average Reel views (last 10) · links to your 3 best and 2 weakest Reels · upload 5 Instagram Insights screenshots (last 30 days reach, audience age/gender/city, top Reels with watch time / skip data where shown).
- *Goals:* main goal (brand deals / customer enquiries / authority / followers / product sales) · what you sell or want to promote · where enquiries should go (WhatsApp / website / DM keyword).
- *Boundaries ("what NOT to post"):* topics, words, family/children appearances, religious/political lines, competitors not to mention. Doctors/health: registration details you want disclosed; any claims that need your approval.
- *Style:* 3 creators you admire · editing style (fast retention / clean aesthetic / storyteller) · fonts/colours/logo (upload) · music preference.
- *Logistics:* shooting days that suit you · who shoots · phone model and mic (if any) · who approves scripts/Reels (+ backup) · best time for calls.
- *Consents:* collab-tag `@vanindracreations` (yes/no) · use of your Reels in our portfolio (yes/no) · privacy notice acknowledgement (link).

**5.4 Delivery Tracker (Google Sheet)** — copy the template (§8), share with the client as Viewer/Commenter. This is what we call the "client portal" until a real one exists.

**T-11 Welcome**
- EN: *Welcome to VanIndra Creations, [Name]! This group is your direct line to our studio — Founder Vandana Yadav, Akarsh Yadav (editing) and I reply here from our official desk. Three quick things: 1) Please fill the intake form (10 min): [form link] 2) Your Drive folder: [link] — raw clips go in "04_Raw_Footage_Upload" 3) Track every script and Reel here: [tracker link]. Your strategy and first script pack arrive by [date].*
- Hinglish: *VanIndra Creations mein aapka swagat hai, [Name] ji! Ye group hamare studio se aapki direct line hai — Founder Vandana Yadav, Akarsh Yadav (editing) aur main yahin official desk se reply karenge. 3 cheezein: 1) Intake form bhar dijiye (10 min): [form link] 2) Aapka Drive folder: [link] — raw clips "04_Raw_Footage_Upload" mein daalein 3) Har script aur Reel yahan track karein: [tracker link]. Strategy aur pehla script pack [date] tak aa jayega.*

**T-12 Intake reminder (after 1 working day)**
- EN: *Hi [Name], a gentle reminder to fill the intake form — your strategy starts the moment we have it: [link].*
- Hinglish: *[Name] ji, intake form ka chhota sa reminder — form milte hi aapki strategy shuru ho jaayegi: [link].*

---

### Stage 6 — Strategy & Script Approval

**Steps (Vandana):**
1. Prompt #2 → brand bible into `01_Onboarding_and_Brand_Voice/`. Prompt #3 → calendar into `02_Monthly_Content_Calendar/` — **change "20-Reel" to the plan's number (3 / 12 / 20 / 30)**.
2. Prompt #4 → weekly script pack into `03_Scripts_and_Hooks/Week_[NN].md` (or a Google Doc).
3. Rewrite anything that sounds robotic; check boundaries from the intake form.
4. Health/food/nutrition claims → Akarsh fact-checks with a named source and writes the source in the tracker; the client approves every medical or health statement in writing.
5. Replace any "editor note" names in the prompt output with official names before sharing.

**Approval rule:** client replies within 24 hours. If there's no reply in 48 hours, we proceed with the scripts as written (stated in terms).

**T-13 Scripts for approval**
- EN: *Your scripts for [week dates] are ready: [link]. Reply "OK 1–[n]" to approve all, or write changes like "Reel 2: change hook". Please approve within 24 hours so your shoot stays on schedule.*
- Hinglish: *[week dates] ki scripts ready hain: [link]. Sab approve karne ke liye "OK 1–[n]" likhiye, ya changes likhiye jaise "Reel 2: hook badlo". Shoot time par ho, isliye 24 ghante mein approve kar dijiye.*

---

### Stage 7 — Shoot Guide (fills the missing "15-minute easy phone shoot guide")

Make this a 1-page PDF + a 60-second Hindi voice note from Vandana Yadav. Send once at onboarding and pin in the group.

**15-minute phone shoot checklist**
1. **Place:** quiet room, face a window (light on your face, not behind you). Plain or tidy background.
2. **Phone:** back camera, vertical (9:16), 1080p or 4K at 30 fps, lens wiped, no beauty filter. Phone at eye level (stack of books / tripod).
3. **Frame:** head and shoulders, eyes in the top third, a little space above the head.
4. **Sound:** lapel mic if you have one; otherwise phone 1 arm's length away, fans/AC off for the take.
5. **Takes:** 2 takes per script line; pause 2 seconds before and after each line; if you stumble, pause and repeat the full sentence.
6. **Hook first:** say the first line with energy, looking straight into the lens — no "hello friends" intro.
7. **B-roll:** 5–8 short clips (3–5 s each) related to the topic: hands at work, product, clinic, street, kitchen.
8. **Send:** upload originals to "04_Raw_Footage_Upload" in Drive, or send on WhatsApp as **Document** (not as video). Name clips like `Reel03_take2`.

**T-14 Shoot reminder**
- EN: *Shoot day reminder for Reels [x–y]! The 15-minute guide is pinned above. Upload originals to Drive (or send as Document) by [day] and your first edit arrives within 48 working hours.*
- Hinglish: *Reels [x–y] ka shoot reminder! 15 minute wala guide upar pinned hai. [day] tak original files Drive par upload karein (ya Document ki tarah bhejein), aur pehla edit 48 working ghante mein aa jaayega.*

---

### Stage 8 — Footage → Edit

**Akarsh (or assigned freelancer):**
1. Check footage within 4 working hours of upload: complete? audible? vertical? If not, ask for a retake immediately (the 48-hour clock starts on usable footage).
2. Update tracker: `Footage received` date/time → `First cut due` = +48 working hours.
3. Edit to the client's style guide; cover from the client's Canva template (not the VanIndra-branded Thumbnail Studio).
4. Run the QA checklist (§6). Vandana does the final 10-minute QA.
5. Export 1080×1920, upload to `05_Edits_for_Review/`, update tracker, Smita (or Akarsh via linked device) sends T-17.

**T-15 Footage received**
- EN: *Received your clips for Reels [x–y] — thank you! First edit of Reel [x] by [day, time]; the full batch by [day].*
- Hinglish: *Reels [x–y] ki clips mil gayi — shukriya! Reel [x] ka pehla edit [day, time] tak, aur poora batch [day] tak.*

**T-16 Footage reminder (Day 3 after script approval, then Day 5)**
- EN: *Hi [Name], we haven't received clips for Reels [x–y] yet. If they reach us by [day], everything stays on schedule. Need help with a script or setup? Just reply here.*
- Hinglish: *[Name] ji, Reels [x–y] ki clips abhi tak nahi aayi. [day] tak mil jaayein toh sab time par rahega. Script ya setup mein madad chahiye toh yahin bata dijiye.*

---

### Stage 9 — Review & Revisions

**T-17 First cut ready**
- EN: *Reel [x] — first edit is ready: [link]. Reply "APPROVED", or send all changes in one message. Each Reel includes 2 rounds of small changes (text, captions, music level, trims). A new concept or new footage counts as a new Reel.*
- Hinglish: *Reel [x] ka pehla edit ready hai: [link]. "APPROVED" likhiye, ya saare changes ek hi message mein bhejiye. Har Reel mein 2 rounds ke chhote changes shamil hain (text, captions, music level, trimming). Naya concept ya nayi footage = nayi Reel.*

Revision turnaround: ≤ 1 working day per round. Log each round in the tracker.

---

### Stage 10 — Delivery / Publishing

**Trial, Starter, Pro (client posts):** final MP4 + cover + posting kit in `06_Final_Approved_Reels_and_Covers/`.

**T-18 Final files + posting kit**
- EN: *Reel [x] is final! Download: [link]. Posting kit: • Caption: [text] • Hashtags: [list] • Cover: [file] • Best time: [time] • Pinned comment: [text] • Music: [add trending audio "[name]" in Instagram before posting / already included] • [If agreed] invite @vanindracreations as collaborator. [If any brand is involved: turn on the "Paid partnership" label and add the disclosure in the first line.]*
- Hinglish: *Reel [x] final hai! Download: [link]. Posting kit: • Caption: [text] • Hashtags: [list] • Cover: [file] • Best time: [time] • Pinned comment: [text] • Music: [post karne se pehle Instagram mein trending audio "[name]" lagayein / pehle se shamil hai] • [Agar tay hua ho] @vanindracreations ko collaborator invite karein. [Agar koi brand juda hai: "Paid partnership" label on karein aur pehli line mein disclosure likhein.]*

**VIP publishing (only after the VIP SOP is tested — see `04`):** client gives access through Meta Business Suite / account partner access and YouTube channel permissions — **never their password**. Schedule from the calendar; check that collaborator invites and music work when scheduling (test first — some features are app-only). Confirm each week with a list of scheduled posts (T-19).

**T-19 VIP weekly schedule confirmation**
- EN: *This week's Reels are scheduled: [Mon – topic – time], [Tue – topic – time] … Anything to change? Reply by [day, time] and we'll update the schedule.*
- Hinglish: *Is hafte ki Reels schedule ho gayi hain: [Mon – topic – time], [Tue – topic – time] … Kuch badalna hai? [day, time] tak bata dijiye, hum schedule update kar denge.*

---

### Stage 11 — Monthly Report & Review Call

**Inputs:** client's Insights screenshots (or partner access), the tracker, the Brand Deals log (Pro/VIP).
**Owner:** Smita compiles by working day 3 of the next cycle; Vandana writes the "what to post next" section.

**1-page report template**
1. **Delivered vs. promised:** scripts [n/n], Reels [n/n], covers [n/n], on-time first cuts [%]. Any miss → reason + make-good.
2. **Performance (from Instagram Insights):** Reels published, plays/views, reach, average watch time, skip rate / 3-second data *where Instagram shows it*, saves, shares, follows from Reels, profile visits, link taps. Compare with the baseline from the intake form. No projections.
3. **Top 3 Reels and why** · **2 weakest and what we'll change.**
4. **What to post / stop next month** (Vandana).
5. **Brand pipeline (Pro/VIP):** brands pitched / replied / negotiating / closed.
6. **Next month:** themes, shoot dates, what we need from the client.

**T-20 Report + call**
- EN: *Your [Month] report is ready: [link]. Highlights: [1 line]. Let's do our [20/30]-minute review call — [Day, Time] or [Day, Time]?*
- Hinglish: *Aapki [Month] ki report ready hai: [link]. Khaas baat: [1 line]. [20/30] minute ki review call karte hain — [Day, Time] ya [Day, Time]?*

---

### Stage 12 — Renewal, Upgrade, Pause, Exit

**Cycle calendar:** Day 23 renewal reminder · Day 25 invoice/payment link · payment before Day 1 of the next cycle · upgrades/downgrades/cancellations by Day 25.

**T-21 Renewal reminder (Day 23)**
- EN: *Hi [Name], your current cycle ends on [date]. Shall we continue with [Plan] for [next month]? Reply YES and I'll send the payment link, or tell me if you'd like to change plans.*
- Hinglish: *[Name] ji, aapka current cycle [date] ko khatam ho raha hai. [Next month] ke liye [Plan] continue karein? YES likhiye, main payment link bhej dungi — ya plan badalna ho toh bata dijiye.*

**T-22 Trial wrap-up + upgrade offer**
- EN: *Your 3 trial Reels are complete! Quick summary: [what worked]. If you'd like to continue, Starter (12 Reels/month) or Pro Growth (20 Reels/month) can start on [date]. [If the owner approves: your ₹2,999 trial is adjusted against the first month if you join by [date].]*
- Hinglish: *Aapki 3 trial Reels complete ho gayi! Chhota summary: [kya achha chala]. Aage badhna ho toh Starter (12 Reels/mahina) ya Pro Growth (20 Reels/mahina) [date] se shuru ho sakta hai. [Owner approve kare toh: [date] tak join karne par ₹2,999 pehle mahine mein adjust ho jaayega.]*

**Exit / pause:** deliver all final files; client keeps final Reels after full payment; remove the client's access to raw-footage folders after 30 days (confirm retention period); keep invoices and agreement in `00_Admin_INTERNAL/`.

**T-26 Pause / cancellation confirmation**
- EN: *Confirmed — your plan will pause after [date]. All your final Reels stay in your Drive folder: [link]. Thank you for working with us, [Name]. Whenever you're ready, we're one message away.*
- Hinglish: *Confirm — aapka plan [date] ke baad pause ho jaayega. Aapki saari final Reels Drive folder mein hain: [link]. Saath kaam karne ke liye shukriya, [Name] ji. Jab bhi chahein, bas ek message kar dijiye.*

---

## 5. Exception Messages

**T-23 Delay on our side (send before the deadline passes, never after)**
- EN: *[Name], an honest update: Reel [x] will reach you by [new time] instead of [old time] because [short reason]. I'm sorry for the delay. [Make-good, e.g., an extra cover / priority on the next batch / per-Reel credit.]*
- Hinglish: *[Name] ji, seedhi baat: Reel [x] [old time] ki jagah [new time] tak aayegi kyunki [short reason]. Der ke liye maafi. [Make-good, jaise extra cover / agle batch mein priority / per-Reel credit.]*

**T-24 Payment overdue (Day 3 after due date)**
- EN: *Hi [Name], a gentle reminder that ₹[amount] for [cycle] was due on [date]: [link]. Production for the next batch resumes as soon as it's received.*
- Hinglish: *[Name] ji, chhota sa reminder — [cycle] ke ₹[amount] [date] ko due the: [link]. Payment milte hi agle batch ka kaam shuru ho jaayega.*

**T-25 Extra request outside scope**
- EN: *Happy to help with [request]! It's outside your current plan, so it would be [₹ amount / count as 1 Reel from your plan]. Shall I go ahead?*
- Hinglish: *[Request] mein zaroor madad karenge! Ye aapke current plan se bahar hai, isliye iska [₹ amount / plan ki 1 Reel count hogi]. Aage badhein?*

---

## 6. Internal QA Checklist (defines the website's "4 retention rules")

Every Reel must pass all 4 rules **and** every safety check before it is sent. Mark Pass/Fail in the tracker.

**The 4 retention rules**
1. **Hook:** on-screen hook text visible by 0.5 s; spoken hook finished by 3 s; no greeting/intro before the hook.
2. **Safe zone:** hook and captions never hidden by Instagram buttons — keep key text out of the bottom ~20% and the right-hand button column; check on a phone preview.
3. **Pace:** a visual change (cut, zoom, B-roll, graphic) at least every 2–4 s; no dead air longer than 1 s.
4. **Payoff + CTA:** the promise of the hook is delivered; one clear CTA (comment keyword / save / WhatsApp) or a loop ending.

**Safety checks**
- Spelling correct in Hindi/Hinglish/English captions and cover.
- Voice clear; music under the voice; only licensed or in-app music; no unlicensed footage.
- Health, food, finance or legal claims: source written in the tracker and client approval received. No cure/guarantee claims.
- Any brand, product, gift or affiliate link involved → disclosure label + Instagram "Paid partnership" tag (ASCI influencer guidelines — confirm current wording).
- No disparagement of named brands/competitors; client boundaries respected.
- Cover: 3–4 words, readable as a grid thumbnail; export 1080×1920.

---

## 7. Side Flows

### 7.1 Brand enquiry for our in-house creators (Vandana Yadav, Smita Yadav)
1. Brand messages → T-27; label `Brand enquiry`.
2. Smita sends the media kit + single public rate card (to be created — `04` T6).
3. Written agreement (`04` L4): deliverables, posting date, script/approval rounds (max 2), disclosure, usage/whitelisting period, exclusivity, payment (e.g., 50% advance, 50% within [x] days of posting), invoice details, TDS (confirm with CA).
4. Product delivery to an address the team is comfortable sharing (not published anywhere).
5. Script → brand approval → shoot (Vandana Yadav, ~1 h slot) → edit (Akarsh) → brand approval → post with disclosure → share 7-day Insights screenshots → final invoice.

**T-27 Brand enquiry reply**
- EN: *Thank you for reaching out to VanIndra Creations! I'm Smita Yadav, handling partnerships for Vandana Yadav (@vandanay2012) and Smita Yadav (@smitayadav_0901). Please share: product, deliverables (Reel/Story/combo), timeline, budget range, usage rights needed and any exclusivity. I'll send our media kit and rate card right away.*
- Hinglish: *VanIndra Creations se contact karne ke liye shukriya! Main Smita Yadav, Vandana Yadav (@vandanay2012) aur Smita Yadav (@smitayadav_0901) ki partnerships dekhti hoon. Please bataiye: product, deliverables (Reel/Story/combo), timeline, budget range, usage rights aur exclusivity. Main turant media kit aur rate card bhej deti hoon.*

### 7.2 D2C UGC Ad Pack (3 ads)
- Brief form (T-28) → agreement with usage term (e.g., brand's paid ads for 30 or 90 days — confirm pricing for longer) → product reaches us → 1 shoot day → edits → 1 revision round per ad → delivery.
- **Timeline:** 7 working days after product receipt (the website says 5 days — recommend changing).
- Deliverables: 3 × 9:16 ads (15–30 s), 3 different hooks, edited files + clean versions without captions, ad copy suggestions. No promise on ROAS/CPA.

**T-28 UGC brief request**
- EN: *Thanks! To scope your 3-ad pack, please share: product link, target customer, 3 key benefits, claims you can substantiate, ad platforms, how long you'll run the ads, and your deadline. Timeline is 7 working days after the product reaches us.*
- Hinglish: *Shukriya! 3-ad pack ke liye please bhejiye: product link, target customer, 3 main benefits, kaunse claims aap prove kar sakte hain, ads kahan chalenge, kitne din chalenge, aur deadline. Product hum tak pahunchne ke 7 working days mein delivery.*

---

## 8. Trackers (Google Sheets — ₹0)

**Lead Sheet** — Date · Source (website AI form / WhatsApp / IG DM / referral / outreach) · Name · Handle · Followers · Niche · Language · Interested in · Stage (`New` → `Qualified` → `Sample sent` → `Call booked` → `Proposal sent` → `Paid` / `Lost` / `Waitlist`) · Next action + date · Owner · Notes. Mirror the stages with WhatsApp Business labels.

**Delivery Tracker (one per client, shared with client)** — Reel # · Week · Topic · Script sent · Script approved · Footage received (date-time) · First cut due (= +48 wh) · First cut sent · Rev 1 · Rev 2 · Final approved · Posted/Scheduled date · Post link · QA pass (Y/N) · Source for claims · Notes.

**Capacity Board (internal)** — rows = weeks; columns = client · Reels due · editing hours (Reels × 2.5) · editor (Akarsh / freelancer) · status. Total editing hours vs. capacity (see `02`). Smita checks it before every quote.

**Payment Log (internal)** — Receipt/Invoice # · Date · Client · Plan/cycle · Amount · GST (if registered) · Mode · UTR/Ref · Received on · Refund/credit notes.

**Weekly ops review (Monday, 30 min — Vandana, Smita, Akarsh):** missed or at-risk deadlines, footage pending, capacity next 4 weeks, leads in pipeline, any client complaint.
