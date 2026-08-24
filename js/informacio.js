/* CB Grup Barna · Demanar informació
   Aquí sí que cal saber qui escriu: la gràcia és poder respondre. La bústia
   de suggeriments, que és anònima, va a part (js/bustia.js).
   Les dues van a la mateixa Apps Script, marcades amb source diferent perquè
   es puguin separar a la full. */
(function () {
  var form = document.getElementById('in-form');
  if (!form) return;
  var cfg = window.CANALS || {};
  var tema = document.getElementById('in-tema');
  var done = document.getElementById('in-done');

  var camps = [
    { id: 'in-nom', nom: 'nom' },
    { id: 'in-via', nom: 'contacteVia' },
    { id: 'in-msg', nom: 'missatge' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  });

  function mostra(c, mal) {
    c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }

  camps.forEach(function (c) {
    c.el.addEventListener('input', function () {
      if (c.err.classList.contains('on')) mostra(c, !c.el.value.trim());
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var primer = null;
    camps.forEach(function (c) {
      var mal = !c.el.value.trim();
      mostra(c, mal);
      if (mal && !primer) primer = c.el;
    });
    if (primer) { primer.focus(); return; }

    form.querySelector('button[type="submit"]').disabled = true;
    // Amb mode no-cors no sabem mai si ha arribat, i si la xarxa es queda
    // penjada l'usuari es queda mirant un botó apagat. Al cap de sis segons
    // es dona per fet igualment.
    var fet = false;
    var acabat = function () {
      if (fet) return;
      fet = true;
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var dades = {
      source: 'informacio',
      idioma: document.documentElement.lang,
      tema: tema && tema.value ? tema.value : '—'
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

    // Al CRM hi va el contacte; a la full de càlcul, la conversa sencera.
    // Són dos destins alhora a posta: la full segueix sent la còpia de
    // seguretat mentre no tinguem tot l'històric a Brevo.
    if (window.BREVO) {
      var via = dades.contacteVia || '';
      var esMail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(via);
      window.BREVO.envia('informacio', {
        email:    esMail ? via : '',
        telefon:  esMail ? '' : via,
        nom:      dades.nom,
        tema:     dades.tema,
        missatge: dades.missatge,
        idioma:   dades.idioma,
        origen:   'escriu-nos'
      });
    }

    setTimeout(acabat, 6000);
    if (cfg.bustiaEndpoint) {
      fetch(cfg.bustiaEndpoint, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
    if (window.gtag) window.gtag('event', 'informacio_enviada');
  });
})();
