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

## 2026-10-23 6:21 AM CDT (Bean, approved by Jacob)
- SPF: removed include:_spf.google.com -> v=spf1 include:_spf.mx.cloudflare.net ~all
- DMARC: back to p=reject; sp=reject (rua Brevo kept)
- 2026-10-23 ~06:40 CDT [bean] IndexNow check: existing key file live (200, body matches); ran `python3 scripts/indexnow_ping.py all` → api.indexnow.org HTTP 200. No new key generated (existing setup already covers this).
- 2026-10-23 ~08:30 CDT Merged themed-images into main (approved by Jacob): themed Pexels WebP header photos on all software pages incl. new nightly pages, homepage hero banner, photo credits on /about/. build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~09:00 CDT Bumped Pages deploy workflow actions off Node 20 (approved by Jacob): checkout v4.4.0→v7.0.1, setup-python v5.6.0→v7.1.0, configure-pages v5.0.0→v6.0.0, upload-pages-artifact v3.0.1→v5.0.0, deploy-pages v4.0.5→v5.0.1 (SHA-pinned).
- 2026-10-23 ~09:25 CDT Published /directory/se-iowa-industrial-contractors/ (approved by Jacob): removed noindex, added to sitemap, footer link; CCS Keokuk card unchanged (photos + both phones). Merged ccs-preview into main; IndexNow `all` ping after deploy.
- 2026-10-23 ~09:25 CDT Moved SE Iowa directory link from footer to top nav after Methodology ('SE Iowa Directory', approved by Jacob); nav is horizontal-scroll nowrap so mobile layout unaffected.
- 2026-10-23 ~09:35 CDT Merged calc-checklist-photos into main (approved by Jacob): dedicated Pexels header photos for the calculator and checklist pages (credits in docs/IMAGE-CREDITS.md + /about/). build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~09:36 CDT Added /disclosure/ affiliate disclosure page (approved by Jacob), linked from footer, trust bar and /about/, plus a short commission line on tool, category, comparison and guide pages. Added 'Get listed free' mailto section to /directory/se-iowa-industrial-contractors/. build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~09:41 CDT SE Iowa directory intro reworded to match Get Listed section: details come from the contractor's own website or from what they send us (approved by Jacob). build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~09:42 CDT SE Iowa directory intro: 'If we don't have it from them, we leave it out.' (consistency with Get Listed, approved by Jacob). build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~11:10 CDT CCS Keokuk listing: phone now only (319) 313-9226 (their preferred number, per their reply); removed (319) 670-0054. build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~11:50 CDT Added approved QuoteIQ affiliate link (?via=jacob-carman) to data/affiliates.json as key `quoteiq`. No pages mention QuoteIQ yet (only BACKLOG #33), so no page/disclosure changes. build + check_links clean.
- 2026-10-23 ~11:55 CDT Published /tools/quoteiq/ (BACKLOG #33, approved by Jacob): pricing/features sourced from myquoteiq.com/pricing + homepage, {{aff:quoteiq}} CTAs (rel sponsored), trustbar disclosure, Pexels header photo 8961008 (Mikael Blomkvist, verified Free). build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23 ~12:02 CDT Published /tools/gorilladesk/ page refresh (approved by Jacob): facts re-verified on vendor pricing page, own Pexels header photo (17903068), affiliate status pending (plain link). build + check_links clean. IndexNow `all` ping after deploy.
- 2026-10-23: d183f62 (nightly) added best pressure washing software page, added Workiz, re-verified prices. (Changelog line added late.)
- 2026-10-24 ~01:30 CDT [bean] Published /best/lawn-care-software/ (BACKLOG #3) plus new tool pages /tools/yardbook/, /tools/service-autopilot/, /tools/lmn/ (sourced from vendor pricing pages, affiliates.json entries status plain); QuoteIQ affiliate CTA. Re-verified all existing tool prices (no changes), last_checked -> 2026-10-24. No settings/DNS/workflow/Pages changes. build + check_links clean.
- 2026-10-24: Pinned Pages deploy runner to ubuntu-26.04 (was ubuntu-latest) to clear the Ubuntu 26 migration notice; actions already on latest majors. [bean] (approved by Jacob Oct 24)
- 2026-10-24: Added branded noindex 404.html (built into dist/), /.well-known/security.txt (RFC 9116) + .nojekyll in dist (Pages artifact now include-hidden-files: true), .github/dependabot.yml (github-actions, weekly); enabled Dependabot alerts + security updates. No DNS/page content changes. [bean] (approved by Jacob Oct 24)
- 2026-10-26: Added BookingKoala to data/affiliates.json (status affiliate, referral link). BookingKoala not linked on any live page yet, so no page changes. [bean] (approved by Jacob 2026-10-26: use BookingKoala referral link)
- 2026-10-26: Published /tools/bookingkoala/ (BACKLOG #44) with BookingKoala referral CTA (rel sponsored); linked from /best/window-cleaning-software/; tool template gains optional who_html/compare_html. build + check_links clean. [bean] (approved by Jacob 2026-10-26: publish BookingKoala page)
- 2026-10-26: Published LawnPro additions (/tools/lawnpro/, LawnPro on /best/lawn-care-software/ and /trades/lawn-care/) and new /field-service-software-cost-1-vs-5-users/. 390px mobile check: no horizontal overflow on new or existing pages (no CSS change). build + check_links clean. [bean] (approved by Jacob 2026-10-26: publish LawnPro and cost-comparison pages)
- 2026-10-26 ~11:22 CDT: Added Synchroteam to data/affiliates.json (status applied); no page changes. Commit 80c277b. [bean] (made by the daily affiliate scout routine under Jacob's standing instruction; not individually approved in chat)
