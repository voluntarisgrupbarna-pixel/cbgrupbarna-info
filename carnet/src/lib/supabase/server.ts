import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

/**
 * Client de servidor amb la clau ANON, subjecte a RLS i a la sessió
 * (cookies) de l'usuari autenticat. Fer servir per a l'àrea /admin.
 */
export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet: { name: string; value: string; options?: Record<string, unknown> }[]) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options as never)
            )
          } catch {
            // Called from Server Component, can be ignored
          }
        },
      },
    }
  )
}
