// API服务测试用例
import { fetchApi } from './apiService';
import { offlineStorageService } from '../data/offlineStorageService';

// 模拟navigator.onLine
Object.defineProperty(navigator, 'onLine', {
  writable: true,
  value: true
});

// 模拟fetch
const mockFetch = jest.fn();
global.fetch = mockFetch;

// 测试套件
describe('apiService', () => {
  // 测试网络在线时的行为
  describe('when online', () => {
    beforeEach(() => {
      // 设置网络在线
      navigator.onLine = true;
      // 清空模拟
      mockFetch.mockClear();
      // 清空本地存储
      return offlineStorageService.clearStore('app-state');
    });

    it('should fetch data from server and cache it', async () => {
      // 模拟成功响应
      const mockResponse = {
        ok: true,
        json: () => Promise.resolve({ data: { id: 1, name: 'Test Course' } })
      };
      mockFetch.mockResolvedValue(mockResponse);

      // 调用API
      const result = await fetchApi('/courses/1');

      // 验证结果
      expect(result).toEqual({ id: 1, name: 'Test Course' });
      expect(mockFetch).toHaveBeenCalledWith('http://localhost:5000/api/courses/1', expect.any(Object));

      // 验证数据已缓存
      const cachedData = await offlineStorageService.getAppState('GET:/courses/1:');
      expect(cachedData).toEqual({ id: 1, name: 'Test Course' });
    });

    it('should use cached data when server request fails', async () => {
      // 先缓存数据
      await offlineStorageService.storeAppState('GET:/courses/1:', { id: 1, name: 'Cached Course' });

      // 模拟失败响应
      const mockResponse = {
        ok: false,
        json: () => Promise.resolve({ error: 'Server error' })
      };
      mockFetch.mockResolvedValue(mockResponse);

      // 调用API
      const result = await fetchApi('/courses/1');

      // 验证结果
      expect(result).toEqual({ id: 1, name: 'Cached Course' });
      expect(mockFetch).toHaveBeenCalledWith('http://localhost:5000/api/courses/1', expect.any(Object));
    });
  });

  // 测试网络离线时的行为
  describe('when offline', () => {
    beforeEach(() => {
      // 设置网络离线
      navigator.onLine = false;
      // 清空模拟
      mockFetch.mockClear();
    });

    it('should use cached data for GET requests', async () => {
      // 先缓存数据
      await offlineStorageService.storeAppState('GET:/courses/1:', { id: 1, name: 'Cached Course' });

      // 调用API
      const result = await fetchApi('/courses/1');

      // 验证结果
      expect(result).toEqual({ id: 1, name: 'Cached Course' });
      expect(mockFetch).not.toHaveBeenCalled();
    });

    it('should add non-GET requests to sync queue', async () => {
      // 清空同步队列
      await offlineStorageService.clearSyncQueue();

      // 调用API
      await fetchApi('/courses/', {
        method: 'POST',
        body: JSON.stringify({ name: 'New Course', subject: 'Math' })
      });

      // 验证同步队列
      const syncQueue = await offlineStorageService.getSyncQueue();
      expect(syncQueue.length).toBe(1);
      expect(syncQueue[0].url).toBe('/courses/');
      expect(syncQueue[0].method).toBe('POST');
      expect(syncQueue[0].data).toEqual({ name: 'New Course', subject: 'Math' });
      expect(mockFetch).not.toHaveBeenCalled();
    });

    it('should throw error for GET requests with no cached data', async () => {
      // 确保没有缓存数据
      await offlineStorageService.clearStore('app-state');

      // 调用API
      await expect(fetchApi('/courses/1')).rejects.toThrow('网络离线且无缓存数据');
      expect(mockFetch).not.toHaveBeenCalled();
    });
  });
});
