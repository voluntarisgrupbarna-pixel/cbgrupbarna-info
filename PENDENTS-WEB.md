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
