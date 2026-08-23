#!/usr/bin/env python3
"""
Escriu els hreflang de cada pàgina a partir de i18n/routes.yml.

    python3 scripts/i18n-hreflang.py --dry-run   # què canviaria
    python3 scripts/i18n-hreflang.py             # ho escriu

Fins ara aquests enllaços s'escrivien a mà, pàgina per pàgina i article per
article —al generador n'hi havia llistes senceres copiades—, i per això n'hi
havia que no hi eren, que no es corresponien i que apuntaven a pàgines que ja
no existien. Són el que li diu a Google que /blog/, /es/blog/ i /en/blog/ són
la mateixa pàgina en tres idiomes i no contingut duplicat: quan fallen, els
cercadors trien ells quina versió ensenyen, i sovint trien malament.

Ara surten d'un sol lloc. El mapa ja sap quina pàgina és quina en cada idioma;
això només ho escriu.

Regles:

  · Cada pàgina d'un grup declara TOTES les versions del grup, la seva
    inclosa. Un hreflang que no és recíproc és un hreflang que Google ignora.
  · L'`x-default` apunta al català, que és la versió per defecte del lloc.
  · El bloc va just després del <link rel="canonical">, que és on ja era.
  · Els grups on la pàgina catalana és `noindex` es deixen estar i es
    diuen pel nom: enllaçar com a versió principal una pàgina que hem tret
    de l'índex és pitjor que no declarar res.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAPA = ROOT / "i18n" / "routes.yml"
SITE = "https://cbgrupbarna.info"

RE_CANONICAL = re.compile(r'([ \t]*)<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
RE_ALTERNATE = re.compile(
    r'[ \t]*<link[^>]+rel=["\']alternate["\'][^>]*hreflang=["\'][^"\']+["\'][^>]*>[ \t]*\n?', re.I)
RE_NOINDEX = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def bloc(grup, sagnat=""):
    """Els <link rel=alternate> d'un grup, en ordre fix: ca, es, en, x-default.

    El sagnat surt de la línia del canonical: hi ha pàgines amb el <head>
    indentat i d'altres sense, i el bloc s'ha de posar com estigui la seva.
    """
    linies = [f'{sagnat}<link rel="alternate" hreflang="{idioma}" href="{SITE}{grup[idioma]}">'
              for idioma in ("ca", "es", "en") if grup.get(idioma)]
    linies.append(f'{sagnat}<link rel="alternate" hreflang="x-default" href="{SITE}{grup["ca"]}">')
    return "\n".join(linies)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rutes = (yaml.safe_load(MAPA.read_text(encoding="utf-8")) or {}).get("rutes", [])
    tocades, saltades, sense_canonical = 0, [], []

    for grup in rutes:
        if not any(grup.get(i) for i in ("es", "en")):
            continue
        if RE_NOINDEX.search(fitxer_de(grup["ca"]).read_text(encoding="utf-8", errors="ignore")):
            saltades.append(grup["ca"])
            continue

        for idioma in ("ca", "es", "en"):
            url = grup.get(idioma)
            if not url:
                continue
            fitxer = fitxer_de(url)
            text = fitxer.read_text(encoding="utf-8", errors="ignore")
            canonical = RE_CANONICAL.search(text)
            if not canonical:
                sense_canonical.append(url)
                continue
            # Fora els que hi havia i, al mateix lloc, els que toquen.
            net = RE_ALTERNATE.sub("", text)
            canonical = RE_CANONICAL.search(net)
            tall = canonical.end()
            # Hi ha pàgines amb tot el <head> en una sola línia: allà el bloc
            # s'obre amb un salt de línia i es torna a tancar, per no deixar
            # el que venia després enganxat a l'últim hreflang.
            enganxat = net[tall:tall + 1] not in ("\n", "")
            final = (net[:tall] + "\n" + bloc(grup, canonical.group(1))
                     + ("\n" if enganxat else "") + net[tall:])
            if final != text:
                tocades += 1
                if not args.dry_run:
                    fitxer.write_text(final, encoding="utf-8")

    print(f"{tocades} pàgines amb els hreflang reescrits"
          + (" (no s'ha desat res)" if args.dry_run else " · desat"))
    if saltades:
        print(f"\n{len(saltades)} grups saltats perquè el català és noindex:")
        for u in saltades:
            print(f"  {u}")
    if sense_canonical:
        print(f"\n{len(sense_canonical)} pàgines sense <link rel=canonical>, que és on va el bloc:")
        for u in sense_canonical:
            print(f"  {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
