#!/usr/bin/env node
/**
 * Import Flickr album → Supabase Gallery
 * Usage: node scripts/import-flickr.mjs
 *
 * Requires in .env.local:
 *   NEXT_PUBLIC_SUPABASE_URL=...
 *   SUPABASE_SERVICE_ROLE_KEY=...
 *   FLICKR_API_KEY=...   (free at https://www.flickr.com/services/apps/create/)
 */

import { createClient } from '@supabase/supabase-js'
import { readFileSync, existsSync } from 'fs'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dir = dirname(fileURLToPath(import.meta.url))

// ─── Config ──────────────────────────────────────────────────────────────────

const FLICKR_ALBUM_URL = 'https://flic.kr/s/aHBqjCk4bA'
const EVENT_TITLE      = 'Campus Time Chamber 2025'
const EVENT_DATE       = '2025-07-01'          // adjust to real date
const EVENT_LOCATION   = 'Barcelona'
const SEASON_NAME      = '2024-2025'
const PHOTO_SIZE       = 'b'                   // b = large 1024px, o = original

// ─── Load env ────────────────────────────────────────────────────────────────

function loadEnv() {
  const envPath = resolve(__dir, '../.env.local')
  if (!existsSync(envPath)) {
    console.error('❌  No .env.local found in galeria/. Copy .env.local.example and fill values.')
    process.exit(1)
  }
  for (const line of readFileSync(envPath, 'utf8').split('\n')) {
    const [k, ...rest] = line.split('=')
    if (k && !k.startsWith('#')) process.env[k.trim()] = rest.join('=').trim()
  }
}

loadEnv()

const SUPABASE_URL  = process.env.NEXT_PUBLIC_SUPABASE_URL
const SERVICE_KEY   = process.env.SUPABASE_SERVICE_ROLE_KEY
const FLICKR_KEY    = process.env.FLICKR_API_KEY

if (!SUPABASE_URL || !SERVICE_KEY) {
  console.error('❌  NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env.local')
  process.exit(1)
}
if (!FLICKR_KEY) {
  console.error('❌  FLICKR_API_KEY not set in .env.local')
  console.error('   Get a free key at: https://www.flickr.com/services/apps/create/')
  process.exit(1)
}

const supabase = createClient(SUPABASE_URL, SERVICE_KEY)

// ─── Helpers ─────────────────────────────────────────────────────────────────

function flickrBase58Decode(str) {
  const alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
  let n = 0n
  for (const c of str) {
    const idx = alphabet.indexOf(c)
    if (idx === -1) throw new Error(`Invalid base58 char: ${c}`)
    n = n * 58n + BigInt(idx)
  }
  return n.toString()
}

function flickrApi(method, params = {}) {
  const url = new URL('https://api.flickr.com/services/rest/')
  url.searchParams.set('method', method)
  url.searchParams.set('api_key', FLICKR_KEY)
  url.searchParams.set('format', 'json')
  url.searchParams.set('nojsoncallback', '1')
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v)
  return fetch(url.toString()).then(r => r.json())
}

async function getPhotosetId(shortUrl) {
  // Try to decode base58 directly from the short URL path
  const match = shortUrl.match(/flic\.kr\/s\/([A-Za-z0-9]+)/)
  if (match) {
    try {
      return flickrBase58Decode(match[1])
    } catch {}
  }
  // Fallback: resolve via Flickr API
  const data = await flickrApi('flickr.urls.lookupGroup', { url: shortUrl })
  if (data.stat === 'fail') throw new Error(`Flickr error: ${data.message}`)
  return data.group?.id
}

async function getAllPhotos(photosetId, ownerId) {
  const photos = []
  let page = 1
  while (true) {
    const data = await flickrApi('flickr.photosets.getPhotos', {
      photoset_id: photosetId,
      user_id: ownerId,
      extras: 'url_b,url_o,url_l,title,description,original_format',
      per_page: 500,
      page,
    })
    if (data.stat === 'fail') throw new Error(`Flickr error: ${data.message}`)
    const { photo, pages } = data.photoset
    photos.push(...photo)
    if (page >= pages) break
    page++
  }
  return photos
}

async function getPhotosetInfo(photosetId, ownerId) {
  const data = await flickrApi('flickr.photosets.getInfo', {
    photoset_id: photosetId,
    user_id: ownerId,
  })
  if (data.stat === 'fail') throw new Error(`Flickr error: ${data.message}`)
  return data.photoset
}

async function getPhotosetOwner(photosetId) {
  // Try photosets.getInfo without owner (works for public sets)
  const data = await flickrApi('flickr.photosets.getInfo', { photoset_id: photosetId })
  if (data.stat === 'ok') return data.photoset.owner
  throw new Error(`Cannot find photoset owner: ${data.message}`)
}

async function downloadPhoto(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${url}`)
  return Buffer.from(await res.arrayBuffer())
}

function mimeFromUrl(url) {
  const ext = url.split('.').pop()?.toLowerCase().split('?')[0]
  const map = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', gif: 'image/gif', webp: 'image/webp' }
  return map[ext] ?? 'image/jpeg'
}

// ─── Supabase helpers ─────────────────────────────────────────────────────────

async function getOrCreateSeason(name) {
  const { data } = await supabase.from('seasons').select('id').eq('name', name).single()
  if (data) return data.id
  const { data: inserted, error } = await supabase
    .from('seasons')
    .insert({ name, is_active: true })
    .select('id')
    .single()
  if (error) throw error
  return inserted.id
}

async function getOrCreateEvent(seasonId) {
  const { data } = await supabase.from('events').select('id').eq('title', EVENT_TITLE).single()
  if (data) return data.id
  const { data: inserted, error } = await supabase
    .from('events')
    .insert({
      season_id: seasonId,
      title: EVENT_TITLE,
      description: 'Campus de bàsquet Time Chamber. Entrenaments intensius, millora individual i molta diversió.',
      event_date: EVENT_DATE,
      location: EVENT_LOCATION,
      allow_downloads: true,
      allow_member_uploads: false,
      is_published: true,
    })
    .select('id')
    .single()
  if (error) throw error
  console.log(`✅  Event created: ${EVENT_TITLE} (id=${inserted.id})`)
  return inserted.id
}

async function uploadToSupabase(buffer, storagePath, mime) {
  const { error } = await supabase.storage
    .from('photos')
    .upload(storagePath, buffer, { contentType: mime, upsert: true })
  if (error) throw error
}

async function insertPhotoRecord(eventId, storagePath, originalName, caption) {
  const { error } = await supabase.from('photos').insert({
    event_id: eventId,
    storage_path: storagePath,
    original_name: originalName,
    caption,
    is_approved: true,
  })
  if (error) throw error
}

async function setEventCover(eventId, firstStoragePath) {
  const { data: photo } = await supabase
    .from('photos')
    .select('id')
    .eq('event_id', eventId)
    .order('uploaded_at', { ascending: true })
    .limit(1)
    .single()
  if (!photo) return
  await supabase.from('events').update({ cover_photo_id: photo.id }).eq('id', eventId)
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('🏀  CB Grup Barna — Flickr → Galeria Supabase')
  console.log(`📁  Àlbum: ${FLICKR_ALBUM_URL}`)
  console.log(`🎪  Esdeveniment: ${EVENT_TITLE}\n`)

  // 1. Resolve photoset ID
  const photosetId = await getPhotosetId(FLICKR_ALBUM_URL)
  console.log(`📸  Photoset ID: ${photosetId}`)

  // 2. Get owner
  const ownerId = await getPhotosetOwner(photosetId)
  console.log(`👤  Owner: ${ownerId}`)

  // 3. Get all photos
  const photos = await getAllPhotos(photosetId, ownerId)
  console.log(`🖼️   ${photos.length} fotos trobades\n`)

  // 4. Ensure season + event exist in Supabase
  const seasonId = await getOrCreateSeason(SEASON_NAME)
  const eventId  = await getOrCreateEvent(seasonId)

  // 5. Upload each photo
  let ok = 0, fail = 0
  for (const photo of photos) {
    const photoUrl = photo.url_b || photo.url_l || photo.url_o
    if (!photoUrl) {
      console.warn(`  ⚠️  No URL for photo ${photo.id}, skipping`)
      fail++
      continue
    }

    const ext          = photoUrl.split('.').pop()?.split('?')[0] ?? 'jpg'
    const fileName     = `${photo.id}.${ext}`
    const storagePath  = `campus-time-chamber-2025/${fileName}`
    const caption      = photo.title || null

    try {
      process.stdout.write(`  ⬇️  ${fileName} ... `)
      const buffer = await downloadPhoto(photoUrl)
      await uploadToSupabase(buffer, storagePath, mimeFromUrl(photoUrl))
      await insertPhotoRecord(eventId, storagePath, fileName, caption)
      console.log('✅')
      ok++
    } catch (err) {
      console.log(`❌  ${err.message}`)
      fail++
    }
  }

  // 6. Set first photo as cover
  await setEventCover(eventId)

  console.log(`\n🎉  Import complet: ${ok} fotos pujades, ${fail} errors`)
  console.log(`🔗  Galeria: ${SUPABASE_URL?.replace('supabase.co', 'supabase.co')}/storage/v1/`)
}

main().catch(err => {
  console.error('💥  Error fatal:', err.message)
  process.exit(1)
})
