#!/usr/bin/env python3
"""Fa que un enllaç d'una pàgina traduïda porti a la mateixa llengua.

PER QUÈ. `i18n/README.md` ho diu amb totes les lletres: posar al menú
castellà un enllaç que porta a una pàgina en català és pitjor que no
posar-l'hi. El mateix val per al cos de la pàgina. Mesurat el 2026-08-24,
487 enllaços de pàgines /es/ i /en/ portaven a l'adreça catalana d'una
pàgina que existeix en aquella llengua: 190 destins diferents, entre ells
/blog/, /premsa/, /club/, /escoleta/ i /partits/.

QUÈ FA. Per a cada pàgina de /es/ i /en/, mira els seus <a href> que
apunten a una adreça catalana i, si `i18n/routes.yml` diu que aquella
pàgina existeix en la llengua de qui llegeix, hi canvia el destí.

QUÈ NO TOCA, i per què:

  - El commutador d'idioma (`.lang-switch`) i qualsevol enllaç amb
    `hreflang`: la seva feina és justament creuar de llengua.
  - Els enllaços el text visible dels quals és una adreça
    («cbgrupbarna.info/partits»): canviar-ne el destí faria que el text
    digués una cosa i l'enllaç en portés una altra.
  - Els <link> de la capçalera: canonical i alternate no són navegació.

    python3 scripts/i18n-enllacos.py             # aplica
    python3 scripts/i18n-enllacos.py --check     # només compta (per a la CI)
"""
import argparse
import json
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
MAPA = ARREL / 'js' / 'nav-i18n.js'

RE_ANCORA = re.compile(r'<a\b[^>]*>', re.I)
RE_HREF = re.compile(r'href="(/[^"]*)"')
RE_ADRECA = re.compile(r'^\s*(https?://|www\.|cbgrupbarna\.info)', re.I)


def per_idioma():
    """{adreça catalana: {es: …, en: …}}, del mapa que ja es genera."""
    text = MAPA.read_text(encoding='utf-8')
    trios = json.loads(re.search(r'=\s*(\[[\s\S]*?\]);', text).group(1))
    return {t[0]: {'es': t[1] or None, 'en': t[2] or None} for t in trios}


def dins_del_commutador(html, pos):
    """Si aquesta posició cau dins d'un bloc .lang-switch."""
    obre = html.rfind('lang-switch', 0, pos)
    if obre == -1:
        return False
    tanca = html.find('</div>', obre)
    return tanca == -1 or pos < tanca


def arregla(html, idioma, mapa):
    canvis = []

    def una(m):
        etiqueta = m.group(0)
        h = RE_HREF.search(etiqueta)
        if not h:
            return etiqueta
        desti = h.group(1)
        if desti.startswith(('/es/', '/en/')):
            return etiqueta
        if 'hreflang' in etiqueta.lower():
            return etiqueta
        if dins_del_commutador(html, m.start()):
            return etiqueta
        # El fragment i la consulta es conserven tal com estan.
        cami = desti.split('#')[0].split('?')[0]
        resta = desti[len(cami):]
        nou = (mapa.get(cami) or {}).get(idioma)
        if not nou:
            return etiqueta
        # El text visible: si és una adreça, el destí ha de continuar sent
        # el que diu el text.
        fi = html.find('</a>', m.end())
        text = re.sub(r'<[^>]+>', '', html[m.end():fi]) if fi != -1 else ''
        if RE_ADRECA.match(text):
            return etiqueta
        canvis.append((desti, nou + resta))
        return etiqueta.replace(f'href="{desti}"', f'href="{nou + resta}"')

    return RE_ANCORA.sub(una, html), canvis


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='no escriu res; falla si en queda cap')
    args = ap.parse_args()

    mapa = per_idioma()
    total, fitxers = 0, 0
    for idioma in ('es', 'en'):
        for f in sorted((ARREL / idioma).rglob('*.html')):
            # El Premi Dona i Esport no s'hi toca: decisió de l'Ana
            # (24/08/2026). És el mirall local d'una candidatura que viu a
            # la web oficial, i qualsevol canvi aquí la fa divergir.
            if 'premidonaesport' in f.parts:
                continue
            html = f.read_text(encoding='utf-8')
            nou, canvis = arregla(html, idioma, mapa)
            if not canvis:
                continue
            total += len(canvis)
            fitxers += 1
            if args.check:
                print(f"✗ {f.relative_to(ARREL)} · {len(canvis)} enllaços a l'altra llengua",
                      file=sys.stderr)
            else:
                f.write_text(nou, encoding='utf-8')

    if args.check:
        if total:
            print(f"\n{total} enllaços de pàgines traduïdes porten a la versió catalana.\n"
                  f"  Arregleu-ho: python3 scripts/i18n-enllacos.py", file=sys.stderr)
            return 1
        print("✓ cap enllaç d'una pàgina traduïda porta a la versió catalana")
        return 0
    print(f"{total} enllaços redirigits a la seva llengua · {fitxers} fitxers")
    return 0


if __name__ == '__main__':
    sys.exit(main())
