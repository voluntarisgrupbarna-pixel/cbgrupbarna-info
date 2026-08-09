import Link from 'next/link'

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-club-black/95 backdrop-blur-sm border-b border-white/5 no-print">
      <div className="max-w-3xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5">
          <img src="https://cbgrupbarna.info/logo.png" alt="CB Grup Barna" className="w-8 h-8 object-contain" />
          <span className="font-display text-xl tracking-wider text-club-cream">
            CARNET <span className="text-club-red">CB GRUP BARNA</span>
          </span>
        </Link>
        <a
          href="https://cbgrupbarna.info"
          className="font-body text-sm text-white/40 hover:text-club-cream transition-colors"
        >
          ← Tornar a la web
        </a>
      </div>
    </nav>
  )
}
