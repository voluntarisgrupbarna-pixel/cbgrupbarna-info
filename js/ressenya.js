/* CB Grup Barna · Ressenya al mateix lloc
   El formulari de ressenyes de Google no es pot encastar —Google el serveix
   amb X-Frame-Options i no deixa posar-lo dins d'un iframe—, així que aquí es
   recull la ressenya sense treure ningú de la pàgina i, un cop enviada,
   s'ofereix publicar-la també a Google, que és el que compta al cercador.
   Va a la mateixa Apps Script que la resta de formularis, amb
   source: 'ressenya'. */
(function () {
  var form = document.getElementById('rs-form');
  if (!form) return;
  var cfg = window.CANALS || {};
  var nom = document.getElementById('rs-nom');
  var mail = document.getElementById('rs-mail');
  var msg = document.getElementById('rs-msg');
  var done = document.getElementById('rs-done');
  var google = document.getElementById('rs-google');

  var errs = {
    nom: document.getElementById('rs-nom-err'),
    mail: document.getElementById('rs-mail-err'),
    msg: document.getElementById('rs-msg-err')
  };

  function mostra(camp, err, mal) {
    err.classList.toggle('on', mal);
    camp.setAttribute('aria-invalid', mal ? 'true' : 'false');
  }
  function mailOk(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); }

  [[nom, errs.nom, function () { return !nom.value.trim(); }],
   [mail, errs.mail, function () { return !mailOk(mail.value); }],
   [msg, errs.msg, function () { return !msg.value.trim(); }]
  ].forEach(function (t) {
    t[0].addEventListener('input', function () {
      if (t[1].classList.contains('on')) mostra(t[0], t[1], t[2]());
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var malNom = !nom.value.trim();
    var malMail = !mailOk(mail.value);
    var malMsg = !msg.value.trim();
    mostra(nom, errs.nom, malNom);
    mostra(mail, errs.mail, malMail);
    mostra(msg, errs.msg, malMsg);
    if (malNom) { nom.focus(); return; }
    if (malMail) { mail.focus(); return; }
    if (malMsg) { msg.focus(); return; }

    var triada = form.querySelector('input[name="estrelles"]:checked');
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
      // El botó de Google és el mateix enllaç que ja fa servir la pàgina.
      var cta = document.getElementById('ctaHero');
      if (google && cta && cta.getAttribute('href')) {
        google.setAttribute('href', cta.getAttribute('href'));
      }
    };

    var dades = {
      source: 'ressenya',
      idioma: document.documentElement.lang,
      estrelles: triada ? triada.value : '',
      nom: nom.value.trim(),
      email: mail.value.trim(),
      missatge: msg.value.trim()
    };

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
    if (window.gtag) {
      window.gtag('event', 'ressenya_al_lloc', { estrelles: dades.estrelles });
    }
  });
})();
