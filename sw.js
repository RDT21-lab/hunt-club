/* Hunt Club — se guarda entero en el móvil para poder jugar sin cobertura.
   VERSION la pone build.py a partir del contenido: al cambiar algo, la caché
   vieja se tira sola en la siguiente apertura. */
const VERSION = 'f56f4661d7';
const CACHE = 'hunt-club-' + VERSION;
const FICHEROS = [
  './', './index.html', './manifest.webmanifest', './assets/icon.webp',
  ...['villa','casa','monasterio','cuartel','cortijo','tren','antartida','orbital']
      .flatMap(n => [`./assets/amb-${n}.webp`, `./assets/tab-${n}.webp`])
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHEROS)).then(() => self.skipWaiting()));
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
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;  // las tipografías van por su cuenta
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      if (res.ok) { const copia = res.clone(); caches.open(CACHE).then(c => c.put(e.request, copia)); }
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
