#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Afegeix, a /premsa/instagram/ (ca/es/en), un bloc JSON-LD amb un
VideoObject (reels) o ImageObject (posts) per a cada publicacio incrustada
—a partir NOMES de dades que ja son al fitxer: la URL, el tag i el peu de
foto. La URL mateixa diu si es un reel (video) o un post: /reel/ vs /p/.

NO inclou uploadDate ni thumbnailUrl: Instagram no les dona sense anar a
buscar-les publicacio a publicacio, i inventar-les seria pitjor que no
posar-les. Un bloc sense aquests dos camps no es candidat als resultats
enriquits de vídeo de Google, però segueix sent estructura real i útil per
a qualsevol assistent d'IA que llegeixi el JSON-LD.

El bloc queda entre <!-- IG-SCHEMA:START --> i <!-- IG-SCHEMA:END -->,
just abans de </main>. L'script es nega a tocar un fitxer que ja el porti
(torna a executar-lo per actualitzar-lo: cal esborrar el bloc a mà primer).

  python3 scripts/inject-ig-schema.py --dry-run
  python3 scripts/inject-ig-schema.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    ("premsa/instagram/index.html", "https://cbgrupbarna.info/premsa/instagram/"),
    ("es/premsa/instagram/index.html", "https://cbgrupbarna.info/es/premsa/instagram/"),
    ("en/premsa/instagram/index.html", "https://cbgrupbarna.info/en/premsa/instagram/"),
]

FIGURE_RE = re.compile(
    r'<figure class="igx"><div class="igx-media" data-ig="(?P<url>[^"]+)">.*?'
    r'<figcaption class="igx-cap"><span class="igx-tag">(?P<tag>[^<]*)</span>'
    r'<p>(?P<caption>[^<]*)</p>',
    re.S,
)

MARKER_START = "<!-- IG-SCHEMA:START -->"
MARKER_END = "<!-- IG-SCHEMA:END -->"


def build_graph(path, page_url):
    text = path.read_text(encoding="utf-8")
    entries = FIGURE_RE.findall(text)
    if not entries:
        raise SystemExit(f"Cap publicacio trobada a {path}")
    graph = []
    for url, tag, caption in entries:
        url = html.unescape(url).rstrip("/")
        tag = html.unescape(tag).strip()
        caption = html.unescape(caption).strip()
        is_reel = "/reel/" in url
        name = tag if tag else caption[:80]
        node = {
            "@type": "VideoObject" if is_reel else "ImageObject",
            "url": url + "/",
            "name": name,
            "description": caption if caption else tag,
            "contentUrl": url + "/",
            "isPartOf": {"@id": page_url + "#page"},
            "publisher": {"@id": "https://cbgrupbarna.info/#club"},
        }
        if is_reel:
            node["embedUrl"] = url + "/embed"
        graph.append(node)
    return graph, len(entries)


def inject(path, graph):
    text = path.read_text(encoding="utf-8")
    if MARKER_START in text:
        raise SystemExit(f"{path} ja te el marcador IG-SCHEMA")
    payload = {"@context": "https://schema.org", "@graph": graph}
    block = (
        MARKER_START
        + '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "</script>"
        + MARKER_END
    )
    idx = text.index("</main>")
    text = text[:idx] + block + "\n" + text[idx:]
    path.write_text(text, encoding="utf-8")


def main():
    dry = "--dry-run" in sys.argv
    for rel, page_url in PAGES:
        path = ROOT / rel
        graph, n = build_graph(path, page_url)
        videos = sum(1 for g in graph if g["@type"] == "VideoObject")
        images = n - videos
        cap = "(prova) " if dry else ""
        print(f"{cap}{rel}: {n} publicacions ({videos} VideoObject, {images} ImageObject)")
        if not dry:
            inject(path, graph)


if __name__ == "__main__":
    main()
