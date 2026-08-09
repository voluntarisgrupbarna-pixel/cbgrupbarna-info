import { createServiceClient } from '@/lib/supabase/service'
import { notFound } from 'next/navigation'
import { CheckCircle2, XCircle, Clock } from 'lucide-react'

export const dynamic = 'force-dynamic'

function fotoUrl(fotoPath: string | null): string | null {
  if (!fotoPath) return null
  const base = process.env.NEXT_PUBLIC_SUPABASE_URL
  return `${base}/storage/v1/object/public/carnets-fotos/${fotoPath}`
}

/**
 * Pàgina pública que obre el comerç sponsor en escanejar el QR del carnet.
 * Només mostra el mínim necessari per identificar visualment el jugador/a
 * (foto, nom, equip, validesa) — mai dades del tutor/a.
 */
export default async function VerificarPage({ params }: { params: { token: string } }) {
  const supabase = createServiceClient()

  // Seleccionem NOMÉS els camps públics — mai tutor_email/tutor_telefon/etc.
  const { data: carnet } = await supabase
    .from('carnets')
    .select('id, nom, cognoms, equip, temporada, estat, data_caducitat, foto_path')
    .eq('qr_token', params.token)
    .single()

  if (!carnet) notFound()

  const avui = new Date().toISOString().slice(0, 10)
  const caducat = carnet.data_caducitat ? carnet.data_caducitat < avui : false
  const valid = carnet.estat === 'actiu' && !caducat

  if (valid) {
    await supabase.from('verificacions').insert({ carnet_id: carnet.id })
  }

  const foto = fotoUrl(carnet.foto_path)

  return (
    <div className="max-w-sm mx-auto px-4 py-16 text-center">
      <div
        className={`rounded-2xl border p-8 ${
          valid ? 'border-green-500/30 bg-green-900/10' : 'border-red-500/30 bg-red-900/10'
        }`}
      >
        {foto ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={foto}
            alt={carnet.nom}
            className={`w-24 h-24 rounded-full object-cover mx-auto mb-4 border-4 ${
              valid ? 'border-green-500/40' : 'border-red-500/40'
            }`}
          />
        ) : (
          <div className="w-24 h-24 rounded-full bg-club-gray-2 mx-auto mb-4" />
        )}

        <div className="font-heading text-2xl text-club-cream font-semibold mb-1">
          {carnet.nom} {carnet.cognoms}
        </div>
        {carnet.equip && <div className="text-sm text-white/50 font-body mb-4">{carnet.equip}</div>}

        {valid ? (
          <div className="flex items-center justify-center gap-2 text-green-400 font-mono text-sm font-semibold">
            <CheckCircle2 className="w-5 h-5" /> CARNET VÀLID
          </div>
        ) : (
          <div className="flex items-center justify-center gap-2 text-red-400 font-mono text-sm font-semibold">
            <XCircle className="w-5 h-5" /> CARNET NO VÀLID
          </div>
        )}

        {carnet.data_caducitat && (
          <div className="flex items-center justify-center gap-1.5 text-white/30 font-mono text-xs mt-3">
            <Clock className="w-3.5 h-3.5" />
            Vàlid fins {new Date(carnet.data_caducitat).toLocaleDateString('ca-ES')}
          </div>
        )}
      </div>

      <p className="text-white/25 font-body text-xs mt-6">
        CB Grup Barna · Temporada {carnet.temporada}
      </p>
    </div>
  )
}
