#!/usr/bin/env python3
"""Genera /search-index.json a partir de sitemap.xml + el <title>/<meta description>
de cada pagina real del lloc. Cal re-executar-lo despres d'afegir o canviar pagines
indexables (noves entrades a blog/, nous articles, etc.)."""
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
OUT = ROOT / "search-index.json"

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

CATEGORY_LABELS = [
    (r"^/blog/", "Blog"),
    (r"^/partits/equips/", "Equips"),
    (r"^/partits/", "Partits"),
    (r"^/patrocinadors/partners/", "Partners"),
    (r"^/patrocinadors/", "Patrocinis"),
    (r"^/premidonaesport/", "Premi Dona i Esport"),
    (r"^/premsa/", "Premsa"),
    (r"^/escoleta/", "Escoleta"),
    (r"^/campus/", "Campus"),
    (r"^/3x3/", "3x3"),
    (r"^/opina/", "Opina"),
    (r"^/fotos", "Fotos"),
    (r"^/briefing/", "Briefing"),
]


def category_for(path):
    for pattern, label in CATEGORY_LABELS:
        if re.match(pattern, path):
            return label
    return "El club"


def url_to_file(url):
    path = url.replace("https://cbgrupbarna.info", "")
    if path == "":
        path = "/"
    fs_path = path.lstrip("/")
    if fs_path == "" or fs_path.endswith("/"):
        fs_path = fs_path + "index.html"
    return ROOT / fs_path, path


def extract(html):
    title_m = re.search(r"<title>([^<]*)</title>", html)
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    title = title_m.group(1).strip() if title_m else ""
    desc = desc_m.group(1).strip() if desc_m else ""
    return title, desc


def main():
    tree = ET.parse(SITEMAP)
    entries = []
    for url_el in tree.getroot().findall("s:url", NS):
        loc = url_el.find("s:loc", NS).text.strip()
        fs_path, path = url_to_file(loc)
        if not fs_path.exists():
            print(f"AVIS: {loc} -> {fs_path} no existeix, s'ignora")
            continue
        html = fs_path.read_text(encoding="utf-8", errors="ignore")
        if 'name="robots" content="noindex' in html:
            continue
        title, desc = extract(html)
        if not title:
            continue
        entries.append({
            "url": path,
            "title": title.split(" · ")[0].split(" | ")[0].strip() or title,
            "full_title": title,
            "desc": desc,
            "cat": category_for(path),
        })

    entries.sort(key=lambda e: e["url"])
    OUT.write_text(json.dumps(entries, ensure_ascii=False, indent=0, separators=(",", ":")), encoding="utf-8")
    print(f"Escrites {len(entries)} entrades a {OUT}")


if __name__ == "__main__":
    main()
