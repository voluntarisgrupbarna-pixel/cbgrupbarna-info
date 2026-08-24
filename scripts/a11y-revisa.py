#!/usr/bin/env python3
"""Revisa l'accessibilitat estructural de totes les pàgines del lloc.

No substitueix obrir el navegador —el contrast i l'ordre de tabulació s'han de
mirar amb axe-core sobre la pàgina servida, vegeu web-cbgb §10— però enganxa
d'una passada el que sí es pot veure llegint l'HTML: pàgines sense enllaç de
salt, sense `<main>`, sense `<h1>`, imatges sense text alternatiu, camps de
formulari sense nom i `<iframe>` sense títol.

Les redireccions (`<meta http-equiv="refresh">`) i les peces per imprimir no
compten: no són pàgines per navegar-hi.

    python3 scripts/a11y-revisa.py          # llista el que falla
    python3 scripts/a11y-revisa.py --breu   # només el recompte

Torna 1 si troba res, de manera que es pot fer servir com a comprovació.
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'node_modules', '.next', 'assets'}
SKIP_PATHS = ('opina/print/',)
BREU = '--breu' in sys.argv

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Cal beautifulsoup4: pip install beautifulsoup4")


def pagines():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT)
            if any(rel.startswith(s) for s in SKIP_PATHS):
                continue
            src = open(p, encoding='utf-8', errors='replace').read()
            if re.search(r'<meta[^>]+http-equiv=["\']?refresh', src, re.I):
                continue
            yield rel, src


def revisa(rel, src):
    soup = BeautifulSoup(src, 'html.parser')
    faltes = []
    if 'class="skip"' not in src and 'skip-link' not in src:
        faltes.append("sense enllaç de salt")
    if not soup.find('main'):
        faltes.append("sense <main>")
    if '/css/a11y.css' not in src:
        faltes.append("sense css/a11y.css")
    if not soup.find('h1'):
        faltes.append("sense <h1>")
    if not re.search(r'<html[^>]*\blang=', src, re.I):
        faltes.append("sense lang a <html>")

    imgs = [str(i)[:60] for i in soup.find_all('img') if i.get('alt') is None]
    if imgs:
        faltes.append("%d imatges sense alt" % len(imgs))
    ifr = [i for i in soup.find_all('iframe') if not i.get('title')]
    if ifr:
        faltes.append("%d iframes sense title" % len(ifr))

    camps = 0
    for el in soup.find_all(['input', 'select', 'textarea']):
        t = (el.get('type') or 'text').lower()
        if el.name == 'input' and t in ('hidden', 'submit', 'button', 'reset', 'image'):
            continue
        if el.get('aria-label') or el.get('aria-labelledby') or el.get('title'):
            continue
        i = el.get('id')
        if i and soup.find('label', attrs={'for': i}):
            continue
        if el.find_parent('label'):
            continue
        camps += 1
    if camps:
        faltes.append("%d camps sense etiqueta" % camps)

    for el in soup.find_all(['a', 'button']):
        if el.name == 'a' and not el.get('href'):
            continue
        if el.get('aria-label') or el.get('aria-labelledby') or el.get('title'):
            continue
        if el.get_text(strip=True):
            continue
        if any((im.get('alt') or '').strip() for im in el.find_all('img')):
            continue
        faltes.append("enllaç o botó sense nom")
        break
    return faltes


def main():
    total = collections.Counter()
    pagines_amb_faltes = 0
    n = 0
    for rel, src in pagines():
        n += 1
        faltes = revisa(rel, src)
        if not faltes:
            continue
        pagines_amb_faltes += 1
        for f in faltes:
            total[re.sub(r'^\d+ ', '', f)] += 1
        if not BREU:
            print("%-58s %s" % (rel, ' · '.join(faltes)))
    print("\n%d pàgines revisades, %d amb alguna cosa a mirar" % (n, pagines_amb_faltes))
    for k, v in total.most_common():
        print("  %5d  %s" % (v, k))
    return 1 if pagines_amb_faltes else 0


if __name__ == '__main__':
    sys.exit(main())
