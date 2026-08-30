/* CB Grup Barna · Portes obertes de setembre · reserva de plaça
   ─────────────────────────────────────────────────────────────────────────
   Dues feines:
     1. Llegir del servidor quantes places queden a cada dissabte i pintar-ho
        a les targetes (comptador i barra d'ocupació). Un torn ple es
        desactiva de veritat, no només a la vista.
     2. Enviar la reserva.

   La disponibilitat que mana és la del servidor
   (scripts/apps-script-portes-obertes.gs): aquí només es pinta. Qui compta
   les places de debò i rebutja la plaça 51 és l'Apps Script, perquè el que
   passa pel navegador es pot falsejar. */
(function () {
  var form = document.getElementById('po-form');
  if (!form) return;
  var cfg = window.CANALS || {};
  var endpoint = cfg.portesObertesEndpoint || '';

  var camps = [
    { id: 'po-nom', nom: 'nom' },
    { id: 'po-edat', nom: 'edat' },
    { id: 'po-any', nom: 'any' },
    { id: 'po-contacte', nom: 'tutor' },
    { id: 'po-correu', nom: 'correu' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  }).filter(function (c) { return c.el && c.err; });

  var msg = document.getElementById('po-msg');
  var tel = document.getElementById('po-tel');
  var done = document.getElementById('po-done');
  var diesErr = document.getElementById('po-dies-err');
  var caselles = [].slice.call(form.querySelectorAll('input[name="dissabtes"]'));

  /* ── 1. Places lliures ─────────────────────────────────────────────── */

  var TOTAL_PER_TORN = 50;

  function pintaPlaces(lliures, ocupacio) {
    caselles.forEach(function (cb) {
      var clau = cb.value;
      var n = lliures && typeof lliures[clau] === 'number' ? lliures[clau] : null;
      var cartell = form.querySelector('[data-places="' + clau + '"]');
      if (!cartell) return;

      if (n === null) { cartell.textContent = ''; return; }

      var pct = ocupacio && typeof ocupacio[clau] === 'number'
        ? ocupacio[clau]
        : Math.round((TOTAL_PER_TORN - n) / TOTAL_PER_TORN * 100);

      cartell.classList.remove('poques', 'ple');
      if (n <= 0) {
        cartell.textContent = 'Complet';
        cartell.classList.add('ple');
        cb.disabled = true;
        cb.checked = false;
      } else {
        cartell.textContent = n === 1
          ? 'Queda 1 plaça · ' + pct + '% ple'
          : 'Queden ' + n + ' places · ' + pct + '% ple';
        // «Poques» a partir de la meitat plena: el vermell ha de voler dir
        // alguna cosa, i si hi és sempre no vol dir res.
        if (pct >= 50) cartell.classList.add('poques');
      }

      var barra = cartell.nextElementSibling;
      if (!barra || !barra.classList.contains('po-barra')) {
        barra = document.createElement('span');
        barra.className = 'po-barra';
        barra.setAttribute('aria-hidden', 'true');
        barra.innerHTML = '<i></i>';
        cartell.parentNode.insertBefore(barra, cartell.nextSibling);
      }
      barra.firstChild.style.width = Math.min(100, Math.max(0, pct)) + '%';
    });
  }

  // Sense endpoint encara desplegat, les targetes no han de quedar dient
  // «Carregant…» per sempre: es deixen netes i el formulari segueix servint.
  if (!endpoint) {
    pintaPlaces(null, null);
  } else {
    fetch(endpoint, { method: 'GET' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.places_lliures) pintaPlaces(d.places_lliures, d.ocupacio_percent);
        else pintaPlaces(null, null);
      })
      .catch(function () { pintaPlaces(null, null); });
  }

  /* ── 2. Validació ──────────────────────────────────────────────────── */

  function mostra(c, mal) {
    c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }

  function malament(c) {
    var v = c.el.value.trim();
    if (!v) return true;
    // L'any de naixement ha de ser un any de veritat, no una edat.
    if (c.nom === 'any') return !/^(19|20)\d{2}$/.test(v);
    if (c.nom === 'edat') return !/^\d{1,2}$/.test(v);
    if (c.nom === 'correu') return !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    return false;
  }

  camps.forEach(function (c) {
    c.el.addEventListener('input', function () {
      if (c.err.classList.contains('on')) mostra(c, malament(c));
    });
  });

  caselles.forEach(function (cb) {
    cb.addEventListener('change', function () {
      if (diesErr.classList.contains('on') && triats().length) {
        diesErr.classList.remove('on');
      }
    });
  });

  function triats() {
    return caselles.filter(function (cb) { return cb.checked && !cb.disabled; })
                   .map(function (cb) { return cb.value; });
  }

  /* ── 3. Enviament ──────────────────────────────────────────────────── */

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var dies = triats();
    var capDia = dies.length === 0;
    diesErr.classList.toggle('on', capDia);

    var primer = null;
    camps.forEach(function (c) {
      var mal = malament(c);
      mostra(c, mal);
      if (mal && !primer) primer = c.el;
    });

    if (capDia) { (primer || caselles[0]).focus(); return; }
    if (primer) { primer.focus(); return; }

    form.querySelector('button[type="submit"]').disabled = true;

    // Amb mode no-cors no sabem mai si ha arribat, i si la xarxa es queda
    // penjada la família es queda mirant un botó apagat. Al cap de sis
    // segons es dona per fet igualment: la reserva ja ha sortit.
    var fet = false;
    var acabat = function () {
      if (fet) return;
      fet = true;
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var jugat = form.querySelector('input[name="jugat"]:checked');
    var dades = {
      source: 'portes-obertes',
      idioma: document.documentElement.lang,
      dissabtes: dies.join(','),
      jugat: jugat ? jugat.value : 'no',
      telefon: tel && tel.value.trim() ? tel.value.trim() : '',
      missatge: msg && msg.value.trim() ? msg.value.trim() : ''
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

    setTimeout(acabat, 6000);
    // Sense l'Apps Script de portes obertes, la reserva cau a la bústia:
    // s'apunta igual, però no surten els correus ni l'esdeveniment de
    // calendari i s'han de fer a mà des de la full.
    var desti = endpoint || cfg.bustiaEndpoint;
    if (desti) {
      fetch(desti, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
    if (window.gtag) window.gtag('event', 'portes_obertes_reserva');
  });
})();
