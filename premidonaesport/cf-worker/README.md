# Cercador amb IA · Cloudflare Worker (gratuït)

Aquest Worker fa la cerca semàntica real (entén sinònims, idiomes barrejats,
descripcions en llenguatge natural) fent servir **Workers AI**, la IA pròpia
de Cloudflare. És gratuïta fins a 10.000 "neurons"/dia — de sobra per a
aquesta web — i no necessita cap clau d'API d'Anthropic ni OpenAI.

## Opció A · Sense terminal (des del panell web, la més senzilla)

1. Crea un compte gratuït a **https://dash.cloudflare.com/sign-up** (no cal
   targeta de crèdit pel pla gratuït).
2. Al menú lateral, ves a **Workers & Pages** → **Create** → **Create Worker**.
3. Posa-li un nom, per exemple `cbgb-premi-search-ai`, i crea'l.
4. Un cop creat, clica **Edit code** (l'editor Quick Edit s'obre al navegador).
5. Esborra tot el contingut per defecte i enganxa-hi el contingut sencer del
   fitxer [`search-ai.js`](./search-ai.js) d'aquesta carpeta.
6. Abans de desplegar, activa la IA: a la pestanya **Settings** del Worker
   → **Bindings** → **Add binding** → tria **Workers AI**, posa-li el nom
   `AI` (exactament així, en majúscules) i desa.
7. Clica **Deploy** (o **Save and deploy**).
8. Cloudflare et donarà una URL del tipus
   `https://cbgb-premi-search-ai.<el-teu-usuari>.workers.dev` — aquesta és
   l'endpoint que necessitem.

## Opció B · Amb terminal (wrangler CLI)

```bash
cd premidonaesport/cf-worker
npm install -g wrangler   # si no el tens ja
wrangler login            # obre el navegador per autoritzar
wrangler deploy
```

Al final del `deploy` et donarà la mateixa URL `*.workers.dev`.

## Últim pas: connectar-ho al lloc web

Un cop tinguis la URL (és pública, no és cap secret — la pots enganxar aquí
al xat sense problema), digue-me-la i actualitzo
`premidonaesport/assets/js/search.js` perquè hi apunti. Mentre no ho facis,
el cercador segueix funcionant igual que ara (cerca local, instantània),
només que sense la capa d'IA semàntica per sobre.

## Cost real

Amb el tràfic esperat d'una web de candidatura (desenes/centenars de
visites, no milers al dia), es queda còmodament dins del tier gratuit de
Workers AI. Si mai el superessis, Cloudflare simplement respon amb un
error que el nostre codi ja gestiona fent *fallback* silenciós a la cerca
local — la web mai es trenca ni et pot arribar una factura sorpresa.
