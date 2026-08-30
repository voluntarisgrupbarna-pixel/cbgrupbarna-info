/* ============================================================
   CB GRUP BARNA · Consentiment de galetes
   ------------------------------------------------------------
   Aquest fitxer substitueix el <script> que carregava Google
   Analytics directament. Ara Analytics NO es descarrega fins que
   la persona ho accepta: mentre no hi hagi consentiment no surt
   ni una sola petició cap a Google.

   Com funciona:
   1. Defineix dataLayer i gtag() perquè els <script> de
      configuració que hi ha a cada pàgina no petin. Les crides
      queden encuades al dataLayer sense enviar-se enlloc.
   2. Si ja hi ha consentiment desat, injecta gtag.js i la cua
      s'envia de cop.
   3. Si no n'hi ha, ensenya la barra. En acceptar, injecta.
      En rebutjar, no injecta res i no torna a preguntar.

   La preferència es desa a localStorage, al navegador de la
   persona. El club no la rep ni la desa enlloc.

   Per reobrir el panell: window.CBGB_GALETES.obrir()
   ============================================================ */
(function () {
  'use strict';

  var GA_ID = 'G-R6XYR7G1WF';
  var CLAU = 'cbgb_galetes';      // 'accepta' | 'rebutja'
  var VERSIO = '1';               // puja-la si canvien les finalitats
  var CLAU_V = 'cbgb_galetes_v';

  // ── 1. Cua: que gtag() existeixi encara que Analytics no hi sigui ──
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== 'function') {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }

  function llegir() {
    try {
      if (localStorage.getItem(CLAU_V) !== VERSIO) return null;
      return localStorage.getItem(CLAU);
    } catch (e) { return null; }
  }
  function desar(valor) {
    try {
      localStorage.setItem(CLAU, valor);
      localStorage.setItem(CLAU_V, VERSIO);
    } catch (e) {}
  }

  // ── 2. Injecció d'Analytics, només amb consentiment ──
  //
  // Compte amb una trampa: carregar gtag.js NO envia cap visita per si sol.
  // Qui la dispara és la crida gtag('config', GA_ID). Les pàgines fetes a mà
  // ja la porten inline, però les que genera scripts/build-pages.py (tot el
  // blog, els partners, els equips…) només carreguen aquest fitxer. Sense la
  // línia de sota, aquelles pàgines injectaven gtag.js i no comptaven ni una
  // sola visita. Per això la fem aquí, i només si la pàgina no l'ha feta ja
  // (si no, comptaríem la visita dues vegades).
  function jaConfigurat() {
    var dl = window.dataLayer || [];
    for (var i = 0; i < dl.length; i++) {
      var c = dl[i];
      if (c && c[0] === 'config' && c[1] === GA_ID) return true;
    }
    return false;
  }

  var injectat = false;
  function activarAnalytics() {
    if (injectat) return;
    injectat = true;
    if (!jaConfigurat()) {
      window.gtag('js', new Date());
      window.gtag('config', GA_ID, { anonymize_ip: true });
    }
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  // ── 3. La barra ──
  var CSS = [
    '.cbgb-gal{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;',
    'background:#10100E;color:#fff;border-top:2px solid #E20613;',
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;",
    'font-size:14px;line-height:1.6;font-weight:300;',
    'padding:18px clamp(16px,4vw,40px);padding-bottom:calc(18px + env(safe-area-inset-bottom));',
    'box-shadow:0 -8px 40px rgba(0,0,0,.35);animation:cbgbGalUp .35s cubic-bezier(.22,1,.36,1)}',
    '@keyframes cbgbGalUp{from{transform:translateY(100%)}to{transform:translateY(0)}}',
    '.cbgb-gal-in{max-width:1180px;margin:0 auto;display:flex;gap:clamp(14px,3vw,32px);',
    'align-items:center;justify-content:space-between;flex-wrap:wrap}',
    '.cbgb-gal-t{flex:1 1 340px;min-width:0}',
    '.cbgb-gal-t b{display:block;font-family:\'Anton\',\'Futura\',sans-serif;font-weight:400;',
    'font-size:11.5px;letter-spacing:.3em;text-transform:uppercase;color:#FF3B41;margin-bottom:7px}',
    '.cbgb-gal-t p{margin:0;color:rgba(255,255,255,.82)}',
    '.cbgb-gal-t a{color:#fff;border-bottom:1px solid #FF3B41;text-decoration:none}',
    '.cbgb-gal-t a:hover{color:#FF3B41}',
    '.cbgb-gal-b{display:flex;gap:10px;flex-wrap:wrap;flex-shrink:0}',
    '.cbgb-gal-b button{font-family:\'Anton\',\'Futura\',sans-serif;font-size:11.5px;letter-spacing:.24em;',
    'text-transform:uppercase;padding:13px 22px;min-height:46px;border:1px solid #fff;cursor:pointer;',
    'background:transparent;color:#fff;transition:background .3s,border-color .3s,color .3s}',
    '.cbgb-gal-b button:hover{background:#fff;color:#10100E}',
    '.cbgb-gal-b button.si{background:#E20613;border-color:#E20613}',
    '.cbgb-gal-b button.si:hover{background:#fff;border-color:#fff;color:#10100E}',
    '@media(max-width:620px){.cbgb-gal{padding:14px 16px;padding-bottom:calc(14px + env(safe-area-inset-bottom))}',
    '.cbgb-gal-in{gap:12px}.cbgb-gal-t p{font-size:12.5px}',
    '.cbgb-gal-b{width:100%}.cbgb-gal-b button{flex:1 1 0;min-width:0;padding:12px 10px;min-height:42px}}',
    // A 320 px la barra feia 342 px d'ample i el boto d'acceptar quedava
    // partit fora de la pantalla: els botons son flex:1 1 0 pero el seu
    // contingut (majuscules amb .24em d'interlletratge) no encongeix, i sense
    // min-width:0 un fill flexible no baixa de l'amplada del seu text. Aquest
    // avis es la primera cosa que es toca en entrar; no pot sortir tallat.
    '@media(max-width:380px){.cbgb-gal{padding:12px 12px;padding-bottom:calc(12px + env(safe-area-inset-bottom))}',
    '.cbgb-gal-b{gap:8px}',
    '.cbgb-gal-b button{font-size:11px;letter-spacing:.12em;padding:12px 6px;hyphens:auto}}',
    '@media(prefers-reduced-motion:reduce){.cbgb-gal{animation:none}}'
  ].join('');

  var barra = null;

  // L'avís de galetes és el primer que llegeix qui entra al lloc, i fins ara
  // sortia sempre en català encara que la pàgina fos en castellà o en anglès.
  // Al club hi ha famílies de mig món i sèniors que només parlen anglès: un
  // consentiment que no s'entén no és consentiment.
  var TEXTOS = {
    ca: {
      aria: 'Consentiment de galetes', titol: 'Galetes', mes: 'Més informació',
      text: 'Fem servir Google Analytics per saber quines pàgines interessen més, sense galetes de publicitat.',
      nomes: 'Només les necessàries', accepta: 'Accepta-les',
      enllac: '/politica-de-privacitat/#galetes'
    },
    es: {
      aria: 'Consentimiento de cookies', titol: 'Cookies', mes: 'Más información',
      text: 'Usamos Google Analytics para saber qué páginas interesan más, sin cookies de publicidad.',
      nomes: 'Solo las necesarias', accepta: 'Aceptarlas',
      enllac: '/es/politica-de-privacidad/#galetes'
    },
    en: {
      aria: 'Cookie consent', titol: 'Cookies', mes: 'More information',
      text: 'We use Google Analytics to see which pages people read most. No advertising cookies.',
      nomes: 'Only the necessary ones', accepta: 'Accept them',
      enllac: '/en/privacy-policy/#galetes'
    }
  };

  // Cada idioma enllaça la seva política de privacitat: llegir com es
  // tracten les teves dades en una llengua que no entens no és informar-te.
  function textos() {
    var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
    return TEXTOS[codi] || TEXTOS.ca;
  }

  // En tancar la barra, el focus tornaria al <body> i qui navega amb teclat
  // es quedaria al principi de tot. El portem al contingut de la pàgina, que
  // és on la persona anava.
  function tancar() {
    if (!barra) return;
    var teniaFocus = barra.contains(document.activeElement);
    barra.remove();
    barra = null;
    document.body.classList.remove('cbgb-gal-obert');
    document.removeEventListener('keydown', escapa);
    if (teniaFocus) {
      var desti = document.getElementById('contingut') || document.querySelector('main');
      if (desti) {
        if (!desti.hasAttribute('tabindex')) desti.setAttribute('tabindex', '-1');
        desti.focus();
      }
    }
  }

  // Escape val com a «només les necessàries», mai com a acceptació. Tancar
  // un avís no és consentir-hi.
  function escapa(e) {
    if (e.key === 'Escape' && barra) { desar('rebutja'); tancar(); }
  }

  function pintar() {
    if (barra) return;
    var est = document.createElement('style');
    est.textContent = CSS;
    document.head.appendChild(est);

    var t = textos();
    barra = document.createElement('div');
    barra.className = 'cbgb-gal';
    barra.setAttribute('role', 'dialog');
    barra.setAttribute('aria-label', t.aria);
    barra.innerHTML =
      '<div class="cbgb-gal-in">' +
        '<div class="cbgb-gal-t">' +
          '<b>' + t.titol + '</b>' +
          '<p>' + t.text + ' ' +
          '<a href="' + t.enllac + '" data-cbgb-mes="1">' + t.mes + '</a>.</p>' +
        '</div>' +
        '<div class="cbgb-gal-b">' +
          '<button type="button" data-cbgb="no">' + t.nomes + '</button>' +
          '<button type="button" class="si" data-cbgb="si">' + t.accepta + '</button>' +
        '</div>' +
      '</div>';

    barra.querySelector('[data-cbgb="si"]').addEventListener('click', function () {
      desar('accepta'); activarAnalytics(); tancar();
    });
    barra.querySelector('[data-cbgb="no"]').addEventListener('click', function () {
      desar('rebutja'); tancar();
    });

    document.body.appendChild(barra);
    // La pestanya d'admin viu a baix a la dreta, just on hi ha els botons de
    // consentiment. No es pot amagar (ha de ser sempre visible) ni pot tapar
    // un boto de consentiment: se li publica l'alcada de la barra perque
    // pugui pujar per sobre mentre la barra hi sigui.
    document.documentElement.style.setProperty('--cbgb-gal-h', barra.offsetHeight + 'px');
    document.body.classList.add('cbgb-gal-obert');
    document.addEventListener('keydown', escapa);
    barra.querySelector('[data-cbgb="si"]').focus();
  }

  // ── 4. Arrencada ──
  var decisio = llegir();
  if (decisio === 'accepta') {
    activarAnalytics();
  } else if (decisio !== 'rebutja') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', pintar);
    } else {
      pintar();
    }
  }

  // ── 5. API per reobrir el panell des del peu ──
  window.CBGB_GALETES = {
    obrir: function () {
      // Si la barra ja hi és, no s'esborra res: abans es netejava el
      // consentiment desat i tot seguit pintar() sortia de seguida perquè
      // la barra existia, així que la decisió desapareixia sense que la
      // persona veiés cap panell nou.
      if (barra) { barra.querySelector('[data-cbgb="si"]').focus(); return; }
      try { localStorage.removeItem(CLAU); localStorage.removeItem(CLAU_V); } catch (e) {}
      pintar();
    },
    estat: function () { return llegir() || 'sense decidir'; }
  };

  // Qualsevol enllaç cap a #galetes reobre el panell sense sortir de la pàgina
  // Les tres polítiques de privacitat tenen una secció #galetes de veritat.
  // Abans només s'excloïa la catalana, i per tant a /es/politica-de-privacidad/
  // i a /en/privacy-policy/ l'àncora de la pàgina quedava segrestada: en lloc
  // de baixar fins a la secció, reobria el panell.
  var POLITIQUES = [
    '/politica-de-privacitat/',
    '/es/politica-de-privacidad/',
    '/en/privacy-policy/'
  ];

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$="#galetes"]');
    if (!a) return;
    // L'enllaç «Més informació» del propi avís ha de portar a la política.
    // Amb el gestor genèric no anava enlloc: es cancel·lava la navegació i
    // es tornava a obrir un panell que ja era obert.
    if (a.hasAttribute('data-cbgb-mes')) return;
    if (POLITIQUES.indexOf(location.pathname) !== -1) return; // allà és una àncora real
    e.preventDefault();
    window.CBGB_GALETES.obrir();
  });

  // ── 6. Accés ràpid al panell d'admin ──
  // Aquest fitxer es carrega a gairebé totes les pàgines (és el punt d'entrada
  // més universal que hi ha, sense build step), per això s'hi enganxa aquesta
  // pestanya discreta cap a /admin/ en lloc d'haver de tocar cada HTML.
  // L'enllaç només hi és visible; l'accés real el segueix controlant el login
  // de Google d'admin/auth.js.
  function pintarAdmin() {
    if (location.pathname.indexOf('/admin/') === 0) return; // ja hi som
    // Les portades porten l'enllaç «Admin» dins de la capçalera, a dalt a la
    // dreta. Alla no cal la pestanya flotant: seria el mateix enllac dos cops.
    if (document.querySelector('.head-admin')) return;
    var est = document.createElement('style');
    // A baix a la dreta, no a dalt. A dalt queia sobre el ticker de novetats,
    // que es del mateix negre que la pestanya: negre sobre negre, invisible.
    // A baix el fons es blanc i s'hi llegeix. El boto de WhatsApp va a l'altre
    // costat, aixi que aqui no tapa res.
    est.textContent = '.cbgb-admin-tab{position:fixed;bottom:14px;right:14px;' +
      "z-index:2147483000;font-family:'Anton','Futura',sans-serif;font-weight:400;" +
      'font-size:11.5px;letter-spacing:.2em;text-transform:uppercase;color:#fff;' +
      'background:#10100E;border:1px solid rgba(255,255,255,.25);border-radius:999px;' +
      'padding:0 16px;min-height:44px;display:inline-flex;align-items:center;' +
      'text-decoration:none;opacity:.62;transition:opacity .25s}' +
      '.cbgb-admin-tab:hover,.cbgb-admin-tab:focus-visible{opacity:1;border-color:#E20613}' +
      /* Es veu SEMPRE, també a mòbil: decisió de l'Ana. S'amagava perquè, quan
         estava a dalt, tapava el commutador d'idioma; ara que és a baix a la
         dreta ja no tapa res. El WhatsApp va a l'altre costat. */
      'body.cbgb-gal-obert .cbgb-admin-tab{bottom:calc(var(--cbgb-gal-h,0px) + 12px)}' +
      '@media(max-width:900px){.cbgb-admin-tab{bottom:12px;right:12px;padding:0 15px}' +
      'body.cbgb-gal-obert .cbgb-admin-tab{bottom:calc(var(--cbgb-gal-h,0px) + 10px)}}';
    document.head.appendChild(est);
    var link = document.createElement('a');
    link.href = '/admin/';
    link.className = 'cbgb-admin-tab';
    link.textContent = 'Admin';
    document.body.appendChild(link);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pintarAdmin);
  } else {
    pintarAdmin();
  }
})();
