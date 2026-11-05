#!/usr/bin/env python3
"""
Genera la nota de premsa «El Barna guanya el 19è Premi Dona i Esport» a les
tres llengües (ca/es/en), reutilitzant la capçalera, el peu i els estils
compartits de scripts/build-pages.py.

    python3 scripts/build-premi-dona-esport.py

Després cal refer el mapa d'idiomes, els hreflang i el sitemap:

    python3 scripts/i18n-routes.py && python3 scripts/i18n-hreflang.py \
        && python3 scripts/build-sitemap.py

No toca el PRESS[] de build-pages.py (pàgines d'articles escrits per altri
sobre el club): aquesta és una nota de premsa pròpia, amb format diferent
(sense «article complet» ni cita reproduïda), i viu en un script a part
perquè no calgui re-executar el generador principal, desfasat respecte al
publicat.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("build_pages", ROOT / "scripts" / "build-pages.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

from i18n_chrome import peu  # noqa: E402

faq_block = bp.faq_block

SITE = bp.SITE
EXT = bp.EXT

IMG = {
    "recollida": ("/premsa/img/premi-dona-i-esport-19a-edicio-recollida.webp", 1500, 2000),
    "trofeu": ("/premsa/img/premi-dona-i-esport-19a-edicio-trofeu.webp", 1097, 1950),
    "xec": ("/premsa/img/premi-dona-i-esport-19a-edicio-xec.webp", 1097, 1950),
}

PDFS = {
    "ca": "/premsa/documents/nota-de-premsa-premi-dona-i-esport-ca.pdf",
    "es": "/premsa/documents/nota-de-prensa-premi-dona-i-esport-es.pdf",
    "en": "/premsa/documents/press-release-premi-dona-i-esport-en.pdf",
}

PATHS = {
    "ca": "/premsa/premi-dona-i-esport-19a-edicio/",
    "es": "/es/premsa/premio-dona-i-esport-19a-edicion/",
    "en": "/en/premsa/dona-i-esport-award-19th-edition/",
}

ALTERNATES = [(c, SITE + p) for c, p in PATHS.items()] + [("x-default", SITE + PATHS["ca"])]


CONTENT = {
# ───────────────────────────────────────────────────────────────── CA ────
"ca": dict(
    lang="ca",
    crumb_inici="Inici", crumb_premsa="Premsa",
    title_tag="El Barna guanya el 19è Premi Dona i Esport · CB Grup Barna",
    desc=("El CB Grup Barna guanya el Premi al Club Esportiu de la 19a edició del Premi Dona i "
          "Esport de l'Ajuntament de Barcelona. Nota de premsa completa, dades i fotografies."),
    kw="Premi Dona i Esport, CB Grup Barna premi, bàsquet femení Barcelona, nota de premsa club bàsquet",
    eyebrow="Nota de premsa · 5 de novembre de 2026",
    h1="9 de les 12 jugadores del sènior B femení han crescut al CB Grup Barna",
    lede=("El Premi Dona i Esport de Barcelona reconeix el model del club del Clot, segon club de "
          "bàsquet guardonat: un club paritari i inclusiu."),
    badge_label="Per a difusió immediata",
    stats=[("35 de 68", "entrenadors són dones: l'equip tècnic compta amb 68 entrenadors, 35 dones"),
           ("50 / 50", "dels ingressos del club van a la línia femenina i a la masculina"),
           ("2n", "club de bàsquet que rep el Premi Dona i Esport")],
    intro=[
      ("La temporada passada (2025-26), 9 de les 12 jugadores del sènior B femení provenien de la "
       "pròpia cantera; en anys anteriors només 3 o 4 feien el salt de júnior a sènior. Aquest "
       "itinerari, de l'escoleta al sènior, forma part del model que ha reconegut el Premi al Club "
       "Esportiu de la 19a edició del Premi Dona i Esport de l'Ajuntament de Barcelona, dotat amb "
       "3.000 euros."),
      ("Fundat l'any 1965 al Clot, el CB Grup Barna és el segon club de bàsquet que rep el premi, "
       "després del CB Santa Rosa de Lima-Horta (12a edició). Avui compta amb 450 jugadors i "
       "jugadores i 35 equips federats. A la pista, els equips sèniors masculí i femení competeixen "
       "a la Supercopa, la màxima categoria del bàsquet català."),
    ],
    quotes_intro=[
      ("«El premi és d'elles, perquè des de petites han decidit apostar pel club, i això és un mèrit.»",
       "Ana Fernández Durán · Junta del CB Grup Barna"),
      ("«Les noies del sènior són un exemple a seguir: és la màxima categoria on pots arribar [al club].»",
       "Jugadora de base · CB Grup Barna"),
    ],
    h2_context="Context i declaracions",
    h3_igualtat="La igualtat, a l'estructura",
    p_igualtat=("El club destina el 50% de tots els seus ingressos a la línia femenina i l'altre 50% "
                "a la masculina, de manera que totes dues disposen dels mateixos recursos. Aquesta "
                "aposta es reflecteix també a la banqueta: l'equip tècnic està format per 68 "
                "entrenadors, dels quals 35 són dones."),
    h3_escoleta="De l'escoleta al sènior",
    p_escoleta=("Al CB Grup Barna, el pas de júnior a sènior és el moment de major abandonament "
                "femení. Per això el club ha analitzat aquest pas. La temporada 2025-26, de les 12 "
                "jugadores de l'equip sènior B femení, 9 provenen de la pròpia cantera, quatre d'elles "
                "des de l'escoleta, i només 3 han estat noves incorporacions; en anys anteriors, només "
                "3 o 4 jugadores feien aquest pas."),
    h3_premi="«El premi és d'elles»",
    p_premi=[
      ("En el seu parlament de recollida, Ana Fernández Durán, membre de la Junta del club, va "
       "dedicar el premi a les jugadores. Va recordar que el camí va començar el 1965 i que el "
       "reconeixement és merescut per totes les persones que han format part del CB Grup Barna."),
      ("El model és un itinerari complet: les més petites poden veure que tenen totes les categories "
       "i tots els equips necessaris per anar pujant fins al sènior. Les grans els serveixen de "
       "referent i el club continua creant entrenadores, perquè les actuals també són referents per "
       "a elles. Habitualment cada equip compta amb tres entrenadors, i ja hi ha equips de noies "
       "dirigits íntegrament per tres entrenadores. A més, cada cop més entrenadores coordinen els "
       "entrenaments i els partits d'equips de nois."),
      ("Fer-ho bé, va subratllar, vol dir crear «un espai segur on els adolescents i els nens petits "
       "es sentin segurs» en un esport «molt integrador»: «el principal orgull»."),
    ],
    pull_quote=("«Tenim moltes copes al club, però estem orgulloses d'elles, des de petites fins a "
                "grans.»"),
    pull_quote_by="Ana Fernández Durán · Junta del CB Grup Barna",
    h3_base="Un reconeixement al bàsquet de base",
    p_base=("El premi reconeix un model que entén que les nenes i les joves no només han de tenir "
            "l'oportunitat de practicar bàsquet, sinó també de créixer, formar-se, assumir "
            "responsabilitats i convertir-se en referents per a les generacions següents. El Premi "
            "Dona i Esport posa en valor la feina quotidiana dels clubs de barri, sovint lluny dels "
            "grans focus mediàtics. Per al CB Grup Barna és un impuls per continuar construint un "
            "esport en què jugar, entrenar i liderar no depenguin del gènere. Aquest compromís conviu "
            "amb l'aposta per l'esport inclusiu, amb el projecte Barna Màgics, i amb una estreta "
            "vinculació amb la vida social del Clot i de Sant Martí."),
    h2_elles="Aquí parlen elles",
    quotes_elles=[
      ("«Porto molt de temps al Barna i el tracte amb la gent del club, les jugadores, és molt agradable.»",
       "Jugadora de base · CB Grup Barna"),
      ("«Des de petita sempre he volgut arribar-hi. Entrenar els de l'escoleta és una experiència molt divertida.»",
       "Jugadora de base · CB Grup Barna"),
      ("«Em veig molts anys en aquest club. Encara que em truquessin d'un altre, no em canviaria.»",
       "Jugadora · CB Grup Barna"),
    ],
    h2_sobre="Sobre el CB Grup Barna",
    p_sobre=("Club de bàsquet de base sense ànim de lucre, fundat el 1965 al Clot (Sant Martí, "
             "Barcelona), amb seu esportiva a La Nau del Clot. Treballa per la paritat, el creixement "
             "del bàsquet femení, la formació d'entrenadores i l'esport inclusiu. Més informació: "
             "cbgrupbarna.info"),
    h2_contacte="Contacte de premsa",
    contacte=["Ana Fernández Durán", "Directora de Màrqueting · CB Grup Barna",
              "ana.fernandez@cbgrupbarna.info", "698 425 153"],
    p_contacte_extra=("Entrevistes, material fotogràfic, dades de la candidatura i visites a La Nau "
                       "del Clot a disposició dels mitjans."),
    h2_descarrega="Descarrega la nota de premsa",
    dl_label="PDF · nota de premsa completa (3 pàg.)",
    dl_other_label="També disponible en",
    dl_langs=[("es", "castellà"), ("en", "anglès")],
    h2_presentacio="Veure també",
    presentacio_text=("La nota de premsa convertida en presentació, llesta per compartir amb "
                       "famílies, patrocinadors i mitjans."),
    presentacio_cta="Descarregar la presentació (PDF)",
    presentacio_cta_pptx="Descarregar en PowerPoint (editable)",
    faq=[
      ("Quin premi ha guanyat el CB Grup Barna?",
       "El Premi al Club Esportiu de la 19a edició del Premi Dona i Esport de l'Ajuntament de "
       "Barcelona, dotat amb 3.000 euros, lliurat el 4 de novembre de 2026."),
      ("Per què ha guanyat el premi el CB Grup Barna?",
       "Pel seu model paritari i inclusiu: el 50% dels ingressos van a la línia femenina i el 50% a "
       "la masculina, 35 dels 68 entrenadors són dones, i 9 de les 12 jugadores del sènior B femení "
       "de la temporada 2025-26 provenen de la pròpia cantera del club."),
      ("Quin altre club de bàsquet ha rebut aquest premi?",
       "El CB Grup Barna és el segon club de bàsquet que el rep, després del CB Santa Rosa de "
       "Lima-Horta, guardonat en la 12a edició."),
      ("Com es pot contactar amb el club per a temes de premsa?",
       "Escrivint a ana.fernandez@cbgrupbarna.info o trucant al 698 425 153. El club ofereix "
       "entrevistes, material fotogràfic i visites a La Nau del Clot."),
    ],
    closer_title="Vols saber més del CB Grup Barna?",
    closer_text="El model paritari i l'itinerari de l'escoleta al sènior, explicats amb dades oficials.",
    closer_btns=[("Bàsquet femení al Barna", "/femeni/", "red", "premi-closer-femeni"),
                 ("Dades oficials del club", "/grup-barna-dades-oficials/", "ghost", "premi-closer-dades")],
),
# ───────────────────────────────────────────────────────────────── ES ────
"es": dict(
    lang="es",
    crumb_inici="Inicio", crumb_premsa="Prensa",
    title_tag="El Barna gana el 19.º Premi Dona i Esport · CB Grup Barna",
    desc=("El CB Grup Barna gana el Premio al Club Deportivo de la 19.ª edición del Premi Dona i "
          "Esport del Ayuntamiento de Barcelona. Nota de prensa completa, datos y fotografías."),
    kw="Premi Dona i Esport, CB Grup Barna premio, baloncesto femenino Barcelona, nota de prensa club baloncesto",
    eyebrow="Nota de prensa · 5 de noviembre de 2026",
    h1="9 de las 12 jugadoras del sénior B femenino se han formado en el CB Grup Barna",
    lede=("El Premi Dona i Esport de Barcelona reconoce el modelo del club del Clot, segundo club de "
          "baloncesto galardonado: un club paritario e inclusivo."),
    badge_label="Para difusión inmediata",
    stats=[("35 de 68", "entrenadores son mujeres: el equipo técnico cuenta con 68 entrenadores, 35 mujeres"),
           ("50 / 50", "de los ingresos del club van a la línea femenina y a la masculina"),
           ("2.º", "club de baloncesto que recibe el Premi Dona i Esport")],
    intro=[
      ("La temporada pasada (2025-26), 9 de las 12 jugadoras del sénior B femenino procedían de la "
       "propia cantera; en años anteriores solo 3 o 4 daban el salto de júnior a sénior. Este "
       "itinerario, de la escoleta al sénior, forma parte del modelo que ha reconocido el Premio al "
       "Club Deportivo de la 19.ª edición del Premi Dona i Esport del Ayuntamiento de Barcelona, "
       "dotado con 3.000 euros."),
      ("Fundado en 1965 en el Clot, el CB Grup Barna es el segundo club de baloncesto que recibe el "
       "premio, después del CB Santa Rosa de Lima-Horta (12.ª edición). Hoy cuenta con 450 jugadores "
       "y jugadoras y 35 equipos federados. En la pista, los equipos sénior masculino y femenino "
       "compiten en la Supercopa, la máxima categoría del baloncesto catalán."),
    ],
    quotes_intro=[
      ("«El premio es de ellas, porque desde pequeñas han decidido apostar por el club, y eso es un mérito.»",
       "Ana Fernández Durán · Junta del CB Grup Barna"),
      ("«Las chicas del sénior son un ejemplo a seguir: es la máxima categoría a la que puedes llegar [en el club].»",
       "Jugadora de base · CB Grup Barna"),
    ],
    h2_context="Contexto y declaraciones",
    h3_igualtat="La igualdad, en la estructura",
    p_igualtat=("El club destina el 50% de todos sus ingresos a la línea femenina y el otro 50% a la "
                "masculina, de modo que ambas disponen de los mismos recursos. Esta apuesta se refleja "
                "también en el banquillo: el equipo técnico está formado por 68 entrenadores, de los "
                "cuales 35 son mujeres."),
    h3_escoleta="De la escoleta al sénior",
    p_escoleta=("En el CB Grup Barna, el paso de júnior a sénior es el momento de mayor abandono "
                "femenino. Por eso el club ha analizado este paso. En la temporada 2025-26, de las 12 "
                "jugadoras del equipo sénior B femenino, 9 proceden de la propia cantera, cuatro de "
                "ellas desde la escoleta, y solo 3 han sido nuevas incorporaciones; en años "
                "anteriores, solo 3 o 4 jugadoras daban este paso."),
    h3_premi="«El premio es de ellas»",
    p_premi=[
      ("En su discurso de recogida, Ana Fernández Durán, miembro de la Junta del club, dedicó el "
       "premio a las jugadoras. Recordó que el camino empezó en 1965 y que el reconocimiento es "
       "merecido por todas las personas que han formado parte del CB Grup Barna."),
      ("El modelo es un itinerario completo: las más pequeñas pueden ver que tienen todas las "
       "categorías y todos los equipos necesarios para ir subiendo hasta el sénior. Las mayores les "
       "sirven de referente y el club sigue creando entrenadoras, porque las actuales también son "
       "referentes para ellas. Habitualmente cada equipo cuenta con tres entrenadores, y ya hay "
       "equipos de chicas dirigidos íntegramente por tres entrenadoras. Además, cada vez más "
       "entrenadoras coordinan los entrenamientos y los partidos de equipos de chicos."),
      ("Hacerlo bien, subrayó, significa crear «un espacio seguro donde los adolescentes y los niños "
       "pequeños se sientan seguros» en un deporte «muy integrador»: «el principal orgullo»."),
    ],
    pull_quote=("«Tenemos muchas copas en el club, pero estamos orgullosas de ellas, desde pequeñas "
                "hasta mayores.»"),
    pull_quote_by="Ana Fernández Durán · Junta del CB Grup Barna",
    h3_base="Un reconocimiento al baloncesto de base",
    p_base=("El premio reconoce un modelo que entiende que las niñas y las jóvenes no solo deben "
            "tener la oportunidad de practicar baloncesto, sino también de crecer, formarse, asumir "
            "responsabilidades y convertirse en referentes para las generaciones siguientes. El Premi "
            "Dona i Esport pone en valor el trabajo cotidiano de los clubes de barrio, a menudo lejos "
            "de los grandes focos mediáticos. Para el CB Grup Barna es un impulso para seguir "
            "construyendo un deporte en el que jugar, entrenar y liderar no dependan del género. Este "
            "compromiso convive con la apuesta por el deporte inclusivo, con el proyecto Barna Màgics "
            "y con un estrecho vínculo con la vida social del Clot y de Sant Martí."),
    h2_elles="Aquí hablan ellas",
    quotes_elles=[
      ("«Llevo mucho tiempo en el Barna y el trato con la gente del club, las jugadoras, es muy agradable.»",
       "Jugadora de base · CB Grup Barna"),
      ("«Desde pequeña siempre he querido llegar. Entrenar a los de la escoleta es una experiencia muy divertida.»",
       "Jugadora de base · CB Grup Barna"),
      ("«Me veo muchos años en este club. Aunque me llamaran de otro, no me cambiaría.»",
       "Jugadora · CB Grup Barna"),
    ],
    h2_sobre="Sobre el CB Grup Barna",
    p_sobre=("Club de baloncesto de base sin ánimo de lucro, fundado en 1965 en el Clot (Sant Martí, "
             "Barcelona), con sede deportiva en La Nau del Clot. Trabaja por la paridad, el "
             "crecimiento del baloncesto femenino, la formación de entrenadoras y el deporte "
             "inclusivo. Más información: cbgrupbarna.info"),
    h2_contacte="Contacto de prensa",
    contacte=["Ana Fernández Durán", "Directora de Márketing · CB Grup Barna",
              "ana.fernandez@cbgrupbarna.info", "698 425 153"],
    p_contacte_extra=("Entrevistas, material fotográfico, datos de la candidatura y visitas a La Nau "
                       "del Clot a disposición de los medios."),
    h2_descarrega="Descarga la nota de prensa",
    dl_label="PDF · nota de prensa completa (3 pág.)",
    dl_other_label="También disponible en",
    dl_langs=[("ca", "catalán"), ("en", "inglés")],
    h2_presentacio="Ver también",
    presentacio_text=("La nota de prensa convertida en presentación, lista para compartir con "
                       "familias, patrocinadores y medios."),
    presentacio_cta="Descargar la presentación (PDF)",
    presentacio_cta_pptx="Descargar en PowerPoint (editable)",
    faq=[
      ("¿Qué premio ha ganado el CB Grup Barna?",
       "El Premio al Club Deportivo de la 19.ª edición del Premi Dona i Esport del Ayuntamiento de "
       "Barcelona, dotado con 3.000 euros, entregado el 4 de noviembre de 2026."),
      ("¿Por qué ha ganado el premio el CB Grup Barna?",
       "Por su modelo paritario e inclusivo: el 50% de los ingresos van a la línea femenina y el 50% "
       "a la masculina, 35 de los 68 entrenadores son mujeres, y 9 de las 12 jugadoras del sénior B "
       "femenino de la temporada 2025-26 proceden de la propia cantera del club."),
      ("¿Qué otro club de baloncesto ha recibido este premio?",
       "El CB Grup Barna es el segundo club de baloncesto que lo recibe, después del CB Santa Rosa "
       "de Lima-Horta, galardonado en la 12.ª edición."),
      ("¿Cómo se puede contactar con el club para temas de prensa?",
       "Escribiendo a ana.fernandez@cbgrupbarna.info o llamando al 698 425 153. El club ofrece "
       "entrevistas, material fotográfico y visitas a La Nau del Clot."),
    ],
    closer_title="¿Quieres saber más sobre el CB Grup Barna?",
    closer_text="El modelo paritario y el itinerario de la escoleta al sénior, explicados con datos oficiales.",
    closer_btns=[("Baloncesto femenino en el Barna", "/es/baloncesto-femenino/", "red", "premi-closer-femeni"),
                 ("Datos oficiales del club", "/es/grup-barna-dades-oficials/", "ghost", "premi-closer-dades")],
),
# ───────────────────────────────────────────────────────────────── EN ────
"en": dict(
    lang="en",
    crumb_inici="Home", crumb_premsa="Press",
    title_tag="CB Grup Barna wins the 19th Premi Dona i Esport · CB Grup Barna",
    desc=("CB Grup Barna wins the Club Award of the 19th edition of Barcelona City Council's Premi "
          "Dona i Esport. Full press release, data and photographs."),
    kw="Premi Dona i Esport, CB Grup Barna award, women's basketball Barcelona, basketball club press release",
    eyebrow="Press release · 5 November 2026",
    h1="9 of 12 players on CB Grup Barna's senior B women's team came up through the club",
    lede=("Barcelona's Premi Dona i Esport recognises the Clot club, the second basketball club to "
          "win it: inclusive and gender-balanced."),
    badge_label="For immediate release",
    stats=[("35 / 68", "coaches are women: the coaching staff has 68 coaches, 35 of them women"),
           ("50 / 50", "of club income goes to the women's line and to the men's line"),
           ("2nd", "basketball club to receive the Premi Dona i Esport")],
    intro=[
      ("Last season (2025-26), 9 of the 12 players on the senior B women's team came from the club's "
       "own youth system; in previous years only 3 or 4 made the step from junior to senior. This "
       "pathway, from the escoleta (youngest ages) to the senior teams, is part of the model "
       "recognised by the Club Award of the 19th Premi Dona i Esport of Barcelona City Council, "
       "worth €3,000."),
      ("Founded in 1965 in the Clot neighbourhood, CB Grup Barna is the second basketball club to "
       "receive the award, after CB Santa Rosa de Lima-Horta (12th edition). It now has 450 players "
       "and 35 federated teams. On court, both the men's and women's senior teams compete in the "
       "Supercopa, the top category of Catalan basketball."),
    ],
    quotes_intro=[
      ("«The award is theirs, because since they were little girls they chose to commit to the club, "
       "and that is a merit.»",
       "Ana Fernández Durán · Board of CB Grup Barna"),
      ("«The senior girls are an example to follow: it is the top category you can reach [at the club].»",
       "Youth player · CB Grup Barna"),
    ],
    h2_context="Context and statements",
    h3_igualtat="Equality, built into the structure",
    p_igualtat=("The club allocates 50% of all its income to the women's line and the other 50% to "
                "the men's, so both have the same resources. This commitment also shows on the bench: "
                "the coaching staff has 68 coaches, 35 of them women."),
    h3_escoleta="From the escoleta to the senior team",
    p_escoleta=("At CB Grup Barna, the step from junior to senior is when most women players drop "
                "out. That is why the club has analysed this step. In 2025-26, of the 12 players on "
                "the senior B women's team, 9 came from the club's own youth system, four of them "
                "since the escoleta, and only 3 were new signings; in previous years, only 3 or 4 "
                "players made this step."),
    h3_premi="«The award is theirs»",
    p_premi=[
      ("In her acceptance speech, Ana Fernández Durán, a member of the club's Board, dedicated the "
       "award to the players. She recalled that the journey began in 1965 and that the recognition "
       "belongs to everyone who has been part of CB Grup Barna."),
      ("The model is a complete pathway: the youngest players can see that all the categories and "
       "teams they need are there to move up to the senior level. The older players serve as role "
       "models, and the club keeps training new women coaches, because the current ones are role "
       "models for them too. Each team usually has three coaches, and there are already girls' teams "
       "led entirely by three women coaches. In addition, more and more women coaches are "
       "coordinating the training sessions and matches of boys' teams."),
      ("Doing it well, she stressed, means creating «a safe space where teenagers and young children "
       "feel safe» in a sport that is «very inclusive»: «our main source of pride»."),
    ],
    pull_quote=("«We have many trophies at the club, but we are proud of them, from the youngest to "
                "the oldest.»"),
    pull_quote_by="Ana Fernández Durán · Board of CB Grup Barna",
    h3_base="Recognition for grassroots basketball",
    p_base=("The award recognises a model that holds that girls and young women should not only have "
            "the chance to play basketball, but also to grow, train, take on responsibility and "
            "become role models for the next generations. The Premi Dona i Esport values the everyday "
            "work of neighbourhood clubs, often far from the media spotlight. For CB Grup Barna it is "
            "a boost to keep building a sport in which playing, coaching and leading do not depend on "
            "gender. This commitment sits alongside its support for inclusive sport, through the "
            "Barna Màgics project, and its close ties to the social life of the Clot and Sant Martí."),
    h2_elles="The players speak",
    quotes_elles=[
      ("«I have been at Barna for a long time, and dealing with the people at the club, the players, "
       "is really pleasant.»",
       "Youth player · CB Grup Barna"),
      ("«Since I was little I have always wanted to get there. Coaching the little ones in the "
       "escoleta is a really fun experience.»",
       "Youth player · CB Grup Barna"),
      ("«I see myself at this club for many years. Even if another club called me, I would not switch.»",
       "Player · CB Grup Barna"),
    ],
    h2_sobre="About CB Grup Barna",
    p_sobre=("Non-profit grassroots basketball club founded in 1965 in the Clot (Sant Martí, "
             "Barcelona), based at La Nau del Clot. It works for gender parity, the growth of women's "
             "basketball, the training of women coaches and inclusive sport. More information: "
             "cbgrupbarna.info"),
    h2_contacte="Press contact",
    contacte=["Ana Fernández Durán", "Marketing Director · CB Grup Barna",
              "ana.fernandez@cbgrupbarna.info", "+34 698 425 153"],
    p_contacte_extra=("Interviews, photographs, application data and visits to La Nau del Clot "
                       "available to the media."),
    h2_descarrega="Download the press release",
    dl_label="PDF · full press release (3 pp.)",
    dl_other_label="Also available in",
    dl_langs=[("ca", "Catalan"), ("es", "Spanish")],
    h2_presentacio="See also",
    presentacio_text=("The press release turned into a presentation, ready to share with families, "
                       "sponsors and the media."),
    presentacio_cta="Download the presentation (PDF)",
    presentacio_cta_pptx="Download as PowerPoint (editable)",
    faq=[
      ("What award did CB Grup Barna win?",
       "The Club Award of the 19th edition of Barcelona City Council's Premi Dona i Esport, worth "
       "€3,000, presented on 4 November 2026."),
      ("Why did CB Grup Barna win the award?",
       "For its gender-balanced, inclusive model: 50% of income goes to the women's line and 50% to "
       "the men's, 35 of the 68 coaches are women, and 9 of the 12 players on the 2025-26 senior B "
       "women's team came from the club's own youth system."),
      ("What other basketball club has received this award?",
       "CB Grup Barna is the second basketball club to receive it, after CB Santa Rosa de "
       "Lima-Horta, which won the 12th edition."),
      ("How can the media contact the club?",
       "By writing to ana.fernandez@cbgrupbarna.info or calling +34 698 425 153. The club offers "
       "interviews, photographs and visits to La Nau del Clot."),
    ],
    closer_title="Want to know more about CB Grup Barna?",
    closer_text="The gender-balanced model and the pathway from the escoleta to the senior team, explained with official data.",
    closer_btns=[("Women's basketball at the Barna", "/en/womens-basketball/", "red", "premi-closer-femeni"),
                 ("Official club data", "/en/grup-barna-dades-oficials/", "ghost", "premi-closer-dades")],
),
}


def build(lang):
    c = CONTENT[lang]
    url = SITE + PATHS[lang]
    img0 = SITE + IMG["recollida"][0]

    stats_html = ''.join(
        f'<div><p style="font-family:var(--display);font-size:clamp(26px,3.4vw,38px);'
        f'margin-bottom:8px">{n}</p><p style="font-size:12.5px;color:var(--ink-2);'
        f'max-width:26ch">{d}</p></div>' for n, d in c["stats"])

    def quote_block(items):
        return ''.join(
            f'<blockquote><p style="font-weight:500">{q}</p>'
            f'<p style="margin-top:10px;font-family:var(--body);font-size:10px;'
            f'letter-spacing:0.16em;text-transform:uppercase;color:var(--muted)">{by}</p></blockquote>'
            for q, by in items)

    intro_html = ''.join(f'<p>{p}</p>' for p in c["intro"])
    premi_html = ''.join(f'<p>{p}</p>' for p in c["p_premi"])

    gallery = (
        f'<figure><img src="{IMG["trofeu"][0]}" alt="{c["h1"]}" loading="lazy" decoding="async" '
        f'width="{IMG["trofeu"][1]}" height="{IMG["trofeu"][2]}"></figure>'
        f'<figure><img src="{IMG["xec"][0]}" alt="{c["h1"]}" loading="lazy" decoding="async" '
        f'width="{IMG["xec"][1]}" height="{IMG["xec"][2]}"></figure>'
    )

    dl_other = ''.join(
        f'<a href="{PDFS[lc]}" class="btn ghost"{EXT} data-cta="premi-pdf-{lc}">{lbl}</a>'
        for lc, lbl in c["dl_langs"])

    faq_html, faq_ld = faq_block(c["faq"])

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "NewsArticle", "@id": url + "#article",
         "headline": c["h1"], "description": c["desc"], "url": url,
         "datePublished": "2026-11-05", "dateModified": "2026-11-05", "inLanguage": c["lang"],
         "author": {"@id": SITE + "/#club"}, "publisher": {"@id": SITE + "/#club"},
         "image": img0, "isPartOf": {"@id": SITE + "/premsa/#premsa"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "about": {"@id": SITE + "/#club"}},
        faq_ld,
        bp.BREADCRUMB([(c["crumb_inici"], "/"), (c["crumb_premsa"], "/premsa/"), (c["h1"][:40] + "…", PATHS[lang])]),
    ]}

    body = f"""
<div class="wrap"><nav class="crumb" aria-label="Fil d'Ariadna"><a href="/">{c["crumb_inici"]}</a> · <a href="/premsa/">{c["crumb_premsa"]}</a> · <span>{c["h1"][:40]}…</span></nav></div>
<div class="wrap">
  <div class="phead narrow">
    <p class="eyebrow red">{c["eyebrow"]}</p>
    <h1>{c["h1"]}</h1>
    <p class="lede">{c["lede"]}</p>
    <div class="press-badge">{c["badge_label"]}</div>
    <div class="phead-media">
      <img src="{IMG["recollida"][0]}" alt="{c["h1"]}" width="{IMG["recollida"][1]}" height="{IMG["recollida"][2]}" fetchpriority="high">
    </div>
  </div>
  <article class="narrow prose">
    <div class="press-grid" style="grid-template-columns:repeat(3,1fr);text-align:center;border:1px solid var(--line);padding:clamp(20px,3vw,32px);background:var(--paper-2)">{stats_html}</div>
    {intro_html}
    {quote_block(c["quotes_intro"])}
    <h2>{c["h2_context"]}</h2>
    <h3>{c["h3_igualtat"]}</h3>
    <p>{c["p_igualtat"]}</p>
    <h3>{c["h3_escoleta"]}</h3>
    <p>{c["p_escoleta"]}</p>
    <h3>{c["h3_premi"]}</h3>
    {premi_html}
    <blockquote><p style="font-weight:500">{c["pull_quote"]}</p>
    <p style="margin-top:10px;font-family:var(--body);font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:var(--muted)">{c["pull_quote_by"]}</p></blockquote>
    <h3>{c["h3_base"]}</h3>
    <p>{c["p_base"]}</p>
    <h2>{c["h2_elles"]}</h2>
    <div class="press-grid two">{gallery}</div>
    {quote_block(c["quotes_elles"])}
    <h2>{c["h2_sobre"]}</h2>
    <p>{c["p_sobre"]}</p>
    <h2>{c["h2_contacte"]}</h2>
    <p><strong>{c["contacte"][0]}</strong><br>{c["contacte"][1]}<br>
    <a href="mailto:{c["contacte"][2]}">{c["contacte"][2]}</a><br>{c["contacte"][3]}</p>
    <p>{c["p_contacte_extra"]}</p>
    <h2>{c["h2_descarrega"]}</h2>
    <div class="btn-row" style="display:flex;flex-wrap:wrap;gap:12px">
      <a href="{PDFS[lang]}" class="btn red"{EXT} data-cta="premi-pdf-{lang}">{c["dl_label"]}</a>
    </div>
    <p style="margin-top:14px;font-size:12.5px;color:var(--muted)">{c["dl_other_label"]}: {dl_other}</p>
    <h2>{c["h2_presentacio"]}</h2>
    <p>{c["presentacio_text"]}</p>
    <div class="btn-row" style="display:flex;flex-wrap:wrap;gap:12px">
      <a href="/premsa/documents/presentacio-premi-dona-i-esport.pdf" class="btn ghost"{EXT} data-cta="premi-presentacio">{c["presentacio_cta"]}</a>
      <a href="/premsa/documents/presentacio-premi-dona-i-esport.pptx" class="btn ghost"{EXT} data-cta="premi-presentacio-pptx">{c["presentacio_cta_pptx"]}</a>
    </div>
    <h2>{{faq_h2}}</h2>
    {faq_html}
    <div style="margin-top:clamp(34px,5vw,60px)">
    {bp.closer(c["closer_title"], c["closer_text"], [(t, u, cl, d) for t, u, cl, d in c["closer_btns"]])}
    </div>
  </article>
</div>
"""
    faq_titles = {"ca": "Preguntes freqüents", "es": "Preguntas frecuentes", "en": "Frequently asked questions"}
    body = body.replace("{faq_h2}", faq_titles[lang])

    html = (bp.head(c["title_tag"], c["desc"], url, img0, ld, c["kw"], ALTERNATES, lang=lang)
            + body + peu(lang))
    rel = PATHS[lang].lstrip("/") + "index.html"
    print(bp.write(rel, html))


if __name__ == "__main__":
    for lang in ("ca", "es", "en"):
        build(lang)
