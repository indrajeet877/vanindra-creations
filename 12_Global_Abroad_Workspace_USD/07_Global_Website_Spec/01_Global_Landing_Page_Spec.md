# Global Landing Page Spec — vanindracreations.com (English, USD)

> **This is a spec, not code.** Build it as a **separate site** from the India funnel. Nothing from the India page (₹ pricing, Hindi toggle, voice input, AI plan generator, 3D phone, festival language) carries over.
> **Goal of the page:** turn a cold visitor into one of two actions — **request a free 15-second sample** or **book a 15-minute call**.

---

## 1. Domain, Hosting & Separation Rules

| Item | Spec |
| :--- | :--- |
| Domain | **`vanindracreations.com`** (the domain plan currently redirects `.com` → `.in`; switching `.com` to the global site needs owner approval). `.in` remains the India site. |
| URL rule | **Do not use or link to the current github.io project URL** — it contains the name of a background team member. The global site must only ever be reachable and shared at `vanindracreations.com`. |
| Repo | A **separate repository** under a neutral GitHub organisation/account (e.g., `vanindracreations`), not this repo. Keeps the global site's history free of internal docs and names. |
| Hosting | Static site on **Cloudflare Pages**, Netlify or Vercel, with the custom domain, HTTPS, and `www` → apex redirect. (All have free tiers — verify limits.) |
| Stack | Plain HTML + CSS (+ minimal JS), or Astro. No heavy frameworks needed. |
| India link | Optional small footer link: "Based in India? Visit vanindracreations.in" (owner decision). |
| Email shown | Domain addresses once Google Workspace is set up: `hello@`, `smita@`, `akarsh@vanindracreations.com`. Until then, Smita Yadav's official email `smitayadav497@gmail.com`. |
| WhatsApp shown | **Only `+91 81128 59437` (Smita Yadav).** No other number anywhere. |
| Names shown | **Only Vandana Yadav, Smita Yadav, Akarsh Yadav.** Official full names, no nicknames. |

---

## 2. Page Structure (Single Long Page + 3 Legal Pages)

```
/            Home (sections 1–12 below)
/privacy     Privacy Policy
/terms       Terms of Service
/refunds     Refund & Guarantee Policy
```
Booking and sample-request forms open as embeds or modals on the home page (no separate pages needed at launch).

| # | Section | Purpose |
| :--- | :--- | :--- |
| 1 | Sticky nav | Orientation + always-visible "Book a call" |
| 2 | Hero | Promise + 2 CTAs + before/after video |
| 3 | How overnight works | Turn "you're overseas" into the selling point |
| 4 | Before / After reel wall | Proof of craft |
| 5 | Who we work with | Visitor self-identifies |
| 6 | What's included | Deliverables at a glance |
| 7 | Pricing | Transparent USD plans + pilot |
| 8 | Promises we can keep | Guarantees, risk reversal |
| 9 | Meet the studio | Real faces, trust |
| 10 | Why teams switch | Positioning vs. alternatives |
| 11 | FAQ | Objection handling |
| 12 | Final CTA + footer | Conversion + legal / contact |

---

## 3. Exact Copy

### 3.1 Nav
`VanIndra Creations` (logo) · Work · How it works · Pricing · Team · FAQ · **[Book a call]** (gold button)

### 3.2 Hero
- **Eyebrow:** Short-form video studio for podcasters, coaches, clinics and founders
- **H1:** **Your videos, edited while you sleep.**
- **Subhead:** Send us raw footage or your latest podcast before you log off. Wake up to captioned, scroll-stopping Reels, TikToks, Shorts and LinkedIn clips — ready to post. Plans from $500/month.
- **Primary CTA:** `Get a free 15-second sample edit`
- **Secondary CTA:** `Book a 15-minute call`
- **Microcopy under buttons:** Month-to-month · Next-business-day delivery · We never ask for your passwords
- **Visual:** two vertical videos side by side, labelled **Before** / **After** (autoplay, muted, loop, `playsinline`). Use only our own or permission-cleared footage.
- **Clock badge (labelled "Example timeline"):** `Upload 6:00 pm ET → Drafts ready ~7:00 am ET`

### 3.3 How overnight works
- **H2:** Upload tonight. Review tomorrow morning.
- **Step 1 — Upload before you log off.** Drop raw clips or a full episode into your shared folder. Add a note if you like.
- **Step 2 — We edit while you sleep.** Our editors cut, caption and design every video. Our creative director checks each one against a 12-point quality list.
- **Step 3 — Review over coffee.** Comment right on the video. Changes come back the next business day. Approve, post, repeat.
- **Time-zone strip:** New York · Toronto · Los Angeles · Sydney · Auckland — drafts usually ready by your morning. London · Dublin — by lunchtime the next day.

### 3.4 Before / After reel wall
- **H2:** Same footage. Better video.
- **Sub:** Every edit starts with the strongest moment, adds captions people can read with the sound off, and keeps the pace up to the last second.
- 6 vertical cards; each caption says what changed, e.g., *"Opened on the punchline · animated captions · 3 B-roll cut-ins."*
- Label spec work honestly: **"Studio sample"**. Client work only with written permission.

### 3.5 Who we work with
- **H2:** Built for people whose content brings in business
- **Podcasters** — Your best moments, clipped and captioned every week.
- **Coaches & consultants** — Content that fills your calendar, without the editing.
- **Health & wellness pros** — Clear, careful education videos, edited by someone with a science background.
- **Founders on LinkedIn** — Turn talks, podcasts and Zoom calls into thought-leadership clips.
- **Real estate** — Listing tours and market updates, back by morning.
- **E-commerce brands** — More hook variants from the footage you already have.

### 3.6 What's included
- **H2:** Everything between "record" and "post"
- Hooks that earn the first two seconds · Animated, brand-styled captions · B-roll, zooms and sound design · Covers and thumbnails · Versions for every platform · Monthly plans and scripts · Posting and community management (Full Studio) · Monthly reports in plain English

### 3.7 Pricing
- **H2:** Simple plans. Real deliverables. No lock-in.
- **Sub:** All prices in USD. Month-to-month — cancel with 15 days' notice. Save 10% when you pay quarterly.

**Pilot strip (above cards):**
> **Not sure yet? Start with a pilot.** $149 one-time — 3 finished videos from your footage, 2 revision rounds, delivered in 5 business days. 100% credited to your first month if you continue within 14 days. **[Start a pilot]**

**Card 1 — Spark — $500/month**
*Turn footage you already have into consistent clips.*
- 12 short videos a month (up to 60 sec)
- Edited from your raw footage, podcast or long-form videos
- Animated captions, hook titles, B-roll and sound design
- Cover frame for every video
- One 9:16 master for Reels, TikTok and Shorts
- 1 revision round · 2-business-day turnaround
- Monthly delivery summary
**[Choose Spark]**

**Card 2 — Momentum — $1,000/month** · badge: **Most popular**
*A plan, scripts and 20 polished videos every month.*
- 20 short videos a month (up to 90 sec)
- Monthly content plan: what to post — and what not to
- Up to 8 scripts written for you to film
- Custom cover for every video
- Versions for Reels, TikTok, Shorts and LinkedIn
- Post captions and keywords for each platform
- 2 revision rounds · next-business-day turnaround
- Monthly 30-minute strategy call + performance report
**[Choose Momentum]**

**Card 3 — Full Studio — $2,000/month**
*We run your short-form presence, start to finish.*
- 30 short videos a month (up to 90 sec)
- Full strategy, research and scripts for every original video
- We schedule and post to up to 3 platforms
- Comment and DM replies, 5 days a week
- Hook testing and a quarterly profile refresh
- Priority next-business-day turnaround + 1 rush video a week
- Bi-weekly calls, weekly snapshot, monthly report
**[Book a call about Full Studio]**

*Founding-client note (only while slots remain, only if owner approves):* "Founding client rate: 20% off your first 3 months — [n] of 5 spots left." Update `[n]` honestly or remove the line.

### 3.8 Promises we can actually keep
- **H2:** Promises we can actually keep
- **On-time, or it's free.** If we miss an agreed delivery date for reasons within our control, that video is credited on your next invoice.
- **Pilot guarantee.** If your first pilot video doesn't match the brief after two revision rounds, we refund the pilot in full.
- **No lock-in.** Month-to-month. Cancel any time with 15 days' notice before your next billing date.
- **Your videos are yours.** Once an invoice is paid, the final videos are yours to use anywhere.
- **What we won't promise:** views, followers or sales. Platforms control distribution — we control the quality, the volume and the deadlines. We never use bots or paid engagement.

### 3.9 Meet the studio
- **H2:** The people behind your videos
- **Vandana Yadav** — Founder & [Chief Influencer Director / Creative Director — owner to choose]
  *Built her own Instagram audience to 50K+ followers (verify the number at launch). Leads creative direction and signs off every video before it reaches you.* · Instagram `@vandanay2012`
- **Smita Yadav** — [Client Partnerships Lead / Growth, Brand Deals & Client Relations Lead]
  *Your point of contact from the first call to every delivery. B.Com, Gargi College, University of Delhi.* · Instagram `@smitayadav_0901` · WhatsApp `+91 81128 59437` · Email
- **Akarsh Yadav** — [Head of Editing / Tech, Video Editing & Scientific Niche Lead]
  *Leads our editing team. B.Voc in Food Technology, University of Allahabad — so science, health and nutrition content is edited by someone who understands it.* · Instagram `@yadavakarsh_07` · Email
- **Studio line:** We're based in India and work your hours through a structured overnight workflow.
- Real photos only. Official app logos next to every handle, number and email (Instagram gradient, WhatsApp green `#25D366`, Gmail envelope).

### 3.10 Why teams switch to us
- **H2:** Why teams switch to us

| | Doing it yourself | Freelance marketplaces | AI clipping tools | **VanIndra Creations** |
| :--- | :--- | :--- | :--- | :--- |
| Your time per week | Hours | Briefing + chasing | Fixing captions and picks | **Upload + 10 minutes of review** |
| What to post | You decide alone | Rarely included | Not included | **Monthly plan + scripts** |
| Human quality check | — | Varies | — | **Every video, 12 points** |
| Turnaround | When you find time | Varies | Instant, needs fixing | **Next business day** |
| Commitment | — | Per gig | Subscription | **Month-to-month** |

*(Keep it factual and neutral; never name competitors.)*

### 3.11 FAQ (exact copy)

1. **Where is your team based?**
   In India. That's how we deliver overnight for North America and Australia: you upload at the end of your day, we edit during ours, and drafts are usually waiting when you start work.
2. **What do I need to send you?**
   Raw video from your phone or camera, or long-form content like podcast episodes, webinars or talks. We'll send a one-page recording guide on day one.
3. **Do you write scripts?**
   On Momentum (up to 8 a month) and Full Studio (every original video). On Spark, we work from your footage and write the hook text and on-screen titles.
4. **Which platforms do you edit for?**
   Instagram Reels, TikTok, YouTube Shorts, LinkedIn and Facebook. Momentum and Full Studio include platform-specific versions.
5. **How many revisions do I get?**
   One round per video on Spark, two on Momentum and Full Studio. Changes come back the next business day.
6. **How fast is delivery?**
   Next business day on Momentum and Full Studio, two business days on Spark — counted from when we receive complete footage.
7. **Do you guarantee views or followers?**
   No — and be wary of anyone who does. We guarantee the work: the number of videos, the deadlines and the quality bar. We report on performance monthly and adjust what we make.
8. **Who owns the videos?**
   You do, once the invoice is paid.
9. **Do you need my passwords?**
   Never. We use partner access through Meta Business Suite, YouTube permissions or your scheduling tool, so you can remove us with one click.
10. **Is the music licensed?**
    Yes. Anything we add comes from a licensed library, or you can add platform audio when you post.
11. **Do you use AI?**
    Yes, for speed — transcription, first-pass clip finding and caption timing. Every video is edited and checked by people before you see it.
12. **How do payments work?**
    Plans are billed monthly in advance, in USD, by card or bank transfer. You'll get a proper invoice every month.
13. **Can I cancel?**
    Any time, with 15 days' notice before your next billing date. No long-term contract.
14. **What if I don't like the first videos?**
    Start with the $149 pilot. If the first video doesn't match the brief after two revision rounds, we refund the pilot in full.

### 3.12 Final CTA + footer
- **H2:** Send us one video. We'll show you what it could be.
- **Sub:** A free 15-second sample edit, delivered privately. No call needed.
- **Buttons:** `Get my free sample` · `Book a 15-minute call`
- **Footer:** VanIndra Creations — The Overnight Short-Form Studio · Founded by Vandana Yadav · [Registered business address — owner to provide] · Email · WhatsApp `+91 81128 59437` (Smita Yadav) · Instagram `@vanindracreations` · Privacy · Terms · Refunds · © 2026 VanIndra Creations

---

## 4. Forms & Booking

### 4.1 Free sample request (Tally / Google Forms / Typeform embed)
Fields: Full name* · Email* · Link to one video you've posted* (or upload) · What do you sell?* · Where do you post most? (Instagram / TikTok / YouTube / LinkedIn / Other) · Monthly budget for video (Under $500 / $500–$1,000 / $1,000–$2,000 / $2,000+) · Anything we should know? · ☐ I agree to be contacted about this request.*
- **Confirmation message:** "Thanks — we review every request personally. If it's a fit, your 15-second sample arrives within 2 business days."
- Submissions go to the global lead tracker (`Source_Channel = Website`) and notify Akarsh Yadav.

### 4.2 Booking (Cal.com or Calendly)
- **Event:** "15-minute intro call with Smita Yadav" (Google Meet or Zoom link auto-generated).
- **Availability (set in India time; the tool shows each visitor their own time):**
  - Americas: Mon–Thu **19:30–22:30**
  - UK / Europe: Mon–Fri **14:30–18:00**
  - Australia / NZ: Mon–Fri **09:00–11:30**
- Buffers 15 min · max 4 calls/day · minimum notice 12 hours · reminders 24 h and 1 h before.
- **Booking questions:** website / profile link · what you sell · platforms · monthly budget band (same options as above) · what you'd like help with.
- **Confirmation copy:** "You're booked with Smita Yadav. Before the call, have one or two of your videos handy — we'll talk about what's working and what we'd change."
- Owner to confirm Smita's availability windows (exam periods especially).

---

## 5. Trust Elements Checklist

- [ ] Real team photos and full names (only the three public team members)
- [ ] Before/after samples, honestly labelled ("Studio sample" vs. client work with permission)
- [ ] Founder's Instagram proof (number verified at launch)
- [ ] Transparent USD pricing on the page
- [ ] Guarantees in plain English + Refund Policy page
- [ ] Business email on our domain; registered business address in the footer
- [ ] Privacy Policy, Terms, Refund Policy pages (reviewed — see Payments & Legal doc)
- [ ] Payment logos **only** for rails that are actually live
- [ ] Testimonials section **hidden until we have real ones** — never placeholders on the live site
- [ ] Review badges (Upwork / Contra / Google / Clutch) only once real reviews exist

---

## 6. Technical & Design Requirements

- **Palette:** Warm Ivory `#FAF8F3`, Alabaster `#FFFFFF`, Deep Studio Emerald `#09241B` / `#0E6B4E`, Imperial Gold `#D4A024` / `#F4C44E` (gold for primary CTAs). Calmer than the India site — more white space, fewer badges.
- **Type:** Space Grotesk (headings, matches the India brand) + Inter (body).
- **Performance:** each video MP4/H.264 ≤ ~4 MB with a poster image; lazy-load everything below the fold; target Largest Contentful Paint under 2.5 s on mobile.
- **Accessibility:** WCAG AA contrast, keyboard-navigable, alt text, captions on all videos, respects `prefers-reduced-motion`.
- **Mobile first:** most cold traffic arrives from phones (LinkedIn / Instagram). 16 px side gutters, no horizontal scroll, thumb-reachable CTAs.
- **SEO:**
  - Title: `VanIndra Creations — Short-Form Video Editing Studio for Reels, TikTok & Shorts`
  - Meta description: `Send raw footage or podcasts before you log off — wake up to captioned, ready-to-post short-form videos. Plans from $500/month. Month-to-month.`
  - Open Graph image: before/after split frame with the tagline.
  - Structured data: Organization, Service, FAQPage.
  - Never claim a US/UK/AU office or address.
- **Analytics & consent:** Plausible (cookie-less) is simplest; if GA4, Meta Pixel or LinkedIn Insight are added, show a consent banner for UK/EU visitors (confirm requirements).
- **Not on this page:** ₹ pricing, Hindi/Hinglish, voice input, AI plan generator, internal scripts, team nicknames, any phone number other than `+91 81128 59437`, any name outside the three public team members.

---

## 7. Launch Checklist

- [ ] Owner approvals: domain switch, prices, titles, founding offer, footer address
- [ ] Separate repo + hosting + custom domain + HTTPS live
- [ ] Copy proofread by someone fluent in US English (read it aloud)
- [ ] 6 before/after samples cleared for use
- [ ] Forms → tracker + notifications tested end-to-end
- [ ] Booking tested from US, UK and AU time-zone settings
- [ ] Legal pages published
- [ ] Mobile test on iPhone + Android; Lighthouse performance check
- [ ] Final grep of the site for banned names, nicknames and numbers before going live
