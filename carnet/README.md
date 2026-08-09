# CB Grup Barna — Carnet Digital

Carnet digital de soci/a per a les famílies del club: identificació i
descomptes en comerços col·laboradors. Descarregable a Google Wallet o com a
PDF/imatge (per a iPhone, on Apple Wallet natiu no és gratuït).

## Stack (100% gratuït)

- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend / BD**: Supabase (PostgreSQL + Storage + Auth) — pla gratuït
- **Wallet**: Google Wallet API (gratuït) — Apple Wallet requereix Apple
  Developer Program (99 $/any) i **no** està inclòs en aquesta primera versió
- **Hosting recomanat**: Vercel (pla Hobby, gratuït)

## Com funciona

1. Una família omple el formulari públic (`/`) amb les dades del jugador/a
   (incloent el **codi de jugador de la federació**) i les del tutor/a.
2. La sol·licitud queda en estat `pendent` — **cap carnet s'activa sense
   revisió manual** d'un admin del club a `/admin`.
3. L'admin (login amb enllaç màgic per email, mateix criteri d'accés que la
   resta de panells del club) revisa i aprova o rebutja.
4. En aprovar, es genera un enllaç únic i no endevinable
   (`/carnet/<access_token>`) que l'admin copia i envia a la família per
   email/WhatsApp (no hi ha enviament automàtic de correu en aquesta
   primera versió, per mantenir-ho a cost zero).
5. La família obre l'enllaç: pot afegir el carnet a **Google Wallet** o
   desar-lo com a **PDF/imatge** (botó "Imprimeix / Desa en PDF").
6. El carnet porta un **codi QR** que apunta a `/verificar/<qr_token>` — la
   pàgina que obre el comerç sponsor en escanejar-lo. Mostra només foto, nom,
   equip i validesa (mai dades del tutor/a) i queda registrada la
   verificació (útil per a l'informe de retorn als sponsors).

## Configuració

### 1. Supabase

1. Crea un projecte gratuït a [supabase.com](https://supabase.com) (pots fer
   servir el mateix projecte que `/galeria` o un de nou).
2. **SQL Editor** → executa tot `supabase/schema.sql`.
3. **Storage** → **New bucket** → nom `carnets-fotos`, marca **Public**
   (veure la nota de privadesa dins de `schema.sql` sobre per què).
4. **Authentication** → activa el proveïdor de login per **Magic Link**
   (ja ve activat per defecte a Supabase).

### 2. Primer admin

Després que algú faci login una vegada a `/login` amb el seu email, ves a
Supabase → **Table Editor** → `profiles` i canvia el seu `role` a `admin`.

### 3. Variables d'entorn

```bash
cp .env.local.example .env.local
```

Omple `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` i
`SUPABASE_SERVICE_ROLE_KEY` (Settings → API a Supabase).

`NEXT_PUBLIC_BASE_URL` ha de ser el domini final on es desplegui aquesta app
(p. ex. `https://carnet.cbgrupbarna.info`) — s'usa per construir els enllaços
del QR i del pase de Google Wallet.

### 4. Google Wallet (opcional, gratuït)

Sense configurar, l'app funciona igualment: la família només veu l'opció de
PDF. Per activar el botó "Afegir a Google Wallet":

1. Registra't a [Google Wallet Business Console](https://pay.google.com/business/console)
   (gratuït) i obtén el teu **Issuer ID**.
2. A Google Cloud Console, crea un **Service Account**, activa l'API
   "Google Wallet API" i dona-li accés des de Business Console amb el rol
   **Wallet Object Issuer**.
3. Descarrega la clau JSON del service account i omple
   `GOOGLE_WALLET_ISSUER_ID`, `GOOGLE_WALLET_CLIENT_EMAIL` i
   `GOOGLE_WALLET_PRIVATE_KEY` a `.env.local` / Vercel.

### 5. Instal·lar i executar

```bash
npm install
npm run dev
```

Obre [http://localhost:3000](http://localhost:3000)

### 6. Deploy a Vercel

```bash
npm i -g vercel
vercel
```

Afegeix totes les variables d'entorn al dashboard de Vercel i configura el
domini `carnet.cbgrupbarna.info` (subdomini de `cbgrupbarna.info`, gratuït).

## Fases futures (no incloses en aquesta versió)

- **Apple Wallet natiu** — requereix Apple Developer Program (99 $/any) i
  generar `.pkpass` signats amb el certificat Pass Type ID.
- **Email automàtic** en aprovar (Resend/Postmark tenen plans gratuïts amb
  límit mensual) en lloc de copiar l'enllaç a mà.
- **Panell per a sponsors** perquè cada comerç vegi les seves pròpies
  verificacions (taula `verificacions` ja les registra).
- **Actualització push** del pase quan canvia l'estat (Google Wallet ho
  permet via API; ara cal que la família re-obri l'enllaç per veure canvis).
