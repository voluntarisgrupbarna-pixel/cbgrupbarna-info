import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { AdminClient } from './AdminClient'

export default async function AdminPage() {
  const supabase = await createClient()
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

  const [
    { data: seasons },
    { data: events },
    { data: members },
    { count: totalPhotos },
  ] = await Promise.all([
    supabase.from('seasons').select('*').order('name', { ascending: false }),
    supabase
      .from('events')
      .select('*, season:seasons(*), photos_count:photos(count)')
      .order('event_date', { ascending: false }),
    supabase.from('profiles').select('*').order('created_at', { ascending: false }),
    supabase.from('photos').select('*', { count: 'exact', head: true }).eq('is_approved', true),
  ])

  const processedEvents = (events ?? []).map(e => ({
    ...e,
    photos_count: Array.isArray(e.photos_count) ? e.photos_count[0]?.count ?? 0 : 0,
  }))

  return (
    <AdminClient
      profile={profile}
      seasons={seasons ?? []}
      events={processedEvents}
      members={members ?? []}
      totalPhotos={totalPhotos ?? 0}
    />
  )
}
