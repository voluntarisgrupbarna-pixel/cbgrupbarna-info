#!/usr/bin/env python3
"""
Genera scripts/idiomes.js: el mapa de quines pàgines existeixen en quin idioma.

El selector i la tria automàtica d'idioma llegeixen aquest mapa. Es genera des
del disc, mai a mà, perquè no pugui prometre una traducció que no existeix i
enviar ningú a una pàgina que no hi és.

    python3 scripts/generate-idiomes.py

Per afegir una traducció nova: crea la pàgina, afegeix-la a GRUPS i torna a
executar això. Si el fitxer no hi és, l'script s'atura i diu quin falta.
"""
import json
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parents[1]
SORTIDA = ARREL / 'scripts' / 'idiomes.js'

# ── Els grups de pàgines que són la mateixa cosa en idiomes diferents ────────
# Clau: 'ca', 'es', 'en'. Si una llengua no hi és, s'omet (no s'inventa).
GRUPS = [
    {
        'ca': '/basquet-femeni/',
        'es': '/es/baloncesto-femenino/',
        'en': '/en/womens-basketball/',
    },
    {
        'ca': '/basquet-femeni/el-metode-barna/',
        'es': '/es/baloncesto-femenino/el-metodo-barna/',
        'en': '/en/womens-basketball/the-barna-method/',
    },
    {
        'ca': '/proteccio-menor/',
        'es': '/es/proteccion-menor/',
        'en': '/en/child-protection/',
    },
    {
        'ca': '/blog/club-formacio-i-competitiu-catalunya/',
        'es': '/es/blog/club-formacion-y-competitivo-cataluna/',
        'en': '/en/blog/formation-and-competitive-club-catalonia/',
    },
]


def fitxer_de(ruta: str) -> Path:
    return ARREL / ruta.strip('/') / 'index.html' if ruta != '/' else ARREL / 'index.html'


def comprova():
    """Cap ruta del mapa pot apuntar a un fitxer que no existeix."""
    problemes = []
    for grup in GRUPS:
        for idioma, ruta in grup.items():
            if not fitxer_de(ruta).is_file():
                problemes.append(f'  {idioma}: {ruta} → no hi ha {fitxer_de(ruta).relative_to(ARREL)}')
    return problemes


def sense_traduir():
    """Les pàgines en català que encara no tenen germanes."""
    traduides = {g['ca'] for g in GRUPS}
    totes = []
    for f in sorted(ARREL.rglob('index.html')):
        rel = f.relative_to(ARREL)
        parts = rel.parts
        if parts[0] in ('.git', 'es', 'en', 'node_modules'):
            continue
        ruta = '/' + '/'.join(parts[:-1])
        ruta = '/' if ruta == '/' else ruta + '/'
        if ruta not in traduides:
            totes.append(ruta)
    return totes


def main():
    problemes = comprova()
    if problemes:
        print('El mapa d\'idiomes apunta a pàgines que no existeixen:', file=sys.stderr)
        print('\n'.join(problemes), file=sys.stderr)
        return 1

    js = (
        '/* GENERAT per scripts/generate-idiomes.py · NO EDITAR A MÀ.\n'
        ' * Quines pàgines existeixen en quin idioma. El selector i la tria\n'
        ' * automàtica només ofereixen el que hi ha aquí, de manera que ningú\n'
        ' * acaba en una pàgina que no existeix. */\n'
        'window.CBGB_IDIOMES = ' + json.dumps(GRUPS, ensure_ascii=False, indent=2) + ';\n'
    )
    SORTIDA.write_text(js, encoding='utf-8')

    pendents = sense_traduir()
    print(f'Escrit {SORTIDA.relative_to(ARREL)} · {len(GRUPS)} grups en tres idiomes.')
    print(f'Pàgines només en català: {len(pendents)}')
    for p in pendents[:12]:
        print(f'  {p}')
    if len(pendents) > 12:
        print(f'  … i {len(pendents) - 12} més')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
