#!/usr/bin/env python3
"""Escriu `js/nav-i18n.js` a partir de `i18n/routes.yml`.

Per què cal. El commutador d'idioma només existia a les tres portades: qui
arribava a una pàgina interior en castellà o en anglès —i hi arriba, perquè
són les que porten trànsit de cercador— no en podia sortir. Posar-l'hi a mà,
pàgina per pàgina, és el que `i18n/routes.yml` diu expressament que s'ha de
deixar de fer.

I sobretot: **les adreces traduïdes no són mecàniques**. `/proteccio-menor/`
és `/es/proteccion-menor/`, no `/es/proteccio-menor/`. Divuit de les rutes
del mapa són així. Qualsevol commutador que es limiti a posar el prefix de
l'idioma davant de l'adreça catalana enviaria la gent a un 404 en aquests
casos. L'única font que ho sap és `routes.yml`.

Què n'emet: un fitxer petit amb la llista de trios (ca, es, en). El
`js/nav.js` en construeix l'índex al navegador i, per a la pàgina on ets, hi
posa només els idiomes que existeixen de debò. Si una pàgina no està
traduïda, no s'hi ofereix el canvi: enllaçar a una pàgina en un altre idioma
és pitjor que no oferir-la, que és el criteri escrit a `i18n/README.md`.

    python3 scripts/genera-nav-i18n.py            # escriu js/nav-i18n.js
    python3 scripts/genera-nav-i18n.py --check    # només comprova (per a la CI)
"""
import argparse
import json
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
RUTES = ARREL / 'i18n' / 'routes.yml'
MENU = ARREL / 'i18n' / 'menu.yml'
NAV = ARREL / 'js' / 'nav.js'
SORTIDA = ARREL / 'js' / 'nav-i18n.js'


def llegeix_rutes():
    """Les parelles de routes.yml, sense dependre de cap llibreria de YAML.

    El fitxer té una forma fixa i molt simple (una llista d'entrades amb tres
    claus), i el repositori no porta PyYAML: llegir-lo amb expressions
    regulars evita afegir-hi una dependència per a vint línies.
    """
    text = RUTES.read_text(encoding='utf-8')
    entrades, actual = [], None
    for linia in text.splitlines():
        m = re.match(r'^-\s*ca:\s*(\S+)', linia)
        if m:
            if actual:
                entrades.append(actual)
            actual = {'ca': m.group(1), 'es': None, 'en': None}
            continue
        if actual is None:
            continue
        m = re.match(r'^\s+(es|en):\s*(\S+)', linia)
        if m:
            valor = m.group(2)
            actual[m.group(1)] = None if valor == 'null' else valor
    if actual:
        entrades.append(actual)
    return entrades


def llegeix_menu():
    """Els rètols del menú en castellà i en anglès, de i18n/menu.yml.

    Mateix criteri que amb routes.yml: el fitxer té una forma fixa i molt
    simple, i el repositori no porta PyYAML. Un `-` en columna zero obre una
    entrada; les línies indentades hi posen claus.
    """
    text = MENU.read_text(encoding='utf-8')
    seccio, columnes, enllacos, actual = None, [], [], None

    def tanca():
        if actual is None:
            return
        (columnes if seccio == 'columnes' else enllacos).append(actual)

    for linia in text.splitlines():
        if re.match(r'^(columnes|enllacos):\s*$', linia):
            tanca()
            seccio, actual = linia.split(':')[0], None
            continue
        m = re.match(r'^-\s*ca:\s*(.+?)\s*$', linia)
        if m:
            tanca()
            actual = {'ca': m.group(1)}
            continue
        m = re.match(r'^\s+(es|en|nota_es|nota_en):\s*(.+?)\s*$', linia)
        if m and actual is not None:
            actual[m.group(1)] = m.group(2)
    tanca()
    return columnes, enllacos


def llegeix_mapa():
    """Les columnes i els destins del menú, tal com són a js/nav.js.

    No per generar-los —el mapa mana i viu allà— sinó per comprovar que la
    traducció els cobreix tots. Si algú afegeix un destí al menú i no el posa
    a menu.yml, l'entrada sortiria en català enmig d'un menú en castellà;
    val més que l'script ho digui.
    """
    text = NAV.read_text(encoding='utf-8')
    inici = text.index('var MAPA')
    blob = text[inici:text.index('\n  ];', inici)]
    titols = re.findall(r"\{ titol: '([^']*)'", blob)
    hrefs = re.findall(r"\['(/[^']*)',", blob)
    return titols, hrefs


def existeix(url):
    """Si una adreça del mapa té fitxer al disc, tal com la serviria Pages."""
    if not url:
        return True
    cami = url.lstrip('/')
    if url.endswith('/'):
        return (ARREL / cami / 'index.html').is_file()
    return (ARREL / cami).is_file() or (ARREL / (cami + '.html')).is_file()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true',
                    help='no escriu res; falla si el fitxer no és al dia o hi ha rutes mortes')
    args = ap.parse_args()

    entrades = llegeix_rutes()

    # Cap adreça del commutador pot ser un 404: val més no oferir l'idioma.
    mortes = [(e['ca'], idioma, e[idioma])
              for e in entrades for idioma in ('es', 'en')
              if e[idioma] and not existeix(e[idioma])]
    if mortes:
        for ca, idioma, url in mortes:
            print(f"✗ {ca} → {idioma}: {url} no existeix al disc", file=sys.stderr)
        print(f"\n{len(mortes)} rutes del mapa apunten a un fitxer que no hi és. "
              f"Arregleu-ho a i18n/routes.yml abans de generar el commutador.", file=sys.stderr)
        return 1

    # Només les pàgines que tenen alguna traducció: la resta no necessiten
    # commutador i només farien el fitxer més gros.
    trios = [[e['ca'], e['es'] or '', e['en'] or '']
             for e in entrades if e['es'] or e['en']]
    trios.sort()

    # --- Rètols del menú ---------------------------------------------------
    columnes, enllacos = llegeix_menu()
    titols, destins = llegeix_mapa()

    if [c['ca'] for c in columnes] != titols:
        print("✗ Les columnes de i18n/menu.yml no són les del mapa de js/nav.js.\n"
              f"  menu.yml: {[c['ca'] for c in columnes]}\n"
              f"  nav.js:   {titols}", file=sys.stderr)
        return 1

    per_ruta = {e['ca']: e for e in entrades}
    dits = {e['ca'] for e in enllacos}
    # Un destí només necessita rètol en l'idioma on el menú l'ensenyarà, i el
    # menú només l'ensenya si la pàgina està traduïda.
    falten = [d for d in destins
              if d not in dits and (per_ruta.get(d, {}).get('es') or per_ruta.get(d, {}).get('en'))]
    if falten:
        for d in falten:
            print(f"✗ {d} surt al menú traduït i no té rètol a i18n/menu.yml", file=sys.stderr)
        return 1

    sobren = [e['ca'] for e in enllacos if e['ca'] not in destins]
    if sobren:
        for d in sobren:
            print(f"! {d} té rètol a i18n/menu.yml i ja no és al menú", file=sys.stderr)

    menu = {
        'columnes': {
            'es': [c.get('es', c['ca']) for c in columnes],
            'en': [c.get('en', c['ca']) for c in columnes],
        },
        'enllacos': {
            e['ca']: {
                'es': [e.get('es', ''), e.get('nota_es', '')],
                'en': [e.get('en', ''), e.get('nota_en', '')],
            }
            for e in enllacos if e['ca'] in destins
        },
    }

    cos = json.dumps(trios, ensure_ascii=False, separators=(',', ':'))
    cos_menu = json.dumps(menu, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
    contingut = f'''/* Mapa d'idiomes · generat per scripts/genera-nav-i18n.py des de i18n/routes.yml.
 *
 * NO S'EDITA A MÀ. Per canviar una parella, toqueu i18n/routes.yml —que sí
 * que s'edita a mà i les seves edicions manen— i torneu a passar l'script.
 *
 * Cada entrada és [català, castellà, anglès]; la cadena buida vol dir que
 * aquella pàgina encara no està traduïda, i llavors el commutador no ofereix
 * aquell idioma. Les adreces traduïdes no són mecàniques ({len([t for t in trios if t[1] and t[1] != "/es" + t[0]])} de {len(trios)} no
 * ho són), i per això aquest mapa no es pot substituir per posar un prefix.
 *
 * {len(trios)} pàgines amb almenys una traducció, de {len(entrades)} del mapa.
 */
window.CBGB_IDIOMES = {cos};

/* Els rètols del menú en castellà i en anglès · generat des de i18n/menu.yml.
 *
 * Els enllaços del menú ja portaven bé —això ho resol el mapa d'aquí dalt—
 * però el text sortia en català a les pàgines /es/ i /en/. Cap paraula d'aquí
 * no s'ha inventat: surten del glossari, del vocabulari tancat d'enllaços o
 * del text que el club ja té publicat en aquell idioma. Per canviar-ne una,
 * toqueu i18n/menu.yml i torneu a passar l'script.
 */
window.CBGB_MENU = {cos_menu};
'''

    if args.check:
        actual = SORTIDA.read_text(encoding='utf-8') if SORTIDA.is_file() else ''
        if actual != contingut:
            print("✗ js/nav-i18n.js no està al dia amb i18n/routes.yml.\n"
                  "  Torneu a passar: python3 scripts/genera-nav-i18n.py", file=sys.stderr)
            return 1
        print(f"✓ js/nav-i18n.js al dia · {len(trios)} pàgines amb traducció")
        return 0

    SORTIDA.write_text(contingut, encoding='utf-8')
    amb_es = sum(1 for t in trios if t[1])
    amb_en = sum(1 for t in trios if t[2])
    print(f"js/nav-i18n.js escrit · {len(trios)} pàgines amb traducció "
          f"({amb_es} en castellà, {amb_en} en anglès) · cap ruta morta")
    return 0


if __name__ == '__main__':
    sys.exit(main())
