#!/usr/bin/env python3
"""
Repassa les pàgines traduïdes i porta els enllaços interns cap a la versió
del mateix idioma quan n'hi ha.

    python3 scripts/i18n-enllacos.py            # diu què canviaria
    python3 scripts/i18n-enllacos.py --escriu   # ho canvia

El muntador ja ho fa quan assembla una pàgina, però només mirava
/<idioma>/<mateix nom>. Les pàgines amb el nom traduït —
/campus-basquet-barcelona/ es publica a /es/campus-baloncesto-barcelona/ —
se li escapaven, i el lector en castellà acabava a una pàgina en català.
Aquí es mira i18n/routes.yml, que és on consta cada trio.

No toca el commutador d'idioma ni els <link rel="alternate">: aquells han
d'apuntar a l'altre idioma a propòsit.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RE_ENLLAC = re.compile(r'((?:href|action)=["\'])(/[^"\'#?]*)([^"\']*)(["\'])', re.I)
RE_COMMUTADOR = re.compile(r'(?is)<(div|nav) class="lang-switch".*?</\1>')
RE_ALTERNATE = re.compile(r'(?i)<link[^>]+rel=["\']alternate["\'][^>]*>')
MARCA = "\x00i18n\x00%d\x00"


def mapa():
    dades = yaml.safe_load((ROOT / "i18n" / "routes.yml").read_text(encoding="utf-8")) or {}
    return {g["ca"]: g for g in dades.get("rutes", []) if g.get("ca")}


def fitxer_de(url):
    resta = url.lstrip("/")
    return ROOT / (resta + "index.html" if url.endswith("/") else resta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escriu", action="store_true")
    args = ap.parse_args()

    rutes = mapa()
    total_pagines = total_enllacos = 0

    for idioma in ("es", "en"):
        for fitxer in sorted((ROOT / idioma).rglob("*.html")):
            html = original = fitxer.read_text(encoding="utf-8")

            # Les parts que no s'han de tocar, fora un moment.
            guardats = []

            def aparca(m):
                guardats.append(m.group(0))
                return MARCA % (len(guardats) - 1)

            html = RE_COMMUTADOR.sub(aparca, html)
            html = RE_ALTERNATE.sub(aparca, html)

            canvis = []

            def canvia(m):
                obre, ruta, cua, tanca = m.groups()
                if ruta.startswith(("/es/", "/en/")):
                    return m.group(0)
                desti = (rutes.get(ruta) or {}).get(idioma)
                if not desti or not fitxer_de(desti).exists():
                    return m.group(0)
                canvis.append((ruta, desti))
                return f"{obre}{desti}{cua}{tanca}"

            html = RE_ENLLAC.sub(canvia, html)
            for i, tros in enumerate(guardats):
                html = html.replace(MARCA % i, tros, 1)

            if not canvis:
                continue
            total_pagines += 1
            total_enllacos += len(canvis)
            print(f"  /{fitxer.relative_to(ROOT)} · {len(canvis)} enllaços")
            if args.escriu:
                fitxer.write_text(html, encoding="utf-8")
            elif html == original:
                print("    (res a fer)")

    print(f"\n{total_enllacos} enllaços a {total_pagines} pàgines")
    if not args.escriu and total_enllacos:
        print("Res escrit. Torna-hi amb --escriu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
