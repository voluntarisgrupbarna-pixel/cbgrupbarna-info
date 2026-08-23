/* CB Grup Barna · Alta a la newsletter
   Envia a Brevo si CANALS.brevoAction està configurat; si no, guarda
   l'alta a la full de càlcul de sempre perquè no es perdi cap correu. */
(function () {
  var form = document.getElementById('nl-form');
  if (!form) return;
  var cfg   = window.CANALS || {};
  var email = document.getElementById('nl-email');
  var nom   = document.getElementById('nl-nom');
  var ok    = document.getElementById('nl-ok');
  var eErr  = document.getElementById('nl-email-err');
  var oErr  = document.getElementById('nl-ok-err');
  var done  = document.getElementById('nl-done');

  function mostra(camp, err, mal) {
    err.classList.toggle('on', mal);
    if (camp) camp.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function valid(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }

  email.addEventListener('input', function () { if (eErr.classList.contains('on')) mostra(email, eErr, !valid(email.value)); });
  ok.addEventListener('change', function () { if (oErr.classList.contains('on')) mostra(null, oErr, !ok.checked); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var malEmail = !valid(email.value), malOk = !ok.checked;
    mostra(email, eErr, malEmail); mostra(null, oErr, malOk);
    if (malEmail) { email.focus(); return; }
    if (malOk) { ok.focus(); return; }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;

    var acabat = function () {
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    if (cfg.brevoAction) {
      // Brevo espera un enviament de formulari clàssic, no JSON.
      var camps = cfg.brevoCamps || { email: 'EMAIL', nom: 'NOM' };
      var fd = new FormData();
      fd.append(camps.email, email.value.trim());
      if (nom.value.trim()) fd.append(camps.nom, nom.value.trim());
      fetch(cfg.brevoAction, { method: 'POST', mode: 'no-cors', body: fd })
        .then(acabat, acabat);
    } else if (cfg.bustiaEndpoint) {
      fetch(cfg.bustiaEndpoint, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nom: nom.value.trim(), email: email.value.trim(),
          newsletter: 'Sí', source: 'newsletter-web',
          idioma: document.documentElement.lang
        })
      }).then(acabat, acabat);
    } else {
      acabat();
    }
  });
})();
