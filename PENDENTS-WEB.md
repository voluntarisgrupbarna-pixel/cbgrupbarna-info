# Temes pendents · cbgrupbarna.info

Auditoria del repositori a 14/08/2026, revisada amb les decisions de l'Ana.

---

## Fase 1 · tancament aquesta setmana (19/08/2026)

Decisió de l'Ana: **Organigrama queda per a una altra fase**; aquesta setmana
es tanca Fase 1 amb CRM, SEO, GEO, UX i Patrocinadors. Estat ara mateix:

| Àrea | Estat | Nota |
|---|---|---|
| Legal (privacitat, cookies, RGPD als formularis) | ✅ Fet | Veure secció "8" de `## ✅ Fet` |
| GBP + missatgeria + NAP identificat | ✅ Fet (sessió paral·lela) | Detall a `INTEGRACIONS-PENDENTS.md` |
| SEO — schema `SportsActivityLocation` a les 6 instal·lacions | ✅ Fet avui | Abast reduït (no 6 landings noves) |
| UX — blocs web i schema de l'arxiu 03 | ⏳ Pendent de rebre el contingut | No es pot avançar sense l'arxiu |
| Patrocinadors — plantilla de dashboard de retorn | ✅ Fet avui | `/patrocinadors/dashboard/` — `noindex`, no enllaçada, dades d'exemple |
| CRM — Brevo connectat als 6 formularis | ⏳ Pendent clau API + accés a l'Apps Script | Codi ja llest, veure `INTEGRACIONS-PENDENTS.md` |
| GEO — bateria de 12 preguntes llançada | ⏳ Pendent que algú amb accés a ChatGPT/Perplexity/Gemini la llanci | Bateria ja escrita |
| Astro per a la migració d'arquitectura | ✅ Decidit (Fase 3, no ara) | — |

Capacitat confirmada: 2 h/dia, cada dia (~14 h/setmana).

---

## Nota de maduresa · proposta "Web 10" (19/08/2026, corregida el mateix dia)

Puntuació pròpia d'aquest repositori, 0–10. **No és una certificació externa ni
s'ha de publicar a cap pàgina pública**: mostrar una nota d'autoavaluació a
famílies o patrocinadors fa més mal que bé. És un marcador intern per fer
seguiment del progrés cap a "web 10".

⚠️ **Correcció:** la primera versió d'aquesta nota es va basar en
`MIGRACIO-WEB-ANTIGA.md` (14/08) sense contrastar-la amb el repositori actual.
En verificar-ho directament, la política de privacitat, l'avís legal, el banner
de cookies (`js/galetes.js`, actiu a 98 pàgines) i l'enllaç al protocol de
menors **ja existien** — no eren un forat. El que sí que era real: dos dels sis
formularis (`/fotos/` i `/galeria-3x3-glories/`) recollien dades sense casella
de consentiment. **Ja s'han arreglat avui** (checkbox + enllaç a política de
privacitat, obligatori per enviar el formulari). `/premidonaesport/` no és un
formulari de dades, és un gate de PIN numèric: no calia tocar-lo.

**Nota actual: 5,6 / 10** (era 4,9; el pilar legal puja de 2 a 8)

| Pilar | Nota | Per què |
|---|---|---|
| GEO / IA generativa | 8 | `llms.txt` + `robots.txt` obert a bots d'IA — gairebé cap club de base ho té |
| Confiança / legal | 8 | Privacitat, avís legal i cookies publicats; els 6 formularis ja tenen consentiment |
| Contingut | 7 | Blog amb FAQ+schema, landing femenina, història i dades oficials |
| SEO local | 6 | JSON-LD, hreflang i sitemap sòlids; falta GBP i landing per instal·lació |
| Arquitectura | 5 | Estàtica i desplegada, però HTML clonat a mà en 3 idiomes i fotos al repositori |
| UX / Producte | 4 | Sense PWA real, àrea de família ni cercador intern |
| Dades / Martech | 4 | GA4 carregat però sense dashboard ni CRM unificat |
| Monetització | 3 | Sense botiga ni dashboard de retorn per a patrocinadors |

**Objectiu:** 10/10, en tres fases (Fundació → Infraestructura → Producte). Detall
complet — diagnòstic, els vuit pilars, full de ruta i backlog priori tzat — a la
proposta "Web 10" treballada amb l'Ana. **Lliçó:** puntuar sempre contra el
repositori real, no contra un document d'auditoria que pot haver quedat vell.

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
(abans el briefing i les dades oficials deien 68%), i l'adreça del club a **C/ Llacuna 172**
(53 ocurrències en 27 fitxers deien 170), seguint la candidatura.

### 7. `noindex` a l'eina interna

`fotos/migrar-flickr.html` ja porta `noindex, nofollow` com la resta d'admins.

### 8. Consentiment RGPD als dos formularis que en faltaven (19/08/2026)

Auditant els sis formularis que recullen dades personals (llista original a
`MIGRACIO-WEB-ANTIGA.md`), quatre ja tenien casella de consentiment enllaçada a
`/politica-de-privacitat/`: portada, `/fotos-3x3/`, `/fotos-esdeveniments/3x3-westfield-2026/`
i el propi `/politica-de-privacitat/`. En faltaven dos:

- **`/fotos/`** (formulari de subscripció per correu): afegida casella de
  consentiment i validació obligatòria a `submitSubscription()` — el botó ja no
  envia res si no està marcada.
- **`/galeria-3x3-glories/`** (nom, cognoms, correu, mòbil, club): mateixa
  casella, i `rgpd` afegit com a condició a `validateGate()`.

`/premidonaesport/` es va revisar i **no calia tocar-lo**: l'única entrada de
tipus `tel` que té és un gate de PIN numèric de 4 dígits, no un formulari que
reculli dades de contacte.

### 9. Google Business Profile, baseline GEO i CRM (Brevo) — 19/08/2026

Detall complet, paquet de contingut per al GBP, la bateria de 12 preguntes GEO
i el codi de l'Apps Script per sincronitzar tots els formularis amb Brevo:
**`INTEGRACIONS-PENDENTS.md`**. Resum: cap dels tres es pot tancar sense una
acció de l'Ana (login a Google, llançar les preguntes a les IA, o donar la
clau API de Brevo) — tot el que jo podia deixar fet, ja hi és.

Troballa important d'aquesta revisió: **el NAP del club no és consistent**.
`guia.barcelona.cat` i `barcelona.cat/metropolis` (fitxes de l'Ajuntament)
tenen adreça, telèfon i correu vells (C/ Llacuna 170, 688 26 52 30,
coordinaciocbgrupbarna@gmail.com) enfront de l'oficial actual (172, 698 425
153, info@cbgrupbarna.com). Cal demanar-ne la correcció abans de donar d'alta
el GBP.

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
