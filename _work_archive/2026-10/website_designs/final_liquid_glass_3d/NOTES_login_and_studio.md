# Client portal + cover studio: Liquid Glass redesign

Both pages are self-contained HTML files. Everything is inline except Google Fonts. There are no CDNs, no GSAP and no three.js. The pages use the same tokens, fonts, glass, buttons, nav pill, EN/हिं switch, Dark Studio Mode, footer and official app-logo SVGs as `base_liquid_glass/index.html`. They are built from `_work/*` by `python3 _work/build.py`.

| File | Size | Inline JS |
|---|---|---|
| `login.html` | 138 KB | 41.5 KB (limit 120 KB) |
| `thumbnail-studio.html` | 114 KB | 47.3 KB |

## Proof

- **`node verify_pages.js`:** **PASS 144 / WARN 0 / FAIL 0.** The last three runs, made after the final build, all passed.
  - **Loop 1:** found 6 failures:
    - the theme toggle could wait on a View Transition;
    - after a signup, logout left the signup tab open;
    - 4 test-side issues.
  - **Loops 2–3:** all failures fixed, and the suite passed.
- **Screenshots:** `qa/` holds 31 PNGs:
  - auth view and dashboard at 1440 and 390, each in light, dark and Hindi;
  - the studio with an uploaded photo at 1440 and 390, in light, dark and Hindi;
  - 320 px versions of both pages;
  - no-JS and reduced-motion captures.
- **Videos** (H.264, CRF 26), each with a `frames_*.png` 12-frame contact sheet:
  - `login_desktop.mp4`: 17 s;
  - `login_mobile.mp4`: 16 s, 390×844 with touch;
  - `studio_desktop.mp4`: 13 s.
- **`preview.png`:** login desktop fold, login mobile fold and studio desktop fold.

## login.html: what changed

- **Auth view.** On the left: the headline "Every Reel, approval and brief — *in one calm place.*", using the same two-tone serif italic as the homepage, followed by three feature rows and an honesty note. On the right is a 3D glass sign-in panel:
  - It tilts toward the pointer (6°), and a specular glare follows the pointer.
  - A tinted "slab" sits 26 px behind the panel, so the panel shows real thickness when it turns.
  - Two glass chips float at +70 and +90 px depth.
  - Behind the panel are a CSS glass orb (emerald, plus a small gold one) with a slowly turning caustic and a thin gold/emerald orbit ring.
  - Everything is CSS 3D. There is no WebGL.
- **Tabs and buttons.** The Log in / Create account tabs use the homepage's sliding glass thumb. "Preview the portal with sample data" is a full-width glass button.
- **Entrance.** Staggered rise plus a 3D tilt-in for the panel. It ends at about 1.1 s, uses pure CSS keyframes, and nothing waits on JS.
- **Dashboard.** It contains:
  - a dashed gold ribbon at the top: "Sample workspace — illustration, not a client result…";
  - a dark emerald welcome panel showing the name, handle, plan and creative QA by Vandana Yadav, with buttons for the cover studio, WhatsApp and Sign out;
  - per-plan deliverable tracking with animated progress bars (Starter 12, Pro Growth 20, Trial 3, Free audit, and a VIP waitlist note);
  - the Reel approval queue, with Approve buttons;
  - the "Send a raw video / request an edit" form, which opens WhatsApp;
  - shortcuts plus an "About this preview" note with "Forget preview data on this device";
  - the studio team with official Instagram, WhatsApp and Gmail logos.
- **Kept.** These functions keep the same names and behaviour: `approveReel`, `demoLogin`, `handleLogin`, `handleSignup`, `logoutClient`, `openDashboardForUser`, `submitClientBrief` and `switchAuthTab`.
  - The localStorage keys `vanindra_active_client` and `vanindra_client_accounts` are unchanged.
  - A saved session still opens automatically on load.
  - Dark mode uses the shared key `vanindra_theme` and `body.dark-studio`.
- **Small improvements.**
  - Logout returns to the Log in tab.
  - Login matches handles with or without "@", ignoring case.
  - Signing up twice with the same email or handle replaces the old account instead of duplicating it.
  - An unknown login says, in a toast, that it is showing a sample workspace.
  - The approve and switch-tab text stays bilingual, so the Hindi round trip is exact after you approve.

## Honesty changes (login)

- **Removed:**
  - "84.2% avg 3-sec hook hold", "+41% above baseline", "Live on IG" and the "3x My Reach" / "90% creators" hook titles.
  - "Free 7-Day Audit".
  - "Flagship Creator & Pro Growth Studio" used as a demo plan.
- **Demo identity.** The demo is now "Sample Creator (@your_handle)", not a real person's account.
- **The sample is labelled** in four places:
  - the ribbon;
  - the "Sample" tags;
  - the tracking note, which says we promise deliverables and deadlines, not views, followers or income;
  - "About this preview".
- **No server, said plainly.** The page states it three times, in both languages: there is no server, this is not a secure account, data stays in this browser on this device, and real workspaces are set up by the studio after onboarding and shared on WhatsApp.
- **No password fields.** A password the page never checks would imply security it does not have. The hint says: "No password in this preview — it only looks for accounts saved in this browser."
- **Plan dropdown.** It matches the homepage exactly:
  - Free page audit + a 15-second sample edit (free, and the default);
  - 3-Reel Trial Pack ₹2,999;
  - Starter 12 Reels/month ₹14,999;
  - Pro Growth 20 Reels/month ₹24,999 · Recommended;
  - VIP: Daily Reels, by application (waitlist). The VIP dashboard says no VIP payments are being taken yet.
- **One number.** The only phone number is +91 81128 59437, and every WhatsApp action goes to `wa.me/918112859437`.

## thumbnail-studio.html: what changed

- **Layout.** A premium glass creative app in four numbered steps: Photo (drop zone, drag and drop, thumbnail, Clear photo), Look (four visual swatches that drive the hidden `#themeSelect`), Words, and Credit.
- **Preview.** A sticky live preview sits in a thick 3D glass frame that tilts toward the pointer, with glare. It has a "Show profile-grid crop (3:4)" overlay and a gold "Download 1080×1920 PNG" button. Over the canvas, the cursor becomes a magnifying loupe.
- **Kept.** These functions keep their names: `clearPhoto`, `downloadThumbnail`, `handleImageUpload` and `renderThumbnail`. The canvas is still 1080×1920 and the file name is unchanged.
- **Better PNG typography.** Checked at 130 px, phone-grid size, in `_work/covers/small.png`:
  - Inter Tight is auto-fitted onto at most 2 lines, so long hooks no longer run off the canvas.
  - Hook line 2 is set in Instrument Serif italic in the accent colour, matching the homepage.
  - The badge and payoff are rounded pills.
  - With a photo, the overlay lets the face show at the top and darkens behind the words. The text block stays inside the 3:4 grid-safe zone.
  - Devanagari typed into the fields renders through Noto Sans Devanagari.
- **Logo and claims.**
  - The unapproved V-wing crest emblem was removed; the cover carries the text wordmark "VanIndra" only.
  - The default payoff "AND HOW WE FIX IT IN 7 DAYS" (a time promise) became "AND WHAT TO POST INSTEAD".
- **UI labels.** They are in Hindi via `data-hi`. The canvas text is whatever the user types.

## Effects and how they degrade

| Effect | Fine pointer (desktop) | Phone (≤ 768 px or coarse pointer) | Reduced motion | No JS |
|---|---|---|---|---|
| **Glass-lens cursor** (ported from M2) | **States:**<br>- *morph* wraps buttons, tabs, swatches and links;<br>- *chat* is a WhatsApp bubble on every WhatsApp action, including the brief submit;<br>- *text* is a gold caret on headlines;<br>- *loupe* gives refraction over the orbs, team photos and canvas;<br>- *native* restores the system cursor and caret on all inputs, selects and the drop zone.<br>**Behaviour:** the lens hides on Tab so focus rings stay clear, and it never takes pointer events. | Off; native cursor | Off | Off |
| Magnetic buttons + pointer light | Yes | Press-scale instead | Off | — |
| Gold-dust trail + click ripple | Canvas, only while particles live | Tap ripples + 7 ms haptic tick (Android) | Off | — |
| Sparkle burst on WhatsApp, demo login, Approve, upload, download | Yes | Yes | Off | — |
| Glass edge light near the pointer | Panels, nav, dashboard cards | Off | Off | — |
| 3D tilt + glare (panel and preview frame) | Up to 6–7°; calms to 25% while typing | Static (no slab) | Static | Static |
| Orb, caustic, orbit ring, chips | CSS animations, paused off-screen (IntersectionObserver) and when the tab is hidden | One static orb only | Static | Static, visible |
| Entrance | CSS stagger, ≤ 1.2 s | Same | 0.3 s fade | None (content shown) |
| Theme switch | Circular View-Transition reveal, with a 250 ms fallback to an instant switch | Instant | Instant | Toggles hidden |
| Refraction (SVG displacement backdrop) | Chromium only; elsewhere frosted | — | — | — |

**Backdrop blur budget.**

| Context | Elements with `backdrop-filter` |
|---|---|
| Phone | 2: the nav and the sign-in panel (limit 8) |
| `prefers-reduced-transparency` | 0 |

**No-JS fallbacks.**

- **Login:** the sign-in panel shows a clear message and a "WhatsApp +91 81128 59437" button. The forms, which cannot work without JS, are hidden, and the dashboard stays hidden.
- **Studio:** shows "The cover studio needs JavaScript" with a WhatsApp link, instead of a dead app.

## Weaknesses and notes

- **Headless capture.**
  - The screenshots and videos come from headless Chromium using software compositing. Blur, glare and motion are softer and less smooth than on a real GPU.
  - Google Fonts are blocked in the sandbox, so the screenshots and the exported PNGs use fallback fonts. With real fonts, Inter Tight and Instrument Serif will look tighter.
- **The 3D is CSS, not WebGL.** It is a deliberate choice for weight and reliability. The panel tilts and has layered depth, but the glass orb does not truly refract the scene behind it.
- **Tilt and refraction are desktop-only.**
  - Phones get no tilt and no gyroscope.
  - The lens refraction works only in Chromium.
- **Sample content.** The sample deliverable numbers and Reel titles are invented placeholders. Each is labelled as a sample, but the owner should confirm she is happy with the wording.
- **Not shown on purpose.** Akarsh Yadav's phone number is not on the page (it is private). His Gmail is shown, as on the homepage.
- **The repo is untouched.** Copy both HTML files to the repo root when approved. `assets/` is symlinked here.

## Review fixes (round 2, 15 Oct 2026)

The design/QA review scored the pages 7.7/10 with two blocking issues. Both are fixed, along with most of the polish list. **`node verify_pages.js`: PASS 151 / WARN 0 / FAIL 0.** I also ran the new checks against the previous build: they fail there 7 times, so they catch the bugs the old suite missed.

### Blocking

1. **The nav clipped at iPad widths (769–850 px).**
   - Between 721 and 1080 px, "Back to website", "Client login (preview)" and "Sign out" become 40 px icon buttons. On touch screens they are 44 px. Their text labels stay in the page for screen readers and translate with the Hindi switch.
   - The breadcrumb hides below 780 px. Nav buttons, tags and labels never wrap.
   - `verify_pages.js` has a new `navFit` check that runs on the login sign-in view, the login dashboard and the studio. It covers 15 widths from 320 to 1440 px, including 769, 800, 810, 820 and 834, in English and Hindi. It fails if any visible nav control sits outside the glass pill, or if any label breaks onto a second line.
   - Screenshots: `qa/nav_dash_{800,820,834}_{en,hi}.png` and `qa/nav_studio_{800,820,834}_{en,hi}.png`.
2. **On phones, the studio's preview was 1,400 px away from the inputs.**
   - At 960 px and below, the controls come first, as on the original page, and the full preview and Download button follow.
   - A **mini live cover** (96 px wide, 9:16) is pinned bottom-right whenever the controls are on screen and the full preview is not. It redraws with every edit.
   - It stays above the on-screen keyboard using `visualViewport`.
   - If a focused field would sit under it, the page scrolls the field clear.
   - Tapping it scrolls to the full preview, flashes the frame gold and moves focus to Download. It uses no backdrop blur.
   - Verified: while typing a hook at 390 px, the mini cover is visible, drawn and not covering the field, and tapping it brings the canvas into view with Download focused.
   - Screenshots: `qa/studio_390_editing.png` (light), `qa/studio_390_editing_dark.png` and `qa/studio_820.png`. Video: `studio_mobile.mp4`.

### Polish applied

- **Readable hooks on busy photos.** With a photo, a soft dark band now sits behind just the hook block. It peaks at 0.90 and feathers out to 0, so the face above stays bright. The top badge pill is darker over photos (0.58).
  - Check: `_work/covers/review_fix_sheet.png` (busy frames, burned-in captions, Hindi, long hooks, all 4 looks) and `_work/covers/review_fix_grid_small.png` (130 px grid size).
  - Very bright burned-in captions can still show faintly through the band. A "strong backdrop" toggle was not added.
- **Balanced line breaks.** Two-line hooks now split where both lines are closest in width, so no single word is left alone. Devanagari gets more line height (1.24–1.34×), so stacked lines no longer touch: "डॉक्टर्स ये / गलती मत करो".
- **Faster typing.**
  - Edits redraw at most once per animation frame (`queueRender()`).
  - The background, photo and overlay are cached offscreen until the look or the photo changes.
  - The live preview uses a 16 px text shadow. Download re-renders with the full 28 px shadow before exporting.
  - Measured with headless Chromium at CPU ×4 and a photo loaded:
    - `renderThumbnail` takes 27–47 ms median across runs; the review measured 69–123 ms.
    - Typing 17 characters takes 1,162 ms, against 1,230 ms for the original repo page and 2,051 ms in the review.
  - The PNG is still 1080×1920, with the same file name.
- **Email wrapping.**
  - Team emails break before the "@" (`<wbr>`), never inside the domain.
  - Below 400 px the email is 12.5 px, so Akarsh's address fits on one line at 390 px.
  - `verify_pages.js` strips `<wbr>` before its text checks. The repo build allows 8756539282, the email digits.
- **Demo button.** On phones it reads "Try it with sample data" (Hindi "सैंपल डेटा से आज़माएं"), so no word is left alone on line 2.
- **Decor placement.**
  - The emerald orb now overlaps only the panel's top-right corner, and the gold orb only the bottom-left corner.
  - In dark mode the back slab is at half opacity with a shorter offset, so it reads as thickness rather than a second edge.
- **Layout gaps.**
  - Vandana's team card has a "See her work on the website" row (to `index.html#portfolio`).
  - The deliverables card ends with a "Next batch: 3 Reels for your approval on Friday" line tagged **Sample**. The wording changes with the plan, and the VIP plan has no line.
  - The deliverables card's note sits at the bottom, so the card has no empty band.
  - The phone dashboard keeps the next-batch line on one row.
- **Phone nav.** Both pages now have a 44 px round WhatsApp button with the official green logo, linking to wa.me/918112859437, like the homepage header. The studio desktop nav also gained the homepage-style WhatsApp pill.
- **Cursor matches the homepage more closely.**
  - Same sizes: 30 px idle, a 46 px "link" lens for large targets and plain links, and a 100×40 chat bubble.
  - Same 6 px emerald dot with a white ring and gold glow.
- **Wow touch: approval stamp.**
  - Approving a Reel or script settles a gold glass ring on its tile in about 450 ms and tints the row.
  - Approving the sample *script* adds 1 to "Scripts & 3-second hooks approved", for example 14 → 15 of 20. The bar grows smoothly and the number ticks.
  - With reduced motion, the ring just appears.
  - The Hindi round trip stays exact after approvals; this is verified.

### Polish skipped (and why)

- **One shared cursor and motion module built into all three pages.** `final_home/index.html` belongs to the homepage build, and this task was scoped to the two pages. I matched the cursor's sizes, states, dot and magnet feel instead. Merging the code into one module is a follow-up for whoever owns the shared build.
- **Lenis smooth scroll and scroll reveals on the dashboard.** These are form-heavy app pages, where native scrolling is safer for inputs, the phone keyboard and the focus jumps that `openDashboardForUser` makes. The dashboard cards already rise in on open, and nothing is hidden waiting for a scroll.
- **"Text backdrop: soft / strong" toggle.** The automatic band covers most frames.
- **Other ideas from the review:**
  - the 3D phone preview with a specular sweep: the desktop preview already tilts in a 3D glass frame;
  - the 3×3 profile-grid mock;
  - the nav-morph View Transition from the homepage.

  They would add weight, and the homepage would need a matching change.

### Re-recorded

All recordings are H.264 at CRF 26, each with a 12-frame `frames_*.png` contact sheet. There were no page errors.

| Video | Length | Size | What it shows |
|---|---|---|---|
| `login_desktop.mp4` | 16.2 s | 1440×900 | Script approval stamp and the 14 → 15 bump |
| `login_mobile.mp4` | 15.4 s | 390×844 | Touch; phone WhatsApp button in the nav |
| `studio_desktop.mp4` | 11.9 s | 1440×900 | — |
| `studio_mobile.mp4` (new) | 12.2 s | 390×844 | Typing with the mini cover following, then tap → full preview → Download |

**Other outputs:**
- `preview.png` was regenerated. It shows the login and studio desktop folds, the login phone view, the studio phone editing view with the mini cover, the iPad 820 px nav, and the dashboard after an approval.
- `qa/` has 49 screenshots, including the new nav, tablet, editing and approval captures.

**Caveats:**
- Capture is still headless Chromium with software rendering and Google Fonts blocked, so it uses fallback fonts.
- I did not test on a real iPad or phone. The keyboard lift uses `visualViewport` and is untested on iOS Safari.

**Repo untouched:** `git status` is clean.
