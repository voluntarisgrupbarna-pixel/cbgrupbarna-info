#!/usr/bin/env python3
"""Genera el bloc «Estrelles del campus» a /campus/, /es/campus/ i /en/campus/.

Per que existeix: el bloc vivia escrit a ma tres vegades i les tres versions
s'havien separat. El catala en tenia tres peces, i el dossier intern «Qui
entrena a La Nau» en documenta setze que no eren enlloc del web. Amb una sola
taula de dades, els tres idiomes no es poden tornar a desincronitzar.

Nomes reescriu el tros entre els marcadors ESTRELLES-CAMPUS. Fora d'aqui no
toca res, aixi que es segur executar-lo encara que la pagina hagi canviat.

Honestedat, que aqui es el que importa: cada peca diu on es va gravar. Les del
grup «a La Nau» son al pavello del club; les altres son sessions amb Time
Chamber, el soci del campus, i no s'hi val a insinuar el contrari. La de Joel
Parra esta geolocalitzada al Pavello Olimpic de Badalona i ho diu.

Us:
    python3 scripts/build-campus-estrelles.py
    python3 scripts/build-campus-estrelles.py --dry-run
"""

import os
import re
import sys

INICI = "<!-- ESTRELLES-CAMPUS:inici · generat per scripts/build-campus-estrelles.py -->"
FINAL = "<!-- ESTRELLES-CAMPUS:final -->"

IG = "https://www.instagram.com"

# (codi, tipus, nom, rol_ca, rol_es, rol_en, text_ca, text_es, text_en, handle)
# tipus: "reel" o "p" (publicacio de feed) — decideix la URL de l'incrustat.
NAU = [
    ("Dbn8AMsIebZ", "reel", "El resum de l'edició", "El resumen de la edición", "The season recap",
     "Reel final del campus", "Reel final del campus", "Camp closing reel",
     "Com va acabar el Campus Timechamber: totes les setmanes en un vídeo.",
     "Cómo acabó el Campus Timechamber: todas las semanas en un vídeo.",
     "How the Timechamber Camp ended: every week in one video.", None),
    ("Datex2OxHcS", "reel", "Shooting Academy", "Shooting Academy", "Shooting Academy",
     "Setmana 3 del campus", "Semana 3 del campus", "Camp week 3",
     "La setmana dedicada al tir, de dins de la pista.",
     "La semana dedicada al tiro, desde dentro de la pista.",
     "The week devoted to shooting, from the court.", None),
    ("DL-n0ZeMaOq", "reel", "Robert Willett", "Robert Willett", "Robert Willett",
     "Entrenador NBA · al campus", "Entrenador NBA · en el campus", "NBA coach · at the camp",
     "Dirigint sessió al campus del club.",
     "Dirigiendo sesión en el campus del club.",
     "Running a session at the club's camp.", "bballwillett"),
    ("DQOhe0qjAPb", "reel", "Robert Willett", "Robert Willett", "Robert Willett",
     "Entrenador NBA · al campus", "Entrenador NBA · en el campus", "NBA coach · at the camp",
     "Segona sessió, un altre bloc de treball.",
     "Segunda sesión, otro bloque de trabajo.",
     "A second session, a different block of work.", "bballwillett"),
    ("C-0jXXDMY5r", "reel", "Ainhoa López", "Ainhoa López", "Ainhoa López",
     "Selecció Espanyola · formada al Clot", "Selección Española · formada en El Clot",
     "Spanish national team · trained at El Clot",
     "Jugadora professional. Va sortir d'aquesta pista i hi ha tornat a entrenar.",
     "Jugadora profesional. Salió de esta pista y ha vuelto a entrenar en ella.",
     "A professional player. She came up on this court and has come back to train on it.",
     "ainhoalopez_official"),
    ("DMcpUFgst4L", "p", "Ainhoa López", "Ainhoa López", "Ainhoa López",
     "Segona peça · publicació de feed", "Segunda pieza · publicación de feed",
     "Second piece · feed post",
     "La segona publicació de la seva visita, la que el club va fer servir a la web del campus.",
     "La segunda publicación de su visita, la que el club usó en la web del campus.",
     "The second post from her visit, the one used on the camp site.",
     "ainhoalopez_official"),
    ("DJXMrhzsqYg", "reel", "Malak Shady", "Malak Shady", "Malak Shady",
     "MVP de 3x3", "MVP de 3x3", "3x3 MVP",
     "Referent del bàsquet a xarxes i MVP de 3x3.",
     "Referente del baloncesto en redes y MVP de 3x3.",
     "A basketball voice online and a 3x3 MVP.", "malakshady_22"),
    ("DFiwKWIMz2q", "reel", "Malak Shady", "Malak Shady", "Malak Shady",
     "MVP de 3x3 · segona peça", "MVP de 3x3 · segunda pieza", "3x3 MVP · second piece",
     "La segona peça seva que el club va publicar a la web del campus.",
     "La segunda pieza suya que el club publicó en la web del campus.",
     "The second piece of hers the club published on the camp site.", "malakshady_22"),
]

COACHES = [
    ("DMLipXBsMMe", "reel", "Nolan Willett", "Nolan Willett", "Nolan Willett",
     "Entrenador NBA", "Entrenador NBA", "NBA coach",
     "Treball de fonaments individuals amb Time Chamber.",
     "Trabajo de fundamentos individuales con Time Chamber.",
     "Individual fundamentals work with Time Chamber.", "nolanwillett3"),
    ("DMQlHE4Mty1", "reel", "Nolan Willett", "Nolan Willett", "Nolan Willett",
     "Entrenador NBA", "Entrenador NBA", "NBA coach",
     "Segona sessió: lectura de joc i resolució a prop de cistella.",
     "Segunda sesión: lectura de juego y resolución cerca del aro.",
     "A second session: reading the game and finishing near the rim.", "nolanwillett3"),
    ("DMGO77UsDoQ", "reel", "Nolan Willett", "Nolan Willett", "Nolan Willett",
     "Entrenador NBA", "Entrenador NBA", "NBA coach",
     "Tercera sessió del bloc de tecnificació.",
     "Tercera sesión del bloque de tecnificación.",
     "A third session in the skills block.", "nolanwillett3"),
    ("DMqb9P8sUic", "reel", "Robert Willett", "Robert Willett", "Robert Willett",
     "Entrenador NBA", "Entrenador NBA", "NBA coach",
     "Una de les dues peces seves que encapçalaven la web del campus 2026.",
     "Una de las dos piezas suyas que encabezaban la web del campus 2026.",
     "One of the two pieces of his that headed the 2026 camp site.", "bballwillett"),
    ("DL0UkAfMJsI", "reel", "Robert Willett", "Robert Willett", "Robert Willett",
     "Entrenador NBA", "Entrenador NBA", "NBA coach",
     "La segona, també publicada a la web del campus 2026.",
     "La segunda, también publicada en la web del campus 2026.",
     "The second, also published on the 2026 camp site.", "bballwillett"),
]

ELIT = [
    ("DO4KaZxCLqY", "reel", "Serge Ibaka", "Serge Ibaka", "Serge Ibaka",
     "Campió NBA 2019", "Campeón NBA 2019", "2019 NBA champion",
     "Sessió de treball amb Time Chamber.",
     "Sesión de trabajo con Time Chamber.",
     "A working session with Time Chamber.", "timechamber_es"),
    ("DN1a1DvUGhg", "reel", "Yankuba Sima", "Yankuba Sima", "Yankuba Sima",
     "Eurolliga", "Euroliga", "EuroLeague",
     "Treball de pivot amb Time Chamber.",
     "Trabajo de pívot con Time Chamber.",
     "Big-man work with Time Chamber.", "yankubasima"),
    ("DL25XRsskTS", "reel", "Pedro Marhuenda", "Pedro Marhuenda", "Pedro Marhuenda",
     "Jugador professional", "Jugador profesional", "Professional player",
     "Sessió individual amb Time Chamber.",
     "Sesión individual con Time Chamber.",
     "An individual session with Time Chamber.", "4future_pedromarhuenda"),
    ("DOHTiwWiKJE", "reel", "Dani Carrasco", "Dani Carrasco", "Dani Carrasco",
     "Jugador professional", "Jugador profesional", "Professional player",
     "Sessió de treball amb Time Chamber.",
     "Sesión de trabajo con Time Chamber.",
     "A working session with Time Chamber.", "timechamber_es"),
    ("DOrQsPRiD_l", "reel", "Salo 23", "Salo 23", "Salo 23",
     "Jugador", "Jugador", "Player",
     "Sessió de tecnificació amb Time Chamber.",
     "Sesión de tecnificación con Time Chamber.",
     "A skills session with Time Chamber.", "salo23_"),
    ("DN5x42hCDpV", "reel", "Kassius", "Kassius", "Kassius",
     "Jugador", "Jugador", "Player",
     "Sessió de tecnificació amb Time Chamber.",
     "Sesión de tecnificación con Time Chamber.",
     "A skills session with Time Chamber.", "kassius_r"),
    ("CguvYo9KuTz", "p", "Joel Parra", "Joel Parra", "Joel Parra",
     "ACB · Joventut", "ACB · Joventut", "ACB · Joventut",
     "Sessió amb Time Chamber al Pavelló Olímpic de Badalona, no a La Nau.",
     "Sesión con Time Chamber en el Pavelló Olímpic de Badalona, no en La Nau.",
     "A session with Time Chamber at the Badalona Olympic Arena, not at La Nau.", "joelparra"),
]

# El graella de #campustimechamber i @cbgrupbarna de la web del campus 2026
# (timechamber.skywork.website). No hi diem on es va gravar cada peça perquè
# la font no ho diu: diem d'on surt, que sí que ho sabem.
RECULL = [
    ("DLA0wKxsM2c", "reel", "La Nau del Clot", "La Nau del Clot", "La Nau del Clot",
     "El pavelló, en vídeo", "El pabellón, en vídeo", "The venue, on video",
     "El reel de la seu que la web del campus feia servir per ensenyar la pista.",
     "El reel de la sede que la web del campus usaba para enseñar la pista.",
     "The venue reel the camp site used to show the court.", None),
    ("DWrubLpDIU0", "reel", "Del campus", "Del campus", "From the camp",
     "Recull #campustimechamber", "Recopilatorio #campustimechamber",
     "#campustimechamber round-up",
     "Peça de la graella de la web del campus 2026.",
     "Pieza de la parrilla de la web del campus 2026.",
     "A piece from the 2026 camp site grid.", None),
    ("DSk2otLiDVo", "reel", "Del campus", "Del campus", "From the camp",
     "Recull #campustimechamber", "Recopilatorio #campustimechamber",
     "#campustimechamber round-up",
     "Peça de la graella de la web del campus 2026.",
     "Pieza de la parrilla de la web del campus 2026.",
     "A piece from the 2026 camp site grid.", None),
    ("DNjFQX1Mm1X", "reel", "Del campus", "Del campus", "From the camp",
     "Publicat a @cbgrupbarna", "Publicado en @cbgrupbarna", "Posted on @cbgrupbarna",
     "Peça del perfil del club dins la graella de la web del campus.",
     "Pieza del perfil del club dentro de la parrilla de la web del campus.",
     "A club-profile piece from the camp site grid.", None),
    ("DW2Iuj-jKwB", "p", "Del campus", "Del campus", "From the camp",
     "Publicació de feed", "Publicación de feed", "Feed post",
     "Publicació de la graella de la web del campus 2026.",
     "Publicación de la parrilla de la web del campus 2026.",
     "A post from the 2026 camp site grid.", None),
    ("DIb0HSfMud_", "p", "Del campus", "Del campus", "From the camp",
     "Publicació de feed", "Publicación de feed", "Feed post",
     "Publicació de la graella de la web del campus 2026.",
     "Publicación de la parrilla de la web del campus 2026.",
     "A post from the 2026 camp site grid.", None),
]

CONVOS = [
    ("DXKxd7VjCJK", "Campus d'estiu · La Nau del Clot", "Campus de verano · La Nau del Clot",
     "Summer camp · La Nau del Clot",
     "Convocatòria del 16 d'abril", "Convocatoria del 16 de abril", "Announced 16 April"),
    ("DUtmAbHjFIs", "Flow Camp · Setmana Santa", "Flow Camp · Semana Santa", "Flow Camp · Easter",
     "Del 30 de març al 3 d'abril", "Del 30 de marzo al 3 de abril", "30 March to 3 April"),
    ("DUT5hyjDD7S", "Campus de Carnaval", "Campus de Carnaval", "Carnival camp",
     "Convocatòria del 3 de febrer", "Convocatoria del 3 de febrero", "Announced 3 February"),
    ("DQ7nLmkjINq", "Edició Limitada 2025", "Edición Limitada 2025", "Limited Edition 2025",
     "Convocatòria de l'11 de novembre de 2025", "Convocatoria del 11 de noviembre de 2025",
     "Announced 11 November 2025"),
]

T = {
    "ca": dict(
        i=2, h2="Estrelles del campus",
        lede=("Una cosa que no fa tothom: al campus hi han passat referents del bàsquet a entrenar amb "
              "els nostres jugadors i jugadores. No de visita per a la foto — a pista, dirigint sessió. "
              "Ho separem en tres grups perquè no tot es va gravar al mateix lloc: primer el que va passar "
              "<strong>a La Nau del Clot</strong>, després la feina dels entrenadors i dels jugadors d'elit "
              "<strong>amb Time Chamber</strong>, que és el nostre soci del campus."),
        g1="A La Nau del Clot",
        g1p="Gravat al pavelló del club, amb els nostres jugadors i jugadores a pista.",
        g2="Entrenadors NBA amb Time Chamber",
        g2p="La metodologia de treball individual que el campus incorpora ve d'aquí.",
        g3="Jugadors d'elit que hi han entrenat",
        g3p=("Sessions amb Time Chamber, el soci del campus. No totes es van gravar a La Nau: quan no hi "
             "va ser, ho diem."),
        g5="El recull de la web del campus",
        g5p=("Les peces que la web del campus 2026 tenia a la graella de <strong>#campustimechamber</strong> i de <strong>@cbgrupbarna</strong>. Són aquí perquè no es perdin quan aquella web deixi d'existir."),
        g4="Les convocatòries publicades",
        g4p=('Cada edició del campus s\'anuncia amb <a href="%s/timechamber_es/" target="_blank" '
             'rel="noopener">@timechamber_es</a>. Aquestes són les quatre darreres.' % IG),
        play="Reproduir el vídeo amb", veure="Veure a Instagram →",
        peu=('Els vídeos són d\'Instagram i es carreguen a mesura que baixes, no tots de cop. Tot el recull de l\'edició '
             'és a <a href="%s/cbgrupbarna/" target="_blank" rel="noopener">@cbgrupbarna</a>.' % IG),
    ),
    "es": dict(
        i=3, h2="Estrellas del campus",
        lede=("Algo que no hace todo el mundo: por el campus han pasado referentes del baloncesto a "
              "entrenar con nuestros jugadores y jugadoras. No de visita para la foto — en pista, "
              "dirigiendo sesión. Lo separamos en tres grupos porque no todo se grabó en el mismo sitio: "
              "primero lo que pasó <strong>en La Nau del Clot</strong>, después el trabajo de los "
              "entrenadores y de los jugadores de élite <strong>con Time Chamber</strong>, que es nuestro "
              "socio del campus."),
        g1="En La Nau del Clot",
        g1p="Grabado en el pabellón del club, con nuestros jugadores y jugadoras en pista.",
        g2="Entrenadores NBA con Time Chamber",
        g2p="La metodología de trabajo individual que el campus incorpora viene de aquí.",
        g3="Jugadores de élite que han entrenado",
        g3p=("Sesiones con Time Chamber, el socio del campus. No todas se grabaron en La Nau: cuando no "
             "fue así, lo decimos."),
        g5="El recopilatorio de la web del campus",
        g5p=("Las piezas que la web del campus 2026 tenía en la parrilla de <strong>#campustimechamber</strong> y de <strong>@cbgrupbarna</strong>. Están aquí para que no se pierdan cuando aquella web deje de existir."),
        g4="Las convocatorias publicadas",
        g4p=('Cada edición del campus se anuncia con <a href="%s/timechamber_es/" target="_blank" '
             'rel="noopener">@timechamber_es</a>. Estas son las cuatro últimas.' % IG),
        play="Reproducir el vídeo con", veure="Ver en Instagram →",
        peu=('Los vídeos son de Instagram y se cargan a medida que bajas, no todos de golpe. Todo el recopilatorio de la '
             'edición está en <a href="%s/cbgrupbarna/" target="_blank" rel="noopener">@cbgrupbarna</a>.' % IG),
    ),
    "en": dict(
        i=4, h2="Camp guests",
        lede=("Something not every club can say: players and coaches at the top of the game have come to "
              "the camp to train with our kids. Not a photo visit — on court, running the session. We "
              "split them into three groups because not everything was filmed in the same place: first "
              "what happened <strong>at La Nau del Clot</strong>, then the work by coaches and elite "
              "players <strong>with Time Chamber</strong>, our camp partner."),
        g1="At La Nau del Clot",
        g1p="Filmed at the club's own court, with our players on it.",
        g2="NBA coaches with Time Chamber",
        g2p="The individual-work method the camp is built on comes from here.",
        g3="Elite players who have trained there",
        g3p=("Sessions with Time Chamber, the camp partner. Not all of them were filmed at La Nau — where "
             "they weren't, we say so."),
        g5="The camp site round-up",
        g5p=("The pieces the 2026 camp site carried in its <strong>#campustimechamber</strong> and <strong>@cbgrupbarna</strong> grids. They live here so they don't vanish with that site."),
        g4="The camps we've announced",
        g4p=('Every edition is announced with <a href="%s/timechamber_es/" target="_blank" '
             'rel="noopener">@timechamber_es</a>. These are the last four.' % IG),
        play="Play the video with", veure="View on Instagram →",
        peu=('The videos are hosted on Instagram and load as you scroll, not all at once. The full set for each edition '
             'is on <a href="%s/cbgrupbarna/" target="_blank" rel="noopener">@cbgrupbarna</a>.' % IG),
    ),
}

PLAY_SVG = ('<em><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">'
            '<path d="M8 5v14l11-7z"/></svg></em>')


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def targeta(fila, t):
    codi, tipus, *resta = fila
    i = t["i"]
    nom, rol, text, handle = resta[i - 2], resta[i + 1], resta[i + 4], resta[-1]
    kind = ' data-kind="p"' if tipus == "p" else ""
    enllac = f"{IG}/{handle}/" if handle else f"{IG}/cbgrupbarna/"
    etiqueta = f"@{handle} →" if handle else t["veure"]
    return f"""        <div class="star">
          <button type="button" class="star-play" data-reel="{codi}"{kind} aria-label="{esc(t['play'])} {esc(nom)}">
            {PLAY_SVG}
            <span>{esc(nom)}</span>
          </button>
          <div class="star-tx">
            <h4>{esc(nom)}</h4>
            <span class="role">{esc(rol)}</span>
            <p>{esc(text)}</p>
            <a href="{enllac}" target="_blank" rel="noopener">{esc(etiqueta)}</a>
          </div>
        </div>"""


def grup(titol, intro, files, t):
    cards = "\n".join(targeta(f, t) for f in files)
    return f"""    <div class="stars-group">
      <h3>{esc(titol)}</h3>
      <p>{intro}</p>
      <div class="stars">
{cards}
      </div>
    </div>
"""


def bloc(lang):
    t = T[lang]
    i = t["i"]
    convos = "\n".join(
        f'        <a href="{IG}/p/{c[0]}/" target="_blank" rel="noopener">\n'
        f'          <b>{esc(c[i - 1])}</b><span>{esc(c[i + 2])}</span></a>'
        for c in CONVOS
    )
    return f"""{INICI}
    <h2>{esc(t['h2'])}</h2>
    <p>{t['lede']}</p>

{grup(t['g1'], esc(t['g1p']), NAU, t)}
{grup(t['g2'], esc(t['g2p']), COACHES, t)}
{grup(t['g3'], esc(t['g3p']), ELIT, t)}
{grup(t['g5'], t['g5p'], RECULL, t)}
    <div class="stars-group">
      <h3>{esc(t['g4'])}</h3>
      <p>{t['g4p']}</p>
      <div class="convos">
{convos}
      </div>
    </div>

    <p style="font-size:13.5px;color:var(--ink-2);margin-top:clamp(22px,3vw,32px)">{t['peu']}</p>
    {FINAL}"""


FITXERS = {"ca": "campus/index.html", "es": "es/campus/index.html", "en": "en/campus/index.html"}


def main():
    dry = "--dry-run" in sys.argv
    for lang, cami in FITXERS.items():
        if not os.path.isfile(cami):
            sys.exit(f"No trobo {cami}. Executa'm des de l'arrel del repositori.")
        text = open(cami, encoding="utf-8").read()
        if INICI not in text or FINAL not in text:
            sys.exit(
                f"{cami} no te els marcadors ESTRELLES-CAMPUS. Posa'ls-hi a ma un cop "
                "i despres ja es podra regenerar sol."
            )
        nou = re.sub(
            re.escape(INICI) + r".*?" + re.escape(FINAL),
            lambda _: bloc(lang),
            text,
            flags=re.S,
        )
        peces = len(NAU) + len(COACHES) + len(ELIT) + len(RECULL)
        if nou == text:
            print(f"  sense canvis: {cami}")
        elif dry:
            print(f"  canviaria:    {cami}  ({peces} vídeos + {len(CONVOS)} convocatòries)")
        else:
            open(cami, "w", encoding="utf-8").write(nou)
            print(f"  escrit:       {cami}  ({peces} vídeos + {len(CONVOS)} convocatòries)")
    if dry:
        print("--dry-run: no he escrit res.")


if __name__ == "__main__":
    main()
