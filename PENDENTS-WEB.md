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
- **Logotip de la Wilson:** no n'hi ha cap fitxer al repositori. La fitxa
  `patrocinadors/partners/wilson/` se'n surt amb el nom escrit amb la tipografia del
  club, que queda digne, però és l'única de les 21 fitxes que no té marca gràfica. Si
  l'Ana en pot demanar un SVG o un PNG amb fons transparent, es posa en un minut. Mentre
  no arribi, la fitxa no queda coixa: no cal fer-hi res.

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

## Preguntes freqüents · fase 1 del cercador que respon (23/08/2026)

Des que el cercador ensenya la resposta i no només l'enllaç, **cada pregunta
freqüent que s'escriu val el doble**: surt a Google com a `FAQPage` i el
cercador del web la dona a l'instant, en el seu idioma. Per tant, la manera de
fer el cercador més llest ja no és tocar codi.

### D'on surt aquesta llista

De comptar què hi ha. El web té **460 preguntes amb resposta** (219 en català),
i estan molt ben repartides per identitat, escoleta, campus, femení,
patrocinis i posicionament d'SEO. **El forat és un altre**: quan una família
ja s'ha convençut i vol entrar, no hi ha res escrit. Nou pàgines de pes no
tenen ni una sola pregunta:

| Pàgina | Pes | Preguntes |
|---|---|---|
| `/partits/equips/` | 90 | 0 |
| `/portes-obertes/` | 88 | 0 |
| `/club/` | 84 | 0 |
| `/fotos/` | 76 | 0 |
| `/blog/`, `/historia/`, `/instal-lacions/`, `/organigrama/` | 72 | 0 |
| `/documents/` | 70 | 0 |

**La asimetria més cridanera és el preu.** El web diu que una setmana de campus
val 195 €, la mitja jornada 160 € i la de Setmana Santa 150 €; diu que un
patrocini d'equip són 500 €. Però a la pregunta «quant costa apuntar-se al
club» —la primera que fa qualsevol família— l'única resposta que hi ha és
*«cal contactar directament amb el club»*. Es publica el preu d'una setmana i
no el de la temporada.

### Bloc A · Diners i compromís — **cal decisió de l'Ana**

Sis preguntes que no es poden escriure sense que algú digui el número. Són les
més buscades i les úniques que avui fan abandonar la pàgina.

1. Quant costa la temporada, per categoria?
2. Què inclou la quota? (fitxa federativa, assegurança, equipació, pistes)
3. Com es paga: un sol cop, mensual o trimestral? Es domicilia?
4. Hi ha descompte per a germans?
5. Hi ha ajuts o beques si una família no hi arriba?
6. Què passa si ens hem de donar de baixa a mig any?

> La 5 no és informació, és marca: un club que diu en veu alta que cap infant
> es queda fora per diners diu una cosa que els seus veïns no diuen.

**On van:** `/faq/` i, la 1 i la 2, també a `/escoleta/` i `/basquet-formatiu/`.

### Bloc B · El primer dia → `/portes-obertes/`

La pàgina amb més pes del web sense cap pregunta, i just la que llegeix qui
està a punt de venir.

7. Què he de portar el primer dia?
8. Cal avisar abans o em puc presentar directament?
9. Quants dies pot venir a provar?
10. El meu fill no ha jugat mai. Hi encaixarà?
11. Em puc quedar a mirar l'entrenament?

### Bloc C · Quin equip li toca → `/basquet-formatiu/` i `/partits/equips/`

Hi ha «Què vol dir Premini, Mini, Infantil, Cadet i Júnior?», que explica el
vocabulari. Falta la resposta directa: *el meu fill del 2015, on va?*

12. Quin equip li toca segons l'any de naixement?
13. Qui decideix a quin equip va? Hi ha proves de nivell?
14. Què vol dir equip A i equip B?
15. Es pot canviar d'equip durant la temporada?
16. Quants entrenaments a la setmana té cada categoria?

### Bloc D · On és tot això → `/instal-lacions/`

17. On és exactament la Nau del Clot i com s'hi arriba?
18. A quines altres pistes entrena el club?
19. Quin metro o bus hi va? Es pot aparcar?
20. Les famílies poden entrar a veure els entrenaments?

### Bloc E · La vida d'un equip — el que ningú ha escrit

Això no és a cap pàgina i és el que més es pregunta pel WhatsApp del club.
Anirien a `/faq/` i a `/partits/calendaris/`.

21. Els partits són sempre en cap de setmana? Quants desplaçaments hi ha?
22. Qui porta els nens als partits de fora?
23. Com ens avisen si canvia una hora o una pista?
24. Què passa si un dia no pot anar a entrenar?
25. És compatible amb els estudis o amb una altra activitat?
26. Cal revisió mèdica? Els jugadors estan assegurats?
27. Què passa si es lesiona en un entrenament?

### Bloc F · Equipació — **cal decisió de l'Ana** (preu)

28. Quina equipació cal comprar i quant costa?
29. On es compra i quan arriba?

### Bloc G · Confiança → `/proteccio-menor/` i `/fotos/`

El contingut de protecció del menor existeix, però escrit com a política de
club. Falta escrit com el pregunta una mare.

30. Els entrenadors i entrenadores tenen el certificat de delictes sexuals?
31. Puc demanar que el meu fill no surti a les fotos del club?
32. Amb qui parlo si tinc un problema amb un entrenador?

### Bloc H · Qui és qui → `/club/` i `/organigrama/`

33. Amb qui parlo de la meva categoria? (coordinador/a)
34. Com puc ser voluntari o entrenador al club?

### I tot això, per tres · el que costa de debò

**34 preguntes no són 34 textos: en són 102**, i cada un ha d'anar a dos llocs
(el `<details>` visible i el `FAQPage` del JSON-LD). Són ~204 insercions
repartides per una trentena de fitxers, i el repositori no té cap framework
d'i18n: cada traducció és un HTML independent que s'actualitza a mà.

Fet a mà, això no es manté. **Ja no s'està mantenint**: comptades sobre
l'índex, **28 pàgines tenen avui les tres versions desquadrades**.

| Pàgina | CA | ES | EN |
|---|---|---|---|
| Portada | 15 | 11 | 11 |
| `/escoleta/` | 8 | 6 | 6 |
| `/grup-barna-dades-oficials/` | 8 | 0 | 0 |
| `/patrocinadors/` | 8 | 5 | 5 |
| `/femeni/` | 5 | 3 | 3 |
| `/posicionament/`, `/empreses/`, `/model-formatiu/`, `/magics/`, 12 articles del blog | 1–6 | 0 | 0 |

I `escoleta/index.html` porta escrita, en un comentari, la regla que avui es
compleix a mà: *«FAQ visible · ha de coincidir sempre amb el FAQPage del
JSON-LD»*. Afegir-hi 102 textos més per la mateixa via empitjora el problema.

**La proposta és no escriure-ho tres vegades a tres llocs.** Una sola font
—`i18n/faq.yml`, una pregunta per entrada amb els seus tres idiomes i la
pàgina on va— i un generador que escrigui tots dos blocs (el `<details>` i el
JSON-LD) entre marcadors, com ja fa `generate-seo-snapshot.py` a `/partits/`.
D'una tacada: s'acaba la desincronització, es poden quadrar les 28 pàgines
d'ara, i el cercador se n'assabenta tot sol perquè llegeix el JSON-LD.

### Un blocatge concret

**`/portes-obertes/` no té versió en castellà ni en anglès.** És la pàgina del
bloc B —cinc preguntes—, té pes 88 i és la porta d'entrada de setembre. Cal
crear `/es/portes-obertes/` i `/en/open-days/` (i donar-les d'alta a
`i18n/routes.yml`) abans o alhora que les preguntes.

La resta de pàgines de la llista sí que tenen les tres versions, amb els noms
de `routes.yml`: `/es/instalaciones/` i `/en/facilities/`,
`/es/baloncesto-formativo/` i `/en/development-basketball/`,
`/es/proteccion-menor/` i `/en/child-protection/`, `/es/organigrama/` i
`/en/organisation/`.

### La regla, perquè serveixi de res

Cada pregunta ha d'anar **a dos llocs alhora**: al `<details>` visible dins
d'una secció `.faq` **i** al JSON-LD `FAQPage` de la mateixa pàgina. Si només
va al `<details>`, ni Google ni el cercador del web la veuen. Els generadors
ja ho fan bé; a les pàgines fetes a mà, cal recordar-ho.

Després, `/es/` i `/en/`: el cercador ensenya la catalana a qui llegeix en
castellà si no n'hi ha versió, però és un pedaç, no la solució.

### Com sabrem si ha funcionat

Les 34 d'aquesta llista portarien el web a prop de 500 preguntes en català. La
prova real no és el número: és que `node tests/cerca/prova-motor.mjs` es pugui
ampliar amb un cas per bloc —«quant costa la temporada», «què porto el primer
dia», «el meu fill del 2015 a quin equip va»— i que totes tornin una resposta.
Avui, cap de les tres en té.


---

## Preguntes freqüents · on som (23/08/2026, final del dia)

La font única existeix (`i18n/faq.yml` + `.github/scripts/generate-faq.py`) i
ja hi ha **16 preguntes publicades en els tres idiomes**. Cap inventada: totes
surten del que el web ja deia, escrit al cos del text o en una altra pàgina, i
que el cercador no podia trobar perquè no constava com a pregunta.

| Pàgina | Preguntes | D'on surt la resposta |
|---|---|---|
| `/portes-obertes/` | 5 | El cos de la mateixa pàgina |
| `/instal-lacions/` | 3 | El cos de la mateixa pàgina |
| `/basquet-formatiu/` | 7 | 5 migrades de la pàgina + 2 noves del seu propi quadre de categories |
| `/fotos/` | 1 | `/politica-de-privacitat/` |

`/basquet-formatiu/` anava **5 en català, 5 en castellà i 4 en anglès**.
Passada per la font única, va 7/7/7. És la primera pàgina amb el descuadre
resolt; en queden 27.

**Les traduccions ja no s'escriuen a mà**: `scripts/faq-tradueix.py` reutilitza
el traductor del web (`scripts/i18n-tradueix.py`) amb el mateix glossari i el
mateix to. Sense `ANTHROPIC_API_KEY` no falla: diu què falta. I
`scripts/i18n-lint.py` ara també les vigila (`faq-sense-traduccio`,
`faq-sense-resposta`), o sigui que una pregunta sense traduir surt a la mateixa
llista que una pàgina sense traduir.

### El que segueix bloquejat · 14 preguntes

Escrites, amb `pendent:`, i **no publicades enlloc, ni en català**. Val més cap
resposta que mitja. `python3 .github/scripts/generate-faq.py --pendents`.

**Vuit números de l'Ana** (7 de diners, 1 d'equipació): quant costa la
temporada per categoria, què inclou la quota, com es paga, descompte de
germans, si hi ha ajuts, què passa amb una baixa a mig any, i quina equipació
cal i quant val. Són les que més es busquen.

**Sis dades del club**: què vol dir equip A i equip B i qui ho decideix; quants
desplaçaments hi ha i qui hi porta els nens; per quin canal s'avisa una família
d'un canvi d'hora o de pista; què fer si un dia no pot anar a entrenar; si cal
revisió mèdica; qui és la persona de contacte de cada categoria; i com s'apunta
qui vol ser entrenador o voluntari.

### Dos temes oberts que no són d'aquesta llista

- **`/portes-obertes/` segueix sense `/es/` ni `/en/`.** Les seves cinc
  preguntes ja estan traduïdes al YAML i esperen la pàgina on viure. Avui, qui
  busca en anglès «what do we bring the first day» no troba res.
- **`scripts/i18n-lint.py` dona 91 errors, tots anteriors a aquesta feina** (hi
  eren igual abans de tocar res: comprovat comparant amb la branca neta). N'hi
  ha un que val la pena mirar perquè és una contradicció amb una decisió ja
  presa: el lint exigeix dir «Dies de partit per equip» a `/partits/calendaris/`,
  però `web-cbgb` §6 diu que l'etiqueta decidida per la direcció l'agost del
  2026 és **«Calendari»**. Sembla que `i18n/etiquetes.yml` va quedar amb el
  vocabulari antic.


---

## Arreglat el 23/08/2026 (tarda)

### Els 91 errors del lint eren un sol error, i el tenia la llista

`i18n/etiquetes.yml` i `i18n/diccionari.yml` s'havien quedat amb el vocabulari
anterior a la decisió de la direcció del club de l'agost del 2026, que va
canviar l'etiqueta a **«Calendari»** (i «Calendari per equip»). El lint
demanava el nom antic a 91 pàgines que ja feien servir el nou: **la web tenia
raó i la llista, no.**

Corregits els dos fitxers i passat `scripts/i18n-aplica-etiquetes.py`. De
passada ha sortit una cosa que el lint no podia veure: **el castellà i l'anglès
s'havien quedat amb el nom antic** («Días de partido», «Match days») mentre el
català ja deia «Calendari» a 240 enllaços. Ara les tres versions diuen el
mateix: **Calendari · Calendario · Calendar**, i **Calendari per equip ·
Calendario por equipo · Calendar by team**. Són 203 enllaços de 150 pàgines.

> És l'únic canvi d'aquesta tanda que es veu a la navegació del web, i és
> reversible: es desfà tornant els dos fitxers enrere i tornant a passar
> l'aplicador.

**El lint ha passat de 91 errors a 0.** Els pendents, de 497 a 392.

### /portes-obertes/ ja té les tres versions

Creades **`/es/puertas-abiertas/`** i **`/en/open-days/`**, amb la pàgina
sencera traduïda: text, formulari (mateixos identificadors, o sigui que
`/js/portes-obertes.js` hi funciona igual), avís de dades i preguntes. La
capçalera i el peu no s'han traduït a mà: els dibuixa `scripts/i18n_chrome.py`
des d'`i18n/diccionari.yml`.

Les seves **cinc preguntes ja surten en els tres idiomes**. Ara «what do we
bring the first day» troba resposta.

De passada, dues coses trencades a la pàgina catalana:
- Els seus `hreflang` apuntaven a `/es/portes-obertes/` i `/en/portes-obertes/`,
  que no han existit mai.
- **El commutador d'idioma portava a un article del blog**
  (`/blog/a-quina-edat-comencar-basquet/`), no a la pàgina. Error de copiar i
  enganxar.

També s'ha afegit `/portes-obertes/` a `llms.txt`, on no hi era.

### El que segueix pendent, i per què

Les **14 preguntes amb `pendent:`** no s'han pogut escriure perquè la seva
resposta no és a cap pàgina del web ni la sap ningú d'aquí: vuit són números
(les quotes i l'equipació) i sis són dades de funcionament del club (equip A i
B, desplaçaments, canal d'avisos, revisió mèdica, coordinació per categoria,
voluntariat). Inventar-les seria pitjor que no tenir-les.

Queden **27 pàgines amb les FAQ desquadrades entre idiomes**. Passar-les per la
font única és mecànic i es pot fer en tandes; la primera, `/basquet-formatiu/`,
ja està feta i va de 5/5/4 a 7/7/7.


---

## Preguntes freqüents · tancat el 23/08/2026

**Les 28 pàgines desquadrades ja no existeixen.** Totes les preguntes del web
han passat per `i18n/faq.yml`, i les 98 pàgines amb FAQ tenen el `<details>`
visible i el `FAQPage` del JSON-LD quadrats, amb exactament un `FAQPage` per
pàgina. Cap pàgina amb versió traduïda té un nombre de preguntes diferent del
català.

| | Abans | Ara |
|---|---|---|
| Preguntes indexades pel cercador | 493 | **546** |
| Pàgines desquadrades entre idiomes | 28 | **0** |
| Errors del lint d'i18n | 91 | **0** |
| Traduccions que falten i tenen on anar | 42 | **0** |
| Portada | 15 / 11 / 11 | **15 / 15 / 15** |

Comprovat que la migració no ha canviat cap contingut: **0 preguntes
perdudes i 0 respostes canviades sota la mateixa pregunta**, comparant l'índex
de cerca abans i després.

### El que va costar, per si torna a passar

- **Aparellar, no perdre.** El perill no era perdre una pregunta —això es
  compta— sinó publicar la resposta d'una sota una altra en un altre idioma.
  `scripts/faq-migra.py` alinea com un diff, respectant l'ordre, i es nega a
  fer-ho quan l'ordre no encaixa.
- **Dues pàgines no eren traduccions.** A `/femeni/` i a
  `/blog/cultura-esforc-club-progres/` el castellà i l'anglès tenien
  preguntes DIFERENTS, no les mateixes traduïdes. S'han fet a mà: cap resposta
  s'ha descartat, i on faltava la contrària s'ha escrit.
- **La portada es va duplicar i es va desfer.** El migrador buscava
  `class="faq"` exacte i la portada la tenia com a `class="faq reveal"`: hi va
  crear una segona secció i durant una estona va ensenyar les quinze
  preguntes dues vegades. Trobat obrint-la al navegador i comparant els
  `<details>` visibles amb els del JSON-LD. Arreglat a les cinc pàgines
  afectades i al regex del migrador.

### El que segueix pendent

Les **14 preguntes amb `pendent:`**, que no es publiquen enlloc perquè la seva
resposta no és a cap pàgina del web: vuit números (les quotes i l'equipació) i
sis dades de funcionament del club. `--pendents` les llista.


---

## Les 9 preguntes que falten · formulari per contestar-les (23/08/2026)

De les 14 que esperaven una dada, **cinc s'han pogut contestar** mirant millor
què sap el web, sense inventar-ne cap:

| Pregunta | D'on ha sortit la resposta |
|---|---|
| Quant costa la temporada? | No la xifra, però sí el que decideix una família: la prova és gratuïta, hi ha beques i el preu exacte de la seva categoria el té el mateix dia si escriu. |
| Quants partits es juguen fora de casa? | **De `partits/data.json`**: 274 partits, 137 a casa i 137 a fora, en 80 pistes. Ningú els havia comptat. |
| Com sé si canvia l'hora o la pista? | El robot diari, la marca «MODIFICAT» set dies i la subscripció `.ics`, que ja existien. |
| Hi ha beques o ajuts? | Ho deia `/femeni/`, on cap família ho busca. |
| Com puc ser entrenador o voluntari? | El canal del club + les 38 entrenadores en actiu + el certificat LOPIVI. |

**En queden nou, i totes demanen un sí o un no que no és enlloc del web.**
Contestar-les aquí és tot el que separa el cercador d'un 10: les redacto en
els tres idiomes el mateix dia.

### Diners · 5 preguntes

1. **Què inclou la quota?** Marca el que hi entra: fitxa federativa ☐ ·
   assegurança FCBQ ☐ · equipació ☐ · lloguer de pistes ☐ · altres:
2. **Com es paga?** Un sol pagament ☐ · mensual ☐ · trimestral ☐ ·
   Es domicilia? ☐ sí ☐ no
3. **Hi ha descompte per a germans?** ☐ sí, de _____ ☐ no
4. **Si es dona de baixa a mig any, què passa amb la quota?**
5. **Equipació:** què és obligatori comprar, què val i on es compra.

### Funcionament · 4 preguntes

6. **Equip A i equip B: què vol dir, i qui ho decideix?** (Hi ha proves de
   nivell? Ho decideix la direcció tècnica, la coordinació de la secció?)
7. **Si un dia no pot anar a entrenar, què s'espera de la família?**
   (Avisar l'entrenador? Per quin canal?)
8. **Cal revisió mèdica per federar-se?** ☐ sí ☐ no
   *(L'assegurança ja està resolta: la de la FCBQ, i ja està publicada.)*
9. **Qui porta els nens als partits de fora?** (Les famílies? Cotxes
   compartits? Hi posa transport el club?)

> Amb aquestes nou respostes, l'auditoria passaria de 75 consultes resoltes
> sobre 98 a prop de 90, i el bloc de diners —que és el que més es busca i el
> que fa marxar més gent— quedaria tancat.


---

## Decisió · els preus no es publiquen (23/08/2026)

**Decisió de l'Ana, presa i tancada.** Les quotes van per **franges d'edat i
per categoria**, i **no es publiquen al web**: fer-ho donaria als clubs del
voltant l'argument econòmic per competir amb el Barna pel preu. No es reobre.

### Com queda contestada, sense cap xifra

La pregunta «quant costa» segueix sent la que més es busca, i ara té resposta
sencera. El que una família necessita per decidir no és el número: és saber
que hi ha una estructura clara, que provar no costa res, que hi ha beques i
que el preu de la SEVA categoria el té el mateix dia si escriu.

> La quota va per franges d'edat i per categoria: l'Escoleta, els equips
> federats i el campus tenen preus diferents […] No publiquem la taula de
> preus al web, però te la donem de seguida: escriu-nos […] amb l'any de
> naixement i et diem la quota exacta que li tocaria, el mateix dia. Abans de
> decidir res, el primer entrenament és de prova i gratuït, i el club manté
> beques socials perquè cap infant es quedi fora per motius econòmics.

**Dir per què no hi és val més que ometre-la.** Un preu absent i sense
explicació sembla un oblit —o que hi ha alquna cosa a amagar—; dit així, és
una política, i la resposta acaba amb tres motius per venir igualment.

Les tres versions d'idioma diuen el mateix, i la pregunta porta les paraules
amb què es busca de debò: *apuntar-se*, *costa* i *temporada*.

### El que segueix faltant NO és el preu

Cinc de les nou pendents eren «de diners», i **cap necessita una xifra**:
necessiten la POLÍTICA, que no dona cap argument econòmic a ningú.

| Pregunta | Què cal, exactament |
|---|---|
| Què inclou la quota? | Si hi entren fitxa federativa, assegurança FCBQ, equipació i pistes. Serveix per comparar què hi ha inclòs, no per saber el preu. |
| Com es paga? | Un sol pagament, mensual o trimestral, i si es domicilia. **Poder pagar a terminis és sovint el que decideix**, i dir-ho no dona cap xifra. |
| Descompte per a germans? | Només si n'hi ha o no. «Sí, escriu-nos i te'l diem» respon sense publicar el percentatge. |
| Baixa a mig any? | La política. És una de les pors que frenen una família que dubta. |
| Equipació | Què és obligatori i on es compra. El preu es pot ometre igual que la quota. |

I quatre de funcionament, que tampoc tenen res a veure amb diners: equip A i
equip B, faltar a un entrenament, revisió mèdica i qui porta els nens als
partits de fora.


---

## Tancat · les nou preguntes, contestades (24/08/2026)

L'Ana les va contestar totes. **Cap pregunta del web queda sense resposta.**

| | Resposta publicada |
|---|---|
| Què inclou la quota? | Tot, excepte l'equipació, que va a part |
| Com es paga? | **Mensualment**, i l'import depèn de l'edat i la categoria |
| Descompte per a germans? | **Sí** (el percentatge, no; es diu escrivint) |
| Baixa a mig any? | La temporada es paga sencera |
| Equipació | Va a part; **ho explica qui porta la inscripció**, sense preu al web |
| Equip A i equip B | L'any de naixement decideix la categoria; dins d'una categoria, **l'entrenador** decideix segons el nivell |
| Faltar a un entrenament | Avisar l'entrenador; **amb el justificant de la família n'hi ha prou** |
| Revisió mèdica | **Sí, i la gestiona el club: és gratuïta per a les famílies** |
| Desplaçaments | **Les famílies**, organitzant-se entre els pares del mateix equip |

### Tres coses que val la pena mirar

- **La revisió mèdica gratuïta i gestionada pel club era un actiu amagat.**
  És una fricció que altres clubs deixen a la família (buscar-la, pagar-la,
  demanar dia) i aquí no existeix. Ara ho diu la web.
- **El pagament mensual, també.** Poder-ho pagar a terminis és sovint el que
  decideix una família que dubta, i no dona cap argument econòmic a ningú.
- **L'equip A i B** s'ha redactat perquè no soni a divisió entre qui val i qui
  no: són la mateixa categoria en competicions diferents, tothom entrena,
  tothom juga i es pot canviar al llarg de la formació.

### Wintym · no s'anomena, i menys s'enllaça (24/08/2026)

**L'Ana avisa que aquesta és l'última temporada amb Wintym**: les famílies ja
han comprat l'equipació d'enguany i el club ha de negociar una marca i un
disseny nous.

Per això la resposta de l'equipació **no diu cap nom de proveïdor**. Parla de
«la botiga oficial del club» i remet al moment en què es dona la plaça, que és
quan la família ho necessita saber de debò. Així la resposta segueix sent
certa el dia que canviï la marca, i no cal recordar-se d'anar-la a buscar.

> **Regla que val per a tot el web:** un nom de tercer dins d'una resposta és
> una data de caducitat amagada. Si el que la família necessita és *com*
> aconseguir una cosa, la resposta ha de dir el «com», no el «qui».

**El preu tampoc hi és** (24/08/2026, decisió de l'Ana): cap xifra al web, i
ho explica la persona que porta la inscripció quan es dona la plaça. Amb la
marca nova el preu canviarà igualment, i així la resposta no caduca.

### Inventari de preus que SÍ segueixen publicats

La norma «cap preu al web» val per al que paga una família per jugar: quota i
equipació. Però al web hi ha altres xifres, i convé saber-ho per decidir si la
norma les abasta o no. **No s'han tocat: són decisions anteriors.**

| On | Xifra | Què és |
|---|---|---|
| `/campus/`, `/campus-basquet-barcelona/`, `/campus/setmana-santa/` | 195 € / 160 € / 150 € | Preu del campus, per setmana i per jornada |
| `/3x3/`, `/3x3-barcelona/` | 2.000 € en premis | Premi del torneig, paritari |
| `/patrocinadors/` | des de 300 € l'any | Nivells de patrocini |
| `/blog/basquet-femeni-…/` | 140.000-160.000 € | Pressupost anual del club, com a argument de posicionament |

Els tres últims no són el que paga una família per jugar. **El del campus
sí**, i és el cas que caldria decidir: avui el campus es ven amb el preu
davant —i el preu és, de fet, un dels seus arguments— mentre que la temporada
no en diu cap. Si la norma ha de valer també per al campus, es treu en un
moment; si no, val la pena que quedi escrit per què no.

### On queda el cercador

| | Al començar | Ara |
|---|---|---|
| Consultes provades | 85 | **109** |
| Amb resposta a dalt de tot | 46 | **90** |
| Només amb enllaços | 36 | **17** |
| Sense cap resultat | 2 | **0** |
| Preguntes pendents d'una dada | 14 | **0** |

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

## Els quatre punts que quedaven per decidir · resolts el 23/08/2026

L'Ana va demanar tancar-los tots. Això és el que s'ha fet i per què.

### 1. El dossier del Premi demanava un PIN i alhora era al sitemap

Hi havia **dues reixes**, no una: les tres portades (`/premidonaesport/` i les
seves versions `/es/` i `/en/`) portaven, a més de la d'`assets/js/auth.js`, una
segona reixa de quatre caselles escrita dins de l'HTML, amb **el mateix codi** i
una clau de sessió diferent. Qui hi arribava havia de teclejar 1965 dues vegades
seguides per entrar al mateix lloc. I qui no el tenia es quedava en un carreró
sense un sol enllaç.

Ara la porta és una: la d'`auth.js`, que cobreix les 72 pàgines del dossier,
reconeix les dues claus antigues (ningú no ha de tornar a entrar-hi), **surt en
l'idioma de la pàgina** —abans sempre en català— i ofereix una sortida a qui no
té el codi: la pàgina pública de bàsquet femení de cada idioma.

Sobre l'indexació: **no s'ha obert el dossier** —això és una decisió de
contingut— però s'ha desfet la contradicció. Les 72 pàgines porten
`noindex,follow` i les seves **69 adreces han sortit del `sitemap.xml`** (de 433
a 364). Ningú no arribarà des d'una cerca a una paret amb un PIN. Si algun dia es
vol obrir, és treure el `<script>` d'`auth.js` i tornar-les a posar al sitemap.

També s'ha corregit `llms.txt`, que descrivia aquest corpus com a «obert i sense
registre» quan no ho és. Ara diu que aquest mirall demana codi i assenyala les
dues versions realment obertes: la web oficial de la candidatura i `/femeni/`.

### 2. El vídeo de la mascota en castellà

`/es/mascota/` ja serveix `mascota-reel-es.mp4`, que era al repositori sense fer
servir. Els rètols del vídeo no són una transcripció de la veu: són targetes en
pantalla, i per tant es poden traduir. Se n'han fet dos `.vtt` nous
—`subtitols-es.vtt` i `subtitols-en.vtt`— amb els mateixos temps que l'original.
`/en/mascota/` segueix amb el muntatge català, que és l'únic que hi ha, però ara
amb els rètols en anglès per defecte i el català com a segona pista.

> **Per confirmar mirant-lo:** el fitxer castellà no s'ha pogut obrir des d'aquí
> per comprovar-ne l'àudio. El nom, la durada (90 s contra els 80 s del català) i
> el germà `-es-capcut.mp4` diuen que és el doblatge, però val la pena veure'n
> deu segons abans de donar-ho per fet.

### 3. Les portades en castellà i en anglès

Tenien el commutador Franges/Extensa, però **l'extensa quedava buida**: hi
faltaven set blocs que només existien en català. Ara hi són tots, traduïts:

- el **masthead** («CB Grup Barna · Bàsquet a Barcelona des de 1965»), amb els
  cinc pilars i les dues crides;
- la capçalera **«La portada»** amb la data del dia, en castellà i en anglès;
- la franja de **paritat**;
- el bloc del lema, **Cultura del Progrés**;
- **El Barna per dins**, amb les tres portes;
- **l'Observatori Barna**, amb tres guies del blog;
- i la secció **Presentacions**.

Pel camí van sortir dues coses més:

- **Cap de les dues portades tenia un `h1` visible a la vista per defecte.** El
  titular de les franges era un `<h2>` i l'únic `h1` vivia en un bloc que només
  surt a l'extensa. Ara les tres portades es comporten igual: un `h1` visible a
  cada vista.
- El titular de la fitxa de l'Escoleta era un segon `h1` («Escoleta de
  baloncesto»), que a més era el que Google llegia com a títol de la portada.
  Ara és un `h2`, com en català.

I una que afectava les tres: **la primera franja no es podia llegir a mòbil**.
La graella manté tres columnes fixes —190 px de foto, el text i la crida de la
dreta, que no parteix—, i a 390 px al text li quedaven vint píxels: queia una
paraula per línia. És la primera cosa que veu qui entra des del mòbil. Per sota
de 700 px la crida ara baixa sota el text.

### 4. El contrast del vermell

Repassat amb el navegador, no a ull: 72 pàgines dels tres idiomes, comparant el
color de cada text amb el fons **compositat** de sota (les capes translúcides
menteixen si es miren pel seu compte). Hi havia **38 combinacions** per sota del
mínim AA. Ara no en queda cap.

El sistema ja tenia la resposta escrita i no s'aplicava:

| On | Abans | Ara |
|---|---|---|
| Text vermell petit sobre crema | `--red` #E20613 · 4,37:1 | `--red-ink` #A8040E · 6,93:1 |
| Text vermell sobre tinta | `--red` #E20613 · 3,87:1 | `--red-light` #FF3B41 · 5,40:1 |
| Botó vermell dins d'un article | tinta sobre vermell · 3,87:1 | blanc · 4,92:1 |

Aquell botó era un cas d'especificitat de manual, del que avisa la guia visual:
`.prose a` (0,1,1) guanyava a `.btn` (0,1,0), i qualsevol botó dins d'un article
es quedava amb el text en tinta i un subratllat que no li tocava.

I quatre pàgines fosques feien servir els grisos pensats per a fons clar:
`/jugadors/` (#6B6560 sobre tinta, 3,32:1), `/presentacions/` (un gris fix que
ignorava el seu propi mode fosc), `/galeria-3x3-glories/` (#2e2e2e sobre negre,
**1,39:1** — text que directament no es veu) i `/mascota/` (blanc sobre el verd
de WhatsApp, 1,98:1). El verd de WhatsApp és seu i s'hi queda; el que ha canviat
és el text, que ara hi va en tinta.

---

## Tercera passada · el que va sortir mirant més endins (23/08/2026)

Amb els punts grossos tancats, un repàs a coses que no es veuen llegint el codi:
dades estructurades, teclat, pantalles de 320 px i pes de pàgina.

### Dades estructurades: 45 pàgines deien a Google que eren en català

El JSON-LD de `/es/` i `/en/` portava `"inLanguage": "ca-ES"` copiat de
l'original. Afectava tot el blog traduït, les fitxes de partner, premsa i les
tres portades. A més, `WebPage` i `FAQPage` declaraven la llista dels tres
idiomes, que només té sentit al node `WebSite`: el lloc és trilingüe; una
pàgina concreta, no. Els 439 blocs de JSON-LD del repositori queden validats i
amb l'idioma correcte.

El generador que ho provocava (`scripts/i18n-munta.py`) només traduïa la forma
curta (`"ca"`), no la llarga ni la llista. Ara les cobreix totes tres, i la
llista la resol llegint el JSON per no tocar el node `WebSite`.

### Teclat

Els camps de text del formulari de la portada anul·laven el contorn de focus i
el substituïen per un filet d'un píxel que només canvia de color. Amb teclat ara
recuperen el contorn vermell de la resta del web; amb ratolí segueix sortint
només el filet. Revisat tabulant de debò per 24 pàgines: no queda cap element
focusable sense indicador visible.

**La galeria no es podia fer servir amb el teclat.** Les caselles de `/fotos/`
eren `<div>` amb un `click` i prou: no s'hi podia arribar ni obrir cap foto, i
un lector de pantalla no les anunciava com a res. Ara són botons de debò, amb
etiqueta («Obrir la foto 3 a pantalla completa»), i s'obren amb Enter o espai.
El visor mou el focus al botó de tancar en obrir-se, el manté a dins mentre es
fa servir i el torna a la mateixa foto en tancar-se.

### Pantalles de 320 px

Sis famílies de pàgina hi desbordaven. El cas més gros era **l'avís de
galetes**: feia 342 px d'ample en una pantalla de 320 i el botó d'acceptar
sortia partit. És la primera cosa que es toca en entrar.

La causa de fons no era la barra. Hi havia contingut més ample que la pantalla,
el navegador eixamplava la finestra de disseny, i la barra —que és
`position: fixed`— l'heretava:

- les cinc estrelles de la valoració (5 dianes de 44 px i les separacions) no hi
  cabien amb els marges de la targeta;
- les capçaleres de `/es/` i `/en/` no retiraven el nom del club, com sí que fa
  la catalana;
- a `/presentacions/` el botó de mode clar/fosc quedava fora de pantalla, sense
  manera d'arribar-hi;
- a `/fotos/` l'enllaç de tornada sortia de la pantalla;
- les files de `/#acces` no cabien en una línia.

Cap diana tàctil baixa dels 44 px: el que s'estreny és l'aire, i el que es
retira són etiquetes que ja diu l'`aria-label`.

### Pes

Cinc imatges es servien senceres, sense `srcset`, en pàgines on mai es mostren a
més de 700 px. `hero-equip.jpg` feia 2100 px i 468 KB per a un marc de 348. És
la regla del sistema de disseny llegida per l'altra banda: si cap foto no s'ha
de mostrar més gran del que és, tampoc no se n'han de baixar més píxels dels que
caben. `scripts/build-imatges-responsives.py` en fa versions WebP a 400, 800 i
1400 px —mai per sobre de l'original— i els `<img>` ja les demanen.

| Pàgina | Abans | Ara |
|---|---|---|
| `/presentacions/` | 1.146 KB | 242 KB |
| `/patrocinadors/` | 548 KB | 240 KB |
| `/3x3/` | 439 KB | 226 KB |
| `/premsa/` | 407 KB | 231 KB |

I `/mascota/` arrencava el vídeo sol. Pesa entre 31 i 50 MB i, arrencant, es
baixa sencer. Ara només ho fa si el vídeo és a pantalla i si qui mira no ha
demanat menys moviment ni té l'estalvi de dades activat.

> **Pendent, i això no és codi:** el reel de la mascota hauria de sortir
> re-codificat. Un vertical de 90 segons no hauria de passar de 10-12 MB, i ara
> en fa 31 (català) i 50 (castellà).

---

## Per decidir (redactat el 23/08/2026, abans de resoldre'ls) — vegeu més amunt

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

## 24-08-2026 — El vídeo de la mascota no arrencava

**Símptoma que veia la gent:** entres a `/mascota/` i no hi ha vídeo. Ni un
fotograma, ni la durada, res: un rectangle buit.

**Causa real:** `mascota/mascota-reel.mp4` era l'únic MP4 del web amb l'índex
(`moov`) DESPRÉS de les dades (`mdat`). Ordre dels àtoms: `ftyp, free, mdat,
moov`. Un navegador no pot pintar res fins que no té l'índex, i amb l'índex al
final això vol dir baixar-se els 30 MB sencers primer. Verificat també en
producció amb `curl -r 0-63`, o sigui que no era cosa de la branca.

**Arreglat:** `scripts/mp4-faststart.py` (qt-faststart en Python pur, sense
dependències). Mou el `moov` al davant i reescriu totes les taules de posicions
`stco`/`co64`. En el cas del reel: 3758 posicions desplaçades 61075 bytes,
totes comprovades byte a byte abans d'escriure. Mida final idèntica i contingut
de vídeo (`mdat`) idèntic — no és una reconversió, és una reordenació.

Comprovats tots els MP4 del repositori: la resta ja tenien l'índex al davant.

**Encara pendent per l'Ana (no es pot fer des d'aquí):** els reels pesen massa.
30 MB el català i 48 MB el castellà per a 90 segons verticals; ben codificat
haurien de ser 10–12 MB. Cal reexportar-los, no reordenar-los.

## 24-08-2026 — Fora el vídeo de la mascota

Decisió de l'Ana: la pàgina de la mascota es queda sense vídeo, en els tres
idiomes.

No n'hi havia prou amb treure l'etiqueta `<video>`. També se n'han anat:

- els comandaments que només servien per al reproductor (botó de reproduir,
  botó de so, l'avís de «Toca per sentir la veu») i tot el seu JavaScript;
- les etiquetes que anunciaven un vídeo a fora — `og:video`, `twitter:player`,
  `og:type: video.other` i `twitter:card: player` —, perquè si no, WhatsApp i
  X continuarien intentant reproduir-ne un que ja no hi és;
- el JSON-LD, que declarava un `VideoObject` amb durada i URL del fitxer. Ara
  és un `WebPage`;
- el CSS que vestia tot això.

**El marc del hero era vertical** (480×848) perquè hi anava un reel 9:16. La
foto de la mascota que tenim és apaisada, i encabir-la-hi retallada donava un
primer pla il·legible. El marc passa a apaisat (750×500) i hi va
`img/blog/clot-mascota@2x.webp`, amb `srcset` per no servir el doble del que
es veu.

Comprovat amb navegador a 390 px en els tres idiomes: cap `<video>`, cap error
de JavaScript, cap petició fallida, res que desbordi, i el commutador d'idioma
damunt la foto a 5,87:1 de contrast. **La pàgina passa de ~62 MB transferits a
133 KB.**

**Pendent de decidir:** els cinc MP4 de `mascota/` (186 MB en total) ja no els
enllaça cap pàgina. Es queden al repositori fins que l'Ana digui, perquè són
els originals; però cada desplegament els ha d'empaquetar.

## 24-08-2026 — Fora també els vídeos del repositori

Decisió de l'Ana. Traguda la reproducció de la pàgina, els fitxers ja no els
enllaçava ningú i cada desplegament els havia d'empaquetar.

Esborrats de `mascota/` (180 MB):

| Fitxer | Mida |
|---|---|
| `mascota-reel-es-capcut.mp4` | 48,2 MB |
| `mascota-reel-es.mp4` | 48,1 MB |
| `mascota-reel.mp4` | 30,2 MB |
| `mascota-teleprompter.mp4` | 38,6 MB |
| `mascota.mp4` | 14,1 MB |
| `subtitols.vtt`, `subtitols-es.vtt`, `subtitols-en.vtt` | els subtítols dels vídeos |

Abans d'esborrar es va buscar cada nom per tot el repositori: cap pàgina,
full d'estil, guió ni el `sitemap.xml` no en referencien cap. Les úniques
mencions eren prosa d'aquest document i un comentari de
`scripts/mp4-faststart.py`, que és una eina general i no en depèn.

**Com recuperar-los si mai calen:** són a l'historial de git, al commit
`c589e7f4`. Amb `git show c589e7f4:mascota/mascota-reel.mp4 > mascota-reel.mp4`
en surt qualsevol, byte a byte.

## 24-08-2026 — El que queda obert d'aquesta tanda de traducció

Tres coses apuntades i no fetes, perquè cap de les tres és una decisió tècnica:

- **Redirect de L'Aquàrium de Barcelona.** Quan es va esborrar el partner, les
  seves tres fitxes (`ca`, `es`, `en`) van passar a 404. GitHub Pages no fa
  redireccions de servidor, així que l'única manera és una pàgina estàtica amb
  `<meta http-equiv="refresh">`, que ja és el mecanisme que fem servir a la
  resta del web per a aquest cas (vegeu `web-cbgb`). No s'ha fet perquè no hi
  ha cap enllaç conegut, intern ni extern, que hi apunti — les tres fitxes
  només sortien del propi `partits/` i del sitemap, i totes dues coses ja
  estan netes. Si l'Ana sap d'algun enllaç extern (una nota de premsa, un post
  antic) que encara hi porti gent, avisa-ho i es posa el redirect en cinc
  minuts.
- **Logotip de la Wilson**, ja apuntat més amunt, a «Pendent de material de
  l'Ana».
- **La skill `mapa-web-cbgb` parla d'una desincronització que ja no existeix.**
  Diu que `/femeni/` és «encara sense traduir» com a exemple del que passa
  quan es toca una pàgina catalana i no es reflecteix a `/es/` i `/en/`. Des
  d'aquesta tanda, `/femeni/` està traduïda sencera i, sobretot, ja no cal fer
  aquesta comprovació a mà: `i18n-paritat.py` i `i18n-contingut.py` ho vigilen
  soles a cada `push` i bloquegen el pull request si es desincronitza. Cal
  actualitzar aquell paràgraf perquè no enviï a ningú a buscar un problema que
  ja no hi és.

## 24-08-2026 — Comença el versionat: `VERSION` i `CHANGELOG.md`

Fins ara l'única manera de dir «això és el que hi havia publicat en tal data»
era el missatge d'un commit. A partir d'ara hi ha una versió amb nom:
**1.0.0**, fixada al commit `205f0861` — el cercador intel·ligent, ja
publicat i comprovat.

**Com queda.** `VERSION`, a l'arrel, porta el número. `CHANGELOG.md` en porta
l'explicació i la convenció, a l'estil habitual `MAJOR.MENOR.PEDAÇ`: un pedaç
per un arreglo o contingut nou que no canvia com funciona res, un menor per
una funcionalitat que s'afegeix sense trencar la que ja hi havia, un major
per un canvi de com es fa servir la web o el repositori. Cada versió nova
puja `VERSION`, hi afegeix l'entrada a `CHANGELOG.md` i es publica a `main`
en el mateix commit.

**Per què no és un tag de git.** Es va intentar primer amb un tag anotat
(`v1.0-cercador`): el `git push` del tag el va rebutjar GitHub amb un 403, i
no hi ha cap eina de GitHub disponible en aquesta sessió per crear-ne un per
API. Un fitxer dins del repositori no depèn d'aquest permís i, de retruc,
queda a l'historial de qualsevol clonatge sense haver de demanar els tags a
part.

**Norma confirmada per l'Ana:** a partir d'ara, cada vegada que es tanqui una
feina es puja la subversió corresponent (`VERSION` + entrada a
`CHANGELOG.md`) en el mateix commit, sense haver-ho de demanar cada cop.

---

## Accessibilitat · 24/08/2026

Passada d'accessibilitat de tot el lloc, mesurada amb axe-core sobre el lloc
servit i comprovada amb teclat a 1280 i 390 px. La declaració pública és a
**`/accessibilitat/`** (`/es/accesibilidad/`, `/en/accessibility/`), enllaçada
des del peu de totes les pàgines i llistada a `llms.txt` i al `sitemap.xml`.

Aquesta passada s'ha fet en paral·lel a «Auditoria d'experiència d'usuari als
tres idiomes» (#78), que ja va arreglar de forma independent bona part del
mateix terreny: els 38 combos de color per sota d'AA d'aleshores, el peu en
castellà/anglès sense columna Legal, el `lang-switch` amb `aria-current` i
`lang` per enllaç, i la navegació per teclat de la galeria. El que segueix és
el que quedava sense cobrir després d'aquella auditoria, mesurat de nou amb
axe-core sobre l'estat actual.

### Fet

- **`css/a11y.css`** — capa compartida, enllaçada des de totes les pàgines
  reals i carregada l'última perquè les seves regles manin: focus visible de
  3 px (amb `!important`, perquè hi havia una trentena de pàgines amb
  `outline:none` a l'atribut `style`), enllaç de salt, `prefers-reduced-motion`,
  mode d'alt contrast del sistema, `.visually-hidden` i les correccions de
  contrast que l'auditoria #78 no cobria.
- **Salt al contingut i `<main>`** a les pàgines que encara no en tenien
  (`scripts/a11y-aplica.py`, idempotent: es pot tornar a passar sempre).
- **~90 camps de formulari** amb nom accessible (`scripts/a11y-etiquetes.py`).
- **Contrast addicional**: `/admin/`, `/briefing/`, `/partners-mapa/`,
  `/mascota/`, `/opina/`, `/jugadors/`, `/fotos-3x3/`, `/fotos-esdeveniments/`,
  el mirall de `/premidonaesport/` (3 idiomes) i les fitxes de partner. Mateix
  criteri que l'auditoria #78: `#FF3B41` sobre fons foscos, `--red-ink` sobre
  fons clars, blanc pur sobre el vermell.
- **`<dt>`/`<dd>` dins d'una `<dl>` de debò** a les 21 fitxes de partner i al
  campus (abans, dins d'un `<div>` pla). `scripts/build-pages.py` i
  `scripts/build-campus-fitxa.py` corregits al mateix lloc.
- **Marcadors del mapa de partners amb nom** (`title`/`alt` a cada `L.marker`);
  iframes d'Instagram amb `title`.
- **PDF**: dels 7 documents enllaçats, 3 ja tenien l'arbre d'etiquetes complet.
  Als altres 4 (presentació de club, dossier de patrocinis, «El Barna amb
  dades» i el dossier de premsa orfe) se'ls ha posat `/Title` i `/Lang`, i els
  enllaços que en deien només «PDF» ara porten nom, pàgines i pes.
- **Vídeo d'`/opina/`**: no hi ha cap vídeo actiu (funcionalitat preparada i
  apagada). `setupVideo()` ara exigeix `CFG.video.captions` a més
  d'`enabled` i `src`, així que no es podrà activar mai sense subtítols.
- **Menús amb `aria-expanded`** i Escape que en retorna el focus; galetes amb
  el mateix comportament i el focus gestionat en tancar.
- **Comprovació repetible**: `scripts/a11y-revisa.py` passa totes les pàgines
  sense navegador (salt, `<main>`, `<h1>`, `alt`, formularis, iframes). Avui
  torna zero.

### Pendent

1. **PDF sense arbre d'etiquetes complet** (ordre de lectura, encapçalaments):
   la presentació de club, el dossier de patrocinis i «El Barna amb dades» són
   exportacions d'una eina de disseny sense accés en aquest entorn. Mentre no
   es refacin, l'alternativa accessible és la pàgina HTML equivalent, que ja
   existeix per a cadascun.
2. **`galeria/`** (l'app Next.js) no ha passat aquesta revisió.
3. **Pàgines de cartells i materials per imprimir** (`partits/cartell.html`,
   `opina/print/*`): generen una imatge, no es llegeixen. Queden fora.
4. Els calendaris per equip són imatges pures (`generate-calendaris.py`,
   Pillow): mai tindran text seleccionable; l'alternativa accessible és la
   fitxa HTML de l'equip i el fitxer `.ics`.
5. **`#pagLlista` del cercador** (`/cerca/`, `/404.html`, `/en/search/`,
   `/es/busqueda/`) — trobat amb axe-core, `aria-required-children`: un
   contenidor amb rol de llista sense cap `role="listitem"` a dins quan no hi
   ha resultats. És a `js/cerca.js`, la funcionalitat de cerca de #78/#84, no
   d'aquesta passada. No s'ha tocat perquè no hi ha cap ocurrència estàtica de
   `pagLlista` al repositori: es crea sencer en JavaScript en temps
   d'execució, i tocar-ho a cegues sense poder-ho provar a fons és més risc
   que valor. Queda apuntat perquè qui toqui `cerca.js` ho vegi.