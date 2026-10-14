# Post-Login Client Rules, Lightweight Data Storage & Payment Gateway Architecture

> **Live Client Portal URL:** [`login.html`](../login.html) (`https://vanindracreations.pages.dev/login.html`)
> **Single Official WhatsApp Desk:** **Smita Yadav (`+91 81128 59437`)**

---

## 1. Golden Rules Once a Client Logs Into `login.html`

When a creator or business owner signs up or logs into our **Client Portal (`login.html`)**, the team follows these 5 strict operating rules:

1. **Rule #1 — Single Point of Communication (`+91 81128 59437`):**
   - All portal brief submissions, raw footage notifications, and approval alerts route directly to **Smita Yadav's Official WhatsApp Concierge (`+91 81128 59437`)** and the client's dedicated WhatsApp group (`VanIndra × [Client Name]`).
2. **Rule #2 — Zero Password Sharing Required for Starter/Pro Clients:**
   - Clients never have to worry about account security. They drop raw phone clips via Google Drive / WhatsApp link inside `login.html`, and download their finished 9:16 Reels + Magnific 4K Covers + Hinglish/English Captions directly.
3. **Rule #3 — 48-Hour Studio Turnaround SLA:**
   - Once raw footage is submitted via the portal, **Akarsh Yadav** delivers the first edited cut within **24–48 hours**, reviewed under **Founder Vandana Yadav's** "What to Post / Not Post" quality checklist.
4. **Rule #4 — 1-Click Approval & 2 Free Revisions:**
   - Inside `login.html`, each Reel has a status pill (`In Editing` → `Ready for Review` → `Approved ✓`). Every Reel includes up to **2 free micro-revisions** (caption tweak, hook banner text, or music level).
5. **Rule #5 — Monthly ROI & Brand Deal Readiness Review:**
   - At the end of every 30 days, **Smita Yadav** shares a 1-page summary of reach growth, top-performing hooks, and brand deal pitch readiness.

---

## 2. Data Storage Architecture (Small Data Now → Auto-Scale Later)

As requested: *"Since it is very small data right now we are reaching out so no need to worry about it. That can be tackled there only if we are going to get more customers."*

| Stage | Active Clients | Data & CRM Storage Solution | Cost | How It Works |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1 (Now: 1 to 15 Clients)** | `1–15 Clients` | **Browser `localStorage` + Direct WhatsApp Payload + Shared Google Drive/Sheet** | **₹0 / Free** | When a prospect or logged-in client submits a form on `index.html` or `login.html`, it saves locally in their browser AND sends the structured brief directly to Smita Yadav's WhatsApp (`+91 81128 59437`). Raw videos live in a free shared Google Drive folder per client (`06_Client_Workspace_Template`). |
| **Phase 2 (Growth: 15 to 100+ Clients)** | `15–100+ Clients` | **Firebase Firestore / Supabase Free Tier + Google Sheets Webhook** | **₹0 / Free Tier** | Without changing the frontend design of `index.html` or `login.html`, we connect a 10-line Firebase/Supabase script so all client logins, reel approval statuses, and invoice links sync across devices in real time. |

---

## 3. Payment Gateway & Billing SOP (Zero Setup Delay)

1. **Immediate Phase (First 10 Clients — Zero Gateway Fees):**
   - **Direct UPI QR & UPI ID / Bank Transfer:** For the **₹2,999 3-Reel Trial Pack** and **₹14,999–₹24,999 Monthly Retainers**, Smita shares the official VanIndra Creations UPI QR code or payment link directly on WhatsApp after the Free 15s Sample Edit is approved.
   - **Payment Split:**
     - `₹2,999 Trial Pack`: 100% upfront before delivering the 3 full reels.
     - `₹14,999 / ₹24,999 / ₹39,999 Monthly Retainers`: **50% on Onboarding Day 1** + **50% on Day 15 (after first 10 Reels delivered)**.
2. **Scale Phase (10+ Clients):**
   - Activate **Razorpay Payment Links / Subscriptions** (supports UPI AutoPay, Credit Cards, and International Cards for NRI creators).
