import { ref, computed } from 'vue';

export interface CrudOptions<T extends Record<string, any>> {
  initialData?: T[];
  primaryKey?: keyof T;
  onSuccess?: (action: string, data: boolean | T | T[] | number) => void;
  onError?: (error: any) => void;
  useMockData?: boolean;
  mockDelay?: number;
}

export interface PaginationOptions {
  page: number;
  pageSize: number;
  total: number;
}

export interface SearchOptions<T extends Record<string, any>> {
  query: string;
  fields: (keyof T)[];
}

export function useCrudOperations<T extends Record<string, any>>(
  _resourceEndpoint: string,
  options: CrudOptions<T> = {}
) {
  // 配置默认值
  const primaryKey = options.primaryKey || 'id' as keyof T;
  const useMockData = options.useMockData ?? true;
  const mockDelay = options.mockDelay ?? 500;

  // 状态管理
  const list = ref<T[]>(options.initialData || []);
  const currentItem = ref<T | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);
  const pagination = ref<PaginationOptions>({
    page: 1,
    pageSize: 10,
    total: options.initialData?.length || 0
  });
  const searchOptions = ref<SearchOptions<T> | null>(null);
  const filters = ref<Record<string, any>>({});

  // 计算属性
  const filteredList = computed(() => {
    let result = [...list.value];

    // 应用搜索
    if (searchOptions.value) {
      const { query, fields } = searchOptions.value;
      if (query) {
        const lowerQuery = query.toLowerCase();
        result = result.filter(item => {
          return fields.some(field => {
            const value = (item as any)[field];
            return String(value).toLowerCase().includes(lowerQuery);
          });
        });
      }
    }

    // 应用筛选
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        result = result.filter(item => {
          const itemValue = (item as any)[key];
          return itemValue === value;
        });
      }
    });

    // 更新总条数
    pagination.value.total = result.length;

    // 应用分页
    const startIndex = (pagination.value.page - 1) * pagination.value.pageSize;
    const endIndex = startIndex + pagination.value.pageSize;
    return result.slice(startIndex, endIndex);
  });

  /**
   * 获取指定ID的项
   * @param id 主键值
   * @returns 找到的项或undefined
   */
  const getItem = (id: any): T | undefined => {
    return list.value.find(item => (item as any)[primaryKey] === id) as T | undefined;
  };

  /**
   * 获取指定ID项的索引
   * @param id 主键值
   * @returns 索引或-1
   */
  const getItemIndex = (id: any): number => {
    return list.value.findIndex(item => (item as any)[primaryKey] === id);
  };

  /**
   * 获取列表数据
   */
  const fetch = async () => {
    loading.value = true;
    error.value = null;
    try {
      if (useMockData) {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, mockDelay));
        
        if (options.initialData) {
          list.value = [...options.initialData];
        }
      } else {
        // 实际API调用（需要根据项目实际情况实现）
        // const response = await api.get(resourceEndpoint, {
        //   params: {
        //     ...filters.value,
        //     page: pagination.value.page,
        //     pageSize: pagination.value.pageSize,
        //     search: searchOptions.value?.query
        //   }
        // });
        // list.value = response.data.items;
        // pagination.value.total = response.data.total;
      }
      
      options.onSuccess?.('fetch', list.value as T[]);
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      options.onError?.(err);
    } finally {
      loading.value = false;
    }
  };

  /**
   * 创建新项
   * @param item 要创建的项
   * @returns 创建的项或null
   */
  const create = async (item: Omit<T, keyof T>) => {
    loading.value = true;
    error.value = null;
    try {
      let newItem: T;

      if (useMockData) {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, mockDelay));
        
        // 生成主键
        const idValue = typeof primaryKey === 'string' && primaryKey === 'id' 
          ? Date.now() 
          : `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        newItem = {
          ...item,
          [primaryKey]: idValue
        } as T;
      } else {
        // 实际API调用
        // const response = await api.post(resourceEndpoint, item);
        // newItem = response.data;
        throw new Error('实际API调用未实现');
      }
      
      list.value.push(newItem as any);
      currentItem.value = newItem;
      pagination.value.total = list.value.length;
      options.onSuccess?.('create', newItem);
      return newItem;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      options.onError?.(err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 更新项
   * @param id 主键值
   * @param item 要更新的部分
   * @returns 更新后的项或null
   */
  const update = async (id: any, item: Partial<T>) => {
    loading.value = true;
    error.value = null;
    try {
      let updatedItem: T;

      if (useMockData) {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, mockDelay));
        
        const index = getItemIndex(id);
        if (index === -1) {
          throw new Error('未找到要更新的项');
        }
        
        updatedItem = {
          ...list.value[index],
          ...item
        } as T;
        list.value[index] = updatedItem as any;
      } else {
        // 实际API调用
        // const response = await api.put(`${resourceEndpoint}/${id}`, item);
        // updatedItem = response.data;
        // const index = getItemIndex(id);
        // if (index !== -1) {
        //   list.value[index] = updatedItem;
        // }
        throw new Error('实际API调用未实现');
      }
      
      currentItem.value = updatedItem;
      options.onSuccess?.('update', updatedItem);
      return updatedItem;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      options.onError?.(err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 删除项
   * @param id 主键值
   * @returns 是否删除成功
   */
  const remove = async (id: any): Promise<boolean> => {
    loading.value = true;
    error.value = null;
    try {
      if (useMockData) {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, mockDelay));
        
        const index = getItemIndex(id);
        if (index === -1) {
          throw new Error('未找到要删除的项');
        }
        
        const deletedItem = list.value[index];
        list.value.splice(index, 1);
        pagination.value.total = list.value.length;
        options.onSuccess?.('delete', deletedItem as T);
      } else {
        // 实际API调用
        // await api.delete(`${resourceEndpoint}/${id}`);
        // const index = getItemIndex(id);
        // if (index !== -1) {
        //   list.value.splice(index, 1);
        //   pagination.value.total = list.value.length;
        // }
        throw new Error('实际API调用未实现');
      }
      
      return true;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      options.onError?.(err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 批量删除
   * @param ids 主键值数组
   * @returns 删除成功的数量
   */
  const batchDelete = async (ids: any[]): Promise<number> => {
    loading.value = true;
    error.value = null;
    let successCount = 0;

    try {
      for (const id of ids) {
        const success = await remove(id);
        if (success) successCount++;
      }
      
      options.onSuccess?.('batchDelete', successCount);
      return successCount;
    } catch (err) {
      error.value = err instanceof Error ? err : new Error(String(err));
      options.onError?.(err);
      return successCount;
    } finally {
      loading.value = false;
    }
  };

  /**
   * 设置搜索选项
   * @param options 搜索选项
   */
  const setSearchOptions = (options: SearchOptions<T>) => {
    searchOptions.value = options;
    pagination.value.page = 1; // 重置页码
  };

  /**
   * 清除搜索
   */
  const clearSearch = () => {
    searchOptions.value = null;
    pagination.value.page = 1;
  };

  /**
   * 设置筛选条件
   * @param newFilters 筛选条件
   */
  const setFilters = (newFilters: Record<string, any>) => {
    filters.value = { ...newFilters };
    pagination.value.page = 1;
  };

  /**
   * 清除筛选
   */
  const clearFilters = () => {
    filters.value = {};
    pagination.value.page = 1;
  };

  /**
   * 设置分页
   * @param page 页码
   * @param pageSize 每页大小
   */
  const setPagination = (page: number, pageSize?: number) => {
    pagination.value.page = page;
    if (pageSize !== undefined) {
      pagination.value.pageSize = pageSize;
    }
  };

  /**
   * 重置状态
   */
  const reset = () => {
    list.value = options.initialData || [];
    currentItem.value = null;
    error.value = null;
    pagination.value = {
      page: 1,
      pageSize: 10,
      total: options.initialData?.length || 0
    };
    searchOptions.value = null;
    filters.value = {};
  };

  return {
    // 状态
    list,
    filteredList,
    currentItem,
    loading,
    error,
    pagination,
    
    // 方法
    fetch,
    create,
    update,
    delete: remove,
    batchDelete,
    getItem,
    setSearchOptions,
    clearSearch,
    setFilters,
    clearFilters,
    setPagination,
    reset
  };
}
