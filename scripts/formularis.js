/* CB GRUP BARNA · ENVIAMENT DE FORMULARIS
 * ---------------------------------------------------------------------------
 * Tots els formularis de la web passen per aquí i acaben al mateix full de
 * càlcul, cadascun a la seva pestanya. La URL del desplegament s'escriu UNA
 * vegada, aquí baix, i no s'ha de repetir a cap pàgina.
 *
 * Mentre ENDPOINT estigui buit no s'envia res i cap pàgina falla: cada
 * formulari continua fent el que feia abans.
 *
 * Ús:
 *   CBGBForms.envia('informacio', { nom:…, mobil:…, correu:… })
 *     → torna una promesa amb true si el full ho ha desat, false si no.
 *
 * Si l'enviament falla (sense cobertura, Google caigut), el contacte NO es
 * perd: queda a la cua del navegador i es torna a provar en obrir qualsevol
 * pàgina de la web.
 * --------------------------------------------------------------------------- */
(function (global) {
  'use strict';

  // ── Enganxa aquí la URL que acaba en /exec del desplegament d'Apps Script ──
  var ENDPOINT = '';

  var CUA = 'cbgb_forms_pendents';
  var MAX_CUA = 20;
  var TEMPS_MAX = 12000;

  var obertaA = Date.now();

  function pendents() {
    try { return JSON.parse(localStorage.getItem(CUA) || '[]'); } catch (e) { return []; }
  }

  function desaPendents(llista) {
    try { localStorage.setItem(CUA, JSON.stringify(llista.slice(-MAX_CUA))); } catch (e) {}
  }

  function encua(payload) {
    var llista = pendents();
    llista.push(payload);
    desaPendents(llista);
  }

  /**
   * Un POST sense capçaleres pròpies: així el navegador no fa la petició
   * prèvia de CORS que Apps Script no sap respondre, i la resposta es pot
   * llegir de debò. Amb mode:'no-cors' s'enviaria a cegues i no sabríem mai
   * si el contacte s'ha desat, que és el que passava fins ara.
   */
  function crida(payload) {
    var control = new AbortController();
    var rellotge = setTimeout(function () { control.abort(); }, TEMPS_MAX);

    return fetch(ENDPOINT, {
      method: 'POST',
      body: JSON.stringify(payload),
      signal: control.signal,
      keepalive: true
    })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (dades) { return !!(dades && dades.ok); })
      .catch(function () { return false; })
      .then(function (b) { clearTimeout(rellotge); return b; });
  }

  function envia(tipus, dades) {
    var payload = {
      tipus: tipus,
      nom: dades.nom || '',
      cognoms: dades.cognoms || '',
      mobil: dades.mobil || '',
      correu: dades.correu || '',
      club: dades.club || '',
      interes: dades.interes || '',
      missatge: dades.missatge || '',
      consentiment: !!dades.consentiment,
      font: dades.font || '',
      pagina: global.location ? global.location.pathname : '',
      web: dades.web || '',                 // trampa per a robots
      ms: Date.now() - obertaA              // temps que ha trigat a omplir-lo
    };

    if (!ENDPOINT) return Promise.resolve(false);

    return crida(payload).then(function (b) {
      if (!b) encua(payload);
      return b;
    });
  }

  /** En obrir qualsevol pàgina, torna a provar el que va quedar pendent. */
  function reintenta() {
    if (!ENDPOINT) return;
    var llista = pendents();
    if (!llista.length) return;
    desaPendents([]);
    llista.forEach(function (p) {
      crida(p).then(function (b) { if (!b) encua(p); });
    });
  }

  if (global.addEventListener) {
    global.addEventListener('load', function () { setTimeout(reintenta, 2500); });
  }

  global.CBGBForms = {
    envia: envia,
    actiu: function () { return !!ENDPOINT; },
    pendents: function () { return pendents().length; }
  };

})(window);
