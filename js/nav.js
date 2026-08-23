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

  // El mapa d'idiomes el genera `scripts/genera-nav-i18n.py` des de
  // `i18n/routes.yml`, que és la font de veritat del club. No es pot
  // substituir per posar un prefix davant de l'adreça: divuit rutes estan
  // traduïdes de debò (/proteccio-menor/ és /es/proteccion-menor/) i un
  // prefix hi enviaria la gent a un 404.
  var TRIOS = window.CBGB_IDIOMES || [];
  var IDIOMES = ['ca', 'es', 'en'];
  var PER_URL = {};   // qualsevol adreça -> {ca:…, es:…, en:…}
  TRIOS.forEach(function (t) {
    var fila = { ca: t[0], es: t[1] || null, en: t[2] || null };
    IDIOMES.forEach(function (l) { if (fila[l]) PER_URL[fila[l]] = fila; });
  });

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

  var LLENGUA = PREFIX === '/' ? 'ca' : PREFIX.slice(1, 3);

  // La destinació d'un enllaç del menú en la llengua de la pàgina on ets, o
  // `null` si aquella pàgina no està traduïda. `null` vol dir que l'entrada
  // no surt al menú d'aquesta llengua: el criteri escrit a i18n/README.md és
  // que posar al menú castellà un enllaç que porta a una pàgina en català és
  // pitjor que no posar-l'hi.
  function desti(href) {
    if (LLENGUA === 'ca') return href;
    var fila = PER_URL[href];
    return (fila && fila[LLENGUA]) || null;
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
      var posats = 0;
      col.enllacos.forEach(function (e) {
        var href = desti(e[0]);
        if (!href) return;               // sense traducció: no surt en aquesta llengua
        posats++;
        var a = doc.createElement('a');
        a.href = href;
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
      // Una columna que s'ha quedat sense cap enllaç en aquesta llengua no
      // ha de deixar un títol solt penjant.
      if (posats) grid.appendChild(d);
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

  // Quina és la capçalera de debò. No val agafar el primer <header>: a
  // /escoleta/ el <header> és el hero de la pàgina i la navegació real és una
  // barra fixa a sobre (.langbar). El botó de menú hi quedava a sota, tapat, i
  // no es podia ni tocar. L'ordre és: la capçalera del sistema, després la
  // barra enganxada de dalt que porti enllaços, i només llavors un <header>.
  function trobaCapcalera() {
    var propia = doc.querySelector('header.head, .head');
    if (propia) return propia;

    var candidates = [].slice.call(doc.querySelectorAll('header, div, nav'));
    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      var cs = getComputedStyle(el);
      if (cs.position !== 'fixed' && cs.position !== 'sticky') continue;
      var r = el.getBoundingClientRect();
      if (r.top > 80 || r.height < 20 || r.width < innerWidth * 0.6) continue;
      if (!el.querySelector('a[href]')) continue;
      return el.querySelector('.wrap') || el;
    }

    var h = doc.querySelector('header');
    if (h) {
      var hs = getComputedStyle(h);
      if (hs.position === 'fixed' || hs.position === 'sticky') return h;
    }
    return null;   // cap: se'n fabricarà una de mínima
  }

  var capcalera = trobaCapcalera();
  var menu = doc.getElementById('menu') || doc.querySelector('.menu');
  var burger = doc.getElementById('burger') || doc.querySelector('.head-burger');

  // Pàgines sense cap capçalera (la mascota, la galeria del 3x3): són públiques
  // i entren per cercador, però no tenien cap sortida cap al club. Se'ls en fa
  // una de mínima —escut i botó de menú— que no els toca el disseny.
  // Aquest fitxer només es carrega on s'ha decidit que hi vagi, així que
  // arribar aquí ja és la decisió: no cal endevinar si la pàgina la vol.
  if (!capcalera) {
    capcalera = doc.createElement('header');
    capcalera.className = 'head head--injectada';
    var dinsNou = doc.createElement('div');
    dinsNou.className = 'head-in';
    var marca = doc.createElement('a');
    marca.className = 'head-brand';
    marca.href = PREFIX;
    marca.setAttribute('aria-label', 'CB Grup Barna · inici');
    var esc = doc.createElement('img');
    esc.src = '/logo.png'; esc.alt = 'Escut del CB Grup Barna';
    esc.width = 30; esc.height = 30; esc.decoding = 'async';
    var nom = doc.createElement('span');
    nom.textContent = 'CB Grup Barna';
    marca.appendChild(esc); marca.appendChild(nom);
    dinsNou.appendChild(marca);
    capcalera.appendChild(dinsNou);
    doc.body.insertBefore(capcalera, doc.body.firstChild);
  }

  if (capcalera && !menu) {
    menu = construeixMenu();
    // Sempre penjat del <body>: dins d'una barra fixa amb `overflow` o un
    // `z-index` propi, un menú a pantalla completa quedaria retallat.
    doc.body.appendChild(menu);
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

  // --- 1 bis. Cercador dins del menú --------------------------------------
  // El menú porta els 30 destins grans del club; el lloc en té més de 400.
  // A un article del blog o a una fitxa d'equip només s'hi arriba si saps de
  // quina secció penja. Amb un camp de cerca s'hi arriba escrivint-ne el
  // nom, que és el que fa tothom quan no sap on és una cosa.
  //
  // L'índex (uns 60 KB) NO es carrega amb la pàgina: es demana el primer cop
  // que algú toca el camp. Qui no el faci servir no en paga res.
  var TEXTOS = {
    ca: { etiqueta: 'Cerca al web', pista: 'Cerca una pàgina…', cap: 'Cap resultat per a',
          un: 'resultat', molts: 'resultats' },
    es: { etiqueta: 'Buscar en la web', pista: 'Busca una página…', cap: 'Sin resultados para',
          un: 'resultado', molts: 'resultados' },
    en: { etiqueta: 'Search the site', pista: 'Search for a page…', cap: 'No results for',
          un: 'result', molts: 'results' }
  };

  function senseAccents(s) {
    // Rang de les marques diacrítiques combinades, escrit amb codis i no amb
    // els caràcters literals: aquests sobreviuen malament a un reformatatge.
    return s.normalize ? s.normalize('NFD').replace(/[\u0300-\u036f]/g, '') : s;
  }

  function posaCercador(menu) {
    if (!menu || menu.querySelector('.menu-cerca')) return;
    var t = TEXTOS[LLENGUA] || TEXTOS.ca;

    var caixa = doc.createElement('div');
    caixa.className = 'menu-cerca';

    var etiqueta = doc.createElement('label');
    etiqueta.className = 'menu-cerca-lab';
    etiqueta.setAttribute('for', 'menu-cerca-camp');
    etiqueta.textContent = t.etiqueta;

    var camp = doc.createElement('input');
    camp.type = 'search';
    camp.id = 'menu-cerca-camp';
    camp.className = 'menu-cerca-camp';
    camp.placeholder = t.pista;
    camp.autocomplete = 'off';
    camp.setAttribute('role', 'combobox');
    camp.setAttribute('aria-expanded', 'false');
    camp.setAttribute('aria-controls', 'menu-cerca-llista');
    camp.setAttribute('aria-autocomplete', 'list');

    var compte = doc.createElement('p');
    compte.className = 'menu-cerca-compte';
    compte.setAttribute('aria-live', 'polite');

    var llista = doc.createElement('ul');
    llista.className = 'menu-cerca-llista';
    llista.id = 'menu-cerca-llista';
    llista.setAttribute('role', 'listbox');
    llista.setAttribute('aria-label', t.etiqueta);

    caixa.appendChild(etiqueta);
    caixa.appendChild(camp);
    caixa.appendChild(compte);
    caixa.appendChild(llista);
    menu.insertBefore(caixa, menu.firstChild);

    var index = null, carregant = false, triat = -1;

    function carrega() {
      if (index || carregant) return;
      carregant = true;
      fetch('/js/cerca-index.json')
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (dades) {
          // Només la llengua de la pàgina on ets: qui busca en català no ha
          // de rebre resultats en anglès.
          index = dades.filter(function (e) { return e.l === LLENGUA; });
          carregant = false;
          if (camp.value.trim()) pinta();
        })
        .catch(function () { carregant = false; index = []; });
    }

    // Es busca paraula a paraula, i cada paraula val si una del text hi
    // encaixa per davant en qualsevol dels dos sentits. Això és el que fa que
    // «partidos» trobi «Dies de partido» i «campus» trobi «camp»: exigir la
    // consulta sencera com a tros de text fallava amb qualsevol plural.
    function encaixa(paraula, mots) {
      var millor = -1;
      for (var i = 0; i < mots.length; i++) {
        var m = mots[i];
        if (!m) continue;
        var val = m.indexOf(paraula) === 0
          || (paraula.length >= 4 && paraula.indexOf(m) === 0 && m.length >= 4);
        if (val) { millor = i; break; }
      }
      return millor;
    }

    function puntua(e, paraules) {
      if (!e._m) e._m = e.b.split(/[^a-z0-9]+/);
      var total = 0;
      for (var i = 0; i < paraules.length; i++) {
        var on = encaixa(paraules[i], e._m);
        if (on < 0) {
          // Última oportunitat: com a tros de text qualsevol (busques «xar»
          // i la pàgina diu «Eixample»).
          var k = e.b.indexOf(paraules[i]);
          if (k < 0) return -1;
          total += 60 + Math.min(k, 40);
        } else {
          total += Math.min(on, 20);
        }
      }
      // A igualtat, davant l'adreça més curta: les seccions grans surten
      // abans que els seus articles.
      return total + e.u.length / 20;
    }

    function pinta() {
      var q = senseAccents(camp.value.trim().toLowerCase());
      llista.innerHTML = '';
      triat = -1;
      menu.classList.toggle('cercant', !!q);
      camp.setAttribute('aria-expanded', q ? 'true' : 'false');
      if (!q) { compte.textContent = ''; return; }
      if (!index) { compte.textContent = '…'; return; }

      var paraules = q.split(/\s+/).filter(Boolean);
      var trobats = index
        .map(function (e) { return { e: e, p: puntua(e, paraules) }; })
        .filter(function (x) { return x.p >= 0; })
        .sort(function (a, b) { return a.p - b.p; })
        .slice(0, 12);

      if (!trobats.length) {
        compte.textContent = t.cap + ' «' + camp.value.trim() + '»';
        return;
      }
      compte.textContent = trobats.length + ' ' + (trobats.length === 1 ? t.un : t.molts);
      trobats.forEach(function (x, i) {
        var li = doc.createElement('li');
        li.setAttribute('role', 'option');
        li.setAttribute('aria-selected', 'false');
        li.id = 'menu-cerca-op-' + i;
        var a = doc.createElement('a');
        a.href = x.e.u;
        a.textContent = x.e.t;
        var ruta = doc.createElement('span');
        ruta.className = 'menu-cerca-ruta';
        ruta.textContent = x.e.u;
        a.appendChild(ruta);
        li.appendChild(a);
        llista.appendChild(li);
      });
    }

    function mou(delta) {
      var ops = llista.querySelectorAll('li');
      if (!ops.length) return;
      if (triat >= 0) ops[triat].setAttribute('aria-selected', 'false');
      // Es fa voltar per n+1 posicions: les n opcions més la de «cap
      // seleccionada», que és quan el cursor torna al camp de text. Es compta
      // amb `triat + 1` perquè -1 vol dir justament aquesta posició de més.
      var quants = ops.length + 1;
      triat = ((triat + 1 + delta) % quants + quants) % quants - 1;
      if (triat < 0) { camp.removeAttribute('aria-activedescendant'); return; }
      ops[triat].setAttribute('aria-selected', 'true');
      camp.setAttribute('aria-activedescendant', ops[triat].id);
      ops[triat].scrollIntoView({ block: 'nearest' });
    }

    camp.addEventListener('focus', carrega);
    camp.addEventListener('input', function () { carrega(); pinta(); });
    camp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); mou(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); mou(-1); }
      else if (e.key === 'Enter') {
        var ops = llista.querySelectorAll('li');
        var anar = triat >= 0 ? ops[triat] : ops[0];
        if (anar) { e.preventDefault(); anar.querySelector('a').click(); }
      }
    });
  }

  if (menu) posaCercador(menu);

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
        // El focus va al camp de cerca: des d'allà s'arriba a qualsevol
        // pàgina del lloc, i amb el tabulador se surt cap al menú de sempre.
        var cerca = menu.querySelector('.menu-cerca-camp');
        var f = focusables();
        var primer = cerca || f[0];
        if (primer) setTimeout(function () { primer.focus(); }, 80);
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

  // --- 2 bis. Commutador d'idioma -----------------------------------------
  // Només existia a les tres portades. Qui entrava per cercador a una pàgina
  // interior en castellà o en anglès —que és per on entra la majoria— no en
  // podia sortir. S'hi posa només quan aquella pàgina té traducció de debò:
  // si no en té, no s'ofereix l'idioma, perquè un enllaç que porta a una
  // pàgina en una altra llengua és pitjor que no oferir-lo.
  (function () {
    if (!capcalera) return;
    if (doc.querySelector('.lang-switch, .langs')) return;   // ja en té un de propi
    var fila = PER_URL[ACTUAL];
    if (!fila) return;                                       // pàgina sense traduccions

    var disponibles = IDIOMES.filter(function (l) { return fila[l]; });
    if (disponibles.length < 2) return;                      // un sol idioma: no hi ha res a commutar

    var NOMS = { ca: 'Català', es: 'Castellano', en: 'English' };
    var caixa = doc.createElement('div');
    caixa.className = 'lang-switch';
    caixa.setAttribute('aria-label', "Canvia d'idioma · Cambiar idioma · Change language");

    disponibles.forEach(function (l, i) {
      if (i) {
        var sep = doc.createElement('span');
        sep.className = 'sep';
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '·';
        caixa.appendChild(sep);
      }
      var a = doc.createElement('a');
      a.href = fila[l];
      a.hreflang = l;
      a.textContent = l.toUpperCase();
      a.setAttribute('lang', l);
      // El nom sencer per a qui ho escolta: «ES» tot sol no diu res.
      a.setAttribute('aria-label', NOMS[l]);
      if (l === LLENGUA) {
        a.className = 'active';
        a.setAttribute('aria-current', 'true');
      }
      caixa.appendChild(a);
    });

    var dins = capcalera.querySelector('.head-in') || capcalera;
    var dreta = dins.querySelector('.head-side.r');
    if (dreta) dreta.appendChild(caixa);
    else dins.appendChild(caixa);
    dins.classList.add('head-in--amb-idiomes');
  }());

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
