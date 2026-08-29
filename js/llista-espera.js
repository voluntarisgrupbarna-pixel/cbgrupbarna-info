/* CB Grup Barna · Llista d'espera del campus
   ───────────────────────────────────────────────────────────────
   Qui deixa el contacte aquí vol saber quan obrim inscripcions.
   L'enviament va a l'Apps Script de CANALS.campusEndpoint, que fa
   tres coses: escriu una fila a la full de càlcul, avisa el club
   per correu, i envia la confirmació a qui s'ha apuntat.

   Amb mode no-cors no sabem mai del cert si ha arribat: per això,
   com a la resta de formularis del web, al cap de sis segons es
   dona per fet igualment i no deixem ningú mirant un botó apagat.
   ─────────────────────────────────────────────────────────────── */
(function () {
  var form = document.getElementById('le-form');
  if (!form) return;
  var cfg = window.CANALS || {};

  var camps = [
    { id: 'le-nom', nom: 'nom' },
    { id: 'le-any', nom: 'any' },
    { id: 'le-tutor', nom: 'tutor' },
    { id: 'le-mail', nom: 'correu' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  });
  var tel = document.getElementById('le-tel');
  var msg = document.getElementById('le-msg');
  var done = document.getElementById('le-done');

  function mostra(c, mal) {
    c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function malament(c) {
    var v = c.el.value.trim();
    if (!v) return true;
    // L'any de naixement ha de ser un any de veritat, no una edat.
    if (c.nom === 'any') return !/^(19|20)\d{2}$/.test(v);
    // Sense correu vàlid no li podem enviar la confirmació, que és
    // mig sentit del formulari.
    if (c.nom === 'correu') return !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
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
    var fet = false;
    var acabat = function () {
      if (fet) return;
      fet = true;
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var edicions = [].slice
      .call(form.querySelectorAll('input[name="edicions"]:checked'))
      .map(function (i) { return i.value; })
      .join(', ');

    var dades = {
      source: 'campus-llista-espera',
      idioma: document.documentElement.lang,
      edicions: edicions,
      telefon: tel && tel.value.trim() ? tel.value.trim() : '',
      missatge: msg && msg.value.trim() ? msg.value.trim() : ''
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

    setTimeout(acabat, 6000);
    var url = cfg.campusEndpoint || cfg.bustiaEndpoint;
    if (url) {
      fetch(url, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
    if (window.gtag) window.gtag('event', 'campus_llista_espera');
  });

  /* El mapa de Google posa galetes. No es carrega fins que algú el demana. */
  var botoMapa = document.getElementById('mapa-carrega');
  if (botoMapa) {
    botoMapa.addEventListener('click', function () {
      var caixa = botoMapa.parentNode;
      var q = encodeURIComponent(caixa.getAttribute('data-mapa') || 'La Nau del Clot Barcelona');
      var f = document.createElement('iframe');
      f.src = 'https://www.google.com/maps?q=' + q + '&output=embed';
      f.setAttribute('loading', 'lazy');
      f.setAttribute('title', caixa.getAttribute('data-mapa') || 'La Nau del Clot');
      f.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
      caixa.replaceChild(f, botoMapa);
    });
  }
})();
