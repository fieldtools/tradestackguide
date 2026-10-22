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
- 2026-10-22 ~13:49 [bean] Contact email jacob@tradestackguide.com on About (#contact) and in footer; footer cross-link to StudioStackGuide (plain link); 12 FAQ entries added (5 per page on 4 pages). FAQPage JSON-LD validated; check_links passed.
- 2026-10-22 ~14:30 [bean] Added /job-quote-estimator/ (client-side JS, user inputs only) and /software-buying-checklist/ (printable, mailto:jacob@tradestackguide.com signup); nav links Calculator + Checklist in build.py. check_links passed.
- 2026-10-22 ~14:45 [bean] Replaced mailto checklist signup on /software-buying-checklist/ with Buttondown embed form (stackguide newsletter, hidden tag=tradestackguide, labeled required email, 'Get updates'); source edited in data/pages/software-buying-checklist.json; FAQ email mention removed. build + check_links passed.
- 2026-10-22 ~14:58 [bean] Pinned all workflow actions to full commit SHAs with tag comments (checkout v4.4.0, setup-python v5.6.0, configure-pages v5.0.0, upload-pages-artifact v3.0.1, deploy-pages v4.0.5).
