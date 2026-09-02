# Pendents · CB Grup Barna (web i fora del web)

Fitxer unificat el 02/09/2026. Substitueix `PENDENTS-WEB.md` com a font única
de pendents: abans hi havia el que faltava al **web** en un fitxer
(`PENDENTS-WEB.md`) i el que faltava **fora del web** (fitxa de Google,
enllaços externs, altes a agendes, premsa) repartit en tres documents de
treball de màrqueting (`POSICIONAMENT-CAMPUS-SEO.md`,
`AUTORITAT-EXTERNA-CAMPUS.md`, `CAMPUS-FITXA-GOOGLE-I-AGENDES.md`). A partir
d'ara tot viu aquí, en dues parts.

**Abast:** aquest fitxer recull tots els pendents que han quedat escrits en
algun document del repositori `cbgrupbarna-info` — que és la memòria de totes
les sessions de Claude Code que han treballat en aquesta web fins avui. No té
accés a xats fora d'aquest repositori (per exemple, sessions d'altres eines o
converses que no s'hagin desat aquí): si hi ha un pendent que només existeix
al cap de l'Ana o en una altra eina, cal apuntar-lo aquí a mà perquè no es
perdi.

`PENDENTS-WEB.md` es manté com a redirecció curta cap a aquest fitxer, per no
trencar les referències que ja hi ha a `CHANGELOG.md` i a la skill
`mapa-web-cbgb`.

---

# PART 1 · Pendents del web (tècnic)

*Contingut migrat sencer des de `PENDENTS-WEB.md`. Auditoria del repositori a
14/08/2026, revisada amb les decisions de l'Ana i actualitzada sessió a
sessió fins al 30/08/2026.*

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
(abans el briefing i les dades oficials deien 68%), i l'adreça del club a **C/ Llacuna 170**
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

- **SEO · el problema no és el CTR, és el TIPUS de visita.** Export de Search Console
  analitzat el 30/08/2026 (`Queries.csv` + `Pages.csv`, propietat de DOMINI, compte del
  club u/1). Totals: 2.910 impressions, 49 clics, CTR 1,7%, posició 8,4 — però **només
  hi ha 11 dies de dades (18→28/08)**, la propietat és nova. Tot és provisional.

  **Diagnòstic:** tres articles informatius s'emporten el 40% de totes les impressions i
  gairebé cap clic, i arrosseguen la mitjana avall:

  | Pàgina | Impr. | Clics | Pos. |
  |---|---|---|---|
  | `/es/blog/a-quina-edat-comencar-basquet/` | 732 | **0** | 6,5 |
  | `/en/blog/que-es-basquet-3x3/` | 387 | 1 | 12,2 |
  | `/en/blog/a-quina-edat-comencar-basquet/` | 152 | 1 | 6,6 |

  Són consultes globals i informatives («what is 3x3», «how long is a 3x3 game», «edad
  cadete baloncesto») que Google respon al mateix resultat o a l'AI Overview: compten
  impressió i ningú clica. No porten famílies — porten trànsit d'Iran, Tailàndia, Japó
  i el món àrab. **No s'han d'optimitzar: s'han d'ignorar.**

  **On sí hi ha diners (i estem a pàgina 2):** 16 consultes de campus sumen 119
  impressions i **1 clic**, totes entre la posició 12 i la 16 — «campus basket barcelona»
  (26 impr, pos 14,6), «campus baloncesto barcelona» (20, pos 12), «campus de basket
  barcelona» (19, pos 14,4), «tecnificacion baloncesto barcelona» (17, **pos 57**).
  Les pàgines: `/es/campus/` pos 16,7 · `/campus/` pos 23,6 · `/en/campus/` pos 14,3.

  **El català guanya i ningú ho diria:**

  | Idioma | Impr. | Clics | CTR |
  |---|---|---|---|
  | CA | 906 | 27 | **2,98%** |
  | ES | 1.412 | 14 | 0,99% |
  | EN | 939 | 10 | 1,06% |

  El castellà té el 48% de les impressions i el 27% dels clics. La portada `/es/` fa 127
  impressions i 2 clics (pos 10,6) contra `/` amb 317 i 18 (pos 4,3).

  **La marca està sana:** «grup barna basquet» pos 2,06 amb CTR 17,6%, «grup barna» pos
  2,05, «club barna» pos 2. Qui ens busca, ens troba. El forat és qui **encara no ens
  coneix**.

  **A fer, per ordre:**
  1. **Campus a la 1a pàgina.** És l'única acció que porta inscripcions. Consolidar les
     pàgines de campus i atacar «campus basquet/baloncesto Barcelona». Passar de la
     posició 14 a la 4 en aquestes 3-4 consultes val més que tota la resta junta.
  2. **Auditar `/es/`.** Meitat de les impressions, un terç dels clics i pitjor posició
     que el català. Mirar si els `<title>`/`<meta>` en castellà són traduccions febles,
     i si l'`hreflang` reparteix bé.
  3. **Local, no global.** Reforçar «bàsquet base Sant Martí / Clot / Barcelona» i
     «escola de bàsquet per a nens Barcelona» (ja hi ha impressions soltes: «basketball
     for kids near me» pos 3, «escuela de basketball para niños» pos 4).
  4. **No tocar** els articles de 3x3 en anglès. Fan bonic al panell i no serveixen de res.

  **Dada per al dossier de patrocini:** les fitxes de partner posicionen pel nom propi
  del negoci — «nova farmacia clot» pos 5,2 (6 impr), «clinica bac de roda» i «dentista
  bac de roda» pos 9-10, «totsalut» pos 9. Argument directe de venda per a
  `dossier-patrocini-cbgb`: patrocinar el club els dóna SEO local.

  **Curiositat a vigilar:** apareixen consultes que són fragments de conversa («busca
  mas», «si porfavor», «mas opciones», «gib mir mehr infos», «cuando empieza», «hay
  foto ?»). Són sessions d'AI Mode / cerca conversacional. El `llms.txt` està fent
  feina; val la pena mesurar-ho a part.

  **🔴 Contingut duplicat entre idiomes: el 84% de les impressions.** El mateix contingut
  viu en 2-3 versions d'idioma que competeixen entre elles (2.739 impressions repartides
  en 19 slugs duplicats, 40 clics). Auditat `campus/index.html`: **no hi ha cap
  `hreflang`, només `canonical`**. Posar hreflang a les tres versions és la correcció
  d'un sol camp amb més impacte de tota la llista.

  **Auditoria de la pàgina de campus** (`campus/index.html`, 30/08/2026). Bé: títol,
  meta, H1, 1.088 paraules i JSON-LD ric (`Service`, `FAQPage`, `BreadcrumbList`…).
  Falta: (a) `hreflang`; (b) schema **`Event` + `Offer`** — hi ha secció de preus i
  «propera edició» visibles però sense marcar, i un campus és exactament el resultat
  enriquit d'esdeveniment que Google mostra; (c) **dates concretes indexables** (es
  busca «campus baloncesto 2025 barcelona» i «campus navidad barcelona»); (d) secció
  pròpia de **tecnificació** — «tecnificacion baloncesto barcelona» té 17 impressions i
  som a la **posició 57**; (e) `/campus-nadal-basquet-barcelona/` existeix, té **1 sola
  impressió** i no està enllaçat des de `/campus/`.

  **🔴 BLOQUEJANT:** al repo local només hi ha `campus/`. **No hi ha `es/campus/` ni
  `en/campus/`**, però totes dues existeixen a la live (136 i 21 impressions). Torna a
  confirmar que aquest repositori **no és la font de la web live**, i `/es/campus/` és
  justament la pàgina amb més potencial desaprofitat. **No es pot arreglar el campus
  editant aquest repo: cal localitzar primer la font real.**

  📄 **Anàlisi completa, amb totes les taules de dades:
  [`SEO-SEARCH-CONSOLE-2026-08.md`](SEO-SEARCH-CONSOLE-2026-08.md)** — evolució diària,
  pàgines, idiomes, duplicats, 113 països, dispositius, les 177 consultes per tema,
  auditoria del campus i pla d'acció ordenat.

  Export desat a: `~/Downloads/cbgrupbarna.info-Performance-on-Search-2026-08-30.zip`
  **Repetir aquesta anàlisi a finals de setembre**, quan hi hagi 3 mesos reals i s'hagi
  vist l'efecte de la campanya de captació.

## Pendent de material de l'Ana · descàrregues

- **Columna `newsletter` al full de càlcul.** La porta de descàrrega de PDF envia les
  dades al mateix Apps Script que la galeria del 3x3 (`action=register`), amb dos camps
  nous: `newsletter` (si/no) i el document demanat dins de `font`. Cal comprovar que
  l'Apps Script els desa en una columna pròpia; si no, queden només dins de `font`.
- **Butlletí:** encara no hi ha eina d'enviament (Mailchimp, Brevo o similar). De moment
  només es recull el consentiment; cal decidir amb què s'envia.

## 🔴 Trobat el 30/08/2026 · mentre s'investigava el SEO

### A. cbgrupbarna.info no respon des d'aquest ordinador

Comprovat el 30/08/2026 a la tarda:

```
cbgrupbarna.info          → DNS OK (188.114.96.5 / 188.114.97.5, Cloudflare)
                            però TCP a :443 i :80 fa TIMEOUT
cistella.cbgrupbarna.info → igual, no respon
cbgrupbarna.com           → HTTP 200 ✅
cbgrupbarna-3x3timechamber.com → HTTP 307 ✅
cloudflare.com            → HTTP 200 ✅   (descarta que sigui la xarxa d'aquí)
example.com               → HTTP 200 ✅
```

El domini **resol** cap a IP de Cloudflare, però aquestes IP no accepten connexió.
Els altres dominis del club funcionen des de la mateixa màquina i al mateix moment, o
sigui que **no és la connexió d'aquí**.

⚠️ **Cal verificar-ho des del mòbil amb dades (no wifi) abans de moure res.** Si també
falla, la web està caiguda.

Context que fa que corri: Search Console tenia impressions **fins al 28/08**, o sigui que
si està caiguda ho està des de fa molt poc. I **som a l'inici de la temporada i de la
captació de setembre**: és el pitjor moment possible per tenir la web principal fora.

**Diagnòstic ampliat (30/08/2026, confirmat també des del mòbil de l'Ana amb dades):**

```
cbgrupbarna.info                 NS: margo/zita.ns.cloudflare.com   → CLOUDFLARE
                                 A:  188.114.96.5 / 188.114.97.5    (IP de proxy CF)
                                 whois: ACTIVE   ·  SOA correcte    ·  DNS OK
                                 :443 timeout · :80 timeout · IPv6 timeout
                                 TLS: connect errno 60 (no arriba a saludar)
                                 la MATEIXA IP tampoc respon amb un altre Host
                                 → no és config del lloc: l'IP no contesta

cbgrupbarna-3x3timechamber.com   NS: dns97/dns98.servidoresdns.net  → ARSYS
                                 A:  216.198.79.1                    → VERCEL
                                 HTTP 307 ✅ funciona
```

**El domini no ha caducat i el DNS funciona.** El que no funciona és el servei que hi ha
darrere de les IP de Cloudflare.

**Conclusió: el problema és a CLOUDFLARE, no a Arsys.** El registre resol bé; el que falla
és que l'edge de Cloudflare no serveix la zona. A Arsys només hi ha **un camp que importi**:
els *name servers*, i ara mateix apunten correctament a Cloudflare.

**Comparació que ho aclareix:** el domini del 3x3, que **sí** funciona, no passa per
Cloudflare — fa servir els DNS d'Arsys apuntant directament a Vercel. I
`.vercel/project.json` diu que el projecte del `.info` també és a Vercel. O sigui que el
`.info` hauria d'estar servit igual que el del 3x3, i en canvi té una capa de Cloudflare
pel mig que ara no respon.

**Què mirar, per ordre:**

1. **Cloudflare** (compte propietari de la zona `cbgrupbarna.info`):
   - Estat de la zona: ha de dir **Active**. Si diu *Pending*, *Moved* o hi ha un avís de
     compte, aquí tens la causa.
   - Registres DNS: mirar cap a on apunta el registre arrel i si té el **núvol taronja**
     (proxy) activat. Si el proxy apunta a un origen de Vercel que ja no existeix, dóna
     exactament aquest símptoma.
   - Prova ràpida: posar el núvol en **gris** (DNS only). Si torna, era el proxy.
2. **Vercel** (projecte `prj_yD9VgtbA13GrIg8jPBKLTFjgG5u6`, equip
   `team_Pp23ffahzD4Myfhb675GAqfd`): estat de l'últim desplegament i si el domini
   `cbgrupbarna.info` hi segueix assignat.
3. **Arsys**: comprovar només que els NS segueixen sent
   `margo.ns.cloudflare.com` i `zita.ns.cloudflare.com`. No cal tocar res més.

**Pla B si s'ha perdut l'accés a Cloudflare:** replicar el que fa el domini del 3x3 —
canviar els NS a Arsys (`dns97`/`dns98.servidoresdns.net`) i apuntar el registre a Vercel,
saltant-se Cloudflare. ⚠️ Això propaga en 24-48 h i deixa la web fora mentrestant, o sigui
que **és l'última opció, no la primera**, i en plena captació de setembre val la pena
esgotar abans la via de Cloudflare.

Pistes addicionals:
- El DNS apunta a **Cloudflare**, però `.vercel/project.json` diu que el projecte és a
  **Vercel** (`prj_yD9VgtbA13GrIg8jPBKLTFjgG5u6`, equip `team_Pp23ffahzD4Myfhb675GAqfd`).
  Si el registre de Cloudflare està en mode *proxy* (núvol taronja) apuntant a un origen
  que ja no existeix, dóna exactament aquest símptoma.
- Mirar l'estat del deploy al panell de Vercel i el registre DNS a Cloudflare.

### B. `build-pages.py` esborraria els preus del campus

`campus/index.html` conté tres seccions que el generador **no** produeix: **«Preus»**,
**«El campus, en imatges»** i **«La seu»**. Es van afegir a mà. Executar
`python3 scripts/build-pages.py` les esborraria sense avisar — inclosos els preus
(**195 €** setmana completa / **160 €** mitja jornada) i l'adreça de La Nau del Clot.

Ja s'ha posat un **avís ben visible a la capçalera de `scripts/build-pages.py`** perquè
no passi. Queda pendent decidir: portar les tres seccions dins de `build_campus()`, o
treure `campus/` de les pàgines generades.

### C. El repositori local està desincronitzat de la live (confirmat)

Proves acumulades:
- `git fetch origin` **es penja** (espera credencials; lliga amb el bloqueig conegut de
  GitHub 2FA i amb el token mai revocat del punt de sota).
- El sitemap local només té **8 URL** sota `/es/` o `/en/`, i al disc només hi ha aquests
  8 fitxers. Però Search Console veu `/es/campus/` (136 impr.), `/es/3x3/`,
  `/es/escoleta/`, `/es/patrocinadors/`, `/es/partits/calendaris/`,
  `/es/grup-barna-dades-oficials/`, `/es/premidonaesport/…`, `/en/campus/`, `/en/partits/`,
  `/en/briefing/`… **cap d'elles és al repositori.**
- `/campus-nadal-basquet-barcelona/` té impressions a Google i **no existeix al disc**.

**Conclusió: no es poden arreglar les pàgines `/es/` i `/en/` des d'aquest repositori.**
Fins que no se sàpiga d'on surt la live, qualsevol edició aquí és a cegues.

### D. Estat real de l'`hreflang`

Només **14 fitxers** en tenen, i cobreixen únicament 4 parelles (bàsquet femení, el mètode,
protecció del menor i un article del blog). **No en tenen:** `campus/`, `3x3/`, `escoleta/`,
`patrocinadors/`, `partits/`, `grup-barna-dades-oficials/` — totes amb versió `/es/` i
`/en/` viva segons Search Console. I la portada declara només `ca` i `x-default`, sense
`es` ni `en`.

Això explica el 84% d'impressions en contingut duplicat de
[`SEO-SEARCH-CONSOLE-2026-08.md`](SEO-SEARCH-CONSOLE-2026-08.md).

**No s'ha tocat res**: posar `hreflang` cap a URL que no es poden verificar, amb la web
caiguda i el repositori desincronitzat, faria més mal que bé. Depèn de resoldre A i C.

### E. Correcció a l'anàlisi de SEO

Vaig escriure que «tecnificació» sortia un sol cop a `campus/index.html`. **Surt 8 cops.**
El problema de «tecnificacion baloncesto barcelona» (posició 57) no és que la paraula no
hi sigui: és que no té secció ni pàgina pròpia, i la consulta és **en castellà** mentre que
la pàgina forta és la catalana.

### F. Perfil de Google del club · 30/08/2026

Investigat el perfil de Google Business del club mentre es preparava un missatge per
demanar ressenyes a les famílies.

**Dades de la fitxa** (per no tornar-les a buscar):

| Camp | Valor |
|---|---|
| Nom a Google | C.B. Grup Barna |
| Place ID | `ChIJj-ZWRSSjpBIRHoeMjElc1nE` |
| CID | `8202845242262325022` |
| Adreça | Carrer de la Llacuna, 170, Sant Martí, 08018 Barcelona |
| Telèfon | 933 09 04 54 |
| Estat | **3,9 ★ · 190 ressenyes** |

**Enllaç per demanar ressenyes** (verificat, obre el formulari d'estrelles directament):
`https://search.google.com/local/writereview?placeid=ChIJj-ZWRSSjpBIRHoeMjElc1nE`

#### 🔴 F.1 · La fitxa NO està verificada — bloqueja tota la resta

El perfil és del club (surt «Gestiones este Perfil de Empresa»), però Google avisa:
«La fitxa no està verificada. És possible que alguns dels canvis que facis no siguin
visibles per als clients», i al gestor de ressenyes: **«Verifica el teu compte per
respondre a ressenyes»**.

Conseqüències mentre no es verifiqui:
- **No es pot respondre cap ressenya.** Hi ha 2 ressenyes noves i 2 de crítiques sense
  contestar.
- Els canvis del perfil (horaris, fotos, web) poden no arribar a mostrar-se.

Verificar a **https://business.google.com/verifications** — mètode vídeo in situ a la Nau
del Clot o telèfon. És el pas que desbloqueja tota la resta.

#### F.2 · Respostes a ressenyes ja redactades, pendents de publicar

Tres respostes escrites i llestes per enganxar quan es desbloquegi, totes signades
«Ana, coordinació — CB Grup Barna» i amb `voluntaris@cbgrupbarna.info` com a contacte:

1. **Cristina Alaminos Pérez** (⭐1, fa un mes) — Cistella Petita, competitivitat per
   damunt del desenvolupament. ⚠️ El text de la ressenya queda **truncat** sense sessió
   iniciada; llegir-lo sencer abans de publicar la resposta.
2. **«Mal educados / están mal enseñados»** — toca conducta cap a menors, així que la
   resposta remet explícitament al **canal de protecció del menor** (LOPIVI) del club,
   `voluntaris@cbgrupbarna.info`.
3. **Jordi Gili** (⭐4, fa 6 dies, Local Guide amb 285 ressenyes) — positiva, en català,
   destaca la secció femenina. Val la pena contestar-la aviat.

Regles fixades: mai el nom de l'entrenador, del jugador ni de l'equip concret; mai
«això no és cert» ni «ja ho vam parlar amb vostè».

#### 🔴 F.3 · Dades de contacte descuadrades a quatre fonts

Quatre llocs públics diuen quatre coses diferents. Cal decidir el joc de dades canònic i
unificar-lo:

| Font | Telèfon | Correu |
|---|---|---|
| Fitxa de Google | 933 09 04 54 | — |
| Guia Barcelona / barcelona.cat | 688 26 52 30 | coordinaciocbgrupbarna@gmail.com |
| cbgrupbarna.com (WordPress) | 688 26 52 30 | cbgrupbarna@gmail.com |
| Badgie | +34 933 09 04 54 | 30cbgrupbarna@gmail.com |

**Decisió ja presa:** el correu públic del club és **`voluntaris@cbgrupbarna.info`**, que
és també el canal per a situacions de protecció del menor. Cap dels gmail antics s'ha de
fer servir en comunicació pública.

Pendent: corregir-ho a la fitxa de Google, a la Guia Barcelona (cal escriure al Districte),
a Badgie i a cbgrupbarna.com — aquest últim bloquejat perquè no hi ha accés a wp-admin.

#### F.4 · Google Ads · compte `747-139-0991` — decidit: NO tocar

Penja del Gmail personal d'Ana (anafernandezduran78@gmail.com), amb l'alta **incompleta**.
- **No hi ha saldo.** Els «400 € de crèdit» són promo condicionada: gastes 400 € i te'n
  donen 400. No és diner regalat.
- Hi ha un esborrany d'anunci autogenerat i **fora de marca**: *«CLUB DE BASQUET GRUP
  BARNA - Eleva tu Fitness / Equipos de última generación y entrenadores expertos»*,
  apuntant a `cbgrupbarna.com` en lloc de `.info`. No s'ha publicat mai.
- La targeta «Termina de crear la campanya» del perfil **no es pot descartar** (no té menú
  ⋮). L'única manera de treure-la seria cancel·lar el compte d'Ads.
- **Decisió d'Ana (30/08/2026): deixar-ho com està.** El compte és inert — sense mètode de
  pagament, sense campanya activa, risc de despesa zero.
- Qualsevol despesa en Ads (400 €) és **decisió de junta**, no d'Ana en solitari.

#### F.5 · Ordre recomanat

1. Verificar la fitxa (gratis) ← desbloqueja tot
2. Enviar el missatge de ressenyes a les famílies (ja es pot fer, no depèn de verificar) —
   individual, 10-15 al dia, no al grup gran
3. Respondre les ressenyes pendents + pujar fotos
4. Unificar les dades de contacte (F.3)

---

## 📱 Proves de mòbil en els 3 idiomes · 30/08/2026

Fetes a **375×812 (iPhone)** servint el repositori a `localhost` (la web live no responia,
vegeu el punt A). Provades les **4 pàgines que existeixen en les tres llengües**, ×3
idiomes = 12 pàgines: bàsquet femení, el Mètode, protecció del menor i l'article de blog
de formació/competitiu.

Recordatori del perquè: **el 65% de les impressions i el 73% dels clics són de mòbil**, i
al mòbil posicionem 3 llocs millor que a escriptori (7,37 vs 10,41).

### ✅ El que està bé

- **Cap desbordament horitzontal** en cap idioma ni cap plantilla: `scrollWidth` = 375 px
  exactes a les 12 pàgines. La pàgina no es mou de costat enlloc.
- **`hreflang` perfecte** on hi és: les 4 parelles declaren `ca` / `es` / `en` /
  `x-default`, **totes amb auto-referència**, i coincideixen amb el `canonical`. Ben fet.
- **`lang` i `og:locale` correctes** a cada versió (`ca`/`ca_ES`, `es`/`es_ES`,
  `en`/`en_US`).
- **Títols i descripcions traduïts de veritat**, no calcats: «Bàsquet femení a
  Barcelona» / «Baloncesto femenino en Barcelona» / «Women's Basketball in Barcelona».
  Longituds entre 41 i 70 caràcters — dins del que Google ensenya.
- `viewport` correcte a totes. Imatges amb `width`/`height` (cap salt de layout).

### ⚠️ El que falla — igual a les 12 pàgines (és de plantilla)

1. **El selector d'idioma és el botó més petit de la pàgina: 15 px d'alçada.**
   `català` 34×15 · `castellano` 59×15 · `English` 42×15.
   El mínim recomanat és 44×44 (Apple) o 48×48 (Google). **Amb el dit no s'encerta.**
   És irònic: la peça que serveix per canviar d'idioma és la que pitjor funciona al mòbil,
   i el castellà és justament la llengua que rendeix pitjor a Google.
2. **Menú de navegació a 9,5 px.** «CLUB», «Escoleta», «Patrocinadors», «Campus»,
   «Màgics», «3x3» i «CB GRUP BARNA» (10 px). Google ho marca com *text massa petit per
   llegir-lo*. El text del cos sí que està bé (16 px).
3. **Molla de pa de 14 px d'alçada**: `INICI` 30×14 · `INICIO` 39×14 · `HOME` 34×14 ·
   `BLOG` 31×14.
4. **6-7 objectius tàctils per sota del mínim a cada pàgina**, en els tres idiomes.
5. **Menor:** la capçalera es parteix en dues línies en català («DIES DE PARTIT») i en
   castellà («DÍAS DE PARTIDO»); en anglès («MATCH DAYS») hi cap. En castellà l'avanttítol
   també passa a dues línies («PUERTAS ABIERTAS AHORA»). No trenca res, però es veu
   desendreçat.

> Cap d'aquests problemes és d'idioma: **són tots de la plantilla compartida**. Es
> corregeixen una vegada al CSS i queden arreglades les tres llengües alhora.

### 🔴 I una cosa que no és de mòbil, però ha sortit provant

### ✅ RESOLT · La xifra de dones a l'staff tècnic (68% → 65,5%)

Les pàgines de bàsquet femení i del Mètode publicaven **68%** mentre que la resta del lloc
deia **65,5%** (la xifra de la candidatura al 19è Premi Dona i Esport).

**L'Ana ha confirmat el 30/08/2026 que la bona és 65,5%.** Unificat a **6 fitxers, 15
ocurrències** — descripcions, `og:description`, JSON-LD i el bloc de dades visible:

| Fitxer | Canvis |
|---|---|
| `basquet-femeni/index.html` | 4 |
| `basquet-femeni/el-metode-barna/index.html` | 1 |
| `es/baloncesto-femenino/index.html` | 4 |
| `es/baloncesto-femenino/el-metodo-barna/index.html` | 1 |
| `en/womens-basketball/index.html` | 4 → `65.5%` (decimal anglès) |
| `en/womens-basketball/the-barna-method/index.html` | 1 → `65.5%` |

Ara **23 fitxers** diuen 65,5% i cap en diu 68 com a estadística.

⚠️ **Correcció d'una anàlisi anterior:** vaig dir que 11 fitxers deien 68% i que dos es
contradeien a si mateixos. **Era fals.** Els 5 fitxers de `presentacio/` i `presentacions/`
tenen `68%` dins d'un `radial-gradient` de CSS (`transparent 68%`), que no té res a veure
amb la dada. Els fitxers afectats de debò eren 6, i cap es contradeia.

**Pendent fora del web:** revisar si la xifra 68% surt en materials ja repartits (PDF de
patrocini, dossiers, xarxes). Al repositori ja no hi és.

---

## Pendent de decisió

- **🔴 Token de GitHub sense revocar.** El 30/08/2026 es va enganxar un Personal Access
  Token al xat de Claude Code per fer canvis urgents (admin de fotos, galeria, marca).
  S'ha fet servir i esborrat del disc, però **mai s'ha revocat**. Cal:
  1. Revocar-lo a github.com/settings/tokens
  2. Crear-ne un de fine-grained nou, limitat a `cbgrupbarna-info`, `Contents: Read and write`
  3. Guardar-lo xifrat a `/admin/token.html` amb la contrasenya del club — i no tornar-lo
     a enganxar mai en text pla enlloc.
- **Els tres àudios de `/premidonaesport/patrocinis/`** (`musica.mp3`, `veu-jugadora.mp3`,
  `mix.mp3`) no són al repositori **ni a la web oficial** (comprovat: 404). La pàgina obre
  amb un overlay «Activa el so · 2 minuts» que depèn d'ells, o sigui que l'experiència
  sonora no funciona. Cal pujar els arxius o treure l'overlay.
- **`/escoleta/basquet-nens-clot/` (30/08/2026):** nova landing de captació, ja amb
  l'estètica real del club (Anton/Inter, vermell #E20613, mateixa capçalera/peu que la
  resta del lloc — la primera versió, feta en un altre artefacte amb Barlow Condensed +
  Lora, no encaixava). Pendent que Ana confirmi:
  - Anys de naixement de Premini, Mini, Preinfantil, Infantil i Cadet (temporada 26-27)
  - Quota mensual de l'Escoleta i si hi ha matrícula
  - Mesos d'inici i final de temporada
  Un cop confirmat, buscar i reemplaçar els `___` de l'HTML. La resta (edats 4-8, horari
  Dc/Ds, alumni) surt de dades ja publicades a `/escoleta/`.
- **`/jugadors/`:** encara no està acabat. Quan hi hagi plantilla, cal omplir
  `jugadors/jugadors.js` i canviar el «Temporada 2025-2026» de la pàgina.
- **`/briefing/`:** encara diu «Temporada 2025-26». Decidir si es refà per a la 26-27 o es
  deixa com a document tancat de la temporada passada.
- **Abans del 5 de setembre:** hi ha 274 partits carregats (05/09/26 → 16/05/27) i cap
  resultat. Convé provar amb un partit jugat de debò que el robot de la FCBQ, les fitxes
  descarregables, els 16 `.ics` i el cartell del cap de setmana funcionen.
- **🔴 `git fetch` es penja en aquest repositori (30/08/2026).** El `push` funciona bé,
  però `git fetch origin main` no acaba mai: es queda a `git index-pack --stdin
  --fix-thin --pack_header=2,32249` i s'hi està minuts sense progressar (provat sis
  cops, també en segon pla i amb el credential helper del `gh`). Això bloqueja qualsevol
  cosa que necessiti comparar amb `origin/main` — per exemple resoldre conflictes de
  merge. Sospita: el repositori té molts objectes (32.249 en un sol pack) i desenes de
  branques `claude/…` acumulades. Val la pena provar `git gc --aggressive`, esborrar
  branques remotes ja fusionades, o reclonar amb `--filter=blob:none`.
- **PR #120 (article Time Chamber, CA/ES/EN) té conflicte amb `main`.** No s'ha pogut
  resoldre per culpa del punt anterior. Els PR #122 (vídeos del campus) i #124 (landing
  de l'Escoleta) sí que es poden fusionar sense conflicte.
- **Vuit fitxers modificats i sense committejar al repositori local (30/08/2026),**
  d'una altra sessió: `basquet-femeni/index.html`,
  `basquet-femeni/el-metode-barna/index.html`, `es/baloncesto-femenino/` (2 fitxers),
  `en/womens-basketball/` (2 fitxers) i `scripts/build-pages.py`. Decidir si es
  committegen o es descarten abans que es perdin o entrin en un commit equivocat.

## Sense acció

- **Esdeveniments «passats»** (3x3 Glòries, Mes de l'Orgull, Campus Time Chamber,
  Little Basket Day): són esdeveniments anuals del club i es queden com estan.

## ✅ Fet el 30/08/2026 · les quatre portades i el generador d'equips (aquesta sessió)

En producció via PR #121, #123 i #125: la campanya de Portes Obertes sencera
(calendari de reserves amb comptador real, motor d'Apps Script pendent de
desplegar per l'Ana, avís a tot el web), la proposta B a `/partits/` i
`/partits/calendaris/`, el menú reorganitzat, la portada C («La Jugada») a
l'Escoleta, la D («L'Edició») a la newsletter amb la plantilla i el número 1
per a Brevo (`docs/newsletter/`), l'article de Portes Obertes als tres
idiomes, la cadència setmanal pertot i les 12 redireccions sense `noindex`.

**Tanda 4 — `generate-team-pages.py`, al dia i executat.** Era l'últim
blocatge tècnic: el generador esborrava el commutador d'idioma, els
`hreflang`, `a11y.css` i el `theme-color` de les 48 fitxes de
`/partits/equips/`. Ara ho emet tot i, a més, **cada fila de partit porta
l'escut del Barna i el del rival**: el nou `scripts/escuts_partits.py`
resol el nom FCBQ contra l'inventari de `partits/logos/` (map → alias →
emparellament automàtic, provant també el nom sense sufixos d'equip).
119 de 120 rivals amb escut; l'únic sense (CB Mollet B) surt amb
inicials. Per afegir-ne un: PNG a `partits/logos/clubs/`, alta a
`index.json` i, si cal, l'àlies a `alias.json`.

---

# PART 2 · Pendents fora del web (autoritat externa i captació)

*Consolidat el 02/09/2026 a partir de `POSICIONAMENT-CAMPUS-SEO.md`,
`AUTORITAT-EXTERNA-CAMPUS.md` i `CAMPUS-FITXA-GOOGLE-I-AGENDES.md`. Aquests
tres documents es mantenen com a "com es fa" (textos llestos, missatges
tipus, calendari de paraules clau); aquí només hi ha la llista de pendents
en si, perquè no calgui rellegir 700 línies per saber què falta fer.*

## 1 · Google Business Profile

- [ ] Confirmar que la fitxa està **verificada** (bloqueja respondre ressenyes
  i que els canvis es vegin — mateix punt F.1 de la Part 1). Verificar a
  https://business.google.com/verifications.
- [ ] Completar/revisar: categoria principal `Club deportivo`, categories
  secundàries, adreça, àrea de servei, telèfon, web, enllaç de
  «Cita/Reserva» (`/campus/` en temporada, `/#info` la resta de l'any), any
  d'obertura 1965, atributs (accessible, apte per a nens, entitat sense
  ànim de lucre).
- [ ] **Horaris** a la fitxa (falten, ho avisa també l'auditoria del web) +
  horari especial de campus (9:00-17:00 les setmanes d'edició).
- [ ] Descripció ca/es enganxada (textos ja escrits a
  `CAMPUS-FITXA-GOOGLE-I-AGENDES.md`).
- [ ] Donar d'alta els **7 serveis** (Escoleta, equips federats, bàsquet
  femení, campus d'estiu, tecnificació de Nadal/Setmana Santa, Barna
  Màgics, 3x3 Westfield) amb la seva descripció curta i enllaç.
- [ ] Pujar **mínim 10 fotos** amb els originals del repositori (no
  captures d'Instagram) en l'ordre recomanat (logo → portada → exterior La
  Nau → interior pista → campus → equip femení) i **renovar-les cada
  edició**.
- [ ] Publicar les **6 preguntes i respostes** precarregades (preu, cal ser
  del club, places, edat mínima, ubicació, Nadal/Setmana Santa) — textos
  llestos al document.
- [ ] Calendari de publicacions: febrer (obertura inscripcions estiu), cada
  setmana d'edició (foto + focus tècnic), setembre (recap), octubre
  (obertura inscripcions Nadal — la publicació més rendible de l'any),
  Setmana Santa.

## 2 · Ressenyes de Google

- [ ] Un cop verificada la fitxa: **respondre les 2 ressenyes noves i les 2
  crítiques pendents** (textos ja redactats, punt F.2 de la Part 1).
- [ ] Convertir l'enllaç curt de ressenya en **QR** (`scripts/qr.py`) i
  imprimir-lo per posar-lo a la porta de la Nau.
- [ ] Instaurar la **rutina setmanal**: missatge de WhatsApp (textos ca/es
  ja escrits) cada divendres de setmana de campus, no en fred.
- [ ] Objectiu de temporada: **30-40 ressenyes noves**. Respondre sempre en
  menys de 48 h, també les dolentes.
- [ ] Unificar les **dades de contacte** (telèfon/correu) a la fitxa de
  Google amb les de la resta de fonts — mateix pendent que F.3 de la Part 1.

## 3 · Altes a agendes i directoris institucionals

- [ ] **Guia d'activitats d'estiu de l'Ajuntament de Barcelona** — alta a la
  convocatòria (gener-febrer).
- [ ] **Districte de Sant Martí** — agenda i butlletí (tot l'any, 3-4
  setmanes d'antelació).
- [ ] **FCBQ** — fitxa de club actualitzada + inclusió al llistat de campus
  (gener-març).
- [ ] **Fundació del Bàsquet Català** — alta al llistat de campus i casals
  (gener-març).
- [ ] **Consell de l'Esport Escolar de Barcelona** — fitxa d'entitat
  (setembre).
- [ ] **Portals de famílies** (Sortim amb Nens, Time Out Kids Barcelona i
  similars) — formulari o correu de premsa (febrer-abril).
- [ ] **Xarxa d'equipaments del barri** (centres cívics, biblioteques, AFA
  de les escoles del Clot i Camp de l'Arpa) — cartell A4 i correu
  (abril-maig per l'estiu, novembre per Nadal).
- [ ] **Agendes de Nadal** del Districte i portals de família
  (octubre-novembre) — **no enviar el correu fins que hi hagi dates i preu
  confirmats** de l'edició de Nadal.

Correus tipus per a cadascuna ja escrits a
`CAMPUS-FITXA-GOOGLE-I-AGENDES.md` §3.

## 4 · Enllaços externs — «Onada 1» amb els partners (la més rendible)

- [ ] Demanar l'enllaç des del web (o, si no en tenen, menció a fitxa de
  Google / bio d'Instagram) als **23 partners**, escalonat en missatges
  setmanals (5 dilluns, 5 dimecres) i seguiment als 15 dies. Missatges
  tipus ja escrits.
  - [ ] **Centre Bac de Roda** (renovat) — enllaç a cbgrupbarna.info
  - [ ] **Globasket** (renovat) — enllaç a `/campus/`
  - [ ] **Nova Farmàcia Clot** (sense web) — publicació a la fitxa de
    Google + enllaç a la bio d'IG + cartellet amb QR al taulell
  - [ ] Els altres 20 partners de la llista
- [ ] Objectiu realista: **12-15 enllaços de 23 demanats**.
- [ ] Registrar cada petició a `autoritat-externa-targets.csv` (qui, quan,
  què es va demanar, resposta) perquè no es dupliqui ni es deixi ningú
  sense demanar.

## 5 · Institucional i federatiu (Onada 3 — mateixos targets que el punt 3)

Ja recollit al punt 3; l'única diferència és l'enfocament «enllaç/menció»
en lloc de «alta a agenda». Es fa amb el mateix correu.

## 6 · Premsa de barri i portals de família (Onada 4)

- [ ] Enviar la **nota de premsa tipus** (ja redactada, amb la dada dels
  ~150 participants del campus) a: Guia Clot, Eix Clot, betevé (districtes),
  El Periódico / La Vanguardia (edició de barris), Sortim amb Nens, Time
  Out Kids Barcelona, Barcelona Secreta, revistes d'AFA del Clot i Camp de
  l'Arpa.
- [ ] Repetir-ho **cada edició** (estiu, Nadal, Setmana Santa) amb la dada
  actualitzada.

## 7 · L'entitat als ulls de Google i les IA (Onada 5)

- [ ] **Crear l'ítem de Wikidata** del club (nom, tipus, any de fundació,
  ubicació, web, esport) — es fa en mitja hora, cal citar fonts (premsa de
  barri, fitxa FCBQ), per això va **després** del punt 6.
- [ ] **Wikipedia**: esperar a tenir articles de mitjans independents abans
  de crear-la (si es crea massa aviat amb fonts febles, s'esborra i deixa
  mal historial).
- [ ] Donar d'alta el club, amb el **NAP idèntic** (Carrer de la Llacuna,
  170-172 · 08018 Barcelona · +34 698 425 153 · marqueting@cbgrupbarna.info),
  a: Apple Business Connect, Bing Places, Facebook, camp d'adreça
  d'Instagram, Foursquare, OpenStreetMap.

## 8 · Ex-jugadors i entrenadors formats al club (Onada 6)

- [ ] Fer **entrevistes al blog** (deu minuts, telèfon o àudios) a gent
  formada al Clot i avui professional: **Javier Torralba** (entrenador,
  València Basket Femení), **Ainhoa López** (capitana, Spar Girona),
  **Roger Fornas** (pivot, ACB/LEB Or), **David Mejía** (campió Tercera
  FEB). Missatge tipus ja escrit.
- [ ] Demanar als gabinets de premsa dels seus clubs actuals que, quan els
  entrevistin, mencionin la seva formació al CB Grup Barna.
- [ ] Nota a la FCBQ quan algun d'ells ascendeixi o guanyi algun títol,
  recordant la formació al club.

## 9 · Cadència i seguiment

- [ ] Instaurar **una hora setmanal** dedicada a autoritat externa (pla de
  7 setmanes ja escrit a `AUTORITAT-EXTERNA-CAMPUS.md`: partners → partners
  + seguiment → Google Business → premsa → directori institucional →
  entrevista → repetir amb els que no han contestat).
- [ ] Mesurar mensualment: dominis que enllacen (Search Console), nombre i
  data de l'última ressenya, presència citada a Google AI Mode / ChatGPT /
  Perplexity amb «campus bàsquet Barcelona» i «campus baloncesto
  Barcelona» (les fonts que hi surtin citades marquen els targets del mes
  següent).

## 10 · Campus de Nadal — calendari per a l'octubre

- [ ] **Octubre:** confirmar dates i preu de l'edició de Nadal, omplir-los
  a la pàgina `/campus-nadal-basquet-barcelona/` (ca i es), afegir el node
  `Event` al schema (plantilla ja escrita a
  `POSICIONAMENT-CAMPUS-SEO.md`), actualitzar `lastmod` al sitemap i el
  bloc de Nadal a `llms.txt`.
  - [ ] Publicació a Google Business Profile.
  - [ ] Correu a agendes de districte i portals de família amb l'activitat
    de Nadal (punt 3, un cop hi hagi dates confirmades).
- [ ] **Novembre:** recordatori a IG i post a Google. Comprovar a Search
  Console que la pàgina ja rep impressions per «campus navidad baloncesto
  barcelona».
- [ ] **Desembre:** fotos de l'edició pujades a la mateixa pàgina (prova
  social per a l'any següent).
- [ ] **Gener:** treure les dates passades, deixar la pàgina en mode
  «propera edició», no esborrar-la mai (la URL ha d'acumular historial).

## 11 · Auditoria SEO de la pàgina de campus (`campus/index.html`)

Ja recollit al detall a la Part 1 («Pendent de desenvolupar · SEO»), es
repeteix aquí per no perdre'l entre els pendents fora del web: falta
`hreflang`, schema `Event`+`Offer`, dates concretes indexables, secció
pròpia de tecnificació i enllaçar `/campus-nadal-basquet-barcelona/` des
de `/campus/`.

## Repetir aquesta anàlisi

- [ ] **Finals de setembre 2026:** repetir l'anàlisi de Search Console amb
  3 mesos reals de dades i veure l'efecte de la campanya de captació
  (mateix punt que la Part 1).
