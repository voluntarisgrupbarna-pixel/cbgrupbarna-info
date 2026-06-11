import { createClient } from '@/lib/supabase/server'
import { EventCard } from '@/components/EventCard'
import { SearchBar } from '@/components/SearchBar'
import { Suspense } from 'react'
import type { Event } from '@/lib/types'

export const dynamic = 'force-dynamic'

interface EventsPageProps {
  searchParams: Promise<{ q?: string; season?: string }>
}

async function EventsList({ q, season }: { q?: string; season?: string }) {
  const supabase = await createClient()
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!

  let query = supabase
    .from('events')
    .select(`
      *,
      season:seasons(*),
      cover_photo:photos!events_cover_photo_fk(*),
      photos_count:photos(count)
    `)
    .eq('is_published', true)
    .order('event_date', { ascending: false })

  if (q) {
    query = query.ilike('title', `%${q}%`)
  }
  if (season) {
    query = query.eq('season_id', parseInt(season))
  }

  const { data: events } = await query

  const processedEvents: Event[] = (events ?? []).map(e => ({
    ...e,
    photos_count: Array.isArray(e.photos_count) ? e.photos_count[0]?.count ?? 0 : 0,
  }))

  if (processedEvents.length === 0) {
    return (
      <div className="text-center py-24">
        <p className="text-white/30 font-body">
          {q ? `Cap resultat per "${q}"` : 'Encara no hi ha esdeveniments.'}
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      {processedEvents.map(event => (
        <EventCard key={event.id} event={event} supabaseUrl={supabaseUrl} />
      ))}
    </div>
  )
}

async function SeasonFilter({ activeSeason }: { activeSeason?: string }) {
  const supabase = await createClient()
  const { data: seasons } = await supabase
    .from('seasons')
    .select('*')
    .order('name', { ascending: false })

  if (!seasons?.length) return null

  return (
    <div className="flex flex-wrap gap-2">
      <a
        href="/events"
        className={`font-mono text-xs px-3 py-1.5 rounded border transition-colors ${
          !activeSeason
            ? 'bg-club-red border-club-red text-white'
            : 'border-white/10 text-white/40 hover:border-white/30 hover:text-white/70'
        }`}
      >
        Totes
      </a>
      {seasons.map(s => (
        <a
          key={s.id}
          href={`/events?season=${s.id}`}
          className={`font-mono text-xs px-3 py-1.5 rounded border transition-colors ${
            activeSeason === String(s.id)
              ? 'bg-club-red border-club-red text-white'
              : 'border-white/10 text-white/40 hover:border-white/30 hover:text-white/70'
          }`}
        >
          {s.name}
          {s.is_active && (
            <span className="ml-1.5 inline-block w-1.5 h-1.5 bg-green-400 rounded-full" />
          )}
        </a>
      ))}
    </div>
  )
}

export default async function EventsPage({ searchParams }: EventsPageProps) {
  const { q, season } = await searchParams

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="section-title mb-2">
          Tots els <span className="text-club-red">Esdeveniments</span>
        </h1>
        <p className="text-white/40 font-body">
          Historial fotogràfic del CB Grup Barna
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4 mb-8">
        <Suspense>
          <SearchBar
            placeholder="Cerca un esdeveniment..."
            className="flex-1 max-w-sm"
          />
        </Suspense>
        <Suspense>
          <SeasonFilter activeSeason={season} />
        </Suspense>
      </div>

      {/* Events grid */}
      <Suspense
        fallback={
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="card">
                <div className="aspect-[4/3] shimmer" />
                <div className="p-4 space-y-2">
                  <div className="h-5 shimmer rounded w-3/4" />
                  <div className="h-3 shimmer rounded w-1/2" />
                </div>
              </div>
            ))}
          </div>
        }
      >
        <EventsList q={q} season={season} />
      </Suspense>
    </div>
  )
}
