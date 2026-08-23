# Pujador de fotos a R2

Aquest Worker rep les fotos i vídeos que puja `/fotos/admin.html` i els
escriu directament al bucket R2 `cbgb-fotos`, sense passar pel repositori.
Substitueix el "una foto = un commit" per "una foto = un objecte a R2".

Mentre no el despleguis i no omplis `fotos/config.js`, la web segueix
funcionant exactament com fins ara (fotos al repositori, pujada via l'API
de GitHub). Res es trenca per tenir aquest codi al repositori sense usar-lo.

## Pas 1 · Crear el bucket R2 (si encara no existeix)

1. Entra al [dashboard de Cloudflare](https://dash.cloudflare.com) → **R2**.
2. **Create bucket** → nom exacte `cbgb-fotos` (si li poses un altre nom,
   canvia'l a `wrangler.toml` d'aquesta carpeta i a `sync-r2.yml`).
3. Un cop creat, entra al bucket → **Settings** → **Public access** →
   activa **Allow public access via the r2.dev subdomain**. Copia la URL
   pública que et dona (`https://pub-XXXXXXXX.r2.dev`) — la necessitaràs
   al pas 4.

## Pas 2 · Desplegar el Worker

**Opció ràpida (sense instal·lar res), des del dashboard:**

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Create Worker**.
2. Nom: `cbgb-fotos-upload`. Crea'l amb el codi per defecte.
3. **Edit code** → esborra tot i enganxa el contingut de `worker.js` d'aquesta
   carpeta → **Deploy**.
4. Torna a la pàgina del Worker → **Settings** → **Bindings** → **Add binding**
   → tipus **R2 Bucket** → variable `BUCKET` → bucket `cbgb-fotos` → Desa.
5. **Settings** → **Variables and Secrets** → **Add** → tipus **Secret** →
   nom `UPLOAD_SECRET` → valor: una contrasenya llarga i aleatòria que et
   inventis ara (per exemple, generada amb `openssl rand -hex 24`). **Apunta-te-la**:
   la necessitaràs al pas 4 i no la tornaràs a veure.
6. Comprova la URL del Worker a dalt de tot de la pàgina (alguna cosa com
   `https://cbgb-fotos-upload.<el-teu-subdomini>.workers.dev`).

**Opció amb wrangler (si prefereixes terminal):**

```bash
cd workers/fotos-upload
npx wrangler login
npx wrangler secret put UPLOAD_SECRET   # t'aturarà per demanar-te el valor
npx wrangler deploy
```

## Pas 3 · Crear l'usuari de GitHub Actions per pujar les derivades

El workflow `.github/workflows/sync-r2-uploads.yml` necessita poder escriure
a R2 (per pujar les versions `web/` i `thumb/` que genera). Fa servir els
mateixos tres secrets que ja demanava `sync-r2.yml`:

1. Cloudflare dashboard → **R2** → **Manage API tokens** → **Create API token**.
2. Permisos: **Object Read & Write**, limitat al bucket `cbgb-fotos`.
3. Copia els tres valors que et dona: **Account ID**, **Access Key ID**,
   **Secret Access Key**.
4. Al repositori de GitHub: **Settings** → **Secrets and variables** →
   **Actions** → **New repository secret**, i crea'n tres:
   - `R2_ACCOUNT_ID`
   - `R2_ACCESS_KEY_ID`
   - `R2_SECRET_ACCESS_KEY`

(Si ja els vas crear per a `sync-r2.yml`, aquest pas ja està fet — els dos
workflows fan servir els mateixos tres secrets.)

## Pas 4 · Activar-ho a la web

Edita `fotos/config.js` i omple aquests dos camps (la resta de l'arxiu es
queda igual):

```js
r2_public_base: 'https://pub-XXXXXXXX.r2.dev',       // del pas 1
r2_worker_url: 'https://cbgb-fotos-upload.xxx.workers.dev',  // del pas 2
```

Puja't `/fotos/admin.html`, entra amb el teu token de GitHub de sempre, i a
sota del token trobaràs un nou camp «Clau de pujada R2»: enganxa-hi el
`UPLOAD_SECRET` del pas 2, punt 5. Es guarda només al teu navegador, mai al
repositori.

A partir d'aquí, cada foto que pugis va directa a R2 (0 commits), i cada 15
minuts un workflow li genera les versions web i miniatura i les puja també
a R2. `events.js` (la llista d'esdeveniments i noms de fitxer) es segueix
desant al repositori com fins ara: pesa poc i ja s'actualitza una sola
vegada per tanda, no per foto.

## Comprovar que funciona

1. A `/fotos/admin.html`, puja una foto de prova a un event.
2. Hauria de completar-se sense passar per GitHub (mira la pestanya Network
   del navegador: hauries de veure un `PUT` cap al domini `workers.dev`, no
   cap a `api.github.com`).
3. Espera fins a 15 minuts (o llança `sync-r2-uploads.yml` a mà des de
   **Actions** → **Run workflow**) i comprova que la foto surt a
   `https://cbgrupbarna.info/fotos/`.
