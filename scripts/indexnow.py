#!/usr/bin/env python3
"""
Avisa els cercadors que unes URLs han canviat, sense esperar que hi tornin sols.

Google no fa servir IndexNow (allà cal el sitemap i la Search Console), però sí
Bing, Yandex, Seznam i Naver — i el que indexa Bing és el que acaben veient
ChatGPT i Copilot quan algú els pregunta per un club de bàsquet del Clot. Per a
un club petit, aquesta és la via ràpida perquè una pàgina nova existeixi als
assistents el mateix dia.

Com funciona: es publica un fitxer <clau>.txt a l'arrel del web amb la clau a
dins, i cada avís referencia aquesta clau. Així el cercador comprova que qui
avisa és qui mana al domini.

    python3 scripts/indexnow.py https://cbgrupbarna.info/blog/una-pagina/ ...

Sense arguments, avisa de tot el que hi ha al sitemap.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOST = "cbgrupbarna.info"
SITE = f"https://{HOST}"
LIMIT = 10000          # el màxim que accepta l'API en una tanda


def clau():
    """La clau és el nom del fitxer .txt de l'arrel, que en conté el valor."""
    for f in ROOT.glob("*.txt"):
        nom = f.stem
        if len(nom) >= 8 and all(c in "0123456789abcdef" for c in nom.lower()):
            if f.read_text(encoding="utf-8").strip() == nom:
                return nom
    return None


def urls_del_sitemap():
    arrel = ET.parse(ROOT / "sitemap.xml").getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    return [e.text.strip() for e in arrel.iter(f"{ns}loc") if e.text]


def avisar(urls, k):
    urls = [u for u in urls if u.startswith(SITE)][:LIMIT]
    if not urls:
        print("Cap URL per avisar.")
        return 0
    cos = json.dumps({
        "host": HOST,
        "key": k,
        "keyLocation": f"{SITE}/{k}.txt",
        "urlList": urls,
    }).encode("utf-8")
    peticio = urllib.request.Request(
        "https://api.indexnow.org/IndexNow",
        data=cos,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(peticio, timeout=30) as r:
            # 200 = acceptat · 202 = acceptat, clau pendent de verificar
            print(f"IndexNow {r.status} · {len(urls)} URLs enviades")
            return 0
    except Exception as e:
        # Que no falli mai el desplegament per això: és un avís, no un requisit.
        print(f"::warning::IndexNow no ha respost bé: {e}")
        return 0


if __name__ == "__main__":
    k = clau()
    if not k:
        print("::warning::No hi ha cap fitxer de clau IndexNow a l'arrel. No s'avisa ningú.")
        sys.exit(0)
    sys.exit(avisar(sys.argv[1:] or urls_del_sitemap(), k))
