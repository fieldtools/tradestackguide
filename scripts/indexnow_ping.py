#!/usr/bin/env python3
"""IndexNow ping: diff dist/sitemap.xml vs previously deployed sitemap; submit new/changed URLs.
Usage: indexnow_ping.py fetch  (save live sitemap to prev file, before deploy)
       indexnow_ping.py ping   (after deploy). Never fails: always exits 0."""
import json, sys, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
R = Path(__file__).resolve().parent.parent
HOST = "tradestackguide.com"; KEY = (R/"static/indexnow-key.txt").read_text().strip()
PREV = Path("/tmp/prev_sitemap.xml"); NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
def parse(xml):
    out = {}
    for u in ET.fromstring(xml).iter(NS+"url"):
        loc = u.findtext(NS+"loc"); out[loc] = u.findtext(NS+"lastmod") or ""
    return out
def main():
    if sys.argv[1:] == ["fetch"]:
        try:
            with urllib.request.urlopen(f"https://{HOST}/sitemap.xml", timeout=20) as r: PREV.write_bytes(r.read())
            print("saved previous sitemap")
        except Exception as ex: print("no previous sitemap:", ex); PREV.unlink(missing_ok=True)
        return
    new = parse((R/"dist/sitemap.xml").read_text())
    try: old = parse(PREV.read_text()); first = False
    except Exception: old = {}; first = True
    urls = [u for u, lm in new.items() if first or old.get(u) != lm]
    urls = [u for u in urls if urlparse(u).netloc == HOST][:10000]
    print(f"{'first run: ' if first else ''}{len(urls)} new/changed URLs of {len(new)}")
    if not urls: return
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow response:", r.status, r.read()[:300])
    except urllib.error.HTTPError as ex: print("IndexNow response:", ex.code, ex.read()[:300])
    except Exception as ex: print("IndexNow error:", ex)
if __name__ == "__main__":
    try: main()
    except Exception as ex: print("indexnow_ping error (ignored):", ex)
    sys.exit(0)
