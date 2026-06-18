'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import {
  Calendar, Users, Images, Plus, Trash2, Eye, EyeOff,
  Loader2, CheckCircle, Heart, Camera, Clock, TrendingUp,
  BarChart2, Upload,
} from 'lucide-react'
import type { Event, Season, Profile } from '@/lib/types'

// ── Exported types used by page.tsx ──────────────────────────────────────────

export interface TopPhotoItem {
  id: number
  likes_count: number
  caption: string | null
  storage_path: string
  thumbnail_path: string | null
  event_title: string
  event_id: number
}

export interface RecentUploadItem {
  id: number
  original_name: string | null
  uploaded_at: string
  storage_path: string
  thumbnail_path: string | null
  event_title: string
  event_id: number
  uploader_name: string | null
}

export interface DashboardData {
  photosThisWeek: number
  totalLikes: number
  pendingApproval: number
  topPhotos: TopPhotoItem[]
  recentUploads: RecentUploadItem[]
  supabaseUrl: string
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 60) return `fa ${m}min`
  const h = Math.floor(m / 60)
  if (h < 24) return `fa ${h}h`
  return `fa ${Math.floor(h / 24)}d`
}

function thumbUrl(supabaseUrl: string, path: string | null, fallback: string) {
  return `${supabaseUrl}/storage/v1/object/public/photos/${path ?? fallback}`
}

// ── Sub-components ────────────────────────────────────────────────────────────

function KpiCard({
  label, value, icon: Icon, accent = false, alert = false,
}: {
  label: string; value: number; icon: React.ElementType; accent?: boolean; alert?: boolean
}) {
  return (
    <div className={`rounded-lg border p-4 ${alert && value > 0 ? 'border-amber-500/40 bg-amber-500/5' : accent ? 'border-club-red/30 bg-club-red/5' : 'border-white/5 bg-club-gray-1'}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="font-mono text-xs text-white/30 uppercase tracking-wider">{label}</span>
        <Icon className={`w-4 h-4 ${alert && value > 0 ? 'text-amber-400' : accent ? 'text-club-red/70' : 'text-white/20'}`} />
      </div>
      <div className={`font-display text-3xl ${alert && value > 0 ? 'text-amber-400' : accent ? 'text-club-red' : 'text-club-cream'}`}>
        {value.toLocaleString('ca-ES')}
      </div>
    </div>
  )
}

function TopPhotosGrid({ photos, supabaseUrl }: { photos: TopPhotoItem[]; supabaseUrl: string }) {
  if (photos.length === 0) {
    return <p className="text-white/20 text-sm font-body text-center py-8">Sense dades encara</p>
  }
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {photos.map((photo, i) => (
        <Link key={photo.id} href={`/events/${photo.event_id}`} className="group relative aspect-[4/3] rounded overflow-hidden block">
          <Image
            src={thumbUrl(supabaseUrl, photo.thumbnail_path, photo.storage_path)}
            alt={photo.caption ?? photo.event_title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 640px) 50vw, 33vw"
          />
          {/* rank badge */}
          <div className="absolute top-2 left-2 w-5 h-5 rounded-full bg-black/70 flex items-center justify-center font-mono text-[10px] text-white/60">
            {i + 1}
          </div>
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-2 flex items-end justify-between gap-1">
            <span className="font-mono text-[10px] text-white/50 truncate leading-tight">{photo.event_title}</span>
            <span className="flex items-center gap-0.5 font-mono text-xs text-club-red shrink-0">
              <Heart className="w-3 h-3 fill-current" />
              {photo.likes_count}
            </span>
          </div>
        </Link>
      ))}
    </div>
  )
}

function RecentUploadsList({ uploads, supabaseUrl }: { uploads: RecentUploadItem[]; supabaseUrl: string }) {
  if (uploads.length === 0) {
    return <p className="text-white/20 text-sm font-body text-center py-8">Sense pujades recents</p>
  }
  return (
    <div className="space-y-2">
      {uploads.map(upload => (
        <Link
          key={upload.id}
          href={`/events/${upload.event_id}`}
          className="flex items-center gap-3 p-2 rounded hover:bg-white/5 transition-colors group"
        >
          <div className="relative w-10 h-10 rounded overflow-hidden shrink-0 bg-club-gray-2">
            <Image
              src={thumbUrl(supabaseUrl, upload.thumbnail_path, upload.storage_path)}
              alt={upload.original_name ?? 'foto'}
              fill
              className="object-cover"
              sizes="40px"
            />
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-body text-xs text-club-cream/80 truncate group-hover:text-white transition-colors">
              {upload.original_name ?? 'foto'}
            </div>
            <div className="font-mono text-[10px] text-white/30 truncate">{upload.event_title}</div>
          </div>
          <div className="text-right shrink-0">
            {upload.uploader_name && (
              <div className="font-mono text-[10px] text-white/30 truncate max-w-[80px]">{upload.uploader_name}</div>
            )}
            <div className="font-mono text-[10px] text-white/20">{timeAgo(upload.uploaded_at)}</div>
          </div>
        </Link>
      ))}
    </div>
  )
}

function TopEventsChart({ events }: { events: { id: number; title: string; photos_count: number }[] }) {
  const sorted = [...events].sort((a, b) => b.photos_count - a.photos_count).slice(0, 6)
  const max = sorted[0]?.photos_count || 1
  if (sorted.length === 0) {
    return <p className="text-white/20 text-sm font-body text-center py-8">Sense events</p>
  }
  return (
    <div className="space-y-3">
      {sorted.map(ev => (
        <Link key={ev.id} href={`/events/${ev.id}`} className="group block">
          <div className="flex items-center justify-between mb-1">
            <span className="font-body text-xs text-white/60 group-hover:text-white/90 transition-colors truncate pr-2">{ev.title}</span>
            <span className="font-mono text-xs text-white/30 shrink-0">{ev.photos_count}</span>
          </div>
          <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
            <div
              className="h-full bg-club-red/60 rounded-full transition-all duration-500 group-hover:bg-club-red"
              style={{ width: `${Math.round((ev.photos_count / max) * 100)}%` }}
            />
          </div>
        </Link>
      ))}
    </div>
  )
}

// ── Main component ─────────────────────────────────────────────────────────────

interface AdminClientProps {
  profile: Profile
  seasons: Season[]
  events: (Event & { photos_count: number })[]
  members: Profile[]
  totalPhotos: number
  dashboard: DashboardData
}

export function AdminClient({ profile, seasons: initialSeasons, events: initialEvents, members: initialMembers, totalPhotos, dashboard }: AdminClientProps) {
  const router = useRouter()
  const supabase = createClient()
  const [activeTab, setActiveTab] = useState<'dashboard' | 'events' | 'seasons' | 'members'>('dashboard')

  // New event form
  const [showNewEvent, setShowNewEvent] = useState(false)
  const [newEvent, setNewEvent] = useState({
    title: '',
    description: '',
    event_date: '',
    location: '',
    season_id: '',
    allow_downloads: true,
    allow_member_uploads: true,
  })
  const [savingEvent, setSavingEvent] = useState(false)
  const [savedEvent, setSavedEvent] = useState(false)

  // New season form
  const [showNewSeason, setShowNewSeason] = useState(false)
  const [newSeasonName, setNewSeasonName] = useState('')
  const [savingSeason, setSavingSeason] = useState(false)

  const [seasons, setSeasons] = useState<Season[]>(initialSeasons)
  const [events, setEvents] = useState(initialEvents)
  const [members, setMembers] = useState<Profile[]>(initialMembers)

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault()
    setSavingEvent(true)
    const { data, error } = await supabase.from('events').insert({
      title: newEvent.title,
      description: newEvent.description || null,
      event_date: newEvent.event_date || null,
      location: newEvent.location || null,
      season_id: newEvent.season_id ? parseInt(newEvent.season_id) : null,
      allow_downloads: newEvent.allow_downloads,
      allow_member_uploads: newEvent.allow_member_uploads,
      created_by: profile.id,
      is_published: true,
    }).select('*, season:seasons(*)').single()
    if (!error && data) {
      setEvents(prev => [{ ...data, photos_count: 0 }, ...prev])
      setNewEvent({ title: '', description: '', event_date: '', location: '', season_id: '', allow_downloads: true, allow_member_uploads: true })
      setShowNewEvent(false)
      setSavedEvent(true)
      setTimeout(() => setSavedEvent(false), 3000)
    }
    setSavingEvent(false)
  }

  const handleTogglePublish = async (eventId: number, current: boolean) => {
    await supabase.from('events').update({ is_published: !current }).eq('id', eventId)
    setEvents(prev => prev.map(e => e.id === eventId ? { ...e, is_published: !current } : e))
  }

  const handleDeleteEvent = async (eventId: number) => {
    if (!confirm('Segur que vols eliminar aquest event i totes les seves fotos?')) return
    await supabase.from('events').delete().eq('id', eventId)
    setEvents(prev => prev.filter(e => e.id !== eventId))
  }

  const handleCreateSeason = async (e: React.FormEvent) => {
    e.preventDefault()
    setSavingSeason(true)
    const { data } = await supabase.from('seasons').insert({ name: newSeasonName }).select().single()
    if (data) {
      setSeasons(prev => [data, ...prev])
      setNewSeasonName('')
      setShowNewSeason(false)
    }
    setSavingSeason(false)
  }

  const handleUpdateMemberRole = async (memberId: string, newRole: string) => {
    await supabase.from('profiles').update({ role: newRole }).eq('id', memberId)
    setMembers(prev => prev.map(m => m.id === memberId ? { ...m, role: newRole as Profile['role'] } : m))
  }

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
    { id: 'events',    label: 'Esdeveniments', icon: Calendar, count: events.length },
    { id: 'seasons',   label: 'Temporades',    icon: Images,   count: seasons.length },
    { id: 'members',   label: 'Membres',       icon: Users,    count: members.length },
  ] as const

  return (
    <div className="max-w-6xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="section-title mb-1">
            <span className="text-club-red">Administrar</span> Galeria
          </h1>
          <p className="text-white/30 font-mono text-xs">
            {profile.full_name ?? profile.id} · {profile.role}
          </p>
        </div>
        <div className="flex gap-4 text-center">
          {[
            { label: 'Fotos', value: totalPhotos },
            { label: 'Events', value: events.length },
            { label: 'Membres', value: members.length },
          ].map(({ label, value }) => (
            <div key={label} className="border border-white/10 rounded px-4 py-2">
              <div className="font-display text-2xl text-club-cream">{value}</div>
              <div className="font-mono text-xs text-white/30">{label}</div>
            </div>
          ))}
        </div>
      </div>

      {savedEvent && (
        <div className="flex items-center gap-2 bg-green-900/30 border border-green-500/30 text-green-400 p-3 rounded-lg mb-4 text-sm">
          <CheckCircle className="w-4 h-4" />
          Esdeveniment creat correctament!
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-white/10 mb-6 gap-1 overflow-x-auto">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 text-sm font-body border-b-2 transition-colors whitespace-nowrap ${
              activeTab === tab.id
                ? 'border-club-red text-club-cream'
                : 'border-transparent text-white/40 hover:text-white/70'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
            {'count' in tab && (
              <span className="font-mono text-xs bg-white/10 px-1.5 py-0.5 rounded">{tab.count}</span>
            )}
          </button>
        ))}
      </div>

      {/* ── DASHBOARD TAB ─────────────────────────────────────────────── */}
      {activeTab === 'dashboard' && (
        <div className="space-y-8">

          {/* KPIs */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <KpiCard label="Fotos 7 dies"       value={dashboard.photosThisWeek}   icon={Camera}    accent />
            <KpiCard label="Likes totals"        value={dashboard.totalLikes}       icon={Heart} />
            <KpiCard label="Pendent aprovació"   value={dashboard.pendingApproval}  icon={Clock}     alert />
            <KpiCard label="Total fotos"         value={totalPhotos}                icon={Images} />
          </div>

          {/* Top fotos + últimes pujades */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Top fotos per likes */}
            <div className="bg-club-gray-1 border border-white/5 rounded-lg p-5">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-4 h-4 text-club-red/60" />
                <h2 className="font-heading text-sm font-semibold text-club-cream">Top fotos per likes</h2>
              </div>
              <TopPhotosGrid photos={dashboard.topPhotos} supabaseUrl={dashboard.supabaseUrl} />
            </div>

            {/* Últimes pujades */}
            <div className="bg-club-gray-1 border border-white/5 rounded-lg p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <Upload className="w-4 h-4 text-white/30" />
                  <h2 className="font-heading text-sm font-semibold text-club-cream">Últimes pujades</h2>
                </div>
                <Link href="/upload" className="font-mono text-xs text-white/30 hover:text-white/60 transition-colors">
                  Pujar →
                </Link>
              </div>
              <RecentUploadsList uploads={dashboard.recentUploads} supabaseUrl={dashboard.supabaseUrl} />
            </div>
          </div>

          {/* Top events chart */}
          <div className="bg-club-gray-1 border border-white/5 rounded-lg p-5">
            <div className="flex items-center gap-2 mb-5">
              <BarChart2 className="w-4 h-4 text-white/30" />
              <h2 className="font-heading text-sm font-semibold text-club-cream">Events per volum de fotos</h2>
            </div>
            <TopEventsChart events={events} />
          </div>

          {/* Pending approval alert */}
          {dashboard.pendingApproval > 0 && (
            <div className="flex items-center gap-3 p-4 bg-amber-500/5 border border-amber-500/20 rounded-lg">
              <Clock className="w-5 h-5 text-amber-400 shrink-0" />
              <div className="flex-1">
                <p className="text-sm font-body text-amber-300">
                  Hi ha <strong>{dashboard.pendingApproval} fotos</strong> pendents d&apos;aprovació.
                </p>
              </div>
              <button
                onClick={() => setActiveTab('events')}
                className="font-mono text-xs text-amber-400 border border-amber-400/30 px-3 py-1.5 rounded hover:bg-amber-400/10 transition-colors shrink-0"
              >
                Veure events →
              </button>
            </div>
          )}
        </div>
      )}

      {/* ── EVENTS TAB ────────────────────────────────────────────────── */}
      {activeTab === 'events' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <p className="text-white/40 text-sm font-body">{events.length} esdeveniments</p>
            <button onClick={() => setShowNewEvent(!showNewEvent)} className="btn-primary text-sm py-1.5">
              <Plus className="w-3.5 h-3.5" />
              Nou event
            </button>
          </div>

          {showNewEvent && (
            <form onSubmit={handleCreateEvent} className="bg-club-gray-1 border border-white/10 rounded-lg p-6 space-y-4">
              <h3 className="font-heading text-lg text-club-cream font-semibold">Nou Esdeveniment</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="sm:col-span-2">
                  <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Títol *</label>
                  <input type="text" value={newEvent.title} onChange={e => setNewEvent(p => ({ ...p, title: e.target.value }))} required placeholder="Ex: Torneig 3x3 Glòries 2025" className="input" />
                </div>
                <div className="sm:col-span-2">
                  <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Descripció</label>
                  <textarea value={newEvent.description} onChange={e => setNewEvent(p => ({ ...p, description: e.target.value }))} placeholder="Descripció de l'event..." rows={2} className="input resize-none" />
                </div>
                <div>
                  <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Data</label>
                  <input type="date" value={newEvent.event_date} onChange={e => setNewEvent(p => ({ ...p, event_date: e.target.value }))} className="input" />
                </div>
                <div>
                  <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Lloc</label>
                  <input type="text" value={newEvent.location} onChange={e => setNewEvent(p => ({ ...p, location: e.target.value }))} placeholder="Ex: Parc de les Glòries" className="input" />
                </div>
                <div>
                  <label className="block text-xs text-white/40 mb-1 font-mono uppercase tracking-wider">Temporada</label>
                  <select value={newEvent.season_id} onChange={e => setNewEvent(p => ({ ...p, season_id: e.target.value }))} className="input">
                    <option value="">Sense temporada</option>
                    {seasons.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>
                <div className="flex items-center gap-6">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" checked={newEvent.allow_downloads} onChange={e => setNewEvent(p => ({ ...p, allow_downloads: e.target.checked }))} className="accent-club-red w-4 h-4" />
                    <span className="text-sm text-white/60 font-body">Permetre descàrregues</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input type="checkbox" checked={newEvent.allow_member_uploads} onChange={e => setNewEvent(p => ({ ...p, allow_member_uploads: e.target.checked }))} className="accent-club-red w-4 h-4" />
                    <span className="text-sm text-white/60 font-body">Membres poden pujar</span>
                  </label>
                </div>
              </div>
              <div className="flex gap-2 pt-2">
                <button type="submit" disabled={savingEvent} className="btn-primary">
                  {savingEvent ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
                  Crear event
                </button>
                <button type="button" onClick={() => setShowNewEvent(false)} className="btn-ghost">Cancel·lar</button>
              </div>
            </form>
          )}

          <div className="space-y-2">
            {events.map(event => (
              <div key={event.id} className={`flex items-center gap-4 p-4 rounded-lg border transition-colors ${event.is_published ? 'bg-club-gray-1 border-white/5' : 'bg-club-gray-2/50 border-white/5 opacity-60'}`}>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-heading text-club-cream font-semibold truncate">{event.title}</span>
                    {event.season && <span className="tag shrink-0">{event.season.name}</span>}
                    {!event.is_published && <span className="font-mono text-xs text-white/30 border border-white/10 px-1.5 py-0.5 rounded">ocult</span>}
                  </div>
                  <div className="flex gap-3 mt-1 text-xs text-white/30 font-mono">
                    {event.event_date && <span>{new Date(event.event_date).toLocaleDateString('ca-ES')}</span>}
                    <span>{event.photos_count} fotos</span>
                    {event.allow_downloads && <span className="text-club-red/40">descàrrega ✓</span>}
                  </div>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  <button onClick={() => router.push(`/events/${event.id}`)} className="p-1.5 text-white/30 hover:text-white/70 transition-colors" title="Veure event">
                    <Eye className="w-4 h-4" />
                  </button>
                  <button onClick={() => handleTogglePublish(event.id, event.is_published)} className="p-1.5 text-white/30 hover:text-white/70 transition-colors" title={event.is_published ? 'Ocultar' : 'Publicar'}>
                    {event.is_published ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                  </button>
                  {profile.role === 'admin' && (
                    <button onClick={() => handleDeleteEvent(event.id)} className="p-1.5 text-white/30 hover:text-red-400 transition-colors" title="Eliminar">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── SEASONS TAB ───────────────────────────────────────────────── */}
      {activeTab === 'seasons' && (
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <p className="text-white/40 text-sm font-body">{seasons.length} temporades</p>
            <button onClick={() => setShowNewSeason(!showNewSeason)} className="btn-primary text-sm py-1.5">
              <Plus className="w-3.5 h-3.5" />
              Nova temporada
            </button>
          </div>
          {showNewSeason && (
            <form onSubmit={handleCreateSeason} className="bg-club-gray-1 border border-white/10 rounded-lg p-4 flex gap-3">
              <input type="text" value={newSeasonName} onChange={e => setNewSeasonName(e.target.value)} placeholder="Ex: 2025-2026" required className="input flex-1" />
              <button type="submit" disabled={savingSeason} className="btn-primary">
                {savingSeason ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Crear'}
              </button>
            </form>
          )}
          <div className="space-y-2">
            {seasons.map(season => (
              <div key={season.id} className="flex items-center justify-between p-4 bg-club-gray-1 border border-white/5 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="font-heading text-club-cream font-semibold">{season.name}</span>
                  {season.is_active && (
                    <span className="inline-flex items-center gap-1 font-mono text-xs text-green-400 border border-green-400/30 px-2 py-0.5 rounded">
                      <span className="w-1.5 h-1.5 bg-green-400 rounded-full" />
                      Activa
                    </span>
                  )}
                </div>
                <span className="text-white/30 font-mono text-xs">{events.filter(e => e.season_id === season.id).length} events</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── MEMBERS TAB ───────────────────────────────────────────────── */}
      {activeTab === 'members' && (
        <div className="space-y-4">
          <p className="text-white/40 text-sm font-body">{members.length} membres registrats</p>
          <div className="space-y-2">
            {members.map(member => (
              <div key={member.id} className="flex items-center justify-between p-4 bg-club-gray-1 border border-white/5 rounded-lg">
                <div>
                  <div className="font-body text-club-cream">{member.full_name ?? 'Sense nom'}</div>
                  <div className="font-mono text-xs text-white/30 mt-0.5">{member.id.slice(0, 8)}...</div>
                </div>
                {profile.role === 'admin' ? (
                  <select value={member.role} onChange={e => handleUpdateMemberRole(member.id, e.target.value)} className="bg-club-gray-2 border border-white/10 text-white/60 text-xs font-mono px-2 py-1.5 rounded focus:outline-none focus:border-club-red">
                    <option value="viewer">viewer</option>
                    <option value="contributor">contributor</option>
                    <option value="editor">editor</option>
                    <option value="admin">admin</option>
                  </select>
                ) : (
                  <span className="tag">{member.role}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
