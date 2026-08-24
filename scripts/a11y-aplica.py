#!/usr/bin/env python3
"""Aplica la capa d'accessibilitat a totes les pàgines del lloc.

Fa tres coses, i cap d'elles toca el contingut visible:

  1. Enllaça `/css/a11y.css` (focus visible, moviment reduït, alt contrast).
  2. Posa un enllaç «Salta al contingut» com a primer element del <body>.
  3. Embolcalla el contingut real amb <main id="contingut">, deixant fora el
     menú de dalt i el peu, perquè un lector de pantalla pugui saltar-hi.

El pas 3 només s'aplica quan es pot fer amb seguretat: el script mira els
fills directes del <body> amb un analitzador d'HTML de debò, i si no sap on
acaba el contingut, no toca la pàgina. Tot són insercions de text; no es
reescriu ni es reformata res del que ja hi ha.

    python3 scripts/a11y-aplica.py --dry-run   # què faria
    python3 scripts/a11y-aplica.py             # ho fa
"""
import os, re, sys
from bs4 import BeautifulSoup

DRY = '--dry-run' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.next', 'assets'}
# Peces que no són pàgines de navegació: cartells per imprimir i imatges OG.
SKIP_PATHS = ('opina/print/',)

SALT = {'ca': 'Salta al contingut', 'es': 'Saltar al contenido', 'en': 'Skip to content'}

# Elements que són "marc" de la pàgina, no contingut: van fora del <main>.
CHROME_TAGS = {'script', 'style', 'noscript', 'link', 'template', 'dialog', 'nav', 'footer'}
CHROME_HINT = re.compile(r'nav|menu|topbar|header-|site-header|skip|cookie|galetes|banner|overlay|modal|toast|foot', re.I)


def is_chrome(el, leading):
    """Un fill directe del <body> que no forma part del contingut de la pàgina."""
    if el.name in CHROME_TAGS:
        return True
    if el.name == 'a' and 'skip' in (el.get('class') or []):
        return True
    cls = ' '.join(el.get('class') or []) + ' ' + (el.get('id') or '')
    if leading:
        # A dalt: capçaleres que només porten navegació, barres de novetats.
        if el.name == 'header' and el.find('nav'):
            return True
        if el.name in ('div', 'section') and el.find('nav') and len(el.get_text(strip=True)) < 400:
            return True
        if el.name in ('div', 'section', 'aside') and CHROME_HINT.search(cls):
            return True
    else:
        # A baix: peu, avisos de galetes, finestres modals, botons flotants.
        if el.name in ('div', 'section', 'aside', 'header') and CHROME_HINT.search(cls):
            return True
    return False


def offsets(src):
    """Índex del primer caràcter de cada línia, per convertir (línia, columna)."""
    out, pos = [0], 0
    for line in src.splitlines(keepends=True):
        pos += len(line)
        out.append(pos)
    return out


def abs_pos(lines, el):
    return lines[el.sourceline - 1] + el.sourcepos


def process(path):
    src = open(path, encoding='utf-8', errors='replace').read()
    if re.search(r'<meta[^>]+http-equiv=["\']?refresh', src, re.I):
        return None                      # redireccions: no són pàgines
    soup = BeautifulSoup(src, 'html.parser')
    body = soup.body
    if body is None or body.sourceline is None:
        return None
    lines = offsets(src)
    edits = []                            # (posició, text) — només insercions
    done = []

    # 1. El full d'accessibilitat, l'últim de tots perquè les seves regles manin.
    if '/css/a11y.css' not in src:
        head = soup.head
        if head:
            m = re.search(r'</head>', src, re.I)
            if m:
                edits.append((m.start(), '<link rel="stylesheet" href="/css/a11y.css">\n'))
                done.append('a11y.css')

    lang = (soup.html.get('lang') or 'ca')[:2].lower() if soup.html else 'ca'
    lang = lang if lang in SALT else 'ca'

    main = soup.find('main')
    target = None
    if main is not None:
        target = main.get('id')
    body_start = src.index('>', abs_pos(lines, body)) + 1

    # 2. Embolcallar el contingut amb <main>, si encara no n'hi ha cap.
    if main is None:
        kids = [c for c in body.children if getattr(c, 'name', None)]
        if not kids:
            return None
        i, j = 0, len(kids) - 1
        while i <= j and is_chrome(kids[i], True):
            i += 1
        while j >= i and is_chrome(kids[j], False):
            j -= 1
        if i > j:
            return None                   # tot marc, cap contingut: no s'hi toca
        open_at = abs_pos(lines, kids[i])
        # El tancament va just abans del peu de pàgina, si n'hi ha cap al
        # nivell del <body> —el que hi hagi després (barres fixes, scripts)
        # tampoc no és contingut—, i si no, just abans del marc de la cua.
        foot = next((k for k in kids[i + 1:] if k.name == 'footer'), None)
        if foot is not None:
            close_at = abs_pos(lines, foot)
        else:
            close_at = abs_pos(lines, kids[j + 1]) if j + 1 < len(kids) else None
        if close_at is None:
            m = re.search(r'</body>', src, re.I)
            if not m:
                return None
            close_at = m.start()
        if close_at <= open_at:
            return None
        target = 'contingut' if 'id="contingut"' not in src else 'contingut-a11y'
        edits.append((open_at, '<main id="%s" tabindex="-1">\n' % target))
        edits.append((close_at, '</main>\n'))
        done.append('<main>')
    elif not target:
        target = 'contingut' if 'id="contingut"' not in src else 'contingut-a11y'
        mpos = abs_pos(lines, main)
        edits.append((mpos + len('<main'), ' id="%s" tabindex="-1"' % target))
        done.append('id a <main>')

    # 3. L'enllaç de salt, com a primer element del <body>.
    if 'class="skip"' not in src and 'skip-link' not in src and target:
        edits.append((body_start, '\n<a class="skip" href="#%s">%s</a>' % (target, SALT[lang])))
        done.append('skip link')

    if not edits:
        return None
    for pos, text in sorted(edits, key=lambda e: -e[0]):
        src = src[:pos] + text + src[pos:]
    if not DRY:
        open(path, 'w', encoding='utf-8').write(src)
    return done


def main():
    changed = 0
    stats = {}
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, ROOT)
            if any(rel.startswith(s) for s in SKIP_PATHS):
                continue
            done = process(path)
            if done:
                changed += 1
                for d in done:
                    stats[d] = stats.get(d, 0) + 1
                if '--verbose' in sys.argv:
                    print(rel, '·', ', '.join(done))
    print(('[assaig] ' if DRY else '') + '%d pàgines' % changed)
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print('  %5d  %s' % (v, k))


if __name__ == '__main__':
    main()
