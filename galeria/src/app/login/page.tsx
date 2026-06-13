'use client'

import { useState, useEffect, Suspense } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { Camera, Loader2, CheckCircle, AlertCircle } from 'lucide-react'

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams.get('redirectTo') ?? '/'
  const supabase = createClient()

  const [mode, setMode] = useState<'signin' | 'signup' | 'magic'>('signin')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (user) router.replace(redirectTo)
    })
  }, [])

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    const { error } = await supabase.auth.signInWithPassword({ email, password })

    if (error) {
      setMessage({ type: 'error', text: 'Credencials incorrectes. Torna-ho a intentar.' })
    } else {
      router.push(redirectTo)
      router.refresh()
    }
    setLoading(false)
  }

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { full_name: fullName },
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      setMessage({ type: 'error', text: error.message })
    } else {
      setMessage({
        type: 'success',
        text: 'Compte creat! Revisa el teu email per confirmar el registre.',
      })
    }
    setLoading(false)
  }

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
      setMessage({
        type: 'success',
        text: `Hem enviat un enllaç màgic a ${email}. Revisa el teu correu.`,
      })
    }
    setLoading(false)
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-club-red mb-4">
            <Camera className="w-6 h-6 text-white" />
          </div>
          <h1 className="font-display text-3xl tracking-wider text-club-cream">
            CB GRUP BARNA
          </h1>
          <p className="text-white/40 text-sm font-body mt-1">Galeria de fotos del club</p>
        </div>

        {/* Mode tabs */}
        <div className="flex border border-white/10 rounded-lg p-1 mb-6 bg-club-gray-1">
          {(['signin', 'signup', 'magic'] as const).map(m => (
            <button
              key={m}
              onClick={() => { setMode(m); setMessage(null) }}
              className={`flex-1 py-1.5 text-sm font-body rounded transition-colors ${
                mode === m
                  ? 'bg-club-red text-white'
                  : 'text-white/40 hover:text-white/70'
              }`}
            >
              {m === 'signin' ? 'Entrar' : m === 'signup' ? 'Registrar-se' : 'Enllaç màgic'}
            </button>
          ))}
        </div>

        {/* Message */}
        {message && (
          <div className={`flex items-start gap-2 p-3 rounded-lg mb-4 text-sm font-body ${
            message.type === 'success'
              ? 'bg-green-900/30 border border-green-500/30 text-green-400'
              : 'bg-red-900/30 border border-red-500/30 text-red-400'
          }`}>
            {message.type === 'success'
              ? <CheckCircle className="w-4 h-4 mt-0.5 shrink-0" />
              : <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />}
            {message.text}
          </div>
        )}

        {/* Forms */}
        {mode === 'signin' && (
          <form onSubmit={handleSignIn} className="space-y-3">
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="nom@email.com"
                required
                className="input"
              />
            </div>
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Contrasenya
              </label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="input"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full justify-center mt-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Entrar'}
            </button>
          </form>
        )}

        {mode === 'signup' && (
          <form onSubmit={handleSignUp} className="space-y-3">
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Nom complet
              </label>
              <input
                type="text"
                value={fullName}
                onChange={e => setFullName(e.target.value)}
                placeholder="El teu nom"
                required
                className="input"
              />
            </div>
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="nom@email.com"
                required
                className="input"
              />
            </div>
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Contrasenya
              </label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Mínim 6 caràcters"
                minLength={6}
                required
                className="input"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full justify-center mt-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Crear compte'}
            </button>
          </form>
        )}

        {mode === 'magic' && (
          <form onSubmit={handleMagicLink} className="space-y-3">
            <div>
              <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
                Email
              </label>
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
              Et enviarem un enllaç per entrar sense contrasenya.
            </p>
            <button type="submit" disabled={loading} className="btn-primary w-full justify-center mt-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Enviar enllaç'}
            </button>
          </form>
        )}

        <p className="mt-6 text-center text-xs text-white/20 font-body">
          <Link href="/" className="hover:text-white/40 transition-colors">
            ← Tornar a la galeria
          </Link>
        </p>
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
