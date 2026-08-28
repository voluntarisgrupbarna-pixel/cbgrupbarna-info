# Límit d'intents per a la porta d'/admin/

`scripts/admin-gate.js` protegia `/admin/` amb un SHA-256 de la contrasenya
del club guardat **en clar en un fitxer públic del repositori**: qualsevol
que el llegís podia intentar-hi milions de contrasenyes per segon amb una
GPU, sense que ningú se n'assabentés. Aquest Worker tapa aquest forat: la
contrasenya (el seu hash, mai en clar) es comprova aquí, i després de 8
intents fallits des de la mateixa IP en 15 minuts, es bloquegen els següents.

**És gratuït.** Cloudflare Workers té un pla gratuït de 100.000 peticions al
dia i Workers KV 100.000 lectures + 1.000 escriptures al dia — per als pocs
intents d'accés a `/admin/` d'un club de barri, no s'hi arriba de bon tros.
El club ja té compte de Cloudflare (per R2 i pel Worker
`workers/fotos-upload/`), així que no cal donar-se d'alta enlloc de nou.

Mentre no el despleguis i no omplis `GATE_ENDPOINT` a
`scripts/admin-gate.js`, la porta segueix funcionant exactament com fins
ara (comparació local, sense límit d'intents). Res es trenca per tenir
aquest codi al repositori sense usar-lo.

## Bindings i variables que ha de tenir el Worker

| Nom | Tipus | Valor |
|---|---|---|
| `INTENTS` | KV namespace binding | un namespace nou, per exemple `admin-gate-intents` |
| `PASS_HASH` | Secret | el SHA-256 de la contrasenya del club (el mateix valor que ara hi ha a `PASS_HASH` dins `scripts/admin-gate.js`) |

## Desplegar-ho

Amb `wrangler` (recomanat, i coherent amb `workers/fotos-upload/`):

```bash
cd workers/admin-gate
npx wrangler login
npx wrangler kv namespace create INTENTS
# et dona un "id": enganxa'l a wrangler.toml, a [[kv_namespaces]] > id
npx wrangler secret put PASS_HASH
# t'aturarà per demanar-te el valor: enganxa-hi el mateix hash de scripts/admin-gate.js
npx wrangler deploy
```

O des del dashboard de Cloudflare, igual que es va fer amb
`fotos-upload` (Workers → Create → enganxar `worker.js` → Deploy, després
Settings del Worker → *Bindings* per l'KV i *Variables and Secrets* pel
`PASS_HASH` marcat com a "Secret").

## Comprovar que funciona

```bash
curl https://admin-gate.cbgrupbarna.workers.dev/health
# {"ok":true,"worker":"admin-gate","passConfigured":true,"kvBound":true}
```

```bash
# Hash equivocat (el de "prova"): ha de donar {"ok":false}
curl -X POST https://admin-gate.cbgrupbarna.workers.dev/ \
  -H "Content-Type: application/json" \
  -d '{"hash":"'"$(printf prova | shasum -a 256 | cut -d' ' -f1)"'"}'

# Repeteix la comanda de dalt 8 cops seguits: la 9a ha de donar {"ok":false,"blocked":true,"retryAfter":...}
# amb estat HTTP 429.
```

## Pas final · activar-ho a la web

Un cop `/health` respon bé, edita `scripts/admin-gate.js` i omple
`GATE_ENDPOINT` amb la URL del Worker (sense `/health` al final):

```js
var GATE_ENDPOINT = 'https://admin-gate.cbgrupbarna.workers.dev';
```

Puja el canvi. A partir d'aquí, cada intent d'entrar a `/admin/` es
comprova contra aquest Worker en lloc de només localment.

## El que això millora — i el que NO arregla del tot

Millora de veritat el cas real: algú que prova contrasenyes des del
formulari de `/admin/`, o amb un script que ataca aquest mateix Worker per
l'API, queda bloquejat al cap de 8 intents. Això és el 99% dels atacs
reals contra una porta com aquesta.

**El que segueix igual:** `scripts/admin-gate.js` continua portant
`PASS_HASH` en clar (és el fallback per si el Worker cau, perquè la
porta no es quedi mai bloquejada per un problema de Cloudflare). Això vol
dir que qui es baixi el codi del repositori i vulgui atacar-lo **offline**,
sense passar mai pel Worker, encara pot intentar-ho contra aquest hash
local sense límit — el Worker no ho impedeix perquè no hi intervé.

Si en algun moment vols tancar aquest últim forat del tot (a canvi de
perdre l'accés de reserva si el Worker cau algun dia): treu la comparació
local a `verificaHash()` i deixa `/admin/` depenent del Worker sense
alternativa. No s'ha fet per defecte perquè, per a un club de barri, que la
porta quedi bloquejada per una caiguda de Cloudflare és pitjor que aquest
risc residual — però la decisió és teva.
