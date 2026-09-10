/* CB Grup Barna · Reserva de la prova d'Escoleta
   ───────────────────────────────────────────────────────────────
   El formulari curt de la portada: reservar la prova del dissabte
   19 de setembre (la mateixa sessió on es proven les nenes i nens
   de l'Escoleta) o demanar un altre dia del setembre de portes
   obertes.

   Va a la mateixa Apps Script que la resta de formularis del web,
   marcat amb source: 'prova-escoleta' perquè es pugui filtrar a la
   full de càlcul. Si l'endpoint no està configurat, el formulari
   segueix donant les gràcies i deixa el WhatsApp del club a la vista:
   val més una família que ens escriu que un botó apagat.
   ─────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var form = document.getElementById('rp-form');
  if (!form) return;
  var cfg = window.CANALS || {};
  var done = document.getElementById('rp-done');

  var camps = [
    { id: 'rp-nom', nom: 'nom' },
    { id: 'rp-any', nom: 'any' },
    { id: 'rp-tutor', nom: 'contacte' },
    { id: 'rp-via', nom: 'contacteVia' }
  ].map(function (c) {
    c.el = document.getElementById(c.id);
    c.err = document.getElementById(c.id + '-err');
    return c;
  });

  function mostra(c, mal) {
    if (c.err) c.err.classList.toggle('on', mal);
    c.el.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function malament(c) {
    var v = (c.el.value || '').trim();
    if (!v) return true;
    /* L'any de naixement és un any de veritat, no una edat. */
    if (c.nom === 'any') return !/^(19|20)\d{2}$/.test(v);
    return false;
  }

  camps.forEach(function (c) {
    c.el.addEventListener('input', function () {
      if (c.err && c.err.classList.contains('on')) mostra(c, malament(c));
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

    /* El consentiment és obligatori i no és un camp de text: es mira a part. */
    var ok = document.getElementById('rp-ok');
    if (ok && !ok.checked) { ok.focus(); return; }

    var boto = form.querySelector('button[type="submit"]');
    if (boto) boto.disabled = true;

    /* Amb mode no-cors mai sabem si ha arribat; als sis segons es dona
       per fet igualment i la família veu la confirmació. */
    var fet = false;
    function acabat() {
      if (fet) return;
      fet = true;
      form.hidden = true;
      if (done) {
        done.classList.add('on');
        done.setAttribute('tabindex', '-1');
        done.focus();
      }
    }

    var dia = form.querySelector('input[name="dia"]:checked');
    var msg = document.getElementById('rp-msg');
    var dades = {
      source: 'prova-escoleta',
      idioma: document.documentElement.lang,
      dia: dia ? dia.value : '',
      missatge: msg && msg.value.trim() ? msg.value.trim() : ''
    };
    camps.forEach(function (c) { dades[c.nom] = c.el.value.trim(); });

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
    if (window.gtag) window.gtag('event', 'reserva_prova_enviada', { dia: dades.dia });
  });
})();
