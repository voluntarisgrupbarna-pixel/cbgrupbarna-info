# Portes obertes del 19 de setembre · posicionament SEO i GEO

Document de treball de màrqueting (no és una pàgina publicada). Recull el
diagnòstic, les paraules clau del bloc **portes obertes / nenes 2018**, a quina
pàgina ha de rankejar cadascuna, i què queda pendent fora del web.

*Escrit l'11/09/2026, a vuit dies de l'esdeveniment.*

---

## 0. Què s'està promocionant, exactament

**Dissabte 19 de setembre de 2026, de 9.00 a 10.30 h, a La Nau del Clot**
(carrer de la Llacuna, 170-172, 08018 Barcelona), dues coses alhora:

1. **Portes obertes de l'Escoleta** — nens i nenes de 4 a 8 anys, entrenament
   de prova gratuït, 50 places per torn, amb reserva prèvia.
2. **Proves per a nenes nascudes el 2018** — l'equip ja existeix i busca
   incorporacions. Mateix dia, mateix torn, mateix lloc.

Hi ha un segon dissabte, el **26 de setembre**, amb el mateix horari. El 19 és
el que mana en tota la comunicació: és el primer i el que té la data a tocar.

Aquestes dades són la matèria primera de tot el que hi ha a sota. Una IA només
pot citar el que pot extreure, i només pot extreure el que està escrit de forma
literal, curta i al mateix lloc que la pregunta.

---

## 1. Diagnòstic: set forats trobats al web (11/09/2026)

El web del club està ben fet i té una infraestructura d'SEO poc habitual en un
club de barri (`llms.txt`, `hreflang` als tres idiomes, FAQ amb font única a
`i18n/faq.yml`, JSON-LD per tipus de pàgina). Els problemes no són de qualitat:
són de **col·locació**.

| # | Forat | Per què importa |
|---|---|---|
| 1 | **`/portes-obertes/` no té cap `Event` al JSON-LD.** Només `WebPage`, `BreadcrumbList` i `FAQPage`. | És *la* pàgina de l'esdeveniment i la que té el formulari de reserva, i és l'única que no és elegible per als resultats enriquits d'esdeveniments de Google. Sense `Event` no surt al mòdul «Esdeveniments a prop». |
| 2 | **L'únic `Event` del lloc és a l'article del blog**, i declara `startDate` 19/09 09:00 amb `endDate` 26/09 10:30. | Google ho llegeix com **un sol esdeveniment de set dies seguits**, no com dos dissabtes de 90 minuts. Un esdeveniment que dura una setmana no entra als resultats d'esdeveniments d'un dia concret, que és exactament la cerca que volem guanyar. |
| 3 | **Aquell `Event` no porta `streetAddress` ni `geo`.** Només «Barcelona, 08018». | És el camp que fa servir Google per a «bàsquet per a nens a prop meu». El club té l'adreça i les coordenades ben posades a la portada: no s'estan reutilitzant on més falta fan. |
| 4 | **El `<title>` no porta la data.** Diu «Portes obertes de setembre». | Les famílies escriuen **«portes obertes 19 de setembre»**, «19 setembre bàsquet Barcelona». Si la data no és al títol ni a la descripció, la coincidència literal es perd. |
| 5 | **`/portes-obertes/` té `priority` 0.6 i `changefreq` monthly al `sitemap.xml`**, amb `lastmod` del 31/08. | És una pàgina de campanya a vuit dies de l'esdeveniment amb la prioritat d'una pàgina secundària i una data d'última modificació de fa dotze dies. |
| 6 | **Zero contingut sobre nenes del 2018 a tot el web.** Cap pàgina, cap FAQ, cap línia a `llms.txt`. | No es pot posicionar el que no existeix. Ara mateix, qui cerqui «equip de bàsquet nenes 2018 Barcelona» no té cap manera d'arribar al club. |
| 7 | **Cap landing ataca «bàsquet per a nenes».** El club té **vuit equips femenins federats** i paritat real de pressupost, i això només es llegeix a `/femeni/`, que és una pàgina de posicionament institucional, no de captació. | El millor actiu del club en aquest terreny no té cap porta d'entrada transaccional. `/femeni/` explica *per què*; faltava el *vine dissabte*. |

**El titular del diagnòstic:** no cal reescriure el web. Cal **posar
l'esdeveniment a la pàgina de l'esdeveniment**, partir-lo en dos dies de veritat,
i obrir una porta que ara no existeix per a les nenes del 2018.

---

## 2. Arquitectura: quina pàgina ataca què

Regla del club, ja aplicada al campus i que aquí es manté: **una intenció, una
pàgina**. Si dues pàgines ataquen la mateixa consulta es fan la competència i
cap de les dues puja.

| Pàgina | Rol | Consultes que ha de guanyar |
|---|---|---|
| `/portes-obertes/` · `/es/puertas-abiertas/` · `/en/open-days/` | **La pàgina de l'esdeveniment i de la reserva.** És on va l'`Event` i on acaba tot el trànsit | «portes obertes bàsquet Barcelona», «portes obertes 19 de setembre», «provar un entrenament de bàsquet», «puertas abiertas baloncesto Barcelona» |
| `/basquet-nenes-2018-barcelona/` · `/es/baloncesto-ninas-2018-barcelona/` · `/en/girls-basketball-2018-barcelona/` | **Landing de captació femenina** (nova). Una intenció pròpia i molt concreta: famílies de nenes de 8 anys | «bàsquet per a nenes Barcelona», «equip de bàsquet nenes 2018», «bàsquet nenes 8 anys», «baloncesto para niñas Barcelona», «club de baloncesto femenino base Barcelona» |
| `/escoleta/` · `/es/escoleta/` · `/en/basketball-school-barcelona/` | Producte: el curs sencer de 4 a 8 anys | «escola de bàsquet», «començar a jugar a bàsquet», horaris i quotes |
| `/femeni/` | Posicionament institucional del projecte femení | «bàsquet femení Barcelona», «paritat», «El Mètode Barna» |
| `/blog/portes-obertes-escoleta-setembre-2026/` (3 idiomes) | Article de campanya, ja publicat | cua llarga i preguntes de famílies |

**El que canvia respecte d'avui:** l'`Event` baixa del blog a
`/portes-obertes/` (i es parteix en dos), i neix la landing de nenes del 2018,
que fins ara no tenia cap pàgina.

---

## 3. Paraules clau · CATALÀ

**Esdeveniment i data (prioritat 1 — la campanya)**
portes obertes bàsquet Barcelona · portes obertes 19 de setembre · portes
obertes escoleta setembre · jornada de portes obertes bàsquet · provar un
entrenament de bàsquet Barcelona · entrenament de prova gratuït bàsquet ·
portes obertes club de bàsquet Clot

**Nenes 2018 (prioritat 1 — la landing nova)**
bàsquet per a nenes Barcelona · equip de bàsquet de nenes Barcelona · bàsquet
nenes 2018 · bàsquet nenes 8 anys · proves de bàsquet per a nenes · premini
femení Barcelona · club de bàsquet femení base Barcelona · on pot jugar a
bàsquet una nena de 8 anys

**Geogràfiques (prioritat 1 — són les que podem guanyar de veritat)**
bàsquet nenes Clot · bàsquet Sant Martí nenes · bàsquet Glòries · bàsquet
Poblenou nenes · bàsquet Camp de l'Arpa · club de bàsquet a prop de casa ·
extraescolar de bàsquet Clot · La Nau del Clot bàsquet

**Cua llarga i preguntes (prioritat 1 per a IA)**
a quina edat pot començar una nena a jugar a bàsquet · com apuntar la meva
filla a bàsquet a Barcelona · què cal portar el primer dia d'entrenament ·
quant costa apuntar-se a un club de bàsquet · cal experiència prèvia per
començar a jugar a bàsquet · hi ha equips només de nenes · què és el premini ·
es pot provar un entrenament abans d'apuntar-se

**Marca (prioritat 1, defensiva)**
portes obertes CB Grup Barna · Grup Barna escoleta · CB Grup Barna nenes ·
Escoleta Grup Barna · Grup Barna Clot

## 4. Palabras clave · CASTELLANO

**Evento y fecha**
puertas abiertas baloncesto Barcelona · puertas abiertas 19 de septiembre ·
jornada de puertas abiertas baloncesto · probar un entrenamiento de baloncesto
Barcelona · entrenamiento de prueba gratuito baloncesto · puertas abiertas club
de baloncesto El Clot

**Niñas 2018**
baloncesto para niñas Barcelona · equipo de baloncesto de niñas Barcelona ·
baloncesto niñas 2018 · baloncesto niñas 8 años · pruebas de baloncesto para
niñas · premini femenino Barcelona · club de baloncesto femenino base Barcelona
· dónde puede jugar a baloncesto una niña de 8 años

**Geográficas**
baloncesto niñas El Clot · baloncesto Sant Martí · baloncesto Poblenou ·
baloncesto Glorias · extraescolar de baloncesto Barcelona · club de baloncesto
cerca de mí

**Cola larga y preguntas**
a qué edad puede empezar una niña a jugar a baloncesto · cómo apuntar a mi hija
a baloncesto en Barcelona · qué hay que llevar el primer día · cuánto cuesta
apuntarse a un club de baloncesto · hace falta experiencia previa · hay equipos
solo de niñas · qué es el premini

**Marca**
puertas abiertas CB Grup Barna · Grup Barna escoleta · Grup Barna niñas

## 5. Keywords · ENGLISH (famílies internacionals del districte)

basketball for girls Barcelona · girls basketball team Barcelona · kids
basketball club Barcelona · basketball open day Barcelona · free basketball
trial Barcelona · basketball for 8 year olds Barcelona · basketball El Clot ·
join a basketball club Barcelona · where can my daughter play basketball in
Barcelona

---

## 6. GEO · què cal perquè una IA ens citi

**SEO** és sortir a una llista de deu blaus. **GEO** és ser la frase que
ChatGPT, Perplexity o l'AI Mode de Google **escriuen** quan algú pregunta «on
pot jugar a bàsquet la meva filla de 8 anys a Barcelona». Són dues feines
diferents i la segona té regles pròpies:

1. **Dades dures literals i juntes.** Una IA cita el que pot extreure sense
   deduir. Data, hora, adreça, edats, any de naixement, preu i contacte han
   d'estar escrits **en text pla, en una llista o taula, i a la mateixa pàgina
   que la pregunta**. Un preu que només es veu en una imatge del cartell no
   existeix.
2. **La pregunta, escrita tal com la fa la gent.** Els blocs de pregunta i
   resposta funcionen perquè la pregunta del web coincideix literalment amb la
   de l'usuari. «Quan són les portes obertes?» val més que «Calendari».
3. **Resposta autònoma en una frase.** La primera frase de cada resposta ha de
   tenir sentit fora de context, perquè és la que es copia: «Les portes obertes
   són el dissabte 19 de setembre de 2026, de 9.00 a 10.30 h, a La Nau del
   Clot» — no «Són aquest dissabte».
4. **`llms.txt`.** El club ja en té un, i és un avantatge real: és l'índex que
   una IA llegeix sense haver de navegar. Tot el que sigui campanya viva hi ha
   de ser, amb les dades dures, no només amb l'enllaç.
5. **Coherència d'entitat.** El nom, l'adreça i el telèfon han de dir exactament
   el mateix a totes les pàgines, al `llms.txt`, a la fitxa de Google i a
   Instagram. Una IA que troba dues adreces distintes es queda amb la
   incertesa i no cita cap de les dues.
6. **`Event` correcte.** És l'únic senyal estructurat que diu «això passa un dia
   concret». És el forat 1 i 2 del diagnòstic, i és el que més valor té dels
   set.

---

## 7. Fet en aquesta tanda

1. **`Event` a `/portes-obertes/`**, als tres idiomes, **partit en dos
   esdeveniments** (19 i 26) amb `startDate`/`endDate` reals de 90 minuts,
   `location` amb `streetAddress` i `geo`, `offers` a preu 0 i
   `organizer` lligat a `#club`.
2. **Landing nova de nenes del 2018** als tres idiomes, amb `Event`,
   `FAQPage`, `SportsTeam` i un bloc de dades dures en taula.
3. **Títols i descripcions** amb la data literal a `/portes-obertes/`.
4. **Bloc destacat del 19 de setembre** a `/portes-obertes/`, amb les dades
   dures abans del formulari.
5. **Preguntes noves a `i18n/faq.yml`** (la font única) i FAQ regenerada.
6. **`llms.txt`**: bloc de dades dures del 19 de setembre i de les nenes 2018.
7. **Enllaçat intern**: escoleta ↔ portes obertes ↔ landing de nenes ↔ femení.
8. **`sitemap.xml`** amb la prioritat de campanya i `lastmod` al dia.
9. **Avís de dalt de tot del web** amb el 19 i les nenes del 2018.

---

## 8. El que queda fora del web (i val tant com el web)

Això no ho pot fer un canvi de codi. Són vuit dies i aquestes són les palanques
que més moguin l'agulla, per ordre:

1. **Fitxa de Google del club.** Crear l'esdeveniment com a **publicació de
   Google Business Profile** amb data, hora i enllaç a `/portes-obertes/`. És
   el que omple el mòdul «Esdeveniments» del mapa i és gratuït. Si la fitxa no
   té l'adreça exactament igual que el web (carrer de la Llacuna, 170-172),
   corregir-ho primer: és el punt 5 de la secció GEO.
2. **IndexNow.** El repositori ja porta `scripts/indexnow.py`. Passar-lo amb les
   URL noves i les tocades el mateix dia de publicar: Bing i Yandex les
   indexen en hores, no en dies. Google no el fa servir, però la
   `Search Console` sí que accepta la inspecció d'URL a mà, que a vuit dies
   val la pena fer una per una.
3. **Instagram.** L'enllaç de la bio ha d'anar a `/portes-obertes/` fins al 27.
   El 19 és dissabte: stories el dijous, el divendres i el mateix matí. El
   contingut de nenes del 2018 és el que millor funciona al perfil (els reels
   de l'escoleta femenina són els que més volen) i ara, per primera vegada, té
   una pàgina on aterrar.
4. **WhatsApp de famílies.** El canal amb més conversió del club, i el que no
   es mesura enlloc. Un missatge a les famílies actuals demanant que ho passin
   a una amiga de la filla val més que qualsevol posició a Google.
5. **Les escoles del barri.** Escola Casas (on ja s'entrena els dimecres), Escola
   Provençals, La Farigola del Clot, La Rambleta. A vuit dies, un cartell a
   l'AFA arriba abans que una pàgina nova.

---

## 9. Com sabrem si ha funcionat

- **Reserves al formulari del 19**, partides per any de naixement. El comptador
  ja hi és: la dada del 2018 se'n pot treure sense feina extra.
- **Search Console**, consultes noves que continguin «nenes», «niñas», «2018»
  o «19 de setembre» — avui són zero, perquè no hi havia pàgina.
- **Trànsit a la landing nova** i quants d'aquests arriben al formulari.
- **Si alguna IA ens cita**: preguntar-ho literalment a ChatGPT, Perplexity i
  l'AI Mode de Google el 18 i el 25 («on pot jugar a bàsquet una nena de 8 anys
  al Clot?»). És una comprovació de dos minuts i és l'única manera de saber si
  la capa GEO ha entrat.

La comprovació honesta: **vuit dies no són prou perquè una pàgina nova
posicioni a Google.** El que sí que pot passar en vuit dies és que l'`Event`
entri als resultats d'esdeveniments, que la fitxa de Google mostri la data, i
que les IA, que reindexen molt més ràpid, ja tinguin què citar. La landing de
nenes del 2018 és una inversió que rendeix aquesta temporada sencera, no
aquest dissabte.
