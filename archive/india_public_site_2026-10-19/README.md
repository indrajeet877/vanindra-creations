# India public site — snapshot, 19 October 2026

This folder is a copy of the public website as it stood before the homepage was rebuilt for global (USD) clients.

| File | What it was |
| :--- | :--- |
| `index.html` | India homepage (Liquid Glass). Rupee pricing: ₹2,999 trial, ₹14,999, ₹24,999, ₹39,999. Hindi toggle, voice input, and the strategy generator. |
| `login.html` | Client portal preview. |
| `pitch-deck.html` | India pitch deck. |
| `thumbnail-studio.html` | Reel cover studio. |

Nothing here was deleted from the product. `login.html`, `pitch-deck.html`, and `thumbnail-studio.html` are still in the repository root and still publish. Only the live homepage (`/index.html`) was replaced.

Image paths inside these files point at `/assets` in the repository root. To put the India homepage back, copy this folder's `index.html` over the root `index.html`.

This folder is excluded from GitHub Pages (`_config.yml`) and from `scripts/build_public_site.sh`, so the rupee homepage is not a second public URL.
