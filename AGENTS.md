# AGENTS.md — Instructions for Muse, OpenAI Codex, Antigravity, Claude & Autonomous Agents

This repository (`VanIndra Creations`) is architected so that **Indrajeet Yadav** can switch seamlessly between **Antigravity (Gemini)**, **Claude**, **Muse**, **Cursor**, or any other LLM/agent at any time without losing a single detail.

## 1. Golden Rules for Every Agent Working in This Folder
1. **Read `CLAUDE.md` and `00_MASTER_BLUEPRINT.md` First:** Never ask the user who the team members are—they are **Indrajeet Yadav**, **Vandana Yadav (`@vandanay2012`)**, **Smita "Guggy" Yadav (`@smitayadav_0901`, `8112859437`, `smitayadav497@gmail.com`)**, and **Akarsh "Sahil" Yadav (`@yadavakarsh_07`, `9415259408`, `akarshgkp8756539282@gmail.com`)**.
2. **Never Make Designs Boring:** Always use the **VanIndra Creations Signature Palette** — Obsidian Slate (`#0D1014`), Carbon Titanium (`#161B22`), Brushed Silver (`#CBD5E1`), Imperial Gold (`#E5B84B`), and Studio Emerald (`#124E37` / `#10B981`). Every UI, thumbnail, or micro-site must look like a ₹100-Crore Indian Media & Creator Studio.
3. **Standard Operating Workflows for Common User Requests:**
   - **"Onboard a new 100K+ client named [X]":**
     1. Duplicate `06_Client_Workspace_Template/_TEMPLATE_Influencer_Name_100K` into `06_Client_Workspace_Template/[ClientName_@Handle]`.
     2. Run the prompts in `05_Content_Factory_and_LLM_Prompts/02_Master_LLM_Prompt_Pack.md` to populate their `01_Onboarding_and_Brand_Voice.md`, `02_Monthly_Content_Calendar.md`, and `03_Scripts_and_Hooks/Week_01_Scripts.md`.
   - **"Generate a Free 7-Day Audit for prospect [@handle]":**
     1. Run **Prompt #1** from `05_Content_Factory_and_LLM_Prompts/02_Master_LLM_Prompt_Pack.md`.
     2. Save the output in `04_Outreach_and_Sales_Pipeline/Prospect_Audits/Audit_[@handle].md` and add a row to `02_Market_Research_and_ICP/02_Target_Influencer_Lead_Sheet.csv`.
   - **"Build a new niche landing page / micro-website":**
     1. Check `09_Tech_Handles_Domains_Servers_and_Apps/01_Handles_Domains_Servers_and_Apps_Master_Plan.md` for our multi-site architecture.
     2. Reuse the design tokens and WhatsApp routing (`918112859437` for Guggy / `919415259408` for Sahil) from `index.html`.
   - **"Work on the Mobile/Web App":**
     1. Follow the App Architecture Spec in `09_Tech_Handles_Domains_Servers_and_Apps/01_Handles_Domains_Servers_and_Apps_Master_Plan.md`.
