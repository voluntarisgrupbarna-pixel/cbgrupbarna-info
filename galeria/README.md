# CB Grup Barna — Galeria de Fotos

Repositori fotogràfic oficial del CB Grup Barna. Construït amb Next.js 14 i Supabase.

## Stack

- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Backend / Auth**: Supabase (PostgreSQL + Storage + Auth)
- **Hosting recomanat**: Vercel (gratuït per a clubs)

## Funcionalitats

- Galeria organitzada per **temporades i esdeveniments**
- **Login de membres** amb email/contrasenya o magic link
- **Subida directa** de fotos per membres
- **Descàrrega de fotos** en alta resolució (configurable per event)
- **Likes i comentaris** per foto
- **Lightbox** amb navegació, títol i descàrrega
- **Cerca i filtres** per event i temporada
- **Panel d'administrador** per gestionar events, temporades i rols
- **Rols**: viewer / contributor / editor / admin

## Configuració

### 1. Crea el projecte a Supabase

1. Ves a [supabase.com](https://supabase.com) i crea un compte gratuït
2. Crea un nou projecte
3. Ves a **SQL Editor** i executa el fitxer `supabase/schema.sql`
4. Ves a **Storage** → **New bucket** → Nom: `photos`, accés **Public**

### 2. Variables d'entorn

```bash
cp .env.local.example .env.local
```

Omple amb les teves claus de Supabase (les trobes a Settings → API):

```
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### 3. Instalar i executar

```bash
npm install
npm run dev
```

Obra [http://localhost:3000](http://localhost:3000)

### 4. Primer admin

Després de crear el teu compte a la galeria, ves a Supabase → Table Editor → `profiles` i canvia el teu `role` a `admin`.

## Deploy a Vercel

```bash
npm i -g vercel
vercel
```

Afegeix les variables d'entorn al dashboard de Vercel.

## Estructura

```
src/
├── app/
│   ├── page.tsx              # Pàgina principal (últims events)
│   ├── events/page.tsx       # Tots els events + cerca
│   ├── events/[id]/page.tsx  # Fotos d'un event
│   ├── upload/page.tsx       # Pujar fotos
│   ├── admin/page.tsx        # Panel d'administrador
│   └── login/page.tsx        # Login / registre
├── components/
│   ├── Navbar.tsx
│   ├── EventCard.tsx
│   ├── PhotoGrid.tsx         # Masonry grid + lightbox
│   ├── UploadZone.tsx        # Drag & drop upload
│   └── SearchBar.tsx
└── lib/
    ├── supabase/             # Clients SSR
    └── types.ts              # TypeScript types
```
