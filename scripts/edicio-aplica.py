#!/usr/bin/env python3
"""Aplica la portada D, «L'Edicio», a la newsletter i les seves traduccions.

La quarta de les quatre portades del 30/08/2026. Per decisio de l'Ana va a
la newsletter SETMANAL: la premsa escrita del club, amb tres peces fixes a
cada numero —l'Open Day dels preferents del cap de setmana, l'obertura del
calendari de partits i un post del blog.

Fa dues coses:

  1. Posa la capcalera de diari a /newsletter/ i les dues traduccions: la
     cinta del numero, el masthead, el teletip de la jornada, la primera
     plana amb el sumari i el colofo.
  2. Corregeix la cadencia. Les tres pagines deien «un enviament al mes»
     perque la decisio d'abans era mensual; l'Ana la va canviar a setmanal
     el 30/08. Es canvia a la meta, a l'og, al JSON-LD i al text.

La FAQ NO es toca aqui: la manté .github/scripts/generate-faq.py des de
i18n/faq.yml, i alla es on s'ha canviat la cadencia.

Idempotent: passar-lo dues vegades deixa el fitxer igual.
"""
from __future__ import annotations

import os
import sys

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FOTO_PORTADA = "/fotos/web/presentacio-equips-25-26-msufdc03/1786803048160-zpte6.webp"
FOTO_PEU = "/escoleta/img/escoleta-2026-03.jpg"

T = {
    "ca": {
        "fitxer": "newsletter/index.html",
        "capcalera": "El diari del Clot",
        "numero": "Edició núm. 61 · Temporada 26-27",
        "cadencia": "Número nou cada setmana",
        "eyebrow": "El club · Cada setmana",
        "mast1": "La Newsletter",
        "mast2": "del Barna",
        "segell": "Des de 1965<br>El Clot · BCN",
        "teletip": "Jornada 1 · 5 de setembre <b>●</b> Cadet Fem. B — Boet Mataró, 10:45 "
                   "<b>●</b> Infantil Masc. B — L'Hospitalet, 10:45 <b>●</b> Júnior Fem. B "
                   "— Ateneu Montserrat, 12:30 <b>●</b> Entrada lliure a la Nau <b>●</b> ",
        "foto_alt": "Tres directius del club, amb la bufanda del Barna, seguint el partit "
                    "asseguts a la grada de La Nau",
        "titular": "El barri té equip",
        "entrada": "Cada setmana surt un número nou: qui juga i on, què s'obre abans que "
                   "enlloc, i una peça escrita des de dins del club. No és un butlletí de "
                   "tot — és el que de veritat val la pena saber.",
        "folio": "S'envia cada setmana · pàg. 1",
        "sumari": "Cada setmana",
        "peces": [
            ("Dv.", "Open Day dels preferents",
             "La convocatòria del cap de setmana: qui hi entra, a quina hora i què hi veurà."),
            ("Ds.", "Obrim el calendari de partits",
             "La jornada sencera de tots els equips, hores i pista. La manté sol el robot de la FCBQ."),
            ("Dm.", "Un post del blog",
             "Una peça de l'Observatori cada setmana, escrita des de dins del club."),
        ],
        "num_peu": "peces fixes<br>a cada número",
        "peu_foto": "Jugador de l'Escoleta botant la pilota a La Nau del Clot",
        "peu_titol": 'Un número cada <em>setmana</em>',
        "peu_text": "Apunta-t'hi aquí sota. El correu és l'única cosa obligatòria i a cada "
                    "enviament hi ha l'enllaç de baixa, que funciona a la primera.",
        "colofo": ["Escrit a La Nau del Clot", "#SOMCLOT", "CB Grup Barna · des de 1965"],
        "canvis": [
            ("Un enviament al mes i baixa amb un clic.", "Un enviament la setmana i baixa amb un clic."),
            ("El correu del club: una vegada al mes, el que de veritat val la pena saber.",
             "El correu del club: una vegada la setmana, el que de veritat val la pena saber."),
            ("<strong>Res més.</strong> Un enviament al mes. Si un mes no hi ha res a explicar, no enviem res.",
             "<strong>Res més.</strong> Un enviament la setmana. Si una setmana no hi ha res a explicar, no enviem res."),
            ("<strong>Calendari</strong> — què hi ha aquest mes i on.",
             "<strong>Calendari</strong> — què hi ha aquest cap de setmana i on."),
        ],
    },
    "es": {
        "fitxer": "es/newsletter/index.html",
        "capcalera": "El diario del Clot",
        "numero": "Edición núm. 61 · Temporada 26-27",
        "cadencia": "Número nuevo cada semana",
        "eyebrow": "El club · Cada semana",
        "mast1": "La Newsletter",
        "mast2": "del Barna",
        "segell": "Desde 1965<br>El Clot · BCN",
        "teletip": "Jornada 1 · 5 de septiembre <b>●</b> Cadete Fem. B — Boet Mataró, 10:45 "
                   "<b>●</b> Infantil Masc. B — L'Hospitalet, 10:45 <b>●</b> Júnior Fem. B "
                   "— Ateneu Montserrat, 12:30 <b>●</b> Entrada libre en la Nau <b>●</b> ",
        "foto_alt": "Tres directivos del club, con la bufanda del Barna, siguiendo el partido "
                    "sentados en la grada de La Nau",
        "titular": "El barrio tiene equipo",
        "entrada": "Cada semana sale un número nuevo: quién juega y dónde, qué se abre antes "
                   "que en ningún sitio, y una pieza escrita desde dentro del club. No es un "
                   "boletín de todo — es lo que de verdad vale la pena saber.",
        "folio": "Se envía cada semana · pág. 1",
        "sumari": "Cada semana",
        "peces": [
            ("Vi.", "Open Day de los preferentes",
             "La convocatoria del fin de semana: quién entra, a qué hora y qué verá."),
            ("Sá.", "Abrimos el calendario de partidos",
             "La jornada entera de todos los equipos, horas y pista. La mantiene solo el robot de la FCBQ."),
            ("Ma.", "Un post del blog",
             "Una pieza del Observatorio cada semana, escrita desde dentro del club."),
        ],
        "num_peu": "piezas fijas<br>en cada número",
        "peu_foto": "Jugador de la Escoleta botando la pelota en La Nau del Clot",
        "peu_titol": 'Un número cada <em>semana</em>',
        "peu_text": "Apúntate aquí abajo. El correo es lo único obligatorio y en cada envío "
                    "está el enlace de baja, que funciona a la primera.",
        "colofo": ["Escrito en La Nau del Clot", "#SOMCLOT", "CB Grup Barna · desde 1965"],
        "canvis": [
            ("Un envío al mes y baja con un clic.", "Un envío a la semana y baja con un clic."),
            ("El correo del club: una vez al mes, lo que de verdad merece la pena saber.",
             "El correo del club: una vez a la semana, lo que de verdad merece la pena saber."),
            ("<strong>Nada más.</strong> Un envío al mes. Si un mes no hay nada que contar, no enviamos nada.",
             "<strong>Nada más.</strong> Un envío a la semana. Si una semana no hay nada que contar, no enviamos nada."),
            ("<strong>Calendario</strong> — qué hay este mes y dónde.",
             "<strong>Calendario</strong> — qué hay este fin de semana y dónde."),
        ],
    },
    "en": {
        "fitxer": "en/newsletter/index.html",
        "capcalera": "The El Clot paper",
        "numero": "Issue no. 61 · Season 26-27",
        "cadencia": "A new issue every week",
        "eyebrow": "The club · Every week",
        "mast1": "The Barna",
        "mast2": "Newsletter",
        "segell": "Since 1965<br>El Clot · BCN",
        "teletip": "Round 1 · 5 September <b>●</b> Cadet Women B — Boet Mataró, 10:45 "
                   "<b>●</b> Under-14 Men B — L'Hospitalet, 10:45 <b>●</b> Junior Women B "
                   "— Ateneu Montserrat, 12:30 <b>●</b> Free entry at La Nau <b>●</b> ",
        "foto_alt": "Three club directors wearing Barna scarves, watching the game from the "
                    "stands at La Nau",
        "titular": "The neighbourhood has a team",
        "entrada": "A new issue every week: who plays and where, what opens before it opens "
                   "anywhere else, and one piece written from inside the club. It is not a "
                   "bulletin about everything — it is what is actually worth knowing.",
        "folio": "Sent every week · p. 1",
        "sumari": "Every week",
        "peces": [
            ("Fri.", "Open Day for members",
             "The weekend call-up: who gets in, at what time and what they will see."),
            ("Sat.", "We open the match calendar",
             "The full round for every team, times and court. Kept up to date by the FCBQ robot."),
            ("Tue.", "A post from the blog",
             "One Observatory piece a week, written from inside the club."),
        ],
        "num_peu": "fixed pieces<br>in every issue",
        "peu_foto": "Escoleta player dribbling the ball at La Nau del Clot",
        "peu_titol": 'One issue every <em>week</em>',
        "peu_text": "Sign up just below. The email address is the only thing we need, and "
                    "every issue carries an unsubscribe link that works first time.",
        "colofo": ["Written at La Nau del Clot", "#SOMCLOT", "CB Grup Barna · since 1965"],
        "canvis": [
            ("One email a month, unsubscribe in one click.", "One email a week, unsubscribe in one click."),
            ("The club's email: once a month, what is actually worth knowing.",
             "The club's email: once a week, what is actually worth knowing."),
            ("<strong>Nothing else.</strong> One email a month. If there is nothing to say that month, we send nothing.",
             "<strong>Nothing else.</strong> One email a week. If there is nothing to say that week, we send nothing."),
            ("<strong>Calendar</strong> — what is on this month, and where.",
             "<strong>Calendar</strong> — what is on this weekend, and where."),
        ],
    },
}


def portada(d: dict) -> str:
    briefs = "".join(
        '\n    <div class="ed-brief"><span class="pg">{}</span><b>{}</b>'
        "<span>{}</span></div>".format(dia, titol, text)
        for dia, titol, text in d["peces"]
    )
    return """<section class="ed" aria-labelledby="ed-titol">
  <div class="ed-bar">
    <span>{capcalera}</span>
    <span class="r">{numero}</span>
    <span>{cadencia}</span>
  </div>
  <div class="ed-mast">
    <p class="eyebrow red">{eyebrow}</p>
    <h1 id="ed-titol">{mast1}<br><span class="out">{mast2}</span></h1>
    <span class="stamp">{segell}</span>
  </div>
  <!-- El teletip repeteix el text dues vegades: l'animacio el desplaça un
       50 % i ha de tornar a començar sense forat. -->
  <div class="ed-marq" aria-hidden="true"><span class="in">{teletip}{teletip}</span></div>
  <div class="ed-grid">
    <div class="ed-main">
      <div class="ed-duo"><img src="{foto}" alt="{foto_alt}" width="2048" height="1365" fetchpriority="high" decoding="async"></div>
      <h2>{titular}</h2>
      <p class="stand">{entrada}</p>
      <p class="folio">{folio}</p>
    </div>
    <div class="ed-side">
      <div class="hd">{sumari}</div>{briefs}
      <div class="ed-num"><span class="n">3</span><span>{num_peu}</span></div>
    </div>
  </div>
  <div class="ed-foot">
    <div class="duo"><img src="{foto_peu}" alt="{peu_foto}" width="900" height="1200" loading="lazy" decoding="async"></div>
    <div class="say">
      <h2>{peu_titol}</h2>
      <p>{peu_text}</p>
    </div>
  </div>
  <div class="ed-colo">{colofo}</div>
</section>
""".format(
        briefs=briefs,
        foto=FOTO_PORTADA,
        foto_peu=FOTO_PEU,
        colofo="".join("<span>{}</span>".format(x) for x in d["colofo"]),
        **{k: v for k, v in d.items() if k not in ("fitxer", "peces", "canvis", "colofo")},
    )


def aplica(codi: str) -> list[str]:
    d = T[codi]
    ruta = os.path.join(ARREL, d["fitxer"])
    with open(ruta, encoding="utf-8") as f:
        html = f.read()
    original = html
    fets = []

    # 1 · La cadencia. Abans que res, perque el text vell encara hi es.
    canviats = 0
    for vell, nou in d["canvis"]:
        if vell in html:
            html = html.replace(vell, nou)
            canviats += 1
    # La descripcio va tambe al JSON-LD, on els apostrofs surten escapats.
    for vell, nou in d["canvis"][:1]:
        esc_vell = vell.replace("'", "\\u2019").replace("í", "\\u00ed").replace("ú", "\\u00fa")
        if esc_vell in html:
            html = html.replace(esc_vell, nou.replace("'", "\\u2019").replace("í", "\\u00ed").replace("ú", "\\u00fa"))
            canviats += 1
    if canviats:
        fets.append(f"{canviats} canvis de cadència")

    # 2 · La portada, al lloc del .phead.
    if 'class="ed"' not in html:
        inici = html.find('<div class="phead narrow">')
        if inici < 0:
            print(f"  ! {d['fitxer']}: no s'ha trobat el .phead", file=sys.stderr)
        else:
            # El .phead viu dins d'un <div class="wrap">; la portada ha de
            # sortir a tota l'amplada, o sigui abans d'aquell wrap.
            obre = html.rfind('<div class="wrap">', 0, inici)
            tanca = html.find("</div>", html.find("</p>", html.find('class="lede"', inici))) + len("</div>")
            html = html[:obre] + portada(d) + html[obre:tanca] + html[tanca:]
            # Ara el .phead es duplicat: es treu del wrap.
            i2 = html.find('<div class="phead narrow">')
            j2 = html.find("</div>", html.find('class="lede"', i2)) + len("</div>")
            html = html[:i2] + html[j2:]
            fets.append("portada")

    if html != original:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
    return fets


def main() -> int:
    for codi in T:
        fets = aplica(codi)
        print(f"{T[codi]['fitxer']}: {', '.join(fets) if fets else 'ja hi era'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
