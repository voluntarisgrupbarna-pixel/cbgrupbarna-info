import { createServiceClient } from '@/lib/supabase/service'
import { buildGoogleWalletSaveUrl } from '@/lib/googleWallet'
import { qrDataUrl } from '@/lib/qr'
import { PrintButton } from '@/components/PrintButton'
import { notFound } from 'next/navigation'
import { AlertTriangle } from 'lucide-react'
import type { Carnet } from '@/lib/types'

export const dynamic = 'force-dynamic'

function fotoUrl(fotoPath: string | null): string | null {
  if (!fotoPath) return null
  const base = process.env.NEXT_PUBLIC_SUPABASE_URL
  return `${base}/storage/v1/object/public/carnets-fotos/${fotoPath}`
}

function baseUrl() {
  return process.env.NEXT_PUBLIC_BASE_URL ?? 'http://localhost:3000'
}

export default async function CarnetPage({ params }: { params: { token: string } }) {
  const supabase = createServiceClient()
  const { data: carnet } = await supabase
    .from('carnets')
    .select('*')
    .eq('access_token', params.token)
    .single<Carnet>()

  if (!carnet) notFound()

  if (carnet.estat === 'pendent') {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <AlertTriangle className="w-10 h-10 text-yellow-400 mx-auto mb-4" />
        <h1 className="font-display text-2xl text-club-cream mb-2">SOL·LICITUD EN REVISIÓ</h1>
        <p className="text-white/50 font-body text-sm">
          El carnet de {carnet.nom} encara no ha estat aprovat pel club.
          Rebràs un email quan estigui llest.
        </p>
      </div>
    )
  }

  if (carnet.estat !== 'actiu') {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <AlertTriangle className="w-10 h-10 text-red-400 mx-auto mb-4" />
        <h1 className="font-display text-2xl text-club-cream mb-2">CARNET NO DISPONIBLE</h1>
        <p className="text-white/50 font-body text-sm">
          Aquest carnet ha estat {carnet.estat === 'rebutjat' ? 'rebutjat' : carnet.estat === 'revocat' ? 'revocat' : 'donat de baixa'}.
          Contacta amb el club si creus que és un error.
        </p>
      </div>
    )
  }

  const foto = fotoUrl(carnet.foto_path)
  const verificationUrl = `${baseUrl()}/verificar/${carnet.qr_token}`
  const qr = await qrDataUrl(verificationUrl)
  const walletUrl = buildGoogleWalletSaveUrl(carnet, { baseUrl: baseUrl(), fotoUrl: foto })

  return (
    <div className="max-w-md mx-auto px-4 py-10">
      <div className="text-center mb-6 no-print">
        <h1 className="section-title">EL TEU <span className="text-club-red">CARNET</span></h1>
        <p className="text-white/40 font-body text-sm mt-1">
          Descarrega&apos;l a Google Wallet o desa&apos;l com a PDF per ensenyar-lo als comerços col·laboradors.
        </p>
      </div>

      {/* Targeta imprimible */}
      <div
        id="printable-card"
        className="rounded-2xl overflow-hidden border border-white/10 bg-gradient-to-br from-club-gray-1 to-club-black p-6"
      >
        <div className="flex items-center gap-3 mb-5">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="https://cbgrupbarna.info/logo.png" alt="CB Grup Barna" className="w-10 h-10 object-contain" />
          <div>
            <div className="font-display text-lg tracking-wide text-club-cream leading-none">CB GRUP BARNA</div>
            <div className="text-xs text-club-red font-mono tracking-widest">CARNET DE SOCI/A</div>
          </div>
        </div>

        <div className="flex items-center gap-4 mb-5">
          {foto ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={foto} alt={carnet.nom} className="w-20 h-20 rounded-full object-cover border-2 border-club-red/40" />
          ) : (
            <div className="w-20 h-20 rounded-full bg-club-gray-2 border-2 border-club-red/40" />
          )}
          <div>
            <div className="font-heading text-xl text-club-cream font-semibold leading-tight">
              {carnet.nom} {carnet.cognoms}
            </div>
            {carnet.equip && <div className="text-sm text-white/50 font-body">{carnet.equip}</div>}
            <div className="text-xs text-white/30 font-mono mt-1">Temporada {carnet.temporada}</div>
          </div>
        </div>

        <div className="flex items-center justify-between bg-white rounded-lg p-3">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={qr} alt="Codi QR de verificació" className="w-24 h-24" />
          <div className="text-right pr-2">
            <div className="text-[10px] text-black/40 font-mono uppercase tracking-widest">Vàlid fins</div>
            <div className="text-sm text-black font-mono font-semibold">
              {carnet.data_caducitat ? new Date(carnet.data_caducitat).toLocaleDateString('ca-ES') : '—'}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 space-y-2 no-print">
        {walletUrl ? (
          <a href={walletUrl} className="block">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="https://developers.google.com/static/wallet/generic/resources/add-to-google-wallet-button.svg"
              alt="Afegir a Google Wallet"
              className="w-full"
            />
          </a>
        ) : (
          <p className="text-xs text-white/30 font-body text-center">
            (Google Wallet encara no configurat pel club — fes servir el PDF)
          </p>
        )}
        <PrintButton />
      </div>

      <p className="mt-6 text-xs text-white/25 font-body text-center no-print">
        El QR es pot escanejar als comerços col·laboradors per verificar el carnet i aplicar el descompte.
      </p>
    </div>
  )
}
