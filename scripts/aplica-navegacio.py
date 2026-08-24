#!/usr/bin/env python3
"""Posa la mateixa navegació a totes les pàgines del lloc.

El problema que resol, mesurat amb `node tests/nav-audit.mjs` abans de tocar
res: de 404 pàgines, 401 no oferien el menú complet del club i 297 no
s'assolien des de la portada seguint només capçalera, menú i peu. A 360 px
hi havia 120 capçaleres diferents. El menú, de fet, només existia a la
portada: en sortir-ne desapareixia.

Què fa aquest script: afegeix a cada pàgina amb capçalera les dues línies que
carreguen la navegació compartida —`/css/nav.css` i `/js/nav.js`—, que és qui
injecta el botó de menú, el mapa complet del club, la marca de la secció on
ets i la molla de pa.

És idempotent: passar-l'hi dues vegades no duplica res. No toca cap altra
cosa del document.

    python3 scripts/aplica-navegacio.py --dry-run   # mira què faria
    python3 scripts/aplica-navegacio.py             # ho aplica
"""
import argparse
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent

# Fora del lloc públic, o amb cicle de vida propi.
# El Premi Dona i Esport no s'hi toca: decisió de l'Ana (24/08/2026).
# És el mirall local d'una candidatura que viu a la web oficial
# (voluntarisgrupbarna-pixel.github.io/cbgrupbarna), i qualsevol canvi
# aquí la fa divergir de l'original.
EXCLOU = ('.git', 'node_modules', 'tests', '.github', 'galeria', '.claude',
          'premidonaesport')

CSS = '<link rel="stylesheet" href="/css/nav.css">'
# L'ordre importa: tots dos són `defer` i s'executen en l'ordre del document,
# i `nav.js` necessita el mapa d'idiomes ja carregat quan arrenca.
I18N = '<script src="/js/nav-i18n.js" defer></script>'
JS = '<script src="/js/nav.js" defer></script>'

# Pàgines públiques sense cap <header>: entren per cercador i no tenien cap
# sortida cap al club. Hi va la navegació igualment, i `js/nav.js` els fa una
# capçalera mínima. Fora d'aquesta llista, una pàgina sense capçalera se salta:
# els panells d'administració i els generadors de cartells no han de dur menú.
SENSE_CAPCALERA_PERO_PUBLIQUES = {
    'mascota/index.html',
    'es/mascota/index.html',
    'en/mascota/index.html',
    'galeria-3x3-glories/index.html',
    'es/galeria-3x3-glories/index.html',
    'en/galeria-3x3-glories/index.html',
}

RE_HEADER = re.compile(r'<header[\s>]', re.I)
RE_HEAD_TANCA = re.compile(r'</head\s*>', re.I)
RE_BODY_TANCA = re.compile(r'</body\s*>', re.I)


def pagines():
    for p in sorted(ARREL.rglob('*.html')):
        rel = p.relative_to(ARREL)
        if any(part in EXCLOU for part in rel.parts):
            continue
        yield p


def aplica(text):
    """Retorna (text_nou, què_s'hi_ha_afegit). Cap canvi => (text, [])."""
    fet = []

    # Es busca l'etiqueta sencera, no el camí: a la portada hi ha un comentari
    # que anomena aquests fitxers i, si es busqués el camí a seques, l'script
    # es pensaria que la pàgina ja està feta i se la saltaria.
    if CSS not in text:
        m = RE_HEAD_TANCA.search(text)
        if m:
            # Amb la sagnia de la línia on va, perquè el diff sigui llegible.
            inici_linia = text.rfind('\n', 0, m.start()) + 1
            sagnia = re.match(r'[ \t]*', text[inici_linia:m.start()]).group(0)
            text = text[:m.start()] + CSS + '\n' + sagnia + text[m.start():]
            fet.append('css')

    # El mapa d'idiomes va SEMPRE davant de nav.js. Si nav.js ja hi és (d'una
    # passada anterior), el mapa s'insereix just abans; si no, tots dos van
    # abans de </body>, en aquest ordre.
    if I18N not in text:
        if JS in text:
            text = text.replace(JS, I18N + '\n' + JS, 1)
            fet.append('i18n')
        else:
            m = RE_BODY_TANCA.search(text)
            if m:
                inici_linia = text.rfind('\n', 0, m.start()) + 1
                sagnia = re.match(r'[ \t]*', text[inici_linia:m.start()]).group(0)
                text = text[:m.start()] + I18N + '\n' + sagnia + text[m.start():]
                fet.append('i18n')
    elif JS in text and text.index(JS) < text.index(I18N):
        # Ordre invertit d'una passada anterior: es repara.
        text = text.replace(I18N + '\n', '', 1).replace(I18N, '', 1)
        text = text.replace(JS, I18N + '\n' + JS, 1)
        fet.append('ordre')

    if JS not in text:
        m = RE_BODY_TANCA.search(text)
        if m:
            inici_linia = text.rfind('\n', 0, m.start()) + 1
            sagnia = re.match(r'[ \t]*', text[inici_linia:m.start()]).group(0)
            text = text[:m.start()] + JS + '\n' + sagnia + text[m.start():]
            fet.append('js')

    return text, fet


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true', help='no desa res, només ho explica')
    args = ap.parse_args()

    tocades = saltades = sense_lloc = 0
    for p in pagines():
        text = p.read_text(encoding='utf-8')

        # Sense capçalera no hi ha on penjar el botó de menú, tret de les
        # públiques de la llista: allà nav.js en fabrica una de mínima.
        rel_str = p.relative_to(ARREL).as_posix()
        if not RE_HEADER.search(text) and rel_str not in SENSE_CAPCALERA_PERO_PUBLIQUES:
            saltades += 1
            continue

        nou, fet = aplica(text)
        if not fet:
            saltades += 1
            continue
        if '</head' not in text.lower() or '</body' not in text.lower():
            sense_lloc += 1

        rel = p.relative_to(ARREL)
        print(f"  {'+'.join(fet):8} {rel}")
        if not args.dry_run:
            p.write_text(nou, encoding='utf-8')
        tocades += 1

    print(f"\n{tocades} pàgines {'es tocarien' if args.dry_run else 'tocades'} · "
          f"{saltades} ja al dia o sense capçalera")
    if sense_lloc:
        print(f"⚠ {sense_lloc} pàgines sense </head> o </body>: reviseu-les a mà")
    return 0


if __name__ == '__main__':
    sys.exit(main())
