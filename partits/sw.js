/* Service worker CBGB Partits.
   Regla: les dades sempre fresques i, si no hi ha xarxa, la darrera còpia.
   L'app (HTML, CSS, JS) es serveix de la cache però es refresca en segon pla,
   perquè qui la tingui instal·lada rebi les millores sense haver de reinstal·lar. */
const VERSION = 'v2';
const CACHE = `cbgb-partits-${VERSION}`;
const SHELL = ['./', './manifest.json', '../icon-192.png', '../icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.allSettled(SHELL.map(u => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;

  // Dades: xarxa primer, cache com a reserva offline.
  if (url.pathname.endsWith('data.json') || url.pathname.endsWith('rivals.json')) {
    e.respondWith(
      fetch(e.request)
        .then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); return r; })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // App: resposta immediata de la cache i actualització en segon pla
  // (stale-while-revalidate). Així una versió nova arriba a la següent visita.
  e.respondWith(
    caches.match(e.request).then(hit => {
      const net = fetch(e.request)
        .then(r => {
          if (r && r.ok) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); }
          return r;
        })
        .catch(() => hit);
      return hit || net;
    })
  );
});

// Permet forçar l'actualització des de la pàgina.
self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});
