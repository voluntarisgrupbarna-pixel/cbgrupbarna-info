'use client'

import { useState, useEffect, Suspense } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter, useSearchParams } from 'next/navigation'
import { ShieldCheck, Loader2, CheckCircle, AlertCircle } from 'lucide-react'

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams.get('redirectTo') ?? '/admin'
  const supabase = createClient()

  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (user) router.replace(redirectTo)
    })
  }, [])

  const handleMagicLink = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback?redirectTo=${redirectTo}` },
    })

    if (error) {
      setMessage({ type: 'error', text: error.message })
    } else {
      setMessage({ type: 'success', text: `Hem enviat un enllaç màgic a ${email}. Revisa el teu correu.` })
    }
    setLoading(false)
  }

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-club-red/10 border border-club-red/20 rounded-lg mb-4">
            <ShieldCheck className="w-6 h-6 text-club-red" />
          </div>
          <h1 className="font-display text-3xl tracking-wider text-club-cream">ADMIN CARNET</h1>
          <p className="text-white/40 text-sm font-body mt-1">Revisió i aprovació de sol·licituds</p>
        </div>

        {message && (
          <div
            className={`flex items-start gap-2 p-3 rounded-lg mb-4 text-sm font-body ${
              message.type === 'success'
                ? 'bg-green-900/30 border border-green-500/30 text-green-400'
                : 'bg-red-900/30 border border-red-500/30 text-red-400'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle className="w-4 h-4 mt-0.5 shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
            )}
            {message.text}
          </div>
        )}

        <form onSubmit={handleMagicLink} className="space-y-3">
          <div>
            <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="nom@email.com"
              required
              className="input"
            />
          </div>
          <p className="text-white/30 text-xs font-body">
            Fes servir un dels emails autoritzats del club. Rebràs un enllaç per entrar sense contrasenya.
          </p>
          <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Enviar enllaç'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  )
}
