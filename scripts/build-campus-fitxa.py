#!/usr/bin/env python3
"""Genera la fitxa i el bloc de preus del campus a /campus/, /es/campus/ i /en/campus/.

Per que existeix: /es/campus/ i /en/campus/ tenien la meitat del text de la
catalana i, sobretot, NO DEIEN EL PREU. Pero si que el declaraven a les dades
estructurades: li deien 160 i 195 a Google i no li deien res a la familia que
llegia la pagina. Es la pagina amb mes intencio de compra del lloc i mitja
audiencia la veia incompleta.

Com que el problema de fons era que hi havia tres copies escrites a ma, aixo
surt d'una taula sola. Nomes reescriu entre els marcadors FITXA-CAMPUS.

Des del 23/08/2026 hi ha una decisio de l'Ana, presa i tancada: la quota no
es publica al web (vegeu PENDENTS-WEB.md, «Decisio · els preus no es
publiquen»). Aixo val tambe per al campus. El bloc de preus ja no mostra cap
xifra: explica les dues modalitats i remet a WhatsApp/correu, amb la mateixa
veu que fa servir el FAQ per a la resta de preguntes de diners.

Us:
    python3 scripts/build-campus-fitxa.py
    python3 scripts/build-campus-fitxa.py --dry-run
"""

import os
import re
import sys

# Dos parells de marcadors, no un de sol. Entre la fitxa i els preus, la pagina
# catalana te cinc seccions de text que aquest script no coneix («Que es el
# campus», «Qui hi entrena», «I fora de l'estiu», «El campus i el 3x3», «Com
# s'organitza»). Un rang unic que anes de la fitxa als preus se les enduria
# totes: ja va passar mentre s'escrivia aixo.
F_INICI = "<!-- FITXA-CAMPUS:inici · generat per scripts/build-campus-fitxa.py -->"
F_FINAL = "<!-- FITXA-CAMPUS:final -->"
P_INICI = "<!-- PREUS-CAMPUS:inici · generat per scripts/build-campus-fitxa.py -->"
P_FINAL = "<!-- PREUS-CAMPUS:final -->"

IG = "https://www.instagram.com/cbgrupbarna/"
WA = "+34 698 425 153"

# Cada fila: (etiqueta_ca, valor_ca, etiqueta_es, valor_es, etiqueta_en, valor_en)
FILES = [
    ("Què és",
     "Campus de tecnificació de bàsquet. No és un casal amb pilota: cada setmana treballa un aspecte concret del joc.",
     "Qué es",
     "Campus de tecnificación de baloncesto. No es un casal con pelota: cada semana trabaja un aspecto concreto del juego.",
     "What it is",
     "A basketball skills camp. Not a summer club with a ball: each week works on one specific part of the game."),
    ("Qui l'organitza",
     "CB Grup Barna × Time Chamber. El club hi posa l'estructura i els entrenadors; Time Chamber, la metodologia de treball individual.",
     "Quién lo organiza",
     "CB Grup Barna × Time Chamber. El club pone la estructura y los entrenadores; Time Chamber, la metodología de trabajo individual.",
     "Who runs it",
     "CB Grup Barna × Time Chamber. The club provides the structure and the coaches; Time Chamber, the individual-work method."),
    ("On",
     "La Nau del Clot, Barcelona. Instal·lació oficial del club.",
     "Dónde",
     "La Nau del Clot, Barcelona. Instalación oficial del club.",
     "Where",
     "La Nau del Clot, Barcelona. The club's own venue."),
    ("Adreça",
     "Carrer de la Llacuna, 170-172 · 08018 Barcelona · barri del Clot, Districte de Sant Martí.",
     "Dirección",
     "Carrer de la Llacuna, 170-172 · 08018 Barcelona · barrio del Clot, Distrito de Sant Martí.",
     "Address",
     "Carrer de la Llacuna, 170-172 · 08018 Barcelona · Clot, Sant Martí district."),
    ("Com arribar-hi",
     "Metro L1 Glòries i L2 Clot · Rodalies Clot-Aragó · autobusos del Clot i Glòries. A peu des de Westfield Glòries.",
     "Cómo llegar",
     "Metro L1 Glòries y L2 Clot · Cercanías Clot-Aragó · autobuses del Clot y Glòries. A pie desde Westfield Glòries.",
     "Getting there",
     "Metro L1 Glòries and L2 Clot · Rodalies Clot-Aragó · buses at Clot and Glòries. Walking distance from Westfield Glòries."),
    ("Per a qui",
     "Set categories: Escoleta, Premini, Mini, Preinfantil, Infantil, Cadet i Júnior. Els grups es fan per categoria i nivell, de manera que qui comença no entrena amb qui ja porta anys competint.",
     "Para quién",
     "Siete categorías: Escoleta, Premini, Mini, Preinfantil, Infantil, Cadete y Júnior. Los grupos se hacen por categoría y nivel, de modo que quien empieza no entrena con quien lleva años compitiendo.",
     "Who it's for",
     "Seven age groups, from Escoleta to Júnior. Groups are set by age and level, so a beginner never trains alongside someone who has been competing for years."),
    ("Nens i nenes",
     "Sí. El campus és mixt i el club té paritat real entre la línia femenina i la masculina.",
     "Niños y niñas",
     "Sí. El campus es mixto y el club tiene paridad real entre la línea femenina y la masculina.",
     "Boys and girls",
     "Yes. The camp is mixed, and the club has real parity between its girls' and boys' sides."),
    ("Cal ser del Barna?",
     "No. És obert a jugadors i jugadores de qualsevol club de Barcelona i de la província. Els del club tenen prioritat d'inscripció i preu propi.",
     "¿Hay que ser del Barna?",
     "No. Está abierto a jugadores y jugadoras de cualquier club de Barcelona y de la provincia. Los del club tienen prioridad de inscripción y precio propio.",
     "Do you have to be a Barna player?",
     "No. It is open to players from any club in Barcelona and the province. Club players get priority and their own price."),
    ("Quan",
     "A l'estiu, en setmanes consecutives de finals de juny a principis d'agost. L'edició 2026 va anar del 23 de juny a l'1 d'agost.",
     "Cuándo",
     "En verano, en semanas consecutivas de finales de junio a principios de agosto. La edición 2026 fue del 23 de junio al 1 de agosto.",
     "When",
     "In summer, in consecutive weeks from late June to early August. The 2026 edition ran from 23 June to 1 August."),
    ("Horari",
     "Jornada completa de 9:00 a 17:00 h · mitja jornada de 9:00 a 13:30 h.",
     "Horario",
     "Jornada completa de 9:00 a 17:00 h · media jornada de 9:00 a 13:30 h.",
     "Hours",
     "Full day 9:00 to 17:00 · half day 9:00 to 13:30."),
    ("Preu",
     "Depèn de la modalitat i de si ets del club. No es publica al web: escriu-nos amb l'edat i te la diem el mateix dia. Pagament fraccionat disponible.",
     "Precio",
     "Depende de la modalidad y de si eres del club. No se publica en la web: escríbenos con la edad y te la damos el mismo día. Pago fraccionado disponible.",
     "Price",
     "Depends on the modality and whether you play for the club. Not published on the site: message us with the age and we'll give it to you the same day. Payment in instalments available."),
    ("Dinar",
     "Inclòs a la jornada completa. La mitja jornada acaba abans de dinar.",
     "Comida",
     "Incluida en la jornada completa. La media jornada acaba antes de comer.",
     "Lunch",
     "Included in the full day. The half day ends before lunch."),
    ("Serveis",
     "Servei d'acollida al matí, dinar a la jornada completa i excursió el divendres a Illa Fantasia.",
     "Servicios",
     "Servicio de acogida por la mañana, comida en la jornada completa y excursión el viernes a Illa Fantasia.",
     "Extras",
     "Early drop-off in the morning, lunch on the full day, and a Friday trip to Illa Fantasia."),
    ("Què s'hi treballa",
     "Tir, maneig de pilota, joc de l'1x1, fonaments individuals i lectura de joc. Cada setmana té un focus propi, de manera que qui ve més d'una setmana no repeteix.",
     "Qué se trabaja",
     "Tiro, manejo de balón, juego del 1x1, fundamentos individuales y lectura de juego. Cada semana tiene un foco propio, de modo que quien viene más de una semana no repite.",
     "What is worked on",
     "Shooting, ball handling, one-on-one play, individual fundamentals and reading the game. Each week has its own focus, so coming for more than one week never means repeating."),
    ("Qui hi entrena",
     "Els entrenadors del club i de Time Chamber. Hi han passat Robert Willett (entrenador NBA, @bballwillett), Ainhoa López (jugadora professional, selecció espanyola) i Malak Shady (MVP de 3x3).",
     "Quién entrena",
     "Los entrenadores del club y de Time Chamber. Han pasado Robert Willett (entrenador NBA, @bballwillett), Ainhoa López (jugadora profesional, selección española) y Malak Shady (MVP de 3x3).",
     "Who coaches",
     "The club's own coaches and Time Chamber's. Robert Willett (NBA coach, @bballwillett), Ainhoa López (professional player, Spanish national team) and Malak Shady (3x3 MVP) have all been through."),
    ("Quants n'hi ha",
     "Més de 200 jugadors i jugadores per edició, amb un límit aproximat de 50 places per setmana per mantenir la ràtio de treball.",
     "Cuántos hay",
     "Más de 200 jugadores y jugadoras por edición, con un límite aproximado de 50 plazas por semana para mantener la ratio de trabajo.",
     "How many",
     "More than 200 players per edition, with a cap of around 50 places a week to keep the coach-to-player ratio."),
    ("Idioma",
     "Català i castellà. Els entrenadors convidats internacionals treballen en anglès amb traducció.",
     "Idioma",
     "Catalán y castellano. Los entrenadores invitados internacionales trabajan en inglés con traducción.",
     "Language",
     "Catalan and Spanish. International guest coaches work in English, with translation."),
    ("Com inscriure-s'hi",
     f"Per WhatsApp al {WA} o pel formulari del club. Les darreres edicions s'han omplert abans de començar.",
     "Cómo inscribirse",
     f"Por WhatsApp al {WA} o por el formulario del club. Las últimas ediciones se han llenado antes de empezar.",
     "How to sign up",
     f"By WhatsApp on {WA} or through the club's form. Recent editions have filled up before they started."),
]

T = {
    "ca": dict(
        i=0,
        h2f="Fitxa del campus",
        ledef=('Totes les dades en un sol lloc, sense haver de buscar-les per la pàgina. La darrera edició '
               'tancada és l\'<strong>Estiu 2026</strong>; les dates de la propera s\'anuncien aquí i a '
               f'<a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a>.'),
        h2p="Preus",
        ledep=("Dues modalitats segons horari, amb àpat inclòs a la jornada completa. Places obertes a "
               "jugadors i jugadores del Barna i de fora del club."),
        tag1="Recomanat", head1="Setmana completa", sched1="9h a 17h",
        li1a="Àpat de migdia inclòs", li1b="Servei d'acollida des de les 9h",
        tag2="Alternativa", head2="Mitja jornada", sched2="9h a 13:30h",
        li2a="Mateixos grups i mateix focus setmanal",
        notap=(f'La quota no es publica al web: escriu-nos per WhatsApp al {WA} o per correu amb l\'edat '
               'del jugador o jugadora i te la diem el mateix dia. Es pot reservar plaça amb pagament '
               'fraccionat en fins a 3 terminis, i cada any s\'obre un descompte per inscripció '
               f'anticipada; les dates i el codi es publiquen aquí i a '
               f'<a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a> quan s\'obren les inscripcions.'),
    ),
    "es": dict(
        i=2,
        h2f="Ficha del campus",
        ledef=('Todos los datos en un solo sitio, sin tener que buscarlos por la página. La última edición '
               'cerrada es el <strong>Verano 2026</strong>; las fechas de la próxima se anuncian aquí y en '
               f'<a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a>.'),
        h2p="Precios",
        ledep=("Dos modalidades según horario, con comida incluida en la jornada completa. Plazas abiertas a "
               "jugadores y jugadoras del Barna y de fuera del club."),
        tag1="Recomendado", head1="Semana completa", sched1="9h a 17h",
        li1a="Comida de mediodía incluida", li1b="Servicio de acogida desde las 9h",
        tag2="Alternativa", head2="Media jornada", sched2="9h a 13:30h",
        li2a="Mismos grupos y mismo foco semanal",
        notap=(f'La cuota no se publica en la web: escríbenos por WhatsApp al {WA} o por correo con la '
               'edad del jugador o jugadora y te la damos el mismo día. Se puede reservar plaza con pago '
               'fraccionado en hasta 3 plazos, y cada año se abre un descuento por inscripción '
               'anticipada; las fechas y el código se publican en esta página y en '
               f'<a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a> cuando se abren las inscripciones.'),
    ),
    "en": dict(
        i=4,
        h2f="Camp fact sheet",
        ledef=('Everything in one place, so you don\'t have to hunt through the page for it. The last '
               'completed edition is <strong>Summer 2026</strong>; dates for the next one are announced here '
               f'and on <a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a>.'),
        h2p="Prices",
        ledep=("Two options depending on hours, with lunch included on the full day. Open to Barna players "
               "and to players from any other club."),
        tag1="Most chosen", head1="Full week", sched1="9 to 17",
        li1a="Lunch included", li1b="Early drop-off from 9",
        tag2="Alternative", head2="Half day", sched2="9 to 13:30",
        li2a="Same groups, same weekly focus",
        notap=(f'The price is not published on the site: message us on WhatsApp at {WA} or by email with '
               'the age and we\'ll give it to you the same day. Places can be held with payment in up to '
               '3 instalments. Every year there is an early-bird discount; the dates and the code go up '
               f'on this page and on <a href="{IG}" target="_blank" rel="noopener">@cbgrupbarna</a> '
               'when sign-ups open.'),
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bloc_fitxa(lang):
    t = T[lang]
    i = t["i"]
    files = "\n".join(
        '    <div class="dl-row"><dt>%s</dt><dd>%s</dd></div>' % (esc(f[i]), esc(f[i + 1]))
        for f in FILES
    )
    return f"""{F_INICI}
    <h2>{esc(t['h2f'])}</h2>
    <p>{t['ledef']}</p>
  </div>
  <dl class="dl narrow">
{files}
  </dl>
  <div class="narrow prose">
    {F_FINAL}"""


def bloc_preus(lang):
    t = T[lang]
    return f"""{P_INICI}
    <h2>{esc(t['h2p'])}</h2>
    <p>{esc(t['ledep'])}</p>
    <div class="price-cards">
      <div class="price-card top">
        <span class="tag">{esc(t['tag1'])}</span>
        <b>{esc(t['head1'])}</b>
        <p class="sched">{esc(t['sched1'])}</p>
        <ul>
          <li>{esc(t['li1a'])}</li>
          <li>{esc(t['li1b'])}</li>
        </ul>
      </div>
      <div class="price-card">
        <span class="tag">{esc(t['tag2'])}</span>
        <b>{esc(t['head2'])}</b>
        <p class="sched">{esc(t['sched2'])}</p>
        <ul>
          <li>{esc(t['li2a'])}</li>
        </ul>
      </div>
    </div>
    <p class="price-note">{t['notap']}</p>
    {P_FINAL}"""


FITXERS = {"ca": "campus/index.html", "es": "es/campus/index.html", "en": "en/campus/index.html"}


def main():
    dry = "--dry-run" in sys.argv
    for lang, cami in FITXERS.items():
        if not os.path.isfile(cami):
            sys.exit(f"No trobo {cami}. Executa'm des de l'arrel del repositori.")
        text = open(cami, encoding="utf-8").read()
        nou = text
        for ini, fi, fn, nom in (
            (F_INICI, F_FINAL, bloc_fitxa, "FITXA-CAMPUS"),
            (P_INICI, P_FINAL, bloc_preus, "PREUS-CAMPUS"),
        ):
            if ini not in nou or fi not in nou:
                sys.exit(
                    f"{cami} no te els marcadors {nom}. Posa'ls-hi a ma un cop "
                    "i despres ja es podra regenerar sol."
                )
            nou = re.sub(
                re.escape(ini) + r".*?" + re.escape(fi),
                lambda _, f=fn: f(lang),
                nou,
                flags=re.S,
            )
        if nou == text:
            print(f"  sense canvis: {cami}")
        elif dry:
            print(f"  canviaria:    {cami}  ({len(FILES)} files + preus)")
        else:
            open(cami, "w", encoding="utf-8").write(nou)
            print(f"  escrit:       {cami}  ({len(FILES)} files + preus)")
    if dry:
        print("--dry-run: no he escrit res.")


if __name__ == "__main__":
    main()
