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

## Pendent · rendiment web (24/08/2026)

Auditoria completa a `claude/web-performance-testing-6k9iwe`: la portada passa de
79 a 97/100 de Lighthouse, LCP de 5,1 s a 1,4 s, -216 KB de pes i -200 MB al
repositori (vídeos de la mascota sense usar). Detall complet a
`tests/README.md` i als missatges de commit d'aquesta branca. Dues coses no
es podien resoldre des del codi:

- **Cabeceres de caché HTTP.** El domini apunta directament a GitHub Pages
  (`CNAME` → `cbgrupbarna.info`, sense Cloudflare ni cap altre CDN al davant
  — R2 només s'usa per emmagatzemar fotos, no com a proxy del lloc). GitHub
  Pages no admet cap fitxer de configuració per personalitzar `Cache-Control`
  (no hi ha equivalent al `_headers` de Netlify): les cabeceres de caché són
  fixes i no es poden allargar des del repositori. Per aconseguir-ho caldria
  posar un CDN (Cloudflare és l'opció més òbvia, ja que R2 ja hi viu) davant
  del domini — és una decisió d'infraestructura, no de codi.
- **451 fotos amb l'original esborrat del repositori.** Als àlbums
  `jugadors-es-2526` (178 de 192 fotos) i `fotos-seniors-2526` (273 de 292),
  la miniatura i la foto gran sí que hi són (`fotos/thumb/`, `fotos/web/`),
  però l'original a `fotos/uploads/` no. El botó de descarregar l'original
  d'aquestes 451 fotos concretes dona un enllaç trencat (404) a producció.
  No sé si és intencionat (es va netejar espai i només es van conservar les
  derivades) o un pas de pujada que va quedar a mitges. Cal decidir: es
  torna a pujar l'original, o es treu el botó de descàrrega en aquests dos
  àlbums.

## Pendent · grups de fotos privats a `galeria/` (24/08/2026)

`/fotos/` (la galeria estàtica publicada) **ja té** grups privats: un
esdeveniment amb `"visibility": "private"` a `fotos/events.js` no surt al
llistat normal, i només es veu entrant amb `/fotos/?marqueting=<clau>` (la
clau és `marketing_pin` de `fotos/config.js`, gestionable des de
`/fotos/admin.html`).

`galeria/` — l'app a part en Next.js + Supabase, amb login de socis i rols
(viewer/contributor/editor/admin), desplegada al seu propi domini de Vercel
i **no enllaçada des de cap pàgina de cbgrupbarna.info** — no ho té:
`galeria/supabase/schema.sql` no defineix cap camp de visibilitat a la
taula `events`, així que qualsevol persona amb compte (fins i tot rol
`viewer`) veu tots els esdeveniments. Cal decidir:
- si aquesta app arriba a fer-se servir de debò (ara mateix sembla parada,
  sense enllaç des del lloc publicat), i
- si es vol, afegir un camp `visibility` (o `is_private` + taula
  d'accessos per esdeveniment) a `events` i filtrar-lo a les consultes,
  seguint el mateix criteri que ja fa `/fotos/`.

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
