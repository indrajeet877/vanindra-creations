# Multi-Terminal CLI Handoff & Deep Audit Guide
## For Claude Code (Opus 5.5), Gemini CLI (Gemini 4 Argon High + Free Credits) & Meta Muse

> **Workspace Path:** `/Users/vanindra/Downloads/Influencer  Agency`
> **Live Production URL:** `https://indrajeet877.github.io/vanindra-creations/`
> **GitHub Repository:** `https://github.com/indrajeet877/vanindra-creations.git` (`main` branch)

---

## 1. How to Launch Each Agent in This Folder

### A. Claude Code Terminal (`Opus 5.5` — Best for Deep Code & UX Auditing)
```bash
cd "/Users/vanindra/Downloads/Influencer  Agency"
claude --model claude-opus-5-5
# Or inside an active Claude Code session:
# /model opus
```
*(Claude Code automatically reads `CLAUDE.md` and `AGENTS.md` in the root folder the moment it starts.)*

### B. Gemini CLI (`Gemini 4 Argon High` — Leverage Free Gemini Credits for Mass Audits, Scripts & Lead Research)
```bash
cd "/Users/vanindra/Downloads/Influencer  Agency"
gemini
# Or specify model flag if supported by your CLI profile:
# gemini --model gemini-4-argon-high
```
*(Gemini CLI automatically loads `GEMINI.md` and `AGENTS.md` on startup.)*

### C. Meta Muse / Cursor / Codex CLI
```bash
cd "/Users/vanindra/Downloads/Influencer  Agency"
# Open workspace and point to AGENTS.md + 00_MASTER_BLUEPRINT.md
```

---

## 2. Current State of the Codebase (As of Commit `c1f95a4`+)

1. **100% English Default + Full-Page Bilingual Toggle (`index.html`):**
   - English (`#btnLangEn`) is active by default across the entire page so zero unintended Hindi text appears when English is selected.
   - Clicking `हिंदी / Hinglish` (`#btnLangHi`) dynamically switches every `[data-hi]` element, `[data-placeholder-hi]` input, 3D iPhone Simulator caption, and ROI Calculator label to Hindi/Hinglish and back.
2. **Sleek Auto-Hiding Deep Studio Emerald & Gold Header (`#stickySiteHeader`):**
   - Single-line Emerald Glass header (`background: rgba(5, 22, 16, 0.94); white-space: nowrap`) that automatically slides out of view (`.header-hidden`) when scrolling down past `180px` and reappears immediately when scrolling up.
3. **Non-Overlapping 3D iPhone Simulator (`#iphone3D`):**
   - Widened `.dynamic-notch` (`width: 136px; white-space: nowrap`) and docked `#chipRetention`, `#chipViews`, and `#chipSponsor` into a clean 3-column `.phone-kpi-dock` inside the screen so zero elements overlap.
4. **Curated 6-Reel Flagship Showcase (`#viral-reels-showcase` — No Page Flooding & Zero Play-Button Watermarks):**
   - Uses clean 9:16 vertical covers (`assets/portfolio/reel_*.jpg`) fetched via Instagram's `/p/<shortcode>/media/?size=l` endpoint (no burned-in gray play icon).
   - Displays **6 curated high-impact cards** in a 3-column grid:
     - **4 Top 100K+ Viral Hits from Founder Vandana Yadav (`@vandanay2012`):** `DZSZW2ey529` (*"Ye 5 mins kaam karte hi..."*), `Ddl3VLbu4P5` (*"Arrey chahiye kya AURAT ko???"*), `Dds1foTyrQm` (*"Jab main apne pati ko unke gharwalon ki galti dikhaun"*), and `DSZ8VilkrA8` (*"Naya saal ❌. Naya janam ✅"*).
     - **2 Featured Youth & Lifestyle Reels from Client Portfolio #02 Smita Yadav (`@smitayadav_0901`):** `DedHDrLgY43` (*"Dandiya Night & Desi Vibes ✨"*) and `Da0lVfrAa47` (*"A Special Kind of Therapy ✨"*).
5. **6-Stream Viral Monetization & Brand Deals Engine:**
   - Documented in `03_InHouse_Content_Flywheel/04_Aggressive_Viral_Growth_and_Brand_Deals_Playbook.md`.
   - Integrated on `index.html` (6 Viral Deal-Magnet Formats + Official Brand Sponsorship Desk) and `pitch-deck.html` (Slide 08: 6-Stream Monetization & Official Brand Rate Card).

---

## 3. Copy-Paste Master Prompt (For Claude Opus 5.5, Gemini 4 Argon High & Meta Muse)

Copy and paste the block below into your new terminal session:

```text
You are the Principal Growth, UI/UX & Full-Stack Auditor for VanIndra Creations working in `/Users/vanindra/Downloads/Influencer  Agency`.

STEP 1 — LOAD CONTEXT & GOLDEN RULES FIRST:
Read `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `00_MASTER_BLUEPRINT.md`, and `03_InHouse_Content_Flywheel/04_Aggressive_Viral_Growth_and_Brand_Deals_Playbook.md`.
Strictly enforce these non-negotiable rules on every public file (`index.html`, `login.html`, `pitch-deck.html`, `thumbnail-studio.html`):
1. Vandana Yadav (`@vandanay2012`, 50K+ followers, 467+ posts) is the SOLE Public-Facing Founder & Chief Influencer Director (and Flagship Client Portfolio #01).
2. Smita Yadav (`@smitayadav_0901`, `+91 81128 59437`, `smitayadav497@gmail.com`, B.Com Gargi College DU — Client Portfolio #02 & Single Official WhatsApp Concierge) and Akarsh Yadav (`@yadavakarsh_07`, `akarshgkp8756539282@gmail.com`, B.Voc Food Tech, Univ. of Allahabad) are presented publicly with their official full names ONLY.
3. NEVER display family nicknames ("Guggy" or "Sahil") or Indrajeet Yadav's name or a second WhatsApp number on any public HTML page.
4. Keep the Viral Reels Showcase curated to the 6 flagship Reels (top 4 100K+ viral hits from `@vandanay2012` + 2 featured Reels from `@smitayadav_0901`) without flooding the page.

STEP 2 — RUN FULL MULTI-FILE AUDIT & HEALTH CHECK:
1. Check `~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite` (read-only) for the `Vanindra Creation Team` group (`Z_PK = 1336`) to see if any new team feedback arrived.
2. Audit `index.html`, `login.html`, `pitch-deck.html`, and `thumbnail-studio.html` for:
   - Golden Rule compliance (`grep -iE "indrajeet|guggy|sahil|9415259408" *.html` must return 0 matches).
   - 100% English default mode (`setLanguageMode('en')`) with zero stray Devanagari outside `data-hi` attributes and the language toggle button.
   - Mobile & desktop visual polish, sticky header scroll behavior, 3D iPhone simulator layout, and clean watermark-free Reel cover images in `assets/portfolio/`.
3. Leverage free Gemini / LLM credits to generate any requested 7-Day Prospect Audits (`04_Outreach_and_Sales_Pipeline/Prospect_Audits/`), D2C Brand Sponsorship Pitches, or Daily Viral Scripts.
4. Always sync `index.html` to `07_Website_and_Client_Portal_Spec/index.html`, commit cleanly, and push to `origin main`.
```
