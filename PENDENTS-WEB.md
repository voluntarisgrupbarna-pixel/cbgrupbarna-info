# Temes pendents · cbgrupbarna.info

Auditoria del repositori a 14/08/2026, revisada amb les decisions de l'Ana.

---

## ✅ Fet

### 1. Els tres enllaços trencats del Premi Dona i Esport

La web oficial del Premi Dona i Esport és
**https://voluntarisgrupbarna-pixel.github.io/cbgrupbarna/** i no es toca: des de .info
només s'hi enllaça.

Les tres pàgines que faltaven al mirall local sí existeixen a la web oficial, així que
els **108 enllaços repartits per 23 pàgines** de `/premidonaesport/` ara hi apunten
(en pestanya nova, amb `rel="noopener"`):

| Abans (404) | Ara |
|---|---|
| `/premidonaesport/el-metode.html` | `…github.io/cbgrupbarna/el-metode.html` |
| `/premidonaesport/investigacio/dossier-8m.html` | `…github.io/cbgrupbarna/investigacio/dossier-8m.html` |
| `/premidonaesport/patrocinis/dones.html` | `…github.io/cbgrupbarna/patrocinis/dones.html` |

Les tres URL també s'han tret del `sitemap.xml`: no són pàgines de .info.

### 2. Secció «Presentacions» a la portada

Nova secció `#presentacions` a `index.html`, just després del bloc que explica què és
el club, amb l'eyebrow **«Què és el Grup Barna»**. Conté els cinc documents:

1. **El Mètode Barna** — Els 3 pilars → web oficial
2. **Dossier 8M** — Fons Barna → web oficial
3. **Patrocinis · Dones empresàries** → web oficial
4. **Presentació d'empresa** → `presentaciocbgrupbarna.skywork.website`
5. **Dossier de patrocinis** → `/patrocinadors/`

### 3. Patrocinadors a `data.json`

El bloc `patrocinadors`, que estava buit, ara té els **22 partners amb fitxa publicada**,
cadascun amb nom, fitxa, logo, web i Instagram, i la temporada 2026-2027.

Queda anotat dins el mateix fitxer:
- **Nivell or/plata/bronze:** `null` a tots. No hi ha aquesta dada enlloc del repositori;
  l'ha de confirmar l'Ana.
- **Instagram per confirmar:** Foto Jané, Ovella Negra, Fundació Mullor, Tot Salut,
  Eix Comercial Sant Martí, Panteres Grogues.
- **Altes 26/27 anunciades a `/patrocinadors/` i encara sense fitxa pròpia:**
  Nova Farmàcia Clot i Clínica Dental 26.
- **Baixa:** Zapic. El logo `/partners/zapic-ai.png` encara és al repositori.

### 4. Sitemap ampliat

24 URL noves, entre elles les **22 fitxes de partner**, més `/partners-mapa/` i
`/fotos-esdeveniments/`. El sitemap passa de 68 a 89 URL.

Tres de les pàgines de la llista original **no s'hi han posat a propòsit**, perquè no són
pàgines reals: `/presentacio/`, `/dossier-patrocinis/` i `/patrocinis/` són redireccions
amb `noindex` cap a `/patrocinadors/`. Posar-les al sitemap seria demanar-li a Google que
indexi tres redireccions. Tampoc hi va `/fotos-esdeveniments/3x3-westfield-2026/`, que
porta `noindex` propi.

### 5. Landing de bàsquet femení · `/femeni/`

Pàgina nova que **integra** el coneixement de la web oficial del Premi Dona i Esport sense
replicar-la: text propi i resumit, i enllaç al document oficial per a la versió completa.

Conté: els tres pilars del Mètode (50% del pressupost, 38 entrenadores / 65,5% de l'staff,
53,7% d'audiència femenina), els 8 equips femenins federats de la 26-27 enllaçats a la seva
fitxa de `/partits/equips/`, el Cicle de Lideratge en sis fases, l'Efecte Ainhoa, la Línia
Femenina, la taula de documentació oficial, FAQ indexable i crida final.

Construïda amb `/css/barna.css` (mateix sistema visual que Campus i 3x3), amb JSON-LD
—`WebPage`, `SportsOrganization`, `FAQPage` i `BreadcrumbList`— i donada d'alta al
`sitemap.xml`, al `llms.txt`, al menú de la portada i a «El Barna, punt per punt».

### 6. Sis articles nous al blog, a partir de la candidatura

El PDF de la candidatura integral al 19è Premi Dona i Esport (53 pàgines) s'ha convertit en sis
articles que no existien, escrits per a famílies i no com a resum del document:

| Article | De quina part surt |
|---|---|
| Per què les noies deixen el bàsquet a l'adolescència | Els cinc mecanismes d'expulsió (4.3) |
| Entrenadores: per què importa qui hi ha a la banqueta | L'escala de reconeixement (T2) i el Fons Barna 8M (7.1) |
| El 0,75%: la paradoxa del bàsquet femení a Barcelona | Diagnòstic estructural i comparativa territorial (4.1-4.2) |
| Onze preguntes per saber si un club cuida la teva filla | Pla d'Igualtat (Part IX) i Protocol anti-assetjament (Part X) |
| «Shrink it and pink it»: quan l'equipació fa marxar jugadores | Línia Femenina d'equipació (5.3) |
| Bàsquet inclusiu: com funciona un equip d'esport adaptat | Barna Màgics (2.4) |
| Protecció del menor i Pla d'Igualtat: què té el club per escrit | Pla d'Igualtat (Part IX), Protocol anti-assetjament (Part X) i LOPIVI |

Cadascun porta FAQ indexable, JSON-LD (`BlogPosting` + `FAQPage` + `BreadcrumbList`) i enllaços
interns creuats. El blog passa de 5 a 12 articles. Actualitzats també l'índex del blog, el
`sitemap.xml` (97 URL) i el `llms.txt`. La xifra de l'staff tècnic femení s'unifica a **65,5%**
(abans el briefing i les dades oficials deien 68%), i l'adreça del club a **C/ Llacuna 170-172**
(53 ocurrències en 27 fitxers deien 170), seguint la candidatura.

### 7. `noindex` a l'eina interna

`fotos/migrar-flickr.html` ja porta `noindex, nofollow` com la resta d'admins.

---

## Correcció de l'auditoria anterior

El PDF `/briefing/materials/briefing-cb-grup-barna-collaboradors.pdf` **sí existeix**.
Era un fals positiu del meu script de comprovació. No hi ha res a fer.

---

## Pendent de material de l'Ana

- **Escoleta:** foto o vídeo d'en Willy Hernangómez entrenant a La Nau amb Time Chamber
  (el forat és a `escoleta/index.html:944`), i confirmar la fitxa del circuit 3x3 amb la
  selecció espanyola (línia 744).
- **Galeries:** `/fotos-esdeveniments/` només té publicada la del 3x3. Falta pujar la resta.
- **Nivells dels patrocinadors:** or / plata / bronze per als 22 partners.

## Pendent de desenvolupar

- **Dashboard d'analítica de la web.** Sistema que analitzi el trànsit i l'ús de
  cbgrupbarna.info i ho presenti en un panell dins de `/admin/`: visites per pàgina
  i per dia, d'on ve la gent (Instagram, cerca, directe), què es fa servir
  (calendaris descarregats, `.ics`, clics als CTA `data-cta`, dies de partit vs
  galeria), i evolució setmanal. Base disponible: ja hi ha **GA4** carregat amb
  consentiment via `js/galetes.js` — el dashboard pot llegir la GA4 Data API, o
  valorar una alternativa lleugera sense galetes (Plausible/GoatCounter) que
  simplificaria el banner. Decidir eina, dissenyar el panell i connectar-lo.

## Pendent de material de l'Ana · descàrregues

- **Columna `newsletter` al full de càlcul.** La porta de descàrrega de PDF envia les
  dades al mateix Apps Script que la galeria del 3x3 (`action=register`), amb dos camps
  nous: `newsletter` (si/no) i el document demanat dins de `font`. Cal comprovar que
  l'Apps Script els desa en una columna pròpia; si no, queden només dins de `font`.
- **Butlletí:** encara no hi ha eina d'enviament (Mailchimp, Brevo o similar). De moment
  només es recull el consentiment; cal decidir amb què s'envia.

## Pendent de decisió

- **`/premsa/moments/` en castellà i anglès.** La pàgina nova (36 moments d'Instagram
  verificats un a un, de febrer a desembre de 2025) només existeix en català. `/premsa/`
  ja té versions a `/es/` i `/en/`; decidir si es tradueix aquesta secció també.
- **Cronologia real vs. «temporada 2025-26».** De les 36 publicacions que l'Ana va
  proposar com a "els temes més importants de la 25/26", la verificació amb data real
  (WebFetch a cada post) va trobar que només ~20 són de tardor 2025 (setembre en
  endavant). La resta són de l'estiu 2025 (majoritàriament la campanya del 60è
  aniversari) o de la temporada 2024-25 (febrer-maig 2025). La pàgina les organitza amb
  les dates reals en tres blocs («Tardor 2025», «Estiu 2025 · 60 anys», «Abans de
  l'estiu»), no com un sol bloc de «temporada 25-26». Revisar si aquesta classificació
  li sembla bé o si en prefereix una altra.
- **Els tres àudios de `/premidonaesport/patrocinis/`** (`musica.mp3`, `veu-jugadora.mp3`,
  `mix.mp3`) no són al repositori **ni a la web oficial** (comprovat: 404). La pàgina obre
  amb un overlay «Activa el so · 2 minuts» que depèn d'ells, o sigui que l'experiència
  sonora no funciona. Cal pujar els arxius o treure l'overlay.
- **`/jugadors/`:** encara no està acabat. Quan hi hagi plantilla, cal omplir
  `jugadors/jugadors.js` i canviar el «Temporada 2025-2026» de la pàgina.
- **`/briefing/`:** encara diu «Temporada 2025-26». Decidir si es refà per a la 26-27 o es
  deixa com a document tancat de la temporada passada.
- **Abans del 5 de setembre:** hi ha 274 partits carregats (05/09/26 → 16/05/27) i cap
  resultat. Convé provar amb un partit jugat de debò que el robot de la FCBQ, les fitxes
  descarregables, els 16 `.ics` i el cartell del cap de setmana funcionen.

## Pendent de decisió · reestructuració del menú (18/08/2026)

Reorganitzat el menú complet (`#menu` a `index.html`) en 6 branques —Juga al
Barna / Equips i temporada / Activitats / El Club / Actualitat / Partners—
seguint l'arbre de continguts que proposa l'Ana. Queden tres coses obertes:

- **`/basquet-femeni/` i `/basquet-femeni/el-metode-barna/`** ara redirigeixen
  (noindex) a `/femeni/` i `/femeni/#metode`: eren dues pàgines completes amb
  el mateix contingut i el mateix `<title>` objectiu ("Bàsquet femení a
  Barcelona"), i s'ha triat `/femeni/` com a canònica per decisió de l'Ana.
  **Pendent:** `/es/baloncesto-femenino/` i `/en/womens-basketball/` encara
  són traduccions de la pàgina antiga (`/basquet-femeni/`), no de `/femeni/`.
  No s'han tocat perquè traduir `/femeni/` és una feina de contingut a part.
- **"Tecnificació"** (dins Activitats) i **"Notícies"** (dins Actualitat) són
  a l'arbre de l'Ana però no tenen cap pàgina real al lloc ni contingut al
  repositori. No s'han afegit al menú per no inventar-hi programa, preus o
  notícies. Falta que l'Ana digui què són exactament i doni el material.

## Sense acció

- **Esdeveniments «passats»** (3x3 Glòries, Mes de l'Orgull, Campus Time Chamber,
  Little Basket Day): són esdeveniments anuals del club i es queden com estan.

---

## Fase de marca · 20/08/2026

Canvi d'objectiu: la web deixa de mesurar-se com a web de club formatiu i passa a
mesurar-se com a **plataforma de marca esportiva i comercial**. La formació hi és, però
com a prova de dimensió, no com a definició de la marca.

### ✅ Fet en aquesta tanda

- **Coherència de dades.** `data.json` guanya el bloc `xifres`, que fa de font de veritat.
  Desapareixen «40 equips», «20F+20M» i «60 anys» de tot el lloc. L'LF2 deixa de ser una
  contradicció dins la mateixa pàgina: el club hi va jugar, avui compet a Supercopa.
- **El peu deixa d'enllaçar cbgrupbarna.com** (165 pàgines i els dos generadors). El
  `sameAs` de schema.org es manté: allà sí que consolida entitat.
- **Capçalera de marca a la portada** i navegació de sis entrades amb Empreses.
- **`/empreses/`**, amb Barna Business i FAQPage.

### Pendent, per ordre

1. **`/empreses/` en castellà i anglès.** `/patrocinadors/` ja té `/es/` i `/en/`; la
   nova pàgina, no. És la pàgina que llegirà una marca de fora de Barcelona.
2. **Els primers equips a la portada.** Sènior Femení A i Sènior Masculí A amb foto,
   plantilla, staff, pròxim partit i resultat, **abans** de la base. L'ordre comunica
   jerarquia, i és el que veu un patrocinador els primers cinc segons. Avui `#seniors`
   queda molt avall.
3. **La Nau del Clot com a actiu de marca.** Avui `/instal-lacions/` és una adreça. Hauria
   de ser la casa del club: fotografia, història, dies de partit, esdeveniments,
   activacions i com arribar-hi. Cal una sessió de fotos.
4. **Barna Media.** El blog ja no és «notícies del club»: és autoritat temàtica. Canviar-li
   el nom implica canviar URL, així que només amb redireccions ben fetes i després de tot
   l'anterior.
5. **Xifres d'audiència verificables.** `data.json → audiencia` cita 439.000
   visualitzacions mensuals a Instagram i no té els seguidors. Revisar cada trimestre amb
   una captura del panell; el que no es pugui justificar, fora de `/empreses/`.
6. **Migració tancada.** Queden enllaços a `cbgrupbarna.com/noticies/`, que és contingut
   real encara no migrat. Fins que no es migri, no es poden treure.
7. ~~**Guia visual «Franges i Extensa».** La portada ja no porta el hero
   `.lg-hero` de les franges (el repetia la capçalera de marca). Cal reflectir-ho a la guia.~~
   **Resolt (21/08/2026):** decisió de l'Ana és mantenir el `.lg-hero` de les Franges tal com
   diu la guia visual, malgrat la repetició amb la capçalera de marca. Restaurat a `index.html`.

### Nota sobre el nom «Patrocinadors» (20/08/2026)

El nom desapareix com a **nom de secció**: la secció es diu **Empreses** (`/empreses/`) i
la llista de qui hi és avui es diu **Partners** (`/patrocinadors/`). S'han canviat les 362
etiquetes visibles, els fils d'Ariadna i el generador.

**La URL `/patrocinadors/` no s'ha tocat**, i és una decisió, no un oblit: hi pengen 22
fitxes de partner més les versions `/es/` i `/en/`, i GitHub Pages no fa redireccions de
servidor —només `<meta refresh>` o JavaScript, que passen molt pitjor l'autoritat. Moure
la URL avui, amb el domini acabat d'estrenar i encara sense posicions guanyades, és
regalar el poc que hi ha. Es podrà fer quan `/patrocinadors/` ja posicioni i valgui la
pena arriscar-hi, i llavors amb redireccions per a totes les fitxes alhora.

---

# Auditoria d'experiència d'usuari als tres idiomes · 23/08/2026

Repàs complet de navegació, usabilitat i UX/UI de `cbgrupbarna.info` en
**català, castellà i anglès** (478 fitxers HTML), fet amb el web servit de
debò i obert amb un navegador a 390 px, no només llegint el codi. Aquí hi ha
el que s'ha arreglat i el que queda per decidir.

## Arreglat

### 1. El calendari de partits no existia en castellà ni en anglès

`/es/partits/` i `/en/partits/` no eren la pàgina pública traduïda: eren una
còpia antiga que portava enganxada **l'eina interna de gestió del club**
(92 KB de JavaScript amb entrada de resultats, generador de cartells i
importació de PDF). A sobre, aquell codi declarava dues vegades les mateixes
variables (`MESOS`, `DIES`), i això és un **error de sintaxi**: el navegador
descartava el bloc sencer i no s'executava res. Resultat: al lloc del
calendari hi sortia «Hay que activar JavaScript para ver el calendario
completo», sempre, encara que el JavaScript estigués activat. Ni un partit,
ni un resultat, ni un horari, per a qui llegeix la web en castellà o anglès.

Ja existia el generador `scripts/build-partits-idiomes.py`, escrit per a
això, però no s'havia arribat a executar. S'ha executat i, de passada,
arreglat i millorat:

- **Els enllaços interns ja no s'endevinen, es llegeixen.** Abans hi havia
  una llista fixa que donava per fet que l'adreça era la mateixa en els tres
  idiomes (`/escoleta/` → `/es/escoleta/`). No sempre ho és: la política de
  privacitat és `/es/politica-de-privacidad/` i `/en/privacy-policy/`, i
  protecció del menor és `/en/child-protection/`. Amb la llista fixa, el peu
  de la pàgina castellana enviava a la política **en català**. Ara cada
  destí es resol amb el `hreflang` de la pàgina catalana corresponent, així
  que quan es tradueixi una secció nova això ho seguirà sol.
- **Substitucions en dues passades.** Una regla curta es menjava el resultat
  d'una de llarga i deixava coses com «Calendarioo global».
- **Textos que quedaven en català** a la pàgina traduïda: el fil d'Ariadna,
  «A casa»/«Fora» de cada partit, el recompte de partits i l'avís de quan
  encara no hi ha resultats.
- **El text que només senten els lectors de pantalla** (`alt` de l'escut,
  «inici», «Fil d'Ariadna») ara també es tradueix.

### 2. El selector d'idioma no hi era a 2 de cada 3 pàgines

De 391 pàgines públiques, **251 no tenien selector d'idioma**. Qui entrava a
`/en/faq/` o a `/campus/` no tenia cap manera de canviar de llengua sense
tornar a la portada. Ara el porten totes (les úniques excepcions són el
panell d'`/admin/`, els fitxers d'impressió d'`/opina/print/` i les
redireccions).

I on hi era, sovint estava trencat:

- **15 pàgines enviaven a un article del blog.** A `/portes-obertes/`,
  `/bustia/`, `/escriu-nos/`, `/newsletter/` i `/proteccio-menor/comunicar/`
  —en els tres idiomes— els tres botons CA · ES · EN apuntaven tots a
  «A quina edat començar a jugar a bàsquet». Clicar «ES» a Portes obertes et
  deixava, després d'un salt de redirecció, en un article sobre l'edat
  d'iniciació. Són justament les cinc pàgines on la gent escriu al club.
- **22 pàgines el pintaven sense estil** perquè el CSS del component estava
  copiat a mà dins de cada pàgina i allà no s'havia copiat.
- **Hi havia vuit versions diferents del mateix CSS**: en 84 pàgines sortia
  amb l'Anton i en la resta amb la Inter. Ara el component viu una sola
  vegada a `css/barna.css` i s'han retirat 472 regles duplicades.
- **Les caselles feien 15-17 px d'ample.** Per sota del mínim de 24×24 px
  que demana la WCAG 2.2 per a qualsevol cosa que s'hagi de tocar amb el
  dit. Ara en fan 26.
- A `/orgull/` i a `/premidonaesport/` el selector quedava **fora de la
  pantalla** a mòbil: hi era al codi, però no s'hi podia arribar.

### 3. 599 enllaços que et treien de la teva llengua

Enllaços dins de pàgines `/es/` i `/en/` que apuntaven a la versió catalana
**tot i existir-ne la traducció**. Inclou els menús sencers d'algunes
pàgines, el «Demanar informació» de la portada i, sobretot, això:

> **El blog en castellà i en anglès amagava dos terços dels seus articles.**
> Sota un títol que deia «Estos artículos están publicados en catalán» /
> «These articles are published in Catalan» hi havia 14 i 15 fitxes amb el
> títol en català i l'enllaç a la versió catalana. **Totes tenien traducció
> completa publicada.** El lector en anglès veia 6 articles disponibles i 15
> «només en català» que en realitat podia llegir en anglès.

### 4. La capçalera es trencava a mòbil

A ~190 pàgines, el nom del club de la capçalera («CB GRUP BARNA», amb
`white-space: nowrap`) i el menú se solapaven, lletra sobre lletra, a
qualsevol mòbil. Per sota de 560 px el nom es retira —l'escut ja hi és, i és
enllaç a l'inici— i el menú recupera l'espai.

### 5. Consentiment i legal

- **L'enllaç «Més informació» de l'avís de galetes no anava enlloc**, en cap
  dels tres idiomes. Un gestor genèric interceptava qualsevol enllaç acabat
  en `#galetes` per reobrir el plafó, i s'enduia també el del propi avís:
  es cancel·lava la navegació, es tornava a obrir un plafó que ja era obert
  i, de propina, s'esborrava el consentiment desat.
- El mateix gestor **segrestava l'àncora real** de `#galetes` a
  `/es/politica-de-privacidad/` i `/en/privacy-policy/`: només s'excloïa la
  catalana.
- **Els peus en castellà i anglès no tenien columna «Legal».** Cap enllaç a
  la política de privacitat, ni a l'avís legal, ni a les galetes, en cap de
  les ~290 pàgines. Afegida als 218 peus que tenen l'estructura estàndard.
- **Dos formularis deien «Más info» / «More info» i portaven al dossier del
  Premi Dona i Esport**, no a la política de privacitat: `/es/fotos-3x3/`,
  `/en/fotos-3x3/` i els dos `3x3-westfield-2026/`.
- **`/galeria-3x3-glories/` recollia nom, cognoms, correu, mòbil i club
  sense casella de consentiment ni cap enllaç a la política**, en els tres
  idiomes. Ara la casella és obligatòria per continuar.

### 6. Accessibilitat i rendiment

- L'`alt` de l'escut i l'`aria-label` de la capçalera eren en català a 255
  llocs de `/es/` i `/en/`: qui fa servir un lector de pantalla sentia
  català llegint la pàgina en un altre idioma.
- **El menú de la portada no retenia el focus**: amb el tabulador se'n
  sortia cap a la pàgina de sota, que està tapada. Ara el focus hi entra en
  obrir-lo, hi dona voltes i torna al botó en tancar-lo.
- **Els errors del formulari de la portada no es llegien.** El missatge
  sortia en un rètol sense `role`, i desapareixia als 2,2 s.
- **El 404 sortia sempre en català.** GitHub Pages el serveix per a
  qualsevol adreça inexistent, també `/es/…` i `/en/…`: qui s'equivocava
  dins la versió castellana o anglesa quedava expulsat a un menú català. Ara
  es reescriu sol segons el camí.
- **Es precarregava `og-image.jpg` (84 KB) a les tres portades** i aquella
  imatge no es veu mai: és la de compartir a xarxes. 84 KB de prioritat alta
  competint amb el que sí que es veu.
- **Les tipografies es baixaven dues vegades.** `/escoleta/` i
  `/partners-mapa/` les demanaven a `/escoleta/fonts/`, una còpia amb URL
  diferent i, per tant, memòria cau diferent: ~130 KB que ja eren al
  navegador.
- Tres `<audio>` de `/premidonaesport/patrocinis/` apuntaven a fitxers
  `.mp3` que no existeixen (els reals són `.m4a`): l'experiència sonora no
  sonava.
- `rel="noopener"` a 9 enllaços `target="_blank"`; `src=""` retirat dels
  visors de `/fotos/` (un `src` buit fa que el navegador torni a demanar la
  pàgina sencera); `noindex` i `viewport` a les 12 redireccions.

### 7. `/escoleta/` tenia el seu propi commutador CAT/CAST

Canviava el text sense canviar l'adreça i, amb el navegador en castellà,
s'obria en castellà tot i que la URL, el `canonical` i el `hreflang` deien
que era la catalana. Al mateix temps ja existeixen `/es/escoleta/` i
`/en/escoleta/`, traduïdes senceres: hi havia **dues versions castellanes en
dues adreces diferents** i cap manera d'arribar a l'anglesa. Ara fa servir
el selector de sempre. El text castellà segueix al marcatge, ocult; es pot
netejar quan es vulgui.

## Per decidir (no s'ha tocat)

1. **`/premidonaesport/` demana un PIN i alhora és al `sitemap.xml`.** Són
   ~115 adreces que es donen a Google com a indexables i que, quan algú hi
   clica, ensenyen una paret amb un PIN. A més el codi és a la vista dins
   d'`assets/js/auth.js`. O s'obre (i es treu la paret) o es treu del
   sitemap amb `noindex`. És una decisió de l'Ana, no un error.
2. **Hi ha un vídeo de la mascota en castellà que no fa servir ningú.**
   `/mascota/mascota-reel-es.mp4` (50 MB) és al repositori, però
   `/es/mascota/` i `/en/mascota/` serveixen el català amb subtítols
   catalans per defecte. Abans de canviar-ho cal confirmar que el fitxer és
   el doblatge bo.
3. **Les portades en castellà i anglès són més pobres que la catalana.** La
   catalana té «La portada», «Cultura del Progrés», «El Barna per dins»,
   «Observatori Barna» i «Presentacions»; les altres dues no, i el seu `h1`
   és «Escoleta de baloncesto» en comptes del club. Són ~45 KB menys de
   pàgina.
4. **El `--red` de l'escut (#E20613) sobre crema (#F4F1EC) dona 4,37:1**,
   just per sota del 4,5:1 que demana la WCAG per a text petit. Per a
   titulars grans és correcte; per a text petit convindria el `--red-dark`
   (#A8040E, 7,81:1).
