# Bateria de proves de cbgrupbarna.info

Eines que no necessiten cap dependència instal·lada al repositori: fan servir
el Chromium i el Playwright que ja hi ha a l'entorn.

## El dia que es publica: una sola ordre

```bash
node tests/llancament.mjs                     # tot; ~20 min (obre el navegador)
node tests/llancament.mjs --rapid             # sense navegador; ~2 min
node tests/llancament.mjs --md tests/out/LLANCAMENT.md
```

Executa tota la bateria i respon **una** pregunta: es pot treure a fora o no.
Torna `0` si és APTE i `1` si no ho és, de manera que serveix igual com a
últim pas abans de publicar i com a comprovació automàtica.

La diferència entre el que atura un llançament i el que no és una decisió
presa i escrita a la constant `BLOQUEIGS` de `llancament.mjs`, no un criteri
que canviï cada vegada. **Bloquegen**: tot el que `audit-llancament.mjs` marca
com a error, els errors durs de l'SEO (enllaç trencat, sitemap o `llms.txt`
que citen adreces inexistents, redirecció morta, canonical absent, accents
trencats, idioma mal declarat), que el cercador falli cap cas, que els tres
idiomes no vagin junts, i qualsevol pàgina que al navegador respongui diferent
de 200, es desbordi, tingui una imatge trencada, demani un fitxer propi que no
existeix o li peti el JavaScript. **No bloquegen** els avisos: un títol massa
llarg fa que una pàgina surti pitjor a Google, no que la web no es pugui
publicar. Es llegeixen a part, amb `report.mjs`.

## Cada peça per separat

```bash
node tests/audit-llancament.mjs               # preparació per publicar
node tests/audit-seo-geo.mjs                  # SEO i GEO, anàlisi estàtica
node tests/audit-browser.mjs                  # renderitzat real a 5 amplades
node tests/report.mjs --md tests/out/INFORME.md
node tests/screenshots.mjs --full             # captures per mirar-s'ho
```

Els resultats en brut queden a `tests/out/` (`llancament.json`, `seo-geo.json`
i `browser.json`), i `report.mjs` ajunta els dos últims en un informe llegible.

## Què comprova cadascuna

### `audit-llancament.mjs`
Les altres dues miren si el lloc està ben fet; aquesta mira si està **llest per
sortir**, que és una pregunta diferent. Una pàgina pot tenir un SEO impecable i
alhora demanar una foto que ningú ha pujat.

- **Actius**: cada `srcset`, `poster`, `<source>`, `<video>`, `<iframe>` i cada
  `url()` del CSS es resol contra el disc. (Els `<a href>`, els `<img src>` i
  els `<script src>` ja els mira `audit-seo-geo.mjs`.)
- **Dependències de tercers**: qualsevol recurs demanat per `http://` dins
  d'una pàgina servida per `https://` —que el navegador bloqueja i deixa la
  pàgina trencada— i, com a avís, els `<a>` que porten a llocs sense xifrar i
  els CDN externs, que la norma del club és no tenir-ne.
- **Dades estructurades**: que cada JSON-LD es pugui llegir de debò (una coma
  de més no dona cap error visible: simplement Google no en fa cas) i que les
  adreces que cita existeixin.
- **Formularis**: que tinguin destí —seguint els `<script src>` propis, perquè
  el gestor sol viure a `/js/`—, botó d'enviar, camps amb etiqueta (compta
  tant `<label for>` com el camp embolcallat dins d'un `<label>`) i, quan
  demanen dades personals, política de privacitat a l'abast i consentiment.
- **Publicació**: `CNAME`, `.nojekyll`, `robots.txt`, `404.html`, mides i
  domini del `sitemap.xml`, i el `manifest.json` amb les seves icones.
- **Res a mig fer**: «lorem ipsum», TODO, «pendent de confirmar»,
  «properament» sense data, dates sense omplir, enllaços amb `href` buit.
- **Secrets**: claus i tokens que s'haurien publicat sense voler. Descarta els
  exemples escrits expressament (`placeholder="ghp_xxxxxxxx"`).
- **Pes**: el HTML més els fitxers propis que necessita per pintar-se.
- **Codi**: cada `<script>` de cada pàgina i cada `.js` propi passen per
  `node --check`. Un error de sintaxi no dona cap avís al navegador: el bloc
  simplement no s'executa i el que en depenia deixa de funcionar en silenci.
  Així es va trobar que una cometa de més a
  `x.font='170px Anton, 'Anton', sans-serif'` tenia mort el generador de
  cartells de `/partits/cartell.html` en els tres idiomes.
- **Idiomes**: que cap canvi d'idioma porti a una adreça morta.

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
quadra amb 4-7. **Actualització 25-08-2026**: la direcció de màrqueting ha
decidit expressament el contrari — «4 a 8 anys, sempre» — i s'ha aplicat a
tot el lloc; no ho «arreglis» de tornada a 4-7 per la lògica d'aquí sobre. També s'hi va fer evergreen tot el «60 anys» que és text viu
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
