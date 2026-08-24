/* CB Grup Barna · Enviament de contactes a Brevo (CRM)
   ───────────────────────────────────────────────────────────────
   Un sol lloc per parlar amb Brevo. Cada formulari del web té el seu
   propi formulari a Brevo (i, per tant, la seva pròpia llista); aquí
   només hi ha la mecànica d'enviar-hi les dades.

   Els formularis allotjats a Brevo (sibforms.com/serve/…) accepten un
   POST clàssic de tota la vida, sense clau d'API. Això és a posta: la
   web és estàtica i una clau d'API dins d'un fitxer .js la pot llegir
   tothom. Amb el formulari allotjat no hi ha res a filtrar.

   Com s'activa: /js/canals.js → bloc `brevo`. Instruccions completes,
   amb els atributs i les llistes que cal crear a Brevo, a
   /js/README-brevo.md.

   El canal de protecció del menor NO passa mai per aquí. Aquelles
   comunicacions no són contactes de màrqueting i no han de viure al CRM.
   ─────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  /* Noms per defecte dels atributs a Brevo. Si al compte del club se'n
     diuen d'una altra manera, es canvien a canals.js → brevo.camps. */
  var CAMPS = {
    email:     'EMAIL',
    nom:       'NOM',
    telefon:   'TELEFON',
    idioma:    'IDIOMA',
    origen:    'ORIGEN',
    interes:   'INTERES',
    tema:      'TEMA',
    missatge:  'MISSATGE',
    any:       'ANY_NAIX',
    contacte:  'CONTACTE',
    estrelles: 'ESTRELLES',
    consent:   'CONSENT',
    campanya:  'CAMPANYA',
    font:      'FONT',
    mitja:     'MITJA',
    referent:  'REFERENT',
    entrada:   'ENTRADA'
  };

  /* ── D'ON VE CADA CONTACTE ──────────────────────────────────────────
     Sense això, al CRM tothom sembla que hagi arribat sol. Amb això se
     sap quina campanya, quin cartell o quin reel ha portat cada alta, i
     es pot deixar de pagar el que no en porta cap.

     S'agafa de dues fonts:
       · Els paràmetres utm_* de l'enllaç (Instagram, anuncis, QR, correu).
       · Si no n'hi ha, d'on venia el navegador (instagram.com, google…).

     Es guarda a la sessió i mana la PRIMERA visita: qui entra per un
     anunci del campus, dona voltes pel web i acaba enviant el formulari
     de la portada, segueix comptant com a alta d'aquell anunci.        */
  var CLAU = 'cbgb-campanya';

  function xarxa(ref) {
    if (!ref) return '';
    try { ref = new URL(ref).hostname.replace(/^www\./, ''); } catch (_) { return ''; }
    if (ref === location.hostname) return '';                 // navegació interna
    if (/instagram/.test(ref))  return 'instagram';
    if (/facebook|fb\.com/.test(ref)) return 'facebook';
    if (/google/.test(ref))     return 'google';
    if (/tiktok/.test(ref))     return 'tiktok';
    if (/youtube|youtu\.be/.test(ref)) return 'youtube';
    if (/whatsapp|wa\.me/.test(ref))   return 'whatsapp';
    if (/bing|duckduckgo|ecosia|yahoo/.test(ref)) return 'cercador';
    return ref;
  }

  function campanya() {
    var desat = null;
    try { desat = JSON.parse(sessionStorage.getItem(CLAU) || 'null'); } catch (_) {}
    if (desat) return desat;

    var q = new URLSearchParams(location.search);
    var d = {
      campanya: q.get('utm_campaign') || q.get('campanya') || '',
      font:     q.get('utm_source')   || q.get('font')     || xarxa(document.referrer),
      mitja:    q.get('utm_medium')   || '',
      referent: xarxa(document.referrer),
      entrada:  location.pathname
    };
    if (!d.font && !d.campanya) d.font = 'directe';
    try { sessionStorage.setItem(CLAU, JSON.stringify(d)); } catch (_) {}
    return d;
  }

  function cfg() {
    return (window.CANALS && window.CANALS.brevo) || {};
  }

  /* L'`action` del formulari de Brevo per aquest canal, si n'hi ha.
     `newsletter` accepta també el `brevoAction` de sempre, perquè els
     comptes que ja el tenien posat no es quedin sense enviar res. */
  function accio(canal) {
    var c = cfg();
    var url = (c.formularis || {})[canal] || '';
    if (!url && canal === 'newsletter') url = (window.CANALS || {}).brevoAction || '';
    return typeof url === 'string' ? url.trim() : '';
  }

  function actiu(canal) { return !!accio(canal); }

  /* Envia un contacte a Brevo. No falla mai cap a fora: si Brevo no està
     configurat o la xarxa peta, la promesa es resol igualment i el
     formulari segueix el seu camí de sempre (Apps Script, Formspree o
     WhatsApp). Cap alta es perd per culpa d'això. */
  function envia(canal, dades) {
    var url = accio(canal);
    if (!url) return Promise.resolve(false);

    var c = cfg();
    var camps = c.camps || {};
    var fd = new FormData();

    /* La campanya s'hi afegeix sola, a tots els formularis: si algun dia
       s'ha de tocar d'on ve, es toca aquí i prou. El que porti el
       formulari mana, per si mai vol dir una altra cosa. */
    var tot = {};
    var orig = campanya();
    Object.keys(orig).forEach(function (k) { tot[k] = orig[k]; });
    Object.keys(dades || {}).forEach(function (k) { tot[k] = dades[k]; });

    Object.keys(tot).forEach(function (clau) {
      var valor = tot[clau];
      if (valor === undefined || valor === null) return;
      if (Array.isArray(valor)) valor = valor.join(', ');
      valor = String(valor).trim();
      if (!valor) return;
      fd.append(camps[clau] || CAMPS[clau] || clau.toUpperCase(), valor);
    });

    if (!fd.has(camps.email || CAMPS.email)) return Promise.resolve(false);

    /* Els dos camps que Brevo posa a tots els seus formularis: el parany
       per a robots (ha d'anar buit) i l'idioma de les seves pantalles de
       confirmació. */
    fd.append('email_address_check', '');
    fd.append('locale', (c.locale || (document.documentElement.lang || 'ca')).slice(0, 2));

    return fetch(url, { method: 'POST', mode: 'no-cors', body: fd })
      .then(function () { return true; }, function () { return false; });
  }

  /* Es desa d'on ve la visita ARA, en carregar la pàgina, no en enviar el
     formulari: qui entra per un anunci pot aterrar a /campus/ i acabar
     enviant el formulari de la portada, i per llavors ja no queda cap
     rastre de l'anunci a l'adreça. Per això aquest fitxer es carrega a
     tot el web, no només a les pàgines amb formulari. */
  campanya();

  window.BREVO = { actiu: actiu, envia: envia, campanya: campanya, CAMPS: CAMPS };
})();
