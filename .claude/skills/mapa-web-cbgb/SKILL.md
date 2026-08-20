---
name: mapa-web-cbgb
description: Mapa complet de cbgrupbarna.info i satèl·lits — què hi ha (totes les seccions, idiomes i pàgines) i com està construït (stack, generadors, robots de GitHub Actions, hosting, fonts de dades). Carrega-la sempre que calgui saber on viu un contingut, quin fitxer o script el genera, com s'actualitza sol, quina és la font de veritat d'una dada, o abans de proposar una pàgina/secció nova per no duplicar el que ja existeix o el que ja s'ha decidit en contra. Complementa web-cbgb, que dona el sistema visual (colors, tipografia, fotografia), no l'inventari ni l'arquitectura.
---

# Mapa · cbgrupbarna.info

Inventari de contingut + arquitectura tècnica del web del club. `web-cbgb` diu
**com s'ha de veure** una peça; aquesta skill diu **què hi ha ja** i **com
funciona per dins**, perquè no es proposi de nou el que ja existeix, no es
trenqui un automatisme sense saber-ho, i es toqui la font real de cada dada.

---

## 0. Els tres documents que cal llegir abans de proposar res nou

Aquest repositori porta la seva pròpia auditoria viva, en català, a l'arrel:

- **`llms.txt`** — l'índex de contingut oficial, pensat perquè humans i IA
  entenguin la web sense navegar-la. És la **font de veritat del que existeix
  i de les dades de contacte**. S'actualitza cada vegada que es publica o es
  retira una pàgina.
- **`PENDENTS-WEB.md`** — auditoria de temes oberts amb data, ja revisada amb
  les decisions de l'Ana: què falta material, què està pendent de decidir, i
  què **s'ha decidit expressament que no es fa** (p. ex. no enllaçar Wintym,
  Flickr ni Facebook; `/femeni/` és la canònica i `/basquet-femeni/` hi
  redirigeix). Llegir-lo evita reobrir un debat ja tancat.
- **`MIGRACIO-WEB-ANTIGA.md`** — comparativa amb l'antiga web WordPress
  (`cbgrupbarna.com`), amb el que ja s'ha migrat i el que encara falta
  (documents històrics amb data concreta, zona de socis, botiga).

Si la tasca és «fes una pàgina de X» o «per què no tenim Y», mira primer aquí:
pot ser que ja hi sigui, que s'hagi decidit expressament que no, o que estigui
anotat com a pendent d'un material concret de l'Ana.

---

## 1. Arquitectura general

**HTML/CSS/JS estàtic al nucli, sense framework.** No hi ha `package.json` a
l'arrel ni build step per a les pàgines del club: cada `.html` és el fitxer
que es serveix. Allotjat a **GitHub Pages**, domini propi via `CNAME`
(`cbgrupbarna.info`).

- **`css/barna.css`** — full d'estils compartit per totes les pàgines
  generades i moltes de manuals (campus, 3x3, blog, patrocinadors, femení).
  Els tokens de color/tipografia hi són descrits a `web-cbgb`.
- **`fonts/`** — Anton i Inter en local (no Google Fonts en producció).
- **`data.json`** (arrel) — CMS lleuger en JSON: `club`, `temporada`,
  `campus`, `tres_x_tres`, `events`, `contactesClub`, `patrocinadors`,
  `xarxes`. Porta el seu propi camp `_howToUpdate` amb instruccions. És la
  font per a peces que necessiten dades del club fora del propi HTML.
- **Tres idiomes**: `ca` a l'arrel (idioma per defecte), **`/es/`** i
  **`/en/`** com a carpetes mirall. **No és un framework d'i18n**: cada
  traducció és un fitxer HTML independent que cal actualitzar a mà. Quan es
  canvia una pàgina en català, comprovar si `/es/` i `/en/` en tenen còpia i
  si cal reflectir-hi el canvi (sovint no es fa i queden desincronitzades —
  vegeu el cas `/femeni/` a `PENDENTS-WEB.md`, encara sense traduir).

---

## 2. Què es genera sol i què es manté a mà

| Contingut | Com es manté | Fitxer/script |
|---|---|---|
| Portada `index.html` | **A mà.** Lògica pròpia, no la toca cap generador. | — |
| `/escoleta/` | **A mà.** Lògica pròpia. | — |
| `/partits/` (calendari, resultats) | **A mà** l'estructura; **robot diari** les dades | vegeu §3 |
| Blog, `/campus/`, `/3x3/`, `/premsa/`, `/patrocinadors/` | **Generades** per un script Python | `scripts/build-pages.py` |
| `/partits/equips/{id}/` (15 fitxes d'equip) | **Generades** cada dia | `.github/scripts/generate-team-pages.py` |
| `/partits/calendaris/` (imatge/PDF per equip) | **Generades** cada dia, només si han canviat | `.github/scripts/generate-calendaris.py` |
| `/partits/calendaris/ics/` (.ics per equip) | **Generat** cada dia | `.github/scripts/generate-ics.py` |
| Bloc `SEO-SNAPSHOT` / `SEO-EVENTS` / `SEO-EQUIPS` dins `partits/index.html` i `calendaris/index.html` | **Reescrit només entre aquests marcadors**, la resta és segur tocar-la a mà | `.github/scripts/generate-seo-snapshot.py` |
| `og-image.jpg` | **Manual**: cal regenerar-la després de canviar la portada | `python3 .github/scripts/generate-og-image.py` |

**⚠️ Trampa coneguda** (heretada de `web-cbgb` §7): `scripts/build-pages.py`
**està desfasat** respecte al publicat — executar-lo sense mirar el diff pot
revertir un repàs d'SEO i un article escrits a mà. Sempre: edita el
generador, no la sortida directa, i revisa el `git diff` sencer abans de
desar.

---

## 3. Robots de GitHub Actions (automatismes que corren sols)

Quatre workflows a `.github/workflows/`:

- **`update-partits.yml`** — el robot més important. Cada dia a les 06:00
  UTC, i cada 20 minuts entre les 08:00-21:00 (hora BCN aprox.) els caps de
  setmana: baixa el calendari de la **FCBQ** (`basquetcatala.cat`, club 24),
  el compara amb `partits/data.json`, actualitza hores/pistes/resultats,
  marca «MODIFICAT» 7 dies si canvia un partit ja publicat, i encadena en
  cascada `generate-calendaris.py` → `generate-seo-snapshot.py` →
  `generate-ics.py` → `generate-team-pages.py`. Fa commit i push només si hi
  ha canvis reals. Si la FCBQ no respon, no passa res: la via manual
  `/partits/` → Gestió segueix activa.
- **`update-counters.yml`** — actualitza comptadors (script
  `.github/scripts/update-counters.py`).
- **`build-gallery-images.yml`** — processa imatges per a les galeries de
  `fotos/`.
- **`deploy-galeria.yml`** — desplega l'app `galeria/` (vegeu §4), separada
  de la resta del lloc.

**Conseqüència pràctica:** `partits/data.json` no s'edita a mà de forma
duradora — el robot diari el sobreescriu. Si cal corregir-hi alguna cosa,
fer-ho a la font (FCBQ) o esperar el cicle, no pedaçar el JSON.

---

## 4. Sub-aplicacions amb stack propi (no és tot HTML pla)

El repositori conté peces amb tecnologia diferent de la resta, cadascuna amb
el seu propi cicle de vida:

- **`galeria/`** — app **Next.js 14 + React 18 + Supabase + Tailwind**, amb
  el seu propi `package.json`. Es desplega amb `deploy-galeria.yml`, no amb
  un simple push de fitxers estàtics. Si cal tocar-la, cal `npm install` /
  `next dev` dins d'aquesta carpeta, no editar HTML a mà.
- **`patrocinis/`** i el bundle `assets/_vinext_fonts` + `assets/*.js`
  (`rolldown-runtime`, `framework-*.js`) a l'arrel — un **mini-lloc estàtic
  exportat** amb una altra eina (font Geist, bundler Rolldown), residu d'una
  versió anterior. **És contingut llegat**: `/patrocinis/`, `/presentacio/`
  i `/dossier-patrocinis/` són ara redireccions `noindex` cap a
  `/patrocinadors/`, que és la pàgina real i mantinguda. No ampliar
  `patrocinis/`; qualsevol canvi de patrocinadors va a `/patrocinadors/` i a
  `data.json`.
- **`premidonaesport/`** — subcarpeta gran (teories, investigació,
  comunitat, patrocinis) que **reflecteix** el dossier del Premi Dona i
  Esport. **La web oficial i canònica és externa**:
  `voluntarisgrupbarna-pixel.github.io/cbgrupbarna/`. Aquesta còpia local
  **no s'edita com a font**: quan hi faltava una pàgina, la solució va ser
  enllaçar cap a la web oficial (108 enllaços a 23 pàgines), no reconstruir-
  la aquí. `/femeni/` és la síntesi pròpia i resumida d'aquest contingut,
  pensada per a la web, i **és la pàgina canònica de bàsquet femení** (no
  `/basquet-femeni/`, que hi redirigeix).
- **`partners-mapa/`** — mapa amb **Leaflet.js** vendored a
  `partners-mapa/vendor/leaflet/` (sense CDN).
- **`admin/`** — àrea protegida per token (`auth.js`, `config.js`,
  `token.html`), amb `noindex`.
- **`fotos/`** — galeria amb pipeline propi: `uploads/` (original),
  `thumb/`, `web/` (mides servides), gestionada en part pel workflow
  `build-gallery-images.yml`.

---

## 5. SEO, analítica i legal

- **JSON-LD per tipus de pàgina**: `SportsOrganization`, `FAQPage`,
  `BlogPosting`, `BreadcrumbList`, `WebPage`. Cada script generador (§2) en
  crea el seu.
- **`sitemap.xml`** — mantingut a mà en paral·lel als generadors; **no hi
  entren** pàgines `noindex` ni redireccions (`/presentacio/`,
  `/dossier-patrocinis/`, `/patrocinis/`, subpàgines `noindex` soltes com
  `/fotos-esdeveniments/3x3-westfield-2026/`).
- **`llms.txt`** — vegeu §0; actualitzar-lo junt amb el sitemap quan es
  publica o es retira una pàgina real.
- **`robots.txt`**, `hreflang` (ca/es/en) i `canonical` a cada pàgina.
- **Google Analytics (GA4, `G-R6XYR7G1WF`)** — carregat via `gtag.js` a
  `index.html`, però **darrere el consentiment de galetes**: no ha de sortir
  cap petició a Google abans d'acceptar. Comprovar-ho amb el panell de xarxa
  del navegador si es toca aquesta part.
- **Legal**: `/avis-legal/` i `/politica-de-privacitat/` (afegides
  14/08/2026), enllaçades al peu de totes les pàgines i des de cada casella
  de consentiment dels sis formularis que recullen dades (portada, `/fotos/`,
  `/fotos-3x3/`, `/galeria-3x3-glories/`,
  `/fotos-esdeveniments/3x3-westfield-2026/`, `/premidonaesport/`).

---

## 6. Contingut per àrees (resum; `llms.txt` és la llista completa i viva)

- **Formació**: `/escoleta/` (4-7 anys, Julio Torralba), `/campus/`
  (tecnificació d'estiu).
- **Competició**: `/partits/` (calendari, resultats, tendències i previsió
  estadística pròpia — no una IA de caixa negra), `/partits/equips/`,
  `/partits/calendaris/` (fitxes + .ics), `/grup-barna-dades-oficials/`.
- **Bàsquet femení**: `/femeni/` (síntesi canònica), `/premidonaesport/`
  (dossier ampli, mirall de la web oficial externa).
- **Esdeveniments**: `/3x3/` (Westfield Glòries), `fotos-esdeveniments/`.
- **Comunitat**: `/fotos/` (galeria), `/blog/` (12 articles, guies per a
  famílies), `/opina/` (ressenyes Google).
- **Institucional/premsa**: `/briefing/` (kit de premsa + PDF de 16 pàgines),
  `/premsa/`, `/documents/` (assegurança, protecció del menor, instal·
  lacions), `/club/` (història, organigrama).
- **Patrocinis**: `/patrocinadors/` (22 fitxes de partner, nivells or/plata/
  bronze pendents de confirmar per l'Ana), `/partners-mapa/`.
- **Legal**: `/avis-legal/`, `/politica-de-privacitat/`.

---

## 7. Abans de proposar una pàgina, secció o funcionalitat nova

1. **Busca-la a `llms.txt` i al `sitemap.xml`.** Pot ja existir amb un altre
   nom (vocabulari unificat a `web-cbgb` §5).
2. **Busca-la a `PENDENTS-WEB.md`.** Pot estar ja decidida en contra (amb el
   motiu), pendent d'un material concret de l'Ana, o ja duta a terme i només
   falta enllaçar-la.
3. **Comprova si la dada ve d'un robot** (§3) abans de proposar editar-la a
   mà — l'edició no duraria.
4. **Si toca una pàgina generada** (§2), proposa el canvi al generador, mai
   només a l'HTML de sortida.
5. **Si és contingut nou de veritat**, decideix on viu: HTML estàtic normal
   (la immensa majoria), entrada nova a `data.json` si és una dada
   reutilitzable, o s'ha de traduir a `/es/` i `/en/` també.

---

## 8. Trampes de sessió (trobades el 20/08/2026, en crear aquesta skill)

Aquest repositori s'ha vist en un estat estrany en obrir una sessió nova: val
la pena comprovar-ho abans de fer cap `git add`/`commit`/`push` massiu.

- **Índex de git fantasma.** `git status` pot mostrar milers de fitxers com a
  «esborrats» (`D`) que en realitat **existeixen intactes al disc** (apareixen
  després com a `??` no seguits). És un `.git/index.lock` orfe (0 bytes,
  cap procés real l'està usant) que ha deixat l'índex a mig actualitzar,
  probablement d'un checkout inicial de contenidor interromput. **Diagnòstic:**
  compara el `git status --short` d'un parell de fitxers concrets amb
  `ls -la` del mateix fitxer. **Solució segura:** `rm -f .git/index.lock` (si
  cap procés `git` real el té obert) i `git reset` (mixed, per defecte) —
  no toca el directori de treball, només reconcilia l'índex amb `HEAD`.
  **No** és feina en curs de ningú; és corrupció d'arrencada.
- **577 fitxers realment absents del disc**, diferents del cas anterior:
  pàgines senceres (`historia/`, `instal-lacions/`, `organigrama/`,
  `politica-de-privacitat/`, `proteccio-menor/`) i 347 fotos de `fotos/`
  desaparegudes del directori de treball tot i estar a `HEAD`. **Mai
  commitejar/pujar això**: esborraria de la web publicada pàgines legals
  RGPD i centenars de fotos. **Solució:** `git restore --source=HEAD
  --worktree -- .` (recupera el contingut del commit, no perd res). Verificat
  el 20/08/2026 amb el vistiplau de l'Ana.
- **`git push` normal pot fer time-out (HTTP 408 / connexió tallada als ~60-70s)**
  quan la branca porta al darrere commits locals sense pujar que l'`origin`
  no té (p. ex. una tanda de «foto: add … [skip ci]» de fotos de jugadors).
  `origin/main` pot anar desenes de commits per darrere del `HEAD` local.
  **No cal arrossegar aquests commits** només per publicar un canvi puntual
  (com una skill nova): es pot construir un commit nou **directament sobre
  `origin/main`**, sense passar pel directori de treball, amb plumbing de
  git —evita el pes de l'historial intermedi i el time-out:
  ```bash
  BLOB=$(git rev-parse <commit-local>:<ruta/al/fitxer>)
  export GIT_INDEX_FILE=/tmp/idx-tmp
  git read-tree origin/main
  git update-index --add --cacheinfo 100644,$BLOB,<ruta/al/fitxer>
  TREE=$(git write-tree)
  COMMIT=$(git commit-tree $TREE -p origin/main -m "missatge")
  unset GIT_INDEX_FILE
  git update-ref refs/heads/<branca> $COMMIT   # no fa checkout, no toca el directori de treball
  git push -u origin refs/heads/<branca>
  ```
  Després, si cal, torna el `ref` local a l'estat que coincideix amb el
  directori de treball (`git update-ref refs/heads/<branca> <commit-local>`)
  perquè `HEAD` i l'índex reals no quedin desincronitzats.

---

## 9. Pla de recuperació si es perd la web

El **codi i el text** de tota la web viuen a un repositori de git; si el
repositori existeix (a GitHub o en qualsevol clon), **es pot tornar a
publicar sencer amb un `git push`**, no cal reconstruir res a mà. El que
**no** viu al repositori —i per tant no es recupera només amb aquesta
skill— són les claus/comptes externs i els fitxers binaris que no s'hi han
pujat. Distingeix els tres nivells de pèrdua:

### Nivell 1 · El repositori existeix, però `cbgrupbarna.info` no respon

El lloc és a **GitHub Pages**. Per reviure'l:
1. A la configuració del repositori (`Settings → Pages`), torna a activar
   Pages sobre la branca de publicació.
2. Comprova que el fitxer **`CNAME`** a l'arrel encara diu
   `cbgrupbarna.info` (si s'ha esborrat per error, recrea'l amb aquest
   contingut exacte).
3. **El DNS del domini és extern al repositori** (registrador del domini,
   no GitHub): cal que els registres A/CNAME de `cbgrupbarna.info`
   segueixin apuntant a GitHub Pages. Si el domini ha caducat o s'ha
   desvinculat, això **no es pot arreglar des del codi** — cal entrar al
   panell del registrador del domini.

### Nivell 2 · El repositori de GitHub es perd, però hi ha un clon (com aquest)

```bash
git remote add origin https://github.com/voluntarisgrupbarna-pixel/cbgrupbarna-info
git push -u origin main    # o la branca que facis servir per publicar
```
Torna a fer Nivell 1 per revincular Pages i el domini. Els **robots de
GitHub Actions** (§3) necessiten que es tornin a donar d'alta els secrets
que fan servir (no viatgen amb el codi, GitHub els esborra si es perd el
repositori):

| Secret | El fa servir | Com es torna a donar d'alta |
|---|---|---|
| `JOTFORM_API_KEY` | `update-counters.yml` | `bash scripts/add-jotform-secret.sh` (clau nova a jotform.com/myaccount/api) |
| `SUPABASE_DB_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` | `deploy-galeria.yml` (app `galeria/`) | Panell del projecte a supabase.com → API settings |
| `VERCEL_TOKEN` | `deploy-galeria.yml` | vercel.com → Account settings → Tokens |

A més, fora dels *secrets* de GitHub:
- **`admin/config.js`** porta el `GOOGLE_CLIENT_ID` de l'OAuth del panell
  `/admin/` — si es perd, cal crear-ne un de nou a Google Cloud Console
  (les instruccions són al mateix fitxer, a dalt de tot).
- **Google Analytics** (`G-R6XYR7G1WF`) és una propietat del compte de
  Google del club, no del repositori — si es perd l'accés al compte, cal
  vincular-ne una de nova i canviar l'ID a `index.html`.
- **El projecte de Supabase** (base de dades i storage de `galeria/`) i el
  **projecte de Vercel** on es desplega són comptes externs propis —
  perdre'ls no es soluciona amb el codi, cal tenir-hi accés o recrear-los
  (i, amb Supabase, **recuperar les dades de la base amb un backup propi**:
  el repositori no en guarda cap còpia).

### Nivell 3 · Es perd tot: repositori, clons i comptes

Aquí la skill deixa de ser una xarxa de seguretat completa. El que **sí**
es podria reconstruir amb els tres documents del punt §0
(`llms.txt`, `PENDENTS-WEB.md`, `MIGRACIO-WEB-ANTIGA.md`) i aquesta skill
és **el text i l'estructura**: quines pàgines hi havia, què deien, com
s'organitzaven, quin sistema visual seguien (`web-cbgb`). El que **no** es
pot reconstruir a partir de text:
- **Les fotografies i vídeos** (`fotos/`, `partits/logos/`, `img/`, etc.).
  Si no hi ha una còpia fora del repositori (Google Drive, disc de l'Ana,
  Instagram), es perden de veritat. **Recomanació:** que les fotos
  originals que es pugen a `fotos/uploads/` es guardin també en algun lloc
  fora del repositori — el repositori no n'és una còpia de seguretat, és
  la web mateixa.
- **L'històric de dades de partits** (`partits/data.json`, `canvis.json`):
  es podria tornar a baixar de la FCBQ (basquetcatala.cat, club 24) amb el
  robot `update-partits.py`, però es perdria l'històric de resultats ja
  jugats si la federació no els conserva igual de bé.
- **Les dades de la base de Supabase** de `galeria/` (comentaris, metadades
  pujades pels usuaris).

**En resum: la millor assegurança és que el repositori de GitHub segueixi
existint** (encara que sigui privat o en un altre compte) i que les fotos
originals tinguin còpia en algun lloc més. Amb això, regenerar la web és
literalment tornar a fer `push` i revincular Pages, el domini i els
secrets — no cal escriure de nou cap pàgina.
