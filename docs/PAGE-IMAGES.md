# Per-page header photos

Every software page (articles from `data/pages/*.json`: best-of, reviews, X-vs-Y, guides, alternatives, calculators, checklists; plus every `/tools/<slug>/` page) gets a 1200x400 WebP header photo above the H1, with alt text, width/height and `loading="lazy"`.

## How build.py picks the photo (`page_img()`)

1. `"image": "<IMG key>"` in the page JSON (or tools.json entry) wins if that key exists in `IMG`.
2. `PAGE_IMG` in build.py: explicit slug -> key picks for existing pages (tool pages use `tools/<slug>`).
3. `TOPIC_WORDS`: regex match on the slug + H1 (or tool name), e.g. "pressure-washing" -> pressure photos.
4. The page's first `trades` entry (trade).
5. `DEFAULT_POOL`: generic fallback.

Steps 3-5 choose from a `TOPIC_POOL` list and rotate by a stable hash of the slug, so new nightly pages on the same topic get varied photos and the same page always gets the same photo. No page can end up without a photo.

## Adding a new photo

1. Pexels only. Confirm the photo page is live and Free; no visible brand names, vendor logos, or NSFW content.
2. Crop to 1200x400 (3:1) WebP, under 80 KB (`/workspace/sites/research/themed_images_preview/process2.py` shows the Pillow crop/quality loop), save in `static/img/`.
3. Add an `IMG` entry: (file, 1200, 400, alt text, photographer exactly as shown on Pexels, Pexels source URL), add the key to a `TOPIC_POOL` list (and optionally `PAGE_IMG`).
4. Add a row to docs/IMAGE-CREDITS.md. The About page credits table is generated from `IMG` automatically (file, pages using it, alt, photographer, source).

## Calculator and checklist pages (2026-10-23)

The calculator and checklist pages each have their own dedicated photo (`calc-*` / `checklist-*` keys in `IMG`, picked via `PAGE_IMG`) that no other page uses. They are deliberately not in any `TOPIC_POOL`, so nightly pages never reuse them. Crop script: `/workspace/sites/research/themed_images_preview/process3.py`.
