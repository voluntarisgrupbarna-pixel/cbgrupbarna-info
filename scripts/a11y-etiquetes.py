#!/usr/bin/env python3
"""Dona nom accessible als camps de formulari que no en tenien.

Molts formularis del lloc ja porten el text visible al costat del camp, però
dins d'una <label> sense `for`: es veu, i en canvi un lector de pantalla no
sap a quin camp correspon. Aquest script fa tres passades, de la més neta a
la més bruta:

  1. Si just abans del camp hi ha una <label> sense `for`, li posa el `for`.
     El text visible passa a ser l'etiqueta de debò, sense tocar el disseny.
  2. Si no n'hi ha cap però el camp té `placeholder`, el copia a `aria-label`.
     (Un `placeholder` sol no val: desapareix en escriure i molts lectors no
     el llegeixen.)
  3. Els que no tenen ni una cosa ni l'altra —caselles de PIN, selectors amb
     fletxes— porten un text escrit a mà a la taula de sota, en els tres
     idiomes del lloc.

    python3 scripts/a11y-etiquetes.py --dry-run
"""
import os, re, sys
from bs4 import BeautifulSoup

DRY = '--dry-run' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Camps sense cap text a prop. La clau és (fitxer sense idioma, id del camp).
MANUAL = {
    ('partits/app.html', 'wk-select'): {
        'ca': 'Tria la jornada', 'es': 'Elige la jornada', 'en': 'Choose the matchday'},
    ('fotos/admin.html', 'file-input'): {
        'ca': 'Tria les fotos que vols pujar', 'es': 'Elige las fotos que quieres subir',
        'en': 'Choose the photos to upload'},
    ('partits/cartell.html', 'f-foto'): {
        'ca': 'Foto del partit', 'es': 'Foto del partido', 'en': 'Match photo'},
}
# Grups de caselles d'una xifra: cada casella diu quina és i de quantes.
PIN = {'ca': 'PIN, xifra %d de %d', 'es': 'PIN, cifra %d de %d', 'en': 'PIN, digit %d of %d'}

FIELD = re.compile(r'<(input|select|textarea)\b[^>]*>', re.I)


def lang_of(src, path):
    m = re.search(r'<html[^>]*\blang="([a-z]{2})', src, re.I)
    l = m.group(1).lower() if m else 'ca'
    return l if l in ('ca', 'es', 'en') else 'ca'


def unlabelled(soup):
    out = []
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
        out.append(el)
    return out


def process(path, rel):
    src = open(path, encoding='utf-8').read()
    lang = lang_of(src, path)
    key = re.sub(r'^(es|en)/', '', rel)
    changed = 0

    # --- 1. <label> sense `for` just abans del camp -> se li posa el `for`.
    def add_for(m):
        nonlocal changed
        lab, txt, tag, attrs = m.group(1), m.group(2), m.group(3), m.group(4)
        if re.search(r'\bfor=', lab, re.I):
            return m.group(0)
        idm = re.search(r'\bid="([^"]+)"', attrs)
        if not idm or not txt.strip():
            return m.group(0)
        changed += 1
        return '<label%s for="%s">%s</label>%s<%s%s>' % (
            lab, idm.group(1), txt, m.group(5), tag, attrs)

    src = re.sub(
        r'<label([^>]*)>([^<]{1,80})</label>(\s*)<(input|select|textarea)([^>]*)>',
        lambda m: add_for(type('M', (), {
            'group': lambda self, n, m=m: [m.group(0), m.group(1), m.group(2), m.group(4),
                                           m.group(5), m.group(3)][n]})()),
        src, flags=re.I)

    # --- 2 i 3. El que encara no té nom: placeholder, o taula de dalt.
    soup = BeautifulSoup(src, 'html.parser')
    pending = unlabelled(soup)
    pins = [e for e in pending if (e.get('id') or '').startswith('pin-')]
    for el in pending:
        i = el.get('id') or ''
        name = None
        if i.startswith('pin-') and i[4:].isdigit():
            name = PIN[lang] % (int(i[4:]) + 1, len(pins))
        elif (key, i) in MANUAL:
            name = MANUAL[(key, i)][lang]
        elif (el.get('placeholder') or '').strip() not in ('', '—', '&nbsp;'):
            name = el['placeholder'].strip()
        if not name or not i:
            continue
        # Es reescriu sobre el text original, no sobre el que tornaria
        # l'analitzador: així no es toca ni el format ni l'ordre dels atributs.
        pat = re.compile(r'<(%s)\b((?:[^>"]|"[^"]*")*?\bid="%s"(?:[^>"]|"[^"]*")*?)(/?)>'
                         % (el.name, re.escape(i)), re.I)
        m = pat.search(src)
        if not m or 'aria-label' in m.group(2):
            continue
        src = src[:m.start()] + '<%s aria-label="%s"%s%s>' % (
            m.group(1), name.replace('"', "'"), m.group(2), m.group(3)) + src[m.end():]
        changed += 1

    if changed and not DRY:
        open(path, 'w', encoding='utf-8').write(src)
    return changed


def main():
    total = files = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in {'.git', 'node_modules', '.next'}]
        for f in sorted(fn):
            if not f.endswith('.html'):
                continue
            path = os.path.join(dp, f)
            rel = os.path.relpath(path, ROOT)
            n = process(path, rel)
            if n:
                files += 1
                total += n
                print(' ', rel, '·', n, 'camps')
    print(('[assaig] ' if DRY else '') + '%d camps etiquetats a %d pàgines' % (total, files))


if __name__ == '__main__':
    main()
