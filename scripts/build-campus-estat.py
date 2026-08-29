#!/usr/bin/env python3
"""Genera dos blocs de /campus/ als tres idiomes.

1. ESTAT-CAMPUS  · l'avis d'inscripcions tancades i el calendari d'anuncis
   (Nadal aviat, gener Setmana Santa i estiu), amb l'enllac a la web de
   l'edicio 2026 i el boto cap a la llista d'espera.

2. ARXIU-CAMPUS  · tot el que deia la web de l'edicio 2026
   (timechamber.skywork.website), ordenat i traduit: xifres, preus amb el
   codi de descompte, serveis, la seu amb el mapa, els hashtags i el
   formulari de llista d'espera que la substitueix.

Per que existeix: aquella web es d'un tercer i pot desapareixer. El que hi
deia ha de viure al web del club, en catala, castella i angles alhora, i
sense que ningu hagi d'escriure tres vegades el mateix.

Els preus i el codi de descompte son els DE L'EDICIO 2026 i aqui es diuen
com el que son: historics, no una oferta oberta. Les inscripcions estan
tancades i el bloc ho diu a dalt de tot.

Us:
    python3 scripts/build-campus-estat.py
    python3 scripts/build-campus-estat.py --dry-run
"""

import os
import re
import sys

E_INICI = "<!-- ESTAT-CAMPUS:inici · generat per scripts/build-campus-estat.py -->"
E_FINAL = "<!-- ESTAT-CAMPUS:final -->"
D_INICI = "<!-- DIFERENCIA-CAMPUS:inici · generat per scripts/build-campus-estat.py -->"
D_FINAL = "<!-- DIFERENCIA-CAMPUS:final -->"
A_INICI = "<!-- ARXIU-CAMPUS:inici · generat per scripts/build-campus-estat.py -->"
A_FINAL = "<!-- ARXIU-CAMPUS:final -->"

WEB2026 = "https://timechamber.skywork.website/"
WA = "https://wa.me/34698425153"
IG = "https://www.instagram.com"
MAPA = ("https://maps.google.com/?q=La+Nau+del+Clot+Carrer+de+la+Llacuna+172+Barcelona")

# Videos de la instal.lacio. Tots tres estan gravats a La Nau del Clot: el
# primer es el reel que la web del campus 2026 feia servir a «LA SEDE», i els
# altres dos son del campus mateix, a la pista del club.
VIDEOS_SEU = [
    ("DLA0wKxsM2c", "reel",
     "La Nau del Clot", "La Nau del Clot", "La Nau del Clot",
     "El pavello, en video", "El pabellon, en video", "The venue, on video"),
    ("Dbn8AMsIebZ", "reel",
     "El campus, de dins", "El campus, por dentro", "Inside the camp",
     "Totes les setmanes a la pista", "Todas las semanas en la pista",
     "Every week on the court"),
    ("Datex2OxHcS", "reel",
     "Shooting Academy", "Shooting Academy", "Shooting Academy",
     "Una setmana, a la mateixa pista", "Una semana, en la misma pista",
     "One week, on the same court"),
]

# Les sis setmanes tal com les anomenava la web de l'edicio 2026.
SETMANES = [
    ("01", "23–27", "FLOW CAMP",
     "Fluïdesa ofensiva i joc en moviment.",
     "Fluidez ofensiva y juego en movimiento.",
     "Attacking flow and playing on the move."),
    ("02", "30–4", "TIMECHAMBER BASICS",
     "Fonaments sòlids per a un joc d'elit.",
     "Fundamentos sólidos para un juego de élite.",
     "Solid fundamentals for an elite game."),
    ("03", "7–11", "SHOOTING ACADEMY",
     "Mecànica, ritme i confiança de tir.",
     "Mecánica, ritmo y confianza de tiro.",
     "Shooting mechanics, rhythm and confidence."),
    ("04", "14–18", "ONE ON ONE MASTERY",
     "Dominar l'1x1. Fintes i creativitat ofensiva.",
     "Dominar el 1x1. Fintas y creatividad ofensiva.",
     "Owning the 1-on-1. Fakes and attacking creativity."),
    ("05", "21–25", "BALLHANDLING LAB",
     "Control de pilota al màxim nivell.",
     "Control de balón al máximo nivel.",
     "Ball control at the highest level."),
    ("06", "28–1", "SKILLS LAB EXPERIENCE",
     "Integració total. El colofó de l'edició.",
     "Integración total. El broche de oro.",
     "Everything together. The closing week."),
]

T = {
    "ca": dict(
        lang="ca",
        seu_vid_h="La Nau, en vídeo",
        seu_vid_p="Tres peces gravades a la pista del club: la instal·lació abans de res, i el campus fent-la servir. Es carreguen soles quan hi arribes.",
        dif_h="Per què en un club, i no en un espai llogat",
        dif=[
            ("Un campus dins d'un club, no en una pista de pas",
             "El campus es fa a <strong>La Nau del Clot</strong>, que és la instal·lació del club, no un espai llogat per a l'ocasió. Els grans campus de la ciutat treballen en seus alquilades i canvien de pista segons l'any; nosaltres entrenem tot l'any al mateix lloc, amb els mateixos entrenadors i el mateix escut a la paret."),
            ("La tecnificació que no torna a cap equip es perd",
             "Una setmana intensiva millora el tir o el bot d'un jugador. Si el setembre torna a un lloc on ningú sap què hi va treballar, allò s'esvaeix. Aquí, els entrenadors del campus i els de temporada són la mateixa gent i parlen entre ells: el que es treballa al juliol continua a l'octubre."),
            ("Fem seguiment, també durant el campus",
             "Els jugadors i jugadores del club no deixen de tenir seguiment perquè sigui estiu: el que es veu al campus entra a la seva fitxa i arriba al seu entrenador o entrenadora de temporada."),
            ("I mirem qui ve de fora",
             "El campus és obert a qualsevol club, i per al Barna també és la millor manera de conèixer jugadors i jugadores que encara no coneixem. Qui ve de fora entrena i se'n va igual; però si hi encaixa i li interessa, la porta del club ja la coneix."),
        ],
        # ---- bloc 1: estat
        estat_tag="Inscripcions tancades",
        estat_h="Ara mateix no hi ha cap campus obert",
        estat_p=(f'Les inscripcions de l\'edició d\'estiu de 2026 estan <strong>tancades</strong>. '
                 f'La web amb què es van obrir segueix consultable: '
                 f'<a href="{WEB2026}" target="_blank" rel="noopener" data-cta="campus-web-2026">'
                 f'web del Campus Timechamber 2026 →</a>. Tot el que hi deia també és més avall '
                 f'en aquesta pàgina, perquè no depengui d\'una web que no és nostra.'),
        estat_cal_h="Què ve ara",
        estat_cal=[
            ("Molt aviat", "Campus de Nadal",
             "L'anunciem en qüestió de dies, aquí i a @cbgrupbarna."),
            ("Al gener", "Setmana Santa i estiu",
             "Publiquem les dues edicions alhora: dates, setmanes i obertura d'inscripcions."),
        ],
        estat_cta=("Si no te'l vols perdre, apunta't a la llista d'espera: "
                   "escrivim a qui hi és <strong>un dia abans</strong> de publicar-ho."),
        estat_btn="Apuntar-me a la llista d'espera",
        estat_btn2="Preguntar per WhatsApp",
        # ---- bloc 2: llista d'espera
        le_h="Llista d'espera del campus",
        le_p=("Deixa'ns el contacte i t'escrivim quan obrim inscripcions, abans de publicar-ho. "
              "Rebràs un correu de confirmació de seguida; si no arriba, mira la carpeta de brossa."),
        le_nom="Nom del jugador o jugadora",
        le_nom_err="Digues-nos com es diu.",
        le_any="Any de naixement",
        le_any_err="Posa l'any de naixement (per exemple, 2014).",
        le_tutor="El teu nom",
        le_tutor_err="Digues-nos qui ens escriu.",
        le_mail="El teu correu",
        le_mail_hint="Aquí t'enviem la confirmació i l'avís d'obertura.",
        le_mail_err="Fa falta un correu vàlid per poder-te avisar.",
        le_tel="Telèfon",
        le_tel_hint="Opcional. Només si prefereixes que t'avisem per WhatsApp.",
        le_quins="Quines edicions t'interessen",
        le_op=[("nadal", "Campus de Nadal"), ("setmana-santa", "Setmana Santa"),
               ("estiu", "Estiu")],
        le_msg="Alguna cosa que hàgim de saber",
        le_msg_hint="Opcional. Categoria, club de procedència, si ve amb algun amic…",
        le_ok="Hi entro",
        le_done_h="Ja hi ets",
        le_done_p=(f'T\'hem apuntat a la llista. Rebràs un correu de confirmació i t\'escrivim quan '
                   f'obrim inscripcions. Si tens pressa, el <a href="{WA}">WhatsApp del club</a> '
                   f'és el camí ràpid.'),
        le_rgpd=('El que escrius aquí el llegeix la direcció del club i només serveix per avisar-te '
                 'del campus. No et posem a cap altra llista. El detall és a la '
                 '<a href="/politica-de-privacitat/">política de privacitat</a>.'),
        # ---- bloc 2: arxiu
        ar_h="L'edició 2026, tal com es va publicar",
        ar_p=(f'Això és el que deia la web del <strong>Timechamber Experience 2026</strong>, '
              f'recollit aquí sencer. Serveix per saber com és el campus quan s\'obre: les xifres, '
              f'les setmanes, els preus i els serveis van ser aquests. '
              f'<strong>Les dates i els preus de la propera edició s\'anunciaran de nou</strong>.'),
        ar_claim="«El campus d'estiu de bàsquet més innovador de Barcelona.»",
        ar_dates="Del 23 de juny a l'1 d'agost · La Nau del Clot",
        xifres=[("6", "setmanes temàtiques"), ("+200", "jugadors per edició"),
                ("NBA", "metodologia d'elit"), ("100%", "satisfacció de les famílies")],
        xifres_peu=("Xifres tal com les publicava la web de l'edició 2026. El recompte propi del club "
                    "per a l'estiu de 2026 és de 150 participants al llarg de les sis setmanes; "
                    "el «+200 per edició» és la xifra de la campanya."),
        set_h="Sis setmanes, sis experiències",
        set_p="Cada setmana tenia identitat pròpia. S'hi podia anar una setmana o totes.",
        set_mes=["juny", "juny–juliol", "juliol", "juliol", "juliol", "juliol–agost"],
        preus_h="Els preus que es van publicar",
        preus_p=("Aquests van ser els preus de l'edició 2026. Els de la propera es publicaran quan "
                 "s'obrin les inscripcions."),
        preus=[("Recomanat", "Setmana completa", "195 €", "9 h a 17 h",
                ["Dinar inclòs", "Servei d'acollida"]),
               ("Alternativa", "Mitja jornada", "160 €", "9 h a 13:30 h",
                ["Mateixos grups i mateix focus setmanal"])],
        dte=("Descompte del 10% per inscripció anticipada, abans del 20 d'abril, amb el codi "
             "<b>BARNAAVIAT</b>. I reserva amb pagament en 3 terminis: un primer pagament "
             "reserva la plaça i la resta es fracciona."),
        serv_h="Els serveis",
        serv=[("Horaris", "9–13:30 h en mitja jornada · 9–17 h en jornada completa"),
              ("Acollida", "Servei d'acollida al matí"),
              ("Dinar", "Àpat de migdia inclòs a la jornada completa"),
              ("Divendres", "Excursió a Illa Fantasia")],
        seu_h="La seu",
        seu_sub="Instal·lació oficial del club",
        seu_adr="La Nau del Clot · Carrer de la Llacuna 172, 08018 Barcelona",
        seu_com="Com arribar-hi →",
        mapa_btn="Carregar el mapa de Google",
        mapa_nota=("El mapa és de Google i posa galetes: només es carrega si el demanes."),
        hash_h="Els hashtags i els comptes",
        hash_p=("La conversa del campus va per aquí. Són els comptes i les etiquetes amb què es va "
                "publicar tot el que has vist en aquesta pàgina."),
        peu=(f'La web original de l\'edició 2026 continua en línia mentre el proveïdor la mantingui: '
             f'<a href="{WEB2026}" target="_blank" rel="noopener">timechamber.skywork.website</a>. '
             f'Aquesta pàgina no en depèn.'),
    ),
    "es": dict(
        lang="es",
        seu_vid_h="La Nau, en vídeo",
        seu_vid_p="Tres piezas grabadas en la pista del club: la instalación primero, y el campus usándola. Se cargan solas cuando llegas.",
        dif_h="Por qué dentro de un club, y no en un espacio alquilado",
        dif=[
            ("Un campus dentro de un club, no en una pista de paso",
             "El campus se hace en <strong>La Nau del Clot</strong>, que es la instalación del club, no un espacio alquilado para la ocasión. Los grandes campus de la ciudad trabajan en sedes alquiladas y cambian de pista según el año; nosotros entrenamos todo el año en el mismo sitio, con los mismos entrenadores y el mismo escudo en la pared."),
            ("La tecnificación que no vuelve a ningún equipo se pierde",
             "Una semana intensiva mejora el tiro o el bote de un jugador. Si en septiembre vuelve a un sitio donde nadie sabe qué trabajó, aquello se diluye. Aquí, los entrenadores del campus y los de temporada son la misma gente y hablan entre ellos: lo que se trabaja en julio sigue en octubre."),
            ("Hacemos seguimiento, también durante el campus",
             "Los jugadores y jugadoras del club no dejan de tener seguimiento porque sea verano: lo que se ve en el campus entra en su ficha y llega a su entrenador o entrenadora de temporada."),
            ("Y miramos a quien viene de fuera",
             "El campus está abierto a cualquier club, y para el Barna es también la mejor manera de conocer a jugadores y jugadoras que aún no conocemos. Quien viene de fuera entrena y se va igual; pero si encaja y le interesa, ya sabe dónde está la puerta del club."),
        ],
        estat_tag="Inscripciones cerradas",
        estat_h="Ahora mismo no hay ningún campus abierto",
        estat_p=(f'Las inscripciones de la edición de verano de 2026 están <strong>cerradas</strong>. '
                 f'La web con la que se abrieron sigue consultable: '
                 f'<a href="{WEB2026}" target="_blank" rel="noopener" data-cta="campus-web-2026">'
                 f'web del Campus Timechamber 2026 →</a>. Todo lo que decía está también más abajo '
                 f'en esta página, para que no dependa de una web que no es nuestra.'),
        estat_cal_h="Qué viene ahora",
        estat_cal=[
            ("Muy pronto", "Campus de Navidad",
             "Lo anunciamos en cuestión de días, aquí y en @cbgrupbarna."),
            ("En enero", "Semana Santa y verano",
             "Publicamos las dos ediciones a la vez: fechas, semanas y apertura de inscripciones."),
        ],
        estat_cta=("Si no te lo quieres perder, apúntate a la lista de espera: escribimos a quien "
                   "está en ella <strong>un día antes</strong> de publicarlo."),
        estat_btn="Apuntarme a la lista de espera",
        estat_btn2="Preguntar por WhatsApp",
        le_h="Lista de espera del campus",
        le_p=("Déjanos el contacto y te escribimos cuando abramos inscripciones, antes de publicarlo. "
              "Recibirás un correo de confirmación enseguida; si no llega, mira la carpeta de spam."),
        le_nom="Nombre del jugador o jugadora",
        le_nom_err="Dinos cómo se llama.",
        le_any="Año de nacimiento",
        le_any_err="Pon el año de nacimiento (por ejemplo, 2014).",
        le_tutor="Tu nombre",
        le_tutor_err="Dinos quién nos escribe.",
        le_mail="Tu correo",
        le_mail_hint="Aquí te enviamos la confirmación y el aviso de apertura.",
        le_mail_err="Hace falta un correo válido para poder avisarte.",
        le_tel="Teléfono",
        le_tel_hint="Opcional. Solo si prefieres que te avisemos por WhatsApp.",
        le_quins="Qué ediciones te interesan",
        le_op=[("nadal", "Campus de Navidad"), ("setmana-santa", "Semana Santa"),
               ("estiu", "Verano")],
        le_msg="Algo que debamos saber",
        le_msg_hint="Opcional. Categoría, club de procedencia, si viene con algún amigo…",
        le_ok="Entro en la lista",
        le_done_h="Ya estás",
        le_done_p=(f'Te hemos apuntado a la lista. Recibirás un correo de confirmación y te escribimos '
                   f'cuando abramos inscripciones. Si tienes prisa, el '
                   f'<a href="{WA}">WhatsApp del club</a> es el camino rápido.'),
        le_rgpd=('Lo que escribes aquí lo lee la dirección del club y solo sirve para avisarte del '
                 'campus. No te metemos en ninguna otra lista. El detalle está en la '
                 '<a href="/es/politica-de-privacidad/">política de privacidad</a>.'),
        ar_h="La edición 2026, tal como se publicó",
        ar_p=(f'Esto es lo que decía la web del <strong>Timechamber Experience 2026</strong>, '
              f'recogido aquí entero. Sirve para saber cómo es el campus cuando se abre: las cifras, '
              f'las semanas, los precios y los servicios fueron estos. '
              f'<strong>Las fechas y los precios de la próxima edición se anunciarán de nuevo</strong>.'),
        ar_claim="«El campus de verano de baloncesto más innovador de Barcelona.»",
        ar_dates="Del 23 de junio al 1 de agosto · La Nau del Clot",
        xifres=[("6", "semanas temáticas"), ("+200", "jugadores por edición"),
                ("NBA", "metodología de élite"), ("100%", "satisfacción de las familias")],
        xifres_peu=("Cifras tal como las publicaba la web de la edición 2026. El recuento propio del "
                    "club para el verano de 2026 es de 150 participantes a lo largo de las seis "
                    "semanas; el «+200 por edición» es la cifra de la campaña."),
        set_h="Seis semanas, seis experiencias",
        set_p="Cada semana tenía identidad propia. Se podía ir una semana o todas.",
        set_mes=["junio", "junio–julio", "julio", "julio", "julio", "julio–agosto"],
        preus_h="Los precios que se publicaron",
        preus_p=("Estos fueron los precios de la edición 2026. Los de la próxima se publicarán cuando "
                 "se abran las inscripciones."),
        preus=[("Recomendado", "Semana completa", "195 €", "9 h a 17 h",
                ["Almuerzo incluido", "Servicio de acogida"]),
               ("Alternativa", "Media jornada", "160 €", "9 h a 13:30 h",
                ["Mismos grupos y mismo foco semanal"])],
        dte=("Descuento del 10% por inscripción anticipada, antes del 20 de abril, con el código "
             "<b>BARNAAVIAT</b>. Y reserva con pago en 3 plazos: un primer pago reserva la plaza y "
             "el resto se fracciona."),
        serv_h="Los servicios",
        serv=[("Horarios", "9–13:30 h en media jornada · 9–17 h en jornada completa"),
              ("Acogida", "Servicio de acogida por la mañana"),
              ("Almuerzo", "Comida de mediodía incluida en la jornada completa"),
              ("Viernes", "Excursión a Isla Fantasía")],
        seu_h="La sede",
        seu_sub="Instalación oficial del club",
        seu_adr="La Nau del Clot · Carrer de la Llacuna 172, 08018 Barcelona",
        seu_com="Cómo llegar →",
        mapa_btn="Cargar el mapa de Google",
        mapa_nota="El mapa es de Google y pone cookies: solo se carga si lo pides.",
        hash_h="Los hashtags y las cuentas",
        hash_p=("La conversación del campus va por aquí. Son las cuentas y las etiquetas con las que "
                "se publicó todo lo que has visto en esta página."),
        peu=(f'La web original de la edición 2026 sigue en línea mientras el proveedor la mantenga: '
             f'<a href="{WEB2026}" target="_blank" rel="noopener">timechamber.skywork.website</a>. '
             f'Esta página no depende de ella.'),
    ),
    "en": dict(
        lang="en",
        seu_vid_h="La Nau, on video",
        seu_vid_p="Three pieces filmed on the club's own court: the venue first, then the camp using it. They load by themselves as you reach them.",
        dif_h="Why inside a club, and not in a rented venue",
        dif=[
            ("A camp inside a club, not on a court passed through",
             "The camp runs at <strong>La Nau del Clot</strong>, the club's own facility, not a space hired for the occasion. The city's big camps work out of rented venues and change courts from year to year; we train there all season, with the same coaches and the same badge on the wall."),
            ("Skills work that goes back to no team gets lost",
             "An intensive week improves a player's shot or handle. If in September they go back somewhere nobody knows what they worked on, it fades. Here the camp coaches and the season coaches are the same people and they talk to each other: what is worked on in July carries into October."),
            ("We keep tracking players during the camp too",
             "Our players don't stop being followed because it is summer: what shows up at the camp goes into their record and reaches their season coach."),
            ("And we watch the ones who come from outside",
             "The camp is open to any club, and for the Barna it is also the best way to meet players we don't know yet. Someone from another club trains and goes home just the same; but if they fit and they're interested, they already know where the door is."),
        ],
        estat_tag="Registration closed",
        estat_h="No camp is open right now",
        estat_p=(f'Registration for the summer 2026 edition is <strong>closed</strong>. The site it '
                 f'opened with is still up: <a href="{WEB2026}" target="_blank" rel="noopener" '
                 f'data-cta="campus-web-2026">the 2026 Timechamber Camp site →</a>. Everything it '
                 f'said is also further down this page, so it does not depend on a site that is not '
                 f'ours.'),
        estat_cal_h="What comes next",
        estat_cal=[
            ("Very soon", "Christmas camp",
             "We announce it within days, here and on @cbgrupbarna."),
            ("In January", "Easter and summer",
             "Both editions at once: dates, weeks and when registration opens."),
        ],
        estat_cta=("If you don't want to miss it, join the waiting list: we write to everyone on it "
                   "<strong>a day before</strong> we publish."),
        estat_btn="Join the waiting list",
        estat_btn2="Ask on WhatsApp",
        le_h="Camp waiting list",
        le_p=("Leave us your contact and we will write when registration opens, before we publish it. "
              "You will get a confirmation email straight away; if it does not arrive, check your "
              "spam folder."),
        le_nom="Player's name",
        le_nom_err="Tell us their name.",
        le_any="Year of birth",
        le_any_err="Please give the year of birth (for example, 2014).",
        le_tutor="Your name",
        le_tutor_err="Tell us who is writing.",
        le_mail="Your email",
        le_mail_hint="This is where the confirmation and the opening notice go.",
        le_mail_err="We need a valid email to be able to tell you.",
        le_tel="Phone",
        le_tel_hint="Optional. Only if you would rather hear from us on WhatsApp.",
        le_quins="Which editions interest you",
        le_op=[("nadal", "Christmas camp"), ("setmana-santa", "Easter"), ("estiu", "Summer")],
        le_msg="Anything we should know",
        le_msg_hint="Optional. Age group, current club, whether they are coming with a friend…",
        le_ok="Add me to the list",
        le_done_h="You're on the list",
        le_done_p=(f'You are on the list. You will get a confirmation email and we will write when '
                   f'registration opens. In a hurry? The <a href="{WA}">club WhatsApp</a> is the '
                   f'fast route.'),
        le_rgpd=('What you write here is read by the club and is used only to tell you about the camp. '
                 'We do not add you to any other list. The detail is in the '
                 '<a href="/en/privacy-policy/">privacy policy</a>.'),
        ar_h="The 2026 edition, as it was published",
        ar_p=(f'This is what the <strong>Timechamber Experience 2026</strong> site said, kept here in '
              f'full. It tells you what the camp looks like when it opens: these were the numbers, '
              f'the weeks, the prices and the services. <strong>Dates and prices for the next '
              f'edition will be announced afresh</strong>.'),
        ar_claim="“The most innovative summer basketball camp in Barcelona.”",
        ar_dates="23 June to 1 August · La Nau del Clot",
        xifres=[("6", "themed weeks"), ("+200", "players per edition"),
                ("NBA", "elite methodology"), ("100%", "family satisfaction")],
        xifres_peu=("Figures as published on the 2026 camp site. The club's own count for summer 2026 "
                    "is 150 participants across the six weeks; the “+200 per edition” is the "
                    "campaign figure."),
        set_h="Six weeks, six experiences",
        set_p="Each week had its own identity. You could come for one week or for all of them.",
        set_mes=["June", "June–July", "July", "July", "July", "July–August"],
        preus_h="The prices that were published",
        preus_p=("These were the 2026 prices. Next edition's will be published when registration "
                 "opens."),
        preus=[("Recommended", "Full week", "€195", "9 am to 5 pm",
                ["Lunch included", "Early drop-off"]),
               ("Alternative", "Half day", "€160", "9 am to 1:30 pm",
                ["Same groups, same weekly focus"])],
        dte=("A 10% early-bird discount before 20 April with the code <b>BARNAAVIAT</b>. And you "
             "could book in 3 instalments: a first payment holds the place and the rest is split."),
        serv_h="What was included",
        serv=[("Hours", "9 am–1:30 pm half day · 9 am–5 pm full day"),
              ("Drop-off", "Early morning drop-off"),
              ("Lunch", "Lunch included on the full day"),
              ("Friday", "Trip to Illa Fantasia")],
        seu_h="The venue",
        seu_sub="The club's own facility",
        seu_adr="La Nau del Clot · Carrer de la Llacuna 172, 08018 Barcelona",
        seu_com="Directions →",
        mapa_btn="Load the Google map",
        mapa_nota="The map is Google's and sets cookies: it only loads if you ask for it.",
        hash_h="Hashtags and accounts",
        hash_p=("The camp conversation lives here. These are the accounts and tags everything on this "
                "page was published under."),
        peu=(f'The original 2026 site stays online for as long as its provider keeps it: '
             f'<a href="{WEB2026}" target="_blank" rel="noopener">timechamber.skywork.website</a>. '
             f'This page does not depend on it.'),
    ),
}

IDX = {"ca": 3, "es": 4, "en": 5}   # index del text de setmana dins SETMANES


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def bloc_estat(lang):
    t = T[lang]
    cal = "\n".join(
        f'      <div class="dl-row"><dt>{esc(q)}</dt><dd><strong>{esc(w)}</strong><br>{esc(e)}</dd></div>'
        for q, w, e in t["estat_cal"]
    )
    return f"""{E_INICI}
  <div class="narrow" style="margin-top:clamp(28px,4vw,44px)">
    <div class="campus-estat">
      <p class="eyebrow red">{esc(t['estat_tag'])}</p>
      <h2 style="margin-top:6px">{esc(t['estat_h'])}</h2>
      <p>{t['estat_p']}</p>
      <h3 style="margin-top:26px">{esc(t['estat_cal_h'])}</h3>
      <dl class="dl">
{cal}
      </dl>
      <p style="margin-top:18px">{t['estat_cta']}</p>
      <div class="btn-row">
        <a href="#llista-espera" class="btn red" data-cta="campus-estat-llista">{esc(t['estat_btn'])}</a>
        <a href="{WA}" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-estat-wa">{esc(t['estat_btn2'])}</a>
        <a href="{WEB2026}" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-estat-web2026">{esc('Web del campus 2026 →' if lang == 'ca' else ('Web del campus 2026 →' if lang == 'es' else '2026 camp site →'))}</a>
      </div>
    </div>
  </div>
  {E_FINAL}"""


def bloc_diferencia(lang):
    t = T[lang]
    files = "\n".join(
        f'      <div class="dl-row"><dt>{esc(a)}</dt><dd>{b}</dd></div>' for a, b in t["dif"]
    )
    return f"""{D_INICI}
    <h2>{esc(t['dif_h'])}</h2>
    <dl class="dl">
{files}
    </dl>
    {D_FINAL}"""


def bloc_arxiu(lang):
    t = T[lang]
    i = IDX[lang]

    ops = "\n".join(
        f'        <label class="check"><input type="checkbox" name="edicions" value="{v}"> {esc(n)}</label>'
        for v, n in t["le_op"]
    )
    xif = "\n".join(
        f'      <div><b>{esc(n)}</b><span>{esc(l)}</span></div>' for n, l in t["xifres"]
    )
    sets = "\n".join(
        f"""      <div class="week">
        <b>{s[0]}</b>
        <time>{esc(s[1])} {esc(t['set_mes'][k])}</time>
        <h4>{esc(s[2])}</h4>
        <p>{esc(s[i])}</p>
      </div>"""
        for k, s in enumerate(SETMANES)
    )
    preus = "\n".join(
        f"""      <div class="price-card{' top' if k == 0 else ''}">
        <span class="tag">{esc(tag)}</span>
        <b>{esc(nom)}</b>
        <p class="sched"><strong>{esc(preu)}</strong> · {esc(hora)}</p>
        <ul>
{chr(10).join(f'          <li>{esc(x)}</li>' for x in items)}
        </ul>
      </div>"""
        for k, (tag, nom, preu, hora, items) in enumerate(t["preus"])
    )
    play = ('<em><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff" aria-hidden="true">'
            '<path d="M8 5v14l11-7z"/></svg></em>')
    videos_seu = "\n".join(
        f"""      <div class="star">
        <button type="button" class="star-play" data-reel="{v[0]}" aria-label="{esc(v[i - 1])}">
          {play}
          <span>{esc(v[i - 1])}</span>
        </button>
        <div class="star-tx">
          <h5>{esc(v[i - 1])}</h5>
          <span class="role">{esc(v[i + 2])}</span>
        </div>
      </div>"""
        for v in VIDEOS_SEU
    )
    serv = "\n".join(
        f'      <div class="dl-row"><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in t["serv"]
    )

    return f"""{A_INICI}
    <h2 id="llista-espera">{esc(t['le_h'])}</h2>
    <p>{esc(t['le_p'])}</p>
    <form class="form" id="le-form" novalidate>
      <div class="form-row">
        <label for="le-nom">{esc(t['le_nom'])} <span class="req" aria-hidden="true">*</span></label>
        <input type="text" id="le-nom" name="nom" required autocomplete="off" aria-describedby="le-nom-err">
        <p class="form-err" id="le-nom-err" role="alert">{esc(t['le_nom_err'])}</p>
      </div>
      <div class="form-row">
        <label for="le-any">{esc(t['le_any'])} <span class="req" aria-hidden="true">*</span></label>
        <input type="text" inputmode="numeric" id="le-any" name="any" required autocomplete="off" aria-describedby="le-any-err">
        <p class="form-err" id="le-any-err" role="alert">{esc(t['le_any_err'])}</p>
      </div>
      <div class="form-row">
        <label for="le-tutor">{esc(t['le_tutor'])} <span class="req" aria-hidden="true">*</span></label>
        <input type="text" id="le-tutor" name="tutor" required autocomplete="name" aria-describedby="le-tutor-err">
        <p class="form-err" id="le-tutor-err" role="alert">{esc(t['le_tutor_err'])}</p>
      </div>
      <div class="form-row">
        <label for="le-mail">{esc(t['le_mail'])} <span class="req" aria-hidden="true">*</span></label>
        <span class="hint">{esc(t['le_mail_hint'])}</span>
        <input type="email" id="le-mail" name="correu" required autocomplete="email" aria-describedby="le-mail-err">
        <p class="form-err" id="le-mail-err" role="alert">{esc(t['le_mail_err'])}</p>
      </div>
      <div class="form-row">
        <label for="le-tel">{esc(t['le_tel'])}</label>
        <span class="hint">{esc(t['le_tel_hint'])}</span>
        <input type="tel" id="le-tel" name="telefon" autocomplete="tel">
      </div>
      <fieldset class="form-row">
        <legend>{esc(t['le_quins'])}</legend>
{ops}
      </fieldset>
      <div class="form-row">
        <label for="le-msg">{esc(t['le_msg'])}</label>
        <span class="hint">{esc(t['le_msg_hint'])}</span>
        <textarea id="le-msg" name="missatge"></textarea>
      </div>
      <div class="btn-row" style="margin-top:22px">
        <button type="submit" class="btn red">{esc(t['le_ok'])}</button>
      </div>
    </form>
    <div class="form-done" id="le-done" role="status">
      <h3>{esc(t['le_done_h'])}</h3>
      <p>{t['le_done_p']}</p>
    </div>
    <p style="font-size:13.5px;color:var(--ink-2)">{t['le_rgpd']}</p>

    <h2>{esc(t['ar_h'])}</h2>
    <p>{t['ar_p']}</p>
    <p style="font-size:19px;line-height:1.45"><em>{esc(t['ar_claim'])}</em><br>
    <span style="font-size:14.5px;color:var(--ink-2)">{esc(t['ar_dates'])}</span></p>

    <div class="facts">
{xif}
    </div>
    <p style="font-size:13.5px;color:var(--ink-2)">{esc(t['xifres_peu'])}</p>

    <h3>{esc(t['set_h'])}</h3>
    <p>{esc(t['set_p'])}</p>
    <div class="weeks">
{sets}
    </div>

    <h3>{esc(t['preus_h'])}</h3>
    <p>{esc(t['preus_p'])}</p>
    <div class="price-cards">
{preus}
    </div>
    <p class="price-note">{t['dte']}</p>

    <h3>{esc(t['serv_h'])}</h3>
    <dl class="dl">
{serv}
    </dl>

    <h3>{esc(t['seu_h'])}</h3>
    <p><strong>{esc(t['seu_sub'])}.</strong> {esc(t['seu_adr'])}.</p>
    <div class="btn-row">
      <a href="{MAPA}" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-com-arribar">{esc(t['seu_com'])}</a>
    </div>
    <h4>{esc(t['seu_vid_h'])}</h4>
    <p>{esc(t['seu_vid_p'])}</p>
    <div class="stars">
{videos_seu}
    </div>

    <div class="mapa-lazy" data-mapa="{esc(t['seu_adr'])}">
      <button type="button" class="btn ghost" id="mapa-carrega">{esc(t['mapa_btn'])}</button>
      <p style="font-size:13px;color:var(--ink-2);margin-top:8px">{esc(t['mapa_nota'])}</p>
    </div>

    <h3>{esc(t['hash_h'])}</h3>
    <p>{esc(t['hash_p'])}</p>
    <div class="btn-row">
      <a href="{IG}/cbgrupbarna/" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-ig-club">@cbgrupbarna</a>
      <a href="{IG}/timechamber_es/" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-ig-tc">@timechamber_es</a>
      <a href="{IG}/explore/tags/campustimechamber/" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-hash-1">#campustimechamber</a>
      <a href="{IG}/explore/tags/timechamber/" class="btn ghost" target="_blank" rel="noopener" data-cta="campus-hash-2">#timechamber</a>
    </div>

    <p style="font-size:13.5px;color:var(--ink-2);margin-top:clamp(22px,3vw,32px)">{t['peu']}</p>
    {A_FINAL}"""


FITXERS = {"ca": "campus/index.html", "es": "es/campus/index.html", "en": "en/campus/index.html"}


def main():
    dry = "--dry-run" in sys.argv
    for lang, cami in FITXERS.items():
        if not os.path.isfile(cami):
            sys.exit(f"No trobo {cami}. Executa'm des de l'arrel del repositori.")
        text = open(cami, encoding="utf-8").read()
        for ini, fi, fn in ((E_INICI, E_FINAL, bloc_estat),
                            (D_INICI, D_FINAL, bloc_diferencia),
                            (A_INICI, A_FINAL, bloc_arxiu)):
            if ini not in text or fi not in text:
                sys.exit(f"{cami} no te els marcadors {ini.split(':')[0][5:]}. "
                         "Posa'ls-hi a ma un cop i despres ja es regenera sol.")
            text = re.sub(re.escape(ini) + r".*?" + re.escape(fi),
                          lambda _, f=fn, l=lang: f(l), text, flags=re.S)
        vell = open(cami, encoding="utf-8").read()
        if text == vell:
            print(f"  sense canvis: {cami}")
        elif dry:
            print(f"  canviaria:    {cami}")
        else:
            open(cami, "w", encoding="utf-8").write(text)
            print(f"  escrit:       {cami}")
    if dry:
        print("--dry-run: no he escrit res.")


if __name__ == "__main__":
    main()
