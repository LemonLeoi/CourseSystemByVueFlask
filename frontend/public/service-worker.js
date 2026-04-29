// 缓存名称和版本
const CACHE_NAME = 'school-management-v1';

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
  
  // 对于API请求，使用网络优先策略
  if (url.pathname.startsWith('/api/')) {
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
  } 
  // 对于静态资源，使用缓存优先策略
  else {
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
  }
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
    
    // 清空已同步的数据
    await clearSyncData();
    
    // 通知客户端同步完成
    const clients = await self.clients.matchAll();
    clients.forEach(client => {
      client.postMessage({ type: 'SYNC_COMPLETE' });
    });
  } catch (error) {
    console.error('同步数据失败:', error);
  }
}

// 获取待同步数据（模拟）
async function getSyncData() {
  // 实际项目中，这里应该从IndexedDB获取待同步数据
  return [];
}

// 清空已同步数据（模拟）
async function clearSyncData() {
  // 实际项目中，这里应该清空IndexedDB中的待同步数据
}
