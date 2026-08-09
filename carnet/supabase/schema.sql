-- CB Grup Barna · Carnet Digital — Database Schema
-- Executa aquest fitxer sencer a Supabase → SQL Editor (projecte gratuït).
--
-- Disseny de seguretat:
--   - La taula `carnets` NO té cap policy oberta a `anon`. Ningú pot llegir-la
--     ni escriure-hi directament des del navegador.
--   - L'alta pública (formulari) i les pàgines públiques (/carnet, /verificar)
--     passen sempre per rutes de servidor de Next.js que fan servir la
--     SUPABASE_SERVICE_ROLE_KEY (mai exposada al navegador).
--   - Només un usuari autenticat amb `profiles.role = 'admin'` pot llegir o
--     modificar la taula `carnets` directament (panell d'administració).

create extension if not exists "pgcrypto";

-- ── PROFILES (autenticació admin) ──────────────────────────────────────────
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  role text not null default 'viewer' check (role in ('viewer', 'admin')),
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;

create policy "Profiles viewable by authenticated users"
  on public.profiles for select to authenticated using (true);
create policy "Users can update own profile"
  on public.profiles for update to authenticated using (auth.uid() = id);
create policy "Users can insert own profile"
  on public.profiles for insert to authenticated with check (auth.uid() = id);

create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, full_name, role)
  values (new.id, new.raw_user_meta_data->>'full_name', 'viewer');
  return new;
end;
$$ language plpgsql security definer set search_path = public;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ── CARNETS ─────────────────────────────────────────────────────────────
create table public.carnets (
  id uuid primary key default gen_random_uuid(),

  -- dades del jugador/a
  nom text not null,
  cognoms text not null,
  equip text,
  codi_federacio text not null,
  temporada text not null default '2025-2026',
  foto_path text, -- ruta dins del bucket privat 'carnets-fotos'

  -- dades del tutor/a (mai es mostren a la pàgina de verificació pública)
  tutor_nom text not null,
  tutor_email text not null,
  tutor_telefon text,
  consentiment_rgpd boolean not null default false,
  consentiment_data timestamptz,

  -- cicle de vida
  estat text not null default 'pendent'
    check (estat in ('pendent', 'actiu', 'rebutjat', 'revocat', 'caducat')),
  notes_admin text,
  data_caducitat date,
  aprovat_per uuid references public.profiles(id),
  aprovat_at timestamptz,

  -- tokens públics no-enumerables (32 hex chars, atzar criptogràfic)
  qr_token text not null unique default encode(gen_random_bytes(16), 'hex'),
  access_token text not null unique default encode(gen_random_bytes(16), 'hex'),

  created_at timestamptz not null default now()
);

create index idx_carnets_estat on public.carnets(estat);
create index idx_carnets_codi_federacio on public.carnets(codi_federacio);

alter table public.carnets enable row level security;

-- Cap policy per anon: l'alta i les pàgines públiques van sempre per servidor
-- (service role, que salta l'RLS). Només els admins hi entren des del navegador.
create policy "Admins can view all carnets"
  on public.carnets for select to authenticated
  using (exists (select 1 from public.profiles where id = auth.uid() and role = 'admin'));

create policy "Admins can update carnets"
  on public.carnets for update to authenticated
  using (exists (select 1 from public.profiles where id = auth.uid() and role = 'admin'));

create policy "Admins can delete carnets"
  on public.carnets for delete to authenticated
  using (exists (select 1 from public.profiles where id = auth.uid() and role = 'admin'));

-- ── VERIFICACIONS (traçabilitat de canvis a comerços sponsor) ─────────────
create table public.verificacions (
  id bigserial primary key,
  carnet_id uuid not null references public.carnets(id) on delete cascade,
  verificat_at timestamptz not null default now(),
  comerç text
);

create index idx_verificacions_carnet_id on public.verificacions(carnet_id);

alter table public.verificacions enable row level security;

create policy "Admins can view verificacions"
  on public.verificacions for select to authenticated
  using (exists (select 1 from public.profiles where id = auth.uid() and role = 'admin'));

-- ── STORAGE ─────────────────────────────────────────────────────────────
-- Executa manualment des del Dashboard → Storage → New bucket:
--   nom: carnets-fotos · Public: SÍ
--
-- Decisió conscient: el bucket és públic (com les fotos de jugadors/es que
-- ja publiqueu a /jugadors) perquè Google Wallet ha de poder carregar la
-- foto des d'una URL pública i estable — una signed URL amb caducitat no
-- serveix per a un pase que la família es pot descarregar avui i mirar
-- d'aquí a mesos. El nom de fitxer és un UUID aleatori (no enumerable), no
-- el nom del jugador/a, així que ningú pot "adivinar" l'URL d'una foto.
-- Si es vol privadesa estricta, es pot tornar el bucket privat i treure la
-- `heroImage` del pase de Google Wallet (queda igual de funcional, sense foto).
-- No calen policies d'INSERT/UPDATE: totes les pujades passen pel servidor
-- (service role), mai directament des del navegador.
