# Ops changelog (expected state)

Log every settings, DNS, workflow or Pages change here before or when it's made. Commits by Bean are tagged [bean].

## Expected state
- Pages: build_type=workflow (GitHub Actions, .github/workflows), cname tradestackguide.com, HTTPS enforced.
- DNS (Cloudflare, DNS-only): A @ 185.199.108-111.153, CNAME www -> fieldtools.github.io, TXT google-site-verification (keep).
- Analytics: Cloudflare Web Analytics JS snippet, token 3c9bce2e6c024eb7a1a4ce2438f2f4ff, on every page.

## Log
- 2026-10-21 [bean] Site created; Pages deploy via GitHub Actions workflow from the first commit (f6c2281); custom domain + HTTPS set.
- 2026-10-21 [bean] Cloudflare Web Analytics snippet added (b8ac08b).
- 2026-10-22 [bean] Added ResponsiBid and Squeegee to data/affiliates.json as plain (non-affiliate) links.
