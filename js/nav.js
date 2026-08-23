/* Navegació del club · una sola per a tot el lloc.
 *
 * El problema que resol: fins ara el mapa complet del club (el menú de sis
 * columnes) només existia a la portada. En sortir-ne, la navegació es reduïa
 * als enllaços de la capçalera —i per sota de 1080 px encara menys, perquè els
 * marcats amb `.opt` es retiren. Resultat: des de qualsevol pàgina interior
 * amb un mòbil hi havia tres destins, el menú semblava desaparèixer i no hi
 * havia manera d'arribar a Campus, Femení, Blog o Partners sense saber-ne
 * l'adreça.
 *
 * Aquest fitxer posa el mateix menú a totes les pàgines i, de passada, respon
 * a la pregunta «on sóc?»: marca la secció actual i hi afegeix una molla de pa
 * quan la pàgina no en porta.
 *
 * COM S'HI TOCA: el mapa és la constant MAPA d'aquí sota, i prou. La portada
 * porta el mateix menú escrit a l'HTML (perquè es vegi encara que el JS no
 * arrenqui); si canvies MAPA, canvia també el <nav class="menu"> de
 * `index.html`, `es/index.html` i `en/index.html`. Són els quatre llocs.
 */
(function () {
  'use strict';

  // El mapa complet del club. Mateix contingut i mateix ordre que el
  // <nav class="menu"> de la portada.
  var MAPA = [
    { titol: 'Juga al Barna', enllacos: [
      ['/escoleta/', 'Escoleta', '4 a 8 anys'],
      ['/basquet-formatiu/', 'Bàsquet formatiu', 'quina edat té?'],
      ['/portes-obertes/', 'Portes obertes', 'tot el setembre, vine a provar'],
      ['/femeni/', 'Bàsquet femení', '8 equips'],
      ['/magics/', 'Barna Màgics', 'bàsquet inclusiu'],
      ['/faq/', 'Preguntes freqüents', ''],
    ] },
    { titol: 'Equips i temporada', enllacos: [
      ['/partits/equips/', 'Equips', 'sènior, júnior, cadet…'],
      ['/partits/', 'Calendari', ''],
      ['/partits/calendaris/', 'Dies de partit', 'per equip'],
      ['/fotos/', 'Galeria', 'fotos de temporada'],
    ] },
    { titol: 'Activitats', enllacos: [
      ['/campus/', 'Campus de bàsquet', ''],
      ['/tecnificacio-basquet-barcelona/', 'Tecnificació', 'amb Time Chamber'],
      ['/3x3/', 'Torneig 3x3', ''],
      ['/cistella-petita/', 'Cistella Petita', '3 a 8 anys'],
    ] },
    { titol: 'El Club', enllacos: [
      ['/club/', 'Qui som', ''],
      ['/historia/', 'Història', 'des de 1965'],
      ['/organigrama/', 'Organigrama', 'junta directiva'],
      ['/instal-lacions/', 'Instal·lacions', ''],
      ['/posicionament/', 'Posicionament', 'vs. Barça, Penya…'],
      ['/grup-barna-dades-oficials/', 'Dades oficials', ''],
      ['/proteccio-menor/', 'Protecció del menor', ''],
      ['/documents/', 'Documents', ''],
    ] },
    { titol: 'Actualitat', enllacos: [
      ['/blog/', 'Coneixement Barna', 'formació, famílies, dades…'],
      ['/premsa/', 'Premsa', 'arxiu 1988–2026'],
      ['/premidonaesport/', 'Premi Dona i Esport', ''],
    ] },
    { titol: 'Empreses', enllacos: [
      ['/empreses/', 'Empreses', 'per què invertir al Barna'],
      ['/patrocinadors/', 'Partners', 'qui hi és avui'],
      ['/partners-mapa/', 'Mapa de partners', ''],
      ['/dossier-patrocinis/', 'Dossier comercial', ''],
      ['/admin/', 'Zona admin', 'amb contrasenya'],
    ] },
  ];

  // Quines destinacions del menú tenen rèplica a /es/ i a /en/. Comprovat
  // contra el disc: la resta no existeixen i, si s'hi enllacés, serien un 404.
  // Actualitzar-ho quan es tradueixi una pàgina nova.
  var REPLICA = {
    es: ['/escoleta/', '/faq/', '/partits/equips/', '/partits/', '/partits/calendaris/',
         '/fotos/', '/campus/', '/3x3/', '/cistella-petita/', '/club/', '/historia/',
         '/organigrama/', '/grup-barna-dades-oficials/', '/blog/', '/premsa/',
         '/premidonaesport/', '/patrocinadors/', '/partners-mapa/', '/dossier-patrocinis/'],
    en: ['/escoleta/', '/faq/', '/partits/equips/', '/partits/', '/partits/calendaris/',
         '/fotos/', '/campus/', '/3x3/', '/cistella-petita/', '/club/',
         '/grup-barna-dades-oficials/', '/documents/', '/blog/', '/premsa/',
         '/premidonaesport/', '/patrocinadors/', '/partners-mapa/', '/dossier-patrocinis/'],
  };

  // Noms de tram que no surten al menú però sí a la molla de pa.
  var NOMS_EXTRA = {
    'partits': 'Calendari', 'equips': 'Equips', 'calendaris': 'Dies de partit',
    'blog': 'Coneixement Barna', 'club': 'El club', 'fotos': 'Galeria',
    'premsa': 'Premsa', 'campus': 'Campus', 'escoleta': 'Escoleta',
    'femeni': 'Bàsquet femení', 'basquet-femeni': 'Bàsquet femení',
    'patrocinadors': 'Partners', 'premidonaesport': 'Premi Dona i Esport',
    'documents': 'Documents', 'briefing': 'Premsa', 'faq': 'Preguntes freqüents',
    'avis-legal': 'Avís legal', 'politica-de-privacitat': 'Política de privacitat',
    'es': 'Castellà', 'en': 'English',
  };

  var doc = document;
  var arrel = doc.documentElement;

  // --- Camí actual, normalitzat -------------------------------------------
  function normalitza(p) {
    if (!p) return '/';
    p = p.replace(/index\.html$/, '');
    if (p.length > 1 && p.slice(-1) !== '/' && !/\.[a-z]{2,5}$/i.test(p)) p += '/';
    return p;
  }
  var ACTUAL = normalitza(location.pathname);
  // Les rèpliques /es/ i /en/ són el mateix mapa amb un prefix.
  var PREFIX = /^\/(es|en)\//.test(ACTUAL) ? ACTUAL.slice(0, 4) : '/';

  // La destinació d'un enllaç del menú segons la llengua de la pàgina on ets.
  function desti(href) {
    if (PREFIX === '/') return href;
    var llengua = PREFIX.slice(1, 3);
    var te = REPLICA[llengua] || [];
    return te.indexOf(href) > -1 ? '/' + llengua + href : href;
  }

  // --- 1. El menú ----------------------------------------------------------
  function construeixMenu() {
    var nav = doc.createElement('nav');
    nav.className = 'menu';
    nav.id = 'menu';
    nav.setAttribute('aria-label', 'Menú complet');

    var grid = doc.createElement('div');
    grid.className = 'menu-grid';

    MAPA.forEach(function (col) {
      var d = doc.createElement('div');
      d.className = 'menu-col';
      var h = doc.createElement('h3');
      h.textContent = col.titol;
      d.appendChild(h);
      col.enllacos.forEach(function (e) {
        var a = doc.createElement('a');
        a.href = desti(e[0]);
        a.textContent = e[1];
        if (e[0] === '/admin/') { a.className = 'menu-admin'; a.rel = 'nofollow'; }
        if (e[2]) {
          var s = doc.createElement('small');
          s.textContent = e[2];
          a.appendChild(doc.createTextNode(' '));
          a.appendChild(s);
        }
        d.appendChild(a);
      });
      grid.appendChild(d);
    });

    nav.appendChild(grid);
    var peu = doc.createElement('div');
    peu.className = 'menu-foot';
    peu.textContent = '@cbgrupbarna · +34 698 425 153 · El Clot, Barcelona';
    nav.appendChild(peu);
    return nav;
  }

  function construeixBurger() {
    var b = doc.createElement('button');
    b.className = 'head-burger';
    b.id = 'burger';
    b.type = 'button';
    b.setAttribute('aria-label', 'Obrir el menú');
    b.setAttribute('aria-expanded', 'false');
    b.setAttribute('aria-controls', 'menu');
    b.innerHTML = '<i></i><i></i>';
    return b;
  }

  var capcalera = doc.querySelector('header.head, header, .head');
  var menu = doc.getElementById('menu') || doc.querySelector('.menu');
  var burger = doc.getElementById('burger') || doc.querySelector('.head-burger');

  if (capcalera && !menu) {
    menu = construeixMenu();
    capcalera.parentNode.insertBefore(menu, capcalera.nextSibling);
  }
  if (capcalera && menu && !burger) {
    burger = construeixBurger();
    // A l'esquerra de tot de la capçalera, davant de l'escut: és on la gent
    // el busca i on és a la portada.
    var dins = capcalera.querySelector('.head-in') || capcalera;
    var costat = dins.querySelector('.head-side');
    if (costat) costat.insertBefore(burger, costat.firstChild);
    else dins.insertBefore(burger, dins.firstChild);
    dins.classList.add('head-in--amb-burger');
  }

  // --- 2. Obrir i tancar, amb el teclat inclòs -----------------------------
  if (burger && menu) {
    var obert = false;
    var ultimFocus = null;

    function focusables() {
      return [].slice.call(menu.querySelectorAll('a[href], button:not([disabled])'))
        .filter(function (el) { return el.offsetParent !== null || el.getClientRects().length; });
    }

    function commuta(open) {
      obert = open;
      menu.classList.toggle('open', open);
      doc.body.classList.toggle('menu-open', open);
      // Bloqueig del fons sense perdre la posició de lectura.
      if (open) {
        ultimFocus = doc.activeElement;
        var y = window.scrollY;
        doc.body.dataset.navScroll = String(y);
        doc.body.style.overflow = 'hidden';
      } else {
        doc.body.style.overflow = '';
        var prev = +(doc.body.dataset.navScroll || 0);
        if (prev && Math.abs(window.scrollY - prev) > 2) window.scrollTo(0, prev);
        delete doc.body.dataset.navScroll;
      }
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Tancar el menú' : 'Obrir el menú');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) {
        var f = focusables();
        if (f.length) setTimeout(function () { f[0].focus(); }, 80);
      } else if (ultimFocus && ultimFocus.focus) {
        ultimFocus.focus();
      }
    }

    menu.setAttribute('aria-hidden', 'true');
    burger.addEventListener('click', function () { commuta(!obert); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) commuta(false); });

    // Escape i captura del tabulador: el menú de la portada no els tenia.
    doc.addEventListener('keydown', function (e) {
      var estaObert = menu.classList.contains('open');
      if (!estaObert) return;
      if (e.key === 'Escape') { e.preventDefault(); commuta(false); return; }
      if (e.key !== 'Tab') return;
      // Amb el menú obert, el tabulador no ha de sortir cap a la pàgina de sota.
      var f = focusables();
      if (!f.length) return;
      var primer = f[0], ultim = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === primer) { e.preventDefault(); ultim.focus(); }
      else if (!e.shiftKey && doc.activeElement === ultim) { e.preventDefault(); primer.focus(); }
    });
  }

  // --- 3. On sóc: marcar la secció actual ----------------------------------
  // Coincidència exacta primer; si no, la secció que conté la pàgina (així una
  // fitxa d'equip marca «Equips» i un article marca «Coneixement Barna»).
  (function () {
    var enllacos = [].slice.call(doc.querySelectorAll('header a[href], .head a[href], .menu a[href]'))
      .filter(function (a) {
        // Fora el commutador d'idioma i les icones de xarxes: el primer apunta
        // sempre a la pàgina on ja ets (i es quedaria la marca per a ell), i
        // les segones no són seccions del club.
        return !a.closest('.lang-switch, .soc');
      });
    var exacte = null, seccio = null, llargSeccio = 0;
    enllacos.forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (!href || href.charAt(0) !== '/' || /^\/\//.test(href)) return;
      var d = normalitza(href);
      if (d === ACTUAL) { exacte = exacte || a; return; }
      if (d !== '/' && ACTUAL.indexOf(d) === 0 && d.length > llargSeccio) { seccio = a; llargSeccio = d.length; }
    });
    enllacos.forEach(function (a) {
      var href = normalitza(a.getAttribute('href') || '');
      if (exacte && href === ACTUAL) a.setAttribute('aria-current', 'page');
      else if (!exacte && seccio && a === seccio) a.setAttribute('aria-current', 'true');
    });
  })();

  // --- 4. Molla de pa: la ruta fins on ets --------------------------------
  (function () {
    if (ACTUAL === '/' || ACTUAL === '/es/' || ACTUAL === '/en/') return;
    // `.crumb` és la molla que ja fan servir 312 pàgines del lloc: si no es
    // mirés, aquí se n'hi afegiria una segona just a sota.
    if (doc.querySelector('.crumb, .molla, .breadcrumb, nav[aria-label*="ruta" i], nav[aria-label*="navegaci" i] ol')) return;
    // On penjar-la, de més precís a més general. L'última xarxa és el primer
    // germà de la capçalera: a les pàgines sense <main> és on comença el cos.
    var main = doc.querySelector('main, #main');
    if (!main) {
      var cap = doc.querySelector('header.head, header, .head');
      var seg = cap && cap.nextElementSibling;
      while (seg && (seg.tagName === 'SCRIPT' || seg.tagName === 'STYLE'
             || seg.classList.contains('menu') || seg.classList.contains('actionbar'))) {
        seg = seg.nextElementSibling;
      }
      main = seg && seg.querySelector('.wrap') ? seg.querySelector('.wrap') : seg;
    }
    if (!main || main.tagName === 'FOOTER') return;

    // Noms coneguts, primer el mapa del menú i després la llista d'extres.
    var noms = {};
    MAPA.forEach(function (c) { c.enllacos.forEach(function (e) { noms[normalitza(e[0])] = e[1]; }); });

    var trams = ACTUAL.split('/').filter(Boolean);
    if (!trams.length) return;
    var nav = doc.createElement('nav');
    nav.className = 'molla';
    nav.setAttribute('aria-label', 'Ruta de navegació');
    var ol = doc.createElement('ol');

    function posa(href, text, ultim) {
      var li = doc.createElement('li');
      if (ultim) {
        li.textContent = text;
        li.setAttribute('aria-current', 'page');
      } else {
        var a = doc.createElement('a');
        a.href = href; a.textContent = text;
        li.appendChild(a);
      }
      ol.appendChild(li);
    }

    posa(PREFIX, 'Inici', false);
    var acumulat = PREFIX === '/' ? '' : PREFIX.replace(/\/$/, '');
    var començaA = PREFIX === '/' ? 0 : 1;
    for (var i = començaA; i < trams.length; i++) {
      acumulat += '/' + trams[i];
      var ruta = normalitza(acumulat + '/');
      var esUltim = i === trams.length - 1;
      var text = noms[ruta] || NOMS_EXTRA[trams[i]];
      if (!text) {
        // L'últim tram sense nom conegut: el titular de la pàgina ho diu millor
        // que l'adreça.
        var h1 = doc.querySelector('h1');
        text = esUltim && h1 && h1.textContent.trim()
          ? h1.textContent.trim()
          : trams[i].replace(/\.html$/, '').replace(/[-_]/g, ' ');
      }
      if (text.length > 46) text = text.slice(0, 44).trim() + '…';
      posa(ruta, text, esUltim);
    }
    if (ol.children.length < 2) return;
    nav.appendChild(ol);
    main.insertBefore(nav, main.firstChild);
  })();
}());
