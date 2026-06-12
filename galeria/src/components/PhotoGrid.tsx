'use client'

import Image from 'next/image'
import { useState } from 'react'
import Lightbox from 'yet-another-react-lightbox'
import 'yet-another-react-lightbox/styles.css'
import Download from 'yet-another-react-lightbox/plugins/download'
import Captions from 'yet-another-react-lightbox/plugins/captions'
import 'yet-another-react-lightbox/plugins/captions.css'
import Counter from 'yet-another-react-lightbox/plugins/counter'
import 'yet-another-react-lightbox/plugins/counter.css'
import { Heart, MessageCircle, Download as DownloadIcon, Trash2 } from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import type { Photo } from '@/lib/types'

interface PhotoGridProps {
  photos: Photo[]
  supabaseUrl: string
  allowDownloads: boolean
  currentUserId?: string
  currentUserRole?: string
  onPhotoDeleted?: (photoId: number) => void
}

export function PhotoGrid({
  photos,
  supabaseUrl,
  allowDownloads,
  currentUserId,
  currentUserRole,
  onPhotoDeleted,
}: PhotoGridProps) {
  const [lightboxIndex, setLightboxIndex] = useState(-1)
  const [likedPhotos, setLikedPhotos] = useState<Set<number>>(
    new Set(photos.filter(p => p.liked_by_user).map(p => p.id))
  )
  const [likeCounts, setLikeCounts] = useState<Record<number, number>>(
    Object.fromEntries(photos.map(p => [p.id, p.likes_count]))
  )
  const supabase = createClient()

  const slides = photos.map(photo => ({
    src: `${supabaseUrl}/storage/v1/object/public/photos/${photo.storage_path}`,
    alt: photo.caption ?? photo.original_name ?? 'Foto',
    description: photo.caption ?? undefined,
    download: allowDownloads
      ? `${supabaseUrl}/storage/v1/object/public/photos/${photo.storage_path}`
      : undefined,
    width: photo.width ?? undefined,
    height: photo.height ?? undefined,
  }))

  const handleLike = async (e: React.MouseEvent, photoId: number) => {
    e.stopPropagation()
    if (!currentUserId) return

    const isLiked = likedPhotos.has(photoId)

    if (isLiked) {
      setLikedPhotos(prev => { const s = new Set(prev); s.delete(photoId); return s })
      setLikeCounts(prev => ({ ...prev, [photoId]: (prev[photoId] ?? 1) - 1 }))
      await supabase.from('photo_likes').delete()
        .eq('photo_id', photoId).eq('user_id', currentUserId)
    } else {
      setLikedPhotos(prev => new Set(prev).add(photoId))
      setLikeCounts(prev => ({ ...prev, [photoId]: (prev[photoId] ?? 0) + 1 }))
      await supabase.from('photo_likes').insert({ photo_id: photoId, user_id: currentUserId })
    }
  }

  const handleDelete = async (e: React.MouseEvent, photoId: number) => {
    e.stopPropagation()
    if (!confirm('Segur que vols eliminar aquesta foto?')) return

    const photo = photos.find(p => p.id === photoId)
    if (!photo) return

    await supabase.storage.from('photos').remove([photo.storage_path])
    if (photo.thumbnail_path) {
      await supabase.storage.from('photos').remove([photo.thumbnail_path])
    }
    await supabase.from('photos').delete().eq('id', photoId)
    onPhotoDeleted?.(photoId)
  }

  const canDelete = (photo: Photo) =>
    currentUserRole === 'admin' ||
    currentUserRole === 'editor' ||
    photo.uploaded_by === currentUserId

  if (photos.length === 0) {
    return (
      <div className="text-center py-24">
        <p className="text-white/30 font-body">Encara no hi ha fotos en aquest esdeveniment.</p>
      </div>
    )
  }

  return (
    <>
      <div className="photo-grid">
        {photos.map((photo, index) => {
          const src = `${supabaseUrl}/storage/v1/object/public/photos/${
            photo.thumbnail_path ?? photo.storage_path
          }`
          const isLiked = likedPhotos.has(photo.id)

          return (
            <div
              key={photo.id}
              className="photo-grid-item relative group cursor-pointer rounded overflow-hidden"
              onClick={() => setLightboxIndex(index)}
            >
              <Image
                src={src}
                alt={photo.caption ?? `Foto ${photo.id}`}
                width={photo.width ?? 400}
                height={photo.height ?? 300}
                className="w-full h-auto block"
                sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 25vw"
              />

              {/* Hover overlay */}
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all duration-200 flex items-end">
                <div className="w-full p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={e => handleLike(e, photo.id)}
                      className={`flex items-center gap-1 text-xs backdrop-blur-sm px-2 py-1 rounded transition-colors ${
                        isLiked
                          ? 'bg-club-red/80 text-white'
                          : 'bg-black/60 text-white/80 hover:bg-club-red/60'
                      }`}
                    >
                      <Heart className={`w-3 h-3 ${isLiked ? 'fill-current' : ''}`} />
                      {likeCounts[photo.id] ?? 0}
                    </button>

                    {allowDownloads && (
                      <a
                        href={`${supabaseUrl}/storage/v1/object/public/photos/${photo.storage_path}`}
                        download={photo.original_name ?? true}
                        onClick={e => e.stopPropagation()}
                        className="bg-black/60 text-white/80 hover:bg-white/20 backdrop-blur-sm px-2 py-1 rounded text-xs flex items-center gap-1 transition-colors"
                      >
                        <DownloadIcon className="w-3 h-3" />
                      </a>
                    )}
                  </div>

                  {canDelete(photo) && (
                    <button
                      onClick={e => handleDelete(e, photo.id)}
                      className="bg-black/60 text-red-400 hover:bg-red-900/60 backdrop-blur-sm p-1.5 rounded transition-colors"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <Lightbox
        open={lightboxIndex >= 0}
        close={() => setLightboxIndex(-1)}
        index={lightboxIndex}
        slides={slides}
        plugins={allowDownloads ? [Download, Captions, Counter] : [Captions, Counter]}
        styles={{
          container: { backgroundColor: 'rgba(4,4,4,0.97)' },
        }}
      />
    </>
  )
}
