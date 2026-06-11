import Link from 'next/link'
import { Camera } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex items-center justify-center text-center px-4">
      <div>
        <Camera className="w-12 h-12 text-white/10 mx-auto mb-4" />
        <h1 className="font-display text-6xl text-club-cream mb-2">404</h1>
        <p className="text-white/40 font-body mb-6">
          Aquesta pàgina no existeix o ha estat eliminada.
        </p>
        <Link href="/" className="btn-primary">
          Tornar a la galeria
        </Link>
      </div>
    </div>
  )
}
