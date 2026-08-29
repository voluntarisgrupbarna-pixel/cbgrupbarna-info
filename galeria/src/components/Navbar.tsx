'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Camera, Upload, Settings, LogOut, LogIn, Menu, X } from 'lucide-react'
import type { User } from '@supabase/supabase-js'
import type { Profile } from '@/lib/types'

export function Navbar() {
  const pathname = usePathname()
  const router = useRouter()
  const supabase = createClient()
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user)
      if (user) {
        supabase
          .from('profiles')
          .select('*')
          .eq('id', user.id)
          .single()
          .then(({ data }) => setProfile(data))
      }
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
      if (!session?.user) setProfile(null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const handleSignOut = async () => {
    await supabase.auth.signOut()
    router.push('/')
    router.refresh()
  }

  const navLinks = [
    { href: '/', label: 'Inici' },
    { href: '/events', label: 'Esdeveniments' },
  ]

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-club-black/95 backdrop-blur-sm border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <Camera className="w-5 h-5 text-club-red group-hover:text-club-red-light transition-colors" />
          <span className="font-display text-xl tracking-wider text-club-cream">
            GALERIA CB GRUP BARNA
          </span>
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-6">
          {navLinks.map(link => (
            <Link
              key={link.href}
              href={link.href}
              className={`font-body text-sm transition-colors ${
                pathname === link.href
                  ? 'text-club-red'
                  : 'text-white/60 hover:text-club-cream'
              }`}
            >
              {link.label}
            </Link>
          ))}

          {user ? (
            <div className="flex items-center gap-3">
              <Link href="/upload" className="btn-primary text-sm py-1.5 px-4">
                <Upload className="w-3.5 h-3.5" />
                Pujar
              </Link>
              {profile?.role === 'admin' || profile?.role === 'editor' ? (
                <Link
                  href="/admin"
                  className={`text-white/50 hover:text-white transition-colors ${
                    pathname.startsWith('/admin') ? 'text-white' : ''
                  }`}
                  aria-label="Administració"
                  title="Administració"
                >
                  <Settings className="w-4.5 h-4.5" />
                </Link>
              ) : null}
              <button
                onClick={handleSignOut}
                className="text-white/40 hover:text-white/80 transition-colors"
                title="Tancar sessió"
                aria-label="Tancar sessió"
              >
                <LogOut className="w-4 h-4" />
              </button>
              <span className="font-mono text-xs text-white/30 border border-white/10 px-2 py-0.5 rounded">
                {profile?.role ?? 'viewer'}
              </span>
            </div>
          ) : (
            <Link href="/login" className="btn-ghost text-sm py-1.5 px-4">
              <LogIn className="w-3.5 h-3.5" />
              Entrar
            </Link>
          )}
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden text-white/60 hover:text-white transition-colors"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label={menuOpen ? 'Tancar el menú' : 'Obrir el menú'}
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-club-gray-1 border-t border-white/5 px-4 py-4 flex flex-col gap-3">
          {navLinks.map(link => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              className={`font-body py-2 transition-colors ${
                pathname === link.href ? 'text-club-red' : 'text-white/60'
              }`}
            >
              {link.label}
            </Link>
          ))}
          {user ? (
            <>
              <Link href="/upload" onClick={() => setMenuOpen(false)} className="btn-primary w-full justify-center">
                <Upload className="w-4 h-4" />
                Pujar fotos
              </Link>
              {(profile?.role === 'admin' || profile?.role === 'editor') && (
                <Link href="/admin" onClick={() => setMenuOpen(false)} className="btn-ghost w-full justify-center">
                  <Settings className="w-4 h-4" />
                  Administrar
                </Link>
              )}
              <button onClick={handleSignOut} className="text-white/40 hover:text-white/80 text-sm text-left py-2">
                Tancar sessió
              </button>
            </>
          ) : (
            <Link href="/login" onClick={() => setMenuOpen(false)} className="btn-ghost w-full justify-center">
              <LogIn className="w-4 h-4" />
              Entrar
            </Link>
          )}
        </div>
      )}
    </nav>
  )
}
