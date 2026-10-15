# VanIndra homepage: 4 new "Crystal" variations of Liquid Glass

SCRATCH = /tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad
WEB = SCRATCH/web2

## What the owner and team said
After seeing the three styles, the team liked **Style 3, Liquid Glass** (`WEB/d3_liquid_glass/index.html`; screenshots `WEB/d3_liquid_glass/shot_*.png`). They want **4 more variations, every one better than Liquid Glass**:
> "more crystal and minimalist and more focused ... cleaner. Check other possibilities."

So: **crystal** (clear, light, precise glass, light refraction, sharp specular edges, not a foggy blur), **minimalist** (fewer elements, more space, fewer colours, fewer badges, shorter copy), **focused** (one idea and one primary action per screen; the eye always knows where to go), **cleaner** (calm alignment, no clutter, no decorative noise, no gradient text). The 4 variations must be clearly different from each other, so the team has a real choice.

## Start from Liquid Glass and fix what the judges said
Start from a copy of `WEB/d3_liquid_glass/index.html`. It already has every feature and the best honesty copy. Then redesign it. Every Liquid Glass weakness the judges named must be gone in every variation:
- The WhatsApp logo vanished on green buttons. Use the official green WhatsApp logo on a white/ivory or dark button, or a white glyph in a contrasting white circle, so it is clearly visible.
- No gradient text on headings (no muddy olive). One ink colour for the "VanIndra" wordmark.
- At 1440×900 the product (phone with its Before/After toggle) and the primary CTA must be **above the fold**. Liquid Glass showed only centred text there.
- No more than **8 elements with backdrop-filter on mobile** (≤ 768 px). Use solid translucent fills elsewhere, and turn blur off under `prefers-reduced-transparency`. No full-page animated mesh on mobile.
- No invented engagement counts in the phone (no likes/comments/shares numbers). KPI chips must never cover the face or the Reel UI.
- Section heads aligned on one consistent axis.
- No dead gaps in the founder tile. Services must not be a generic 3×2 card grid; show the work (a micro-UI) or use a calmer list.
- The Hindi H1 must not use a fake oblique Devanagari, and must not break into 4+ lines or leave an orphan word at 390 px.
- Pricing: "Recommended" instead of "Most popular". VIP: "By application", not "Waitlist · limited to 1 client". On mobile, Pro Growth (₹24,999) is visible without swiping.
- Tap targets ≥ 44 px (goal chips, language buttons, footer links).
- No pitch-deck link anywhere on the page (it is an internal playbook). Keep the links to `login.html` and `thumbnail-studio.html`.
- ROI calculator: show reach and time saved. If a ₹ range is shown, label it "Rough illustration, not a promise of income" in readable contrast.

## Honesty and brand rules (all variations)
Apply `WEB/FINAL_SPEC.md` section B (the honesty rules) and section E (non-negotiables), plus `WEB/BRIEF.md`. In short:
- Text wordmark only (no crest).
- Sole public founder: Vandana Yadav. Official full names: Smita Yadav, Akarsh Yadav. Never write Guggy, Sahil or Indrajeet.
- Only one phone number, +91 81128 59437. Every WhatsApp action goes to wa.me/918112859437.
- Official app logos next to handles, phone and email.
- No fake testimonials, no guaranteed results.
- Illustrations are labelled "Illustration — not a client result".
- Stats carry dates ("50K+ followers · Oct 2026").
- English by default, with a working Hindi `data-hi` toggle that round-trips exactly.
- Ivory is the default surface, plus a 1-click Dark Studio Mode (`toggleSurfaceTheme`).
- Keep all original JS function names: playVandanaViralReel, closeVandanaViralReel, setLanguageMode, switchPhoneSimulation, updateROICalc, startHindiVoiceInput, sendZeroTouchWhatsApp, downloadZeroTouchFile, speakWelcomeGuide, speakVandanaTestimonial, speakGeneratedPlan, openElegantWhatsAppDirect, selectPackageInForm, toggleSurfaceTheme.
- No horizontal scroll from 320 to 1920 px in either theme or language. No page errors.
- `prefers-reduced-motion` is respected.
- Height budget (more focused means shorter): desktop ≤ 8,500 px, mobile ≤ 11,500 px.

## The 4 variations
- **v1_crystal (Pure Crystal):**
  - The purest version of Liquid Glass: an almost colourless crystal look.
  - Bright ivory/white canvas with huge whitespace and a split hero (copy left, a crystal phone right).
  - Panels look like cut glass: a crisp 1px specular top edge, a faint inner light, low blur (≤ 12px) and a very soft shadow.
  - Emerald is the only ink colour, and gold is used for exactly one detail per screen.
  - One primary CTA per section. The calmest, most premium option.
- **v2_prism (Prism):**
  - Swiss-minimal and monochrome: near-white, hairlines, a strict 12-column grid, and a crisp grotesk only (e.g. Geist / Inter Tight, tight tracking, no serif).
  - The single colour moment is a faint prism light dispersion, a thin rainbow edge on the hero glass phone and on the one active element. It nods to Indradhanush (Indra's rainbow) and must be very subtle.
  - Extremely focused copy: short headlines, short sentences.
- **v3_vision (Vision):**
  - Apple visionOS / spatial UI: soft depth with floating glass "windows" over a calm ambient background, made from one real Reel cover blurred heavily into soft light (`assets/portfolio/*.jpg`; keep it subtle and readable).
  - Pill tab bars, ornaments, and segmented controls for sections such as Reels / Formats / Services, so the page shows one window of content at a time instead of long stacks.
  - Feels like an app, not a website.
- **v4_focus (Focus Story):**
  - Apple product-page storytelling, with one idea per screen.
  - The crystal phone stays pinned (sticky) while short scenes scroll past it: raw clip → hook banner → captions → delivered (the Before/After simulator becomes the story), then proof, then the offer.
  - Big statements, very short text. Long content (formats, 9 steps, FAQ, services detail) goes into compact expandable glass drawers.
  - The most focused and shortest page.
  - Must still work perfectly on mobile, where the sticky scenes become a simple vertical sequence with no scroll-jacking.

## Deliverables per variation (in WEB/<id>/)
- `index.html`: single self-contained file; `assets/` is symlinked in your folder.
- Screenshots via `node WEB/shoot.js WEB/<id> WEB/<id>/shot`, plus your own Playwright shots in `WEB/<id>/qa/`: dark mode at 1440 and 390, Hindi at 390, and 320 px.
- `WEB/<id>/preview.png`: one image for the team email, containing the desktop fold (1440×900 scaled to 960 wide) and the mobile fold (390×844) side by side on a neutral background, with the variation name written small at the top.
- `node WEB/verify.js WEB/<id>` must report FAIL 0.
