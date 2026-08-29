#!/usr/bin/env python3
"""Genera js/mapa.js: el mapa de navegació complet darrere del botó ≡.

És la quarta decisió tancada de «L'estètica definitiva» (25/08/2026): un sol
botó ≡ que no es perd mai, a totes les capçaleres. El component és
autocontingut —el JavaScript injecta el botó, l'estil i el diàleg— perquè
cap de les ~480 pàgines necessiti tocar la seva capçalera: només carregar
aquest fitxer (ho fa scripts/mapa-aplica.py).

L'arbre és el mateix de sis branques del menú de la portada, i les adreces
de cada idioma surten de i18n/routes.yml: si una ruta canvia de nom, es
regenera i ja està. Regenerar:

    python3 scripts/build-mapa.py
"""

import json
from pathlib import Path

import yaml

ARREL = Path(__file__).resolve().parent.parent

# L'arbre canònic, en català i amb la ruta catalana. Les etiquetes ES/EN
# segueixen el vocabulari de i18n/etiquetes.yml (Calendari · Calendario ·
# Calendar). /dossier-patrocinis/ i /admin/ no hi són: l'un és una
# redirecció noindex i l'altre és intern.
ARBRE = [
    ("Juga al Barna", "Juega en el Barna", "Play at Barna", [
        ("/escoleta/", "Escoleta", "Escoleta", "Escoleta"),
        ("/basquet-formatiu/", "Bàsquet formatiu", "Baloncesto formativo", "Development basketball"),
        ("/portes-obertes/", "Portes obertes", "Puertas abiertas", "Open days"),
        ("/femeni/", "Bàsquet femení", "Baloncesto femenino", "Women's basketball"),
        ("/magics/", "Barna Màgics", "Barna Màgics", "Barna Màgics"),
        ("/faq/", "Preguntes freqüents", "Preguntas frecuentes", "FAQ"),
    ]),
    ("Equips i temporada", "Equipos y temporada", "Teams and season", [
        ("/partits/equips/", "Equips", "Equipos", "Teams"),
        ("/partits/", "Calendari", "Calendario", "Calendar"),
        ("/partits/calendaris/", "Calendari per equip", "Calendario por equipo", "Calendar by team"),
        ("/fotos/", "Galeria de fotos", "Galería de fotos", "Photo gallery"),
    ]),
    ("Activitats", "Actividades", "Activities", [
        ("/campus/", "Campus de bàsquet", "Campus de baloncesto", "Basketball camp"),
        ("/tecnificacio-basquet-barcelona/", "Tecnificació", "Tecnificación", "Skills training"),
        ("/3x3/", "Torneig 3x3", "Torneo 3x3", "3x3 tournament"),
        ("/cistella-petita/", "Cistella Petita", "Cistella Petita", "Cistella Petita"),
    ]),
    ("El Club", "El Club", "The Club", [
        ("/club/", "Qui som", "Quiénes somos", "Who we are"),
        ("/historia/", "Història", "Historia", "History"),
        ("/palmares/", "Palmarès", "Palmarés", "Honours"),
        ("/organigrama/", "Organigrama", "Organigrama", "Organisation"),
        ("/instal-lacions/", "Instal·lacions", "Instalaciones", "Facilities"),
        ("/grup-barna-dades-oficials/", "Dades oficials", "Datos oficiales", "Official data"),
        ("/proteccio-menor/", "Protecció del menor", "Protección del menor", "Child protection"),
        ("/documents/", "Documents", "Documentos", "Documents"),
        ("/posicionament/", "Posicionament del club", "Posicionamiento del club", "Club positioning"),
    ]),
    ("Actualitat", "Actualidad", "News", [
        ("/blog/", "Coneixement Barna", "Conocimiento Barna", "Barna knowledge"),
        ("/video/", "Vídeo", "Vídeo", "Videos"),
        ("/premsa/", "Premsa", "Prensa", "Press"),
        ("/premsa/moments/", "Moments a Instagram", "Momentos en Instagram", "Instagram highlights"),
        ("/premidonaesport/", "Premi Dona i Esport", "Premi Dona i Esport", "Premi Dona i Esport"),
    ]),
    ("Empreses", "Empresas", "Companies", [
        ("/empreses/", "Empreses", "Empresas", "Companies"),
        ("/patrocinadors/", "Partners", "Partners", "Partners"),
        ("/avantatges-familia/", "Avantatges de la família", "Ventajas de la familia", "Family benefits"),
        ("/partners-mapa/", "Mapa de partners", "Mapa de partners", "Partner map"),
        ("/briefing/", "Briefing del club", "Briefing del club", "Club briefing"),
    ]),
]

TEXTOS = {
    "ca": {"obre": "Obre el mapa del web", "titol": "Tot el web", "tanca": "Tanca",
           "cerca": "Cercar al web", "inici": "Inici"},
    "es": {"obre": "Abre el mapa de la web", "titol": "Toda la web", "tanca": "Cerrar",
           "cerca": "Buscar en la web", "inici": "Inicio"},
    "en": {"obre": "Open the site map", "titol": "The whole site", "tanca": "Close",
           "cerca": "Search the site", "inici": "Home"},
}

INICI = {"ca": "/", "es": "/es/", "en": "/en/"}
CERCA = {"ca": "/cerca/", "es": "/es/busqueda/", "en": "/en/search/"}


def carrega_rutes():
    rutes = yaml.safe_load((ARREL / "i18n" / "routes.yml").read_text())["rutes"]
    return {r["ca"]: r for r in rutes}


def construeix_dades():
    idx = carrega_rutes()
    dades = {}
    for lang, li in (("ca", 1), ("es", 2), ("en", 3)):
        cols = []
        for branca in ARBRE:
            titol = branca[li - 1] if lang == "ca" else branca[{"es": 1, "en": 2}[lang]]
            enllacos = []
            for ruta_ca, ca, es, en in branca[3]:
                etiqueta = {"ca": ca, "es": es, "en": en}[lang]
                r = idx.get(ruta_ca)
                url = ruta_ca if lang == "ca" else (r[lang] if r else ruta_ca)
                enllacos.append([url, etiqueta])
            cols.append([branca[0] if lang == "ca" else titol, enllacos])
        dades[lang] = {
            "t": TEXTOS[lang], "cols": cols,
            "inici": INICI[lang], "cerca": CERCA[lang],
        }
    return dades


PLANTILLA = r"""/* Mapa de navegació · generat per scripts/build-mapa.py — NO editar a mà.
   Un sol botó ≡ a totes les capçaleres («L'estètica definitiva», decisió 4).
   Autocontingut: injecta botó, estil i diàleg. */
(function () {
  'use strict';
  if (document.getElementById('mapa-btn')) return;
  var DADES = __DADES__;
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
  if (seu) {
    seu.insertBefore(btn, seu.firstChild);
    // Algunes capçaleres ja anaven plenes: si el botó fa vessar la pàgina
    // per la dreta (p. ex. /partits/ a 1280), passa a flotant i no trenca res.
    var doc = document.documentElement;
    if (doc.scrollWidth > doc.clientWidth) {
      seu.removeChild(btn);
      btn.className = 'mapa-flotant';
      document.body.appendChild(btn);
    }
  } else { btn.className = 'mapa-flotant'; document.body.appendChild(btn); }

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
"""


def main():
    dades = construeix_dades()
    js = PLANTILLA.replace("__DADES__", json.dumps(dades, ensure_ascii=True))
    (ARREL / "js" / "mapa.js").write_text(js)
    print(f"js/mapa.js · {len(js)} bytes · 3 idiomes, {len(ARBRE)} branques")


if __name__ == "__main__":
    main()
