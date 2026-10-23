#!/usr/bin/env python3
"""Build TradeStackGuide static site from data/*.json into dist/. No dependencies."""
import json, re, shutil, html, zlib
from pathlib import Path
R = Path(__file__).parent; D = R/"data"; OUT = R/"dist"
site = json.loads((D/"site.json").read_text()); aff = json.loads((D/"affiliates.json").read_text())
tools = {t["slug"]: t for t in json.loads((D/"tools.json").read_text())}
trades = json.loads((D/"trades.json").read_text())
pages = [json.loads(p.read_text()) for p in sorted((D/"pages").glob("*.json"))]
BASE, LC = site["base_url"].rstrip("/"), site["last_checked"]
from urllib.parse import urlparse
PREFIX = urlparse(BASE).path.rstrip("/")
e = html.escape
urls = []

ICONS = {  # simple original inline SVG paths (24x24, stroke)
 "pool": '<path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M2 22c2 0 2-1.5 4-1.5S8 22 10 22s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M8 15V5a2 2 0 0 1 4 0M16 15V5a2 2 0 0 0-4 0M8 9h8"/>',
 "pest": '<ellipse cx="12" cy="14" rx="4" ry="6"/><circle cx="12" cy="6" r="2"/><path d="M8 11 4 9M8 15H3M8 18l-4 2M16 11l4-2M16 15h5M16 18l4 2M11 4 9 2M13 4l2-2"/>',
 "lawn": '<path d="M2 21h20M5 21c0-4-1-7-3-9M8 21c0-6 1-10 4-13M12 21c0-5 0-9-2-12M16 21c0-6 2-10 5-12M19 21c0-3 1-6 3-7"/>',
 "window": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16M15 6l2 2M7 15l2 2"/>',
 "pressure": '<path d="M3 10h8l2 2h3M5 10V7h5v3M16 12l5-3M16 12l5 0M16 12l5 3M6 14v6M3 20h6"/>',
}
IMG = {  # header photos (Pexels license: free commercial use, no attribution required); credits in docs/IMAGE-CREDITS.md
 "hero": ("hero-lawn-care-crew.webp", 1600, 640, "Lawn care worker pushing a mower across a sunlit green lawn", "Magic K", "https://www.pexels.com/photo/man-mowing-lawn-6728933/"),
 "pressure": ("pressure-washing.webp", 1200, 400, "Worker pressure washing a paved surface, black and white", "Nikita Nikitin", "https://www.pexels.com/photo/man-watering-pavement-12111864/"),
 "window": ("window-cleaning.webp", 1200, 400, "Gloved hand cleaning a window with a squeegee", "Blissful Place Cleaning company in Perth", "https://www.pexels.com/photo/person-cleaning-window-with-squeegee-and-gloves-31435403/"),
 "pest": ("pest-control.webp", 1200, 400, "Pest control technician in protective suit fogging a warehouse", "Cristian Aragón", "https://www.pexels.com/photo/professional-fumigation-in-warehouse-setting-32055757/"),
 "pool": ("pool-service.webp", 1200, 400, "Clean blue residential swimming pool beside a patio", "Ahmet ÇÖTÜR", "https://www.pexels.com/photo/swimming-pool-in-the-yard-of-a-house-19084144/"),
 "lawn": ("lawn-care.webp", 1200, 400, "Gardener trimming a green hedge with long shears", "el jusuf", "https://www.pexels.com/photo/garden-maintenance-trimming-hedges-in-jakarta-32427439/"),
 # per-page photos (articles + /tools/ pages); see docs/PAGE-IMAGES.md
 "pest2": ("pest-fumigation.webp", 1200, 400, "Technician in a white protective suit fogging a plant with a fumigation wand", "Michelangelo Buonarroti", "https://www.pexels.com/photo/4176548/"),
 "pool2": ("pool-backyard.webp", 1200, 400, "Backyard swimming pool set in a green lawn beside a modern house", "Max Vakhtbovych", "https://www.pexels.com/photo/8134748/"),
 "pool3": ("pool-dusk.webp", 1200, 400, "Residential pool and lounge chairs in a leafy garden at dusk", "Rachel Claire", "https://www.pexels.com/photo/5864697/"),
 "pressure2": ("pressure-washing-steps.webp", 1200, 400, "Worker in hi-vis gear pressure washing stone steps", "Antonio Lorenzana Bermejo", "https://www.pexels.com/photo/14965464/"),
 "window2": ("window-cleaning-facade.webp", 1200, 400, "Window cleaner using a squeegee pole on a glass building front", "Cihat Dede", "https://www.pexels.com/photo/professional-window-cleaner-at-work-outdoors-37440103/"),
 "lawn2": ("lawn-mower-service.webp", 1200, 400, "Gloved worker servicing a lawn mower on the grass", "Gustavo Fring", "https://www.pexels.com/photo/5163424/"),
 # industrial cleaning (directory pages)
 "industrial": ("industrial-tank-hydroblasting.webp", 1200, 400, "Overhead view of workers in hard hats hydro blasting the floor of a large industrial tank", "Saruhan Osmanoğlu", "https://www.pexels.com/photo/industrial-workers-cleaning-large-floor-surface-37443412/"),
 "industrial-card": ("industrial-ppe-spray-card.webp", 480, 320, "Industrial worker in a protective suit and mask spraying with a high-pressure gun on scaffolding", "Caleb Oquendo", "https://www.pexels.com/photo/standing-person-holding-hose-3186687/"),
 "lawn3": ("hedge-trimming.webp", 1200, 400, "Close-up of a gardener trimming a hedge with shears", "Magda Ehlers", "https://www.pexels.com/photo/38936334/"),
}
PAGE_IMG = {  # explicit picks for existing pages (slug -> IMG key)
 "best/pest-control-software": "pest2", "best/pool-service-software": "pool2", "best/pressure-washing-software": "pressure2",
 "best/window-cleaning-software": "window2", "compare/jobber-vs-housecall-pro": "lawn2", "software-buying-checklist": "lawn3",
 "job-quote-estimator": "window",
 "tools/jobber": "lawn", "tools/housecall-pro": "pool", "tools/gorilladesk": "pest", "tools/skimmer": "pool3",
 "tools/responsibid": "window", "tools/workiz": "pressure"}
TOPIC_WORDS = [("pressure", r"pressure|power.?wash|soft.?wash|exterior clean"), ("window", r"window|gutter|squeegee"),
 ("pest", r"pest|termite|mosquito|extermin|bug"), ("pool", r"pool|spa\b|hot.?tub|skimmer"), ("lawn", r"lawn|landscap|mow|turf|garden|tree|snow")]
TOPIC_POOL = {"pressure": ["pressure", "pressure2"], "window": ["window", "window2"], "pest": ["pest", "pest2"],
 "pool": ["pool", "pool2", "pool3"], "lawn": ["lawn", "lawn2", "lawn3"]}
DEFAULT_POOL = ["lawn2", "lawn3", "window2", "pressure2"]  # generic field-service fallback
def page_img(slug, text="", topics=(), explicit=None):
    """Pick a header photo key for a page. Order: page JSON "image" -> PAGE_IMG -> keyword match on
    slug/title -> first listed trade/studio type -> DEFAULT_POOL. Pools rotate by a stable slug hash."""
    if explicit in IMG: return explicit
    if slug in PAGE_IMG: return PAGE_IMG[slug]
    hay = f"{slug} {text}".lower(); topic = next((k for k, rx in TOPIC_WORDS if re.search(rx, hay)), None)
    topic = topic or next((t for t in topics if t in TOPIC_POOL), None)
    pool = TOPIC_POOL.get(topic, DEFAULT_POOL)
    return pool[zlib.crc32(slug.encode()) % len(pool)]
def page_targets():
    """(path, slug, image key) for every software page; used by the build and the About credits."""
    out = [(f"/{p['slug']}/", p["slug"], page_img(p["slug"], p.get("h1",""), p.get("trades",[]), p.get("image"))) for p in pages]
    out += [(f"/tools/{x['slug']}/", "tools/"+x["slug"], page_img("tools/"+x["slug"], x["name"], x.get("trades",[]), x.get("image"))) for x in tools.values()]
    return out
def pic(key, cls="ph-img", lazy=True):
    if key not in IMG: return ""
    f, w, h, alt, _, _ = IMG[key]
    att = 'loading="lazy" decoding="async"' if lazy else 'fetchpriority="high" decoding="async"'
    ss = f' srcset="/img/{f[:-5]}-800.webp 800w, /img/{f} {w}w" sizes="(max-width: 820px) 100vw, 1100px"' if key == "hero" else ""
    return f'<img class="{cls}" src="/img/{f}"{ss} width="{w}" height="{h}" alt="{e(alt)}" {att}>'
def credits_html():
    uses = {}
    for path, _, k in page_targets(): uses.setdefault(k, []).append(path)
    rows = "".join(f'<tr><td>{e(v[0])}</td><td>{", ".join(e(u) for u in (["Homepage"] if k=="hero" else []) + (["category page"] if k in ICONS else []) + (["/directory/se-iowa-industrial-contractors/"] if k.startswith("industrial") else []) + uses.get(k, [])) or "-"}</td><td>{e(v[3])}</td><td>{e(v[4])}</td><td><a href="{e(v[5])}" rel="nofollow noopener">{e(v[5])}</a></td></tr>' for k, v in IMG.items())
    return f'<div class="tw" tabindex="0" role="region" aria-label="Photo credits table"><table><tr><th>File</th><th>Used on</th><th>Alt text</th><th>Photographer</th><th>Source (Pexels)</th></tr>{rows}</table></div>'
def icon(key, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS.get(key,"")}</svg>'
CHECK = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M5 12l5 5 9-10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
def proscons(x):
    if not x.get("pros"): return ""
    return ('<div class="pc"><div><h3 class="pro-h">Pros</h3><ul class="pros">' + "".join(f"<li>{CHECK}{e(p)}</li>" for p in x["pros"]) +
            '</ul></div><div><h3 class="con-h">Cons</h3><ul class="cons">' + "".join(f"<li>{CROSS}{e(c)}</li>" for c in x.get("cons",[])) + '</ul></div></div>')
def toolcard(x, full=False):
    key = x["slug"].replace("-","")
    cta = afflink(key, f"Visit {x['name']}") if key in aff else ""
    return (f'<article class="card tool"><h3><a href="/tools/{x["slug"]}/">{x["name"]}</a></h3>'
            f'<p class="bf"><span class="lbl">Best for</span> {e(x.get("best_for","unknown"))}</p>'
            f'<p class="price"><span class="lbl">Starting price</span> {e(x.get("starting_price", x["plans"][0]["monthly_no_commit"]))}</p>'
            + (proscons(x) if full else "") +
            f'<div class="actions">{cta}<a class="btn2" href="/tools/{x["slug"]}/">Pricing details</a></div>'
            f'<p class="src">Source: <a href="{e(x["sources"][0])}" rel="nofollow">vendor pricing page</a> · verified {LC}</p></article>')
def trustbar():
    return f'<p class="trust"><span>✔ Last verified {LC}</span><span>✔ Prices linked to vendor sources</span><span><a href="/about/">✔ Our methodology</a></span><span><a href="/about/#disclosure">Affiliate disclosure</a></span></p>'

def layout(path, title, desc, body, schema=None, noindex=False):
    nav = "".join(f'<a href="/trades/{t["slug"]}/">{t["name"]}</a>' for t in trades)
    cmp_ = next((p for p in pages if p.get("type") == "compare"), None)
    cmp_link = f'<a class="pill" href="/{cmp_["slug"]}/">Compare</a>' if cmp_ else ""
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in (schema or []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<meta name="theme-color" content="#0f5e4f"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">{ROBOTS_NOINDEX if noindex else ""}{ld}</head><body><a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap hd"><a class="logo" href="/"><svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#0f5e4f"/><path d="M8 11h16M8 16h11M8 21h7" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>{site['name']}</a>
<nav class="quick" aria-label="Quick"><a class="pill pri" href="/#trades">Best for my trade</a>{cmp_link}</nav></div>
<nav class="trades wrap" aria-label="Trades">{nav}<a href="/job-quote-estimator/">Calculator</a><a href="/software-buying-checklist/">Checklist</a><a href="/about/">Methodology</a></nav></header>
<main id="main" class="wrap">{body}</main><footer><div class="wrap"><p><strong>{site['name']}</strong>: {e(site['tagline'])}.</p><p>Last checked: {LC}. Some links may be affiliate links; see our <a href="/about/#disclosure">disclosure</a>. Prices come from vendor pages and can change. <a href="/about/">Methodology</a></p><p class="credits">Photos from <a href="https://www.pexels.com/" rel="nofollow noopener">Pexels</a> (free license). <a href="/about/#photo-credits">Photo credits</a></p><p>Contact: <a href="mailto:jacob@tradestackguide.com">jacob@tradestackguide.com</a></p><p>Local directory: <a href="/directory/se-iowa-industrial-contractors/">SE Iowa industrial contractors</a>.</p><p>Run a martial arts school or studio? See <a href="https://studiostackguide.com/">StudioStackGuide</a>.</p></div></footer><!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "3c9bce2e6c024eb7a1a4ce2438f2f4ff"}}'></script><!-- End Cloudflare Web Analytics --></body></html>"""

def write(path, content):
    f = OUT/path.strip("/")/"index.html" if path != "/" else OUT/"index.html"
    f.parent.mkdir(parents=True, exist_ok=True); f.write_text(re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{PREFIX}/', content)); urls.append(path)

def afflink(key, text):
    a = aff[key]; return f'<a class="cta" href="{e(a["url"])}" rel="sponsored nofollow noopener" target="_blank">{e(text)}</a>'

def table(slugs):
    ts = [tools[s] for s in slugs]
    rows = [("Starting price", lambda t: "<br>".join(f'{p["name"]}: {p["monthly_no_commit"]} / {p["annual"]}' for p in t["plans"][:2])),
            ("Users / billing unit", lambda t: t["extra_user"]), ("Free trial", lambda t: t["free_trial"]),
            ("Contract", lambda t: t["contract"]), ("Routing", lambda t: t["routing"]),
            ("Chemical/material tracking", lambda t: t["chemical_tracking"]), ("QuickBooks", lambda t: t["quickbooks"]),
            ("Payment fees", lambda t: t["card_fee"]), ("Rating", lambda t: t["rating"]),
            ("Source", lambda t: " ".join(f'<a href="{s}" rel="nofollow">vendor page</a>' for s in t["sources"]))]
    h = "<tr><th></th>" + "".join(f'<th><a href="/tools/{t["slug"]}/">{t["name"]}</a></th>' for t in ts) + "</tr>"
    b = "".join("<tr><th>"+n+"</th>"+"".join(f"<td>{f(t)}</td>" for t in ts)+"</tr>" for n, f in rows)
    return f'<div class="tw" tabindex="0" role="region" aria-label="Comparison table (scroll sideways)"><table class="cmp">{h}{b}</table></div><p class="hint">Swipe sideways to see every tool →</p><p class="note">Prices as published (monthly no-commitment / annual where shown). "unknown" = not published. Checked {LC}.</p>'

def render(body):
    body = re.sub(r"\{\{table:([^}]+)\}\}", lambda m: table(m.group(1).split(",")), body)
    return re.sub(r"\{\{aff:([a-z0-9-]+)\|([^}]+)\}\}", lambda m: afflink(m.group(1), m.group(2)), body)

def crumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

ROBOTS_NOINDEX = '<meta name="robots" content="noindex,nofollow">'
LISTING_TRADE_IMG = {"industrial": "industrial-card"}  # trade -> stock card photo fallback
def listing_img(l, trade):
    """Per-listing photo: l["image"] = IMG key, or {"src","alt","width","height","credit"} supplied by the
    contractor (with permission). Falls back to the trade-matched stock photo."""
    im = l.get("image")
    if isinstance(im, dict) and im.get("src"):
        cr = f'<figcaption>{e(im["credit"])}</figcaption>' if im.get("credit") else ""
        return f'<figure class="lc-img"><img src="{e(im["src"])}" width="{int(im["width"])}" height="{int(im["height"])}" alt="{e(im.get("alt",""))}" loading="lazy" decoding="async">{cr}</figure>'
    key = im if im in IMG else LISTING_TRADE_IMG.get(l.get("trade", trade))
    return f'<figure class="lc-img">{pic(key, "")}</figure>' if key else ""
def listing_card(l, trade="industrial"):
    ul = lambda xs: "<ul>" + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ul>"
    phones = l["phone"] if isinstance(l["phone"], list) else [l["phone"]]
    tels = " · ".join(f'<a href="tel:+1{re.sub(r"[^0-9]", "", p)}">{e(p)}</a>' for p in phones)
    srcs = " ".join(f'<a href="{e(u)}" rel="nofollow">{e(u)}</a>' for u in l["sources"])
    return (f'<article class="card listing">{listing_img(l, trade)}<h2>{e(l["name"])}</h2><p>{e(l["summary"])}</p><ul class="facts">'
            f'<li>Location: {e(l["location"])}</li><li>Phone: {tels}</li>'
            f'<li>Email: <a href="mailto:{e(l["email"])}">{e(l["email"])}</a></li>'
            f'<li>Website: <a href="{e(l["website"])}" rel="nofollow">{e(l["website"])}</a></li><li>{e(l["hours"])}</li></ul>'
            f'<h3>Industrial services</h3>{ul(l["services"])}<h3>Licensing and compliance</h3>{ul(l["credentials"])}'
            f'<p>{e(l["also"])}</p><p class="src">Sources: {srcs} · checked {l["checked"]}</p></article>')
def build_directory():
    """Directory pages: indexed, in sitemap, linked from footer."""
    dd = D/"directory"
    for f in (sorted(dd.glob("*.json")) if dd.exists() else []):
        d = json.loads(f.read_text()); path = "/" + d["slug"] + "/"
        body = f'{pic(d.get("image", "industrial"), lazy=False)}<h1>{e(d["h1"])}</h1><p>{e(d["intro"])}</p>' + "".join(listing_card(l, d.get("trade", "industrial")) for l in d["listings"])
        write(path, layout(path, d["title"], d["intro"][:155], body))

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); shutil.copy(R/"static/style.css", OUT/"style.css"); shutil.copy(R/"static/favicon.svg", OUT/"favicon.svg"); shutil.copytree(R/"static/img", OUT/"img")
    _k=(R/"static/indexnow-key.txt").read_text().strip(); (OUT/f"{_k}.txt").write_text(_k)
    # home
    cards = "".join(f'<li><a class="card trade" href="/trades/{t["slug"]}/">{icon(t["key"])}<span>{t["name"]} software</span></a></li>' for t in trades)
    arts = "".join(f'<li><a class="card guide" href="/{p["slug"]}/"><span class="tag">{e(p.get("type","guide")).title()}</span>{e(p["h1"])}</a></li>' for p in pages)
    tcards = "".join(toolcard(x) for x in tools.values())
    write("/", layout("/", f"{site['name']}: Software Comparisons for Pool, Pest, Lawn & Cleaning Pros",
        "Sourced, no-fluff comparisons of scheduling, routing and invoicing software for small pool, pest control, lawn care, window cleaning and pressure washing businesses.",
        f"<section class='hero'><div class='banner'>{pic('hero','banner-img',lazy=False)}<div class='banner-txt'><h1>Find the right software for your service business</h1><p class='lead'>{site['tagline']}. Every price links to its source. If a number isn't public, we say unknown.</p></div></div><ul class='grid trades-g' id='trades' aria-label='Choose your trade'>{cards}</ul>{trustbar()}</section><h2>Tools we track</h2><div class='grid tools-g'>{tcards}</div><h2>Guides and comparisons</h2><ul class='grid guides-g'>{arts}</ul>",
        [{"@context":"https://schema.org","@type":"WebSite","name":site["name"],"url":BASE+"/"}]))
    # about
    write("/about/", layout("/about/", f"About & Methodology | {site['name']}", "How TradeStackGuide collects pricing and feature data, how often it's checked, and how we make money (affiliate disclosure).",
        f"""<h1>About and methodology</h1><h2>How we collect data</h2><p>We only use information published on each vendor's own public pricing and feature pages. Each tool entry lists its source URLs and a last-checked date (currently {LC}). We don't invent ratings, review scores or prices. Anything a vendor doesn't publish is marked <em>unknown</em>.</p>
<h2>How often we update</h2><p>We re-check prices on a rolling basis and at least quarterly. Promotions change often, so always confirm on the vendor's site.</p>
<h2 id="disclosure">Affiliate disclosure</h2><p>Some links on this site are affiliate or referral links. If you sign up through them, we may earn a commission at no extra cost to you. Commissions never affect the data we publish, and we list tools whether or not they have an affiliate program.</p>
<h2 id="contact">Contact</h2><p>Questions, corrections or pricing updates: email <a href="mailto:jacob@tradestackguide.com">jacob@tradestackguide.com</a>.</p><h2 id="photo-credits">Photo credits</h2><p>Photos are from Pexels under the Pexels license (free for commercial use, attribution not required). We credit the photographers anyway:</p>"""+credits_html()+""""""))
    # trades
    for t in trades:
        ts = [x for x in tools.values() if t["key"] in x["trades"]]
        rel = "".join(f'<li><a href="/{p["slug"]}/">{e(p["h1"])}</a></li>' for p in pages if t["key"] in p["trades"])
        li = "".join(f'<li><a href="/tools/{x["slug"]}/">{x["name"]}</a>: from {x["plans"][0]["monthly_no_commit"]}</li>' for x in ts)
        path = f"/trades/{t['slug']}/"
        write(path, layout(path, f"{t['name']} Business Software: Tools, Prices & Comparisons ({LC[:4]})",
            f"{t['name']} software compared: {', '.join(x['name'] for x in ts)}. Published prices, trials and features with sources, last checked {LC}.",
            f"{pic(t['key'])}<div class='ph'>{icon(t['key'],'ic big')}<h1>{t['name']} software</h1></div><p class='lead'>{t['intro']}</p>{trustbar()}<h2>Tools</h2><div class='grid tools-g'>{''.join(toolcard(x) for x in ts)}</div><h2>Side-by-side comparison</h2>{table([x['slug'] for x in ts])}<ul class='sr'>{li}</ul>" + (f"<h2>Guides</h2><ul>{rel}</ul>" if rel else ""),
            [crumbs([("Home","/"),(t["name"],path)])]))
    PIMG = {slug: k for _, slug, k in page_targets()}
    # tools
    for x in tools.values():
        path = f"/tools/{x['slug']}/"
        plans = "".join(f"<tr><td>{p['name']}</td><td>{p['users']}</td><td>{p['monthly_no_commit']}</td><td>{p['annual']}</td></tr>" for p in x["plans"])
        key = x["slug"].replace("-","")
        cta = afflink(key, f"Visit {x['name']}") if key in aff else ""
        write(path, layout(path, f"{x['name']} Pricing & Features ({LC[:4]}): Sourced Overview", f"{x['name']} plans, prices, trial and key features from the vendor's public pricing page, last checked {LC}.",
            f"{pic(PIMG['tools/'+x['slug']])}<h1>{x['name']}: pricing and features</h1>{trustbar()}<div class='summary card'><p class='bf'><span class='lbl'>Best for</span> {e(x.get('best_for','unknown'))}</p><p class='price'><span class='lbl'>Starting price</span> {e(x.get('starting_price','unknown'))}</p>{proscons(x)}<div class='actions'>{cta}</div></div><h2>Plans</h2><div class='tw' tabindex='0' role='region' aria-label='Plans table'><table><tr><th>Plan</th><th>Users</th><th>Monthly</th><th>Annual</th></tr>{plans}</table></div><h2>Key facts</h2><ul class='facts'><li>Trial: {x['free_trial']}</li><li>Contract: {x['contract']}</li><li>Extra users/units: {x['extra_user']}</li><li>Routing: {x['routing']}</li><li>Payments: {x['card_fee']}</li><li>Rating: {x['rating']}</li></ul><p>Sources: "+" ".join(f'<a href="{s}" rel="nofollow">{s}</a>' for s in x['sources'])+"</p>"+(("<h2>Guides featuring "+x['name']+"</h2><ul>"+"".join(f'<li><a href="/{p["slug"]}/">{e(p["h1"])}</a></li>' for p in pages if x['slug'] in p.get('tools',[]))+"</ul>") if any(x['slug'] in p.get('tools',[]) for p in pages) else "")+f"<div class='actions'>{cta}</div>",
            [crumbs([("Home","/"),(x["name"],path)]),{"@context":"https://schema.org","@type":"SoftwareApplication","name":x["name"],"applicationCategory":"BusinessApplication","url":x["website"]}]))
    # articles
    for p in pages:
        path = f"/{p['slug']}/"
        faq = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in p.get("faq",[]))
        sch = [crumbs([("Home","/"),(p["h1"],path)]),{"@context":"https://schema.org","@type":"Article","headline":p["h1"],"dateModified":LC,"author":{"@type":"Organization","name":site["name"]}}]
        if p.get("faq"): sch.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]})
        write(path, layout(path, p["title"], p["description"], f"{pic(PIMG[p['slug']])}<h1>{e(p['h1'])}</h1>{trustbar()}{render(p['body'])}" + (f"<h2>FAQ</h2>{faq}" if faq else ""), sch))
    build_directory()
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{LC}</lastmod></url>" for u in urls) + "</urlset>\n")
    (OUT/"CNAME").write_text(urlparse(BASE).netloc + "\n")
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"Built {len(urls)} pages -> {OUT}")
if __name__ == "__main__": build()
