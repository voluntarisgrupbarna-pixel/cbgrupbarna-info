#!/usr/bin/env python3
"""Escriu el <nav class="menu"> de les portades /es/ i /en/.

PER QUÈ CAL. El menú del club es construeix a js/nav.js i arriba a totes les
pàgines. Les tres portades en tenen una còpia escrita a l'HTML perquè el
menú es vegi encara sense JavaScript, i js/nav.js respecta la que ja hi és.
Aquesta còpia s'havia de mantenir a mà, i no s'havia mantingut: mesurat el
2026-08-23, /es/ i /en/ oferien 10 destins mentre qualsevol pàgina interior
en aquells idiomes n'oferia 28. Aquesta diferència és exactament la sensació
que el menú «apareix i desapareix» segons on siguis.

QUÈ FA. Torna a escriure el bloc del menú de es/index.html i en/index.html a
partir de tres fonts que ja manen a la resta del lloc:

  - el mapa de js/nav.js: quins destins hi ha i en quin ordre;
  - i18n/routes.yml: quina és l'adreça d'aquell destí en aquell idioma;
  - i18n/menu.yml: com se'n diu en aquell idioma.

La portada catalana NO es toca: avui ja és correcta, i els seus `data-cta`
són els que fa servir l'analítica des de fa temps. D'allà se'n llegeixen els
`data-cta` per posar-hi els mateixos, de manera que una mateixa entrada del
menú es digui igual a les tres portades a l'hora de comptar clics.

    python3 scripts/genera-menu-portades.py
    python3 scripts/genera-menu-portades.py --check    # per a la CI
"""
import argparse
import html
import importlib.util
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent


def carrega_germa():
    """Reaprofita els lectors de genera-nav-i18n.py (el nom porta guions)."""
    spec = importlib.util.spec_from_file_location(
        'genera_nav_i18n', ARREL / 'scripts' / 'genera-nav-i18n.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PORTADES = {'es': ARREL / 'es' / 'index.html', 'en': ARREL / 'en' / 'index.html'}
ETIQUETA = {'es': 'Menú completo', 'en': 'Full menu'}
BLOC = re.compile(r'<nav class="menu" id="menu"[^>]*>.*?</nav>', re.S)


def ctas_del_catala():
    """href -> data-cta, tal com són a la portada catalana."""
    text = (ARREL / 'index.html').read_text(encoding='utf-8')
    m = BLOC.search(text)
    if not m:
        return {}
    return {href: cta for href, cta in
            re.findall(r'<a href="([^"]+)"[^>]*data-cta="([^"]+)"', m.group(0))}


def construeix(idioma, mapa, columnes, retols, rutes, ctas):
    per_ruta = {e['ca']: e for e in rutes}
    linies = [f'<nav class="menu" id="menu" aria-label="{ETIQUETA[idioma]}">',
              '  <div class="menu-grid">']
    posats = 0
    for i, (titol, enllacos) in enumerate(mapa):
        cos = []
        for href, etiqueta_ca, nota_ca in enllacos:
            desti = (per_ruta.get(href) or {}).get(idioma)
            if not desti:
                continue          # sense traduir: no surt en aquesta llengua
            fila = retols.get(href, {})
            etiqueta = fila.get(idioma) or etiqueta_ca
            nota = fila.get('nota_' + idioma, '')
            attrs = f' href="{desti}"'
            if href == '/admin/':
                attrs += ' class="menu-admin" rel="nofollow"'
            if href in ctas:
                attrs += f' data-cta="{ctas[href]}"'
            petita = f' <small>{html.escape(nota)}</small>' if nota else ''
            cos.append(f'      <a{attrs}>{html.escape(etiqueta)}{petita}</a>')
        if not cos:
            continue              # columna buida en aquesta llengua: fora
        titol_idioma = columnes[i].get(idioma) or titol
        linies.append('    <div class="menu-col">')
        linies.append(f'      <h3>{html.escape(titol_idioma)}</h3>')
        linies.extend(cos)
        linies.append('    </div>')
        posats += len(cos)
    linies.append('  </div>')
    linies.append('  <div class="menu-foot">@cbgrupbarna · +34 698 425 153 · El Clot, Barcelona</div>')
    linies.append('</nav>')
    return '\n'.join(linies), posats


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='no escriu res; falla si no està al dia')
    args = ap.parse_args()

    germa = carrega_germa()
    rutes = germa.llegeix_rutes()
    columnes, enllacos = germa.llegeix_menu()
    retols = {e['ca']: e for e in enllacos}

    # El mapa, amb notes incloses, llegit de js/nav.js.
    text = (ARREL / 'js' / 'nav.js').read_text(encoding='utf-8')
    inici = text.index('var MAPA')
    blob = text[inici:text.index('\n  ];', inici)]
    mapa = []
    for tros in blob.split('{ titol: ')[1:]:
        titol = re.match(r"'([^']*)'", tros).group(1)
        mapa.append((titol, re.findall(r"\['(/[^']*)', '([^']*)', '([^']*)'\]", tros)))

    ctas = ctas_del_catala()
    problemes = 0

    # La portada catalana no es reescriu, però sí que es comprova: si algú
    # afegeix un destí al mapa i no el posa allà, la portada tornaria a
    # ensenyar un menú diferent del de la resta del lloc, que és el defecte
    # que aquest script existeix per no repetir.
    del_mapa = [h for _, enllacos in mapa for h, _, _ in enllacos]
    de_la_portada = list(ctas) or []
    if de_la_portada and de_la_portada != del_mapa:
        falten = [h for h in del_mapa if h not in de_la_portada]
        sobren = [h for h in de_la_portada if h not in del_mapa]
        for h in falten:
            print(f"✗ index.html: {h} és al mapa de js/nav.js i no al menú de la portada", file=sys.stderr)
        for h in sobren:
            print(f"✗ index.html: {h} és al menú de la portada i no al mapa de js/nav.js", file=sys.stderr)
        if not falten and not sobren:
            print("✗ index.html: el menú de la portada té els mateixos destins "
                  "que el mapa però en un altre ordre", file=sys.stderr)
        problemes += 1
    for idioma, cami in PORTADES.items():
        pagina = cami.read_text(encoding='utf-8')
        if not BLOC.search(pagina):
            print(f"✗ {cami.relative_to(ARREL)}: no s'hi troba el bloc del menú", file=sys.stderr)
            return 1
        nou, quants = construeix(idioma, mapa, columnes, retols, rutes, ctas)
        resultat = BLOC.sub(lambda _: nou, pagina, count=1)
        if args.check:
            if resultat != pagina:
                print(f"✗ {cami.relative_to(ARREL)}: el menú de la portada no és el del club.\n"
                      f"  Torneu a passar: python3 scripts/genera-menu-portades.py", file=sys.stderr)
                problemes += 1
            else:
                print(f"✓ {cami.relative_to(ARREL)} al dia · {quants} destins")
            continue
        cami.write_text(resultat, encoding='utf-8')
        print(f"{cami.relative_to(ARREL)} · {quants} destins al menú")
    return 1 if problemes else 0


if __name__ == '__main__':
    sys.exit(main())
