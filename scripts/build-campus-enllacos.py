#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la pàgina d'enllaços i vídeos del campus als tres idiomes:
/campus/enllacos/, /es/campus/enlaces/ i /en/campus/links/.

Per què existeix: el rastre del campus estava escampat. Els vídeos de les
estrelles viuen a /campus/, les convocatòries a Instagram, les edicions de
vacances a tres pàgines diferents i els articles al blog. Qui volia veure-ho
tot seguit —una família decidint, un partner, la premsa— havia de saltar de
pàgina en pàgina. Aquesta pàgina ho posa tot junt: **tots els vídeos
incrustats** i tots els enllaços, en un sol lloc i en tres idiomes.

D'on surten les dades: de `scripts/build-campus-estrelles.py`, que ja és la
taula única dels vídeos de /campus/. Aquí s'importen, no es copien: si algú
afegeix una estrella allà, aquesta pàgina la té a la següent execució.

Els vídeos es carreguen **al clic**, com a /campus/: fins que algú no en vol
veure un, no es demana res a Instagram. És la mateixa decisió de galetes que
la resta del lloc, i evita vint iframes de tercers en una sola pàgina.

L'escorxa (capçalera, commutador d'idioma i peu) es llegeix de les pàgines de
Setmana Santa, que són de la mateixa família i estan al dia. Així no hi ha una
tercera còpia del menú per mantenir.

Ús:
    python3 scripts/build-campus-enllacos.py
    python3 scripts/build-campus-enllacos.py --dry-run
"""

import html
import importlib.util
import os
import re
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://cbgrupbarna.info"
IG = "https://www.instagram.com"


def _importa(nom, cami):
    spec = importlib.util.spec_from_file_location(nom, cami)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ESTRELLES = _importa(
    "campus_estrelles", os.path.join(ARREL, "scripts", "build-campus-estrelles.py")
)
NAU, COACHES, ELIT, CONVOS = (
    ESTRELLES.NAU,
    ESTRELLES.COACHES,
    ESTRELLES.ELIT,
    ESTRELLES.CONVOS,
)

# Ruta de la pàgina i de la seva germana de Setmana Santa, d'on surt l'escorxa.
RUTES = {
    "ca": "/campus/enllacos/",
    "es": "/es/campus/enlaces/",
    "en": "/en/campus/links/",
}
FONT_ESCORXA = {
    "ca": "campus/setmana-santa/index.html",
    "es": "es/campus/semana-santa/index.html",
    "en": "en/campus/easter/index.html",
}
RUTES_VELLES = ["/campus/setmana-santa/", "/es/campus/semana-santa/", "/en/campus/easter/"]

# Les pàgines del campus, en els tres idiomes. Cada fila és la mateixa pàgina.
PAGINES = [
    ("estiu",
     ("Campus d'estiu", "Campus de verano", "Summer camp"),
     ("Sis setmanes amb Time Chamber, del juny al juliol.",
      "Seis semanas con Time Chamber, de junio a julio.",
      "Six weeks with Time Chamber, from June to July."),
     ("/campus/", "/es/campus/", "/en/campus/")),
    ("setmana-santa",
     ("Campus de Setmana Santa", "Campus de Semana Santa", "Easter camp"),
     ("El Flow Camp, en vacances escolars de primavera.",
      "El Flow Camp, en vacaciones escolares de primavera.",
      "The Flow Camp, over the spring school holidays."),
     ("/campus/setmana-santa/", "/es/campus/semana-santa/", "/en/campus/easter/")),
    ("nadal",
     ("Campus de Nadal", "Campus de Navidad", "Christmas camp"),
     ("L'edició d'hivern, amb un altre públic i una altra durada.",
      "La edición de invierno, con otro público y otra duración.",
      "The winter edition, a different length and a different group."),
     ("/campus-nadal-basquet-barcelona/", "/es/campus-navidad-baloncesto-barcelona/",
      "/en/christmas-basketball-camp-barcelona/")),
    ("comparativa",
     ("Comparativa de campus de Barcelona", "Comparativa de campus de Barcelona",
      "Barcelona camps compared"),
     ("Totes les opcions de la ciutat, amb edats, dates i preus.",
      "Todas las opciones de la ciudad, con edades, fechas y precios.",
      "Every option in the city, with ages, dates and prices."),
     ("/campus-basquet-barcelona/", "/es/campus-baloncesto-barcelona/",
      "/en/basketball-camps-barcelona/")),
    ("presentacio",
     ("Presentació Campus × Time Chamber", "Presentación Campus × Time Chamber",
      "Camp × Time Chamber presentation"),
     ("Què és el campus i qui hi ha al darrere, explicat sencer.",
      "Qué es el campus y quién hay detrás, explicado entero.",
      "What the camp is and who runs it, in full."),
     ("/presentacions/campus-timechamber/", "/es/presentaciones/campus-timechamber/",
      "/en/presentations/campus-timechamber/")),
]

# Els articles del blog que parlen del campus.
ARTICLES = [
    (("Campus Time Chamber 2026: com va anar l'edició",
      "Campus Time Chamber 2026: cómo fue la edición",
      "Time Chamber Camp 2026: how the edition went"),
     ("La crònica de les sis setmanes d'estiu, setmana a setmana.",
      "La crónica de las seis semanas de verano, semana a semana.",
      "The six summer weeks, recapped one by one."),
     ("/blog/campus-time-chamber-2026/", "/es/blog/campus-time-chamber-2026/",
      "/en/blog/time-chamber-camp-2026/")),
    (("Com triar un campus de bàsquet a Barcelona",
      "Cómo elegir un campus de baloncesto en Barcelona",
      "How to choose a basketball camp in Barcelona"),
     ("Què mirar abans d'apuntar-hi ningú, sigui el nostre o un altre.",
      "Qué mirar antes de apuntar a nadie, sea el nuestro o cualquier otro.",
      "What to look at before signing anyone up, ours or anyone else's."),
     ("/blog/campus-basquet-barcelona-guia/", "/es/blog/guia-campus-baloncesto-barcelona/",
      "/en/blog/basketball-camp-barcelona-guide/")),
]

IDX = {"ca": 0, "es": 1, "en": 2}

T = {
    "ca": dict(
        i=2,
        lang="ca", locale="ca_ES",
        title="Vídeos i enllaços del campus de bàsquet | CB Grup Barna",
        desc=("Tots els vídeos del campus de bàsquet del CB Grup Barna en una sola pàgina, "
              "amb les convocatòries de cada edició i els enllaços a totes les pàgines i "
              "articles del campus."),
        eyebrow="Campus · tot en una pàgina",
        h1="Tots els vídeos i enllaços del campus",
        lede=("Vint vídeos, sis pàgines i dos articles, junts. Els vídeos es carreguen quan hi "
              "cliques: fins llavors, aquesta pàgina no demana res a Instagram."),
        crumb_home="Inici", crumb_campus="Campus de bàsquet", crumb_here="Vídeos i enllaços",
        btn_campus="Anar al campus →",
        btn_wa="Escriure'ns per WhatsApp →",
        h_videos="Els vídeos del campus",
        p_videos=("Qui ha passat per la pista. Van separats en tres grups perquè no tot es va "
                  "gravar al mateix lloc, i això no s'infla: primer el que va passar a "
                  "<strong>La Nau del Clot</strong>, després la feina feta <strong>amb Time "
                  "Chamber</strong>, el nostre soci del campus."),
        g1="A La Nau del Clot", g2="Entrenadors NBA amb Time Chamber",
        g3="Elit que ha treballat amb Time Chamber",
        g1p="Gravat al pavelló del club, amb els nostres jugadors i jugadores a pista.",
        g2p="Sessions de tecnificació dirigides pels entrenadors del soci del campus.",
        g3p="Jugadors professionals treballant amb Time Chamber. On no és La Nau, ho diu la fitxa.",
        h_convos="Les convocatòries, edició per edició",
        p_convos=("Cada campus es va anunciar i es pot comprovar. No és una promesa: és un rastre "
                  "amb data."),
        h_pagines="Totes les pàgines del campus",
        p_pagines="La mateixa pàgina en català, castellà i anglès. Tria la fila i l'idioma.",
        th_pagina="Pàgina", th_ca="Català", th_es="Castellà", th_en="Anglès",
        h_articles="El campus, escrit",
        p_articles="El que hem publicat al blog sobre el campus, en els tres idiomes.",
        veure="Veure a Instagram →",
        play="Reproduir", reproduir="Reproduir el vídeo amb",
        reproduir_convo="Reproduir la publicació de",
        nota=("Els vídeos són d'Instagram i s'obren des del seu servidor quan hi cliques. "
              "El bloc d'estrelles d'aquesta pàgina i el de <a href=\"/campus/\">/campus/</a> "
              "surten de la mateixa taula: no es poden desincronitzar."),
    ),
    "es": dict(
        i=3,
        lang="es", locale="es_ES",
        title="Vídeos y enlaces del campus de baloncesto | CB Grup Barna",
        desc=("Todos los vídeos del campus de baloncesto del CB Grup Barna en una sola página, "
              "con las convocatorias de cada edición y los enlaces a todas las páginas y "
              "artículos del campus."),
        eyebrow="Campus · todo en una página",
        h1="Todos los vídeos y enlaces del campus",
        lede=("Veinte vídeos, seis páginas y dos artículos, juntos. Los vídeos se cargan cuando "
              "haces clic: hasta entonces, esta página no le pide nada a Instagram."),
        crumb_home="Inicio", crumb_campus="Campus de baloncesto", crumb_here="Vídeos y enlaces",
        btn_campus="Ir al campus →",
        btn_wa="Escríbenos por WhatsApp →",
        h_videos="Los vídeos del campus",
        p_videos=("Quién ha pasado por la pista. Van separados en tres grupos porque no todo se "
                  "grabó en el mismo sitio, y eso no se infla: primero lo que pasó en "
                  "<strong>La Nau del Clot</strong>, después el trabajo hecho <strong>con Time "
                  "Chamber</strong>, nuestro socio del campus."),
        g1="En La Nau del Clot", g2="Entrenadores NBA con Time Chamber",
        g3="Élite que ha trabajado con Time Chamber",
        g1p="Grabado en el pabellón del club, con nuestros jugadores y jugadoras en pista.",
        g2p="Sesiones de tecnificación dirigidas por los entrenadores del socio del campus.",
        g3p="Jugadores profesionales trabajando con Time Chamber. Donde no es La Nau, lo dice la ficha.",
        h_convos="Las convocatorias, edición por edición",
        p_convos=("Cada campus se anunció y se puede comprobar. No es una promesa: es un rastro "
                  "con fecha."),
        h_pagines="Todas las páginas del campus",
        p_pagines="La misma página en catalán, castellano e inglés. Elige la fila y el idioma.",
        th_pagina="Página", th_ca="Catalán", th_es="Castellano", th_en="Inglés",
        h_articles="El campus, escrito",
        p_articles="Lo que hemos publicado en el blog sobre el campus, en los tres idiomas.",
        veure="Ver en Instagram →",
        play="Reproducir", reproduir="Reproducir el vídeo con",
        reproduir_convo="Reproducir la publicación de",
        nota=("Los vídeos son de Instagram y se abren desde su servidor cuando haces clic. "
              "El bloque de estrellas de esta página y el de <a href=\"/es/campus/\">/es/campus/</a> "
              "salen de la misma tabla: no se pueden desincronizar."),
    ),
    "en": dict(
        i=4,
        lang="en", locale="en_GB",
        title="Camp videos and links | CB Grup Barna",
        desc=("Every video from the CB Grup Barna basketball camp on one page, with each "
              "edition's announcement and links to all the camp pages and articles."),
        eyebrow="Camp · everything on one page",
        h1="Every camp video and link",
        lede=("Twenty videos, six pages and two articles, together. Videos load when you click "
              "them: until then, this page asks Instagram for nothing."),
        crumb_home="Home", crumb_campus="Basketball camp", crumb_here="Videos and links",
        btn_campus="Go to the camp →",
        btn_wa="Message us on WhatsApp →",
        h_videos="The camp on video",
        p_videos=("Who has been on this court. They are split into three groups because not "
                  "everything was filmed in the same place, and we don't blur that: first what "
                  "happened at <strong>La Nau del Clot</strong>, then the work done <strong>with "
                  "Time Chamber</strong>, our camp partner."),
        g1="At La Nau del Clot", g2="NBA coaches with Time Chamber",
        g3="Elite players who have worked with Time Chamber",
        g1p="Filmed at the club's arena, with our own players on court.",
        g2p="Skills sessions run by the camp partner's coaches.",
        g3p="Professional players working with Time Chamber. Where it isn't La Nau, the card says so.",
        h_convos="Each edition, as it was announced",
        p_convos="Every camp was announced and can be checked. Not a promise: a dated trail.",
        h_pagines="All the camp pages",
        p_pagines="The same page in Catalan, Spanish and English. Pick the row and the language.",
        th_pagina="Page", th_ca="Catalan", th_es="Spanish", th_en="English",
        h_articles="The camp, written up",
        p_articles="What we have published on the blog about the camp, in all three languages.",
        veure="View on Instagram →",
        play="Play", reproduir="Play the video with",
        reproduir_convo="Play the post for",
        nota=("The videos are Instagram's and load from their server when you click. The stars "
              "block on this page and the one on <a href=\"/en/campus/\">/en/campus/</a> come "
              "from the same table: they cannot drift apart."),
    ),
}

CSS = """
  /* Vídeos del campus. Mateixes peces que /campus/: el reel només es carrega
     quan algú hi clica, i fins llavors no es demana res a Instagram. */
  .stars { display: grid; grid-template-columns: 1fr; gap: 18px; margin: clamp(26px, 4vw, 44px) 0; }
  @media (min-width: 780px) { .stars { grid-template-columns: repeat(3, 1fr); } }
  .star { border: 1px solid var(--line); background: var(--paper); display: flex; flex-direction: column; }
  .star-play { border: 0; width: 100%; aspect-ratio: 9/14; background: var(--ink); color: #fff; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; font: inherit; }
  .star-play span { font-family: var(--display); font-size: 9px; letter-spacing: 0.24em; text-transform: uppercase; opacity: 0.6; }
  .star-play em { width: 46px; height: 46px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; }
  .star-embed { aspect-ratio: 9/14; }
  .star-embed iframe { width: 100%; height: 100%; border: 0; }
  .star-tx { padding: 18px 18px 20px; }
  .star-tx h4 { font-size: 14px; letter-spacing: 0.1em; margin: 0 0 4px; font-family: var(--display); font-weight: 400; text-transform: uppercase; }
  .star-tx p { font-size: 13px; color: var(--ink-2); margin: 0 0 10px; }
  .star-tx a { font-family: var(--display); font-size: 9.5px; letter-spacing: 0.2em; text-transform: uppercase; }
  .star-tx .role { display: block; font-family: var(--display); font-size: 8.5px; letter-spacing: 0.24em;
    text-transform: uppercase; color: var(--red-dark); margin-bottom: 7px; }
  .stars-group { margin-top: clamp(30px, 4vw, 46px); }
  .stars-group > h3 { font-family: var(--display); font-weight: 400; font-size: 13px; letter-spacing: 0.2em;
    text-transform: uppercase; margin: 0 0 6px; padding-bottom: 9px; border-bottom: 2px solid var(--red); }
  .stars-group > p { font-size: 13.5px; color: var(--ink-2); max-width: 64ch; margin: 12px 0 0; }
  .stars-group .stars { margin-top: clamp(18px, 2.4vw, 26px); }
  /* Les convocatòries són publicacions de feed: quadrades, no verticals. */
  .stars.feed .star-play, .stars.feed .star-embed { aspect-ratio: 1 / 1; }
  /* La taula de pàgines per idioma pot ser més ampla que el mòbil. */
  .tbl-scroll { overflow-x: auto; margin-top: clamp(18px, 2.4vw, 26px); }
  .tbl-scroll table.vs { min-width: 620px; }
  table.vs td a { color: var(--red-dark); }
  .enll-nota { font-size: 13px; color: var(--ink-2); max-width: 66ch; margin-top: clamp(20px, 2.6vw, 30px); }
"""

JS = """
    <script>
      // Un iframe per vídeo, i només quan algú el demana.
      document.querySelectorAll('.star-play').forEach(function (b) {
        b.addEventListener('click', function () {
          var d = document.createElement('div');
          d.className = 'star-embed';
          var kind = b.dataset.kind === 'p' ? 'p' : 'reel';
          d.innerHTML = '<iframe src="https://www.instagram.com/' + kind + '/' + b.dataset.reel +
            '/embed/" loading="lazy" allowtransparency="true" allowfullscreen title="' +
            (b.dataset.title || 'Instagram') + '"></iframe>';
          b.replaceWith(d);
        });
      });
    </script>
"""

PLAY_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">'
            '<path d="M8 5v14l11-7z"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def fitxa(c, t):
    """Una fitxa de vídeo: botó de reproduir + text. c és una fila de les taules
    de build-campus-estrelles.py."""
    i = t["i"]
    nom, rol, tx = c[i], c[i + 3], c[i + 6]
    kind = ' data-kind="p"' if c[1] == "p" else ""
    perfil = f"{IG}/{c[11]}/" if c[11] else f"{IG}/cbgrupbarna/"
    return f"""        <div class="star">
          <button type="button" class="star-play" data-reel="{c[0]}"{kind} data-title="{esc(nom)}" aria-label="{esc(t['reproduir'] + ' ' + nom)}">
            <em>{PLAY_SVG}</em>
            <span>{esc(t['play'])}</span>
          </button>
          <div class="star-tx">
            <h4>{esc(nom)}</h4>
            <span class="role">{esc(rol)}</span>
            <p>{esc(tx)}</p>
            <a href="{perfil}" target="_blank" rel="noopener">{esc(t['veure'])}</a>
          </div>
        </div>"""


def grup(titol, intro, files, t):
    fitxes = "\n".join(fitxa(c, t) for c in files)
    return f"""    <div class="stars-group">
      <h3>{esc(titol)}</h3>
      <p>{esc(intro)}</p>
      <div class="stars">
{fitxes}
      </div>
    </div>"""


def convo(c, t):
    i = t["i"]
    nom, sub = c[i - 1], c[i + 2]
    return f"""        <div class="star">
          <button type="button" class="star-play" data-reel="{c[0]}" data-kind="p" data-title="{esc(nom)}" aria-label="{esc(t['reproduir_convo'] + ' ' + nom)}">
            <em>{PLAY_SVG}</em>
            <span>{esc(t['play'])}</span>
          </button>
          <div class="star-tx">
            <h4>{esc(nom)}</h4>
            <span class="role">{esc(sub)}</span>
            <a href="{IG}/p/{c[0]}/" target="_blank" rel="noopener">{esc(t['veure'])}</a>
          </div>
        </div>"""


def taula(t):
    files = []
    for _clau, noms, subs, rutes in PAGINES:
        nom = esc(noms[IDX[t["lang"]]])
        sub = esc(subs[IDX[t["lang"]]])
        cel = "".join(
            f'<td><a href="{r}">{r}</a></td>' for r in rutes
        )
        files.append(
            f'        <tr><th scope="row">{nom}<br><span style="font-family:var(--body);'
            f'font-size:12.5px;letter-spacing:0;text-transform:none;color:var(--muted)">{sub}'
            f"</span></th>{cel}</tr>"
        )
    cos = "\n".join(files)
    return f"""    <div class="tbl-scroll">
      <table class="vs">
        <thead><tr><th>{esc(t['th_pagina'])}</th><th>{esc(t['th_ca'])}</th><th>{esc(t['th_es'])}</th><th>{esc(t['th_en'])}</th></tr></thead>
        <tbody>
{cos}
        </tbody>
      </table>
    </div>"""


def articles(t):
    j = IDX[t["lang"]]
    targetes = []
    for noms, subs, rutes in ARTICLES:
        targetes.append(f"""      <div class="card">
        <div class="card-body">
          <span class="card-tag">Blog</span>
          <h3><a href="{rutes[j]}">{esc(noms[j])}</a></h3>
          <p>{esc(subs[j])}</p>
        </div>
      </div>""")
    return '    <div class="cards">\n' + "\n".join(targetes) + "\n    </div>"


def cap(t):
    ruta = RUTES[t["lang"]]
    url = SITE + ruta
    alt = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{RUTES[l]}">' for l in ("ca", "es", "en")
    )
    j = IDX[t["lang"]]
    ld = {
        "ca": ("Inici", "/", "/campus/"),
        "es": ("Inicio", "/es/", "/es/campus/"),
        "en": ("Home", "/en/", "/en/campus/"),
    }[t["lang"]]
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10100E">
<title>{esc(t['title'])}</title>
<meta name="description" content="{esc(t['desc'])}">
<link rel="canonical" href="{url}">
{alt}
<link rel="alternate" hreflang="x-default" href="{SITE}{RUTES['ca']}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CB Grup Barna">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:title" content="{esc(t['title'])}">
<meta property="og:description" content="{esc(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/campus-hero.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@cbgrupbarna">
<link rel="icon" href="/logo.png">
<link rel="apple-touch-icon" href="/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/barna.css">
<style>{CSS}</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "CollectionPage",
      "@id": "{url}#webpage",
      "url": "{url}",
      "name": "{esc(t['title'])}",
      "description": "{esc(t['desc'])}",
      "inLanguage": "{t['lang']}",
      "isPartOf": {{ "@id": "{SITE}/#website" }},
      "about": {{ "@id": "{SITE}{ld[2]}#course" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "{url}#crumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "{esc(t['crumb_home'])}", "item": "{SITE}{ld[1]}" }},
        {{ "@type": "ListItem", "position": 2, "name": "{esc(t['crumb_campus'])}", "item": "{SITE}{ld[2]}" }},
        {{ "@type": "ListItem", "position": 3, "name": "{esc(t['crumb_here'])}" }}
      ]
    }}
  ]
}}
</script>
</head>"""


def escorxa(lang):
    """Capçalera i peu de la pàgina germana de Setmana Santa, amb el commutador
    d'idioma reapuntat a aquesta pàgina."""
    cami = os.path.join(ARREL, FONT_ESCORXA[lang])
    with open(cami, encoding="utf-8") as f:
        pag = f.read()
    dalt = pag[pag.index("<body>"): pag.index('<main id="main">') + len('<main id="main">')]
    baix = pag[pag.index('<footer class="foot">'):]
    for vella, clau in zip(RUTES_VELLES, ("ca", "es", "en")):
        dalt = dalt.replace(vella, RUTES[clau])
    return dalt, baix


def pagina(lang):
    t = T[lang]
    dalt, baix = escorxa(lang)
    j = IDX[lang]
    inici = {"ca": "/", "es": "/es/", "en": "/en/"}[lang]
    campus = {"ca": "/campus/", "es": "/es/campus/", "en": "/en/campus/"}[lang]
    wa = ("https://api.whatsapp.com/send?phone=+34698425153&amp;text=Hola!%20Vull%20informaci"
          "%C3%B3%20del%20campus%20del%20CB%20Grup%20Barna")
    convos = "\n".join(convo(c, t) for c in CONVOS)
    cos = f"""
<div class="wrap"><nav class="crumb" aria-label="{esc(t['crumb_here'])}"><a href="{inici}">{esc(t['crumb_home'])}</a> · <a href="{campus}">{esc(t['crumb_campus'])}</a> · <span>{esc(t['crumb_here'])}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{esc(t['eyebrow'])}</p>
    <h1>{esc(t['h1'])}</h1>
    <p class="lede">{esc(t['lede'])}</p>
    <div class="btn-row" style="margin-top:28px">
      <a href="{campus}" class="btn red" data-cta="enllacos-campus">{esc(t['btn_campus'])}</a>
      <a href="{wa}" class="btn ghost" target="_blank" rel="noopener" data-cta="enllacos-whatsapp">{esc(t['btn_wa'])}</a>
    </div>
  </div>

  <div class="narrow prose">
    <h2>{esc(t['h_videos'])}</h2>
    <p>{t['p_videos']}</p>
  </div>
{grup(t['g1'], t['g1p'], NAU, t)}
{grup(t['g2'], t['g2p'], COACHES, t)}
{grup(t['g3'], t['g3p'], ELIT, t)}

  <div class="narrow prose">
    <h2>{esc(t['h_convos'])}</h2>
    <p>{esc(t['p_convos'])}</p>
  </div>
  <div class="stars feed">
{convos}
  </div>

  <div class="narrow prose">
    <h2>{esc(t['h_pagines'])}</h2>
    <p>{esc(t['p_pagines'])}</p>
  </div>
{taula(t)}

  <div class="narrow prose">
    <h2>{esc(t['h_articles'])}</h2>
    <p>{esc(t['p_articles'])}</p>
  </div>
{articles(t)}

  <p class="enll-nota">{t['nota']}</p>
</div>
{JS}
</main>
"""
    return cap(t) + "\n" + dalt + cos + baix


ENLLAC_CAMPUS = {
    "ca": ("/campus/enllacos/", "Tots els vídeos i enllaços →"),
    "es": ("/es/campus/enlaces/", "Todos los vídeos y enlaces →"),
    "en": ("/en/campus/links/", "Every video and link →"),
}
ANCORA = 'data-cta="campus-ig-carnaval"'


def enllaça_des_del_campus(lang, cami, dry):
    """Afegeix l'enllaç a la pàgina nova dins la fila de botons d'Instagram de
    /campus/. Idempotent: si ja hi és, no fa res."""
    ruta, text = ENLLAC_CAMPUS[lang]
    with open(cami, encoding="utf-8") as f:
        pag = f.read()
    if ruta in pag:
        return False
    linia = re.search(r'\n( *)<a [^>]*' + ANCORA + r'[^>]*>.*?</a>', pag)
    if not linia:
        print(f"  avís: no trobo la fila de botons a {cami}, no s'hi afegeix l'enllaç")
        return False
    sagnat = linia.group(1)
    nou = (linia.group(0) + f'\n{sagnat}<a href="{ruta}" class="btn ghost" '
           f'data-cta="campus-enllacos">{text}</a>')
    pag = pag.replace(linia.group(0), nou, 1)
    if not dry:
        with open(cami, "w", encoding="utf-8") as f:
            f.write(pag)
    return True


def main():
    dry = "--dry-run" in sys.argv
    for lang, ruta in RUTES.items():
        cami = os.path.join(ARREL, ruta.strip("/"), "index.html")
        html_pag = pagina(lang)
        if dry:
            print(f"  generaria:  {cami}  ({len(html_pag)} bytes)")
        else:
            os.makedirs(os.path.dirname(cami), exist_ok=True)
            with open(cami, "w", encoding="utf-8") as f:
                f.write(html_pag)
            print(f"  escrit:     {cami}  ({len(html_pag)} bytes)")
    for lang, ruta in {"ca": "campus/index.html", "es": "es/campus/index.html",
                       "en": "en/campus/index.html"}.items():
        cami = os.path.join(ARREL, ruta)
        if enllaça_des_del_campus(lang, cami, dry):
            print(f"  enllaçat des de {ruta}")


if __name__ == "__main__":
    main()
