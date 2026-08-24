#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Posa el cercador a totes les pàgines que tenen la capçalera del club.

  python3 scripts/afegeix-cerca.py --dry-run   # mira què faria
  python3 scripts/afegeix-cerca.py             # ho fa

Afegeix dues línies i prou:
  <link rel="stylesheet" href="/css/cerca.css">   just abans de </head>
  <script src="/js/cerca.js" defer></script>      just abans de </body>

El botó de la lupa no s'escriu a l'HTML: el planta /js/cerca.js dins de la
capçalera que hi hagi. Així una pàgina nova només ha de portar aquestes dues
línies, i no cal tocar el marcatge de cap capçalera.

És idempotent: passar-l'hi dues vegades no duplica res. Cal tornar-l'hi a
passar quan es publiquen pàgines noves (o executar-lo dins del mateix pas que
les genera).

Salta: /admin/, l'app /galeria/, els residus de /patrocinis/, /presentacio/ i
/dossier-patrocinis/, i les proves.
"""

import os
import re
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = '<link rel="stylesheet" href="/css/cerca.css">'
JS = '<script src="/js/cerca.js" defer></script>'

# Les carpetes van pel nom que tenen al disc, i cada idioma té el seu: quan
# es van traduir les presentacions, /es/presentacion/ i /en/presentation/ no
# eren a la llista i van sortir amb lupa mentre la catalana no en tenia. Una
# pàgina que canvia en dos idiomes i no en el tercer és exactament el que
# atura la comprovació de paritat, i amb raó.
EXCLOSES = ("galeria", "admin", "patrocinis",
            "presentacio", "presentacion", "presentation",
            "dossier-patrocinis", "dosier-patrocinios", "sponsorship-pack",
            "tests", "node_modules", "workers")


def cal(cami):
    rel = os.path.relpath(cami, ARREL).replace(os.sep, "/")
    trossos = rel.split("/")
    return not any(t in EXCLOSES for t in trossos[:-1])


def main():
    prova = "--dry-run" in sys.argv
    tocats, ja, sense_cap = 0, 0, 0

    for arrel, dirs, fitxers in os.walk(ARREL):
        dirs[:] = [d for d in dirs if d not in EXCLOSES and not d.startswith(".")]
        for f in sorted(fitxers):
            if not f.endswith(".html"):
                continue
            cami = os.path.join(arrel, f)
            if not cal(cami):
                continue
            s = open(cami, encoding="utf-8").read()

            # Sense capçalera del club no hi ha on posar la lupa.
            if 'class="head"' not in s:
                sense_cap += 1
                continue
            # Les redireccions no són pàgines.
            if re.search(r'http-equiv=["\']refresh', s, re.I):
                continue

            te_css, te_js = CSS in s, "/js/cerca.js" in s
            if te_css and te_js:
                ja += 1
                continue

            nou = s
            if not te_css and "</head>" in nou:
                nou = nou.replace("</head>", CSS + "\n</head>", 1)
            if not te_js and "</body>" in nou:
                nou = nou.replace("</body>", JS + "\n</body>", 1)
            if nou == s:
                continue

            rel = os.path.relpath(cami, ARREL)
            if prova:
                print("  afegiria  " + rel)
            else:
                open(cami, "w", encoding="utf-8").write(nou)
            tocats += 1

    print(("(prova) " if prova else "") +
          f"{tocats} pàgines amb cerca nova · {ja} ja la tenien · "
          f"{sense_cap} sense capçalera del club (no s'hi toca)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
