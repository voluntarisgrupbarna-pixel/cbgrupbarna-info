#!/usr/bin/env python3
"""Aplica la portada C, «La Jugada», a l'Escoleta i les seves traduccions.

La proposta C de les quatre portades del 30/08/2026: la pàgina és una
possessió de 24 segons. El rellotge baixa mentre es fa scroll i cada tram
de la història és un moment de la jugada, del primer bot a la cistella.

Es fa amb un script i no a mà perque son tres fitxers mirall (ca, es, en)
i vuit trams a cadascun: fer-ho a dit garanteix que un dels tres quedi
diferent, i el circuit d'i18n ho barraria.

El que NO fa, i es a proposit: no toca ni una lletra del contingut. La
historia, les fotos, les FAQ i el JSON-LD de l'Escoleta es queden tal com
son — hi ha una estrategia de SEO que hi depen. La Jugada es la portada:
el rellotge, el marcador de cada tram i el submenu. Res mes.

Idempotent: passar-lo dues vegades deixa el fitxer igual.
"""
from __future__ import annotations

import os
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = '<link rel="stylesheet" href="/css/jugada.css">'
JS = '<script src="/js/jugada.js" defer></script>'

# Els vuit trams de la possessio, identificats pel titol de la seccio
# perque els numeros de linia dels tres fitxers no coincideixen. L'ordre
# es el de la pagina; el JavaScript reparteix els segons de :24 a :00.
TRAMS = {
    "ca": [
        ("Tot va començar", "El primer bot"),
        ("El document", "La prova"),
        ("Els que van", "La passada"),
        ("Dinou anys", "El rebot"),
        ("Els que<br>venen ara", "El contraatac"),
        ("L’Escoleta,<br>avui", "La pantalla"),
        ("Qui entrena", "El tir"),
        ("El proper", "Cistella"),
    ],
    "es": [
        ("Todo empezó", "El primer bote"),
        ("El documento", "La prueba"),
        ("Los que llegaron", "El pase"),
        ("Diecinueve años", "El rebote"),
        ("Los que<br>vienen ahora", "El contraataque"),
        ("La Escoleta,<br>hoy", "El bloqueo"),
        ("Quién entrena", "El tiro"),
        ("El próximo", "Canasta"),
    ],
    "en": [
        ("It all started", "The first dribble"),
        ("The document", "The proof"),
        ("The ones who", "The pass"),
        ("Nineteen years", "The rebound"),
        ("The ones<br>coming up now", "The fast break"),
        ("The Escoleta,<br>today", "The screen"),
        ("Who trains", "The shot"),
        ("The next one", "Basket"),
    ],
}

SUBMENU = {
    "ca": ("Dins de l'Escoleta", "Història de l'escola", "Història del club", "Galeria de fotos"),
    "es": ("Dentro de la Escoleta", "Historia de la escuela", "Historia del club", "Galería de fotos"),
    "en": ("Inside the Escoleta", "History of the school", "History of the club", "Photo gallery"),
}

HISTORIA_CLUB = {"ca": "/historia/", "es": "/es/historia/", "en": "/en/history/"}
GALERIA = {"ca": "/fotos/", "es": "/es/fotos/", "en": "/en/fotos/"}

# La pista, geometria pura en SVG com mana el sistema: cap imatge de fons.
PISTA = (
    '<div class="jug-court" aria-hidden="true">'
    '<svg viewBox="0 0 600 1400" preserveAspectRatio="xMidYMid slice" fill="none" '
    'stroke="#ffffff" stroke-width="2">'
    '<rect x="40" y="40" width="520" height="1320"/>'
    '<line x1="40" y1="700" x2="560" y2="700"/>'
    '<circle cx="300" cy="700" r="90"/>'
    '<rect x="190" y="40" width="220" height="180"/>'
    '<rect x="190" y="1180" width="220" height="180"/>'
    '<path d="M 90 40 A 260 260 0 0 0 510 40"/>'
    '<path d="M 90 1360 A 260 260 0 0 1 510 1360"/>'
    "</svg></div>"
)

FITXERS = {
    "ca": "escoleta/index.html",
    "es": "es/escoleta/index.html",
    "en": "en/escoleta/index.html",
}


def aplica(codi: str, rel: str) -> list[str]:
    ruta = os.path.join(ARREL, rel)
    with open(ruta, encoding="utf-8") as f:
        html = f.read()
    original = html
    fets = []

    # 1 · El full d'estil, just despres del de la cerca.
    if CSS not in html:
        html = html.replace(
            '<link rel="stylesheet" href="/css/cerca.css">',
            '<link rel="stylesheet" href="/css/cerca.css">\n' + CSS,
            1,
        )
        fets.append("css")

    # 2 · El script, al costat dels altres.
    if JS not in html:
        html = html.replace(
            '<script src="/js/avis-portes-obertes.js" defer></script>',
            '<script src="/js/avis-portes-obertes.js" defer></script>\n' + JS,
            1,
        )
        fets.append("js")

    # 3 · Els vuit trams. Es marca la <section> que conte cada titol.
    marcats = 0
    for titol, nom in TRAMS[codi]:
        pos = html.find("<h2>" + titol)
        if pos < 0:
            pos = html.find(">" + titol)
        if pos < 0:
            print(f"  ! {rel}: no s'ha trobat el tram «{titol}»", file=sys.stderr)
            continue
        obre = html.rfind("<section", 0, pos)
        if obre < 0:
            continue
        fi = html.find(">", obre)
        etiqueta = html[obre:fi]
        if "data-jugada" in etiqueta:
            continue
        # Sobre superficie vermella el marcador fosc no es llegeix.
        extra = ' data-jugada="' + nom + '"'
        if 'class="cta"' in etiqueta:
            extra += ' data-jug-to="vermell"'
        html = html[:fi] + extra + html[fi:]
        marcats += 1
    if marcats:
        fets.append(f"{marcats} trams")

    # Sobre superficie vermella el marcador fosc no es llegeix: el
    # tancament de la pagina es una franja vermella i el seu :00 ha
    # d'anar en blanc.
    html = html.replace(' data-jug-to="vermell"', "")
    if 'class="cta jug-vermell"' not in html:
        html = html.replace('<section class="cta"', '<section class="cta jug-vermell"', 1)

    # 4 · id="historia" al primer tram, que es on porta el submenu. El
    #     fitxer catala ja el porta; les traduccions, no.
    if 'id="historia"' not in html:
        primer = TRAMS[codi][0][0]
        pos = html.find("<h2>" + primer)
        if pos > 0:
            obre = html.rfind("<section", 0, pos)
            fi = html.find(">", obre)
            html = html[:fi] + ' id="historia"' + html[fi:]
            fets.append("id=historia")

    # 5 · La pista de fons i el submenu, al hero.
    if "jug-court" not in html:
        html = html.replace('<header class="hero">', '<header class="hero">\n  ' + PISTA, 1)
        fets.append("pista")

    if "jug-sub" not in html:
        etiqueta, escola, club, galeria = SUBMENU[codi]
        nav = (
            '\n    <nav class="jug-sub" aria-label="' + etiqueta + '">'
            '<a href="#historia"><span class="tag">01</span>' + escola + "</a>"
            '<a href="' + HISTORIA_CLUB[codi] + '" data-cta="escoleta-historia-club">'
            '<span class="tag">02</span>' + club + "</a>"
            '<a href="' + GALERIA[codi] + '" data-cta="escoleta-galeria">'
            '<span class="tag">03</span>' + galeria + "</a>"
            "</nav>\n"
        )
        # Just abans del peu del hero, que es on acaba el text.
        marca = '<div class="credit">'
        pos = html.find(marca)
        if pos > 0:
            html = html[:pos] + nav.lstrip("\n") + "    " + html[pos:]
            fets.append("submenu")

    if html != original:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
    return fets


def main() -> int:
    for codi, rel in FITXERS.items():
        fets = aplica(codi, rel)
        print(f"{rel}: {', '.join(fets) if fets else 'ja hi era'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
