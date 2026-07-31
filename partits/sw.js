/* Service worker CBGB Partits: app shell en cache, dades sempre fresques amb reserva offline. */
const CACHE = 'cbgb-partits-v1';
const SHELL = ['./', './manifest.json', '../logo.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  if (url.pathname.endsWith('data.json')) {
    // xarxa primer (dades al dia), cache si no hi ha connexió
    e.respondWith(
      fetch(e.request).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); return r; })
        .catch(() => caches.match(e.request))
    );
  } else {
    e.respondWith(
      caches.match(e.request).then(hit => hit || fetch(e.request).then(r => {
        const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); return r;
      }))
    );
  }
});
