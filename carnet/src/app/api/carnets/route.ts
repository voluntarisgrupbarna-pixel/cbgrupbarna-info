import { NextResponse } from 'next/server'
import { randomUUID } from 'crypto'
import { createServiceClient } from '@/lib/supabase/service'

export const runtime = 'nodejs'

const FOTOS_BUCKET = 'carnets-fotos'
const MAX_FOTO_BYTES = 5 * 1024 * 1024 // 5MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function bad(message: string, status = 400) {
  return NextResponse.json({ error: message }, { status })
}

/**
 * Alta pública del carnet (formulari de família).
 * S'insereix sempre amb estat 'pendent' — cap carnet s'activa sense
 * revisió manual d'un admin al panell /admin.
 */
export async function POST(req: Request) {
  let form: FormData
  try {
    form = await req.formData()
  } catch {
    return bad('Formulari invàlid.')
  }

  const nom = String(form.get('nom') ?? '').trim()
  const cognoms = String(form.get('cognoms') ?? '').trim()
  const equip = String(form.get('equip') ?? '').trim() || null
  const codiFederacio = String(form.get('codi_federacio') ?? '').trim()
  const tutorNom = String(form.get('tutor_nom') ?? '').trim()
  const tutorEmail = String(form.get('tutor_email') ?? '').trim().toLowerCase()
  const tutorTelefon = String(form.get('tutor_telefon') ?? '').trim() || null
  const consentiment = form.get('consentiment_rgpd') === 'on' || form.get('consentiment_rgpd') === 'true'
  const foto = form.get('foto') as File | null

  if (!nom || !cognoms) return bad('Falten el nom i els cognoms del jugador/a.')
  if (!codiFederacio) return bad('Falta el codi de jugador de la federació.')
  if (!tutorNom || !tutorEmail) return bad('Falten les dades del tutor/a.')
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(tutorEmail)) return bad('Email del tutor/a no vàlid.')
  if (!consentiment) return bad('Cal acceptar el consentiment de protecció de dades.')

  const supabase = createServiceClient()
  let fotoPath: string | null = null

  if (foto && foto.size > 0) {
    if (foto.size > MAX_FOTO_BYTES) return bad('La foto no pot superar 5MB.')
    if (!ALLOWED_TYPES.includes(foto.type)) return bad('La foto ha de ser JPG, PNG o WebP.')

    const ext = foto.type === 'image/png' ? 'png' : foto.type === 'image/webp' ? 'webp' : 'jpg'
    const fileName = `${randomUUID()}.${ext}`
    const bytes = new Uint8Array(await foto.arrayBuffer())

    const { error: uploadError } = await supabase.storage
      .from(FOTOS_BUCKET)
      .upload(fileName, bytes, { contentType: foto.type, upsert: false })

    if (uploadError) {
      return bad(`No s'ha pogut pujar la foto: ${uploadError.message}`, 500)
    }
    fotoPath = fileName
  }

  const { error: insertError } = await supabase.from('carnets').insert({
    nom,
    cognoms,
    equip,
    codi_federacio: codiFederacio,
    tutor_nom: tutorNom,
    tutor_email: tutorEmail,
    tutor_telefon: tutorTelefon,
    consentiment_rgpd: true,
    consentiment_data: new Date().toISOString(),
    foto_path: fotoPath,
    estat: 'pendent',
  })

  if (insertError) {
    return bad(`No s'ha pogut registrar la sol·licitud: ${insertError.message}`, 500)
  }

  return NextResponse.json({ ok: true })
}
