const CACHE_NAME = 'school-management-v4';

const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/img/logo.png',
  '/vite.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) => Promise.all(
        cacheNames
          .filter((cacheName) => cacheName !== CACHE_NAME)
          .map((cacheName) => caches.delete(cacheName))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  if (url.origin !== location.origin || !url.protocol.startsWith('http')) {
    return;
  }

  if (url.pathname.startsWith('/api/')) {
    if (event.request.method === 'GET') {
      event.respondWith(networkFirst(event.request));
    } else {
      event.respondWith(fetch(event.request));
    }
    return;
  }

  if (url.pathname.match(/\.(js|css|png|jpg|jpeg|svg|woff|woff2|ttf|eot)$/)) {
    event.respondWith(cacheFirst(event.request));
    return;
  }

  if (url.pathname.endsWith('.html') || url.pathname === '/') {
    event.respondWith(networkFirst(event.request));
    return;
  }

  event.respondWith(fetch(event.request));
});

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    throw error;
  }
}

async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }

  const response = await fetch(request);
  const cache = await caches.open(CACHE_NAME);
  cache.put(request, response.clone());
  return response;
}

async function syncData() {
  const syncItems = await getSyncData();

  for (const item of syncItems) {
    await fetch(item.url, {
      method: item.method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(item.data)
    });
  }
}

async function getSyncData() {
  return [];
}
