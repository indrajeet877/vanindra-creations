# Master LLM Prompt Pack (Copy-Paste Into Any LLM)

Indrajeet: Since you mentioned *"I'll be using other LLM, I will create everything in that pipe"*, here is the **complete 4-Prompt Master Pipeline**. Whenever a new 100K+ lead or client comes in, copy-paste these prompts in sequence into any LLM (Gemini, Claude, ChatGPT) to generate their entire strategy, calendar, scripts, and captions!

---

## PROMPT 1: The "100K+ Prospect Free Audit & 5 Hook Generator" (Use During Outreach)
*Use this when Guggy or Sahil finds a 100K+ influencer and wants to send them a jaw-dropping free audit in 2 minutes.*

```markdown
You are India's top Short-Form Content Strategist for 100K–500K Instagram Influencers.
Analyze the following Indian influencer profile and create a 1-Page "High-Retention Content Audit & 5 Viral Reel Hooks" document that we can send them as a gift.

[INFLUENCER DETAILS]
- Name & Handle: {{Name_and_Handle}}
- Follower Count: {{Followers}}
- Niche / Category: {{Niche}}
- Language / Tone: {{Hindi / Hinglish / English}}
- Recent 5 Reel Topics & Views: {{Paste_Recent_Topics_or_Observations}}
- Main Weakness We Noticed: {{e.g., slow first 3 seconds, inconsistent topics, plain editing, no clear CTA}}

[OUTPUT FORMAT REQUIRED]
1. **Quick Compliment & Strengths (2 bullets):** Genuine praise for their current authority/audience.
2. **The 2 Hidden Growth Leaks:** Explain clearly why their views or brand readiness are being held back right now.
3. **"What To Post vs. What NOT To Post" Matrix:** A 4-row table showing exact content types they should stop posting vs. start posting immediately.
4. **5 Ready-to-Shoot Viral Reel Concepts:** For each concept, provide:
   - **Visual On-Screen Text Hook (0–3 sec)**
   - **Spoken Opening Line (in natural {{Hindi/Hinglish/English}})**
   - **Core Value / Twist (15–35 sec)**
   - **Engagement CTA (Comment trigger)**
Keep the tone warm, insider, sharp, and 100% tailored to the Indian Instagram ecosystem.
```

---

## PROMPT 2: The "Client Onboarding Brand Bible — What To Post & What NOT To Post"
*Use this as soon as a 100K+ Influencer fills out our Website Requirement Form.*

```markdown
You are the Chief Content Strategist at our Influencer Growth Agency. A new 100K+ Indian influencer client just submitted their onboarding requirements. Create their complete **"Brand Voice & Content Pillars Bible"** (save output to `01_Onboarding_and_Brand_Voice.md`).

[CLIENT INTAKE DATA]
- Creator Name & Handle: {{Name_and_Handle}}
- Followers & Current Avg Views: {{Followers_and_Views}}
- Niche & Target Audience in India: {{Niche_and_Audience}}
- Language Preference: {{Hinglish / Hindi / English}}
- How They Monetize (or want to monetize): {{Brand deals / Coaching / Clinic / Products / YouTube}}
- Creator's Biggest Frustration: {{What they wrote in the form}}
- 3 Creators They Admire: {{Competitors_or_Inspirations}}

[GENERATE THE FOLLOWING]
1. **Positioning Statement & Bio Upgrade:** 3 high-converting Instagram Bio options (including brand-friendly authority positioning).
2. **The 4 Core Content Pillars (with % split):**
   - Pillar 1: Viral Reach / Broad Relatability (40%)
   - Pillar 2: Deep Niche Authority / Saveable Value (30%)
   - Pillar 3: Personal Story / Trust & Connection (20%)
   - Pillar 4: Brand-Ready / Monetization / Case Studies (10%)
3. **Strict "What To Post vs. What NOT To Post" Rules:**
   - 5 specific topics/formats to NEVER post on the main grid (and why they hurt reach).
   - 5 high-retention formats to post every week.
4. **Visual & Editing Style Guide (for our editor Akarsh Yadav):** Pacing, caption style, color vibe, B-roll types, and thumbnail rules.
```

---

## PROMPT 3: The "30-Day High-Retention Content Calendar Generator"
*Run this right after Prompt 2 in the same LLM chat to build their `02_Monthly_Content_Calendar.md`.*

```markdown
Based on the Brand Bible above for {{Name_and_Handle}}, generate a structured **20-Reel Monthly Content Calendar** (5 Reels per week for 4 weeks).

For every single Reel (#1 to #20), output a Markdown table with these exact columns:
1. **Reel # & Day**
2. **Content Pillar** (Reach / Authority / Story / Brand-Ready)
3. **Format Type** (Myth-Buster / Green Screen Breakdown / Storytime / 3-Step Listicle / Before-After / Skid-Relatable)
4. **Working Title / Core Topic**
5. **The 3-Second Scroll-Stopper Hook (Spoken + Visual Text)**
6. **Why This Will Work for Their 100K+ Audience**

Make sure the topics are hyper-relevant to India in 2026, avoid generic textbook clichés, and balance viral shareability with sponsor-friendly authority.
```

---

## PROMPT 4: The "Batch Word-for-Word Script, B-Roll & Caption Writer"
*Use this weekly (for 5 Reels at a time) to generate the files inside `03_Scripts_and_Hooks/`.*

```markdown
Now write the complete **Production-Ready Shoot & Edit Pack** for Reels {{e.g., #1 to #5}} from the calendar above for {{Name_and_Handle}} in natural {{Hinglish / Hindi / English}}.

For EACH Reel, use this exact template so the Creator knows exactly how to shoot it in 10 minutes, and our Editor (Akarsh Yadav) knows exactly how to edit it:

---
### 🎬 REEL #[X]: [Topic Name]
- **Target Duration:** [30–45 seconds]
- **Energy / Vibe:** [e.g., Fast & punchy / Calm authority / Warm storytime]
- **On-Screen Thumbnail / Cover Title (3–4 Words Max):** [Text]

#### 🗣️ WORD-FOR-WORD SCRIPT & EDITING CUES:
- **[0:00 – 0:03 | THE HOOK]**
  - *Spoken Line:* "..."
  - *Visual / Camera Action:* [e.g., Start mid-action holding X / Close-up zoom]
  - *Editor Note (Akarsh):* [On-screen hook banner + sound effect]
- **[0:03 – 0:15 | THE AGITATION / TWIST]**
  - *Spoken Line:* "..."
  - *Editor Note (Akarsh):* [B-roll overlay or split-screen graphic]
- **[0:15 – 0:35 | THE VALUE PAYOFF (3 Crisp Points)]**
  - *Spoken Line:* "..."
  - *Editor Note (Akarsh):* [Pop-up numbered list 1, 2, 3]
- **[0:35 – 0:42 | CALL TO ACTION / LOOP]**
  - *Spoken Line:* "..."

#### 📝 INSTAGRAM CAPTION, TAG & HASHTAGS:
- **First Line (Curiosity Hook):** ...
- **Body (3–4 short scannable lines):** ...
- **Agency Attribution Footer:**
  ✨ *Content Strategy & Edit by @[AgencyHandle]*
- **8 Niche SEO Hashtags:** ...
- **Pinned Comment to Post Immediately:** ...
---
```
