# Image credits

All photos are from [Pexels](https://www.pexels.com/) under the [Pexels License](https://www.pexels.com/license/): free for commercial use, no attribution required. We credit photographers anyway (footer link + /about/#photo-credits).

Files live in `static/img/` (WebP, resized/cropped from the Pexels originals). Hero images also have a `-800.webp` mobile variant.

| File | Used on | Alt text | Photographer | Source page |
|---|---|---|---|---|
| `hero-lawn-care-crew.webp` (1600x640) | Homepage hero | Lawn care worker pushing a mower across a sunlit green lawn | Magic K | https://www.pexels.com/photo/man-mowing-lawn-6728933/ |
| `pressure-washing.webp` (1200x400) | Category page (pressure) | Worker pressure washing a paved surface, black and white | Nikita Nikitin | https://www.pexels.com/photo/man-watering-pavement-12111864/ |
| `window-cleaning.webp` (1200x400) | Category page (window) | Gloved hand cleaning a window with a squeegee | Blissful Place Cleaning company in Perth | https://www.pexels.com/photo/person-cleaning-window-with-squeegee-and-gloves-31435403/ |
| `pest-control.webp` (1200x400) | Category page (pest) | Pest control technician in protective suit fogging a warehouse | Cristian Aragón | https://www.pexels.com/photo/professional-fumigation-in-warehouse-setting-32055757/ |
| `pool-service.webp` (1200x400) | Category page (pool) | Clean blue residential swimming pool beside a patio | Ahmet ÇÖTÜR | https://www.pexels.com/photo/swimming-pool-in-the-yard-of-a-house-19084144/ |
| `lawn-care.webp` (1200x400) | Category page (lawn) | Gardener trimming a green hedge with long shears | el jusuf | https://www.pexels.com/photo/garden-maintenance-trimming-hedges-in-jakarta-32427439/ |

## Per-page header photos (software pages)

Assigned automatically by `page_img()` in build.py (see docs/PAGE-IMAGES.md). "Used on" reflects the build on 2026-10-23; the live list is always on /about/#photo-credits.

| File | Used on | Alt text | Photographer | Source page |
|---|---|---|---|---|
| `pressure-washing.webp` (1200x400) | /tools/workiz/ | Worker pressure washing a paved surface, black and white | Nikita Nikitin | https://www.pexels.com/photo/man-watering-pavement-12111864/ |
| `window-cleaning.webp` (1200x400) | /tools/responsibid/ | Gloved hand cleaning a window with a squeegee | Blissful Place Cleaning company in Perth | https://www.pexels.com/photo/person-cleaning-window-with-squeegee-and-gloves-31435403/ |
| `pest-control.webp` (1200x400) | /tools/gorilladesk/ | Pest control technician in protective suit fogging a warehouse | Cristian Aragón | https://www.pexels.com/photo/professional-fumigation-in-warehouse-setting-32055757/ |
| `pool-service.webp` (1200x400) | /tools/housecall-pro/ | Clean blue residential swimming pool beside a patio | Ahmet ÇÖTÜR | https://www.pexels.com/photo/swimming-pool-in-the-yard-of-a-house-19084144/ |
| `lawn-care.webp` (1200x400) | /tools/jobber/ | Gardener trimming a green hedge with long shears | el jusuf | https://www.pexels.com/photo/garden-maintenance-trimming-hedges-in-jakarta-32427439/ |
| `pest-fumigation.webp` (1200x400) | /best/pest-control-software/ | Technician in a white protective suit fogging a plant with a fumigation wand | Michelangelo Buonarroti | https://www.pexels.com/photo/4176548/ |
| `pool-backyard.webp` (1200x400) | /best/pool-service-software/ | Backyard swimming pool set in a green lawn beside a modern house | Max Vakhtbovych | https://www.pexels.com/photo/8134748/ |
| `pool-dusk.webp` (1200x400) | /tools/skimmer/ | Residential pool and lounge chairs in a leafy garden at dusk | Rachel Claire | https://www.pexels.com/photo/5864697/ |
| `pressure-washing-steps.webp` (1200x400) | /best/pressure-washing-software/ | Worker in hi-vis gear pressure washing stone steps | Antonio Lorenzana Bermejo | https://www.pexels.com/photo/14965464/ |
| `window-cleaning-facade.webp` (1200x400) | /best/window-cleaning-software/ | Window cleaner using a squeegee pole on a glass building front | Cihat Dede | https://www.pexels.com/photo/professional-window-cleaner-at-work-outdoors-37440103/ |
| `lawn-mower-service.webp` (1200x400) | /compare/jobber-vs-housecall-pro/ | Gloved worker servicing a lawn mower on the grass | Gustavo Fring | https://www.pexels.com/photo/5163424/ |
| `hedge-trimming.webp` (1200x400) | topic pool (lawn); was /software-buying-checklist/ until 2026-10-23 | Close-up of a gardener trimming a hedge with shears | Magda Ehlers | https://www.pexels.com/photo/38936334/ |

Checked 2026-10-23: each source page was live and marked Free. Images were reviewed for visible logos/brand names and SFW content.

## Directory pages (unlisted, noindex)

| File | Used on | Alt text | Photographer | Source page |
|---|---|---|---|---|
| `industrial-tank-hydroblasting.webp` (1200x400) | /directory/se-iowa-industrial-contractors/ header | Overhead view of workers in hard hats hydro blasting the floor of a large industrial tank | Saruhan Osmanoğlu | https://www.pexels.com/photo/industrial-workers-cleaning-large-floor-surface-37443412/ |
| `industrial-ppe-spray-card.webp` (480x320) | CCS Keokuk listing card (stock fallback for trade "industrial") | Industrial worker in a protective suit and mask spraying with a high-pressure gun on scaffolding | Caleb Oquendo | https://www.pexels.com/photo/standing-person-holding-hose-3186687/ |
| `quote-estimate-notebook.webp` (1200x400) | /job-quote-estimator/ | Hand writing job notes in a notebook beside garden soil and plants | Antoni Shkraba | https://www.pexels.com/photo/a-person-writing-on-a-notebook-7342626/ |
| `service-checklist-clipboard.webp` (1200x400) | /software-buying-checklist/ | Worker in a hi-vis vest holding a pen and a printed checklist on a clipboard | RDNE Stock project | https://www.pexels.com/photo/person-in-yellow-reflective-safety-vest-holding-a-pen-and-checklist-of-house-inspection-8293680/ |

Listing cards take an optional `"image"` in `data/directory/*.json`: an `IMG` key, or `{"src","alt","width","height","credit"}` for a contractor-supplied photo (only with written permission). If it's empty, the card uses the trade-matched stock photo (`LISTING_TRADE_IMG` in build.py).
| `contractor-tablet-quote.webp` (1200x400) | /tools/quoteiq/ | Contractor in a hard hat and hi-vis vest checking a tablet on a job site | Mikael Blomkvist | https://www.pexels.com/photo/an-engineer-using-a-digital-tablet-8961008/ |
