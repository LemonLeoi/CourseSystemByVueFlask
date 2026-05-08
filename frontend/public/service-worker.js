// 缓存名称和版本
const CACHE_NAME = 'school-management-v3';

// 需要预缓存的核心静态资源
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/static/img/logo.png',
  '/assets/vue.svg'
];

// 安装事件 - 预缓存核心资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('缓存已打开，正在添加预缓存资源');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.filter((cacheName) => {
          return cacheName !== CACHE_NAME;
        }).map((cacheName) => {
          return caches.delete(cacheName);
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 拦截网络请求
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // 跳过同源请求和非http/https请求
  if (url.origin !== location.origin || !url.protocol.startsWith('http')) {
    return;
  }

  // 对于API请求，使用网络优先策略
  if (url.pathname.startsWith('/api/')) {
    // 只缓存 GET 请求的 API 响应，不缓存 POST 请求
    if (event.request.method === 'GET') {
      event.respondWith(
        fetch(event.request)
          .then((response) => {
            // 缓存成功的API响应
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
            return response;
          })
          .catch(() => {
            // 网络请求失败时，尝试从缓存中获取
            return caches.match(event.request);
          })
      );
    } else {
      // 对于非 GET 请求（如 POST），直接使用网络请求，不尝试缓存
      event.respondWith(fetch(event.request));
    }
    return;
  }

  // 对于静态资源（.js, .css, .png, .jpg, .svg等），使用缓存优先策略
  if (url.pathname.match(/\.(js|css|png|jpg|jpeg|svg|woff|woff2|ttf|eot)$/)) {
    event.respondWith(
      caches.match(event.request)
        .then((response) => {
          return response || fetch(event.request).then((response) => {
            // 缓存新的静态资源
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseToCache);
            });
            return response;
          });
        })
    );
    return;
  }

  // 对于HTML页面，使用网络优先策略，确保获取最新内容
  if (url.pathname.endsWith('.html') || url.pathname === '/') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // 缓存HTML响应
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
          return response;
        })
        .catch(() => {
          // 网络请求失败时，尝试从缓存中获取
          return caches.match(event.request);
        })
    );
    return;
  }

  // 对于其他请求（如前端路由），直接使用网络请求，不尝试缓存
  event.respondWith(fetch(event.request));
});

// 后台同步事件 - 用于网络恢复时的数据同步
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

// 数据同步函数
async function syncData() {
  try {
    // 获取待同步的数据
    const syncData = await getSyncData();

    // 遍历同步数据并发送请求
    for (const item of syncData) {
      await fetch(item.url, {
        method: item.method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(item.data)
      });
    }
  } catch (error) {
    console.error('数据同步失败:', error);
  }
}

// 从本地存储中获取待同步的数据
async function getSyncData() {
  // 实现获取待同步数据的逻辑
  return [];
}

// 消息监听 - 用于与主线程通信
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});