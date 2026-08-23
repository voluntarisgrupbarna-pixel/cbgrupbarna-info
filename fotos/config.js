// CB Grup Barna · Galeria · Configuració
// Editable des del panell d'administrador: /fotos/admin.html

window.GALERIA_CONFIG = {
  require_access: false,
  // Dona accés als grups privats: /fotos/?marqueting=<aquesta clau>
  marketing_pin: 'barna-mk-1965',
  newsletter_email: 'voluntarisgrupbarna@gmail.com',
  // R2: buits = tot funciona com fins ara (fotos al repositori, pujada via
  // GitHub). Omple'ls seguint workers/fotos-upload/README.md per passar a
  // pujar directament a R2 sense generar un commit per foto.
  r2_public_base: '',   // p.ex. 'https://pub-xxxx.r2.dev'
  r2_worker_url: '',    // p.ex. 'https://cbgb-fotos-upload.xxx.workers.dev'
};
