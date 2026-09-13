/* CB Grup Barna · Comptador de la campanya de setembre
   ───────────────────────────────────────────────────────────────
   Pinta les tres xifres del bloc #compte-2018 de la portada:

     · els DIES que falten, calculats aquí des de data-fins;
     · les PLACES LLIURES del grup de noies del 2018;
     · els APUNTATS de portes obertes del setembre, amb la barra.

   Els dies no depenen de ningú. Les altres dues xifres surten del
   full de reserves si `comptadorEndpoint` està configurat a
   js/canals.js (vegeu scripts/apps-script-comptador.gs); si no hi
   és, o si la crida falla, es queden els números escrits als data-
   del bloc, que és el que ja hi ha a l'HTML. Mai es buida ni surt
   un «carregant…» que es quedi penjat.

   La lectura es fa amb JSONP perquè una Apps Script desplegada com
   a aplicació web redirigeix a un altre domini i una crida normal
   hi queda bloquejada. No s'hi envia res: només es demana el número.
   ─────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var c = document.getElementById('compte-2018');
  if (!c) return;

  /* ── 1 · Els dies ─────────────────────────────────────────── */
  var elDies = c.querySelector('[data-dies]');
  var fins = c.getAttribute('data-fins');
  if (elDies && fins) {
    var avui = new Date(); avui.setHours(0, 0, 0, 0);
    var dia = new Date(fins + 'T00:00:00');
    var dies = Math.round((dia - avui) / 86400000);
    elDies.textContent = dies > 0 ? dies : 0;
    if (dies <= 0) c.setAttribute('data-avui', 'si');
  }

  /* ── 2 · Les places, si hi ha d'on llegir-les ─────────────── */
  var url = (window.CANALS || {}).comptadorEndpoint;
  if (!url) return;

  var elLliures = c.querySelector('[data-lliures-n]');
  var elGrup = c.querySelectorAll('[data-grup-n]');
  var elPct = c.querySelector('[data-pct]');
  var elApuntats = c.querySelectorAll('[data-apuntats-n]');
  var elPlaces = c.querySelectorAll('[data-places-n]');
  var barra = c.querySelector('.compte-barra');
  var franja = barra ? barra.querySelector('i') : null;

  function enter(v, min, max) {
    var n = parseInt(v, 10);
    if (isNaN(n)) return null;
    return Math.min(max, Math.max(min, n));
  }
  function escriu(llista, valor) {
    Array.prototype.forEach.call(llista, function (el) { el.textContent = valor; });
  }

  window.cbgbComptador = function (d) {
    if (!d || d.ok === false) return;

    var grup = enter(d.grup, 1, 999);
    var lliures = enter(d.lliures, 0, grup || 999);
    var places = enter(d.places, 1, 9999);
    var apuntats = enter(d.apuntats, 0, places || 9999);

    if (lliures !== null && elLliures) {
      elLliures.textContent = lliures;
      c.setAttribute('data-lliures', lliures);
    }
    if (grup !== null) { escriu(elGrup, grup); c.setAttribute('data-grup', grup); }
    if (apuntats !== null) { escriu(elApuntats, apuntats); c.setAttribute('data-apuntats', apuntats); }
    if (places !== null) { escriu(elPlaces, places); c.setAttribute('data-places', places); }

    if (apuntats !== null && places) {
      var pct = Math.round(apuntats * 100 / places);
      if (elPct) elPct.textContent = pct + '%';
      if (franja) franja.style.width = pct + '%';
      if (barra) barra.setAttribute('aria-label', apuntats + ' / ' + places + ' · ' + pct + '%');
    }
  };

  var sc = document.createElement('script');
  sc.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'callback=cbgbComptador';
  sc.async = true;
  /* Si no carrega, no passa res: els números de l'HTML es queden. */
  sc.onerror = function () { sc.remove(); };
  document.head.appendChild(sc);
})();
