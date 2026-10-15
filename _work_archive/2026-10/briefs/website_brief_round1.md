# VanIndra Creations — Website Redesign Brief

SCRATCH = /tmp/claude-0/-home-user-vanindra-creations/704148cb-74ad-5713-93e9-04b0ce97a9f0/scratchpad
- Current live page (source of ALL content and features): SCRATCH/web2/current_index.html (≈3,700 lines; read it in parts). Also /home/user/vanindra-creations/login.html, pitch-deck.html, thumbnail-studio.html for linked pages.
- Screenshots of the current page: SCRATCH/web2/current_desktop_*.png, current_mobile_*.png. LOOK at them first.
- Screenshot tool: `node SCRATCH/web2/shoot.js <your_dir> <your_dir>/shot` (serves your folder; `assets/` is symlinked to the real portfolio images). Read the PNGs with the Read tool. Full-page PNGs are tall: crop them first (ImageMagick `convert in.png -crop 1440x2400+0+0 out.png`, or `-resize 50%`).
- CLAUDE.md in the repo has the brand rules (auto-loaded).

## The problem
The owner says: "Front end still I don't like. Fix this, work more. Why don't you use some beautiful frontend design which is popular on X?" The current page is crowded: emoji everywhere, many inline-styled boxes, too many competing badges, long walls of text, a cartoonish 3D crest logo, everything shouting at once. It looks like a template, not a premium studio.

## What "popular on X" means here (design Twitter, 2025–26)
Pick from these and execute them with taste, never all at once:
- **Bento grids**: asymmetric rounded tiles mixing big numbers, photos (Reel covers), short copy and micro-UI.
- **Editorial type pairing**: a big expressive serif display (e.g. Instrument Serif, Fraunces, Cormorant Garamond), often italic for one or two words, plus a crisp grotesk (Geist, Inter Tight, Manrope, Bricolage Grotesque). Tight tracking on big type, generous whitespace.
- **Aurora / mesh glow** behind the hero, a subtle **grain/noise** layer, **hairline 1px borders** and soft inner glows (Linear, Vercel, Raycast).
- **Glass** panels (backdrop-filter blur) used sparingly (Apple "Liquid Glass").
- **Product-as-hero**: a real phone mockup playing the Reel cover, floating UI chips.
- **Logo/marquee strips**, **stats rows**, **testimonial walls** (only with REAL proof), **sticky scroll storytelling**, **micro-interactions** (hover tilt, magnetic buttons, subtle reveal-on-scroll with IntersectionObserver; respect prefers-reduced-motion).
- **Pricing cards** with one highlighted plan, toggle chips, clean check lists.
- **Big, calm CTA** sections; floating pill nav that shrinks on scroll.
- No emoji as decoration (at most 1–2 meaningful ones); real SVG icons drawn inline (lucide-style strokes).

## Brand constraints (non-negotiable)
- Palette (from CLAUDE.md): Warm Ivory `#FAF8F3` / Alabaster `#FFFFFF`, Deep Studio Emerald `#09241B` / `#0E6B4E`, Imperial Gold `#D4A024` / `#F4C44E`. You may add near-neutrals and tints derived from these. Gold is an accent, not a fill for everything.
- **Logo**: the old 3D crest is REJECTED and a new logo is not approved yet. Use a refined TEXT wordmark only ("VanIndra" + small "CREATIONS"), no crest image.
- Golden Rules: Vandana Yadav (@vandanay2012, 50K+ followers, 467+ posts) is the SOLE public founder; Smita Yadav (@smitayadav_0901, official WhatsApp +91 81128 59437, smitayadav497@gmail.com, B.Com Gargi College DU) and Akarsh Yadav (@yadavakarsh_07, akarshgkp8756539282@gmail.com, B.Voc Food Technology, University of Allahabad) with official full names only. NEVER the words Guggy, Sahil, Indrajeet; NEVER any phone number except +91 81128 59437. All WhatsApp CTAs go to wa.me/918112859437.
- Official app logos (Instagram gradient, WhatsApp green, Gmail) next to handles, phone and email (inline SVGs exist in the current page; reuse them).
- English by default. Hindi/Hinglish toggle must work: every visible text node that has a `data-hi` translation in the current page must keep it (`data-hi="..."`); the toggle swaps innerHTML (see `setLanguageMode` in the current page).
- Mobile-first: most visitors are Indian creators on phones (390 px). No horizontal scroll at any width 320–1920. Tap targets ≥ 44 px. Sticky bottom bar on mobile with WhatsApp + Free AI Plan.
- Real content only. The current page's three 5-star testimonials are invented personas — do NOT present them as real client reviews. Replace that section with real proof (the two live portfolios @vandanay2012 and @smitayadav_0901, the 6 real Reels, founder story) or clearly labelled "example outcomes".
- Keep honest wording: no guaranteed views/followers.
- Single self-contained `index.html` (inline CSS + JS). Google Fonts allowed. Optional small libraries from cdnjs only (e.g. GSAP) — prefer none. Images: `assets/portfolio/*.jpg` (6 showcase Reels: reel_DZSZW2ey529, reel_Ddl3VLbu4P5, reel_Dds1foTyrQm, reel_DSZ8VilkrA8 from @vandanay2012; reel_DedHDrLgY43, reel_Da0liqXAemF (plays Da0lVfrAa47) from @smitayadav_0901; dp_vandanay2012.jpg, dp_smitayadav_0901.jpg).

## Content that must exist on the page (order and grouping are yours)
Nav (Portfolio, Reels, Services, How it works, Pricing, Team, Client Login, WhatsApp CTA) · Hero (value proposition: AI + human content studio for 1 lakh+ creators, doctors, coaches and brands — strategy, viral hooks/scripting, high-retention 9:16 editing, brand-deal positioning, without the daily operations) with WhatsApp concierge (editable message → wa.me) and a phone mockup Before/After simulator · Founder Vandana Yadav story + live portfolios #01 @vandanay2012 and #02 @smitayadav_0901 + "Your profile next" slot #03 · 6 Viral Reels showcase with inline Instagram embed player (playVandanaViralReel/closeVandanaViralReel) · Viral formats & brand-deal engine (sponsorship desk) · Services (6) · How it works (the framework/steps) · Client portal preview (link to login.html) · Free AI Growth Plan generator (form + voice mic + generation; keep the existing JS behaviour: pollinations API with fallback, WhatsApp send, download) · Team (3 cards with app-logo contact rows) · Pricing (Trial ₹2,999 one-time; Starter ₹14,999/mo; Pro Growth ₹24,999/mo highlighted; 360° VIP ₹39,999/mo) + ROI calculator · FAQ · Footer · links to login.html, pitch-deck.html, thumbnail-studio.html.
NOTE: current mobile page is ~29,000px tall
