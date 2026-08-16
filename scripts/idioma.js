/* CB GRUP BARNA · IDIOMA
 * ---------------------------------------------------------------------------
 * Dues coses:
 *
 *  1. Tria l'idioma per defecte segons d'on es connecta qui entra:
 *     Catalunya → català · resta d'Espanya → castellà · resta del món → anglès.
 *
 *  2. Pinta el selector CA · ES · EN, sempre visible, per canviar quan es vulgui.
 *     La tria manual mana per damunt de tot i es recorda.
 *
 * REGLA DE SEGURETAT: només es redirigeix cap a una pàgina que EXISTEIX. El
 * mapa del que hi ha en cada idioma és a idiomes.js, generat des del disc per
 * scripts/generate-idiomes.py. Avui la portada i 72 pàgines més només són en
 * català: allà no es mou ningú, i el selector ho diu clar en comptes de deixar
 * un enllaç trencat.
 * --------------------------------------------------------------------------- */
(function (global) {
  'use strict';

  var doc = global.document;
  if (!doc) return;

  // ── Configuració ──────────────────────────────────────────────────────────

  /** 'territori' = la regla d'aquí dalt (fa servir el país/regió de connexió).
   *  'idioma'     = mana l'idioma que la persona té posat al mòbil o al navegador.
   *  Amb 'territori', qui té el mòbil en castellà i es connecta des del Clot
   *  veu la web en català; amb 'idioma', la veu en castellà. */
  var MANA = 'territori';

  /** Servei que diu el país i la regió. Només es consulta si cal decidir de
   *  debò (vegeu més avall): la immensa majoria de visites no el criden mai. */
  var GEO_URL = 'https://ipapi.co/json/';
  var GEO_MS = 3500;
  var GEO_DIES = 30;

  var NOMS = { ca: 'Català', es: 'Español', en: 'English' };
  var CURT = { ca: 'CA', es: 'ES', en: 'EN' };
  var ORDRE = ['ca', 'es', 'en'];

  var K_IDIOMA = 'cbgb-idioma';
  var K_GEO = 'cbgb-territori';
  var K_SESSIO = 'cbgb-idioma-fet';

  var TEXTOS = {
    ca: { etiqueta: 'Idioma', nomes: 'Aquesta pàgina encara només és en català. Ho recordem per a la resta del web.' },
    es: { etiqueta: 'Idioma', nomes: 'Esta página todavía solo está en catalán. Lo recordamos para el resto de la web.' },
    en: { etiqueta: 'Language', nomes: 'This page is only in Catalan for now. We will remember your choice for the rest of the site.' }
  };

  // ── Memòria ───────────────────────────────────────────────────────────────

  function llegeix(k) { try { return global.localStorage.getItem(k); } catch (e) { return null; } }
  function escriu(k, v) { try { global.localStorage.setItem(k, v); } catch (e) {} }

  function triaDesada() {
    var v = llegeix(K_IDIOMA);
    return ORDRE.indexOf(v) > -1 ? v : null;
  }

  function territoriDesat() {
    try {
      var v = JSON.parse(llegeix(K_GEO) || 'null');
      if (v && v.quan && (Date.now() - v.quan) < GEO_DIES * 864e5) return v;
    } catch (e) {}
    return null;
  }

  // ── Qui ets ───────────────────────────────────────────────────────────────

  /** L'idioma del navegador, si és un dels tres. */
  function delNavegador() {
    var llista = global.navigator.languages || [global.navigator.language || ''];
    for (var i = 0; i < llista.length; i++) {
      var l = String(llista[i]).toLowerCase();
      if (l.indexOf('ca') === 0) return 'ca';
      if (l.indexOf('es') === 0) return 'es';
      if (l.indexOf('en') === 0) return 'en';
    }
    return null;
  }

  /** Catalunya és ES-CT. S'accepten variants perquè no tots els serveis
   *  escriuen el codi igual. */
  function esCatalunya(t) {
    if (!t) return false;
    var codi = String(t.regio || '').toUpperCase().replace(/[^A-Z]/g, '');
    if (codi === 'CT' || codi === 'ESCT' || codi === 'CAT') return true;
    return /catalu/i.test(String(t.nom || ''));
  }

  function perTerritori(t, nav) {
    if (!t || !t.pais) return nav || 'en';        // sense territori, l'idioma del mòbil
    if (String(t.pais).toUpperCase() !== 'ES') return 'en';
    return esCatalunya(t) ? 'ca' : 'es';
  }

  function demanaTerritori(cb) {
    var desat = territoriDesat();
    if (desat) return cb(desat);
    if (!global.fetch) return cb(null);

    var control = typeof AbortController === 'function' ? new AbortController() : null;
    var rellotge = setTimeout(function () { if (control) control.abort(); }, GEO_MS);

    global.fetch(GEO_URL, control ? { signal: control.signal } : undefined)
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        clearTimeout(rellotge);
        if (!d) return cb(null);
        var t = { pais: d.country_code || d.country, regio: d.region_code, nom: d.region, quan: Date.now() };
        escriu(K_GEO, JSON.stringify(t));
        cb(t);
      })
      .catch(function () { clearTimeout(rellotge); cb(null); });
  }

  // ── El mapa de traduccions ────────────────────────────────────────────────

  function ruta() {
    var p = global.location.pathname.replace(/index\.html$/, '');
    return p.charAt(p.length - 1) === '/' ? p : p + '/';
  }

  /** El grup de la pàgina actual: { ca:…, es:…, en:… }. Si no és a cap grup,
   *  la pàgina existeix només en un idioma. */
  function grupActual() {
    var grups = global.CBGB_IDIOMES || [];
    var aqui = ruta();
    for (var i = 0; i < grups.length; i++) {
      for (var k in grups[i]) {
        if (grups[i][k] === aqui) return grups[i];
      }
    }
    return null;
  }

  function idiomaDeLaPagina() {
    var l = (doc.documentElement.getAttribute('lang') || 'ca').toLowerCase().slice(0, 2);
    return ORDRE.indexOf(l) > -1 ? l : 'ca';
  }

  // ── Decidir ───────────────────────────────────────────────────────────────

  function decideix(cb) {
    // Una tria explícita a l'adreça mana i es recorda: serveix per compartir
    // un enllaç ja en un idioma i per provar-ho sense esborrar res.
    var url = new URLSearchParams(global.location.search);
    var forcat = url.get('lang');
    if (ORDRE.indexOf(forcat) > -1) { escriu(K_IDIOMA, forcat); return cb(forcat, 'adreça'); }

    var desat = triaDesada();
    if (desat) return cb(desat, 'tria desada');

    var nav = delNavegador();
    if (MANA !== 'territori') return cb(nav || 'en', 'idioma del navegador');

    demanaTerritori(function (t) { cb(perTerritori(t, nav), t ? 'territori' : 'idioma del navegador'); });
  }

  // ── Redirigir, només si hi ha on ─────────────────────────────────────────

  /**
   * Només es mou ningú que arribi a l'adreça per defecte (la catalana). Qui
   * obre directament una adreça /es/ o /en/ —perquè li han passat l'enllaç,
   * perquè el tenia desat o perquè és un cercador indexant— es queda on és.
   * Sense això, un enllaç en castellà compartit amb algú de Barcelona
   * l'expulsava al català, i els cercadors no podien veure mai més d'una
   * versió de cada pàgina.
   */
  function potRedirigir(grup) {
    if (new URLSearchParams(global.location.search).has('lang')) return false;
    if (grup.ca !== ruta()) return false;
    try { if (global.sessionStorage.getItem(K_SESSIO)) return false; } catch (e) {}
    return true;
  }

  function marcaFet() {
    try { global.sessionStorage.setItem(K_SESSIO, '1'); } catch (e) {}
  }

  // ── El selector ───────────────────────────────────────────────────────────

  var CSS =
    '.cbgb-idi{display:inline-flex;align-items:center;gap:2px;flex-shrink:0}' +
    '.cbgb-idi button{font:inherit;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;' +
    'background:none;border:0;padding:8px 6px;min-height:34px;color:inherit;cursor:pointer;opacity:.5;' +
    'transition:opacity .25s}' +
    '.cbgb-idi button:hover{opacity:1}' +
    '.cbgb-idi button[aria-current]{opacity:1;font-weight:600;box-shadow:inset 0 -1px 0 currentColor}' +
    '.cbgb-idi button.buit{opacity:.28}' +
    '.cbgb-idi button:focus-visible{outline:2px solid currentColor;outline-offset:2px;opacity:1}' +
    '.cbgb-idi .sep{opacity:.3;font-size:9px;user-select:none}' +
    '.cbgb-idi-nota{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2000;' +
    'max-width:min(92vw,420px);background:#10100E;color:#fff;padding:14px 18px;font-size:13px;' +
    'line-height:1.5;box-shadow:0 12px 40px rgba(0,0,0,.3)}';

  function estils() {
    if (doc.getElementById('cbgb-idi-css')) return;
    var s = doc.createElement('style');
    s.id = 'cbgb-idi-css';
    s.textContent = CSS;
    doc.head.appendChild(s);
  }

  function nota(text) {
    var vella = doc.querySelector('.cbgb-idi-nota');
    if (vella) vella.remove();
    var d = doc.createElement('div');
    d.className = 'cbgb-idi-nota';
    d.setAttribute('role', 'status');
    d.textContent = text;
    doc.body.appendChild(d);
    setTimeout(function () { d.remove(); }, 5200);
  }

  /** On va el selector: primer un lloc reservat a mà, després el costat dret
   *  de la capçalera del web, i si no n'hi ha cap, al final de la pàgina. */
  function onVa() {
    return doc.querySelector('[data-idioma]')
        || doc.querySelector('.head-side.r')
        || doc.querySelector('.head-nav')
        || doc.body;
  }

  function pinta(actiu) {
    estils();
    var grup = grupActual();
    var t = TEXTOS[actiu] || TEXTOS.ca;

    var nav = doc.createElement('nav');
    nav.className = 'cbgb-idi';
    nav.setAttribute('aria-label', t.etiqueta);

    ORDRE.forEach(function (codi, i) {
      if (i) {
        var sep = doc.createElement('span');
        sep.className = 'sep';
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '·';
        nav.appendChild(sep);
      }
      var desti = grup && grup[codi];
      var b = doc.createElement('button');
      b.type = 'button';
      b.textContent = CURT[codi];
      b.lang = codi;
      if (codi === actiu) b.setAttribute('aria-current', 'true');
      if (!desti && codi !== actiu) {
        b.className = 'buit';
        b.title = t.nomes;
      }
      b.setAttribute('aria-label', NOMS[codi] + (!desti && codi !== actiu ? ' — ' + t.nomes : ''));
      b.addEventListener('click', function () {
        escriu(K_IDIOMA, codi);
        if (desti && desti !== ruta()) { global.location.href = desti; return; }
        if (!desti) nota((TEXTOS[codi] || t).nomes);
        pintaDeNou(codi);
      });
      nav.appendChild(b);
    });

    var lloc = onVa();
    var anterior = doc.querySelector('.cbgb-idi');
    if (anterior) anterior.replaceWith(nav);
    else lloc.appendChild(nav);
  }

  function pintaDeNou(codi) {
    var n = doc.querySelector('.cbgb-idi');
    if (n) n.remove();
    pinta(codi);
  }

  // ── Engegada ──────────────────────────────────────────────────────────────

  function arrenca() {
    var grup = grupActual();
    var aqui = idiomaDeLaPagina();

    // Si la pàgina no té germanes, no hi ha res a decidir ni cap redirecció
    // possible: només cal el selector, que recordarà la tria per a la resta.
    if (!grup) { pinta(triaDesada() || aqui); return; }

    decideix(function (idioma) {
      var desti = grup[idioma];
      if (potRedirigir(grup) && desti && desti !== ruta()) {
        // La tria queda desada: a partir d'ara mana com si l'haguessin fet a
        // mà, i per tant no cal tornar a mirar d'on es connecta ningú.
        escriu(K_IDIOMA, idioma);
        marcaFet();
        global.location.replace(desti + global.location.hash);
        return;
      }
      pinta(grup[aqui] ? aqui : idioma);
    });
  }

  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', arrenca);
  else arrenca();

  global.CBGBIdioma = {
    actual: function () { return triaDesada() || idiomaDeLaPagina(); },
    posa: function (c) { if (ORDRE.indexOf(c) > -1) { escriu(K_IDIOMA, c); pintaDeNou(c); } },
    grup: grupActual
  };

})(window);
