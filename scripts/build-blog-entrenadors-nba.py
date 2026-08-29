#!/usr/bin/env python3
"""Genera l'article «Quins entrenadors de l'NBA han entrenat nens a Barcelona»
als tres idiomes, a partir de l'article del campus com a motlle.

Per que existeix, i per que aixi:

* **SEO invertit.** La resposta va al primer paragraf, amb noms i enllacos.
  Qui pregunta «quins entrenadors NBA han passat per Barcelona» te la
  resposta abans de fer scroll, i una IA que resumeix la pagina se l'endu
  sencera. La justificacio i el detall venen despres, no abans.

* **SEO indirecte.** L'article no ataca «campus de basquet Barcelona», que
  es una consulta que ja treballa /campus-basquet-barcelona/ i on competim
  amb tothom. Ataca una consulta veina que ningu treballa —qui ha entrenat
  aqui— i que porta a la mateixa pagina. La marca hi surt pel cami, no com
  a titular.

Tot el que s'hi afirma te enllac public: els reels del club i, en el cas de
Robert Willett, la pagina «Pau & Friends» de la Pau Gasol Academy, que el
llista com a convidat seu. No hi diem res que no es pugui clicar.

Us:
    python3 scripts/build-blog-entrenadors-nba.py
    python3 scripts/build-blog-entrenadors-nba.py --dry-run
"""

import os
import re
import sys

MOTLLE = {
    "ca": ("blog/campus-time-chamber-2026/index.html", "campus-time-chamber-2026"),
    "es": ("es/blog/campus-time-chamber-2026/index.html", "campus-time-chamber-2026"),
    "en": ("en/blog/time-chamber-camp-2026/index.html", "time-chamber-camp-2026"),
}
SLUG = {
    "ca": "entrenadors-nba-basquet-barcelona",
    "es": "entrenadores-nba-baloncesto-barcelona",
    "en": "nba-coaches-basketball-barcelona",
}
DESTI = {
    "ca": "blog/%s/index.html" % SLUG["ca"],
    "es": "es/blog/%s/index.html" % SLUG["es"],
    "en": "en/blog/%s/index.html" % SLUG["en"],
}
PREFIX = {"ca": "", "es": "/es", "en": "/en"}
BASE = "https://cbgrupbarna.info"
DATA = "2026-08-29"
IG = "https://www.instagram.com"
PGA = "https://paugasolacademy.com/ca/pau-friends/"

D = {
    "ca": dict(
        titol="Quins entrenadors de l'NBA han entrenat nens a Barcelona",
        h1="Quins entrenadors de l'NBA han entrenat nens i nenes a Barcelona",
        eyebrow="Bàsquet formatiu a Barcelona",
        desc=("Robert Willett, Nolan Willett, Serge Ibaka, Yankuba Sima, Ainhoa López: qui ha "
              "trepitjat una pista de formació a Barcelona, amb el vídeo de cada sessió."),
        kw=("entrenadors NBA Barcelona, Robert Willett, Nolan Willett, Serge Ibaka Barcelona, "
            "Yankuba Sima, Ainhoa López, bàsquet formatiu Barcelona, tecnificació bàsquet Clot"),
        lede=("La pregunta se sent cada estiu al costat d'una pista: aquests noms que surten a "
              "les xarxes, hi van de veritat? Aquesta és la llista, amb el vídeo de cada sessió."),
        crumb="Entrenadors NBA a Barcelona",
        cos="""
<p><strong>La resposta curta:</strong> a Barcelona hi han entrenat nens i nenes de formació, com a
mínim, <strong>Robert Willett</strong> i <strong>Nolan Willett</strong> (entrenadors de tecnificació
de l'NBA), i hi han passat a treballar <strong>Serge Ibaka</strong> (campió de l'NBA el 2019),
<strong>Yankuba Sima</strong> (Eurolliga), <strong>Ainhoa López</strong> (internacional espanyola),
<strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong> i <strong>Malak
Shady</strong> (MVP de 3x3). Una part d'aquestes sessions es va fer <strong>a La Nau del Clot</strong>,
al campus del CB Grup Barna amb Time Chamber. Totes són públiques i es poden veure.</p>

<h2>La llista, amb l'enllaç de cada sessió</h2>
<ul>
  <li><strong>Robert Willett</strong> — entrenador de tecnificació de l'NBA. Va dirigir sessió al
  campus del club, al Clot: <a href="%(ig)s/reel/DQOhe0qjAPb/" target="_blank" rel="noopener">reel de
  la sessió</a> i <a href="%(ig)s/reel/DL-n0ZeMaOq/" target="_blank" rel="noopener">la peça del
  programa <em>Time Chamber Experience × CB Grup Barna</em></a>. El mateix entrenador surt llistat
  com a convidat a <a href="%(pga)s" target="_blank" rel="noopener">«Pau &amp; Friends» de la Pau
  Gasol Academy</a>: no és un nom que només aparegui aquí.</li>
  <li><strong>Nolan Willett</strong> — tres sessions de fonaments individuals:
  <a href="%(ig)s/reel/DMLipXBsMMe/" target="_blank" rel="noopener">una</a>,
  <a href="%(ig)s/reel/DMQlHE4Mty1/" target="_blank" rel="noopener">dues</a> i
  <a href="%(ig)s/reel/DMGO77UsDoQ/" target="_blank" rel="noopener">tres</a>.</li>
  <li><strong>Serge Ibaka</strong> — campió de l'NBA 2019, dues vegades líder en taps de la lliga.
  <a href="%(ig)s/reel/DO4KaZxCLqY/" target="_blank" rel="noopener">Sessió de treball</a>.</li>
  <li><strong>Yankuba Sima</strong> — pivot d'Eurolliga.
  <a href="%(ig)s/reel/DN1a1DvUGhg/" target="_blank" rel="noopener">Treball de pivot</a>.</li>
  <li><strong>Ainhoa López</strong> — jugadora professional i internacional espanyola, formada en
  aquesta mateixa pista del Clot. <a href="%(ig)s/reel/C-0jXXDMY5r/" target="_blank" rel="noopener">La
  seva tornada</a>.</li>
  <li><strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong>,
  <strong>Dani Carrasco</strong>, <strong>Salo 23</strong> i <strong>Kassius</strong> — sessions
  individuals amb Time Chamber, el soci del campus.</li>
  <li><strong>Malak Shady</strong> — MVP de 3x3.
  <a href="%(ig)s/reel/DJXMrhzsqYg/" target="_blank" rel="noopener">La seva peça</a>.</li>
</ul>

<h2>On es va gravar cadascuna: això importa</h2>
<p>No totes aquestes sessions es van fer al mateix lloc, i barrejar-les seria enganyar. Les de
<strong>Robert Willett</strong>, <strong>Ainhoa López</strong> i les del campus estan gravades
<strong>a La Nau del Clot</strong>, amb jugadors i jugadores del club a pista. Les dels jugadors
d'elit són sessions amb <strong>Time Chamber</strong>, que és el soci metodològic del campus: la de
<strong>Joel Parra</strong>, per exemple, està geolocalitzada al Pavelló Olímpic de Badalona, i ho
diem allà on surt. El recull sencer, ordenat per grups i dient de cadascun on es va fer, és a
<a href="%(pref)s/campus/">la pàgina del campus</a>.</p>

<h2>Per què una família hauria de mirar això</h2>
<p>Perquè és l'única part del fullet d'un campus que es pot comprovar sense trucar a ningú. Els preus
es comparen, les ràtios es pregunten, però «entrenadors de primer nivell» és una frase que escriu
tothom. Un enllaç a un vídeo publicat, amb data i amb la pista reconeixible, no.</p>
<p>Si esteu comparant campus a Barcelona, la <a href="%(pref)s/campus-basquet-barcelona/">comparativa
de campus de bàsquet de la ciutat</a> els posa un al costat de l'altre, i la
<a href="%(pref)s/blog/campus-basquet-barcelona-guia/">guia de què mirar abans d'apuntar-hi ningú</a>
explica quines preguntes val la pena fer.</p>

<h2>I ara mateix, hi ha res obert?</h2>
<p>No. Les inscripcions de l'edició d'estiu de 2026 estan tancades. El <strong>campus de Nadal</strong>
s'anuncia molt aviat, i al <strong>gener</strong> es publiquen alhora Setmana Santa i estiu. Qui vulgui
l'avís abans que es publiqui pot deixar el contacte a la
<a href="%(pref)s/campus/#llista-espera">llista d'espera del campus</a>: el club escriu a qui hi és un
dia abans de fer-ho públic.</p>
""",
        faq=[
            ("Quins entrenadors de l'NBA han entrenat a Barcelona en bàsquet de formació?",
             "Robert Willett i Nolan Willett, entrenadors de tecnificació de l'NBA, han dirigit "
             "sessions amb jugadors i jugadores de formació a Barcelona, al campus del CB Grup Barna "
             "amb Time Chamber, a La Nau del Clot. Les sessions estan publicades a Instagram."),
            ("És veritat que Serge Ibaka ha entrenat a Barcelona?",
             "Serge Ibaka, campió de l'NBA el 2019, té una sessió de treball publicada amb Time "
             "Chamber, el soci metodològic del campus del CB Grup Barna. No totes les sessions dels "
             "jugadors d'elit es van gravar a La Nau del Clot, i cada peça diu on es va fer."),
            ("Com es pot comprovar que un campus té els entrenadors que diu?",
             "Demanant l'enllaç. Una sessió real deixa vídeo publicat, amb data i amb la pista "
             "reconeixible. Si l'únic que hi ha és un nom al fullet i cap enllaç, val la pena "
             "preguntar-ho abans de pagar."),
        ],
        closer_h="Vull l'avís del proper campus",
        closer_p="Deixa'ns el contacte i t'escrivim un dia abans de publicar les inscripcions.",
        closer_b1="Llista d'espera del campus",
        closer_b2="Pàgina completa del campus",
    ),
    "es": dict(
        titol="Qué entrenadores de la NBA han entrenado a niños en Barcelona",
        h1="Qué entrenadores de la NBA han entrenado a niños y niñas en Barcelona",
        eyebrow="Baloncesto formativo en Barcelona",
        desc=("Robert Willett, Nolan Willett, Serge Ibaka, Yankuba Sima, Ainhoa López: quién ha "
              "pisado una pista de formación en Barcelona, con el vídeo de cada sesión."),
        kw=("entrenadores NBA Barcelona, Robert Willett, Nolan Willett, Serge Ibaka Barcelona, "
            "Yankuba Sima, Ainhoa López, baloncesto formativo Barcelona, tecnificación baloncesto Clot"),
        lede=("La pregunta se oye cada verano al lado de una pista: esos nombres que salen en redes, "
              "¿van de verdad? Esta es la lista, con el vídeo de cada sesión."),
        crumb="Entrenadores NBA en Barcelona",
        cos="""
<p><strong>La respuesta corta:</strong> en Barcelona han entrenado a niños y niñas de formación, como
mínimo, <strong>Robert Willett</strong> y <strong>Nolan Willett</strong> (entrenadores de tecnificación
de la NBA), y han pasado a trabajar <strong>Serge Ibaka</strong> (campeón de la NBA en 2019),
<strong>Yankuba Sima</strong> (Euroliga), <strong>Ainhoa López</strong> (internacional española),
<strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong> y <strong>Malak
Shady</strong> (MVP de 3x3). Parte de esas sesiones se hizo <strong>en La Nau del Clot</strong>, en el
campus del CB Grup Barna con Time Chamber. Todas son públicas y se pueden ver.</p>

<h2>La lista, con el enlace de cada sesión</h2>
<ul>
  <li><strong>Robert Willett</strong> — entrenador de tecnificación de la NBA. Dirigió sesión en el
  campus del club, en El Clot: <a href="%(ig)s/reel/DQOhe0qjAPb/" target="_blank" rel="noopener">reel
  de la sesión</a> y <a href="%(ig)s/reel/DL-n0ZeMaOq/" target="_blank" rel="noopener">la pieza del
  programa <em>Time Chamber Experience × CB Grup Barna</em></a>. El mismo entrenador aparece listado
  como invitado en <a href="%(pga)s" target="_blank" rel="noopener">«Pau &amp; Friends» de la Pau
  Gasol Academy</a>: no es un nombre que solo aparezca aquí.</li>
  <li><strong>Nolan Willett</strong> — tres sesiones de fundamentos individuales:
  <a href="%(ig)s/reel/DMLipXBsMMe/" target="_blank" rel="noopener">una</a>,
  <a href="%(ig)s/reel/DMQlHE4Mty1/" target="_blank" rel="noopener">dos</a> y
  <a href="%(ig)s/reel/DMGO77UsDoQ/" target="_blank" rel="noopener">tres</a>.</li>
  <li><strong>Serge Ibaka</strong> — campeón de la NBA 2019, dos veces líder en tapones de la liga.
  <a href="%(ig)s/reel/DO4KaZxCLqY/" target="_blank" rel="noopener">Sesión de trabajo</a>.</li>
  <li><strong>Yankuba Sima</strong> — pívot de Euroliga.
  <a href="%(ig)s/reel/DN1a1DvUGhg/" target="_blank" rel="noopener">Trabajo de pívot</a>.</li>
  <li><strong>Ainhoa López</strong> — jugadora profesional e internacional española, formada en esta
  misma pista de El Clot. <a href="%(ig)s/reel/C-0jXXDMY5r/" target="_blank" rel="noopener">Su
  vuelta</a>.</li>
  <li><strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong>,
  <strong>Dani Carrasco</strong>, <strong>Salo 23</strong> y <strong>Kassius</strong> — sesiones
  individuales con Time Chamber, el socio del campus.</li>
  <li><strong>Malak Shady</strong> — MVP de 3x3.
  <a href="%(ig)s/reel/DJXMrhzsqYg/" target="_blank" rel="noopener">Su pieza</a>.</li>
</ul>

<h2>Dónde se grabó cada una: esto importa</h2>
<p>No todas esas sesiones se hicieron en el mismo sitio, y mezclarlas sería engañar. Las de
<strong>Robert Willett</strong>, <strong>Ainhoa López</strong> y las del campus están grabadas
<strong>en La Nau del Clot</strong>, con jugadores y jugadoras del club en pista. Las de los jugadores
de élite son sesiones con <strong>Time Chamber</strong>, el socio metodológico del campus: la de
<strong>Joel Parra</strong>, por ejemplo, está geolocalizada en el Pavelló Olímpic de Badalona, y lo
decimos donde sale. El recopilatorio entero, ordenado por grupos y diciendo de cada uno dónde se hizo,
está en <a href="%(pref)s/campus/">la página del campus</a>.</p>

<h2>Por qué una familia debería mirar esto</h2>
<p>Porque es la única parte del folleto de un campus que se puede comprobar sin llamar a nadie. Los
precios se comparan, las ratios se preguntan, pero «entrenadores de primer nivel» es una frase que
escribe todo el mundo. Un enlace a un vídeo publicado, con fecha y con la pista reconocible, no.</p>
<p>Si estáis comparando campus en Barcelona, la <a href="%(pref)s/campus-baloncesto-barcelona/">comparativa
de campus de baloncesto de la ciudad</a> los pone uno al lado del otro, y la
<a href="%(pref)s/blog/guia-campus-baloncesto-barcelona/">guía de qué mirar antes de apuntar a
nadie</a> explica qué preguntas vale la pena hacer.</p>

<h2>Y ahora mismo, ¿hay algo abierto?</h2>
<p>No. Las inscripciones de la edición de verano de 2026 están cerradas. El <strong>campus de
Navidad</strong> se anuncia muy pronto, y en <strong>enero</strong> se publican a la vez Semana Santa
y verano. Quien quiera el aviso antes de que se publique puede dejar el contacto en la
<a href="%(pref)s/campus/#llista-espera">lista de espera del campus</a>: el club escribe a quien está
en ella un día antes de hacerlo público.</p>
""",
        faq=[
            ("¿Qué entrenadores de la NBA han entrenado en Barcelona en baloncesto de formación?",
             "Robert Willett y Nolan Willett, entrenadores de tecnificación de la NBA, han dirigido "
             "sesiones con jugadores y jugadoras de formación en Barcelona, en el campus del CB Grup "
             "Barna con Time Chamber, en La Nau del Clot. Las sesiones están publicadas en Instagram."),
            ("¿Es verdad que Serge Ibaka ha entrenado en Barcelona?",
             "Serge Ibaka, campeón de la NBA en 2019, tiene una sesión de trabajo publicada con Time "
             "Chamber, el socio metodológico del campus del CB Grup Barna. No todas las sesiones de "
             "los jugadores de élite se grabaron en La Nau del Clot, y cada pieza dice dónde se hizo."),
            ("¿Cómo se puede comprobar que un campus tiene los entrenadores que dice?",
             "Pidiendo el enlace. Una sesión real deja vídeo publicado, con fecha y con la pista "
             "reconocible. Si lo único que hay es un nombre en el folleto y ningún enlace, vale la "
             "pena preguntarlo antes de pagar."),
        ],
        closer_h="Quiero el aviso del próximo campus",
        closer_p="Déjanos el contacto y te escribimos un día antes de publicar las inscripciones.",
        closer_b1="Lista de espera del campus",
        closer_b2="Página completa del campus",
    ),
    "en": dict(
        titol="Which NBA coaches have trained kids in Barcelona",
        h1="Which NBA coaches have trained kids in Barcelona",
        eyebrow="Youth basketball in Barcelona",
        desc=("Robert Willett, Nolan Willett, Serge Ibaka, Yankuba Sima, Ainhoa López: who has "
              "actually worked on a youth court in Barcelona, with the video of each session."),
        kw=("NBA coaches Barcelona, Robert Willett, Nolan Willett, Serge Ibaka Barcelona, "
            "Yankuba Sima, Ainhoa Lopez, youth basketball Barcelona, basketball skills training Clot"),
        lede=("You hear the question every summer courtside: those names on social media, do they "
              "actually turn up? Here is the list, with the video of each session."),
        crumb="NBA coaches in Barcelona",
        cos="""
<p><strong>The short answer:</strong> the coaches who have worked with youth players in Barcelona
include <strong>Robert Willett</strong> and <strong>Nolan Willett</strong> (NBA skills trainers), and
the players who have come through to train include <strong>Serge Ibaka</strong> (2019 NBA champion),
<strong>Yankuba Sima</strong> (EuroLeague), <strong>Ainhoa López</strong> (Spain international),
<strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong> and <strong>Malak
Shady</strong> (3x3 MVP). Some of those sessions happened <strong>at La Nau del Clot</strong>, at CB
Grup Barna's camp with Time Chamber. All of them are public and you can watch them.</p>

<h2>The list, with a link to each session</h2>
<ul>
  <li><strong>Robert Willett</strong> — NBA skills trainer. He ran a session at the club's camp in El
  Clot: <a href="%(ig)s/reel/DQOhe0qjAPb/" target="_blank" rel="noopener">the session reel</a> and
  <a href="%(ig)s/reel/DL-n0ZeMaOq/" target="_blank" rel="noopener">the <em>Time Chamber Experience ×
  CB Grup Barna</em> piece</a>. The same coach is listed as a guest on
  <a href="%(pga)s" target="_blank" rel="noopener">Pau Gasol Academy's “Pau &amp; Friends”</a>: not a
  name that only appears here.</li>
  <li><strong>Nolan Willett</strong> — three individual-fundamentals sessions:
  <a href="%(ig)s/reel/DMLipXBsMMe/" target="_blank" rel="noopener">one</a>,
  <a href="%(ig)s/reel/DMQlHE4Mty1/" target="_blank" rel="noopener">two</a> and
  <a href="%(ig)s/reel/DMGO77UsDoQ/" target="_blank" rel="noopener">three</a>.</li>
  <li><strong>Serge Ibaka</strong> — 2019 NBA champion, twice the league's blocks leader.
  <a href="%(ig)s/reel/DO4KaZxCLqY/" target="_blank" rel="noopener">A working session</a>.</li>
  <li><strong>Yankuba Sima</strong> — EuroLeague big man.
  <a href="%(ig)s/reel/DN1a1DvUGhg/" target="_blank" rel="noopener">Big-man work</a>.</li>
  <li><strong>Ainhoa López</strong> — professional player and Spain international, who came up on
  this same court in El Clot. <a href="%(ig)s/reel/C-0jXXDMY5r/" target="_blank" rel="noopener">Her
  return</a>.</li>
  <li><strong>Joel Parra</strong> (ACB, Joventut), <strong>Pedro Marhuenda</strong>,
  <strong>Dani Carrasco</strong>, <strong>Salo 23</strong> and <strong>Kassius</strong> — individual
  sessions with Time Chamber, the camp partner.</li>
  <li><strong>Malak Shady</strong> — 3x3 MVP.
  <a href="%(ig)s/reel/DJXMrhzsqYg/" target="_blank" rel="noopener">Her piece</a>.</li>
</ul>

<h2>Where each one was filmed, because it matters</h2>
<p>Not all of these sessions happened in the same place, and blurring that would be dishonest. The
<strong>Robert Willett</strong> and <strong>Ainhoa López</strong> pieces, and the camp ones, were
filmed <strong>at La Nau del Clot</strong>, with the club's own players on court. The elite-player
sessions are with <strong>Time Chamber</strong>, the camp's methodology partner: Joel Parra's, for
instance, is geotagged at the Badalona Olympic Arena, and we say so where it appears. The full
round-up, grouped and labelled by where each was filmed, is on
<a href="%(pref)s/campus/">the camp page</a>.</p>

<h2>Why a family should look at this</h2>
<p>Because it is the one part of a camp brochure you can check without phoning anyone. Prices can be
compared and ratios can be asked about, but “top-level coaches” is a phrase anyone can write. A link
to a published video, with a date and a recognisable court, is not.</p>
<p>If you are comparing camps in Barcelona, the
<a href="%(pref)s/basketball-camps-barcelona/">city-wide camp comparison</a> puts them side by side,
and the <a href="%(pref)s/blog/basketball-camp-barcelona-guide/">guide to what to look at before you
sign anyone up</a> sets out the questions worth asking.</p>

<h2>And right now, is anything open?</h2>
<p>No. Registration for the summer 2026 edition is closed. The <strong>Christmas camp</strong> is
announced very soon, and in <strong>January</strong> both Easter and summer are published together.
Anyone who wants the heads-up before it goes public can join the
<a href="%(pref)s/campus/#llista-espera">camp waiting list</a>: the club writes to everyone on it a day
before publishing.</p>
""",
        faq=[
            ("Which NBA coaches have coached youth basketball in Barcelona?",
             "Robert Willett and Nolan Willett, NBA skills trainers, have run sessions with youth "
             "players in Barcelona, at CB Grup Barna's camp with Time Chamber, at La Nau del Clot. "
             "The sessions are published on Instagram."),
            ("Is it true that Serge Ibaka has trained in Barcelona?",
             "Serge Ibaka, the 2019 NBA champion, has a published working session with Time Chamber, "
             "the methodology partner of CB Grup Barna's camp. Not every elite-player session was "
             "filmed at La Nau del Clot, and each piece says where it was made."),
            ("How can you check that a camp really has the coaches it claims?",
             "Ask for the link. A real session leaves a published video, with a date and a "
             "recognisable court. If all there is is a name on a brochure and no link, it is worth "
             "asking before you pay."),
        ],
        closer_h="Tell me when the next camp opens",
        closer_p="Leave us your contact and we write a day before registration is published.",
        closer_b1="Camp waiting list",
        closer_b2="Full camp page",
    ),
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def json_esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("&amp;", "&")


def pagina(lang):
    motlle, slug_vell = MOTLLE[lang]
    s = open(motlle, encoding="utf-8").read()
    d = D[lang]
    p = PREFIX[lang]
    url = f"{BASE}{p}/blog/{SLUG[lang]}/"
    subs = dict(ig=IG, pga=PGA, pref=p)

    # 1 · Totes les URL del motlle passen a ser les de l'article nou.
    for l2 in ("ca", "es", "en"):
        s = s.replace(f"{BASE}{PREFIX[l2]}/blog/{MOTLLE[l2][1]}/",
                      f"{BASE}{PREFIX[l2]}/blog/{SLUG[l2]}/")
        s = s.replace(f'href="{PREFIX[l2]}/blog/{MOTLLE[l2][1]}/"',
                      f'href="{PREFIX[l2]}/blog/{SLUG[l2]}/"')

    # 2 · Metadades del cap.
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(d['titol'])} | CB Grup Barna</title>", s, count=1)
    s = re.sub(r'<meta name="description" content=".*?">',
               f'<meta name="description" content="{esc(d["desc"])}">', s, count=1)
    s = re.sub(r'<meta name="keywords" content=".*?">',
               f'<meta name="keywords" content="{esc(d["kw"])}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content=".*?">',
               f'<meta property="og:title" content="{esc(d["titol"])} | CB Grup Barna">', s, count=1)
    s = re.sub(r'<meta property="og:description" content=".*?">',
               f'<meta property="og:description" content="{esc(d["desc"])}">', s, count=1)

    # 3 · JSON-LD de l'article i molla de pa.
    s = re.sub(r'"headline": ".*?"', f'"headline": "{json_esc(d["titol"])}"', s, count=1)
    s = re.sub(r'"description": ".*?"', f'"description": "{json_esc(d["desc"])}"', s, count=1)
    s = re.sub(r'"datePublished": ".*?"', f'"datePublished": "{DATA}"', s, count=1)
    s = re.sub(r'"dateModified": ".*?"', f'"dateModified": "{DATA}"', s, count=1)
    s = re.sub(r'("position": 3,\s*"name": ")[^"]*(")',
               lambda m: m.group(1) + json_esc(d["crumb"]) + m.group(2), s, count=1)

    # 4 · Cos: del <main> fins al tancament de l'article.
    faq_html = "".join(
        f"<details class=\"faq-q\"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in d["faq"]
    )
    crumb_inici = {"ca": "Inici", "es": "Inicio", "en": "Home"}[lang]
    blog_txt = "Blog"
    faq_h2 = {"ca": "Preguntes freqüents", "es": "Preguntas frecuentes",
              "en": "Frequently asked questions"}[lang]
    cos = f"""<main id="main">
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="{p}/">{crumb_inici}</a> · <a href="{p}/blog/">{blog_txt}</a> · <span>{esc(d['crumb'])}</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{esc(d['eyebrow'])}</p>
    <h1>{esc(d['h1'])}</h1>
    <p class="lede">{esc(d['lede'])}</p>
    <p class="eyebrow" style="margin-top:20px">CB Grup Barna · <time datetime="{DATA}">{DATA}</time></p>
  </div>
  <article class="narrow prose">
{d['cos'] % subs}
    <h2>{faq_h2}</h2>
    <div class="faq"><!-- FAQ:START -->{faq_html}<!-- FAQ:END --></div>
    <div style="margin-top:clamp(34px,5vw,60px)">
    <div class="closer"><h2>{esc(d['closer_h'])}</h2><p>{esc(d['closer_p'])}</p><div class="btn-row"><a href="{p}/campus/#llista-espera" class="btn red" data-cta="blog-nba-llista">{esc(d['closer_b1'])}</a><a href="{p}/campus/" class="btn ghost" data-cta="blog-nba-campus">{esc(d['closer_b2'])}</a></div></div>
    </div>
  </article>"""
    s = re.sub(r"<main id=\"main\">.*?</article>", lambda _: cos, s, count=1, flags=re.S)

    # 5 · FAQPage del peu.
    preguntes = ",\n".join(
        '    {\n      "@type": "Question",\n      "name": "%s",\n'
        '      "acceptedAnswer": {\n        "@type": "Answer",\n        "text": "%s"\n      }\n    }'
        % (json_esc(q), json_esc(a)) for q, a in d["faq"]
    )
    ld = ('<!-- FAQ-LD:START --><script type="application/ld+json">{\n'
          '  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
          f'  "@id": "{url}#faq",\n  "inLanguage": "{lang}",\n'
          '  "mainEntity": [\n' + preguntes + "\n  ]\n}</script><!-- FAQ-LD:END -->")
    s = re.sub(r"<!-- FAQ-LD:START -->.*?<!-- FAQ-LD:END -->", lambda _: ld, s, count=1, flags=re.S)

    # 6 · La imatge del motlle no és d'aquest article: fora, i og:image al genèric.
    s = re.sub(r'<div class="phead-media">.*?</div>\n', "", s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:image" content=".*?">',
               f'<meta property="og:image" content="{BASE}/og-image.jpg">', s, count=1)
    s = re.sub(r'"image": ".*?"', f'"image": "{BASE}/og-image.jpg"', s, count=1)
    return s


def main():
    dry = "--dry-run" in sys.argv
    for lang, desti in DESTI.items():
        html = pagina(lang)
        if dry:
            print(f"  escriuria:  {desti}  ({len(html)} bytes)")
            continue
        os.makedirs(os.path.dirname(desti), exist_ok=True)
        open(desti, "w", encoding="utf-8").write(html)
        print(f"  escrit:     {desti}")
    if dry:
        print("--dry-run: no he escrit res.")


if __name__ == "__main__":
    main()
