#!/usr/bin/env python3
"""Build TradeStackGuide static site from data/*.json into dist/. No dependencies."""
import json, re, shutil, html
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

def layout(path, title, desc, body, schema=None):
    nav = "".join(f'<a href="/trades/{t["slug"]}/">{t["name"]}</a>' for t in trades)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in (schema or []))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{BASE}{path}">
<link rel="stylesheet" href="/style.css">{ld}</head><body><header><a class="logo" href="/">{site['name']}</a><nav>{nav}<a href="/about/">Methodology</a></nav></header>
<main>{body}</main><footer><p>Last checked: {LC}. Some links may be affiliate links; see our <a href="/about/#disclosure">disclosure</a>. Prices come from vendor pages and can change.</p></footer></body></html>"""

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
    return f'<div class="tw"><table>{h}{b}</table></div><p class="note">Prices as published (monthly no-commitment / annual where shown). "unknown" = not published. Checked {LC}.</p>'

def render(body):
    body = re.sub(r"\{\{table:([^}]+)\}\}", lambda m: table(m.group(1).split(",")), body)
    return re.sub(r"\{\{aff:([a-z0-9-]+)\|([^}]+)\}\}", lambda m: afflink(m.group(1), m.group(2)), body)

def crumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

def build():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(); shutil.copy(R/"static/style.css", OUT/"style.css")
    # home
    cards = "".join(f'<li><a href="/trades/{t["slug"]}/">{t["name"]} software</a></li>' for t in trades)
    arts = "".join(f'<li><a href="/{p["slug"]}/">{e(p["h1"])}</a></li>' for p in pages)
    write("/", layout("/", f"{site['name']}: Software Comparisons for Pool, Pest, Lawn & Cleaning Pros",
        "Sourced, no-fluff comparisons of scheduling, routing and invoicing software for small pool, pest control, lawn care, window cleaning and pressure washing businesses.",
        f"<h1>Find the right software for your service business</h1><p>{site['tagline']}. Every price links to its source. If a number isn't public, we say unknown.</p><h2>Browse by trade</h2><ul class='grid'>{cards}</ul><h2>Guides</h2><ul>{arts}</ul>",
        [{"@context":"https://schema.org","@type":"WebSite","name":site["name"],"url":BASE+"/"}]))
    # about
    write("/about/", layout("/about/", f"About & Methodology | {site['name']}", "How TradeStackGuide collects pricing and feature data, how often it's checked, and how we make money (affiliate disclosure).",
        f"""<h1>About and methodology</h1><h2>How we collect data</h2><p>We only use information published on each vendor's own public pricing and feature pages. Each tool entry lists its source URLs and a last-checked date (currently {LC}). We don't invent ratings, review scores or prices. Anything a vendor doesn't publish is marked <em>unknown</em>.</p>
<h2>How often we update</h2><p>We re-check prices on a rolling basis and at least quarterly. Promotions change often, so always confirm on the vendor's site.</p>
<h2 id="disclosure">Affiliate disclosure</h2><p>Some links on this site are affiliate or referral links. If you sign up through them, we may earn a commission at no extra cost to you. Commissions never affect the data we publish, and we list tools whether or not they have an affiliate program.</p>"""))
    # trades
    for t in trades:
        ts = [x for x in tools.values() if t["key"] in x["trades"]]
        rel = "".join(f'<li><a href="/{p["slug"]}/">{e(p["h1"])}</a></li>' for p in pages if t["key"] in p["trades"])
        li = "".join(f'<li><a href="/tools/{x["slug"]}/">{x["name"]}</a>: from {x["plans"][0]["monthly_no_commit"]}</li>' for x in ts)
        path = f"/trades/{t['slug']}/"
        write(path, layout(path, f"{t['name']} Business Software: Tools, Prices & Comparisons ({LC[:4]})",
            f"{t['name']} software compared: {', '.join(x['name'] for x in ts)}. Published prices, trials and features with sources, last checked {LC}.",
            f"<h1>{t['name']} software</h1><p>{t['intro']}</p>{table([x['slug'] for x in ts])}<h2>Tools</h2><ul>{li}</ul>" + (f"<h2>Guides</h2><ul>{rel}</ul>" if rel else ""),
            [crumbs([("Home","/"),(t["name"],path)])]))
    # tools
    for x in tools.values():
        path = f"/tools/{x['slug']}/"
        plans = "".join(f"<tr><td>{p['name']}</td><td>{p['users']}</td><td>{p['monthly_no_commit']}</td><td>{p['annual']}</td></tr>" for p in x["plans"])
        key = x["slug"].replace("-","")
        cta = afflink(key, f"Visit {x['name']}") if key in aff else ""
        write(path, layout(path, f"{x['name']} Pricing & Features ({LC[:4]}): Sourced Overview", f"{x['name']} plans, prices, trial and key features from the vendor's public pricing page, last checked {LC}.",
            f"<h1>{x['name']}: pricing and features</h1><div class='tw'><table><tr><th>Plan</th><th>Users</th><th>Monthly</th><th>Annual</th></tr>{plans}</table></div><ul><li>Trial: {x['free_trial']}</li><li>Contract: {x['contract']}</li><li>Extra users/units: {x['extra_user']}</li><li>Routing: {x['routing']}</li><li>Payments: {x['card_fee']}</li><li>Rating: {x['rating']}</li></ul><p>Sources: "+" ".join(f'<a href="{s}" rel="nofollow">{s}</a>' for s in x['sources'])+f"</p>{cta}",
            [crumbs([("Home","/"),(x["name"],path)]),{"@context":"https://schema.org","@type":"SoftwareApplication","name":x["name"],"applicationCategory":"BusinessApplication","url":x["website"]}]))
    # articles
    for p in pages:
        path = f"/{p['slug']}/"
        faq = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in p.get("faq",[]))
        sch = [crumbs([("Home","/"),(p["h1"],path)]),{"@context":"https://schema.org","@type":"Article","headline":p["h1"],"dateModified":LC,"author":{"@type":"Organization","name":site["name"]}}]
        if p.get("faq"): sch.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in p["faq"]]})
        write(path, layout(path, p["title"], p["description"], f"<h1>{e(p['h1'])}</h1><p class='note'>Last checked {LC}. Sourced from vendor pricing pages.</p>{render(p['body'])}" + (f"<h2>FAQ</h2>{faq}" if faq else ""), sch))
    (OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{LC}</lastmod></url>" for u in urls) + "</urlset>\n")
    (OUT/"CNAME").write_text(urlparse(BASE).netloc + "\n")
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"Built {len(urls)} pages -> {OUT}")
if __name__ == "__main__": build()
