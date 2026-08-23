# Pujador de fotos a R2

Aquest Worker rep les fotos i vídeos que puja `/fotos/admin.html` i els
escriu directament al bucket R2 `cbgb-fotos`, sense passar pel repositori.
Substitueix el "una foto = un commit" per "una foto = un objecte a R2".

Mentre no el despleguis i no omplis `fotos/config.js`, la web segueix
funcionant exactament com fins ara (fotos al repositori, pujada via l'API
de GitHub). Res es trenca per tenir aquest codi al repositori sense usar-lo.

## Estat (22 d'agost 2026)

Ja fet des del dashboard de Cloudflare:

- ✅ Bucket `cbgb-fotos` creat, amb accés públic
- ✅ Worker `fotos-upload` desplegat a `fotos-upload.cbgrupbarna.workers.dev`
- ✅ Binding R2 `FOTOS` → bucket `cbgb-fotos`
- ✅ Variable `PUBLIC_BASE`

Pendent (els dos únics passos que falten):

1. **Enganxar el codi** de `worker.js` (aquest fitxer) a l'editor del Worker
   i fer **Deploy**.
2. **Crear el secret `UPLOAD_TOKEN`** a Settings del Worker → *Variables and
   Secrets* → tipus **Secret**, marcant la casella "Secreto"/"Secret" abans
   de desar.

Un cop fets aquests dos passos, ves a **Comprovar que funciona** més avall.

## Bindings i variables que ha de tenir el Worker

| Nom | Tipus | Valor |
|---|---|---|
| `FOTOS` | R2 bucket binding | bucket `cbgb-fotos` |
| `PUBLIC_BASE` | Variable normal | URL pública del bucket, p.ex. `https://pub-xxxx.r2.dev` |
| `UPLOAD_TOKEN` | Secret | contrasenya llarga i aleatòria (la que ja tens generada) |

Si en algun moment redesplegues el Worker des de zero i vols fer-ho amb
`wrangler` en comptes del dashboard:

```bash
cd workers/fotos-upload
npx wrangler login
npx wrangler secret put UPLOAD_TOKEN   # t'aturarà per demanar-te el valor
npx wrangler deploy
```

(`wrangler.toml` ja porta el binding `FOTOS` i la variable `PUBLIC_BASE`
configurats amb els mateixos noms que el Worker desplegat al dashboard.)

## Comprovar que el Worker funciona

Sense tocar res de `fotos/admin.html` encara, pots comprovar-ho directament
des del navegador o amb `curl`:

```bash
curl https://fotos-upload.cbgrupbarna.workers.dev/health
# {"ok":true,"worker":"fotos-upload","bucketBound":true,"tokenConfigured":true,"publicBase":"https://pub-xxxx.r2.dev"}
```

Si `bucketBound` o `tokenConfigured` surten en `false`, falta algun dels
passos de dalt. Si `publicBase` surt `null` o no coincideix amb la URL
pública real del bucket, corregeix la variable `PUBLIC_BASE`.

```bash
curl "https://fotos-upload.cbgrupbarna.workers.dev/list?secret=EL_TEU_UPLOAD_TOKEN"
# {"ok":true,"prefix":"uploads/","truncated":false,"objects":[]}
```

Una llista buida és el resultat correcte ara mateix: encara no s'hi ha
pujat res.

**Abans de donar-ho per bo**, comprova que `/uploads/...` rebutja el que ha
de rebutjar:

```bash
# Sense contrasenya: ha de donar 401
curl -X PUT "https://fotos-upload.cbgrupbarna.workers.dev/uploads/prova/x.jpg" \
  -H "Content-Type: image/jpeg" --data-binary "res"

# Contrasenya correcta pero fitxer que no és foto ni video: ha de donar 400
curl -X PUT "https://fotos-upload.cbgrupbarna.workers.dev/uploads/prova/x.exe" \
  -H "X-Upload-Secret: EL_TEU_UPLOAD_TOKEN" --data-binary "res"

# Contrasenya correcta i extensio valida: ha de donar 200 i {"ok":true,...}
curl -X PUT "https://fotos-upload.cbgrupbarna.workers.dev/uploads/prova/x.jpg" \
  -H "X-Upload-Secret: EL_TEU_UPLOAD_TOKEN" --data-binary "res"
# esborra-la despres amb el mateix mecanisme que faries servir per a
# qualsevol objecte de prova, o deixa-la — "prova/x.jpg" no surt enlloc
# perque cap event de events.js hi apunta.
```

El content-type que queda desat a R2 el decideix el Worker per l'extensió
de la clau, no pas el `Content-Type` que enviï qui puja — així ningú pot
declarar el que vulgui i un HEIC mal etiquetat pel navegador tampoc es
rebutja per error.

## Pas final · activar-ho a la web

Un cop `/health` respon bé, edita `fotos/config.js` i omple:

```js
r2_public_base: 'https://pub-xxxx.r2.dev',                        // = publicBase de /health
r2_worker_url: 'https://fotos-upload.cbgrupbarna.workers.dev',
```

I els tres secrets a GitHub (**Settings → Secrets and variables → Actions**),
per als workflows `sync-r2.yml` i `sync-r2-uploads.yml`:

- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`

(Aquests tres són d'un API Token d'R2 amb permís *Object Read & Write* sobre
`cbgb-fotos` — Cloudflare dashboard → R2 → *Manage API tokens*. És diferent
de `UPLOAD_TOKEN`: aquell l'usa el Worker per validar pujades des del
navegador; aquests tres els usa GitHub Actions per generar i pujar les
miniatures.)

Puja't `/fotos/admin.html`, entra amb el teu token de GitHub de sempre, i a
sota trobaràs un camp «Clau de pujada R2»: enganxa-hi el valor de
`UPLOAD_TOKEN`. Es guarda només al teu navegador, mai al repositori.

A partir d'aquí, cada foto que pugis va directa a R2 (0 commits), i cada 15
minuts `sync-r2-uploads.yml` li genera les versions web i miniatura i les
puja també a R2. `events.js` (la llista d'esdeveniments i noms de fitxer) es
segueix desant al repositori com fins ara: pesa poc i ja s'actualitza una
sola vegada per tanda, no per foto.

## Comprovar una pujada real

1. A `/fotos/admin.html`, puja una foto de prova a un event.
2. Hauria de completar-se sense passar per GitHub (mira la pestanya Network
   del navegador: hauries de veure un `PUT` cap a `fotos-upload.cbgrupbarna.workers.dev`,
   no cap a `api.github.com`).
3. `curl ".../list?secret=..."` hauria de mostrar-hi la clau nova.
4. Espera fins a 15 minuts (o llança `sync-r2-uploads.yml` a mà des de
   **Actions** → **Run workflow**) i comprova que la foto surt a
   `https://cbgrupbarna.info/fotos/`.

## Límits coneguts d'aquesta primera versió

- Esborrar una foto pujada per R2 des de l'admin panel la treu de la
  galeria (del `events.js`) però no l'esborra del bucket: queda orfe a R2.
  No és un problema de funcionament, només d'espai; es pot netejar més
  endavant amb un endpoint `DELETE` al Worker si cal.
- La detecció de duplicats per SHA que fa l'admin panel per a les fotos
  antigues (contra `fotos/uploads/` a GitHub) no aplica a les fotos que ja
  viuen a R2.
