import type { Metadata, Viewport } from 'next'
import './globals.css'
import { Navbar } from '@/components/Navbar'

export const viewport: Viewport = {
  themeColor: '#C8102E',
}

export const metadata: Metadata = {
  title: 'Carnet Digital · CB Grup Barna',
  description: 'Sol·licita el carnet digital del teu fill/a: identificació al club i descomptes als comerços col·laboradors.',
  icons: {
    icon: 'https://cbgrupbarna.info/favicon.svg',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ca">
      <body className="min-h-screen bg-club-black text-club-cream antialiased">
        <Navbar />
        <main className="pt-16">
          {children}
        </main>
        <footer className="mt-24 border-t border-white/5 py-8 text-center no-print">
          <p className="font-mono text-xs text-white/30">
            CB Grup Barna · Bàsquet al Clot · Sant Martí, Barcelona · des de 1965
          </p>
        </footer>
      </body>
    </html>
  )
}
