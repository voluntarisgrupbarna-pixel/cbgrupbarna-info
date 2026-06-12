export type UserRole = 'viewer' | 'contributor' | 'editor' | 'admin'

export interface Profile {
  id: string
  full_name: string | null
  role: UserRole
  avatar_url: string | null
  created_at: string
}

export interface Season {
  id: number
  name: string
  is_active: boolean
  created_at: string
}

export interface Event {
  id: number
  season_id: number | null
  title: string
  description: string | null
  event_date: string | null
  location: string | null
  cover_photo_id: number | null
  allow_downloads: boolean
  allow_member_uploads: boolean
  is_published: boolean
  created_by: string | null
  created_at: string
  // joins
  season?: Season
  photos_count?: number
  cover_photo?: Photo
}

export interface Photo {
  id: number
  event_id: number
  storage_path: string
  thumbnail_path: string | null
  original_name: string | null
  caption: string | null
  width: number | null
  height: number | null
  file_size: number | null
  uploaded_by: string | null
  uploaded_at: string
  likes_count: number
  is_approved: boolean
  // joins
  uploader?: Profile
  liked_by_user?: boolean
}

export interface Comment {
  id: number
  photo_id: number
  user_id: string | null
  content: string
  created_at: string
  // joins
  profile?: Profile
}

export interface PhotoLike {
  photo_id: number
  user_id: string
  created_at: string
}
