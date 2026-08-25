/* Mapa de navegació · generat per scripts/build-mapa.py — NO editar a mà.
   Un sol botó ≡ a totes les capçaleres («L'estètica definitiva», decisió 4).
   Autocontingut: injecta botó, estil i diàleg. */
(function () {
  'use strict';
  if (document.getElementById('mapa-btn')) return;
  var DADES = {"ca": {"t": {"obre": "Obre el mapa del web", "titol": "Tot el web", "tanca": "Tanca", "cerca": "Cercar al web", "inici": "Inici"}, "cols": [["Juga al Barna", [["/escoleta/", "Escoleta"], ["/basquet-formatiu/", "B\u00e0squet formatiu"], ["/portes-obertes/", "Portes obertes"], ["/femeni/", "B\u00e0squet femen\u00ed"], ["/magics/", "Barna M\u00e0gics"], ["/faq/", "Preguntes freq\u00fcents"]]], ["Equips i temporada", [["/partits/equips/", "Equips"], ["/partits/", "Calendari"], ["/partits/calendaris/", "Calendari per equip"], ["/fotos/", "Galeria de fotos"]]], ["Activitats", [["/campus/", "Campus de b\u00e0squet"], ["/tecnificacio-basquet-barcelona/", "Tecnificaci\u00f3"], ["/3x3/", "Torneig 3x3"], ["/cistella-petita/", "Cistella Petita"]]], ["El Club", [["/club/", "Qui som"], ["/historia/", "Hist\u00f2ria"], ["/organigrama/", "Organigrama"], ["/instal-lacions/", "Instal\u00b7lacions"], ["/grup-barna-dades-oficials/", "Dades oficials"], ["/proteccio-menor/", "Protecci\u00f3 del menor"], ["/documents/", "Documents"]]], ["Actualitat", [["/blog/", "Coneixement Barna"], ["/premsa/", "Premsa"], ["/premsa/moments/", "Moments a Instagram"], ["/premidonaesport/", "Premi Dona i Esport"]]], ["Empreses", [["/empreses/", "Empreses"], ["/patrocinadors/", "Partners"], ["/partners-mapa/", "Mapa de partners"]]]], "inici": "/", "cerca": "/cerca/"}, "es": {"t": {"obre": "Abre el mapa de la web", "titol": "Toda la web", "tanca": "Cerrar", "cerca": "Buscar en la web", "inici": "Inicio"}, "cols": [["Juega en el Barna", [["/es/escoleta/", "Escoleta"], ["/es/baloncesto-formativo/", "Baloncesto formativo"], ["/es/puertas-abiertas/", "Puertas abiertas"], ["/es/baloncesto-femenino/", "Baloncesto femenino"], ["/es/magics/", "Barna M\u00e0gics"], ["/es/faq/", "Preguntas frecuentes"]]], ["Equipos y temporada", [["/es/partits/equips/", "Equipos"], ["/es/partits/", "Calendario"], ["/es/partits/calendaris/", "Calendario por equipo"], ["/es/fotos/", "Galer\u00eda de fotos"]]], ["Actividades", [["/es/campus/", "Campus de baloncesto"], ["/es/tecnificacion-baloncesto-barcelona/", "Tecnificaci\u00f3n"], ["/es/3x3/", "Torneo 3x3"], ["/es/cistella-petita/", "Cistella Petita"]]], ["El Club", [["/es/club/", "Qui\u00e9nes somos"], ["/es/historia/", "Historia"], ["/es/organigrama/", "Organigrama"], ["/es/instalaciones/", "Instalaciones"], ["/es/grup-barna-dades-oficials/", "Datos oficiales"], ["/es/proteccion-menor/", "Protecci\u00f3n del menor"], ["/es/documentos/", "Documentos"]]], ["Actualidad", [["/es/blog/", "Conocimiento Barna"], ["/es/premsa/", "Prensa"], ["/es/premsa/momentos/", "Momentos en Instagram"], ["/es/premidonaesport/", "Premi Dona i Esport"]]], ["Empresas", [["/es/empresas/", "Empresas"], ["/es/patrocinadors/", "Partners"], ["/es/partners-mapa/", "Mapa de partners"]]]], "inici": "/es/", "cerca": "/es/busqueda/"}, "en": {"t": {"obre": "Open the site map", "titol": "The whole site", "tanca": "Close", "cerca": "Search the site", "inici": "Home"}, "cols": [["Play at Barna", [["/en/escoleta/", "Escoleta"], ["/en/development-basketball/", "Development basketball"], ["/en/open-days/", "Open days"], ["/en/womens-basketball/", "Women's basketball"], ["/en/magics/", "Barna M\u00e0gics"], ["/en/faq/", "FAQ"]]], ["Teams and season", [["/en/partits/equips/", "Teams"], ["/en/partits/", "Calendar"], ["/en/partits/calendaris/", "Calendar by team"], ["/en/fotos/", "Photo gallery"]]], ["Activities", [["/en/campus/", "Basketball camp"], ["/en/basketball-skills-training-barcelona/", "Skills training"], ["/en/3x3/", "3x3 tournament"], ["/en/cistella-petita/", "Cistella Petita"]]], ["The Club", [["/en/club/", "Who we are"], ["/en/history/", "History"], ["/en/organisation/", "Organisation"], ["/en/facilities/", "Facilities"], ["/en/grup-barna-dades-oficials/", "Official data"], ["/en/child-protection/", "Child protection"], ["/en/documents/", "Documents"]]], ["News", [["/en/blog/", "Barna knowledge"], ["/en/premsa/", "Press"], ["/en/premsa/highlights/", "Instagram highlights"], ["/en/premidonaesport/", "Premi Dona i Esport"]]], ["Companies", [["/en/companies/", "Companies"], ["/en/patrocinadors/", "Partners"], ["/en/partners-mapa/", "Partner map"]]]], "inici": "/en/", "cerca": "/en/search/"}};
  var path = location.pathname;
  var lang = path.indexOf('/es/') === 0 ? 'es' : path.indexOf('/en/') === 0 ? 'en' : 'ca';
  var D = DADES[lang];

  var css = ''
    + '#mapa-btn{appearance:none;border:1px solid currentColor;background:transparent;color:inherit;'
    + 'width:38px;height:38px;min-width:38px;display:inline-flex;flex-direction:column;align-items:center;'
    + 'justify-content:center;gap:4px;cursor:pointer;padding:0;flex:none}'
    + '#mapa-btn span{display:block;width:16px;height:2px;background:currentColor}'
    + '#mapa-btn:focus-visible{outline:3px solid #E20613;outline-offset:2px}'
    + '#mapa-btn.mapa-flotant{position:fixed;top:14px;right:14px;z-index:990;background:#10100E;'
    + 'color:#fff;border-color:rgba(255,255,255,.4);box-shadow:0 4px 18px rgba(16,16,14,.35)}'
    + '#mapa-ov{position:fixed;inset:0;z-index:995;background:rgba(16,16,14,.72);display:flex;'
    + 'align-items:flex-start;justify-content:center;padding:5vh 16px;overflow:auto}'
    + '#mapa-ov[hidden]{display:none}'
    + '#mapa-card{background:#fff;color:#10100E;width:100%;max-width:960px;'
    + 'border:1px solid rgba(16,16,14,.14);box-shadow:0 30px 70px rgba(0,0,0,.5);'
    + "font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;font-size:15px;line-height:1.5}"
    + '#mapa-hd{display:flex;align-items:center;justify-content:space-between;gap:14px;'
    + 'padding:18px 26px;border-bottom:2px solid #10100E}'
    + "#mapa-hd strong{font-family:'Anton','Haettenschweiler','Arial Narrow',sans-serif;font-weight:400;"
    + 'font-size:21px;letter-spacing:.02em;text-transform:uppercase}'
    + '#mapa-x{appearance:none;border:1px solid #10100E;background:transparent;color:#10100E;'
    + 'width:36px;height:36px;font-size:17px;cursor:pointer;line-height:1}'
    + '#mapa-x:focus-visible{outline:3px solid #E20613;outline-offset:2px}'
    + '.mapa-grid{display:grid;grid-template-columns:repeat(3,1fr)}'
    + '.mapa-col{padding:20px 26px;border-right:1px solid rgba(16,16,14,.14);border-bottom:1px solid rgba(16,16,14,.14)}'
    + '.mapa-col:nth-child(3n){border-right:none}'
    + '.mapa-col h3{margin:0 0 11px;font-family:inherit;font-weight:800;font-size:10.5px;'
    + 'letter-spacing:.2em;text-transform:uppercase;color:#A8040E}'
    + '.mapa-col ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}'
    + '.mapa-col a{color:#46433f;text-decoration:none;font-weight:600;font-size:14.5px;display:block;padding:2px 0}'
    + '.mapa-col a:hover{color:#A8040E}'
    + '.mapa-col a:focus-visible{outline:3px solid #E20613;outline-offset:2px}'
    + '#mapa-ft{display:flex;flex-wrap:wrap;gap:8px 22px;align-items:center;padding:14px 26px;'
    + 'border-top:1px solid rgba(16,16,14,.14);font-size:12.5px;color:#6B6560}'
    + '#mapa-ft a{color:#A8040E;text-decoration:none;font-weight:700}'
    + '@media(max-width:760px){.mapa-grid{grid-template-columns:1fr}.mapa-col{border-right:none}}'
    + '@media print{#mapa-btn,#mapa-ov{display:none !important}}';
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  var btn = document.createElement('button');
  btn.id = 'mapa-btn';
  btn.type = 'button';
  btn.setAttribute('aria-label', D.t.obre);
  btn.setAttribute('aria-haspopup', 'dialog');
  btn.setAttribute('aria-expanded', 'false');
  btn.innerHTML = '<span></span><span></span><span></span>';

  // Només la capçalera estàndard (.head-in) té un lloc previst per al botó.
  // A la resta —heros d'una peça, portades autònomes— el botó va flotant a
  // dalt a la dreta, que és el «no es perd mai» de la guia.
  var seu = document.querySelector('.head-in');
  if (seu) { seu.insertBefore(btn, seu.firstChild); }
  else { btn.className = 'mapa-flotant'; document.body.appendChild(btn); }

  var ov = document.createElement('div');
  ov.id = 'mapa-ov';
  ov.hidden = true;
  var cols = '';
  for (var i = 0; i < D.cols.length; i++) {
    var c = D.cols[i];
    cols += '<div class="mapa-col"><h3>' + c[0] + '</h3><ul>';
    for (var j = 0; j < c[1].length; j++) {
      cols += '<li><a href="' + c[1][j][0] + '">' + c[1][j][1] + '</a></li>';
    }
    cols += '</ul></div>';
  }
  ov.innerHTML = '<div id="mapa-card" role="dialog" aria-modal="true" aria-label="' + D.t.titol + '">'
    + '<div id="mapa-hd"><strong>' + D.t.titol + '</strong>'
    + '<button id="mapa-x" type="button" aria-label="' + D.t.tanca + '">&#10005;</button></div>'
    + '<div class="mapa-grid">' + cols + '</div>'
    + '<div id="mapa-ft"><a href="' + D.inici + '">' + D.t.inici + '</a>'
    + '<a href="' + D.cerca + '">&#8981; ' + D.t.cerca + '</a>'
    + '<span>CB Grup Barna &#183; El Clot &#183; Barcelona</span></div></div>';
  document.body.appendChild(ov);

  var x = ov.querySelector('#mapa-x');
  function obre() {
    ov.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    x.focus();
  }
  function tanca() {
    ov.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    btn.focus();
  }
  btn.addEventListener('click', function () { ov.hidden ? obre() : tanca(); });
  x.addEventListener('click', tanca);
  ov.addEventListener('click', function (e) { if (e.target === ov) tanca(); });
  document.addEventListener('keydown', function (e) {
    if (ov.hidden) return;
    if (e.key === 'Escape') { tanca(); return; }
    if (e.key !== 'Tab') return;
    var focusables = ov.querySelectorAll('a[href],button');
    var primer = focusables[0], darrer = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === primer) { e.preventDefault(); darrer.focus(); }
    else if (!e.shiftKey && document.activeElement === darrer) { e.preventDefault(); primer.focus(); }
  });
})();
