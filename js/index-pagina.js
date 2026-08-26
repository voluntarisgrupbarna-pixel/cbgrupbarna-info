/* Índex d'una pàgina llarga.
 *
 * L'Escoleta i el Campus fan 28.000 px d'alçada al mòbil: el contingut hi és
 * i és bo, però ningú hi arriba al final perquè no se sap què hi ha a sota.
 * Aquest fitxer llegeix els <h2> que ja hi ha i en fa una barra enganxada a
 * dalt, de manera que la pàgina digui de què va sencera sense haver-la de
 * recórrer.
 *
 * No toca el contingut: si un <h2> ja porta id, la fa servir; si no, en posa
 * una de derivada del text. Per això val per a qualsevol pàgina llarga i no
 * cal repetir cap marcatge als tres idiomes.
 *
 * S'activa sol quan la pàgina passa de 12.000 px i té quatre seccions o més:
 * en una pàgina curta, una barra d'índex només fa nosa.
 */
(function () {
  'use strict';

  var MIN_ALCADA = 12000;
  var MIN_SECCIONS = 4;

  var ETIQUETES = {
    ca: { titol: 'En aquesta pàgina', nav: 'Seccions d’aquesta pàgina' },
    es: { titol: 'En esta página', nav: 'Secciones de esta página' },
    en: { titol: 'On this page', nav: 'Sections on this page' }
  };

  function idioma() {
    var l = (document.documentElement.getAttribute('lang') || 'ca').slice(0, 2);
    return ETIQUETES[l] ? l : 'ca';
  }

  function textNet(h) {
    return (h.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function fesId(text, usades) {
    var base = text
      .toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .slice(0, 40) || 'seccio';
    var id = base, n = 2;
    while (document.getElementById(id) || usades[id]) { id = base + '-' + n; n++; }
    usades[id] = true;
    return id;
  }

  function alcadaCapcalera() {
    var caps = document.querySelectorAll('header, .head, .langbar, .site-header');
    var max = 0;
    for (var i = 0; i < caps.length; i++) {
      var el = caps[i];
      var pos = getComputedStyle(el).position;
      if (pos !== 'sticky' && pos !== 'fixed') continue;
      var h = el.getBoundingClientRect().height;
      if (h > max && h < 200) max = h;
    }
    return Math.round(max);
  }

  function estils() {
    var s = document.createElement('style');
    s.textContent = [
      '.idx-pag{position:sticky;z-index:40;background:#F4F1EC;',
      'border-top:1px solid rgba(16,16,14,.14);border-bottom:1px solid rgba(16,16,14,.14)}',
      '.idx-in{display:flex;align-items:baseline;gap:16px;',
      'padding:9px clamp(16px,5vw,72px);max-width:100%}',
      '.idx-t{flex-shrink:0;font-family:Inter,system-ui,sans-serif;font-size:9px;font-weight:700;',
      'letter-spacing:.2em;text-transform:uppercase;color:#6B6560;margin:0}',
      '.idx-l{display:flex;gap:18px;overflow-x:auto;scrollbar-width:none;min-width:0;',
      'padding-right:26px;',
      '-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 30px),transparent 100%);',
      'mask-image:linear-gradient(90deg,#000 calc(100% - 30px),transparent 100%)}',
      '.idx-l::-webkit-scrollbar{display:none}',
      '.idx-l a{position:relative;flex-shrink:0;padding:3px 0;font-family:Inter,system-ui,sans-serif;',
      'font-size:11.5px;line-height:1.3;color:#46433f;text-decoration:none;white-space:nowrap}',
      '.idx-l a:hover{color:#10100E}',
      '.idx-l a[aria-current="true"]{color:#A8040E;font-weight:700}',
      '.idx-l a[aria-current="true"]::after{content:"";position:absolute;left:0;right:0;bottom:-1px;',
      'height:2px;background:#E20613}',
      '.idx-l a:focus-visible{outline:2px solid #E20613;outline-offset:3px}',
      '@media (max-width:700px){.idx-in{flex-direction:column;gap:5px;padding-top:8px;padding-bottom:8px}',
      '.idx-l{width:100%}}',
      '@media print{.idx-pag{display:none}}'
    ].join('');
    document.head.appendChild(s);
  }

  function munta() {
    if (document.querySelector('.idx-pag')) return;
    if (document.documentElement.scrollHeight < MIN_ALCADA) return;

    var tots = document.querySelectorAll('h2');
    var seccions = [], usades = {};
    for (var i = 0; i < tots.length; i++) {
      var h = tots[i];
      if (h.closest('.idx-pag, footer, .foot, template, [hidden]')) continue;
      var text = textNet(h);
      if (!text || text.length > 60) continue;
      if (!h.id) h.id = fesId(text, usades);
      h.style.scrollMarginTop = 'calc(var(--idx-top, 0px) + 64px)';
      seccions.push(h);
    }
    if (seccions.length < MIN_SECCIONS) return;

    estils();

    var lang = idioma();
    var barra = document.createElement('div');
    barra.className = 'idx-pag';
    var nav = document.createElement('nav');
    nav.className = 'idx-in';
    nav.setAttribute('aria-label', ETIQUETES[lang].nav);
    var titol = document.createElement('p');
    titol.className = 'idx-t';
    titol.textContent = ETIQUETES[lang].titol;
    var llista = document.createElement('div');
    llista.className = 'idx-l';

    var enllacos = {};
    seccions.forEach(function (h) {
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = textNet(h);
      llista.appendChild(a);
      enllacos[h.id] = a;
    });

    nav.appendChild(titol);
    nav.appendChild(llista);
    barra.appendChild(nav);

    // Va just després de la capçalera de la pàgina, abans del primer contingut.
    var ancora = document.querySelector('main') || seccions[0].closest('section, div');
    if (ancora && ancora.parentNode) ancora.parentNode.insertBefore(barra, ancora);
    else document.body.insertBefore(barra, document.body.firstChild);

    function colocaTop() {
      var t = alcadaCapcalera();
      barra.style.top = t + 'px';
      document.documentElement.style.setProperty('--idx-top', t + 'px');
    }
    colocaTop();
    window.addEventListener('resize', colocaTop);

    // La secció activa: la darrera que ha passat per sobre de la barra.
    var actiu = null;
    function marca(id) {
      if (id === actiu) return;
      if (actiu && enllacos[actiu]) enllacos[actiu].removeAttribute('aria-current');
      actiu = id;
      var a = enllacos[id];
      if (!a) return;
      a.setAttribute('aria-current', 'true');
      var r = a.getBoundingClientRect(), c = llista.getBoundingClientRect();
      if (r.left < c.left || r.right > c.right) {
        llista.scrollTo({
          left: llista.scrollLeft + (r.left - c.left) - 20,
          behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
        });
      }
    }

    if ('IntersectionObserver' in window) {
      var vistes = {};
      var io = new IntersectionObserver(function (entrades) {
        entrades.forEach(function (e) { vistes[e.target.id] = e.isIntersecting; });
        for (var i = seccions.length - 1; i >= 0; i--) {
          var s = seccions[i];
          if (s.getBoundingClientRect().top <= (alcadaCapcalera() + 80)) { marca(s.id); return; }
        }
        marca(seccions[0].id);
      }, { rootMargin: '-15% 0px -70% 0px', threshold: 0 });
      seccions.forEach(function (s) { io.observe(s); });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', munta);
  } else {
    munta();
  }
})();
