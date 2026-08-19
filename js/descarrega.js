/* =========================================================
   CB Grup Barna · Porta de descàrrega de documents
   ---------------------------------------------------------
   Qualsevol enllaç amb data-descarrega="<nom del document>"
   demana les dades de contacte abans de descarregar el PDF.
   Les dades van a la mateixa full de càlcul del club que fa
   servir la galeria d'esdeveniments (Apps Script), amb el
   camp "font" marcant quin document s'ha demanat, i amb la
   subscripció al butlletí com a casella a part.

   Ús:
     <a href="/…/dossier.pdf" download
        data-descarrega="Dossier de l'Escoleta">Descarregar</a>
     <script src="/js/descarrega.js" defer></script>

   Qui ja ha deixat les dades una vegada no les torna a
   escriure: es recorda al navegador i descarrega directament.
   ========================================================= */
(function () {
  'use strict';

  var API_URL = 'https://script.google.com/macros/s/AKfycbyLOfEUjKpj3ezbLp1L_ZaZVQ3482dfYFoFOc_WvIH_nQfuDjU6_7hqn16g4uGcIz-Z/exec';
  var LS_KEY = 'cbgb_lead_descarrega';
  var RED = '#E20613';
  var INK = '#0a0a0a';

  function lead() {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || 'null'); } catch (e) { return null; }
  }
  function enc(s) { return encodeURIComponent(s || ''); }

  function baixa(href, nomFitxer) {
    var a = document.createElement('a');
    a.href = href;
    a.download = nomFitxer || '';
    a.rel = 'noopener';
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { a.remove(); }, 0);
  }

  function fonts() {
    if (document.getElementById('cbgb-dl-fonts')) return;
    var l = document.createElement('link');
    l.id = 'cbgb-dl-fonts';
    l.rel = 'stylesheet';
    l.href = 'https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400;500&family=Inter:wght@300;400;500;600&display=swap';
    document.head.appendChild(l);
  }

  function estils() {
    if (document.getElementById('cbgb-dl-css')) return;
    var s = document.createElement('style');
    s.id = 'cbgb-dl-css';
    s.textContent = [
      // Per sobre del rètol de galetes (z-index 2147483000 a galetes.js):
      // és un diàleg que l'usuari acaba d'obrir i no s'ha de quedar tapat.
      '.cbgb-dl-bg{position:fixed;inset:0;z-index:2147483100;background:rgba(10,10,10,.62);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:20px;overflow-y:auto}',
      '.cbgb-dl{background:#fff;color:' + INK + ';font-family:Inter,-apple-system,system-ui,sans-serif;font-weight:300;width:100%;max-width:430px;padding:30px 26px 26px;position:relative;max-height:calc(100vh - 40px);overflow-y:auto}',
      // Reset defensiu: cada pàgina té els seus estils (.eyebrow, inputs,
      // botons…) i no han de tenyir el diàleg. Va primer; les regles pròpies
      // de sota el sobreescriuen.
      '.cbgb-dl *,.cbgb-dl *::before,.cbgb-dl *::after{box-sizing:border-box}',
      '.cbgb-dl p,.cbgb-dl h2,.cbgb-dl label,.cbgb-dl span,.cbgb-dl div,.cbgb-dl form,.cbgb-dl input,.cbgb-dl button{background:none;border-radius:0;box-shadow:none;float:none;text-align:left;letter-spacing:normal;text-transform:none;margin:0;padding:0;max-width:none;min-height:0}',
      '.cbgb-dl h2{font-family:Jost,"Futura",sans-serif;font-weight:300;text-transform:uppercase;letter-spacing:.1em;font-size:1.15rem;line-height:1.35;margin:0 0 8px}',
      '.cbgb-dl h2 em{font-style:normal;color:' + RED + '}',
      '.cbgb-dl .cbgb-dl-eye{font-family:Jost,sans-serif;font-size:9px;letter-spacing:.3em;text-transform:uppercase;color:#8a8681;margin:0 0 14px}',
      '.cbgb-dl .cbgb-dl-intro{font-size:.85rem;color:#46433f;line-height:1.6;margin:0 0 20px}',
      '.cbgb-dl label.cbgb-dl-f{display:block;margin-bottom:12px}',
      '.cbgb-dl label.cbgb-dl-f span{display:block;font-family:Jost,sans-serif;font-size:9px;letter-spacing:.22em;text-transform:uppercase;color:#8a8681;margin-bottom:5px}',
      '.cbgb-dl input[type=text],.cbgb-dl input[type=email],.cbgb-dl input[type=tel]{width:100%;background:#f6f4f1;border:1px solid #e4e1dd;color:' + INK + ';padding:.65rem .8rem;font-family:Inter,sans-serif;font-size:.92rem;outline:none}',
      '.cbgb-dl input:focus{border-color:' + RED + '}',
      '.cbgb-dl .cbgb-dl-chk{display:flex;gap:10px;align-items:flex-start;margin:14px 0;font-size:.78rem;line-height:1.55;color:#46433f}',
      '.cbgb-dl .cbgb-dl-chk input{margin-top:3px;flex:none;accent-color:' + RED + ';width:16px;height:16px}',
      '.cbgb-dl .cbgb-dl-chk a{color:' + INK + ';border-bottom:1px solid ' + RED + '}',
      '.cbgb-dl .cbgb-dl-news{background:#f6f4f1;padding:12px 14px;margin:16px 0 4px}',
      '.cbgb-dl .cbgb-dl-news .cbgb-dl-chk{margin:0}',
      '.cbgb-dl button.go{width:100%;background:' + INK + ';border:1px solid ' + INK + ';color:#fff;padding:.85rem 1rem;font-family:Jost,sans-serif;font-size:10px;letter-spacing:.24em;text-transform:uppercase;cursor:pointer;margin-top:16px;transition:background .3s,border-color .3s}',
      '.cbgb-dl button.go:hover{background:' + RED + ';border-color:' + RED + '}',
      '.cbgb-dl button.go:disabled{opacity:.55;cursor:default}',
      '.cbgb-dl button.x{position:absolute;top:10px;right:12px;background:none;border:0;font-size:1.5rem;line-height:1;color:#8a8681;cursor:pointer;padding:4px 8px}',
      '.cbgb-dl button.x:hover{color:' + RED + '}',
      '.cbgb-dl .cbgb-dl-err{display:none;color:' + RED + ';font-size:.78rem;margin-top:10px;line-height:1.5}',
      '.cbgb-dl .cbgb-dl-peu{font-family:Jost,sans-serif;font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:#8a8681;margin:18px 0 0;line-height:1.7;text-align:center}',
      '.cbgb-dl :focus-visible{outline:1px solid ' + RED + ';outline-offset:3px}',
      '@media (max-width:420px){.cbgb-dl{padding:26px 20px 22px}}'
    ].join('');
    document.head.appendChild(s);
  }

  function obre(doc, href, doneFn) {
    fonts(); estils();

    var bg = document.createElement('div');
    bg.className = 'cbgb-dl-bg';
    bg.innerHTML =
      '<div class="cbgb-dl" role="dialog" aria-modal="true" aria-labelledby="cbgb-dl-t">' +
        '<button class="x" type="button" aria-label="Tancar">&times;</button>' +
        '<p class="cbgb-dl-eye">CB Grup Barna · Document</p>' +
        '<h2 id="cbgb-dl-t">Descarrega <em>' + doc.replace(/[<>&]/g, '') + '</em></h2>' +
        '<p class="cbgb-dl-intro">Deixa\'ns el contacte i te\'l descarreguem ara mateix. Ens serveix per ' +
          'saber qui s\'interessa pel club i poder-te ajudar si tens preguntes.</p>' +
        '<form novalidate>' +
          '<label class="cbgb-dl-f"><span>Nom i cognoms</span>' +
            '<input type="text" name="nom" autocomplete="name" required></label>' +
          '<label class="cbgb-dl-f"><span>Correu electrònic</span>' +
            '<input type="email" name="email" autocomplete="email" inputmode="email" required></label>' +
          '<label class="cbgb-dl-f"><span>Mòbil (opcional)</span>' +
            '<input type="tel" name="mobil" autocomplete="tel" inputmode="tel"></label>' +
          '<div class="cbgb-dl-news"><label class="cbgb-dl-chk">' +
            '<input type="checkbox" name="news" checked>' +
            '<span>Sí, vull rebre el butlletí del club: novetats, portes obertes, campus i ' +
            'dies de partit. Un correu de tant en tant, i baixa quan vulguis.</span>' +
          '</label></div>' +
          '<label class="cbgb-dl-chk"><input type="checkbox" name="rgpd">' +
            '<span>Accepto que el CB Grup Barna guardi aquestes dades per contactar-me. ' +
            '<a href="/politica-de-privacitat/" target="_blank" rel="noopener">Política de privacitat</a>.</span>' +
          '</label>' +
          '<button class="go" type="submit">Descarregar el document</button>' +
          '<p class="cbgb-dl-err"></p>' +
        '</form>' +
        '<p class="cbgb-dl-peu">Les teves dades no es venen ni es cedeixen a ningú.</p>' +
      '</div>';
    document.body.appendChild(bg);

    var form = bg.querySelector('form');
    var err = bg.querySelector('.cbgb-dl-err');
    var btn = bg.querySelector('button.go');
    var previ = document.activeElement;

    function tanca() {
      bg.remove();
      document.removeEventListener('keydown', esc);
      if (previ && previ.focus) previ.focus();
    }
    function esc(e) { if (e.key === 'Escape') tanca(); }
    function crit(msg, camp) {
      err.textContent = msg; err.style.display = 'block';
      if (camp) camp.focus();
    }

    document.addEventListener('keydown', esc);
    bg.querySelector('button.x').onclick = tanca;
    bg.addEventListener('mousedown', function (e) { if (e.target === bg) tanca(); });
    setTimeout(function () { form.nom.focus(); }, 60);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var nom = form.nom.value.trim();
      var email = form.email.value.trim();
      var mobil = form.mobil.value.trim();
      var news = form.news.checked;

      if (!nom) return crit('Cal el teu nom.', form.nom);
      if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email)) return crit('Revisa el correu electrònic.', form.email);
      if (!form.rgpd.checked) return crit('Cal acceptar la política de privacitat per continuar.', form.rgpd);

      btn.disabled = true;
      btn.textContent = 'Un moment…';
      err.style.display = 'none';

      var parts = nom.split(/\s+/);
      var url = API_URL + '?action=register'
        + '&nom=' + enc(parts.shift())
        + '&cognom=' + enc(parts.join(' '))
        + '&email=' + enc(email)
        + '&mobil=' + enc(mobil)
        + '&newsletter=' + (news ? 'si' : 'no')
        + '&event=' + enc('descarrega-document')
        + '&font=' + enc('descarrega-pdf · doc:' + doc + ' · newsletter:' + (news ? 'si' : 'no')
                         + ' · pagina:' + location.pathname);

      var fet = false;
      function acaba() {
        if (fet) return;
        fet = true;
        try {
          localStorage.setItem(LS_KEY, JSON.stringify({
            nom: nom, email: email, mobil: mobil, news: news, data: new Date().toISOString().slice(0, 10)
          }));
        } catch (_) {}
        if (window.gtag) {
          window.gtag('event', 'generate_lead', { method: 'descarrega_document', document: doc });
          if (news) window.gtag('event', 'newsletter_signup', { document: doc });
        }
        tanca();
        doneFn();
      }

      // Si la xarxa triga o falla, la descàrrega no s'ha de quedar bloquejada.
      var ctrl = typeof AbortController === 'function' ? new AbortController() : null;
      var t = setTimeout(function () { if (ctrl) ctrl.abort(); acaba(); }, 8000);
      fetch(url, ctrl ? { signal: ctrl.signal, mode: 'no-cors' } : { mode: 'no-cors' })
        .catch(function () {})
        .then(function () { clearTimeout(t); acaba(); });
    });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[data-descarrega]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href) return;

    var ja = lead();
    if (ja && ja.email) {
      // Ja ens ha deixat les dades: registrem la descàrrega i prou.
      if (window.gtag) window.gtag('event', 'file_download', { document: a.getAttribute('data-descarrega') });
      return;
    }

    e.preventDefault();
    obre(a.getAttribute('data-descarrega'), href, function () {
      baixa(href, a.getAttribute('download') || '');
    });
  });
})();
