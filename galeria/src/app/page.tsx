import Link from 'next/link'
import { createClient } from '@/lib/supabase/server'
import { EventCard } from '@/components/EventCard'
import { ArrowRight, Images, Users, Calendar } from 'lucide-react'
import type { Event } from '@/lib/types'

export const dynamic = 'force-dynamic'

export default async function HomePage() {
  const supabase = await createClient()
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!

  // Get recent events with photo count and cover
  const { data: events } = await supabase
    .from('events')
    .select(`
      *,
      season:seasons(*),
      cover_photo:photos!events_cover_photo_fk(*),
      photos_count:photos(count)
    `)
    .eq('is_published', true)
    .order('event_date', { ascending: false })
    .limit(6)

  // Stats
  const [{ count: totalPhotos }, { count: totalEvents }, { count: totalMembers }] =
    await Promise.all([
      supabase.from('photos').select('*', { count: 'exact', head: true }).eq('is_approved', true),
      supabase.from('events').select('*', { count: 'exact', head: true }).eq('is_published', true),
      supabase.from('profiles').select('*', { count: 'exact', head: true }),
    ])

  const processedEvents: Event[] = (events ?? []).map(e => ({
    ...e,
    photos_count: Array.isArray(e.photos_count) ? e.photos_count[0]?.count ?? 0 : 0,
  }))

  return (
    <div>
      {/* Hero */}
      <section className="relative min-h-[50vh] flex items-center justify-center overflow-hidden bg-black border-b border-white/5">
        {/* Red accent bar — top */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-club-red" />
        <div className="relative text-center px-4 py-24">
          <p className="font-mono text-xs text-white/30 tracking-[0.35em] uppercase mb-8">
            CB Grup Barna · Bàsquet al Clot · des de 1965
          </p>
          <h1 className="font-display text-7xl md:text-9xl text-white tracking-wider leading-none mb-8 uppercase">
            GALERIA<br /><span className="text-club-red">FOTOS</span>
          </h1>
          <p className="font-body text-white/40 max-w-md mx-auto mb-10">
            El repositori fotogràfic oficial del club. Tots els esdeveniments, totes les temporades.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <Link href="/events" className="btn-primary">
              Veure tots els events
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/upload" className="btn-ghost">
              Pujar fotos
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="border-b border-white/5 bg-club-gray-1">
        <div className="max-w-7xl mx-auto px-4 py-8 grid grid-cols-3 gap-4">
          {[
            { icon: Images, value: totalPhotos ?? 0, label: 'Fotos' },
            { icon: Calendar, value: totalEvents ?? 0, label: 'Esdeveniments' },
            { icon: Users, value: totalMembers ?? 0, label: 'Membres' },
          ].map(({ icon: Icon, value, label }) => (
            <div key={label} className="text-center">
              <Icon className="w-5 h-5 text-club-red/60 mx-auto mb-1" />
              <div className="font-display text-3xl text-club-cream">{value.toLocaleString('ca-ES')}</div>
              <div className="font-mono text-xs text-white/30 uppercase tracking-wider">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Recent events */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="section-title">Darrers <span className="text-club-red">Eventos</span></h2>
          <Link
            href="/events"
            className="text-sm text-white/40 hover:text-white/80 transition-colors flex items-center gap-1 font-body"
          >
            Veure tots
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {processedEvents.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {processedEvents.map(event => (
              <EventCard key={event.id} event={event} supabaseUrl={supabaseUrl} />
            ))}
          </div>
        ) : (
          <div className="text-center py-24">
            <Images className="w-12 h-12 text-white/10 mx-auto mb-3" />
            <p className="text-white/30 font-body">Encara no hi ha esdeveniments publicats.</p>
          </div>
        )}
      </section>
    </div>
  )
}
