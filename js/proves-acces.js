/* CB Grup Barna · Proves d'accés de Setmana Santa 2027 · sol·licitud
   ─────────────────────────────────────────────────────────────────────────
   Formulari de /proves-acces/ (i les versions /es/ i /en/). És la porta
   d'entrada de TOTES les categories que no reserven a Portes Obertes:
   Premini masculí, Mini, Preinfantil, Infantil, Cadet, Júnior, Sub-22 i
   Sènior, masculí i femení.

   L'Escoleta (nascuts 2018-2022) i les nenes del 2018 NO van aquí: van a
   /portes-obertes/. El formulari ho diu quan l'any de naixement ho demana.

   Tres feines:
     1. Dir, mentre s'escriu l'any, quina categoria li tocaria el 2027-28.
        Només orienta: l'equip el decideix la direcció esportiva.
     2. Validar i explicar què falta.
     3. Enviar la sol·licitud a l'Apps Script de Portes Obertes
        (scripts/apps-script-portes-obertes.gs) amb source: 'proves-acces'.
        Allà va a un full a part i surten els dos correus. */
(function () {
  var form = document.getElementById('pa-form');
  if (!form) return;
  var cfg = window.CANALS || {};
  var endpoint = cfg.provesAccesEndpoint || cfg.portesObertesEndpoint || '';
  var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();

  var PO = { ca: '/portes-obertes/#po-form', es: '/es/puertas-abiertas/#po-form', en: '/en/open-days/#po-form' };

  var T = {
    ca: {
      cat: 'Categoria orientativa 2027-28: <b>{c}</b>',
      escoleta: 'Amb aquest any de naixement li toca l\'Escoleta: reserva plaça a les <a href="{u}">Portes Obertes</a>, no aquí.',
      nena2018: 'Les nenes nascudes el 2018 tenen plaça directa a les <a href="{u}">Portes Obertes</a>: reserva-la allà, no cal prova.',
      noms: { 'Premini': 'Premini', 'Mini': 'Mini', 'Preinfantil': 'Preinfantil', 'Infantil': 'Infantil', 'Cadet': 'Cadet', 'Júnior': 'Júnior', 'Sub-22 / Sènior': 'Sub-22 / Sènior', 'Sènior': 'Sènior' }
    },
    es: {
      cat: 'Categoría orientativa 2027-28: <b>{c}</b>',
      escoleta: 'Con este año de nacimiento le toca la Escoleta: reserva plaza en las <a href="{u}">Puertas Abiertas</a>, no aquí.',
      nena2018: 'Las niñas nacidas en 2018 tienen plaza directa en las <a href="{u}">Puertas Abiertas</a>: resérvala allí, no hace falta prueba.',
      noms: { 'Premini': 'Premini', 'Mini': 'Mini', 'Preinfantil': 'Preinfantil', 'Infantil': 'Infantil', 'Cadet': 'Cadete', 'Júnior': 'Júnior', 'Sub-22 / Sènior': 'Sub-22 / Sénior', 'Sènior': 'Sénior' }
    },
    en: {
      cat: 'Indicative age group for 2027-28: <b>{c}</b>',
      escoleta: 'With this year of birth the right door is the Escoleta: book a place at the <a href="{u}">Open Days</a>, not here.',
      nena2018: 'Girls born in 2018 have a direct place at the <a href="{u}">Open Days</a>: book there, no tryout needed.',
      noms: { 'Premini': 'U10 (Premini)', 'Mini': 'U12 (Mini)', 'Preinfantil': 'U13 (Preinfantil)', 'Infantil': 'U14 (Infantil)', 'Cadet': 'U16 (Cadet)', 'Júnior': 'U18 (Júnior)', 'Sub-22 / Sènior': 'U22 / Senior', 'Sènior': 'Senior' }
    }
  };
  var t = T[codi] || T.ca;

  /* Model FCBQ per a la temporada 2027-28. El mateix càlcul és a l'Apps
     Script (categoria2728): si es canvia aquí, es canvia allà. */
  function categoria(any) {
    var a = parseInt(any, 10);
    if (!a) return '';
    if (a >= 2019) return 'Escoleta';
    if (a >= 2018) return 'Premini';
    if (a >= 2016) return 'Mini';
    if (a === 2015) return 'Preinfantil';
    if (a === 2014) return 'Infantil';
    if (a >= 2012) return 'Cadet';
    if (a >= 2010) return 'Júnior';
    if (a >= 2005) return 'Sub-22 / Sènior';
    return 'Sènior';
  }

  var camps = [
    { id: 'pa-nom', nom: 'nom' },
    { id: 'pa-any', nom: 'any' },
    { id: 'pa-contacte', nom: 'tutor' },
    { id: 'pa-correu', nom: 'correu' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  }).filter(function (c) { return c.el && c.err; });

  var equips = [].slice.call(form.querySelectorAll('input[name="equip"]'));
  var equipErr = document.getElementById('pa-equip-err');
  var anyEl = document.getElementById('pa-any');
  var anyAvis = document.getElementById('pa-any-avis');
  var catEl = document.getElementById('pa-cat');
  var club = document.getElementById('pa-club');
  var anysJugant = document.getElementById('pa-anys');
  var posicio = document.getElementById('pa-posicio');
  var tel = document.getElementById('pa-tel');
  var msg = document.getElementById('pa-msg');
  var done = document.getElementById('pa-done');

  function equipTriat() {
    var e = null;
    equips.forEach(function (r) { if (r.checked) e = r.value; });
    return e;
  }

  /* Cap a on ha d'anar segons l'any: aquí, a l'Escoleta o a les nenes 2018. */
  function porta(any) {
    var a = parseInt(any, 10);
    if (!a) return 'cap';
    if (a >= 2019) return 'escoleta';
    if (a === 2018 && equipTriat() === 'femeni') return 'nena2018';
    return 'aqui';
  }

  function pintaAny() {
    var v = anyEl ? anyEl.value.trim() : '';
    if (catEl) { catEl.innerHTML = ''; catEl.classList.remove('on'); }
    if (anyAvis) { anyAvis.innerHTML = ''; anyAvis.classList.remove('on'); }
    if (!/^(19|20)\d{2}$/.test(v)) return;
    var on = porta(v);
    var u = PO[codi] || PO.ca;
    if (on === 'escoleta' || on === 'nena2018') {
      if (anyAvis) { anyAvis.innerHTML = t[on].replace('{u}', u); anyAvis.classList.add('on'); }
      return;
    }
    var c = categoria(v);
    if (catEl && c) {
      catEl.innerHTML = t.cat.replace('{c}', t.noms[c] || c);
      catEl.classList.add('on');
    }
  }

  function mostra(c, mal) {
    c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }

  function malament(c) {
    var v = c.el.value.trim();
    if (!v) return true;
    if (c.nom === 'any') return !/^(19|20)\d{2}$/.test(v) || porta(v) !== 'aqui';
    if (c.nom === 'correu') return !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    return false;
  }

  camps.forEach(function (c) {
    c.el.addEventListener('input', function () {
      if (c.err.classList.contains('on')) mostra(c, malament(c));
    });
  });
  if (anyEl) anyEl.addEventListener('input', pintaAny);
  equips.forEach(function (r) {
    r.addEventListener('change', function () {
      if (equipErr) equipErr.classList.remove('on');
      pintaAny();
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var capEquip = equips.length > 0 && !equipTriat();
    if (equipErr) equipErr.classList.toggle('on', capEquip);

    var primer = null;
    camps.forEach(function (c) {
      var mal = malament(c);
      mostra(c, mal);
      if (mal && !primer) primer = c.el;
    });
    if (capEquip) { equips[0].focus(); return; }
    if (primer) { pintaAny(); primer.focus(); return; }

    form.querySelector('button[type="submit"]').disabled = true;

    // Amb mode no-cors no sabem mai si ha arribat, i si la xarxa es queda
    // penjada la família es queda mirant un botó apagat. Al cap de sis
    // segons es dona per fet igualment: la sol·licitud ja ha sortit.
    var fet = false;
    var acabat = function () {
      if (fet) return;
      fet = true;
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var disp = form.querySelector('input[name="disponibilitat"]:checked');
    var dades = {
      source: 'proves-acces',
      idioma: document.documentElement.lang,
      equip: equipTriat() || '',
      categoria: categoria(anyEl ? anyEl.value : ''),
      club: club && club.value.trim() ? club.value.trim() : '',
      anysJugant: anysJugant && anysJugant.value ? anysJugant.value : '',
      posicio: posicio && posicio.value ? posicio.value : '',
      disponibilitat: disp ? disp.value : '',
      telefon: tel && tel.value.trim() ? tel.value.trim() : '',
      missatge: msg && msg.value.trim() ? msg.value.trim() : ''
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

    setTimeout(acabat, 6000);
    if (endpoint) {
      fetch(endpoint, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
    if (window.gtag) window.gtag('event', 'proves_acces_solicitud');
  });
})();
