'use client'

import { useEffect, useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { UploadZone } from '@/components/UploadZone'
import Link from 'next/link'
import { ArrowLeft, CheckCircle, ChevronDown } from 'lucide-react'
import type { Event, Profile } from '@/lib/types'

function UploadPageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const preselectedEventId = searchParams.get('event')
  const supabase = createClient()

  const [user, setUser] = useState<{ id: string } | null>(null)
  const [profile, setProfile] = useState<Profile | null>(null)
  const [events, setEvents] = useState<Event[]>([])
  const [selectedEventId, setSelectedEventId] = useState<number | null>(
    preselectedEventId ? parseInt(preselectedEventId) : null
  )
  const [uploadedCount, setUploadedCount] = useState(0)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (!user) {
        router.replace('/login?redirectTo=/upload')
        return
      }
      setUser(user)

      Promise.all([
        supabase.from('profiles').select('*').eq('id', user.id).single(),
        supabase
          .from('events')
          .select('*, season:seasons(*)')
          .eq('is_published', true)
          .eq('allow_member_uploads', true)
          .order('event_date', { ascending: false }),
      ]).then(([profileRes, eventsRes]) => {
        setProfile(profileRes.data)
        setEvents(eventsRes.data ?? [])
        setLoading(false)
      })
    })
  }, [])

  const selectedEvent = events.find(e => e.id === selectedEventId)

  if (loading) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12">
        <div className="space-y-4">
          <div className="h-8 shimmer rounded w-48" />
          <div className="h-48 shimmer rounded" />
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <Link
        href={selectedEvent ? `/events/${selectedEvent.id}` : '/events'}
        className="inline-flex items-center gap-1.5 text-white/40 hover:text-white/80 transition-colors text-sm font-body mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        {selectedEvent ? selectedEvent.title : 'Tornar'}
      </Link>

      <h1 className="section-title mb-2">
        Pujar <span className="text-club-red">Fotos</span>
      </h1>
      <p className="text-white/40 font-body mb-8">
        Afegeix fotos al repositori del club. Les teves fotos seran visibles per tots els membres.
      </p>

      {/* Success message */}
      {uploadedCount > 0 && (
        <div className="flex items-center gap-2 bg-green-900/30 border border-green-500/30 text-green-400 p-4 rounded-lg mb-6">
          <CheckCircle className="w-5 h-5 shrink-0" />
          <p className="font-body text-sm">
            {uploadedCount} foto{uploadedCount !== 1 ? 's' : ''} pujada{uploadedCount !== 1 ? 's' : ''} correctament!
            {selectedEvent && (
              <> <Link href={`/events/${selectedEvent.id}`} className="underline">Veure l&apos;event</Link></>
            )}
          </p>
        </div>
      )}

      {/* Event selector */}
      <div className="mb-6">
        <label className="block text-xs text-white/40 mb-1.5 font-mono uppercase tracking-wider">
          Esdeveniment *
        </label>
        <div className="relative">
          <select
            value={selectedEventId ?? ''}
            onChange={e => setSelectedEventId(e.target.value ? parseInt(e.target.value) : null)}
            className="input appearance-none pr-10 cursor-pointer"
          >
            <option value="">Selecciona un event...</option>
            {events.map(event => (
              <option key={event.id} value={event.id}>
                {event.title}
                {event.event_date
                  ? ` · ${new Date(event.event_date).toLocaleDateString('ca-ES')}`
                  : ''}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30 pointer-events-none" />
        </div>
      </div>

      {/* Upload zone */}
      {selectedEventId && user ? (
        <UploadZone
          eventId={selectedEventId}
          userId={user.id}
          onUploadComplete={count => setUploadedCount(prev => prev + count)}
        />
      ) : (
        <div className="border-2 border-dashed border-white/10 rounded-lg p-10 text-center">
          <p className="text-white/30 font-body text-sm">
            Selecciona un esdeveniment per començar a pujar fotos
          </p>
        </div>
      )}

      {/* Role info */}
      {profile && (
        <p className="mt-6 text-xs text-white/20 font-mono text-center">
          Rol actual: {profile.role} · {profile.full_name ?? user?.id}
        </p>
      )}
    </div>
  )
}

export default function UploadPage() {
  return (
    <Suspense>
      <UploadPageContent />
    </Suspense>
  )
}
