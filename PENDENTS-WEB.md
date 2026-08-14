# Temes pendents · cbgrupbarna.info

Auditoria del repositori a 14/08/2026. Ordenat per urgència.
Cada punt porta la prova (fitxer i línia) perquè es pugui verificar.

---

## P0 · Errors que ja es veuen a la web

### 1. Tres pàgines del microsite Premi Dona i Esport no existeixen

Estan enllaçades des de **23 pàgines cadascuna** i, a més, publicades al `sitemap.xml`:
Google les rastreja i troba 404.

| Enllaç trencat | Enllaçat des de | Al sitemap |
|---|---|---|
| `/premidonaesport/el-metode.html` | 23 pàgines (menú lateral) | Sí |
| `/premidonaesport/investigacio/dossier-8m.html` | 23 pàgines | Sí |
| `/premidonaesport/patrocinis/dones.html` | 23 pàgines | Sí |

No s'han esborrat mai (no surten a l'historial de git): es van enllaçar pàgines
que no es van arribar a fer. Pel títol, el destí correcte d'"El Mètode" podria ser
`premidonaesport/metode-extern.html`, que sí existeix.

**Decisió a prendre:** crear les tres pàgines o redirigir els enllaços a les que ja hi ha
(i treure-les del sitemap). És la candidatura institucional del club: convé que no tingui 404.

### 2. Tres àudios que no hi són

`premidonaesport/patrocinis/index.html` crida:
`assets/audio/veu-jugadora.mp3`, `assets/audio/mix.mp3`, `assets/audio/musica.mp3`.
Cap dels tres és al repositori.

### 3. El sitemap enllaça un PDF inexistent

`/briefing/materials/briefing-cb-grup-barna-collaboradors.pdf` — al `sitemap.xml`, no al repositori.

---

## P1 · Contingut buit o desactualitzat

### 4. La plantilla pública està buida

`jugadors/jugadors.js` → `window.JUGADORS = []`.
La pàgina `/jugadors/` i `/jugadors/estadistiques.html` existeixen i estan enllaçades
des del panell d'administració, però no mostren ningú. A més, la pàgina encara diu
**"Temporada 2025-2026"** quan la resta del web ja és 26/27.

### 5. `data.json`: patrocinadors buits

```json
"patrocinadors": { "gold": [], "silver": [], "bronze": [],
  "_todoAna": "Omplir aquest llistat amb els patrocinadors actuals de la temporada 2025-2026" }
```

Mentrestant hi ha **22 fitxes de partner publicades** a `/patrocinadors/partners/`.
La font de dades i el web van per separat. Cal decidir quina mana i sincronitzar-les
(i actualitzar el text del `_todoAna`, que encara parla de 25/26).

### 6. Escoleta: dos buits marcats al codi

- `escoleta/index.html:944` — comentari `PENDENT`: falta la foto o el vídeo d'en Willy
  Hernangómez entrenant a La Nau amb Time Chamber.
- `escoleta/index.html:744` — fitxa amb "Pendent de confirmar · Circuit 3x3 amb la selecció espanyola".

---

## P2 · SEO i indexació

### 7. Pàgines públiques fora del sitemap

No hi són, i totes són pàgines de venda o de comunitat:

- Les **22 fitxes de partner** (`/patrocinadors/partners/*/`)
- `/patrocinis/` i `/dossier-patrocinis/`
- `/partners-mapa/`
- `/presentacio/`
- `/fotos-esdeveniments/` i `/fotos-esdeveniments/3x3-westfield-2026/`

Les fitxes de partner són l'actiu més fàcil de rendibilitzar: cada empresa col·laboradora
té una pàgina pròpia que ara mateix Google no té llistada.

*(Les pàgines `/admin` també queden fora, i això és correcte: totes porten `noindex`.)*

### 8. Una eina interna sense `noindex`

`fotos/migrar-flickr.html` és l'única pàgina d'ús intern sense `<meta name="robots">`.
La resta d'admins ja el porten.

---

## P3 · Temporada 2026-27

### 9. Rodatge de temporada a mig fer

`/partits/`, `/partits/equips/`, `/patrocinadors/` i la portada ja diuen 2026-27.
Encara diuen 2025-26: `/jugadors/` (cal canviar-ho, punt 4) i `/briefing/`
(cal decidir si es refà o es deixa com a document tancat de la temporada passada).
A `/premidonaesport/` la data 2025-26 és correcta: és la candidatura d'aquell any.

### 10. Preparar el web abans del 5 de setembre

`partits/data.json` ja té **274 partits carregats, del 05/09/2026 al 16/05/2027, i cap resultat**
(normal, la lliga no ha començat). Abans de la primera jornada convé comprovar en una prova real
que el robot diari de la FCBQ, les fitxes descarregables, els 16 `.ics` i el cartell del cap de setmana
funcionen amb dades de partit jugat, no només amb calendari.

### 11. Esdeveniments passats: arxivar o actualitzar

Al `data.json` i a les pàgines corresponents encara consten com a vigents esdeveniments
ja celebrats: 3x3 Westfield Glòries (juny 26), Mes de l'Orgull (juny 26),
Campus Time Chamber (juliol 26) i Little Basket Day (juny 26).
Cal decidir per a cadascun: arxiu amb la galeria de fotos, o actualització a la propera edició.

### 12. Galeries d'esdeveniments: només n'hi ha una

`/fotos-esdeveniments/` mostra una targeta "Properament · Aviat hi haurà més galeries:
campus d'estiu, portes obertes, partits especials". L'única galeria publicada és
la del 3x3 Westfield 2026. El campus d'estiu ja s'ha fet i no hi és.

---

## Resum executiu

| Prioritat | Temes | Què desbloqueja |
|---|---|---|
| P0 | 1, 2, 3 | Treure els 404 de la candidatura institucional |
| P1 | 4, 5, 6 | Que la plantilla i els patrocinadors deixin de ser pàgines buides |
| P2 | 7, 8 | Posar 27 pàgines al sitemap, entre elles les 22 de partners |
| P3 | 9, 10, 11, 12 | Deixar el web a punt per a la temporada, abans del 5 de setembre |
