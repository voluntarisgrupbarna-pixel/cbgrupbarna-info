import { createClient as createSupabaseClient } from '@supabase/supabase-js'

/**
 * Client amb la SERVICE ROLE KEY — salta l'RLS completament.
 *
 * ⚠ NOMÉS es pot importar des de codi que s'executa al servidor (Route
 * Handlers, Server Components, Server Actions). Mai des d'un fitxer marcat
 * amb 'use client'. La clau viu només a la variable d'entorn del servidor
 * (Vercel), mai al bundle del navegador.
 *
 * És el que permet que /api/carnets (alta pública) i les pàgines
 * /carnet/[token] i /verificar/[token] (públiques, sense sessió) puguin
 * llegir o escriure carnets sense necessitar policies obertes a `anon`.
 */
export function createServiceClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY

  if (!url || !key) {
    throw new Error(
      'Falten NEXT_PUBLIC_SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY. Revisa .env.local.'
    )
  }

  return createSupabaseClient(url, key, {
    auth: { autoRefreshToken: false, persistSession: false },
  })
}
