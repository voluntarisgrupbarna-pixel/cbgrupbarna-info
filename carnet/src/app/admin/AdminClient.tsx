'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import {
  CheckCircle, XCircle, Ban, Copy, Loader2, ExternalLink, Clock,
} from 'lucide-react'
import type { Carnet, Profile } from '@/lib/types'

interface Props {
  profile: Profile
  initialCarnets: Carnet[]
}

const ESTAT_LABEL: Record<Carnet['estat'], string> = {
  pendent: 'Pendent',
  actiu: 'Actiu',
  rebutjat: 'Rebutjat',
  revocat: 'Revocat',
  caducat: 'Caducat',
}

const ESTAT_COLOR: Record<Carnet['estat'], string> = {
  pendent: 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10',
  actiu: 'text-green-400 border-green-400/30 bg-green-400/10',
  rebutjat: 'text-red-400 border-red-400/30 bg-red-400/10',
  revocat: 'text-white/40 border-white/20 bg-white/5',
  caducat: 'text-white/40 border-white/20 bg-white/5',
}

function fotoUrl(fotoPath: string | null): string | null {
  if (!fotoPath) return null
  const base = process.env.NEXT_PUBLIC_SUPABASE_URL
  return `${base}/storage/v1/object/public/carnets-fotos/${fotoPath}`
}

/** Fi de temporada per defecte: 30 de juny de l'any en curs o el següent. */
function defaultCaducitat(): string {
  const now = new Date()
  const year = now.getMonth() >= 6 ? now.getFullYear() + 1 : now.getFullYear()
  return `${year}-06-30`
}

export function AdminClient({ profile, initialCarnets }: Props) {
  const supabase = createClient()
  const [carnets, setCarnets] = useState<Carnet[]>(initialCarnets)
  const [tab, setTab] = useState<'pendent' | 'actiu' | 'altres'>('pendent')
  const [busyId, setBusyId] = useState<string | null>(null)
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const filtered = carnets.filter(c => {
    if (tab === 'pendent') return c.estat === 'pendent'
    if (tab === 'actiu') return c.estat === 'actiu'
    return c.estat === 'rebutjat' || c.estat === 'revocat' || c.estat === 'caducat'
  })

  async function aprovar(c: Carnet) {
    setBusyId(c.id)
    const { data, error } = await supabase
      .from('carnets')
      .update({
        estat: 'actiu',
        aprovat_per: profile.id,
        aprovat_at: new Date().toISOString(),
        data_caducitat: defaultCaducitat(),
      })
      .eq('id', c.id)
      .select()
      .single()
    if (!error && data) setCarnets(prev => prev.map(x => (x.id === c.id ? data : x)))
    setBusyId(null)
  }

  async function rebutjar(c: Carnet) {
    const motiu = window.prompt('Motiu del rebuig (opcional):') ?? ''
    setBusyId(c.id)
    const { data, error } = await supabase
      .from('carnets')
      .update({ estat: 'rebutjat', notes_admin: motiu || null })
      .eq('id', c.id)
      .select()
      .single()
    if (!error && data) setCarnets(prev => prev.map(x => (x.id === c.id ? data : x)))
    setBusyId(null)
  }

  async function revocar(c: Carnet) {
    if (!window.confirm(`Revocar el carnet de ${c.nom} ${c.cognoms}? Deixarà de ser vàlid als comerços.`)) return
    setBusyId(c.id)
    const { data, error } = await supabase
      .from('carnets')
      .update({ estat: 'revocat' })
      .eq('id', c.id)
      .select()
      .single()
    if (!error && data) setCarnets(prev => prev.map(x => (x.id === c.id ? data : x)))
    setBusyId(null)
  }

  function copyLink(c: Carnet) {
    const url = `${window.location.origin}/carnet/${c.access_token}`
    navigator.clipboard.writeText(url)
    setCopiedId(c.id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const tabs = [
    { id: 'pendent' as const, label: 'Pendents', count: carnets.filter(c => c.estat === 'pendent').length },
    { id: 'actiu' as const, label: 'Actius', count: carnets.filter(c => c.estat === 'actiu').length },
    { id: 'altres' as const, label: 'Altres', count: carnets.filter(c => !['pendent', 'actiu'].includes(c.estat)).length },
  ]

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="mb-6">
        <h1 className="section-title">
          <span className="text-club-red">ADMIN</span> CARNETS
        </h1>
        <p className="text-white/30 font-mono text-xs mt-1">{profile.full_name ?? profile.id}</p>
      </div>

      <div className="flex border-b border-white/10 mb-6 gap-1">
        {tabs.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-body border-b-2 transition-colors ${
              tab === t.id ? 'border-club-red text-club-cream' : 'border-transparent text-white/40 hover:text-white/70'
            }`}
          >
            {t.label}
            <span className="font-mono text-xs bg-white/10 px-1.5 py-0.5 rounded">{t.count}</span>
          </button>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-white/30 font-body text-sm py-8 text-center">No hi ha carnets en aquest estat.</div>
      )}

      <div className="space-y-3">
        {filtered.map(c => {
          const foto = fotoUrl(c.foto_path)
          return (
            <div key={c.id} className="card p-4 flex gap-4">
              {foto ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={foto} alt="" className="w-16 h-16 rounded-full object-cover shrink-0 bg-club-gray-2" />
              ) : (
                <div className="w-16 h-16 rounded-full bg-club-gray-2 shrink-0" />
              )}

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-heading text-club-cream font-semibold">{c.nom} {c.cognoms}</span>
                  <span className={`font-mono text-xs px-2 py-0.5 rounded border ${ESTAT_COLOR[c.estat]}`}>
                    {ESTAT_LABEL[c.estat]}
                  </span>
                  {c.equip && <span className="tag">{c.equip}</span>}
                </div>
                <div className="text-xs text-white/40 font-mono mt-1">
                  Codi federació: {c.codi_federacio}
                </div>
                <div className="text-xs text-white/40 font-body mt-1">
                  Tutor/a: {c.tutor_nom} · {c.tutor_email}{c.tutor_telefon ? ` · ${c.tutor_telefon}` : ''}
                </div>
                <div className="flex items-center gap-1 text-xs text-white/25 font-mono mt-1">
                  <Clock className="w-3 h-3" />
                  {new Date(c.created_at).toLocaleString('ca-ES')}
                </div>
                {c.notes_admin && (
                  <div className="text-xs text-white/40 font-body mt-1 italic">Nota: {c.notes_admin}</div>
                )}
              </div>

              <div className="flex flex-col gap-1.5 shrink-0 items-end">
                {c.estat === 'pendent' && (
                  <>
                    <button
                      onClick={() => aprovar(c)}
                      disabled={busyId === c.id}
                      className="btn-primary text-xs py-1.5 px-3"
                    >
                      {busyId === c.id ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle className="w-3.5 h-3.5" />}
                      Aprovar
                    </button>
                    <button
                      onClick={() => rebutjar(c)}
                      disabled={busyId === c.id}
                      className="text-xs text-white/40 hover:text-red-400 flex items-center gap-1 py-1"
                    >
                      <XCircle className="w-3.5 h-3.5" /> Rebutjar
                    </button>
                  </>
                )}
                {c.estat === 'actiu' && (
                  <>
                    <button
                      onClick={() => copyLink(c)}
                      className="btn-ghost text-xs py-1.5 px-3"
                    >
                      <Copy className="w-3.5 h-3.5" /> {copiedId === c.id ? 'Copiat!' : 'Copiar enllaç'}
                    </button>
                    <a
                      href={`/carnet/${c.access_token}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs text-white/40 hover:text-club-cream flex items-center gap-1 py-1"
                    >
                      <ExternalLink className="w-3.5 h-3.5" /> Obrir
                    </a>
                    <button
                      onClick={() => revocar(c)}
                      disabled={busyId === c.id}
                      className="text-xs text-white/40 hover:text-red-400 flex items-center gap-1 py-1"
                    >
                      <Ban className="w-3.5 h-3.5" /> Revocar
                    </button>
                  </>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
