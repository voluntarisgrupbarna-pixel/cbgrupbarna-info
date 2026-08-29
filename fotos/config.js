// CB Grup Barna · Galeria · Configuració
// Editable des del panell d'administrador: /fotos/admin.html

window.GALERIA_CONFIG = {
  require_access: false,
  // Clau mestra: obre TOTS els grups privats de cop amb
  // /fotos/?marqueting=<aquesta clau>. Cada grup privat té a més la seva
  // pròpia clau (`access_key` a events.js) i el seu enllaç, que només obre
  // aquell grup: és el que es passa a un equip o a una família.
  marketing_pin: 'barna-mk-1965',
  newsletter_email: 'marqueting@cbgrupbarna.info',
  // R2: buits = tot funciona com fins ara (fotos al repositori, pujada via
  // GitHub). Omple'ls seguint workers/fotos-upload/README.md per passar a
  // pujar directament a R2 sense generar un commit per foto.
  r2_public_base: '',   // p.ex. 'https://pub-xxxx.r2.dev'
  r2_worker_url: '',    // p.ex. 'https://cbgb-fotos-upload.xxx.workers.dev'
};
