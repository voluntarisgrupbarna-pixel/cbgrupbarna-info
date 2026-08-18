/* CB Grup Barna · selector d'idioma global i persistent (CA/ES/EN)
   S'injecta sol si la pàgina no en té cap altre ja (evita duplicats amb
   pàgines que ja tenen un selector propi fet a mà). */
(function () {
  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  ready(function () {
    // Si la pàgina ja té un selector d'idioma funcional (link amb hreflang
    // o botó amb data-set d'idioma), no n'afegim un altre a sobre.
    if (document.querySelector('a[hreflang][href], button[data-set]')) return;

    function currentLang() {
      var p = location.pathname;
      if (p === '/es' || p.indexOf('/es/') === 0) return 'es';
      if (p === '/en' || p.indexOf('/en/') === 0) return 'en';
      return 'ca';
    }
    var lang = currentLang();

    function fallbackUrl(target) {
      var stripped = location.pathname.replace(/^\/(es|en)(\/|$)/, '/');
      return target === 'ca' ? stripped : '/' + target + stripped;
    }
    var urls = { ca: fallbackUrl('ca'), es: fallbackUrl('es'), en: fallbackUrl('en') };

    var css =
      '.cbgb-lang-pill{position:fixed;top:50%;right:0;transform:translateY(-50%);' +
      'z-index:2000;display:flex;flex-direction:column;' +
      'background:rgba(16,16,14,.92);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);' +
      'border:1px solid rgba(255,255,255,.22);border-right:none;' +
      'border-radius:8px 0 0 8px;overflow:hidden;box-shadow:-2px 2px 14px rgba(0,0,0,.35)}' +
      '.cbgb-lang-pill a{display:flex;align-items:center;justify-content:center;' +
      'width:34px;height:34px;color:#F4F1EC;font-family:Inter,system-ui,-apple-system,sans-serif;' +
      'font-size:11px;font-weight:600;letter-spacing:.04em;text-decoration:none}' +
      '.cbgb-lang-pill a.active{background:#E20613;color:#fff}' +
      '.cbgb-lang-pill a:not(.active):hover{background:rgba(255,255,255,.16)}' +
      '.cbgb-lang-pill a:focus-visible{outline:2px solid #fff;outline-offset:-2px}' +
      '@media(max-width:420px){.cbgb-lang-pill a{width:30px;height:30px;font-size:10px}}';
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var nav = document.createElement('nav');
    nav.className = 'cbgb-lang-pill';
    nav.setAttribute('aria-label', "Canvia d'idioma · Cambiar idioma · Change language");
    ['ca', 'es', 'en'].forEach(function (l) {
      var a = document.createElement('a');
      a.href = urls[l];
      a.textContent = l.toUpperCase();
      a.setAttribute('hreflang', l);
      a.setAttribute('lang', l);
      if (l === lang) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'true');
      }
      nav.appendChild(a);
    });
    document.body.appendChild(nav);
  });
})();
