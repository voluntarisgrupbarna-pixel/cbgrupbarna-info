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
  var injectat = false;
  function activarAnalytics() {
    if (injectat) return;
    injectat = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  // ── 3. La barra ──
  var CSS = [
    '.cbgb-gal{position:fixed;left:0;right:0;bottom:0;z-index:2147483000;',
    'background:#0a0a0a;color:#fff;border-top:2px solid #E20613;',
    "font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;",
    'font-size:14px;line-height:1.6;font-weight:300;',
    'padding:18px clamp(16px,4vw,40px);padding-bottom:calc(18px + env(safe-area-inset-bottom));',
    'box-shadow:0 -8px 40px rgba(0,0,0,.35);animation:cbgbGalUp .35s cubic-bezier(.22,1,.36,1)}',
    '@keyframes cbgbGalUp{from{transform:translateY(100%)}to{transform:translateY(0)}}',
    '.cbgb-gal-in{max-width:1180px;margin:0 auto;display:flex;gap:clamp(14px,3vw,32px);',
    'align-items:center;justify-content:space-between;flex-wrap:wrap}',
    '.cbgb-gal-t{flex:1 1 340px;min-width:0}',
    '.cbgb-gal-t b{display:block;font-family:\'Jost\',\'Futura\',sans-serif;font-weight:400;',
    'font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:#E20613;margin-bottom:7px}',
    '.cbgb-gal-t p{margin:0;color:rgba(255,255,255,.82)}',
    '.cbgb-gal-t a{color:#fff;border-bottom:1px solid #E20613;text-decoration:none}',
    '.cbgb-gal-t a:hover{color:#E20613}',
    '.cbgb-gal-b{display:flex;gap:10px;flex-wrap:wrap;flex-shrink:0}',
    '.cbgb-gal-b button{font-family:\'Jost\',\'Futura\',sans-serif;font-size:10px;letter-spacing:.24em;',
    'text-transform:uppercase;padding:13px 22px;min-height:46px;border:1px solid #fff;cursor:pointer;',
    'background:transparent;color:#fff;transition:background .3s,border-color .3s,color .3s}',
    '.cbgb-gal-b button:hover{background:#fff;color:#0a0a0a}',
    '.cbgb-gal-b button.si{background:#E20613;border-color:#E20613}',
    '.cbgb-gal-b button.si:hover{background:#fff;border-color:#fff;color:#0a0a0a}',
    '@media(max-width:620px){.cbgb-gal{padding:14px 16px;padding-bottom:calc(14px + env(safe-area-inset-bottom))}',
    '.cbgb-gal-in{gap:12px}.cbgb-gal-t p{font-size:12.5px}',
    '.cbgb-gal-b{width:100%}.cbgb-gal-b button{flex:1 1 0;padding:12px 10px;min-height:42px}}',
    '@media(prefers-reduced-motion:reduce){.cbgb-gal{animation:none}}'
  ].join('');

  var barra = null;

  function tancar() {
    if (!barra) return;
    barra.remove();
    barra = null;
  }

  function pintar() {
    if (barra) return;
    var est = document.createElement('style');
    est.textContent = CSS;
    document.head.appendChild(est);

    barra = document.createElement('div');
    barra.className = 'cbgb-gal';
    barra.setAttribute('role', 'dialog');
    barra.setAttribute('aria-live', 'polite');
    barra.setAttribute('aria-label', 'Consentiment de galetes');
    barra.innerHTML =
      '<div class="cbgb-gal-in">' +
        '<div class="cbgb-gal-t">' +
          '<b>Galetes</b>' +
          '<p>Fem servir Google Analytics per saber quines pàgines interessen més, sense galetes de publicitat. ' +
          '<a href="/politica-de-privacitat/#galetes">Més informació</a>.</p>' +
        '</div>' +
        '<div class="cbgb-gal-b">' +
          '<button type="button" data-cbgb="no">Només les necessàries</button>' +
          '<button type="button" class="si" data-cbgb="si">Accepta-les</button>' +
        '</div>' +
      '</div>';

    barra.querySelector('[data-cbgb="si"]').addEventListener('click', function () {
      desar('accepta'); activarAnalytics(); tancar();
    });
    barra.querySelector('[data-cbgb="no"]').addEventListener('click', function () {
      desar('rebutja'); tancar();
    });

    document.body.appendChild(barra);
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
      try { localStorage.removeItem(CLAU); localStorage.removeItem(CLAU_V); } catch (e) {}
      pintar();
    },
    estat: function () { return llegir() || 'sense decidir'; }
  };

  // Qualsevol enllaç cap a #galetes reobre el panell sense sortir de la pàgina
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$="#galetes"]');
    if (!a) return;
    if (location.pathname === '/politica-de-privacitat/') return; // allà és una àncora real
    e.preventDefault();
    window.CBGB_GALETES.obrir();
  });
})();
