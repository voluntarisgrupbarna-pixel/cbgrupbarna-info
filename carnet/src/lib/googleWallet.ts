import jwt from 'jsonwebtoken'
import type { Carnet } from './types'

/**
 * Genera l'enllaç "Afegir a Google Wallet" per a un carnet.
 *
 * Gratuït: només cal un compte a Google Wallet Business Console
 * (https://pay.google.com/business/console) i un service account de Google
 * Cloud amb el rol "Wallet Object Issuer". No requereix cap pagament, a
 * diferència d'Apple Wallet (que exigeix Apple Developer Program, 99$/any).
 *
 * El pase (classe + objecte) es defineix sencer dins del JWT — no cal
 * crear-lo prèviament amb una crida a l'API REST de Google Wallet.
 */
export function buildGoogleWalletSaveUrl(
  carnet: Carnet,
  opts: { baseUrl: string; fotoUrl: string | null }
): string | null {
  const issuerId = process.env.GOOGLE_WALLET_ISSUER_ID
  const clientEmail = process.env.GOOGLE_WALLET_CLIENT_EMAIL
  const privateKey = process.env.GOOGLE_WALLET_PRIVATE_KEY?.replace(/\\n/g, '\n')

  if (!issuerId || !clientEmail || !privateKey) {
    // Encara no configurat — la pàgina de descàrrega mostra només el PDF/QR.
    return null
  }

  const classId = `${issuerId}.carnet_cbgb_v1`
  const objectId = `${issuerId}.carnet_${carnet.id.replace(/-/g, '_')}`
  const verificationUrl = `${opts.baseUrl}/verificar/${carnet.qr_token}`

  const genericClass = {
    id: classId,
    issuerName: 'CB Grup Barna',
    reviewStatus: 'UNDER_REVIEW',
  }

  const genericObject: Record<string, unknown> = {
    id: objectId,
    classId,
    state: 'ACTIVE',
    cardTitle: { defaultValue: { language: 'ca', value: 'CB GRUP BARNA' } },
    header: { defaultValue: { language: 'ca', value: `${carnet.nom} ${carnet.cognoms}` } },
    subheader: { defaultValue: { language: 'ca', value: 'Carnet de soci/a' } },
    textModulesData: [
      { id: 'equip', header: 'EQUIP', body: carnet.equip ?? '—' },
      { id: 'temporada', header: 'TEMPORADA', body: carnet.temporada },
      { id: 'codi', header: 'CODI DE JUGADOR/A', body: carnet.codi_federacio },
    ],
    barcode: {
      type: 'QR_CODE',
      value: verificationUrl,
      alternateText: carnet.qr_token.slice(0, 8).toUpperCase(),
    },
    hexBackgroundColor: '#0A0A0A',
    logo: {
      sourceUri: { uri: 'https://cbgrupbarna.info/logo.png' },
      contentDescription: { defaultValue: { language: 'ca', value: 'Logo CB Grup Barna' } },
    },
    ...(opts.fotoUrl ? { heroImage: { sourceUri: { uri: opts.fotoUrl } } } : {}),
  }

  const claims = {
    iss: clientEmail,
    aud: 'google',
    typ: 'savetowallet',
    origins: [opts.baseUrl],
    payload: {
      genericClasses: [genericClass],
      genericObjects: [genericObject],
    },
  }

  const token = jwt.sign(claims, privateKey, { algorithm: 'RS256' })
  return `https://pay.google.com/gp/v/save/${token}`
}
