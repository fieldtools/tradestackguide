#!/usr/bin/env python3
"""Check internal href/src links in dist/ resolve to built files. Exit 1 on broken links."""
import re, sys
from pathlib import Path
D = Path(__file__).resolve().parent.parent / "dist"
bad = []
for f in D.rglob("*.html"):
    for u in re.findall(r'(?:href|src)="([^"]+)"', f.read_text()):
        if u.startswith(("http", "//", "mailto:", "tel:", "#", "data:")): continue
        path = u.split("#")[0].split("?")[0]
        if not path.startswith("/"): path = "/" + str(f.parent.relative_to(D)) + "/" + path
        t = D / path.lstrip("/")
        if not (t.is_file() or (t / "index.html").is_file()): bad.append(f"{f.relative_to(D)} -> {u}")
print("\n".join(bad) or "No broken internal links"); sys.exit(1 if bad else 0)
