#!/usr/bin/env bash
# Build the PUBLIC website into dist/ for Cloudflare Pages / Netlify.
#
# Only the files on the allowlist below are published. Everything else in this
# repository (internal docs, SOPs, pricing, scripts, lead sheets) stays private.
# The build FAILS if:
#   - a non-website file type ends up in dist/
#   - a public page mentions a background team member, a family nickname,
#     or any WhatsApp/phone number other than the official one
#   - a public page links to a local file that was not published
#
# Cloudflare Pages settings: Build command `bash scripts/build_public_site.sh`, Build output directory `dist`
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist"

PUBLIC_PAGES=(index.html login.html pitch-deck.html thumbnail-studio.html)
PUBLIC_DIRS=(assets)

rm -rf "$OUT"
mkdir -p "$OUT"

for page in "${PUBLIC_PAGES[@]}"; do
  cp "$ROOT/$page" "$OUT/$page"
done
for dir in "${PUBLIC_DIRS[@]}"; do
  cp -R "$ROOT/$dir" "$OUT/$dir"
done
cp "$ROOT/site_config/_headers" "$OUT/_headers"
cp "$ROOT/site_config/robots.txt" "$OUT/robots.txt"

fail() { echo "BUILD BLOCKED: $1" >&2; exit 1; }

# 1. Only website file types may be published.
unexpected="$(find "$OUT" -type f ! \( -name '*.html' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \
  -o -name '*.webp' -o -name '*.svg' -o -name '*.ico' -o -name '_headers' -o -name 'robots.txt' \) -print)"
[ -z "$unexpected" ] || fail "non-website files in dist/:
$unexpected"

# 2. Golden Rules on every public page.
if grep -inE "indrajeet|guggy|sahil|9415259408" "$OUT"/*.html; then
  fail "a public page mentions a background team member, a nickname or a second number (see lines above)"
fi
# Normalise every Indian mobile number (with or without the 91 country code) to its last 10 digits.
# Allowed: 8112859437 (official WhatsApp) and 8756539282 (part of the official team email address).
other_numbers="$(grep -ohE '(\+?91[ -]?)?[6-9][0-9]{4}[ -]?[0-9]{5}' "$OUT"/*.html | tr -d ' +-' | grep -oE '[0-9]{10}$' \
  | sort -u | grep -vE '^(8112859437|8756539282)$' || true)"
[ -z "$other_numbers" ] || fail "unexpected phone number(s) on public pages: $other_numbers"

# 3. Every local link and image on the public pages must exist in dist/.
missing=""
for page in "$OUT"/*.html; do
  while IFS= read -r ref; do
    path="${ref%%[?#]*}"
    [ -z "$path" ] && continue
    [ -e "$OUT/$path" ] || missing="$missing\n  $(basename "$page") -> $path"
  done < <(grep -oE '(src|href)="[^"]+"' "$page" | sed -E 's/^(src|href)="//; s/"$//' \
            | grep -vE '^(https?:|mailto:|tel:|data:|about:|#|javascript:|//)' || true)
done
[ -z "$missing" ] || fail "broken local links:$(printf "$missing")"

echo "Public site built in dist/:"
(cd "$OUT" && find . -type f | sort | sed 's|^\./|  |' | awk -F/ '{print $1 (NF>1 ? "/" $2 : "")}' | sort | uniq -c)
