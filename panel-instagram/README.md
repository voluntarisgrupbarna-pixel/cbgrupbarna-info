# Panell d'Instagram · CB Grup Barna

Panell tipus **Hootsuite** per analitzar, controlar i monitoritzar el compte
[@cbgrupbarna](https://instagram.com/cbgrupbarna): seguidors, abast, engagement,
millors publicacions, barreja de contingut, audiència i **qui ens etiqueta**.

- **Panell resum:** [`index.html`](./index.html) → publicat a `https://cbgrupbarna.info/panel-instagram/`
- **Explorador BI:** [`bi.html`](./bi.html) → `https://cbgrupbarna.info/panel-instagram/bi.html`
- **Dades:** [`data.json`](./data.json) — l'omple un GitHub Action cada dia
- **Fetcher:** [`../scripts/fetch-instagram.mjs`](../scripts/fetch-instagram.mjs)
- **Automatització:** [`../.github/workflows/instagram-panel.yml`](../.github/workflows/instagram-panel.yml)

## Arquitectura (per què és així)

La web és estàtica (GitHub Pages), així que **no hi ha servidor on amagar el token**.
La solució segura, sense servidor i sense cost:

```
GitHub Action (cada dia)  →  crida la Graph API amb el token (a Secrets)
        │                     └─ escriu panel-instagram/data.json  →  git commit
        ▼
Pàgina estàtica index.html  →  llegeix data.json  →  pinta el panell
```

El token **mai** és al codi ni a la pàgina: viu a **GitHub → Settings → Secrets**.
Fins que no el connectis, el panell funciona en **mode DEMO** amb dades d'exemple.

## Com connectar-ho a dades reals (una sola vegada)

### 1. Requisits del compte
- @cbgrupbarna ha de ser un compte **Business** o **Creator**.
- Ha d'estar **vinculat a una pàgina de Facebook** (Instagram → Configuració →
  Compte → Comptes vinculats).

### 2. Crear l'app de Meta i el token
1. Entra a [developers.facebook.com](https://developers.facebook.com/) → **My Apps** → **Create App** (tipus *Business*).
2. Afegeix el producte **Instagram Graph API**.
3. A **Graph API Explorer** (o via *System User* a Business Settings) genera un token amb aquests permisos:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `instagram_manage_comments`  *(necessari per a "qui ens etiqueta")*
   - `pages_read_engagement`
   - `pages_show_list`
   - `business_management`  *(necessari per al benchmark de rivals)*
4. Converteix-lo a **token de llarga durada** (60 dies) o, millor, un **System User token** (no caduca):
   ```
   https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=TOKEN_CURT
   ```

### 3. Trobar l'IG_USER_ID
```
https://graph.facebook.com/v21.0/me/accounts?access_token=EL_TEU_TOKEN
   → agafa l'id de la pàgina de Facebook
https://graph.facebook.com/v21.0/PAGE_ID?fields=instagram_business_account&access_token=EL_TEU_TOKEN
   → et retorna instagram_business_account.id  ← aquest és IG_USER_ID
```

### 4. Guardar-ho a GitHub Secrets
Al repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Nom | Valor |
|-----|-------|
| `IG_ACCESS_TOKEN` | el token de llarga durada / system user |
| `IG_USER_ID` | l'id numèric del compte de Instagram |

Opcional, com a *Variable* (no secret): `IG_API_VERSION` (per defecte `v21.0`).

### 5. Executar
- **Actions → "Panell Instagram (fetch dades)" → Run workflow** per provar-ho a l'instant.
- A partir d'aquí s'executa **sol cada dia** i el panell passa a mode **EN DIRECTE**.

## Què mostra el panell

| Bloc | Contingut |
|------|-----------|
| **Resum** | Seguidors (+Δ del dia), abast 30d, visites al perfil, engagement mitjà, mencions, nº de publicacions |
| **Creixement** | Corba de seguidors dels últims 30 dies (sèrie que acumulem nosaltres, dia a dia) |
| **Barreja de contingut** | Reels vs vídeo vs carrusel vs imatge |
| **Millors publicacions** | Top posts per engagement, amb abast, likes, comentaris, guardats i compartits |
| **Comparativa any rere any** | Un mes (p. ex. Juliol) comparat entre anys — nous seguidors, seguidors, abast o engagement, amb variació interanual |
| **Qui ens etiqueta** | Comptes que ens etiqueten (monitorització estil Hootsuite) |
| **Audiència** | Top ciutats dels seguidors |

## Tot el que treu de l'API (`fetch-instagram.mjs`)

L'extractor treu **tot el que la Graph API ofereix** per a un compte Business, amb
degradació robusta (cada bloc va dins d'un try/catch; el que no arriba es registra a
`meta.coverage` i la resta segueix). Blocs:

| Bloc | Contingut |
|------|-----------|
| **Perfil** | usuari, nom, bio, seguidors, seguits, nº publicacions, web, foto, `ig_id` |
| **Límit de publicació** | quota d'API restant (`content_publishing_limit`) |
| **Insights de compte (30 d)** | abast, visites al perfil, clics web/email/telèfon/direccions, comptes que interactuen, interaccions totals, likes, comentaris, guardats, compartits, respostes, taps a enllaços, follows/unfollows, vistes |
| **Sèries diàries** | abast per dia i nous seguidors per dia |
| **Audiència** | per **ciutat, país, edat i gènere** |
| **Publicacions (totes)** | paginades, amb insights per tipus (reels: reproduccions i temps de visionat; feed: guardats, visites al perfil, follows) |
| **Stories** | actives, amb abast, respostes, compartits, navegació |
| **Etiquetes** | comptes que ens etiqueten (`/tags`) |
| **Hashtag `#somclot`** | publicacions recents del barri (`ig_hashtag_search`) |
| **Benchmark** | seguidors i publicacions dels rivals via `business_discovery` (vegeu `benchmark.json`) |
| **Acumulació** | sèrie diària i mensual pròpia, per a tendències i any-rere-any |

La cobertura de cada execució queda a `data.json → meta.coverage`, així saps què ha
arribat i què no (per permisos o versió de l'API).

### Benchmark de rivals (`benchmark.json`)

Posa a [`benchmark.json`](./benchmark.json) els noms d'usuari **públics** dels rivals
(SESE, UE Horta, CB Roser…). El fetcher en treu seguidors i publicacions per comparar-los
amb el Barna. Necessita el permís `business_management` al token.

## Explorador BI (`bi.html`)

Eina d'anàlisi lliure, estil Business Intelligence, per **analitzar qualsevol mètrica
i comparar dies i mesos d'anys anteriors**:

- **Mètrica**: nous seguidors · seguidors totals · abast · visites al perfil · publicacions · engagement.
- **Granularitat**: dia · setmana · mes.
- **Dues vistes**:
  - *Tendència* — evolució en un rang (30 d / 90 d / 12 m / tot).
  - *Comparativa anual* — superposa una línia per any (X = mes o dia de l'any). L'any en curs
    es ressalta en vermell; els anteriors, en gris. Comparació **YTD justa** (mateix període,
    no un any parcial contra un de complet).
- **Rendiment per dia de la setmana** — quin dia rendeix més.
- **Taula de dades** amb variació i **exportació a CSV**.

Tot es calcula al navegador des de `data.json` (sèrie diària + mensual). Els mesos passats
d'anys anteriors surten de `historic.json`; els dies/setmanes d'anys anteriors s'acumulen
sols a mesura que el panell funciona.

## Comparativa any rere any (`historic.json`)

L'API d'Instagram **no dona històric de fa anys**, així que la comparativa mensual
s'alimenta de dues fonts que el panell combina soles:

1. **Mesos que el panell acumula sol** — cada execució desa el mes vigent a `data.json` → `monthly`.
   Amb el temps es va omplint any rere any.
2. **[`historic.json`](./historic.json)** — mesos passats que **omples tu una vegada** amb el
   que ja tinguis a **Meta Business Suite → Estadístiques** (es pot exportar per mes).

Per afegir un any anterior, edita `historic.json` i afegeix entrades a `months`:

```json
"months": {
  "2025-07": { "followers": 2680, "newFollowers": 49, "reach": 35200, "profileViews": 4600, "posts": 10, "avgEngagement": 5.9 }
}
```

Deixa a `null` el que no sàpigues; el panell ho ignora. Els mesos mesurats en directe
tenen prioritat sobre `historic.json` (no els sobreescriu).

## Notes i límits

- La **corba de creixement** es construeix acumulant un snapshot diari: al principi
  es veurà curta i s'anirà omplint (la Graph API no dona històric de seguidors llarg).
- **"Qui ens etiqueta"** usa l'endpoint `/tags` (posts on ens etiqueten). Les mencions
  dins de *comentaris* requereixen el webhook de mencions de Meta; es pot afegir més endavant.
- Algunes mètriques a nivell de compte canvien segons la versió de l'API; el fetcher
  captura cada error i el panell segueix funcionant amb la resta de dades.
- El token de llarga durada **caduca als ~60 dies** si no és de System User: renova'l o
  automatitza la renovació.

---
Fet per al CB Grup Barna · #somclot
