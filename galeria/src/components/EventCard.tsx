import Link from 'next/link'
import Image from 'next/image'
import { Calendar, MapPin, Images, Download } from 'lucide-react'
import type { Event } from '@/lib/types'

interface EventCardProps {
  event: Event
  supabaseUrl: string
}

export function EventCard({ event, supabaseUrl }: EventCardProps) {
  const coverUrl = event.cover_photo
    ? `${supabaseUrl}/storage/v1/object/public/photos/${event.cover_photo.storage_path}`
    : null

  const formattedDate = event.event_date
    ? new Date(event.event_date).toLocaleDateString('ca-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
      })
    : null

  return (
    <Link href={`/events/${event.id}`} className="card group block">
      {/* Cover image */}
      <div className="aspect-[4/3] bg-club-gray-2 relative overflow-hidden">
        {coverUrl ? (
          <Image
            src={coverUrl}
            alt={event.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-500"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Images className="w-12 h-12 text-white/10" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />

        {/* Photo count badge */}
        <div className="absolute bottom-3 right-3 bg-black/60 backdrop-blur-sm text-white/80 text-xs font-mono px-2 py-1 rounded flex items-center gap-1">
          <Images className="w-3 h-3" />
          {event.photos_count ?? 0}
        </div>

        {/* Season badge */}
        {event.season && (
          <div className="absolute top-3 left-3 tag">
            {event.season.name}
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-4">
        <h3 className="font-heading text-lg font-semibold text-club-cream group-hover:text-white transition-colors line-clamp-2">
          {event.title}
        </h3>

        {event.description && (
          <p className="text-white/40 text-sm mt-1 line-clamp-2 font-body">
            {event.description}
          </p>
        )}

        <div className="mt-3 flex flex-wrap gap-3 text-xs text-white/40">
          {formattedDate && (
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {formattedDate}
            </span>
          )}
          {event.location && (
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {event.location}
            </span>
          )}
          {event.allow_downloads && (
            <span className="flex items-center gap-1 text-club-red/60">
              <Download className="w-3 h-3" />
              Descàrrega
            </span>
          )}
        </div>
      </div>
    </Link>
  )
}
