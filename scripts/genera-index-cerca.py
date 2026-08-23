#!/usr/bin/env python3
"""Escriu `js/cerca-index.json`: el títol i l'adreça de cada pàgina pública.

Per què. El menú porta els 30 destins grans del club, però el lloc en té més
de 400: cada article, cada fitxa d'equip, cada partner. A aquestes s'hi
arriba des de la seva secció, i només si saps de quina secció pengen. Amb un
camp de cerca dins del menú s'hi arriba escrivint-ne el nom, que és el que fa
tothom quan no sap on és una cosa.

L'índex NO es carrega amb la pàgina: `js/nav.js` el demana el primer cop que
algú toca el camp de cerca. Qui no el faci servir no en paga res.

Què hi entra i què no:

  · Fora els panells d'administració, els generadors de cartells i les
    pàgines de 404: no són destins on algú vulgui anar a parar.
  · Fora les redireccions `noindex`: portarien a un lloc diferent del que
    diu el títol.
  · Cada entrada porta la llengua, perquè qui busca en català no ha de
    rebre resultats en anglès.

    python3 scripts/genera-index-cerca.py
    python3 scripts/genera-index-cerca.py --check    # per a la CI
"""
import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
SORTIDA = ARREL / 'js' / 'cerca-index.json'

EXCLOU_CARPETA = ('.git', 'node_modules', 'tests', '.github', 'galeria', '.claude')

# Pàgines que no són un destí: eines internes i pàgines d'error.
EXCLOU_RUTA = re.compile(
    r'(^|/)(admin|404|cartell|estadistiques|print|token)'
    r'|/admin\.html$|/token\.html$|(^|/)opina/print/',
    re.I)

RE_TITOL = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
RE_DESC = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', re.I | re.S)
RE_NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', re.I)
RE_REFRESH = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)

# El sufix de marca es repeteix a tots els títols i no ajuda a distingir res.
RE_SUFIX = re.compile(r'\s*[·|–—-]\s*(CB Grup Barna|Grup Barna|CBGB)\s*$', re.I)


def sense_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def pagines():
    for p in sorted(ARREL.rglob('*.html')):
        rel = p.relative_to(ARREL)
        if any(part in EXCLOU_CARPETA for part in rel.parts):
            continue
        url = '/' + rel.as_posix().replace('index.html', '')
        if EXCLOU_RUTA.search(url):
            continue
        yield p, url


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='no escriu; falla si no està al dia')
    args = ap.parse_args()

    entrades, sense_titol = [], []
    for cami, url in pagines():
        text = cami.read_text(encoding='utf-8', errors='replace')

        # Una redirecció porta a una altra banda: indexar-la enganya.
        if RE_NOINDEX.search(text) or RE_REFRESH.search(text):
            continue

        m = RE_TITOL.search(text)
        if not m:
            sense_titol.append(url)
            continue
        titol = RE_SUFIX.sub('', html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip())
        if not titol:
            sense_titol.append(url)
            continue

        trams = url.strip('/').split('/')
        llengua = trams[0] if trams and trams[0] in ('es', 'en') else 'ca'

        # El text que es busca: títol i adreça, sense accents, perquè
        # «basquet» trobi «bàsquet» i a l'inrevés.
        buscable = sense_accents((titol + ' ' + url.replace('-', ' ').replace('/', ' ')).lower())

        entrades.append({'u': url, 't': titol[:90], 'l': llengua, 'b': buscable[:180]})

    entrades.sort(key=lambda e: e['u'])
    contingut = json.dumps(entrades, ensure_ascii=False, separators=(',', ':')) + '\n'

    if args.check:
        actual = SORTIDA.read_text(encoding='utf-8') if SORTIDA.is_file() else ''
        if actual != contingut:
            print("✗ js/cerca-index.json no està al dia.\n"
                  "  Torneu a passar: python3 scripts/genera-index-cerca.py", file=sys.stderr)
            return 1
        print(f"✓ js/cerca-index.json al dia · {len(entrades)} pàgines")
        return 0

    SORTIDA.write_text(contingut, encoding='utf-8')
    per_llengua = {}
    for e in entrades:
        per_llengua[e['l']] = per_llengua.get(e['l'], 0) + 1
    detall = ' · '.join(f"{k}: {v}" for k, v in sorted(per_llengua.items()))
    print(f"js/cerca-index.json escrit · {len(entrades)} pàgines ({detall}) · "
          f"{SORTIDA.stat().st_size // 1024} KB")
    if sense_titol:
        print(f"⚠ {len(sense_titol)} pàgines sense <title>, fora de l'índex: "
              f"{', '.join(sense_titol[:5])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
