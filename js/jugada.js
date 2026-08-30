/* CB Grup Barna · Proposta C «La Jugada» · el rellotge de possessió
   ─────────────────────────────────────────────────────────────────────
   Fa tres feines a /escoleta/ i les seves traduccions:

     1. Planta el rellotge de possessió a dalt de la pàgina i el fa
        baixar de :24.0 a :00.0 a mesura que es fa scroll. Quan arriba a
        zero, la barra es torna vermella: la jugada ha entrat.
     2. Reparteix els segons entre els trams de la història
        (data-jugada="El primer bot") i els hi escriu el marcador.
     3. Revela cada tram quan entra a la pantalla.

   Es pinta amb JavaScript, com l'avís de galetes i el botó ≡, perquè el
   marcatge de les tres pàgines no s'hagi de tocar tram per tram — i
   perquè si el JavaScript no arriba, la pàgina segueix sencera i
   llegible: el rellotge és un adorn, no el contingut.

   Amb prefers-reduced-motion no hi ha ni compte enrere ni revelat: tot
   surt quiet i complet, que és la regla del sistema.
   ───────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var trams = [].slice.call(document.querySelectorAll('[data-jugada]'));
  if (!trams.length) return;

  var codi = (document.documentElement.lang || 'ca').slice(0, 2).toLowerCase();
  var ETIQUETA = {
    ca: 'Possessió · CB Grup Barna',
    es: 'Posesión · CB Grup Barna',
    en: 'Shot clock · CB Grup Barna'
  };

  var quiet = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. Els segons de cada tram ─────────────────────────────────── */

  /* Repartits de :24 fins a :00 pel nombre de trams que hi hagi, així
     afegir o treure una secció de la pàgina no obliga a recalcular res
     a mà. L'últim tram és sempre el :00, la cistella. */
  var n = trams.length;
  trams.forEach(function (sec, i) {
    var seg = n === 1 ? 0 : Math.round(24 - (24 * i) / (n - 1));
    var marca = document.createElement('span');
    marca.className = 'jug-tm';
    marca.setAttribute('aria-hidden', 'true');
    marca.textContent = ':' + (seg < 10 ? '0' : '') + seg;

    var nom = sec.getAttribute('data-jugada');
    if (nom) {
      var petit = document.createElement('small');
      petit.textContent = nom;
      marca.appendChild(petit);
    }

    // Dins del .wrap, davant del títol: així el marcador queda alineat
    // amb el text i no amb la vora de la pantalla.
    var caixa = sec.querySelector('.wrap') || sec;
    var titol = caixa.querySelector('h2');
    if (titol) caixa.insertBefore(marca, titol);
    else caixa.insertBefore(marca, caixa.firstChild);

    if (!quiet) sec.classList.add('jug-reveal');
  });

  /* ── 2. El revelat ──────────────────────────────────────────────── */

  if (quiet || !('IntersectionObserver' in window)) {
    trams.forEach(function (s) { s.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entrades) {
      entrades.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    trams.forEach(function (s) { io.observe(s); });
  }

  /* ── 3. El rellotge ─────────────────────────────────────────────── */

  var barra = document.createElement('div');
  barra.className = 'jug-clock';
  barra.setAttribute('role', 'presentation');

  var etiqueta = document.createElement('span');
  etiqueta.className = 'lbl';
  etiqueta.textContent = ETIQUETA[codi] || ETIQUETA.ca;

  var xifra = document.createElement('span');
  xifra.className = 't';
  xifra.textContent = ':24.0';

  barra.appendChild(etiqueta);
  barra.appendChild(xifra);

  /* L'alcada real de la barra del web. Al mobil fa dues linies, aixi que
     no es pot escriure un numero al full d'estil i confiar-hi. */
  function mesuraBarra() {
    var barraWeb = document.querySelector('.langbar');
    if (!barraWeb) return;
    var alt = Math.round(barraWeb.getBoundingClientRect().height);
    if (alt > 0) document.documentElement.style.setProperty('--jug-top', alt + 'px');
  }

  function planta() {
    // Sota l'avís de campanya si n'hi ha, però abans de tot el contingut:
    // el rellotge ha de ser el primer que es veu de la pàgina.
    var avis = document.querySelector('.cbgb-po');
    if (avis && avis.nextSibling) document.body.insertBefore(barra, avis.nextSibling);
    else if (document.body.firstChild) document.body.insertBefore(barra, document.body.firstChild);
    else document.body.appendChild(barra);
  }

  function arrenca() { planta(); mesuraBarra(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrenca);
  } else {
    arrenca();
  }
  window.addEventListener('resize', mesuraBarra, { passive: true });

  if (quiet) return;

  var demanat = false;
  function actualitza() {
    demanat = false;
    var doc = document.documentElement;
    // El recorregut útil és tot el que es pot fer scroll. Si la pàgina
    // no arriba a omplir la pantalla no hi ha possessió a comptar.
    var recorregut = doc.scrollHeight - window.innerHeight;
    if (recorregut <= 0) return;
    var p = Math.min(1, Math.max(0, (window.pageYOffset || doc.scrollTop) / recorregut));
    var t = 24 * (1 - p);
    xifra.textContent = ':' + (t < 10 ? '0' : '') + t.toFixed(1);
    barra.classList.toggle('zero', t <= 0.05);
  }

  window.addEventListener('scroll', function () {
    if (!demanat) { demanat = true; requestAnimationFrame(actualitza); }
  }, { passive: true });
  window.addEventListener('resize', function () {
    if (!demanat) { demanat = true; requestAnimationFrame(actualitza); }
  }, { passive: true });
  actualitza();
})();
