# Bateria de proves de cbgrupbarna.info

Tres eines que no necessiten cap dependència instal·lada al repositori: fan
servir el Chromium i el Playwright que ja hi ha a l'entorn.

```bash
node tests/audit-seo-geo.mjs                  # SEO i GEO, anàlisi estàtica
node tests/audit-browser.mjs                  # renderitzat real a 5 amplades
node tests/report.mjs --md tests/out/INFORME.md
node tests/screenshots.mjs --full             # captures per mirar-s'ho
```

Els resultats en brut queden a `tests/out/` (`seo-geo.json` i `browser.json`),
i `report.mjs` els ajunta en un informe llegible.

## Què comprova cadascuna

### `audit-seo-geo.mjs`
Recorre totes les pàgines `.html` del repositori sense obrir cap navegador.

- **Bàsics**: doctype, `lang`, charset, viewport, bloqueig del zoom, accents
  trencats.
- **Metadades**: títol i descripció amb la llargada que Google respecta,
  canonical absoluta i coherent amb la pròpia URL, Open Graph i Twitter Card.
- **Estructura**: un sol `<h1>`, imatges amb `alt`, enllaços externs amb
  `noopener`.
- **Enllaços**: cada destí intern es resol contra el disc, tal com ho faria
  GitHub Pages (`/x/` → `/x/index.html`, `/x` → `/x.html`). Els que un script
  munta en temps d'execució (`${…}`) no es poden resoldre i s'ometen.
- **Sitemap**: URLs que no existeixen, pàgines publicades que hi falten,
  duplicats, `lastmod` amb data futura.
- **hreflang**: reciprocitat, autoreferència, `x-default` i que l'idioma
  declarat coincideixi amb el de la pàgina de destí.
- **GEO geogràfic**: meta `geo.*` i `ICBM`, coordenades dins de Barcelona,
  entitat `SportsClub`/`LocalBusiness` amb adreça, horaris i `sameAs`, i
  **coherència del NAP** (nom, adreça i telèfon iguals a tot el lloc).
- **GEO generatiu**: `llms.txt` viu i amb les dades dures, permisos dels
  rastrejadors d'IA a `robots.txt`, encapçalaments en forma de pregunta,
  dades estructurades datades i amb autoria.

### `audit-browser.mjs`
Serveix el repositori i el carrega amb Chromium a 360, 430, 820, 1024 i
1440 px. Talla tot el trànsit extern a propòsit: així les proves són
deterministes i, de passada, es veu si alguna cosa del lloc depèn d'un tercer
per aparèixer.

- **Desbordament horitzontal** i quin element el provoca.
- **Zones tocables** per sota de 44 px, comptant la unió amb el seu `<label>`.
- **Contrast** calculat amb la fórmula de la WCAG sobre el fons real, resolent
  transparències i acumulant els fons dels pares.
- **Mida de lletra** per sota de 12 px.
- **Fotografia**: imatges que es pinten més grans del que fa el fitxer (la
  regla del club: cap foto ampliada), imatges sobredimensionades, sense `alt`
  o trencades.
- **Focus de teclat**: tabula de debò amb `Tab`. Cridar `element.focus()` no
  activa `:focus-visible` a Chromium i donaria un fals positiu.
- **Mode fosc**: compara el renderitzat amb `prefers-color-scheme: dark`.
- Errors de consola, peticions fallides, IDs duplicats, punts de referència
  (`main`, `nav`, `footer`), salts de nivell d'encapçalament, controls sense
  nom accessible, taules que desborden i pes del DOM.

## Sobre auditories externes rebudes com a PDF

Si algú aporta una auditoria SEO/GEO d'una eina externa, **verifica-la contra el
disc abans d'actuar-hi**. El 17/08/2026 se'n va rebre una de 63 pàgines que
citava en detall 21 URLs (`/club/`, `/femeni/`, `/historia/`,
`/organigrama/`, `/instal-lacions/`, `/posicionament/`, `/documents/`,
`/magics/`, `/cistella-petita/`...) que **no existeixen en aquest repositori**:
són noms plausibles per a un club de bàsquet genèric, no els reals. Bona part
de les captures «reconstruïdes» i cites textuals associades a aquestes URLs
eren, per tant, fabricades.

Dins d'aquell mateix informe hi havia també un grapat de troballes reals,
confirmades una per una contra el codi: el tipogràfic «Respostem» → hauria de
ser «Responem» (`index.html`), «Cerca un event…» → «Cerca un esdeveniment…»
(`fotos/index.html`), i una inconsistència real i no trivial: l'edat de
l'Escoleta es deia «4 a 7 anys» a nou fitxers i «4 a 8 anys» només a
`escoleta/index.html` i a un bloc de `blog/com-triar-escola-basquet-barcelona/`
— aquest últim fitxer es contradeia fins i tot amb si mateix (FAQ deia 4-7,
cos de l'article deia 4-8). Es va poder resoldre sense preguntar perquè la
pròpia lògica de transició del club («als 8 anys passen a premini») només
quadra amb 4-7. També s'hi va fer evergreen tot el «60 anys» que és text viu
(no citació d'un article de premsa real, que sí s'ha de deixar intacte amb el
número que porti).

La lliçó: una auditoria externa pot barrejar troballes certes amb estructura
inventada. Grep contra el repositori cada afirmació concreta abans de tocar
res — és ràpid i evita construir sobre un fonament fals.

## El que s'ha provat i s'ha descartat

Hi va haver una prova de **col·lisions** que buscava text damunt de text. Es va
retirar: donava 133 avisos en només quatre pàgines, perquè tot el que viu dins
d'una capçalera enganxada té coordenades de finestra i «trepitja» el que passa
per sota en fer scroll. Un test que crida el llop 133 vegades fa que ningú miri
la 134a. Aquesta mena de defecte es veu de seguida a `screenshots.mjs`, i és
així com es va trobar el solapament de la capçalera a partir de 1366 px.

La prova de **controls tapats** va passar pel mateix i s'ha pogut salvar: ara
prova cinc punts de cada element, només mira els que caben sencers a la
pantalla, i no compta les finestres modals ni les pantalles d'accés, que tapen
la pàgina perquè és la seva feina. De ~180 avisos va baixar a 13.

## Límits coneguts

- El contrast no es calcula sobre text que cau damunt d'una imatge de fons:
  no es pot saber quin píxel hi ha a sota. Aquests casos s'ometen.
- La detecció d'idioma compta paraules funcionals. Una pàgina de bibliografia
  plena de títols en anglès es detecta com a anglesa encara que el text propi
  sigui en català: cal mirar-s'ho abans de donar-la per bona.
- Les emoji es compten com a text acolorit i poden aparèixer com a contrast
  insuficient encara que es vegin perfectament.
- Els números decoratius grans i esvaïts (`01`, `02`…) surten com a contrast
  baix perquè el test no sap que no s'han de llegir.
- El servidor de proves imita GitHub Pages, però no la seva caché ni la
  compressió: els temps de càrrega no són comparables amb els de producció.
