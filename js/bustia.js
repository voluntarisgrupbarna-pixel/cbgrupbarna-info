/* CB Grup Barna · Bústia de suggeriments
   Anònima: no demana ni envia cap dada d'identificació si l'usuari
   no deixa el correu expressament. */
(function () {
  var form = document.getElementById('bu-form');
  if (!form) return;
  var cfg  = window.CANALS || {};
  var tema = document.getElementById('bu-tema');
  var msg  = document.getElementById('bu-msg');
  var mail = document.getElementById('bu-mail');
  var mErr = document.getElementById('bu-msg-err');
  var eErr = document.getElementById('bu-mail-err');
  var done = document.getElementById('bu-done');

  function mostra(camp, err, mal) {
    err.classList.toggle('on', mal);
    camp.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function mailOk(v) { return v.trim() === '' || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }

  msg.addEventListener('input', function () { if (mErr.classList.contains('on')) mostra(msg, mErr, !msg.value.trim()); });
  mail.addEventListener('input', function () { if (eErr.classList.contains('on')) mostra(mail, eErr, !mailOk(mail.value)); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var malMsg = !msg.value.trim(), malMail = !mailOk(mail.value);
    mostra(msg, mErr, malMsg); mostra(mail, eErr, malMail);
    if (malMsg) { msg.focus(); return; }
    if (malMail) { mail.focus(); return; }

    form.querySelector('button[type="submit"]').disabled = true;
    var acabat = function () {
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };

    var dades = {
      tema: tema.value || '—',
      missatge: msg.value.trim(),
      source: 'bustia',
      idioma: document.documentElement.lang
    };
    // El correu només viatja si l'usuari l'ha escrit.
    if (mail.value.trim()) dades.email = mail.value.trim();

    // Al CRM només hi va el contacte de qui ha deixat el correu expressament,
    // i sense el text del missatge: la bústia és anònima i el que s'hi escriu
    // es queda a la full, no al CRM. Si no hi ha correu, aquí no s'envia res.
    if (window.BREVO && dades.email) {
      window.BREVO.envia('bustia', {
        email:  dades.email,
        tema:   dades.tema,
        idioma: dades.idioma,
        origen: 'bustia'
      });
    }

    if (cfg.bustiaEndpoint) {
      fetch(cfg.bustiaEndpoint, {
        method: 'POST', mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dades)
      }).then(acabat, acabat);
    } else {
      acabat();
    }
  });
})();
