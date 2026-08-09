'use client'

import { useState } from 'react'
import { CreditCard, Loader2, CheckCircle2, AlertCircle, Ticket } from 'lucide-react'

export default function SolicitudPage() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{ ok: boolean; message: string } | null>(null)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)
    setResult(null)

    const form = e.currentTarget
    const data = new FormData(form)

    try {
      const res = await fetch('/api/carnets', { method: 'POST', body: data })
      const json = await res.json()
      if (!res.ok) throw new Error(json.error ?? 'Error desconegut')
      setResult({ ok: true, message: 'Sol·licitud enviada! Rebràs un email quan el club aprovi el carnet.' })
      form.reset()
    } catch (err) {
      setResult({ ok: false, message: err instanceof Error ? err.message : 'Error enviant la sol·licitud.' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-10">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 bg-club-red/10 border border-club-red/20 rounded-xl mb-4">
          <CreditCard className="w-7 h-7 text-club-red" />
        </div>
        <h1 className="section-title">
          SOL·LICITA EL <span className="text-club-red">CARNET</span>
        </h1>
        <p className="text-white/50 font-body mt-2 text-sm max-w-md mx-auto">
          El carnet digital del teu fill/a: identificació al club i descomptes
          als comerços col·laboradors del CB Grup Barna.
        </p>
      </div>

      <div className="card p-5 mb-6 flex gap-3 items-start">
        <Ticket className="w-5 h-5 text-club-red shrink-0 mt-0.5" />
        <p className="text-sm text-white/60 font-body">
          Un cop enviada la sol·licitud, el club la revisa i l&apos;aprova
          (normalment en 1-2 dies). Rebràs un email amb l&apos;enllaç per
          descarregar el carnet i afegir-lo a Google Wallet.
        </p>
      </div>

      {result && (
        <div
          className={`flex items-start gap-2 p-4 rounded-lg mb-6 text-sm font-body ${
            result.ok
              ? 'bg-green-900/30 border border-green-500/30 text-green-400'
              : 'bg-red-900/30 border border-red-500/30 text-red-400'
          }`}
        >
          {result.ok ? (
            <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
          )}
          {result.message}
        </div>
      )}

      {!result?.ok && (
        <form onSubmit={handleSubmit} className="card p-6 space-y-5">
          <div>
            <h2 className="font-heading text-lg text-club-cream font-semibold mb-3">Dades del jugador/a</h2>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Nom *</label>
                <input name="nom" required className="input" placeholder="Nom" />
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Cognoms *</label>
                <input name="cognoms" required className="input" placeholder="Cognoms" />
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Equip</label>
                <input name="equip" className="input" placeholder="Ex: Infantil Masculí" />
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">
                  Codi de jugador/a (federació) *
                </label>
                <input name="codi_federacio" required className="input" placeholder="Codi FCBQ" />
              </div>
              <div className="col-span-2">
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">
                  Foto (opcional, JPG/PNG/WebP, màx 5MB)
                </label>
                <input
                  name="foto"
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="input file:mr-3 file:py-1 file:px-3 file:rounded file:border-0 file:bg-club-red file:text-white file:text-xs"
                />
              </div>
            </div>
          </div>

          <div>
            <h2 className="font-heading text-lg text-club-cream font-semibold mb-3">Dades del tutor/a</h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="col-span-2">
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Nom del tutor/a *</label>
                <input name="tutor_nom" required className="input" placeholder="Nom i cognoms" />
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Email *</label>
                <input name="tutor_email" type="email" required className="input" placeholder="email@exemple.com" />
              </div>
              <div>
                <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Telèfon</label>
                <input name="tutor_telefon" type="tel" className="input" placeholder="600 000 000" />
              </div>
            </div>
          </div>

          <label className="flex items-start gap-2.5 cursor-pointer">
            <input
              name="consentiment_rgpd"
              type="checkbox"
              required
              className="accent-club-red w-4 h-4 mt-0.5 shrink-0"
            />
            <span className="text-xs text-white/50 font-body leading-relaxed">
              Autoritzo el CB Grup Barna a tractar les dades del meu fill/a
              (nom, foto, equip) amb la finalitat d&apos;emetre un carnet
              digital identificatiu per accedir a descomptes en comerços
              col·laboradors. Puc revocar aquest consentiment en qualsevol
              moment escrivint al club.
            </span>
          </label>

          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            {loading ? 'Enviant…' : 'Enviar sol·licitud'}
          </button>
        </form>
      )}
    </div>
  )
}
