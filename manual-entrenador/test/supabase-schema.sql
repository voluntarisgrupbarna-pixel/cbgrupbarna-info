-- ═══════════════════════════════════════════════════════════════
-- Test del Entrenador Nivel 1 — CB Grup Barna
-- Pega este script entero en Supabase → SQL Editor → Run, UNA vez,
-- en el proyecto que uses para guardar los resultados del test.
-- ═══════════════════════════════════════════════════════════════

-- Tabla con una fila por cada persona que completa el test
create table if not exists public.test_entrenador_respostes (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  nombre text not null,
  email text not null,
  movil text not null,
  puntuacion int not null,
  total_preguntas int not null,
  detalle jsonb not null,            -- [{"cap":2,"ok":true}, {"cap":2,"ok":false}, ...]
  participa_sorteo boolean not null default false,
  consentimiento boolean not null default false
);

-- Activa seguridad a nivel de fila: por defecto, nadie puede leer ni escribir
alter table public.test_entrenador_respostes enable row level security;

-- Permite que cualquier visitante de la web pueda INSERTAR su resultado
-- (usando la clave pública "anon"), pero NO leer, modificar ni borrar filas.
-- Esto protege los emails/móviles de todo el mundo: solo tú, entrando en
-- Supabase con tu cuenta de propietaria, puedes verlos (Table Editor).
create policy "Insercio publica del test"
  on public.test_entrenador_respostes
  for insert
  to anon
  with check (true);

-- ───────────────────────────────────────────────────────────────
-- VISTA: en qué capítulo falla más la gente (para saber qué reforzar)
-- Consulta con: select * from test_entrenador_fallos_por_capitulo;
-- ───────────────────────────────────────────────────────────────
create or replace view public.test_entrenador_fallos_por_capitulo as
select
  (item->>'cap')::int as capitulo,
  count(*) filter (where (item->>'ok')::boolean = false) as fallos,
  count(*) as total_respuestas,
  round(100.0 * count(*) filter (where (item->>'ok')::boolean = false) / count(*), 1) as pct_fallo
from public.test_entrenador_respostes t,
     jsonb_array_elements(t.detalle) as item
group by capitulo
order by pct_fallo desc;

-- ───────────────────────────────────────────────────────────────
-- PARA EL SORTEO: lista de participantes (15 aciertos o más)
-- Consulta con: select * from test_entrenador_sorteo;
-- Para elegir un ganador al azar entre ellos:
--   select * from test_entrenador_sorteo order by random() limit 1;
-- ───────────────────────────────────────────────────────────────
create or replace view public.test_entrenador_sorteo as
select id, created_at, nombre, email, movil, puntuacion
from public.test_entrenador_respostes
where participa_sorteo = true
order by created_at desc;
