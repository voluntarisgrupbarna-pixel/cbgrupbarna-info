import { createClient } from '@/lib/supabase/server'
import { PhotoGrid } from '@/components/PhotoGrid'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import {
  ArrowLeft, Calendar, MapPin, Images, Download,
  Upload, Users
} from 'lucide-react'
import type { Photo } from '@/lib/types'

export const dynamic = 'force-dynamic'

interface EventPageProps {
  params: Promise<{ eventId: string }>
}

export async function generateMetadata({ params }: EventPageProps) {
  const { eventId } = await params
  const supabase = await createClient()
  const { data: event } = await supabase
    .from('events')
    .select('title, description')
    .eq('id', parseInt(eventId))
    .single()

  if (!event) return { title: 'Esdeveniment · CB Grup Barna' }

  return {
    title: `${event.title} · CB Grup Barna`,
    description: event.description ?? `Fotos de ${event.title}`,
  }
}

export default async function EventPage({ params }: EventPageProps) {
  const { eventId } = await params
  const supabase = await createClient()
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!

  const { data: { user } } = await supabase.auth.getUser()

  // Get event
  const { data: event } = await supabase
    .from('events')
    .select(`*, season:seasons(*), cover_photo:photos!events_cover_photo_fk(*)`)
    .eq('id', parseInt(eventId))
    .eq('is_published', true)
    .single()

  if (!event) notFound()

  // Get photos with like status for current user
  const photosQuery = supabase
    .from('photos')
    .select('*')
    .eq('event_id', event.id)
    .eq('is_approved', true)
    .order('uploaded_at', { ascending: true })

  const { data: photos } = await photosQuery

  // Get user profile
  let userProfile = null
  let likedPhotoIds = new Set<number>()

  if (user) {
    const [profileResult, likesResult] = await Promise.all([
      supabase.from('profiles').select('*').eq('id', user.id).single(),
      supabase.from('photo_likes').select('photo_id').eq('user_id', user.id),
    ])
    userProfile = profileResult.data
    likedPhotoIds = new Set((likesResult.data ?? []).map(l => l.photo_id))
  }

  const processedPhotos: Photo[] = (photos ?? []).map(p => ({
    ...p,
    liked_by_user: likedPhotoIds.has(p.id),
  }))

  const formattedDate = event.event_date
    ? new Date(event.event_date).toLocaleDateString('ca-ES', {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    : null

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Back */}
      <Link
        href="/events"
        className="inline-flex items-center gap-1.5 text-white/40 hover:text-white/80 transition-colors text-sm font-body mb-6"
      >
        <ArrowLeft className="w-4 h-4" />
        Tots els esdeveniments
      </Link>

      {/* Event header */}
      <div className="mb-8 border-b border-white/5 pb-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            {event.season && (
              <span className="tag mb-3 inline-block">{event.season.name}</span>
            )}
            <h1 className="font-heading text-4xl md:text-5xl font-bold text-club-cream mb-3">
              {event.title}
            </h1>
            {event.description && (
              <p className="text-white/50 font-body max-w-2xl">{event.description}</p>
            )}

            <div className="flex flex-wrap gap-4 mt-4 text-sm text-white/40">
              {formattedDate && (
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-4 h-4" />
                  <span className="capitalize">{formattedDate}</span>
                </span>
              )}
              {event.location && (
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-4 h-4" />
                  {event.location}
                </span>
              )}
              <span className="flex items-center gap-1.5">
                <Images className="w-4 h-4" />
                {processedPhotos.length} foto{processedPhotos.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-2 flex-wrap">
            {event.allow_downloads && processedPhotos.length > 0 && (
              <div className="flex items-center gap-1.5 text-xs text-club-red/70 border border-club-red/20 px-3 py-1.5 rounded font-mono">
                <Download className="w-3.5 h-3.5" />
                Descàrrega disponible
              </div>
            )}
            {event.allow_member_uploads && user && (
              <Link
                href={`/upload?event=${event.id}`}
                className="btn-primary text-sm py-1.5"
              >
                <Upload className="w-3.5 h-3.5" />
                Afegir fotos
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Photo grid */}
      <PhotoGrid
        photos={processedPhotos}
        supabaseUrl={supabaseUrl}
        allowDownloads={event.allow_downloads}
        currentUserId={user?.id}
        currentUserRole={userProfile?.role}
      />

      {/* Upload CTA for non-logged users */}
      {!user && event.allow_member_uploads && (
        <div className="mt-12 text-center border border-white/5 rounded-lg p-8 bg-club-gray-1/30">
          <Users className="w-8 h-8 text-white/20 mx-auto mb-3" />
          <p className="text-white/50 font-body mb-4">
            Ets membre del club? Entra per pujar les teves fotos d&apos;aquest event.
          </p>
          <Link
            href={`/login?redirectTo=/events/${event.id}`}
            className="btn-primary"
          >
            Entrar al club
          </Link>
        </div>
      )}
    </div>
  )
}
