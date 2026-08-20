#!/usr/bin/env python3
"""
Genera les tres versions idiomàtiques de /escoleta/ a partir d'un únic origen.

Origen  : scripts/src/escoleta.source.html  (blocs data-lang="ca" i data-lang="es")
Sortida : escoleta/index.html     (ca)
          es/escoleta/index.html  (es)
          en/escoleta/index.html  (en)

Cada sortida conté NOMÉS el seu idioma al DOM (res amagat amb CSS), amb el seu
propi <html lang>, canonical, hreflang recíproc, Open Graph i JSON-LD.

Ús:  python3 scripts/build_escoleta_i18n.py
"""
import json
import os
import re

import lxml.html as LH
from lxml import etree

SRC = 'scripts/src/escoleta.source.html'
BASE = 'https://cbgrupbarna.info'
URLS = {
    'ca': f'{BASE}/escoleta/',
    'es': f'{BASE}/es/escoleta/',
    'en': f'{BASE}/en/escoleta/',
}
OUT = {
    'ca': 'escoleta/index.html',
    'es': 'es/escoleta/index.html',
    'en': 'en/escoleta/index.html',
}
OG_LOCALE = {'ca': 'ca_ES', 'es': 'es_ES', 'en': 'en_GB'}
LANG_NAME = {'ca': 'CAT', 'es': 'CAST', 'en': 'ENG'}

# ---------------------------------------------------------------- anglès
# Traducció dels 110 blocs data-lang="ca", per índex. Es conserva el marcatge
# intern (<br>, <em>, <strong>, <b>, <span>, <svg>…) exactament igual.
EN = {
0: 'Basketball school · CB Grup Barna · since 1965',
1: 'Ten of them<br>started on<br><em>this court</em>',
2: 'And none of them knew it at six years old.',
3: 'A Liga Femenina Endesa head coach and a captain in that same league. An ACB player. A Tercera FEB champion. Four from Barça. All of them got their first licence here, and none of them remembers it as paperwork: they remember a schoolyard court and a man who taught them to dribble.',
4: 'And it is not just these ten. There are many more: dozens of players formed on this court over sixty years. We have picked a few here to introduce people who matter to the club, but the real list would not fit on one page.',
5: 'Grup Barna Basketball School · Sant Martí, Barcelona',
6: 'Open Days · Escoleta',
7: 'Come and try<br>a session',
8: 'No commitment and no payment. Your son or daughter trains with us for a day, meets the coaches and the rest of the group, and then you decide. That is how everyone on this page started.',
9: 'Book an Open Day',
10: 'About the Escoleta',
11: '<b>Ages 4 to 8</b>Beginners’ basketball school',
12: '<b>El Clot</b>Sant Martí, Barcelona',
13: '<b>Since 1965</b>60 years coaching in the neighbourhood',
14: 'It all began<br>in a schoolyard',
15: 'There was no parquet. There were no stands. There was a hoop bolted to a wall, a concrete floor and eleven children in black shirts and red shorts.',
16: 'The club and the Escoleta were born in <strong>1965</strong>. On the left of the photo, in glasses and a jumper, is <strong>Julio Torralba</strong>, founder of the club and its defining coach for decades. Today, sixty years on, he is still on court every week with the four- to eight-year-olds of the Escoleta.',
17: '<b>The 1990s.</b> The boy carrying the ball is <b>Javier Torralba</b>, today head coach of Valencia Basket Femení in the Liga Femenina Endesa. An outdoor game; the crowd sitting on the kerb.',
18: '<b>One trophy, ten hands.</b> The celebration has not changed at all.',
19: '<b>Generation after generation.</b> Julio, on the right, with another intake.',
20: 'The club was not born in a sports hall.<br>It was born in a schoolyard.',
21: 'The document<br>that proves it',
22: 'Season 1993-94. Boys’ Mini Championship, Level A. An eleven-year-old files his first federation licence.',
23: 'Original document',
24: 'Player',
25: 'Born',
26: 'Club',
27: 'Category',
28: 'Season',
29: 'That boy is today <strong>Javier Torralba</strong>, head coach of <strong>Valencia Basket Femení</strong>. He previously led Segle XXI, one of the leading development centres in Spanish women’s basketball, and has worked with Spain’s youth national teams.',
30: 'When he was presented in Valencia he said he felt “strongly identified with the development and growth of young players”. That is not a line for the cameras. It is what he saw at home: his father, Julio, still does it every Tuesday.',
31: 'Father and son.<br>The same craft, thirty years apart.',
32: 'The ones who<br>went far',
33: 'No basketball school can promise a child will reach the elite. What the Barna can show is that some have come from here.',
34: 'Head coach · Valencia Basket · LF Endesa',
35: 'This is the photo from his first licence, season 93-94. He led Segle XXI and has worked with Spain’s development squads. Today he coaches in the top tier of Spanish women’s basketball.',
36: '<span class="tag">NOW</span><span class="val">Head coach of Valencia Basket Femení<em>Liga Femenina Endesa · under contract to 2029</em></span>',
37: 'Centre · ACB and LEB Or',
38: 'Barcelona, 1982. A 2.02 m centre and the same intake as Javier: they appear in the same team photo. He debuted in the ACB with Caprabo Lleida in 2003 and spent his career in the LEB — Tarragona, Breogán, Lleida, Valladolid, Cáceres, Andorra, Palencia, Burgos and Palma. By 2018 he was the ninth most-capped player in LEB Or history.',
39: '<span class="tag">NOW</span><span class="val">A career in the ACB and the LEB<em>Last known club: Palma Air Europa</em></span>',
40: 'Tercera FEB champion 2026',
41: 'Ángel David Mejía Beriguete. Point guard, 1.79 m, born April 2000. He joined the Escoleta at four. He has played for Villarrobledo, Martinenc, Santfeliuenc and La Roda; in June 2026 he was promoted to Segunda FEB with Badajoz, and the first thing he did was go back and find Julio.',
42: '<span class="tag">NOW</span><span class="val">Baloncesto Ciudad de Badajoz · Segunda FEB<em>Vítaly La Mar BCBadajoz · promoted in June 2026</em></span>',
43: 'Shooting guard · Spar Girona · LF Endesa',
44: 'Barcelona, 1997. A 1.82 m guard and captain of Spar Girona in the Liga Femenina Endesa. She started playing here and developed at CB Femení Sant Adrià. She debuted in the top flight in 2016-17 with Uni Girona; then Quesos El Pastor, Ensino and Barça CBS, with whom she won promotion to the Liga Femenina. In 2023-24 she returned to Fontajau.',
45: '<span class="tag">NOW</span><span class="val">Spar Girona · Liga Femenina Endesa<em>Captain · re-signed in July 2026 for 26-27</em></span>',
46: 'DCA Academy · player development',
47: 'One of the most followed voices in Spanish-language youth basketball. He runs <strong>DCA Academy</strong>, a development academy in Les Franqueses del Vallès, with an online academy and camps in Girona and Tarragona. He has coached players such as Marc Gasol, Thomas Heurtel and Anna Cruz, has worked with more than a thousand families and has written a book about what lies beyond the result.',
48: '<span class="tag">NOW</span><span class="val">Director of DCA Academy<em>Player development · Les Franqueses del Vallès</em></span>',
49: 'FC Barcelona youth system',
50: 'Born in 2005. He passed through this court before wearing blaugrana: with Barça he played the Spanish club championship and the ANGT EuroLeague. Then Liga EBA with Castelldefels and Tercera FEB with SD Espanyol, Cuarte de Huerva and UE Sant Cugat.',
51: '<span class="tag">NOW</span><span class="val">UE Sant Cugat · Tercera FEB<em>Since November 2025, per his FEB record</em></span>',
52: 'No photo:<br>still a minor',
53: 'FC Barcelona · Catalan national team',
54: 'Born in 2009. From the Escoleta to Barça’s youth system, where he played the Spanish under-14 club championship. He has also played for the Catalan national team. We do not publish his picture: he is still a minor.',
55: '<span class="tag">NOW</span><span class="val">FC Barcelona youth system<em>Junior category · FEB record</em></span>',
56: '3x3 national team',
57: 'Spain · 3x3 FCBQ PRO',
58: 'He started here too. Today he competes in the 3x3 circuit wearing the Spain shirt.',
59: '<span class="tag">NOW</span><span class="val">To be confirmed<em>3x3 circuit with the Spanish national team</em></span>',
60: 'No photo:<br>still minors',
61: 'FC Barcelona · Joventut Badalona',
62: 'Twins, born in 2009. Both came out of the Escoleta: Oriol is still in FC Barcelona’s youth system and Marc now plays for Joventut Badalona. We do not publish their picture: they are still minors and their career is theirs.',
63: '<span class="tag">NOW</span><span class="val">FC Barcelona and Joventut Badalona<em>Junior category · 17 years old</em></span>',
64: 'From a court in El Clot<br>to the Liga Femenina Endesa.',
65: '<strong>Ainhoa López</strong> started playing here. Today she is captain of Spar Girona and plays in the same league Javier Torralba coaches in.',
66: 'In the girls’ pre-mini team of 2004-05 she was seven years old. Eleven years later she was debuting in the top tier of Spanish women’s basketball.',
67: 'Her career, though, is not told through games alone. In February 2022, playing for Barça CBS, she announced she had Hodgkin lymphoma, and she beat it. In September 2024 she spent twenty-five days in hospital with severe haemolytic anaemia and needed twelve transfusions. She came back to the court both times. Today she is an ambassador for blood donation and carries one phrase as a banner: <strong>“Living is urgent”</strong>.',
68: 'Hers is the name that best explains why a basketball school exists: because you never know who is standing in front of you.',
69: '<b>Girls’ pre-mini, 2004-05.</b> Seven years old. Her first season at the club.',
70: '<b>Formed at the Barna.</b> Before Sant Adrià, Barça CBS and Fontajau.',
71: '<b>Playing.</b> Girls’ youth basketball at the Barna, more than twenty years ago.',
72: '<b>The Escoleta.</b> Somewhere among these children was a future LF Endesa captain.',
73: '<b>One photo, two careers.</b> This 1990s team contains both Javier Torralba and Roger Fornas. Neither of them knew it yet.',
74: 'Nineteen years<br>later',
75: 'In February 2007 a six-year-old had his photo taken with the club mascot. In June 2026 the same young man lifted a trophy in Badajoz.',
76: '<b>24 · 02 · 2007.</b> Grup Barna Basketball School.',
77: '<b>June 2026.</b> Champion of the Tercera FEB final phase. Promotion to Segunda FEB.',
78: '<b>The reunion.</b> The coach who welcomed him at four and the player who has just gone up a division. Some stories define what the Barna is.',
79: '<b>“Hemos vuelto”.</b> Tercera FEB final phase 2025/26, Badajoz.',
80: 'The ones<br>coming now',
81: 'Marta joined the Escoleta as a little girl. This year she turned eighteen and is leaving home. The Escoleta said goodbye the way a family does.',
82: '<b>The little ones watch.</b> What they see today is what they will want to be tomorrow.',
83: '<b>Eighteen.</b> The whole Escoleta, with Julio in the middle.',
84: 'And another intake is already coming up behind her. There are Escoleta graduates playing in <strong>FC Barcelona’s</strong> youth system and on the <strong>Spanish national 3x3 circuit</strong>. Some are still minors, which is why we do not put a face or a name to them here: their career is theirs, not our marketing.',
85: 'The Escoleta,<br>today',
86: 'The Escoleta is founded',
87: 'Years old · Escoleta',
88: 'Families at the club',
89: 'Girls and boys',
90: '<b>Cistella Petita day · 13.06.2026.</b> Second edition. Small great players.',
91: '<b>21.05.2026.</b> Meet-up with the Nacho Solozabal school.',
92: '<b>14.02.2026.</b> A visit from the Mayor of Barcelona, Mr Collboni, and the Sports Councillor, Mr Escudé.',
93: 'We do not sign talent here.<br>We raise it.',
94: 'Who trains<br>at La Nau',
95: 'The same court where a four-year-old learns to dribble is where professional players train in the off-season.',
96: '<strong>Time Chamber</strong>, a club partner led by <strong>Iandrey Panisa</strong>, works out of <strong>La Nau</strong>. Internationals such as <strong>Willy Hernangómez</strong> — a European champion with Spain and an NBA and EuroLeague player — have trained here.',
97: 'This is not an anecdote for Instagram. It is what lets a child from the Escoleta walk through the door and see, with their own eyes, what really committing to this looks like.',
98: 'The same court.<br>The four-year-old and the international.',
99: 'The next one<br>to come out of here<br>cannot dribble yet',
100: 'The CB Grup Barna Escoleta is for girls and boys aged 4 to 8. We are not looking for the best: we are looking for children who want to come back next week. The rest we have seen happen a few times already.',
101: None,  # es manté el SVG + s'hi canvia el text solt
102: 'If you are deciding',
103: 'What does a four-year-old learn playing basketball?',
104: 'At what age can a child start playing basketball?',
105: 'How to choose a basketball school in Barcelona',
106: 'Summer basketball camp',
107: '© CB Grup Barna · La Nau del Clot · Sant Martí, Barcelona',
108: 'Open Days · Try a session',
109: 'I want to try a session',
}
EN_WA_TEXT = ' I want information'  # bloc 101, text després del SVG

# Missatge prellistat de WhatsApp, per idioma
WA_MSG = {
    'ca': "Hola! Vull informació de les Portes Obertes de l'Escoleta del CB Grup Barna",
    'es': "¡Hola! Quiero información de las Puertas Abiertas de la Escoleta del CB Grup Barna",
    'en': "Hello! I'd like information about the Open Days at the CB Grup Barna basketball school",
}

# Text alternatiu de les imatges (accessibilitat + cerca d'imatges per idioma)
ALT = {
'Equip mini del Grup Barna als anys 90 en una pista de pati, amb Julio Torralba': (
    'Equipo mini del Grup Barna en los años 90 en una pista de patio, con Julio Torralba',
    'Grup Barna mini team in the 1990s on a schoolyard court, with Julio Torralba'),
'Partit de bàsquet en una pista de pati als anys 90': (
    'Partido de baloncesto en una pista de patio en los años 90',
    'A basketball game on a schoolyard court in the 1990s'),
'Nens del Grup Barna celebrant amb un trofeu als anys 90': (
    'Niños del Grup Barna celebrando con un trofeo en los años 90',
    'Grup Barna children celebrating with a trophy in the 1990s'),
'Equip del Grup Barna amb medalles i Julio Torralba': (
    'Equipo del Grup Barna con medallas y Julio Torralba',
    'A Grup Barna team with medals, alongside Julio Torralba'),
'Llicència federativa de la Federació Catalana de Basquetbol de Xavier Torralba Liso, Grup Barna, temporada 1993-94': (
    'Licencia federativa de la Federación Catalana de Baloncesto de Xavier Torralba Liso, Grup Barna, temporada 1993-94',
    'Catalan Basketball Federation licence for Xavier Torralba Liso, Grup Barna, 1993-94 season'),
'Javier Torralba de nen, foto de la seva primera llicència federativa': (
    'Javier Torralba de niño, foto de su primera licencia federativa',
    'Javier Torralba as a child, in the photo from his first federation licence'),
'Roger Fornas, pivot professional': (
    'Roger Fornas, pívot profesional',
    'Roger Fornas, professional centre'),
'David Mejía amb el trofeu de campió de la Tercera FEB': (
    'David Mejía con el trofeo de campeón de la Tercera FEB',
    'David Mejía with the Tercera FEB champions’ trophy'),
"Ainhoa López, entrenadora de l'Escoleta del CB Grup Barna": (
    'Ainhoa López, entrenadora de la Escoleta del CB Grup Barna',
    'Ainhoa López, coach at the CB Grup Barna basketball school'),
'Darío Naharro, entrenador i divulgador de bàsquet formatiu': (
    'Darío Naharro, entrenador y divulgador de baloncesto formativo',
    'Darío Naharro, coach and youth-basketball educator'),
'Daniel Iruela, jugador format al FC Barcelona': (
    'Daniel Iruela, jugador formado en el FC Barcelona',
    'Daniel Iruela, a player developed at FC Barcelona'),
"Exjugador de l'Escoleta amb la samarreta de la selecció espanyola de 3x3": (
    'Exjugador de la Escoleta con la camiseta de la selección española de 3x3',
    'A former Escoleta player in the Spain 3x3 national team shirt'),
'Equip pre-mini femení del CB Grup Barna, temporada 2004-2005': (
    'Equipo pre-mini femenino del CB Grup Barna, temporada 2004-2005',
    'CB Grup Barna girls’ pre-mini team, 2004-2005 season'),
'Equip femení de formació del CB Grup Barna': (
    'Equipo femenino de formación del CB Grup Barna',
    'A CB Grup Barna girls’ youth team'),
'Partit de bàsquet femení de formació del CB Grup Barna': (
    'Partido de baloncesto femenino de formación del CB Grup Barna',
    'A CB Grup Barna girls’ youth basketball game'),
"L'Escoleta del CB Grup Barna al complet": (
    'La Escoleta del CB Grup Barna al completo',
    'The full CB Grup Barna Escoleta'),
'Equip mini del Grup Barna dels anys 90': (
    'Equipo mini del Grup Barna de los años 90',
    'A Grup Barna mini team from the 1990s'),
"David Mejía de nen a l'Escola de Bàsquet Grup Barna, febrer de 2007": (
    'David Mejía de niño en la Escuela de Baloncesto Grup Barna, febrero de 2007',
    'David Mejía as a child at the Grup Barna basketball school, February 2007'),
'David Mejía amb el trofeu de campió de la Fase Final Tercera FEB 2025/26': (
    'David Mejía con el trofeo de campeón de la Fase Final Tercera FEB 2025/26',
    'David Mejía with the 2025/26 Tercera FEB final-phase champions’ trophy'),
'Julio Torralba i David Mejía retrobant-se': (
    'Julio Torralba y David Mejía reencontrándose',
    'Julio Torralba and David Mejía meeting again'),
'Celebració del campionat de la Fase Final Tercera FEB 2025/26': (
    'Celebración del campeonato de la Fase Final Tercera FEB 2025/26',
    'Celebrating the 2025/26 Tercera FEB final-phase title'),
"Els nens i nenes de l'Escoleta asseguts a la pista escoltant": (
    'Los niños y niñas de la Escoleta sentados en la pista escuchando',
    'The Escoleta children sitting on the court, listening'),
"L'Escoleta felicitant la Marta pels seus 18 anys": (
    'La Escoleta felicitando a Marta por sus 18 años',
    'The Escoleta wishing Marta a happy 18th birthday'),
'Dia de la Cistella Petita 2026 al CB Grup Barna': (
    'Día de la Cistella Petita 2026 en el CB Grup Barna',
    'Cistella Petita day 2026 at CB Grup Barna'),
"Trobada de l'Escola Grup Barna amb l'Escola Nacho Solozabal": (
    'Encuentro de la Escuela Grup Barna con la Escuela Nacho Solozabal',
    'A meet-up between the Grup Barna school and the Nacho Solozabal school'),
"Visita de l'alcalde de Barcelona Jaume Collboni al CB Grup Barna": (
    'Visita del alcalde de Barcelona Jaume Collboni al CB Grup Barna',
    'A visit from the Mayor of Barcelona, Jaume Collboni, to CB Grup Barna'),
}

# ---------------------------------------------------------------- metadades
META = {
    'ca': {
        'title': 'Escola de bàsquet a Barcelona (4-8 anys) · Escoleta CB Grup Barna',
        'desc': "Escoleta del CB Grup Barna (4 a 8 anys) al Clot, Barcelona. Portes Obertes: vine a provar un entrenament sense compromís. 60 anys formant jugadors i jugadores al barri.",
        'ogtitle': 'Escola de bàsquet a Barcelona · Escoleta CB Grup Barna (4 a 8 anys)',
        'ogdesc': "Escola de bàsquet per a nens i nenes de 4 a 8 anys al Clot, Barcelona. D'aquesta pista han sortit jugadors d'ACB, de Lliga Femenina Endesa i del Barça.",
        'kw': 'escola de bàsquet Barcelona, escoleta bàsquet, bàsquet nens 4 anys, escola bàsquet Clot, bàsquet Sant Martí',
        'faqtitle': "Preguntes freqüents sobre l'Escoleta",
    },
    'es': {
        'title': 'Escuela de baloncesto en Barcelona (4-8 años) · Escoleta CB Grup Barna',
        'desc': 'Escuela de baloncesto del CB Grup Barna (4 a 8 años) en El Clot, Barcelona. Puertas Abiertas: ven a probar un entrenamiento sin compromiso. 60 años formando en el barrio.',
        'ogtitle': 'Escuela de baloncesto en Barcelona · Escoleta CB Grup Barna (4 a 8 años)',
        'ogdesc': 'Escuela de baloncesto para niños y niñas de 4 a 8 años en El Clot, Barcelona. De esta pista han salido jugadores de ACB, de Liga Femenina Endesa y del Barça.',
        'kw': 'escuela de baloncesto Barcelona, baloncesto niños 4 años, escuela basket Barcelona, baloncesto El Clot, baloncesto Sant Martí',
        'faqtitle': 'Preguntas frecuentes sobre la Escoleta',
    },
    'en': {
        'title': 'Basketball school in Barcelona (ages 4-8) · CB Grup Barna',
        'desc': 'Basketball school for children aged 4 to 8 in El Clot, Barcelona. Open Days: come and try a session with no commitment. Sixty years coaching in the neighbourhood.',
        'ogtitle': 'Basketball school in Barcelona · CB Grup Barna Escoleta (ages 4-8)',
        'ogdesc': 'Basketball school for girls and boys aged 4 to 8 in El Clot, Barcelona. Players from this court have reached the ACB, the Liga Femenina Endesa and FC Barcelona.',
        'kw': 'basketball school Barcelona, basketball for kids Barcelona, children basketball Barcelona, basketball classes Barcelona, basketball El Clot',
        'faqtitle': 'Frequently asked questions about the Escoleta',
    },
}

FAQ = {
    'ca': [
        ("Quina és l'escola de bàsquet del CB Grup Barna?",
         "L'Escoleta és l'escola de bàsquet del CB Grup Barna per a nens i nenes de 4 a 8 anys, al barri del Clot, Districte de Sant Martí de Barcelona. Funciona amb equips mixtos i tres grups per edat."),
        ("Qui dirigeix l'Escoleta del CB Grup Barna?",
         "L'Escoleta la dirigeix Julio Torralba. Es pot contactar amb ell per telèfon o WhatsApp al 646 205 526."),
        ("A partir de quina edat es pot començar a jugar a bàsquet al Barna?",
         "Des dels 4 anys. L'Escoleta acull nens i nenes de 4 a 8 anys. A partir dels 8 i a mida que estan preparats, passen als equips federats del club (premini, mini i la resta de categories)."),
        ("Es pot provar un entrenament abans d'apuntar-s'hi?",
         "Sí. El primer entrenament és de prova i sense compromís. Cal escriure o trucar a Julio Torralba al 646 205 526 per reservar dia."),
        ("On entrena l'Escoleta del CB Grup Barna?",
         "Al barri del Clot, al Districte de Sant Martí de Barcelona. La Nau del Clot és el punt esportiu principal del club."),
    ],
    'es': [
        ("¿Cuál es la escuela de baloncesto del CB Grup Barna?",
         "La Escoleta es la escuela de baloncesto del CB Grup Barna para niños y niñas de 4 a 8 años, en el barrio de El Clot, Distrito de Sant Martí de Barcelona. Funciona con equipos mixtos y tres grupos por edad."),
        ("¿Quién dirige la Escoleta del CB Grup Barna?",
         "La Escoleta la dirige Julio Torralba. Se puede contactar con él por teléfono o WhatsApp en el 646 205 526."),
        ("¿A partir de qué edad se puede empezar a jugar a baloncesto en el Barna?",
         "Desde los 4 años. La Escoleta acoge a niños y niñas de 4 a 8 años. A partir de los 8, y a medida que están preparados, pasan a los equipos federados del club (premini, mini y el resto de categorías)."),
        ("¿Se puede probar un entrenamiento antes de apuntarse?",
         "Sí. El primer entrenamiento es de prueba y sin compromiso. Hay que escribir o llamar a Julio Torralba al 646 205 526 para reservar día."),
        ("¿Dónde entrena la Escoleta del CB Grup Barna?",
         "En el barrio de El Clot, en el Distrito de Sant Martí de Barcelona. La Nau del Clot es el punto deportivo principal del club."),
    ],
    'en': [
        ("What is the CB Grup Barna basketball school?",
         "The Escoleta is CB Grup Barna's basketball school for girls and boys aged 4 to 8, in the El Clot neighbourhood of the Sant Martí district of Barcelona. It runs with mixed teams and three groups by age."),
        ("Who runs the CB Grup Barna Escoleta?",
         "The Escoleta is run by Julio Torralba. You can reach him by phone or WhatsApp on +34 646 205 526."),
        ("From what age can a child start playing basketball at the Barna?",
         "From the age of 4. The Escoleta takes girls and boys aged 4 to 8. From 8, and as they are ready, they move up to the club's federated teams (premini, mini and the rest of the age groups)."),
        ("Can we try a session before signing up?",
         "Yes. The first session is a trial with no commitment. Write or call Julio Torralba on +34 646 205 526 to book a day."),
        ("Where does the CB Grup Barna Escoleta train?",
         "In the El Clot neighbourhood, in the Sant Martí district of Barcelona. La Nau del Clot is the club's main sports venue."),
    ],
}

SERVICE_DESC = {
    'ca': "Escola de bàsquet a Barcelona per a nens i nenes de 4 a 8 anys. L'Escoleta del CB Grup Barna, al barri del Clot (Districte de Sant Martí), funciona amb equips mixtos, tres grups per edat i trobades amb altres clubs de la ciutat i la província. D'aquesta mateixa pista han sortit jugadors i jugadores que han arribat a l'ACB, a la Lliga Femenina Endesa i al FC Barcelona. La dirigeix Julio Torralba.",
    'es': "Escuela de baloncesto en Barcelona para niños y niñas de 4 a 8 años. La Escoleta del CB Grup Barna, en el barrio de El Clot (Distrito de Sant Martí), funciona con equipos mixtos, tres grupos por edad y encuentros con otros clubes de la ciudad y la provincia. De esta misma pista han salido jugadores y jugadoras que han llegado a la ACB, a la Liga Femenina Endesa y al FC Barcelona. La dirige Julio Torralba.",
    'en': "Basketball school in Barcelona for girls and boys aged 4 to 8. The CB Grup Barna Escoleta, in the El Clot neighbourhood (Sant Martí district), runs with mixed teams, three groups by age and meet-ups with other clubs across the city and province. Players from this same court have reached the ACB, the Liga Femenina Endesa and FC Barcelona. It is run by Julio Torralba.",
}
SERVICE_NAME = {
    'ca': 'Escola de bàsquet · Escoleta CB Grup Barna',
    'es': 'Escuela de baloncesto · Escoleta CB Grup Barna',
    'en': 'Basketball school · CB Grup Barna Escoleta',
}
CRUMB = {'ca': 'Escola de bàsquet · Escoleta', 'es': 'Escuela de baloncesto · Escoleta',
         'en': 'Basketball school · Escoleta'}
TRIAL = {
    'ca': 'Primer entrenament de prova sense compromís.',
    'es': 'Primer entrenamiento de prueba sin compromiso.',
    'en': 'First session is a free trial with no commitment.',
}
SEG_TAGS = {  # etiquetes dels enllaços de context
    'ca': ['Observatori Barna', 'Guia per a famílies', 'Guia per a famílies', 'El Clot, Barcelona'],
    'es': ['Observatori Barna', 'Guía para familias', 'Guía para familias', 'El Clot, Barcelona'],
    'en': ['Observatori Barna', 'Family guide', 'Family guide', 'El Clot, Barcelona'],
}
SEG_HEAD = {'ca': 'Si esteu decidint', 'es': 'Si estáis decidiendo', 'en': 'If you are deciding'}


def jsonld(lang):
    u = URLS[lang]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": ["SportsClub", "SportsOrganization", "LocalBusiness"],
                "@id": f"{BASE}/#club",
                "name": "CB Grup Barna",
                "alternateName": ["Club Bàsquet Grup Barna", "Club Baloncesto Grupo Barna", "Grup Barna"],
                "url": BASE,
                "logo": f"{BASE}/logo.png",
                "foundingDate": "1965",
                "address": {"@type": "PostalAddress", "streetAddress": "La Nau del Clot",
                            "addressLocality": "Barcelona", "addressRegion": "Catalunya",
                            "postalCode": "08018", "addressCountry": "ES"},
                "geo": {"@type": "GeoCoordinates", "latitude": 41.4036, "longitude": 2.1878},
                "email": "info@cbgrupbarna.com",
                "telephone": "+34698425153",
                "sameAs": ["https://www.instagram.com/cbgrupbarna/",
                           "https://www.tiktok.com/@cbgrupbarna",
                           "https://www.cbgrupbarna.com",
                           "https://www.basquetcatala.cat/club/24"],
            },
            {"@type": "WebSite", "@id": f"{BASE}/#website", "url": BASE, "name": "CB Grup Barna",
             "publisher": {"@id": f"{BASE}/#club"}},
            {"@type": "Person", "@id": f"{BASE}/#julio-torralba", "name": "Julio Torralba",
             "jobTitle": {"ca": "Responsable de l'Escoleta de bàsquet del CB Grup Barna",
                          "es": "Responsable de la Escoleta de baloncesto del CB Grup Barna",
                          "en": "Head of the CB Grup Barna basketball school"}[lang],
             "worksFor": {"@id": f"{BASE}/#club"}, "telephone": "+34646205526",
             "knowsAbout": ["Bàsquet base", "Iniciació esportiva", "Escola de bàsquet", "Minibàsquet"]},
            {
                "@type": "Service",
                "@id": f"{u}#escoleta",
                "name": SERVICE_NAME[lang],
                "description": SERVICE_DESC[lang],
                "serviceType": {"ca": "Escola de bàsquet base", "es": "Escuela de baloncesto base",
                                "en": "Youth basketball school"}[lang],
                "url": u,
                "inLanguage": f"{lang}-ES" if lang != 'en' else "en",
                "provider": {"@id": f"{BASE}/#club"},
                "employee": {"@id": f"{BASE}/#julio-torralba"},
                "areaServed": [{"@type": "City", "name": "Barcelona"},
                               {"@type": "AdministrativeArea", "name": "Província de Barcelona"}],
                "audience": {"@type": "PeopleAudience", "suggestedMinAge": 4, "suggestedMaxAge": 8},
                "availableChannel": {"@type": "ServiceChannel", "serviceUrl": u,
                                     "servicePhone": {"@type": "ContactPoint", "telephone": "+34646205526",
                                                      "contactType": "Escoleta", "name": "Julio Torralba",
                                                      "availableLanguage": ["ca", "es", "en"]}},
                "offers": {"@type": "Offer", "description": TRIAL[lang],
                           "availability": "https://schema.org/InStock"},
            },
            {"@type": "WebPage", "@id": f"{u}#webpage", "url": u, "name": META[lang]['title'],
             "inLanguage": f"{lang}-ES" if lang != 'en' else "en",
             "about": {"@id": f"{u}#escoleta"}, "isPartOf": {"@id": f"{BASE}/#website"},
             "translationOfWork": None if lang == 'ca' else {"@id": f"{URLS['ca']}#webpage"}},
            {"@type": "FAQPage", "@id": f"{u}#faq",
             "inLanguage": f"{lang}-ES" if lang != 'en' else "en",
             "mainEntity": [{"@type": "Question", "name": q,
                             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[lang]]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "CB Grup Barna", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": CRUMB[lang], "item": u}]},
        ],
    }


def strip_nulls(o):
    if isinstance(o, dict):
        return {k: strip_nulls(v) for k, v in o.items() if v is not None}
    if isinstance(o, list):
        return [strip_nulls(v) for v in o]
    return o


def build(lang):
    doc = LH.parse(SRC).getroot()

    # 1 · anglès: sobreescriu el contingut dels blocs catalans
    if lang == 'en':
        for i, el in enumerate(doc.xpath('//*[@data-lang="ca"]')):
            rep = EN.get(i)
            if rep is None:
                continue
            for c in list(el):
                el.remove(c)
            el.text = None
            frag = LH.fragment_fromstring(f'<x>{rep}</x>')
            el.text = frag.text
            for c in frag:
                el.append(c)
        # bloc 101: conserva l'SVG i canvia només el text
        for a in doc.xpath('//a[svg]'):
            if a.getchildren():
                a.getchildren()[-1].tail = EN_WA_TEXT

    # 2 · esborra els blocs dels altres idiomes
    keep = 'ca' if lang in ('ca', 'en') else 'es'
    for el in doc.xpath(f'//*[@data-lang and @data-lang!="{keep}"]'):
        el.getparent().remove(el)
    for el in doc.xpath('//*[@data-lang]'):
        del el.attrib['data-lang']

    # 3 · si el <h1> real s'ha esborrat (versió ES), promou .h1-alt a <h1>
    if not doc.xpath('//h1'):
        alt = doc.xpath('//*[contains(@class,"h1-alt")]')
        if alt:
            alt[0].tag = 'h1'
            for attr in ('role', 'aria-level'):
                alt[0].attrib.pop(attr, None)
    else:
        for el in doc.xpath('//*[contains(@class,"h1-alt")]'):
            el.getparent().remove(el)

    # 4 · selector d'idioma: enllaços reals, no JS
    for bar in doc.xpath('//*[contains(@class,"langs")]'):
        for c in list(bar):
            bar.remove(c)
        bar.text = None
        for code in ('ca', 'es', 'en'):
            a = etree.SubElement(bar, 'a')
            a.text = LANG_NAME[code]
            a.set('href', URLS[code].replace(BASE, '') or '/')
            a.set('hreflang', code)
            if code == lang:
                a.set('aria-current', 'true')

    # 5 · fora el JS i el CSS del toggle
    for sc in doc.xpath('//script[not(@src)]'):
        if 'cbgb-lang' in (sc.text or ''):
            sc.getparent().remove(sc)
    for st in doc.xpath('//style'):
        if st.text:
            st.text = re.sub(
                r'body\[data-active="ca"\][^}]*\}', '', st.text)
            st.text = st.text.replace(
                '.langs button', '.langs a').replace(
                '.langs a[aria-pressed="true"]', '.langs a[aria-current="true"]')
    for b in doc.xpath('//body'):
        b.attrib.pop('data-active', None)
    # l'analítica llegia data-active, que ja no existeix: ara llegeix <html lang>
    for sc in doc.xpath('//script[not(@src)]'):
        if sc.text and 'data-active' in sc.text:
            sc.text = sc.text.replace(
                "document.body.getAttribute('data-active')||'ca'",
                "document.documentElement.lang||'ca'")

    # 5b · alt de les imatges i missatge de WhatsApp en l'idioma de la pàgina
    if lang != 'ca':
        idx = 0 if lang == 'es' else 1
        for img in doc.xpath('//img[@alt]'):
            tr = ALT.get(img.get('alt'))
            if tr:
                img.set('alt', tr[idx])
    from urllib.parse import quote
    for a in doc.xpath('//a[contains(@href,"wa.me")]'):
        href = a.get('href').split('?')[0]
        a.set('href', f'{href}?text={quote(WA_MSG[lang])}')

    # 6 · etiquetes dels enllaços de context
    for i, el in enumerate(doc.xpath('//*[contains(@class,"seg-s")]')):
        if i < len(SEG_TAGS[lang]):
            el.text = SEG_TAGS[lang][i]
    for el in doc.xpath('//section[contains(@class,"segueix")]//h2'):
        el.text = SEG_HEAD[lang]

    # 7 · FAQ visible (a l'origen només existeix en català)
    for sec in doc.xpath('//section[contains(@class,"faq-sec")]'):
        wrap = sec.xpath('.//div[contains(@class,"wrap")]')[0]
        for c in list(wrap):
            wrap.remove(c)
        h2 = etree.SubElement(wrap, 'h2')
        h2.set('id', 'faq-escoleta')
        h2.text = META[lang]['faqtitle']
        for q, a in FAQ[lang]:
            d = etree.SubElement(wrap, 'details')
            d.set('class', 'faq-q')
            s = etree.SubElement(d, 'summary')
            s.text = q
            p = etree.SubElement(d, 'p')
            p.text = a

    # 8 · <head>
    head = doc.xpath('//head')[0]
    doc.set('lang', lang)
    for xp in ('//title', '//meta[@name="description"]', '//meta[@name="keywords"]',
               '//link[@rel="canonical"]', '//link[@rel="alternate"]',
               '//meta[starts-with(@property,"og:")]', '//meta[starts-with(@name,"twitter:")]'):
        for el in doc.xpath(xp):
            el.getparent().remove(el)

    def meta_el(**kw):
        m = etree.SubElement(head, 'meta')
        for k, v in kw.items():
            m.set(k.replace('_', ':'), v)

    t = etree.SubElement(head, 'title')
    t.text = META[lang]['title']
    meta_el(name='description', content=META[lang]['desc'])
    meta_el(name='keywords', content=META[lang]['kw'])
    meta_el(name='robots', content='index,follow,max-image-preview:large,max-snippet:-1')
    c = etree.SubElement(head, 'link'); c.set('rel', 'canonical'); c.set('href', URLS[lang])
    for code in ('ca', 'es', 'en'):
        l = etree.SubElement(head, 'link')
        l.set('rel', 'alternate'); l.set('hreflang', code); l.set('href', URLS[code])
    x = etree.SubElement(head, 'link')
    x.set('rel', 'alternate'); x.set('hreflang', 'x-default'); x.set('href', URLS['ca'])
    meta_el(property='og:type', content='website')
    meta_el(property='og:site_name', content='CB Grup Barna')
    meta_el(property='og:title', content=META[lang]['ogtitle'])
    meta_el(property='og:description', content=META[lang]['ogdesc'])
    meta_el(property='og:url', content=URLS[lang])
    meta_el(property='og:image', content=f'{BASE}/escoleta/img/equip-anys90-julio.webp')
    meta_el(property='og:image:alt', content='Equip mini del Grup Barna als anys 90, amb Julio Torralba')
    meta_el(property='og:locale', content=OG_LOCALE[lang])
    for code in ('ca', 'es', 'en'):
        if code != lang:
            meta_el(property='og:locale:alternate', content=OG_LOCALE[code])
    meta_el(name='twitter:card', content='summary_large_image')
    meta_el(name='twitter:site', content='@cbgrupbarna')

    # 9 · JSON-LD
    for sc in doc.xpath('//script[@type="application/ld+json"]'):
        sc.getparent().remove(sc)
    sc = etree.SubElement(head, 'script')
    sc.set('type', 'application/ld+json')
    sc.text = json.dumps(strip_nulls(jsonld(lang)), ensure_ascii=False, indent=2)

    # 10 · rutes absolutes (les subcarpetes /es/ i /en/ no poden usar rutes relatives)
    if lang != 'ca':
        for el in doc.xpath('//img[@src] | //source[@srcset] | //link[@href]'):
            for attr in ('src', 'srcset', 'href'):
                v = el.get(attr)
                if v and not v.startswith(('http', '/', '#', 'data:', 'mailto:', 'tel:')):
                    el.set(attr, '/escoleta/' + v)
        # …i també les url() de dins del CSS (les @font-face són relatives)
        for st in doc.xpath('//style'):
            if st.text:
                st.text = re.sub(r'url\((?![\'"]?(?:https?:|/|data:))[\'"]?([^)\'"]+)[\'"]?\)',
                                 r'url(/escoleta/\1)', st.text)

    out = OUT[lang]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    html = '<!DOCTYPE html>\n' + LH.tostring(doc, encoding='unicode', pretty_print=False)
    open(out, 'w', encoding='utf-8').write(html)
    return out


if __name__ == '__main__':
    for lg in ('ca', 'es', 'en'):
        print('escrit:', build(lg))
