import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { AdminClient } from './AdminClient'
import type { TopPhotoItem, RecentUploadItem } from './AdminClient'

export default async function AdminPage() {
  const supabase = await createClient()
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login?redirectTo=/admin')

  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single()

  if (!profile || !['admin', 'editor'].includes(profile.role)) {
    redirect('/?error=unauthorized')
  }

  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()

  const [
    { data: seasons },
    { data: events },
    { data: members },
    { count: totalPhotos },
    { data: rawTopPhotos },
    { data: rawRecentUploads },
    { count: photosThisWeek },
    { count: pendingApproval },
    { data: allLikes },
  ] = await Promise.all([
    supabase.from('seasons').select('*').order('name', { ascending: false }),
    supabase
      .from('events')
      .select('*, season:seasons(*), photos_count:photos(count)')
      .order('event_date', { ascending: false }),
    supabase.from('profiles').select('*').order('created_at', { ascending: false }),
    supabase.from('photos').select('*', { count: 'exact', head: true }).eq('is_approved', true),
    supabase
      .from('photos')
      .select('id, likes_count, caption, storage_path, thumbnail_path, event:events(id, title)')
      .eq('is_approved', true)
      .order('likes_count', { ascending: false })
      .limit(6),
    supabase
      .from('photos')
      .select('id, original_name, uploaded_at, storage_path, thumbnail_path, event:events(id, title), uploader:profiles(full_name)')
      .eq('is_approved', true)
      .order('uploaded_at', { ascending: false })
      .limit(8),
    supabase
      .from('photos')
      .select('*', { count: 'exact', head: true })
      .eq('is_approved', true)
      .gte('uploaded_at', sevenDaysAgo),
    supabase
      .from('photos')
      .select('*', { count: 'exact', head: true })
      .eq('is_approved', false),
    supabase
      .from('photos')
      .select('likes_count')
      .eq('is_approved', true),
  ])

  const processedEvents = (events ?? []).map(e => ({
    ...e,
    photos_count: Array.isArray(e.photos_count) ? e.photos_count[0]?.count ?? 0 : 0,
  }))

  const totalLikes = (allLikes ?? []).reduce((s, p) => s + (p.likes_count || 0), 0)

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const resolve = (v: any) => (Array.isArray(v) ? v[0] : v)

  const topPhotos: TopPhotoItem[] = (rawTopPhotos ?? []).flatMap(raw => {
    const ev = resolve(raw.event)
    if (!ev) return []
    return [{ id: raw.id, likes_count: raw.likes_count, caption: raw.caption ?? null, storage_path: raw.storage_path, thumbnail_path: raw.thumbnail_path ?? null, event_title: ev.title, event_id: ev.id }]
  })

  const recentUploads: RecentUploadItem[] = (rawRecentUploads ?? []).flatMap(raw => {
    const ev = resolve(raw.event)
    const up = resolve(raw.uploader)
    if (!ev) return []
    return [{ id: raw.id, original_name: raw.original_name ?? null, uploaded_at: raw.uploaded_at, storage_path: raw.storage_path, thumbnail_path: raw.thumbnail_path ?? null, event_title: ev.title, event_id: ev.id, uploader_name: up?.full_name ?? null }]
  })

  return (
    <AdminClient
      profile={profile}
      seasons={seasons ?? []}
      events={processedEvents}
      members={members ?? []}
      totalPhotos={totalPhotos ?? 0}
      dashboard={{
        photosThisWeek: photosThisWeek ?? 0,
        totalLikes,
        pendingApproval: pendingApproval ?? 0,
        topPhotos,
        recentUploads,
        supabaseUrl,
      }}
    />
  )
}
