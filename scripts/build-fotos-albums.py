#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera una pagina estatica i rastrejable per a cada album de fotos/web/,
amb graella d'<img> real i JSON-LD ImageObject amb les URL reals.

PER QUE EXISTEIX
-----------------
/fotos/ es una sola URL que carrega les 1.709 fotos amb JavaScript des de
fotos/events.js. Cap robot que no executi JavaScript (i molts assistents
d'IA no ho fan) no en veu cap ni una. Aquest script no toca la galeria
interactiva: afegeix, per cada album real (source:"repo" a events.js, els
que tenen les fotos al mateix repositori), una pagina prima nomes-lectura a
/fotos/<id>/ amb totes les fotos com a <img> normals i el seu propi bloc
ImageObject, perque hi hagi almenys una URL rastrejable per album.

L'album "3x3-westfield-glories-2026" no te fotos al repositori (venen de
Google Drive, camp "source": null): es queda fora, no se li inventa cap URL.

events.js llista els noms de fitxer amb l'extensio d'ABANS de convertir-los
a webp (un .jpg que ara es .webp): aquest script llegeix el DISC, no la
llista de events.js, per no publicar cap URL trencada.

  python3 scripts/build-fotos-albums.py --dry-run
  python3 scripts/build-fotos-albums.py
"""
import html
import json
import os
import re
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS = os.path.join(ARREL, "fotos", "events.js")
BASE = "https://cbgrupbarna.info"


def carrega_events():
    text = open(EVENTS, encoding="utf-8").read()
    m = re.search(r"window\.GALERIA_EVENTS\s*=\s*(\[.*\]);?\s*$", text, re.S)
    return json.loads(m.group(1))


def titol_net(t):
    """events.js sol portar el titol tot en majuscules. Nomes es transforma
    la caixa (MAJUSCULES -> Frase capitalitzada); el text en si, mai."""
    t = t.strip()
    if t and t == t.upper():
        return t.capitalize()
    return t


def pagina(event, fitxers):
    slug = event["id"]
    url = f"{BASE}/fotos/{slug}/"
    titol_raw = titol_net(event["title"].strip())
    titol = html.escape(titol_raw, quote=True)
    data = event.get("date")
    n = len(fitxers)

    imgs = "".join(
        f'<a class="ag-item" href="/fotos/web/{slug}/{f}" target="_blank" rel="noopener">'
        f'<img src="/fotos/web/{slug}/{f}" alt="{titol}" loading="lazy" decoding="async"></a>'
        for f in fitxers
    )

    image_objects = [
        {
            "@type": "ImageObject",
            "contentUrl": f"{BASE}/fotos/web/{slug}/{f}",
            "url": f"{BASE}/fotos/web/{slug}/{f}",
        }
        for f in fitxers
    ]
    graph = [
        {
            "@type": "CollectionPage",
            "@id": url + "#page",
            "url": url,
            "name": f"{titol_raw} · Galeria · CB Grup Barna",
            "description": f"{n} fotografies de «{titol_raw}», del CB Grup Barna.",
            "inLanguage": "ca",
            "isPartOf": {"@id": f"{BASE}/#website"},
            "about": {"@id": f"{BASE}/#club"},
            "hasPart": [{"@id": io["url"]} for io in image_objects],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inici", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Fotos", "item": f"{BASE}/fotos/"},
                {"@type": "ListItem", "position": 3, "name": titol_raw, "item": url},
            ],
        },
    ] + image_objects
    if data:
        graph[0]["datePublished"] = data

    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

    data_line = f'<p class="eyebrow" style="margin-top:8px">{data}</p>' if data else ""

    return f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10100E">
<title>{titol} · Galeria · CB Grup Barna</title>
<meta name="description" content="{n} fotografies de «{titol}», del CB Grup Barna.">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="ca_ES">
<meta property="og:title" content="{titol} · Galeria · CB Grup Barna">
<meta property="og:description" content="{n} fotografies de «{titol}», del CB Grup Barna.">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/fotos/web/{slug}/{fitxers[0]}">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/barna.css">
<style>
.ag-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px;margin-top:28px}}
.ag-item{{display:block;aspect-ratio:1;overflow:hidden;background:var(--line)}}
.ag-item img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s}}
.ag-item:hover img{{transform:scale(1.04)}}
</style>
<script type="application/ld+json">
{jsonld}
</script>
<link rel="stylesheet" href="/css/a11y.css">
</head>
<body>
<a href="#main" class="skip">Saltar al contingut</a>
<header class="head">
  <div class="head-in">
    <a class="head-brand" href="/" aria-label="CB Grup Barna · inici">
      <img src="/logo.png" alt="Escut del CB Grup Barna" width="30" height="30">
      <span>CB Grup Barna</span>
    </a>
    <nav class="head-nav" aria-label="Navegació principal">
      <a href="/partits/equips/">Equips</a>
      <a href="/club/">Club</a>
      <a href="/partits/">Calendari</a>
      <a href="/fotos/" class="opt">Fotos</a>
    </nav>
  </div>
</header>
<main id="main">
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="/">Inici</a> · <a href="/fotos/">Fotos</a> · <span>{titol}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">Galeria · {n} fotos</p>
    <h1>{titol}</h1>
    {data_line}
    <p class="lede">Totes les fotografies de «{titol}» del CB Grup Barna. Per navegar-les amb el visor interactiu, <a href="/fotos/">torna a la galeria</a>.</p>
  </div>
  <div class="ag-grid">{imgs}</div>
</div>
</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-btm">
      <div class="foot-mark">#Som<em>Clot</em></div>
      <div class="foot-legal">© 2026 CB Grup Barna · Bàsquet base al Clot des de 1965</div>
    </div>
  </div>
</footer>
</body>
</html>
"""


def main():
    dry = "--dry-run" in sys.argv
    events = carrega_events()
    fets = []
    for e in events:
        if e.get("source") != "repo":
            print(f"  (fora) {e['id']} — no es del repositori, no se li fa pagina")
            continue
        d = os.path.join(ARREL, "fotos", "web", e["id"])
        if not os.path.isdir(d):
            print(f"  (fora) {e['id']} — no hi ha carpeta a fotos/web/")
            continue
        fitxers = sorted(os.listdir(d))
        if not fitxers:
            continue
        html = pagina(e, fitxers)
        out_dir = os.path.join(ARREL, "fotos", e["id"])
        out_file = os.path.join(out_dir, "index.html")
        print(f"{'(prova) ' if dry else ''}{e['id']}: {len(fitxers)} fotos -> fotos/{e['id']}/index.html")
        if not dry:
            os.makedirs(out_dir, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(html)
        fets.append((e["id"], len(fitxers)))
    print(f"\n{len(fets)} albums {'a generar' if dry else 'generats'}, {sum(n for _, n in fets)} fotos en total")


if __name__ == "__main__":
    main()
