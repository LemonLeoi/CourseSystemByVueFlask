// 离线存储服务测试用例
import { offlineStorageService } from './offlineStorageService';

// 测试套件
describe('offlineStorageService', () => {
  // 测试初始化数据库
  describe('initDatabase', () => {
    it('should initialize the database successfully', async () => {
      const db = await offlineStorageService.initDatabase();
      expect(db).toBeDefined();
      expect(db.name).toBe('school-management-db');
    });
  });

  // 测试存储和获取数据
  describe('storeData and getData', () => {
    it('should store and retrieve data successfully', async () => {
      const testData = { id: 1, name: 'Test Course', subject: 'Math' };
      await offlineStorageService.storeData('courses', testData);
      const retrievedData = await offlineStorageService.getData('courses', 1);
      expect(retrievedData).toEqual(testData);
    });
  });

  // 测试获取所有数据
  describe('getAllData', () => {
    it('should retrieve all data from a store', async () => {
      // 清空存储
      await offlineStorageService.clearStore('courses');
      
      // 添加测试数据
      const testData1 = { id: 1, name: 'Test Course 1', subject: 'Math' };
      const testData2 = { id: 2, name: 'Test Course 2', subject: 'English' };
      await offlineStorageService.storeData('courses', testData1);
      await offlineStorageService.storeData('courses', testData2);
      
      // 获取所有数据
      const allData = await offlineStorageService.getAllData('courses');
      expect(allData.length).toBe(2);
      expect(allData).toContainEqual(testData1);
      expect(allData).toContainEqual(testData2);
    });
  });

  // 测试删除数据
  describe('deleteData', () => {
    it('should delete data successfully', async () => {
      // 添加测试数据
      const testData = { id: 1, name: 'Test Course', subject: 'Math' };
      await offlineStorageService.storeData('courses', testData);
      
      // 删除数据
      await offlineStorageService.deleteData('courses', 1);
      
      // 验证数据已删除
      const retrievedData = await offlineStorageService.getData('courses', 1);
      expect(retrievedData).toBeNull();
    });
  });

  // 测试清空存储
  describe('clearStore', () => {
    it('should clear a store successfully', async () => {
      // 添加测试数据
      const testData1 = { id: 1, name: 'Test Course 1', subject: 'Math' };
      const testData2 = { id: 2, name: 'Test Course 2', subject: 'English' };
      await offlineStorageService.storeData('courses', testData1);
      await offlineStorageService.storeData('courses', testData2);
      
      // 清空存储
      await offlineStorageService.clearStore('courses');
      
      // 验证存储已清空
      const allData = await offlineStorageService.getAllData('courses');
      expect(allData.length).toBe(0);
    });
  });

  // 测试同步队列
  describe('sync queue', () => {
    it('should add items to the sync queue', async () => {
      // 清空同步队列
      await offlineStorageService.clearSyncQueue();
      
      // 添加到同步队列
      const syncItem = {
        url: '/api/courses/',
        method: 'POST',
        data: { name: 'Test Course', subject: 'Math' }
      };
      await offlineStorageService.addToSyncQueue(syncItem);
      
      // 获取同步队列
      const syncQueue = await offlineStorageService.getSyncQueue();
      expect(syncQueue.length).toBe(1);
      expect(syncQueue[0].url).toBe(syncItem.url);
      expect(syncQueue[0].method).toBe(syncItem.method);
      expect(syncQueue[0].data).toEqual(syncItem.data);
    });

    it('should clear the sync queue', async () => {
      // 添加到同步队列
      const syncItem = {
        url: '/api/courses/',
        method: 'POST',
        data: { name: 'Test Course', subject: 'Math' }
      };
      await offlineStorageService.addToSyncQueue(syncItem);
      
      // 清空同步队列
      await offlineStorageService.clearSyncQueue();
      
      // 验证同步队列已清空
      const syncQueue = await offlineStorageService.getSyncQueue();
      expect(syncQueue.length).toBe(0);
    });
  });

  // 测试应用状态存储
  describe('app state storage', () => {
    it('should store and retrieve app state', async () => {
      const testState = { user: { id: 1, name: 'Test User' }, theme: 'dark' };
      await offlineStorageService.storeAppState('userState', testState);
      const retrievedState = await offlineStorageService.getAppState('userState');
      expect(retrievedState).toEqual(testState);
    });
  });
});
