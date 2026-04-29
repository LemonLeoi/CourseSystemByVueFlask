// 离线存储服务 - 使用IndexedDB

// 数据库名称和版本
const DB_NAME = 'school-management-db';
const DB_VERSION = 1;

// 存储对象名称
const STORES = {
  COURSES: 'courses',
  STUDENTS: 'students',
  TEACHERS: 'teachers',
  GRADES: 'grades',
  EXAMS: 'exams',
  SYNC_QUEUE: 'sync-queue',
  APP_STATE: 'app-state'
};

// 数据库连接实例
let db: IDBDatabase | null = null;

// 同步队列项类型
export interface SyncQueueItem {
  id?: number;
  url: string;
  method: string;
  data: Record<string, unknown>;
  timestamp: string;
}

// 应用状态项类型
export interface AppStateItem {
  key: string;
  value: unknown;
}

// 初始化数据库
async function initDatabase(): Promise<IDBDatabase> {
  if (db) return db;

  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => {
      reject(new Error('数据库打开失败'));
    };

    request.onsuccess = () => {
      db = request.result;
      resolve(db);
    };

    request.onupgradeneeded = (event) => {
      const database = (event.target as IDBOpenDBRequest).result;

      // 创建课程存储
      if (!database.objectStoreNames.contains(STORES.COURSES)) {
        database.createObjectStore(STORES.COURSES, { keyPath: 'id' });
      }

      // 创建学生存储
      if (!database.objectStoreNames.contains(STORES.STUDENTS)) {
        database.createObjectStore(STORES.STUDENTS, { keyPath: 'id' });
      }

      // 创建教师存储
      if (!database.objectStoreNames.contains(STORES.TEACHERS)) {
        database.createObjectStore(STORES.TEACHERS, { keyPath: 'id' });
      }

      // 创建成绩存储
      if (!database.objectStoreNames.contains(STORES.GRADES)) {
        database.createObjectStore(STORES.GRADES, { keyPath: 'id' });
      }

      // 创建考试存储
      if (!database.objectStoreNames.contains(STORES.EXAMS)) {
        database.createObjectStore(STORES.EXAMS, { keyPath: 'id' });
      }

      // 创建同步队列存储
      if (!database.objectStoreNames.contains(STORES.SYNC_QUEUE)) {
        database.createObjectStore(STORES.SYNC_QUEUE, { keyPath: 'id', autoIncrement: true });
      }

      // 创建应用状态存储
      if (!database.objectStoreNames.contains(STORES.APP_STATE)) {
        database.createObjectStore(STORES.APP_STATE, { keyPath: 'key' });
      }
    };
  });
}

// 存储数据
async function storeData<T extends { id?: string | number }>(storeName: string, data: T): Promise<void> {
  const database = await initDatabase();
  return new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    const request = store.put(data);

    request.onerror = () => {
      reject(new Error('数据存储失败'));
    };

    request.onsuccess = () => {
      resolve();
    };
  });
}

// 获取数据
async function getData<T extends { id?: string | number }>(storeName: string, key: string | number): Promise<T | null> {
  const database = await initDatabase();
  return new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readonly');
    const store = transaction.objectStore(storeName);
    const request = store.get(key);

    request.onerror = () => {
      reject(new Error('数据获取失败'));
    };

    request.onsuccess = () => {
      resolve(request.result as T | null);
    };
  });
}

// 获取所有数据
async function getAllData<T>(storeName: string): Promise<T[]> {
  const database = await initDatabase();
  return new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readonly');
    const store = transaction.objectStore(storeName);
    const request = store.getAll();

    request.onerror = () => {
      reject(new Error('数据获取失败'));
    };

    request.onsuccess = () => {
      resolve(request.result as T[]);
    };
  });
}

// 删除数据
async function deleteData(storeName: string, key: string | number): Promise<void> {
  const database = await initDatabase();
  return new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    const request = store.delete(key);

    request.onerror = () => {
      reject(new Error('数据删除失败'));
    };

    request.onsuccess = () => {
      resolve();
    };
  });
}

// 清空存储
async function clearStore(storeName: string): Promise<void> {
  const database = await initDatabase();
  return new Promise((resolve, reject) => {
    const transaction = database.transaction(storeName, 'readwrite');
    const store = transaction.objectStore(storeName);
    const request = store.clear();

    request.onerror = () => {
      reject(new Error('存储清空失败'));
    };

    request.onsuccess = () => {
      resolve();
    };
  });
}

// 添加到同步队列
async function addToSyncQueue(data: {
  url: string;
  method: string;
  data: Record<string, unknown>;
}): Promise<void> {
  const syncItem: SyncQueueItem = {
    ...data,
    timestamp: new Date().toISOString()
  };
  await storeData(STORES.SYNC_QUEUE, syncItem);
}

// 获取同步队列
async function getSyncQueue(): Promise<SyncQueueItem[]> {
  return await getAllData<SyncQueueItem>(STORES.SYNC_QUEUE);
}

// 清空同步队列
async function clearSyncQueue(): Promise<void> {
  await clearStore(STORES.SYNC_QUEUE);
}

// 存储应用状态
async function storeAppState(key: string, value: unknown): Promise<void> {
  await storeData<AppStateItem & { id: string }>(STORES.APP_STATE, { key, value, id: key });
}

// 获取应用状态
async function getAppState(key: string): Promise<unknown | null> {
  const state = await getData<AppStateItem & { id: string }>(STORES.APP_STATE, key);
  return state ? state.value : null;
}

// 导出离线存储服务
export const offlineStorageService = {
  initDatabase,
  storeData,
  getData,
  getAllData,
  deleteData,
  clearStore,
  addToSyncQueue,
  getSyncQueue,
  clearSyncQueue,
  storeAppState,
  getAppState,
  STORES
};
