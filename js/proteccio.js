/* CB Grup Barna · Canal de protecció del menor (LOPIVI)
   Comportament segur per defecte: si no hi ha un endpoint PROPI
   configurat a /js/canals.js, el formulari NO es mostra i es deixa
   el correu de la Delegada de Protecció, que és un canal vàlid.
   Mai s'envia per l'endpoint compartit amb la resta del web. */
(function () {
  var cfg      = window.CANALS || {};
  var wrap     = document.getElementById('pm-wrap');
  var fallback = document.getElementById('pm-fallback');
  if (!wrap || !fallback) return;

  var endpoint = cfg.proteccioEndpoint;
  if (!endpoint) return;                       // es queda el correu de la Delegada
  if (endpoint === cfg.bustiaEndpoint) {       // xarxa de seguretat: mai el compartit
    if (window.console) console.warn(
      'canals.js: proteccioEndpoint no pot ser el mateix que bustiaEndpoint. ' +
      'El formulari de protecció es manté desactivat.');
    return;
  }

  wrap.hidden = false;
  fallback.hidden = true;

  var form = document.getElementById('pm-form');
  var what = document.getElementById('pm-what');
  var wErr = document.getElementById('pm-what-err');
  var done = document.getElementById('pm-done');

  what.addEventListener('input', function () {
    if (wErr.classList.contains('on')) {
      var mal = !what.value.trim();
      wErr.classList.toggle('on', mal);
      what.setAttribute('aria-invalid', mal ? 'true' : 'false');
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!what.value.trim()) {
      wErr.classList.add('on');
      what.setAttribute('aria-invalid', 'true');
      what.focus();
      return;
    }
    form.querySelector('button[type="submit"]').disabled = true;
    var acabat = function () {
      form.classList.add('sent');
      done.classList.add('on');
      done.setAttribute('tabindex', '-1');
      done.focus();
    };
    fetch(endpoint, {
      method: 'POST', mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        que:       what.value.trim(),
        quan:      document.getElementById('pm-when').value.trim(),
        qui:       document.getElementById('pm-who').value.trim(),
        rol:       document.getElementById('pm-role').value,
        contacte:  document.getElementById('pm-contact').value.trim(),
        source:    'proteccio-menor',
        idioma:    document.documentElement.lang
      })
    }).then(acabat, acabat);
  });
})();
