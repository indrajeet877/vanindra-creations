# Private Repo + Public Website on Cloudflare Pages (Free)

> **Status (Oct 2026):** the GitHub repository is **private**. GitHub Pages is now off, so the old `indrajeet877.github.io` address no longer works (and must never be used again). The website moves to **Cloudflare Pages**: free, unlimited bandwidth, fast in India, free HTTPS, and it works with private repos.
> **Who does this:** the repository owner (needs to log in to GitHub). Time: about 10 minutes, plus about a day for a new domain to go live.

## What gets published (and what never does)
`scripts/build_public_site.sh` copies **only** these into the website:
- `index.html`, `login.html`, `pitch-deck.html`, `thumbnail-studio.html`
- `assets/` (portfolio images)
- `site_config/_headers` (security headers) and `site_config/robots.txt`

Everything else (all numbered folders, CLAUDE.md, pricing, scripts, lead sheets, logo proposals) stays private. The build **refuses to deploy** if any public page contains:
- a family nickname or a background team member's name
- a phone number other than the official WhatsApp `+91 81128 59437`
- a non-website file (for example a `.md` or `.csv` dropped into `assets/`)
- a broken local link or image

To add a new public page later, add its filename to `PUBLIC_PAGES` in that script.

---

## Step 1 — Create the Cloudflare Pages project (about 5 minutes)
1. Sign up or log in at **dash.cloudflare.com** (free plan; use the business Gmail).
2. In the left menu, open **Workers & Pages**, click **Create**, choose the **Pages** tab, then **Connect to Git**.
3. Click **Connect GitHub**. When GitHub asks which repositories to allow, choose **Only select repositories**, then **vanindra-creations**, then **Install & Authorize**. This gives Cloudflare read access to this one private repo only.
4. Select **vanindra-creations**, then **Begin setup**.
5. Fill in exactly:

| Field | Value |
| :--- | :--- |
| Project name | `vanindracreations` (this becomes `vanindracreations.pages.dev`) |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `bash scripts/build_public_site.sh` |
| Build output directory | `dist` |
| Root directory | *(leave empty)* |

6. Click **Save and Deploy**. After about 1 minute the site is live at **https://vanindracreations.pages.dev**.

If the name `vanindracreations` is already taken, Cloudflare adds a suffix. Send the exact address so every link in the docs can be updated.

### Preview before going live (approval-first)
Cloudflare also builds every **other branch** as a private preview link, for example the work branch `claude/stoic-tesla-l103vu`. Open it from **Workers & Pages → vanindracreations → Deployments**, check it on your phone, and merge into `main` only when happy. Merging to `main` updates the live site automatically.

---

## Step 2 — Connect `vanindracreations.in` (about 5 minutes, plus DNS time)
1. **Buy the domain** if you haven't already: `vanindracreations.in` (and `vanindracreations.com` to protect the name) from an Indian registrar such as Hostinger, GoDaddy or BigRock, roughly ₹500–₹900 a year each. Cloudflare's own registrar may not sell `.in`, so buy it elsewhere.
2. In Cloudflare: **Add a domain**, enter `vanindracreations.in`, choose the **Free** plan, and note the **2 nameservers** Cloudflare shows.
3. At the registrar: open the domain's **Nameservers** setting, choose **custom**, paste Cloudflare's 2 nameservers and save. This usually takes 15 minutes to a few hours, at most 24.
4. Back in **Workers & Pages → vanindracreations → Custom domains**: add `vanindracreations.in`, then add `www.vanindracreations.in`. Cloudflare creates the DNS records and HTTPS certificate itself.
5. Optional, for the global site later: add `vanindracreations.com` to Cloudflare the same way. Until the separate global site exists, use **Rules → Redirect Rules** to send `.com` to `https://vanindracreations.in`.

---

## Step 3 — After it's live
- [ ] Update the Instagram bio link on `@vanindracreations`, `@vandanay2012` and `@smitayadav_0901` to the new address.
- [ ] Once the domain works, replace `vanindracreations.pages.dev` with `vanindracreations.in` across the docs. (Claude can do this in one step: just say "domain is live".)
- [ ] Check in GitHub → **Settings → Pages** that GitHub Pages shows as disabled or unpublished.
- [ ] Keep the repository **private**. Never switch it back to public; the public website no longer needs it.

## Netlify (backup option)
If Cloudflare is ever unavailable: Netlify → **Add new site → Import from Git → GitHub → vanindra-creations**. The included `netlify.toml` already sets the build command and the `dist` folder.
