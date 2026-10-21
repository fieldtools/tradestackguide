# Nightly add-one-page workflow

Site base URL: https://tradestackguide.com/ (set in data/site.json; build.py also writes dist/CNAME and root robots.txt). Pages deploy automatically on push to main via .github/workflows/pages.yml.
1. Pick the first `todo` row in BACKLOG.md.
2. For every tool the page needs that isn't in data/tools.json: fetch the vendor's **public pricing page** and add an entry using the same fields. Use only values stated on the page. Also add the card fields the templates show: `best_for` (one line, factual), `starting_price` (as published), `pros` and `cons` (2-3 short items each, every item restating a sourced field; no ratings or opinions without a source). Put the URL in `sources` and write `"unknown"` for anything not published. Never invent ratings or prices.
3. If prices on existing tools changed, update them and bump `last_checked` in data/site.json.
4. Create `data/pages/<name>.json` with: slug, title (unique, ≤60 chars ideally), description (unique, ≤160), h1, keyword, type, tools[], trades[], body (HTML; `{{table:slug1,slug2}}` inserts the comparison table and `{{aff:key|Link text}}` inserts an affiliate CTA from data/affiliates.json), faq [[q,a],...] with sourced answers.
5. Link to at least 2 existing pages (trade page plus a related guide) inside the body.
6. Run `python3 build.py`, then the checks: no `{{` left in dist, no broken internal links, and titles/descriptions unique (see scripts below).
7. Mark the backlog row `done (YYYY-MM-DD)`. Commit locally; deploy/push only once a human has approved the hosting and git remote.

Checks:
```
grep -rl "{{" dist && echo "UNRENDERED TOKENS"
grep -rho "<title>[^<]*" dist | sort | uniq -d
```
Templates (build.py `layout`, `toolcard`, `trustbar`, `table`) render tool cards, the trust bar (last verified date, methodology, disclosure), the sticky header with 'Best for my trade' and 'Compare' (links to the first page with `type: compare`), inline SVG trade icons (`ICONS` keyed by trade `key`; add one for any new trade) and static/favicon.svg. Body HTML in page JSON needs no special classes.

Affiliate links: edit only data/affiliates.json (`url`, set `status` to `live`). Templates add `rel="sponsored nofollow"` automatically.
