/* =========================================================
   CONFIGURACIÓ DEL PANELL D'ADMINISTRACIÓ · CB Grup Barna
   =========================================================
   1) Cal crear un ID de client de Google (gratuït i de 5 minuts):
      · Entra a https://console.cloud.google.com/apis/credentials amb
        el compte voluntarisgrupbarna@gmail.com
      · "Crear credenciales" → "ID de cliente de OAuth" → Tipus: Aplicación web
      · Nom: CB Grup Barna Admin
      · "Orígenes autorizados de JavaScript", afegeix-hi EXACTAMENT:
            https://cbgrupbarna.info
            https://www.cbgrupbarna.info
      · Crear → copia l'ID (acaba en .apps.googleusercontent.com)
   2) Enganxa'l aquí sota a GOOGLE_CLIENT_ID i puja el fitxer a GitHub.

   NOTA DE SEGURETAT: aquesta validació passa al navegador. Serveix per
   controlar QUI entra al panell i evitar que ningú de fora hi tafanegi,
   però no és una barrera criptogràfica: la barrera real és que per
   publicar canvis cal accés d'escriptura al repositori de GitHub.

   3) Per al Cuadro de mando (/admin/analitica.html) cal, a més:
      · L'ID de la propietat de GA4 (NO el "G-XXXXXXX" del gtag, un
        número): a Google Analytics → Administració → Detalls de la
        propietat → "ID de la propietat". Enganxa'l a GA4_PROPERTY_ID.
      · El compte de Google amb què es connecti al panell ha de tenir
        accés de lector (com a mínim) a aquesta propietat de GA4:
        Administració → Accés a la propietat → afegeix-hi el compte.
      · El mateix GOOGLE_CLIENT_ID d'aquí sobre ja serveix per a això;
        no cal crear-ne un altre.
   ========================================================= */

window.CBGB_ADMIN = {
  // ── Enganxa aquí l'ID de client de Google ──
  GOOGLE_CLIENT_ID: "",

  // ── ID numèric de la propietat GA4 (Cuadro de mando) ──
  GA4_PROPERTY_ID: "",

  // Comptes autoritzats a entrar al panell (afegeix-ne els que calgui)
  ALLOWED_EMAILS: [
    "voluntarisgrupbarna@gmail.com",
    "cbgrupbarna@gmail.com",
    "anafernandezduran78@gmail.com",
  ],

  // Domini de Google Workspace autoritzat (opcional, deixa'l buit si no en teniu)
  ALLOWED_DOMAIN: "",
};
