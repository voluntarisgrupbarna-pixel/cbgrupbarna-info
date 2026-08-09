'use client'

import { Printer } from 'lucide-react'

export function PrintButton() {
  return (
    <button onClick={() => window.print()} className="btn-ghost w-full no-print">
      <Printer className="w-4 h-4" />
      Imprimeix / Desa en PDF
    </button>
  )
}
