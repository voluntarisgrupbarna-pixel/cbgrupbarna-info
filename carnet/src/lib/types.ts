export type EstatCarnet = 'pendent' | 'actiu' | 'rebutjat' | 'revocat' | 'caducat'

export interface Profile {
  id: string
  full_name: string | null
  role: 'viewer' | 'admin'
  created_at: string
}

export interface Carnet {
  id: string
  nom: string
  cognoms: string
  equip: string | null
  codi_federacio: string
  temporada: string
  foto_path: string | null
  tutor_nom: string
  tutor_email: string
  tutor_telefon: string | null
  consentiment_rgpd: boolean
  consentiment_data: string | null
  estat: EstatCarnet
  notes_admin: string | null
  data_caducitat: string | null
  aprovat_per: string | null
  aprovat_at: string | null
  qr_token: string
  access_token: string
  created_at: string
}

/** Camps mínims que es mostren a la pàgina pública de verificació (comerços). */
export interface CarnetPublic {
  nom: string
  cognoms: string
  equip: string | null
  temporada: string
  estat: EstatCarnet
  data_caducitat: string | null
  foto_url: string | null
}
