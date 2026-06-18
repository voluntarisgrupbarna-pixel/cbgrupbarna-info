import type { Metadata, Viewport } from 'next'
import Script from 'next/script'
import { Analytics } from '@vercel/analytics/react'
import './globals.css'
import { Navbar } from '@/components/Navbar'

export const viewport: Viewport = {
  themeColor: '#C8102E',
}

export const metadata: Metadata = {
  title: 'Galeria Fotos · CB Grup Barna',
  description: 'Repositori fotogràfic oficial del CB Grup Barna · Bàsquet al Clot · Sant Martí, Barcelona · des de 1965',
  keywords: ['CB Grup Barna', 'bàsquet', 'fotos', 'galeria', 'Clot', 'Sant Martí', 'Barcelona'],
  openGraph: {
    title: 'Galeria Fotos · CB Grup Barna',
    description: 'Repositori fotogràfic oficial del CB Grup Barna',
    siteName: 'CB Grup Barna',
    locale: 'ca_ES',
    type: 'website',
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
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
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-R6XYR7G1WF"
          strategy="afterInteractive"
        />
        <Script id="ga4-galeria" strategy="afterInteractive">{`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-R6XYR7G1WF', { send_page_view: true });
        `}</Script>
        <Navbar />
        <main className="pt-16">
          {children}
        </main>
        <footer className="mt-24 border-t border-white/5 py-8 text-center">
          <p className="font-mono text-xs text-white/30">
            CB Grup Barna · Bàsquet al Clot · Sant Martí, Barcelona · des de 1965
          </p>
          <p className="font-mono text-xs text-white/20 mt-1">
            #somclot
          </p>
        </footer>
        <Analytics />
      </body>
    </html>
  )
}
