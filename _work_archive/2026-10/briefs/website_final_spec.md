# VanIndra homepage — FINAL build spec (D2 Editorial Ivory + grafts)

SCRATCH = /tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad
WEB = SCRATCH/web2

## Decision
Judges: D2 Editorial Ivory won (8.0 / 8.3 / 7.7; avg 8.0), D1 Noir Bento 7.4, D3 Liquid Glass 7.4. The final page is **D2 as the base** (`WEB/d2_editorial_ivory/index.html`), improved with the fixes and grafts below. Full judge verdicts: `WEB/judges.json`. Original brief and rules: `WEB/BRIEF.md` (still applies). Source pages for grafts: `WEB/d1_noir_bento/index.html`, `WEB/d3_liquid_glass/index.html`. The current live page (source of truth for content): `WEB/current_index.html`. Honesty reference: `/home/user/vanindra-creations/13_India_Delivery_and_Fulfillment_Backend/03_Risky_Claims_and_Fixes.md` (R1–R29).

Output: `WEB/final/index.html` (folder `WEB/final/` already has an `assets` symlink). Single self-contained file. Keep D2's look and voice: ivory default, emerald ink, gold accents, Instrument Serif display + grotesk, hairlines, one dark emerald band.

## A. Hero
1. Desktop (1440×900): keep the split hero; the headline, the WhatsApp composer with its Send button, and the phone with its Before/After toggle must all be above the 900 px fold.
2. Cut the clutter around the phone: the Before/After toggle plus **at most two** KPI chips, and no chip may overlap the Reel UI (like/comment/share icons, caption, the "Follow" pill). Remove the stacked 3rd chip and the floating retention card (or put the retention line inside the phone). Add realistic phone chrome (9:41 status bar, signal, battery) from D3. **No invented engagement counts** (no likes/comments/shares numbers).
3. Left column: merge the founder pill into the eyebrow line (e.g. "AI + human content studio · Founded by creator Vandana Yadav"), and use D1's compact composer (textarea 2–3 rows, an "Editable" tag, goal chips, Send on one row where space allows).
4. Under the CTA, D3's risk-reversal line: "✓ Free 7-day audit + a 15-second sample edit of your own video, before you pay." (with a Hindi data-hi).
5. Mobile hero order: eyebrow → headline → subhead → two big full-width buttons ("Chat on WhatsApp" → opens the WhatsApp concierge flow / wa.me; "Get my free AI plan" → #smart-ai-portal) → risk-reversal line → the phone with its toggle → KPI chips as a 2-up row under the phone (short labels that never wrap) → the composer. Target mobile hero ≤ ~1,300 px.
6. Mobile sticky bar (WhatsApp + Free AI plan, and a labelled Login) appears only once the hero CTAs have scrolled out of view (IntersectionObserver), so it never covers the composer or hero buttons.
7. Fix the "Follow" pill / comment icon collision in the phone mockup at every width.

## B. Honesty (apply the safer wording from 03_Risky_Claims_and_Fixes.md)
- Remove "84.2% 3-sec hook hold" as a founder fact. Hook-hold %, "6.8L+ views" and similar numbers may appear only inside the simulator, always labelled "Illustration — not a client result".
- KPI chips: no "6.8L+ views". Use e.g. "3-sec hook: On" / "Captions: Kinetic" style toggles or one illustrative metric clearly labelled.
- "1 lakh+ views" badges: keep only on the 4 @vandanay2012 Reels (R24). Smita's two Reels get "Portfolio #02" only.
- Dated stats: "50K+ followers · Oct 2026", "467+ posts".
- Delete "Hooks 100K+ viewers in the first 4 seconds" and every multiplier/superlative (2x fees, 5x revenue, #1 most forwarded, doubles ROAS) (R9, R18).
- AI plan: "Get a free AI-drafted starter plan in about a minute" instead of "seconds" (R15). Privacy note under the generate button (R7): "Your answers go to Pollinations, a free third-party AI service, only to write this plan. Nothing reaches us unless you tap Send on WhatsApp."
- Pricing subhead (R13): "For many creators, one paid collaboration a month can offset the cost — but results vary and we don't guarantee deals."
- Turnaround (R16): "First edit within 48 working hours of receiving your footage" (footnote style), not "24–48h".
- VIP (R8): no "fully hands-free"; button "Apply for VIP"; label "By application"; comment-to-DM shown as "(coming soon)".
- "Most popular" → "Recommended".
- Client portal section: title it "Client portal (preview)", tag the dashboard "Sample data", and add the line "Today every client gets a private WhatsApp group with our studio desk and a shared tracker for scripts, drafts and reports." (R6)
- Minimal effort wording (R14): "about 30–60 minutes a week to record" instead of "zero operations"/"100%".
- Sponsorship desk (F1): "Brands: enquire about a collaboration" instead of "sponsor @vandanay2012 & @smitayadav_0901"; keep the WhatsApp brand enquiry.
- Remove the "Client pitch deck" link from the Portfolio #03 tile; link pitch-deck.html from the footer only.
- No fake scarcity: no "2 slots open" unless written as "Slots open for October 2026".
- The Hindi (data-hi) versions must carry the same honest wording.

## C. Visual and UX fixes
1. Founder tile: replace the B&W crop with the baked "Photo mast aayi hai 😊" caption. Use a clean colour crop of a Reel cover where the text is not the focus, or D3's fanned Reel-cover stack, and fill the dead gap between the stats and the buttons.
2. Small Reel tiles: the @handle overlay must not sit on top of the baked caption text: darker bottom scrim, or move the handle outside the image.
3. Instrument Serif only at ≥ 36 px. Smaller headings (service titles, format titles, ROI label, card titles) in the grotesk at 600.
4. Team cards: real photos for Vandana Yadav (`assets/portfolio/dp_vandanay2012.jpg`) and Smita Yadav (`assets/portfolio/dp_smitayadav_0901.jpg`); keep a monogram for Akarsh Yadav. Remove the dead space in the founder card.
5. Pricing on mobile: Pro Growth (₹24,999, "Recommended") must be visible without swiping, and the other plans easy to find (e.g. the scroller starts on Pro with the Starter card peeking, plus dots or a "Swipe to compare all 4 plans" hint, or a vertical stack). Remove the empty gap in the Trial card.
6. Contrast: every text including disclaimers ≥ 4.5:1 (the --faint colour is too light).
7. Tap targets ≥ 44 px on mobile for chips, language buttons, footer links, filter tabs.
8. Mic button halo must not clip the viewport edge on mobile.
9. **Dark Studio Mode** (required by CLAUDE.md): a 1-click sun/moon toggle in the nav (and mobile menu) that flips the page to a noir palette built from D1's tokens (#06130E base, hairline tiles with an inset top highlight, emerald/gold accents). Persist in localStorage (wrap in try/catch) and respect prefers-color-scheme only if the user has not chosen. Every section must look right in both themes (check screenshots of both).
10. Hindi mode: when the WhatsApp message has not been edited, switch it to natural Hinglish (as D1 does: "Namaste Smita Yadav ji, maine VanIndra Creations ka portfolio (@vandanay2012 & @smitayadav_0901) dekha aur apna page grow karna chahta/chahti hoon…") and back. Translate the remaining English bits (client-portal bullets "Your only job" etc.). Check the Hindi H1 is not heavier/longer than 3 lines at 390 px.

## D. Grafts
- From D1: Reels filter tabs (All 6 / @vandanay2012 / @smitayadav_0901) above the Reels bento.
- From D1: micro-UIs in the services grid: the editing timeline with a playhead (HOOK / V1 / CAP tracks) in the editing cell and the "Post more / Stop posting" mini-card in the strategy cell.
- From D1: activity rows (e.g. "Reel #17 · Delivered", "Script #20 · Approved") under the portal KPI grid (inside the "Sample data" dashboard).
- From D1: small numbered mono eyebrows ("01 — Live portfolio") for wayfinding, used consistently.
- From D3: Slot #03 mini-stats: "Free 7-day audit · 15-sec sample edit · First edit in 48 working hrs".
- From D2 (keep): the stats strip under the hero, the photographic Reels bento, the formats accordion, the 9 steps grouped Diagnose / Produce / Scale, the dark emerald AI band, the pricing + ROI split, FAQ, the giant bleed wordmark footer.

## E. Non-negotiables (re-check at the end)
- Everything in BRIEF.md "Content that must exist" and "Brand constraints". Text wordmark only (no crest). Only phone number +91 81128 59437; every WhatsApp action → wa.me/918112859437. Never the words Guggy, Sahil, Indrajeet. Official app logos next to handles/phone/email.
- Every visible text node has a data-hi translation; `setLanguageMode('hi')` then `setLanguageMode('en')` must restore the page exactly.
- All original function names kept: playVandanaViralReel, closeVandanaViralReel, setLanguageMode, switchPhoneSimulation, updateROICalc, startHindiVoiceInput, sendZeroTouchWhatsApp, downloadZeroTouchFile, speakWelcomeGuide, speakVandanaTestimonial, speakGeneratedPlan, openElegantWhatsAppDirect, selectPackageInForm, toggleSurfaceTheme (dark mode).
- No horizontal scroll at any width 320–1920 in either theme or language. No page errors. Heights: desktop ≤ 9,500 px, mobile ≤ 13,500 px.
- Respect prefers-reduced-motion. Keep blur/backdrop-filter to ≤ 10 elements on mobile.

## Tools
- Screenshots: `node WEB/shoot.js WEB/final WEB/final/shot` (desktop/mobile fold + full). For dark mode / Hindi / other widths, write your own Playwright script (`require('/opt/node22/lib/node_modules/playwright')`). Crop tall PNGs before reading them (ImageMagick).
- Acceptance checker: `node WEB/verify.js WEB/final` must end with FAIL 0 (WARNs are reviewed by hand).
