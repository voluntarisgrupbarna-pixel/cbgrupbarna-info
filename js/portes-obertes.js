/* CB Grup Barna · Portes obertes de setembre
   Demanar venir a provar un entrenament. A diferència de la bústia, aquí sí
   que cal saber qui escriu: hem de poder respondre amb el dia i l'hora.
   Va a la mateixa Apps Script que la resta de formularis, marcat amb
   source: 'portes-obertes' perquè es pugui filtrar a la full. */
(function () {
  var form = document.getElementById('po-form');
  if (!form) return;
  var cfg = window.CANALS || {};

  var camps = [
    { id: 'po-nom', nom: 'nom' },
    { id: 'po-any', nom: 'any' },
    { id: 'po-contacte', nom: 'contacte' },
    { id: 'po-tel', nom: 'contacteVia' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  });
  var msg = document.getElementById('po-msg');
  var done = document.getElementById('po-done');

  function mostra(c, mal) {
    c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function malament(c) {
    var v = c.el.value.trim();
    if (!v) return true;
    // L'any de naixement ha de ser un any de veritat, no una edat.
    if (c.nom === 'any') return !/^(19|20)\d{2}$/.test(v);
    return false;
  }

  camps.forEach(function (c) {
    c.el.addEventListener('input', function () {
      if (c.err.classList.contains('on')) mostra(c, malament(c));
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var primer = null;
    camps.forEach(function (c) {
      var mal = malament(c);
      mostra(c, mal);
      if (mal && !primer) primer = c.el;
    });
    if (primer) { primer.focus(); return; }

    form.querySelector('button[type="submit"]').disabled = true;
    var acabat = function () {
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var dades = {
      source: 'portes-obertes',
      idioma: document.documentElement.lang,
      missatge: msg && msg.value.trim() ? msg.value.trim() : ''
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

    if (cfg.bustiaEndpoint) {
      fetch(cfg.bustiaEndpoint, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
    if (window.gtag) window.gtag('event', 'portes_obertes_enviat');
  });
})();
