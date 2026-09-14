/* CB Grup Barna · Portes obertes de setembre · reserva de plaça
   ─────────────────────────────────────────────────────────────────────────
   DES DEL 13/09/2026 només reserven dos grups: l'Escoleta (4 a 8 anys) i
   les nenes nascudes el 2018 (Premini femení). La resta de categories no
   reserva aquí: se les porta a /proves-acces/ (Setmana Santa 2027). El
   formulari ho diu a la cara quan l'any de naixement no quadra amb el grup,
   i l'Apps Script ho torna a comprovar al servidor.

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
  var grups = [].slice.call(form.querySelectorAll('input[name="grup"]'));
  var grupErr = document.getElementById('po-grup-err');
  var anyAvis = document.getElementById('po-any-avis');

  /* Quins anys de naixement admet cada grup. El mateix mapa és a l'Apps
     Script (GRUPS): si es canvia aquí, es canvia allà. */
  var ANYS = {
    'escoleta':   [2018, 2019, 2020, 2021, 2022],
    'nenes-2018': [2018]
  };
  var PROVES = { ca: '/proves-acces/', es: '/es/pruebas-de-acceso/', en: '/en/tryouts/' };
  var done = document.getElementById('po-done');
  var diesErr = document.getElementById('po-dies-err');
  var caselles = [].slice.call(form.querySelectorAll('input[name="dissabtes"]'));

  /* ── 1. Places lliures ─────────────────────────────────────────────── */

  var TOTAL_PER_TORN = 50;

  /* El comptador es construeix aquí, no al marcatge, així que ha de saber
     l'idioma: si no, una família que llegeix la pàgina en castellà veu
     «Queden 15 places» enmig del seu formulari. */
  var T = {
    ca: { una: 'Queda 1 plaça', moltes: 'Queden {n} places', ple: 'Complet', ocup: '{p}% ple',
          gran: 'Amb aquest any de naixement no li toca Portes Obertes: li toca la <a href="{u}">prova d\'accés de Setmana Santa 2027</a>.',
          no2018: 'Aquest grup és només per a nenes nascudes el 2018. Si té una altra edat, tria Escoleta (2018-2022) o demana <a href="{u}">prova d\'accés</a>.',
          petit: 'Fins als 4 anys (nascuts el 2022) encara no hi ha grup. Escriu-nos i t\'avisem quan en tingui.' },
    es: { una: 'Queda 1 plaza', moltes: 'Quedan {n} plazas', ple: 'Completo', ocup: '{p}% lleno',
          gran: 'Con este año de nacimiento no le tocan las Puertas Abiertas: le toca la <a href="{u}">prueba de acceso de Semana Santa 2027</a>.',
          no2018: 'Este grupo es solo para niñas nacidas en 2018. Si tiene otra edad, elige Escoleta (2018-2022) o pide <a href="{u}">prueba de acceso</a>.',
          petit: 'Hasta los 4 años (nacidos en 2022) todavía no hay grupo. Escríbenos y te avisamos cuando lo haya.' },
    en: { una: '1 place left', moltes: '{n} places left', ple: 'Full', ocup: '{p}% full',
          gran: 'With this year of birth the Open Days are not the right door: apply for the <a href="{u}">Easter 2027 tryout</a> instead.',
          no2018: 'This group is only for girls born in 2018. For any other age, choose Escoleta (2018-2022) or apply for a <a href="{u}">tryout</a>.',
          petit: 'Children born after 2022 do not have a group yet. Write to us and we will let you know when there is one.' }
  };
  var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
  var t = T[codi] || T.ca;

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
        cartell.textContent = t.ple;
        cartell.classList.add('ple');
        cb.disabled = true;
        cb.checked = false;
      } else {
        var quantes = n === 1 ? t.una : t.moltes.replace('{n}', n);
        cartell.textContent = quantes + ' · ' + t.ocup.replace('{p}', pct);
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

  function grupTriat() {
    var g = null;
    grups.forEach(function (r) { if (r.checked) g = r.value; });
    return g;
  }

  /* L'any de naixement mana. Si no quadra amb el grup, s'explica a sota del
     camp per què i cap a on s'ha d'anar, en comptes d'un «any no vàlid» mut. */
  function avisAny() {
    if (!anyAvis) return false;
    var v = (document.getElementById('po-any') || {}).value || '';
    v = v.trim();
    var g = grupTriat();
    anyAvis.innerHTML = '';
    anyAvis.classList.remove('on');
    if (!/^(19|20)\d{2}$/.test(v) || !g) return false;
    var a = parseInt(v, 10);
    if (ANYS[g].indexOf(a) !== -1) return false;
    var u = PROVES[codi] || PROVES.ca;
    var text = g === 'nenes-2018' && a <= 2022 && a >= 2018 ? t.no2018
             : a > 2022 ? t.petit
             : t.gran;
    anyAvis.innerHTML = text.replace('{u}', u);
    anyAvis.classList.add('on');
    return true;
  }

  function malament(c) {
    var v = c.el.value.trim();
    if (!v) return true;
    // L'any de naixement ha de ser un any de veritat, no una edat, i ha de
    // quadrar amb el grup triat (Escoleta 2018-2022 · nenes 2018).
    if (c.nom === 'any') {
      if (!/^(19|20)\d{2}$/.test(v)) return true;
      var g = grupTriat();
      return !g || ANYS[g].indexOf(parseInt(v, 10)) === -1;
    }
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

  var campAny = camps.filter(function (c) { return c.nom === 'any'; })[0];
  grups.forEach(function (r) {
    r.addEventListener('change', function () {
      if (grupErr) grupErr.classList.remove('on');
      avisAny();
      if (campAny && campAny.err.classList.contains('on')) mostra(campAny, malament(campAny));
    });
  });
  if (campAny) campAny.el.addEventListener('input', avisAny);

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

    var capGrup = grups.length > 0 && !grupTriat();
    if (grupErr) grupErr.classList.toggle('on', capGrup);

    var primer = null;
    camps.forEach(function (c) {
      var mal = malament(c);
      mostra(c, mal);
      if (mal && !primer) primer = c.el;
    });

    if (capDia) { (primer || caselles[0]).focus(); return; }
    if (capGrup) { grups[0].focus(); return; }
    if (primer) { avisAny(); primer.focus(); return; }

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
      grup: grupTriat() || '',
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
