# Campus de bàsquet · mapa de paraules clau i pla de posicionament

Document de treball de màrqueting (no és una pàgina publicada). Recull totes les
paraules clau del bloc **campus / tecnificació**, a quina pàgina ha de rankejar
cadascuna, i què queda pendent fora del web.

Punt de partida (agost 2026): a Google AI Mode, la pregunta *"campus basquet
barcelona"* respon amb Barça Escola, Campus Gigantes, Offlimits, Pau Gasol
Academy, ITW Sport i la Fundació del Bàsquet Català. El Barna no hi sortia. El
motiu no és que el web estigui mal fet: és que **no teníem la pàgina que aquestes
respostes citen** —la que compara totes les opcions de la ciutat— i que
**faltaven dades dures extraïbles** (preu, places, edats, horaris) en format que
una IA pugui llegir i citar.

## Arquitectura: quina pàgina ataca què

| Pàgina | Rol | Consultes que ha de guanyar |
|---|---|---|
| `/campus-basquet-barcelona/` · `/es/campus-baloncesto-barcelona/` · `/en/basketball-camps-barcelona/` | **Comparativa de ciutat** (nova). És la peça citable per IA i la que competeix amb els llistats i blogs | genèriques i comparatives: "campus bàsquet Barcelona", "mejores campus de baloncesto Barcelona" |
| `/campus/` · `/es/campus/` · `/en/campus/` | Producte: el campus del Barna | transaccionals: preu, inscripcions, dates, "campus Grup Barna" |
| `/campus-nadal-basquet-barcelona/` · `/es/campus-navidad-baloncesto-barcelona/` | **Campus de Nadal** (nova). Landing estacional pròpia, viva tot l'any | "campus Nadal bàsquet Barcelona", "campus navidad baloncesto Barcelona" |
| `/tecnificacio-basquet-barcelona/` | Tecnificació fora d'estiu, paraigua de les tres èpoques | "tecnificació", "entrenament individual", "Setmana Santa" |
| `/blog/campus-basquet-barcelona-guia/` (3 idiomes) | Guia de criteri per a famílies | "com triar", "què mirar", "ràtio", "quant costa" |
| `/escoleta/` | Curs sencer, no campus | "escola de bàsquet", "començar a jugar" |

Regla: **una intenció, una pàgina**. Si dues pàgines ataquen la mateixa consulta
es fan la competència i cap de les dues puja.

## Paraules clau · CATALÀ

**Nucli (prioritat 1)**
campus bàsquet Barcelona · campus de bàsquet a Barcelona · campus d'estiu de
bàsquet Barcelona · campus bàsquet estiu 2026 · millors campus de bàsquet
Barcelona · campus de bàsquet per a nens i nenes Barcelona

**Tecnificació (prioritat 1)**
campus de tecnificació bàsquet Barcelona · tecnificació bàsquet Barcelona ·
entrenament individual bàsquet Barcelona · campus tecnificació tir bàsquet ·
campus 1x1 bàsquet · campus manejo de pilota

**Estacionals (prioritat 2)**
campus bàsquet Nadal Barcelona · campus bàsquet Setmana Santa Barcelona ·
casal esportiu estiu Barcelona bàsquet · campus juliol bàsquet Barcelona

**Geogràfiques (prioritat 1 — són les que podem guanyar de veritat)**
campus bàsquet Clot · campus bàsquet Sant Martí · campus bàsquet Glòries ·
campus bàsquet Poblenou · campus bàsquet Camp de l'Arpa · campus bàsquet
Eixample Barcelona · campus bàsquet a prop de casa

**Segmentades (prioritat 2)**
campus bàsquet femení Barcelona · campus bàsquet per a nenes · campus bàsquet
mini · campus bàsquet cadet · campus bàsquet júnior · campus bàsquet 8 anys /
10 anys / 12 anys

**Cua llarga i preguntes (prioritat 1 per a IA)**
quant costa un campus de bàsquet · quin és el millor campus de bàsquet de
Barcelona · què inclou el preu d'un campus de bàsquet · quants jugadors per
entrenador ha de tenir un campus · cal ser d'un club per anar a un campus ·
a quina edat es pot anar a un campus de bàsquet · campus de bàsquet obert a
jugadors d'altres clubs

**Marca (prioritat 1, defensiva)**
campus CB Grup Barna · Grup Barna campus · campus Time Chamber · campus Time
Chamber Barcelona · CB Grup Barna estiu

## Palabras clave · CASTELLANO

**Núcleo**
campus baloncesto Barcelona · campus de baloncesto en Barcelona · campus de
verano baloncesto Barcelona · campus baloncesto verano 2026 · mejores campus de
baloncesto Barcelona · campus de basket Barcelona · campus de básquet Barcelona

**Tecnificación**
campus tecnificación baloncesto Barcelona · tecnificación baloncesto Barcelona ·
entrenamiento individual baloncesto Barcelona · campus de tiro baloncesto ·
campus 1x1 baloncesto · academia de baloncesto Barcelona

**Estacionales**
campus baloncesto Navidad Barcelona · campus baloncesto Semana Santa Barcelona ·
campamento de baloncesto Barcelona · campus urbano baloncesto Barcelona

**Geográficas**
campus baloncesto El Clot · campus baloncesto Sant Martí · campus baloncesto
Poblenou · campus baloncesto cerca de mí · campus baloncesto Barcelona ciudad

**Segmentadas**
campus baloncesto niños Barcelona · campus baloncesto niñas · campus baloncesto
femenino Barcelona · campus baloncesto 10 años · campus baloncesto infantil ·
campus baloncesto cadete

**Cola larga y preguntas**
cuánto cuesta un campus de baloncesto · cuál es el mejor campus de baloncesto de
Barcelona · qué incluye un campus de baloncesto · diferencia entre campus y
casal de baloncesto · campus de baloncesto sin ser del club · campus de
baloncesto con comida incluida

**Marca**
campus CB Grup Barna · Grup Barna baloncesto · campus Time Chamber

## Keywords · ENGLISH (famílies internacionals i estades)

basketball camp Barcelona · summer basketball camp Barcelona · basketball skills
camp Barcelona · basketball academy Barcelona · basketball camp for kids
Barcelona · basketball camp for girls Barcelona · youth basketball camp Spain ·
best basketball camps Barcelona · Easter basketball camp Barcelona · Christmas
basketball camp Barcelona · basketball camp El Clot

## Fet en aquesta tanda

1. **Pàgina comparativa nova** en tres idiomes, amb taula de tots els campus de
   referència de Barcelona, criteris de tria, preus de mercat i FAQ. És el
   format que les respostes d'IA citen.
2. **`Course` + `Offer` amb preu** (195 € / 160 €) al schema de `/campus/` en
   ca, es i en: fa que el preu sigui extraïble per Google i per les IA.
3. **`ItemList` + `FAQPage`** a la comparativa, amb les preguntes tal com les
   escriu la gent ("quin és el millor campus…", "quant costa…").
4. **`llms.txt`**: bloc de dades dures del campus (format, preus, places, edats,
   ubicació, contacte) i entrada de la comparativa.
5. **Meta keywords, títols i descripcions** ampliats amb el vocabulari de dalt.
6. **Enllaçat intern**: campus ↔ comparativa ↔ guia del blog ↔ tecnificació.
7. **Sitemap** actualitzat.

## Pendent fora del web (això és el que falta per sortir "entre els millors")

El web ja és competitiu. El que decideix la resta és **autoritat externa**: les
respostes d'IA citen qui està mencionat en més llocs, no qui té millor HTML.

- **Google Business Profile** del club amb la categoria d'escola/club esportiu,
  fotos del campus, horaris i publicacions cada edició. És el senyal local més
  fort i el més barat.
- **Ressenyes de famílies** al perfil de Google, després de cada setmana de
  campus. Objectiu realista: 30-40 ressenyes.
- **Directoris i agendes**: guia d'activitats d'estiu de l'Ajuntament de
  Barcelona i del Districte de Sant Martí, agendes de casals i campus d'estiu,
  portals de famílies (tipus Sortim amb nens, Time Out Kids), FCBQ i Fundació
  del Bàsquet Català.
- **Premsa de barri**: Guia Clot, Eix Clot, mitjans de Sant Martí — una nota per
  edició amb dades (places, procedència dels inscrits, entrenadors).
- **Wikipedia / Wikidata** del club: les IA hi pesen molt per fixar l'entitat.
- **Contingut a Instagram amb el mateix vocabulari**: peu de foto i text en
  pantalla dient "campus de bàsquet a Barcelona", no només "campus".
- **Entrenadors i jugadors formats al club**: cada esment extern (NBA, ACB,
  Lliga Femenina) que enllaci al web val més que deu pàgines pròpies. Convé
  demanar-los l'enllaç, no només l'etiqueta.

## Com mesurar-ho

- Search Console: impressions i posició mitjana de les consultes de la llista,
  filtrades per pàgina.
- Comprovació manual mensual a Google AI Mode, ChatGPT i Perplexity amb
  "campus bàsquet Barcelona", "campus baloncesto Barcelona" i "mejores campus de
  baloncesto Barcelona": mirar si el club hi surt citat i amb quines dades.
- Peticions per WhatsApp amb l'origen "us he trobat a Google".


---

# Campus de Nadal · pla per a l'octubre

Ana publica l'edició de Nadal a l'**octubre**. La pàgina ja és viva des d'ara,
perquè Google necessita setmanes per indexar i posicionar una URL nova: si es
publica l'octubre des de zero, arriba tard a la temporada de cerques (que arrenca
a mitjans de novembre i pica fort la primera quinzena de desembre).

## Paraules clau del clúster de Nadal

**Català**: campus Nadal bàsquet Barcelona · campus de bàsquet vacances de Nadal ·
tecnificació Nadal bàsquet Barcelona · campus bàsquet desembre Barcelona ·
casal de Nadal esportiu Barcelona · activitats de Nadal per a nens Barcelona ·
campus bàsquet Nadal Clot / Sant Martí

**Castellà**: campus Navidad baloncesto Barcelona · campus de baloncesto
diciembre Barcelona · campus de Navidad deportivo Barcelona · tecnificación
Navidad baloncesto · campus baloncesto vacaciones de Navidad · casal de Navidad
Barcelona baloncesto · actividades de Navidad para niños Barcelona ·
campus baloncesto Navidad El Clot

**Preguntes (per a IA)**: hi ha campus de bàsquet per Nadal a Barcelona · què
fer amb els nens les vacances de Nadal a Barcelona · quant costa un campus de
Nadal · quins dies es fa el campus de Nadal · campus de Nadal obert a nens
d'altres clubs

## Calendari

| Quan | Què |
|---|---|
| **Ara (agost)** | La pàgina ja és publicada, indexable i enllaçada des de campus, tecnificació i comparativa. Sense dates: diu que es confirmen a l'octubre. |
| **Setembre** | Fitxa de Google al dia amb fotos de l'estiu. Un post d'Instagram que enllaci la pàgina (el perfil és l'única font d'enllaços que controlem). |
| **Octubre — publicació** | Omplir dates i preu a la pàgina (ca i es), afegir el node `Event` del schema (plantilla a sota), actualitzar `lastmod` al sitemap i el bloc de Nadal a `llms.txt`. Publicació a Google Business Profile. Correu a les agendes de districte i portals de famílies amb l'activitat de Nadal. |
| **Novembre** | Recordatori a IG i post de Google. Comprovar a Search Console que la pàgina ja rep impressions per "campus navidad baloncesto barcelona". |
| **Desembre** | Fotos de l'edició a la mateixa pàgina: la converteix en prova social per a l'any següent. |
| **Gener** | Treure les dates passades, deixar la pàgina en mode "propera edició" i mantenir-la viva. No esborrar-la mai: la URL ha d'acumular historial. |

## Plantilla del node `Event` (enganxar dins de `@graph` quan hi hagi dates)

```json
{
  "@type": "Event",
  "@id": "https://cbgrupbarna.info/campus-nadal-basquet-barcelona/#edicio-2026",
  "name": "Campus de Nadal de bàsquet · CB Grup Barna",
  "description": "Tecnificació de bàsquet durant les vacances escolars de Nadal a La Nau del Clot: tir, manejo de pilota, 1x1 i lectura de joc, en grups per edat i nivell.",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "startDate": "2026-12-DD",
  "endDate": "2026-12-DD",
  "organizer": { "@id": "https://cbgrupbarna.info/#club" },
  "location": {
    "@type": "Place",
    "name": "La Nau del Clot",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Carrer de la Llacuna, 172",
      "addressLocality": "Barcelona",
      "addressRegion": "Catalunya",
      "postalCode": "08018",
      "addressCountry": "ES"
    }
  },
  "offers": {
    "@type": "Offer",
    "price": "PREU",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-10-DD",
    "url": "https://cbgrupbarna.info/campus-nadal-basquet-barcelona/"
  },
  "audience": { "@type": "PeopleAudience", "suggestedMinAge": 5, "suggestedMaxAge": 17 }
}
```

Amb `Event` + `Offer` datats, Google pot mostrar la fitxa d'esdeveniment i les
IA poden respondre "del X al Y de desembre, N euros" citant-nos. Sense dates, no
s'ha de posar el node: un `Event` amb dades inventades o buides fa més mal que bé.

## Després de cada edició: la xifra

L'estiu de 2026 hi van passar **unes 150 nenes i nens**. Aquesta xifra ja és a la
pàgina del campus, a la comparativa, a la landing de Nadal i a `llms.txt`, perquè
és exactament el tipus de dada que una IA cita quan compara campus i que una
família llegeix com a prova que la cosa funciona.

Cada edició ha de deixar la seva xifra: participants, setmanes, clubs de
procedència. **La facturació no es publica** —ni al web, ni a la fitxa de Google,
ni a les notes de premsa—: va al dossier de Junta i al de patrocinis, on sí que
és un argument de pes.
