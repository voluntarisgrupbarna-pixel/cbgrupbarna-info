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
    consent:   'CONSENT'
  };

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

    Object.keys(dades || {}).forEach(function (clau) {
      var valor = dades[clau];
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

  window.BREVO = { actiu: actiu, envia: envia, CAMPS: CAMPS };
})();
