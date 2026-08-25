#!/usr/bin/env python3
"""Genera /es/partits/ i /en/partits/ a partir de /partits/.

Per que existeix: les versions en castella i angles de «Dies de partit» NO
eren la pagina publica traduida. Eren una altra cosa: l'eina de GESTIO del
club, de 152 KB, amb sis pestanyes i un formulari d'entrada, mentre que la
catalana es una pagina publica neta de 33 KB. Qui llegia la web en castella o
en angles no arribava mai al calendari; arribava al taulell d'administracio.

Com que el problema de fons era que hi havia tres copies escrites a ma que
havien divergit fins a ser pagines diferents, aixo passa a tenir una sola
font: la catalana. Les altres dues es generen.

Que NO es tradueix, a proposit:
  - noms d'equip i de competicio (C.B GRUP BARNA B, C.C. CADET FEMENI...),
    que son els noms oficials de la FCBQ;
  - noms de pavello i de poblacio;
  - el text de dins dels marcadors SEO-SNAPSHOT, SEO-EVENTS i SEO-EQUIPS, que
    el genera .github/scripts/generate-seo-snapshot.py.

Es pot executar tantes vegades com calgui: la sortida nomes depen de la pagina
catalana, aixi que passar-hi dues vegades dona el mateix fitxer.

Com esta fet, i per que importa: totes les taules de text (TEXTOS, JS,
JS_DATES, LD) es passen EN UNA SOLA passada amb marques intermedies i ordenades
per llargada. Fer-ho taula per taula tenia un error dificil de veure: una frase
curta d'una taula es menjava el principi d'una de llarga d'una altra i la
deixava mig traduida per sempre, dins d'una resposta de la FAQ, on ningu no hi
mirava. Abans de escriure res, `_comprova` busca restes de catala al text que
es veu i s'atura si en troba.

Us:
    python3 scripts/build-partits-idiomes.py
    python3 scripts/build-partits-idiomes.py --dry-run
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "partits" / "index.html"

# Cap a on va cada enllaç intern en castella i en angles. NO es una llista
# escrita a ma: es llegeix del <link rel="alternate" hreflang> de la propia
# pagina catalana de desti. Aixi, si una seccio canvia d'adreca o se'n tradueix
# una de nova, aixo ho segueix sol i no cal tocar aquest fitxer.
#
# Abans hi havia una llista fixa amb el suposit que l'adreca era la mateixa en
# els tres idiomes (/escoleta/ → /es/escoleta/). No sempre ho es:
# /politica-de-privacitat/ es /es/politica-de-privacidad/ i /en/privacy-policy/,
# i /proteccio-menor/ es /en/child-protection/. Amb la llista fixa, el peu de
# la pagina castellana enviava a la politica de privacitat EN CATALA.
def _mapa_traduccions():
    mapa = {}
    for fitxer in ROOT.rglob("index.html"):
        rel = fitxer.relative_to(ROOT).as_posix()
        if rel.startswith(("es/", "en/", ".git/", "galeria/node_modules/")):
            continue
        try:
            text = fitxer.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        alts = {}
        for etiqueta in re.finditer(r'<link[^>]*rel="alternate"[^>]*>', text):
            t = etiqueta.group(0)
            lg = re.search(r'hreflang="([^"]+)"', t)
            hf = re.search(r'href="([^"]+)"', t)
            if lg and hf and lg.group(1) in ("ca", "es", "en"):
                alts[lg.group(1)] = re.sub(r'^https?://(www\.)?cbgrupbarna\.info', '', hf.group(1))
        if len(alts) == 3:
            ca = "/" + rel[: -len("index.html")]
            mapa[ca] = alts
    return mapa

# Text de la interficie. L'ordre importa: els fragments llargs, primer, perque
# no se'ls mengi una substitucio mes curta.
TEXTOS = [
    # (catala, castella, angles)
    ("Calendari · dies de partit i resultats · CB Grup Barna",
     "Calendario · días de partido y resultados · CB Grup Barna",
     "Calendar · match days and fixtures · CB Grup Barna"),
    ("Tots els equips federats del club, en un sol calendari. S'actualitza cada dia a partir",
     "Todos los equipos federados del club, en un solo calendario. Se actualiza cada día a partir",
     "Every federated team at the club, in one calendar. Updated daily from"),
    ("del calendari oficial de la",
     "del calendario oficial de la",
     "the official calendar of the"),
    ("Federació Catalana de Basquetbol",
     "Federación Catalana de Baloncesto",
     "Catalan Basketball Federation"),
    (": dia, hora,\n          rival, casa o fora i pista, i els resultats de la jornada anterior.",
     ": día, hora,\n          rival, casa o fuera y pista, y los resultados de la jornada anterior.",
     ": day, time,\n          opponent, home or away and venue, plus last round's results."),
    ("La primera plantilla del club, femenina i masculina, els seus propers partits.",
     "La primera plantilla del club, femenina y masculina, y sus próximos partidos.",
     "The club's first teams, women's and men's, and their next fixtures."),
    ("Cal activar JavaScript per veure el Gameday Seniors.",
     "Hay que activar JavaScript para ver el Gameday Seniors.",
     "JavaScript needs to be enabled to see the Seniors Gameday."),
    ("Cal activar JavaScript per veure els resultats.",
     "Hay que activar JavaScript para ver los resultados.",
     "JavaScript needs to be enabled to see the results."),
    ("Cal activar JavaScript per veure el calendari complet.",
     "Hay que activar JavaScript para ver el calendario completo.",
     "JavaScript needs to be enabled to see the full calendar."),
    ("Tots els partits de la temporada, mes a mes. També pots subscriure-t'hi des de",
     "Todos los partidos de la temporada, mes a mes. También puedes suscribirte desde",
     "Every fixture of the season, month by month. You can also subscribe from"),
    ("Google Calendar, Apple o Outlook i rebre els canvis d'hora automàticament.",
     "Google Calendar, Apple u Outlook y recibir los cambios de hora automáticamente.",
     "Google Calendar, Apple or Outlook and get time changes automatically."),
    ("Cada equip té la seva pàgina amb la competició, el balanç i el calendari complet.",
     "Cada equipo tiene su página con la competición, el balance y el calendario completo.",
     "Each team has its own page with the competition, its record and the full calendar."),
    ("Els dies de partit es viuen a la Nau del Clot. I els que no hi puguis ser,",
     "Los días de partido se viven en la Nau del Clot. Y los que no puedas venir,",
     "Match days happen at La Nau del Clot. And when you can't make it,"),
    ("els resultats i les millors jugades surten a l'Instagram del club.",
     "los resultados y las mejores jugadas salen en el Instagram del club.",
     "the results and the best plays go up on the club's Instagram."),
    ("Resultats del cap de setmana anterior",
     "Resultados del fin de semana anterior",
     "Last weekend's results"),
    ("Pròxims partits del CB Grup Barna",
     "Próximos partidos del CB Grup Barna",
     "Upcoming CB Grup Barna fixtures"),
    ("Calendari global de tots els equips",
     "Calendario global de todos los equipos",
     "Full calendar, all teams"),
    ("Temporada 2026-2027 · #SomClot",
     "Temporada 2026-2027 · #SomClot",
     "2026-2027 season · #SomClot"),
    ("Vine a la Nau. O segueix-nos.",
     "Ven a la Nau. O síguenos.",
     "Come to La Nau. Or follow us."),
    ("A la pista i a les xarxes",
     "En la pista y en las redes",
     "On court and online"),
    ("Subscriure'm al calendari (.ics)",
     "Suscribirme al calendario (.ics)",
     "Subscribe to the calendar (.ics)"),
    ("Calendari per equip", "Calendario por equipo", "Team calendars"),
    ("Aquest cap de setmana", "Este fin de semana", "This weekend"),
    ("Descarregar per equip", "Descargar por equipo", "Download by team"),
    ("Posicionament del club", "Posicionamiento del club", "Where the club stands"),
    ("La jornada anterior", "La jornada anterior", "Last round"),
    ("Política de privacitat", "Política de privacidad", "Privacy policy"),
    ("Preguntes freqüents", "Preguntas frecuentes", "Frequently asked questions"),
    ("Demanar informació", "Pedir información", "Request information"),
    ("Calendaris per equip", "Calendario por equipo", "Team calendars"),
    ("Premi Dona i Esport", "Premio Mujer y Deporte", "Women and Sport Award"),
    ("Articles i premsa", "Artículos y prensa", "Articles and press"),
    ("Campus de bàsquet", "Campus de baloncesto", "Basketball camp"),
    ("Escola de bàsquet", "Escuela de baloncesto", "Basketball school"),
    ("Galeria de fotos", "Galería de fotos", "Photo gallery"),
    ("Saltar al contingut", "Saltar al contenido", "Skip to content"),
    # Trossos que quedaven en català a la pàgina traduïda (vistos amb el
    # navegador, no llegint el fitxer): el fil d'Ariadna, l'etiqueta de local
    # o visitant de cada partit i l'avís de quan encara no hi ha resultats.
    ("La temporada 2026-2027 encara no ha començat: el primer cap de setmana amb partits és el del 5 i 6 de setembre. Els resultats sortiran aquí l\\'endemà de cada jornada.",
     "La temporada 2026-2027 todavía no ha empezado: el primer fin de semana con partidos es el del 5 y 6 de septiembre. Los resultados saldrán aquí al día siguiente de cada jornada.",
     "The 2026-2027 season has not started yet: the first weekend with matches is 5 and 6 September. Results will appear here the day after each round."),
    # Els avisos de quan no hi ha res a ensenyar. Es veuen poc, pero es veuen:
    # fora de temporada la pagina es NOMES aixo, i qui la llegia en angles la
    # trobava en catala sencera.
    ("Encara no hi ha partits programats per als equips sèniors.",
     "Todavía no hay partidos programados para los equipos sénior.",
     "No fixtures scheduled yet for the senior teams."),
    ("No hi ha partits programats a partir d\\'avui. Consulta el calendari global aquí sota.",
     "No hay partidos programados a partir de hoy. Consulta el calendario global aquí abajo.",
     "No fixtures scheduled from today. See the full calendar below."),
    ("No s\\'ha pogut carregar el calendari. Torna-ho a provar d\\'aquí una estona.",
     "No se ha podido cargar el calendario. Vuelve a probarlo dentro de un rato.",
     "The calendar could not be loaded. Try again in a little while."),
    ("Dies de partit", "Días de partido", "Match days"),
    (">A casa<", ">En casa<", ">Home<"),
    ("'A casa contra '", "'En casa contra '", "'Home vs '"),
    ("'Fora contra '", "'Fuera contra '", "'Away at '"),
    ("' partits</i></summary>'", "' partidos</i></summary>'", "' fixtures</i></summary>'"),
    ("'A casa'", "'En casa'", "'Home'"),
    (">Fora<", ">Fuera<", ">Away<"),
    # Text que nomes llegeix qui fa servir un lector de pantalla: si no es
    # tradueix, el sent en catala tot i llegir la pagina en un altre idioma.
    ("Escut del CB Grup Barna", "Escudo del CB Grup Barna", "CB Grup Barna crest"),
    ("CB Grup Barna · inici", "CB Grup Barna · inicio", "CB Grup Barna · home"),
    ("Fil d'Ariadna", "Ruta de navegación", "Breadcrumb"),
    ("Vull jugar al Barna", "Quiero jugar en el Barna", "I want to play for Barna"),
    ("Bàsquet femení", "Baloncesto femenino", "Women's basketball"),
    ("Dades oficials", "Datos oficiales", "Official data"),
    ("Instal·lacions", "Instalaciones", "Facilities"),
    ("Calendari", "Calendario", "Calendar"),
    ("Cistella Petita", "Cistella Petita", "Cistella Petita"),
    ("Barna Màgics", "Barna Màgics", "Barna Màgics"),
    ("Torneig 3x3", "Torneo 3x3", "3x3 tournament"),
    ("Tota la temporada", "Toda la temporada", "The whole season"),
    ("Organigrama", "Organigrama", "Who's who"),
    ("Els equips", "Los equipos", "The teams"),
    ("La jornada", "La jornada", "The round"),
    ("Bústia de suggeriments", "Buzón de sugerencias", "Suggestions box"),
    ("Accessibilitat", "Accesibilidad", "Accessibility"),
    ("Avís legal", "Aviso legal", "Legal notice"),
    ("Per equip", "Por equipo", "By team"),
    ("Temporada", "Temporada", "Season"),
    ("El Barna", "El Barna", "El Barna"),
    ("Empreses", "Empresas", "Businesses"),
    ("Contacte", "Contacto", "Contact"),
    ("Escoleta", "Escoleta", "Escoleta"),
    ("Partners", "Partners", "Partners"),
    ("Galetes", "Cookies", "Cookies"),
    ("Galeria", "Galería", "Gallery"),
    ("Premsa", "Prensa", "Press"),
    ("Màgics", "Màgics", "Màgics"),
    ("Xarxes", "Redes", "Social"),
    ("Campus", "Campus", "Camp"),
    ("Inici", "Inicio", "Home"),
    ("Legal", "Legal", "Legal"),
    ("Club", "Club", "Club"),
]

# Cadenes que viuen dins del JavaScript.
JS = [
    ("Sense resultat", "Sin resultado", "No result"),
    ("anàlisi viuen a l", "análisis viven en l", "analysis live at l"),
]

# Els tres llistats del JavaScript, tal com son a l'original: dies comencant en
# diumenge (l'ordre de Date.getDay()), dies curts i mesos sencers.
DIES_CA = "['Diumenge', 'Dilluns', 'Dimarts', 'Dimecres', 'Dijous', 'Divendres', 'Dissabte']"
CURT_CA = "['dg.', 'dl.', 'dt.', 'dc.', 'dj.', 'dv.', 'ds.']"
MESOS_CA = ("['gener', 'febrer', 'març', 'abril', 'maig', 'juny',\n"
            "               'juliol', 'agost', 'setembre', 'octubre', 'novembre', 'desembre']")

DIES = {
    "es": "['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']",
    "en": "['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']",
}
CURT = {
    "es": "['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb']",
    "en": "['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']",
}
# Trossos del JavaScript que construeixen dates i comptadors. Cal-hi tocar
# perque si no queden connectors en catala enmig d'una frase traduida
# («Fin de semana del 5 i 6 de septiembre · 7 partits»).
JS_DATES = [
    ("' partits.';",
     "' partidos.';",
     "' fixtures.';"),
    ("'Cap de setmana del '",
     "'Fin de semana del '",
     "'Weekend of '"),
    ("da.getDate() + ' i ' + db.getDate() + ' de ' + MESOS[db.getMonth()]",
     "da.getDate() + ' y ' + db.getDate() + ' de ' + MESOS[db.getMonth()]",
     "da.getDate() + ' and ' + db.getDate() + ' ' + MESOS[db.getMonth()]"),
    ("da.getDate() + ' de ' + MESOS[da.getMonth()] + ' i ' + db.getDate() + ' de ' + MESOS[db.getMonth()]",
     "da.getDate() + ' de ' + MESOS[da.getMonth()] + ' y ' + db.getDate() + ' de ' + MESOS[db.getMonth()]",
     "da.getDate() + ' ' + MESOS[da.getMonth()] + ' and ' + db.getDate() + ' ' + MESOS[db.getMonth()]"),
    ("DIES[d.getDay()] + ' ' + d.getDate() + ' de ' + MESOS[d.getMonth()]",
     "DIES[d.getDay()] + ' ' + d.getDate() + ' de ' + MESOS[d.getMonth()]",
     "DIES[d.getDay()] + ' ' + d.getDate() + ' ' + MESOS[d.getMonth()]"),
]

MESOS = {
    "es": ("['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',\n"
           "               'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']"),
    "en": ("['January', 'February', 'March', 'April', 'May', 'June',\n"
           "               'July', 'August', 'September', 'October', 'November', 'December']"),
}

# Dades estructurades. La FAQ i el WebPage son text estatic —queden FORA dels
# marcadors SEO-*, comprovat—, aixi que es poden traduir aqui sense que el
# generador de la instantania SEO els trepitgi.
LD = [
    ("Calendari · CB Grup Barna",
     "Calendario · CB Grup Barna",
     "Calendar · CB Grup Barna"),
    ("Calendari global de tots els equips del CB Grup Barna, partits del cap de setmana i resultats de la jornada anterior.",
     "Calendario global de todos los equipos del CB Grup Barna, partidos del fin de semana y resultados de la jornada anterior.",
     "Full calendar for every CB Grup Barna team, this weekend's fixtures and last round's results."),
    ("Quan juga el CB Grup Barna aquest cap de setmana?",
     "¿Cuándo juega el CB Grup Barna este fin de semana?",
     "When does CB Grup Barna play this weekend?"),
    ("On juga els seus partits el CB Grup Barna?",
     "¿Dónde juega sus partidos el CB Grup Barna?",
     "Where does CB Grup Barna play its home games?"),
    ("On es pot veure el resultat d'un partit del CB Grup Barna?",
     "¿Dónde se puede ver el resultado de un partido del CB Grup Barna?",
     "Where can I see the result of a CB Grup Barna game?"),
    ("Quins equips té el CB Grup Barna?",
     "¿Qué equipos tiene el CB Grup Barna?",
     "What teams does CB Grup Barna have?"),
    ("El calendari complet de tots els equips del CB Grup Barna (cadet, infantil, júnior i sènior, femení i masculí) s'actualitza cada dia a partir del calendari oficial de la Federació Catalana de Basquetbol",
     "El calendario completo de todos los equipos del CB Grup Barna (cadete, infantil, júnior y sénior, femenino y masculino) se actualiza cada día a partir del calendario oficial de la Federación Catalana de Baloncesto",
     "The full calendar for every CB Grup Barna team (cadet, infantil, junior and senior, women's and men's) is updated daily from the official Catalan Basketball Federation calendar"),
    ("La majoria de partits de casa del CB Grup Barna es juguen a la Nau del Clot i al Pavelló del Parc del Clot, al barri del Clot, Districte de Sant Martí de Barcelona.",
     "La mayoría de partidos de casa del CB Grup Barna se juegan en la Nau del Clot y en el Pabellón del Parc del Clot, en el barrio del Clot, Distrito de Sant Martí de Barcelona.",
     "Most CB Grup Barna home games are played at La Nau del Clot and the Parc del Clot sports hall, in the Clot neighbourhood, Sant Martí district of Barcelona."),
    ("El pavelló exacte de cada partit apareix al calendari de",
     "El pabellón exacto de cada partido aparece en el calendario de",
     "The exact venue for each game appears in the calendar at"),
    ("Els resultats de tots els equips del CB Grup Barna es publiquen a",
     "Los resultados de todos los equipos del CB Grup Barna se publican en",
     "Results for every CB Grup Barna team are published at"),
    (", a l'apartat de resultats del cap de setmana anterior, i a la pàgina de cada equip.",
     ", en el apartado de resultados del fin de semana anterior, y en la página de cada equipo.",
     ", under last weekend's results, and on each team's own page."),
    ("El CB Grup Barna té equips federats en categories Cadet, Infantil, Júnior i Sènior, tant femenins com masculins,",
     "El CB Grup Barna tiene equipos federados en categorías Cadete, Infantil, Júnior y Sénior, tanto femeninos como masculinos,",
     "CB Grup Barna has federated teams in the Cadet, Infantil, Junior and Senior age groups, both women's and men's,"),
    ("i es pot consultar a", "y se puede consultar en", "and can be seen at"),
    (", amb els partits del cap de setmana, els resultats de la jornada anterior i el calendari global de la temporada.",
     ", con los partidos del fin de semana, los resultados de la jornada anterior y el calendario global de la temporada.",
     ", with this weekend's fixtures, last round's results and the full season calendar."),
]

# Les paraules clau del <meta name="keywords">. Es reescriuen senceres perque
# son una llista, no una frase: traduir-les tros a tros deixava una barreja
# dels tres idiomes dins de la mateixa etiqueta.
KEYWORDS = {
    "es": ("partidos CB Grup Barna, resultados Grup Barna, calendario baloncesto Clot, "
           "baloncesto Barcelona, La Nau del Clot, dias de partido"),
    "en": ("CB Grup Barna fixtures, Grup Barna results, basketball calendar Clot, "
           "basketball Barcelona, La Nau del Clot, match days"),
}

META = {
    "es": ("Días de partido del CB Grup Barna: calendario y resultados de todos los equipos "
           "federados, actualizado cada día desde la Federación Catalana de Baloncesto."),
    "en": ("CB Grup Barna match days: fixtures and results for every federated team, "
           "updated daily from the Catalan Basketball Federation."),
}


def _substitueix(html, taules, idx):
    """Substitueix en dues passades, amb marques intermedies.

    Fer-ho directament tenia un error: una regla curta es menjava el resultat
    d'una de llarga que ja s'havia aplicat. «Calendari global de tots els
    equips» passava a «Calendario global de todos los equipos», i tot seguit la
    regla «Calendari» → «Calendario» hi tornava a picar a dins i deixava
    «Calendarioo global». Amb marques, cada tros original es toca una vegada i
    prou: primer s'amaga darrere un @@n@@ i despres es revela ja traduit.

    Les taules entren TOTES A LA VEGADA, a proposit. Quan cada taula es
    passava per separat, l'ordre per llargada nomes valia dins de la seva, i
    una frase curta de TEXTOS es menjava el principi d'una de llarga de LD:
    «Calendari global de tots els equips» es traduia sol i deixava la resta
    de la frase del JSON-LD —«…del CB Grup Barna, partits del cap de setmana
    i resultats de la jornada anterior»— en catala per sempre, perque la
    regla llarga ja no hi trobava el seu text sencer. Amb una sola passada,
    la regla mes llarga sempre guanya, vingui de la taula que vingui.
    """
    files = [f for taula in taules for f in taula if f[0]]
    ordre = sorted(range(len(files)), key=lambda i: -len(files[i][0]))
    marca = {}
    for i in ordre:
        original = files[i][0]
        if original not in html:
            continue
        clau = f"@@T{i}@@"
        html = html.replace(original, clau)
        marca[clau] = files[i][idx]
    for clau, valor in marca.items():
        html = html.replace(clau, valor)
    return html


def tradueix(html, idx, lang):
    # El JavaScript de dates es comprova ABANS de tocar res: si l'original ha
    # canviat, val mes aturar-se que publicar una pagina amb mitja frase en
    # catala enmig d'una de traduida.
    for fila in JS_DATES:
        if fila[0] not in html:
            sys.exit(f"No trobo aquest tros de JavaScript:\n  {fila[0][:70]}")

    html = _substitueix(html, (TEXTOS, JS, JS_DATES, LD), idx)

    # Llistes de dies i mesos del JavaScript, substituides senceres.
    for vell, nou in ((DIES_CA, DIES[lang]), (CURT_CA, CURT[lang]), (MESOS_CA, MESOS[lang])):
        if vell not in html:
            sys.exit(f"No trobo aquest llistat a la pagina catalana:\n  {vell[:60]}...\n"
                     "Si l'han canviat, cal actualitzar-lo tambe aqui.")
        html = html.replace(vell, nou)

    # Les adreces de dins del JSON-LD han d'apuntar a la pagina d'aquest idioma.
    html = html.replace("cbgrupbarna.info/partits/", f"cbgrupbarna.info/{lang}/partits/")

    # Idioma del document i de les dades estructurades.
    html = html.replace('<html lang="ca">', f'<html lang="{lang}">')
    # inLanguage, en totes les formes que hi ha a la pagina: al JSON-LD compacte
    # hi diu "ca" sense espai, al de sota "ca" o "ca-ES" amb espai. Buscar-ne
    # nomes una deixava l'altra en catala dins d'una pagina en angles.
    # Es respecta la forma que hi hagi a l'original: "ca" surt "es"/"en" i
    # "ca-ES" surt "es-ES"/"en-GB". Aixi no s'hi inventa una regio que la
    # pagina catalana no declarava.
    REGIO = {"es": "es-ES", "en": "en-GB"}
    html = re.sub(
        r'("inLanguage":\s*")ca(-ES)?(")',
        lambda m: m.group(1) + (REGIO[lang] if m.group(2) else lang) + m.group(3),
        html)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  lambda m: m.group(1) + META[lang] + m.group(2), html)
    html = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
                  lambda m: m.group(1) + META[lang] + m.group(2), html)
    html = re.sub(r'(<meta name="keywords" content=")[^"]*(")',
                  lambda m: m.group(1) + KEYWORDS[lang] + m.group(2), html)
    html = html.replace('content="ca_ES"', f'content="{lang}_ES"' if lang == "es"
                        else 'content="en_GB"')

    # data.json es relatiu a l'original: des de /es/ i /en/ ha de ser absolut.
    html = html.replace("'data.json'", "'/partits/data.json'")
    html = html.replace('"data.json"', '"/partits/data.json"')

    # Enllaços interns cap a la versio de l'idioma, nomes on existeix. El
    # selector d'idioma es queda tal qual: els seus tres enllaços ja apunten,
    # a proposit, a les tres versions.
    mapa = _mapa_traduccions()
    switch = re.search(r'(?s)<nav class="lang-switch"[^>]*>.*?</nav>', html)
    if switch:
        html = html.replace(switch.group(0), "@@LANGSWITCH@@", 1)

    def _enllac(m):
        adreca = m.group(1)
        base, _, ancora = adreca.partition("#")
        base = base or "/"
        desti = mapa.get(base, {}).get(lang)
        if not desti:
            return m.group(0)
        return 'href="' + desti + ("#" + ancora if ancora else "") + '"'

    html = re.sub(r'href="(/[^"]*)"', _enllac, html)

    if switch:
        nou = switch.group(0)
        nou = nou.replace(' class="active" aria-current="true"', '')
        nou = re.sub(r'(<a href="[^"]*" hreflang="' + lang + r'"[^>]*?)>',
                     r'\1 class="active" aria-current="true">', nou, count=1)
        html = html.replace("@@LANGSWITCH@@", nou, 1)
    # El canonical i les alternates es reescriuen SENCERS al final, perque les
    # substitucions d'adreces d'abans se'ls emportaven per davant: el hreflang
    # del catala acabava apuntant a /es/partits/.
    html = re.sub(r'<link rel="canonical"[^>]*>',
                  f'<link rel="canonical" href="https://cbgrupbarna.info/{lang}/partits/"/>',
                  html, count=1)
    ALT = ('<link rel="alternate" hreflang="ca" href="https://cbgrupbarna.info/partits/">\n'
           '<link rel="alternate" hreflang="es" href="https://cbgrupbarna.info/es/partits/">\n'
           '<link rel="alternate" hreflang="en" href="https://cbgrupbarna.info/en/partits/">\n'
           '<link rel="alternate" hreflang="x-default" href="https://cbgrupbarna.info/partits/">')
    html = re.sub(r'<link rel="alternate" hreflang="ca"[^>]*>\s*'
                  r'<link rel="alternate" hreflang="es"[^>]*>\s*'
                  r'<link rel="alternate" hreflang="en"[^>]*>\s*'
                  r'<link rel="alternate" hreflang="x-default"[^>]*>',
                  ALT, html, count=1)
    return html


# Paraules que, si surten al text que llegeix una persona, volen dir que una
# frase s'ha quedat a mitges. No hi son totes les del catala: hi son les que no
# es poden confondre amb un nom propi ni amb castella ni angles. FEMENÍ i
# MASCULÍ no hi son a proposit: formen part dels noms oficials d'equip de la
# FCBQ i no es tradueixen mai.
# Es comproven amb limit de paraula, que si no el castella hi pica sol: dins
# de «el calendario oficial» hi ha «el calendari», i «la jornada anterior»
# s'escriu igual en catala i en castella. Per aixo la llista nomes te trossos
# que no existeixen en cap dels altres dos idiomes.
RESTES = [
    "cap de setmana", "dies de partit", "s'actualitza", "Cal activar",
    "Encara no", "aquí sota", "els partits", "el calendari", "Torna-ho",
    "tots els equips", "hi ha partits", "resultats", "sortiran",
]


def _comprova(html, lang):
    """Avisa si ha quedat catala al text que es veu.

    Les etiquetes, el JavaScript i els comentaris no compten: alli el catala
    hi pot ser i no el llegeix ningu. El que no pot passar es que una frase
    quedi mig traduida —«…and can be seen at cbgrupbarna.info/en/partits/, amb
    els partits del cap de setmana…»—, que es exactament el que passava quan
    una regla curta es menjava el principi d'una de llarga.
    """
    visible = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html)
    visible = re.sub(r"(?s)<!--.*?-->", " ", visible)
    # Els atributs que si que llegeix algu: alt, title, aria-label i les meta.
    llegible = " ".join(re.findall(r'(?:alt|title|aria-label|content)="([^"]*)"', visible))
    visible = re.sub(r"(?s)<[^>]+>", " ", visible) + " " + llegible
    trobats = sorted({t for t in RESTES
                      if re.search(r"\b" + re.escape(t) + r"\b", visible, re.I)})
    if trobats:
        sys.exit(f"Ha quedat catala a la versio «{lang}»: {', '.join(trobats)}\n"
                 "Segurament una regla curta s'ha menjat el principi d'una de llarga.\n"
                 "Afegeix la frase sencera a TEXTOS o a LD i torna-ho a provar.")


def main():
    dry = "--dry-run" in sys.argv
    if not FONT.is_file():
        sys.exit(f"No trobo {FONT}.")
    base = FONT.read_text(encoding="utf-8")

    for lang, idx in (("es", 1), ("en", 2)):
        desti = ROOT / lang / "partits" / "index.html"
        nou = tradueix(base, idx, lang)
        _comprova(nou, lang)
        anterior = desti.read_text(encoding="utf-8") if desti.is_file() else ""
        if nou == anterior:
            print(f"  sense canvis: {desti.relative_to(ROOT)}")
        elif dry:
            print(f"  escriuria:    {desti.relative_to(ROOT)}  "
                  f"({len(anterior):,} → {len(nou):,} bytes)")
        else:
            desti.parent.mkdir(parents=True, exist_ok=True)
            desti.write_text(nou, encoding="utf-8")
            print(f"  escrit:       {desti.relative_to(ROOT)}  "
                  f"({len(anterior):,} → {len(nou):,} bytes)")
    if dry:
        print("--dry-run: no he escrit res.")


if __name__ == "__main__":
    main()
