/* CB Grup Barna · Reels i publicacions d'Instagram incrustats
   ───────────────────────────────────────────────────────────────
   Abans calia clicar cada vídeo per veure'l. Ningú ho feia: la
   pàgina del campus semblava plena de caixes negres.

   Ara es carreguen SOLS, però no tots de cop: cada incrustació
   s'activa quan s'acosta a la finestra. Vint-i-sis iframes
   d'Instagram carregats a l'obrir la pàgina la deixarien morta al
   mòbil; d'aquesta manera només es baixa el que la persona
   realment mira, i per a qui llegeix la pàgina el resultat és el
   mateix: els vídeos hi són.

   Si el navegador no té IntersectionObserver (molt vell), es
   carreguen igualment tots: val més pesada que buida.
   ─────────────────────────────────────────────────────────────── */
(function () {
  var botons = document.querySelectorAll('.star-play');
  if (!botons.length) return;

  function carrega(b) {
    if (b.dataset.fet === '1') return;
    b.dataset.fet = '1';
    var d = document.createElement('div');
    d.className = 'star-embed';
    // Uns són reels i uns altres publicacions de feed: data-kind="p" ho marca.
    var kind = b.dataset.kind === 'p' ? 'p' : 'reel';
    var f = document.createElement('iframe');
    f.src = 'https://www.instagram.com/' + kind + '/' + b.dataset.reel + '/embed/';
    f.loading = 'lazy';
    f.title = b.querySelector('span') ? b.querySelector('span').textContent : 'Instagram';
    f.setAttribute('allowfullscreen', '');
    f.setAttribute('allowtransparency', 'true');
    d.appendChild(f);
    b.replaceWith(d);
  }

  // Clicar segueix funcionant: si algú hi arriba abans que es carregui sol.
  botons.forEach(function (b) {
    b.addEventListener('click', function () { carrega(b); });
  });

  if (!('IntersectionObserver' in window)) {
    botons.forEach(carrega);
    return;
  }

  // 400px de marge: quan la incrustació és a punt d'entrar per baix, ja
  // s'ha demanat, i quan hi arribes l'estàs veient.
  var obs = new IntersectionObserver(function (entrades) {
    entrades.forEach(function (e) {
      if (!e.isIntersecting) return;
      obs.unobserve(e.target);
      carrega(e.target);
    });
  }, { rootMargin: '400px 0px' });

  botons.forEach(function (b) { obs.observe(b); });
})();
