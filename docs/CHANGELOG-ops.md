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
- 2026-10-22 ~15:30 [bean] Added IndexNow: key file /6cabc1c04669fb5700750a6c49177f2a.txt (static/indexnow-key.txt, copied by build.py); scripts/indexnow_ping.py diffs built sitemap vs live one (fetched pre-deploy) and POSTs new/changed URLs to api.indexnow.org after deploy-pages (plain run steps, never fails deploy).
- 2026-10-22 ~15:35 [bean] IndexNow: treat missing live key file as first run; added 'all' mode. Ran initial full submission locally (first deploy diff was empty since sitemap pre-existed).

## 2026-10-22 — Email sending via Brevo (by Bean, approved by Jacob in chat)
- ~6:44 PM CDT: SPF TXT added `include:_spf.google.com` (for a Gmail send-as attempt that then failed DMARC; candidate for removal).
- ~7:03 PM CDT: DMARC temporarily set to p=none during setup.
- ~7:07 PM CDT: root TXT `brevo-code:da12bc01b2332e1d08cdfaa65d048b1a` (Brevo domain verification); CNAMEs `brevo1._domainkey` -> b1.tradestackguide-com.dkim.brevo.com and `brevo2._domainkey` -> b2.tradestackguide-com.dkim.brevo.com (DNS only).
- ~7:38 PM CDT: DMARC set to `v=DMARC1; p=quarantine; sp=quarantine; rua=mailto:rua@dmarc.brevo.com` (was p=reject; returning to reject pending Jacob).
- Purpose: outreach from jacob@tradestackguide.com sent through the Brevo API.
