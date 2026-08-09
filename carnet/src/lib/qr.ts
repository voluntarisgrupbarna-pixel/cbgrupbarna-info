import QRCode from 'qrcode'

/** Genera un QR com a data URL PNG (per incrustar directament en una <img>). */
export async function qrDataUrl(text: string): Promise<string> {
  return QRCode.toDataURL(text, {
    errorCorrectionLevel: 'M',
    margin: 1,
    width: 480,
    color: { dark: '#0A0A0A', light: '#FFFFFF' },
  })
}
