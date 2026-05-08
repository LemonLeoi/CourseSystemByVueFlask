// 基础服务接口和实现

import type { PaginatedResponse, ApiResponse } from '../types';

// 带ID的基础类型
export interface Identifiable {
  id: string;
}

// 基础CRUD服务接口
export interface IBaseService<T extends Identifiable, CreateDto = Partial<T>, UpdateDto = Partial<T>> {
  // 获取所有数据
  getAll(params?: Record<string, unknown>): Promise<ApiResponse<T[]>>;
  
  // 分页获取数据
  getPaginated(page: number, pageSize: number, params?: Record<string, unknown>): Promise<ApiResponse<PaginatedResponse<T>>>;
  
  // 根据ID获取单个数据
  getById(id: string): Promise<ApiResponse<T>>;
  
  // 创建数据
  create(data: CreateDto): Promise<ApiResponse<T>>;
  
  // 更新数据
  update(id: string, data: UpdateDto): Promise<ApiResponse<T>>;
  
  // 删除数据
  delete(id: string): Promise<ApiResponse<boolean>>;
  
  // 搜索数据
  search(query: string, params?: Record<string, unknown>): Promise<ApiResponse<T[]>>;
}

// 基础服务实现（使用模拟数据）
export abstract class BaseService<T extends Identifiable, CreateDto = Partial<T>, UpdateDto = Partial<T>> implements IBaseService<T, CreateDto, UpdateDto> {
  protected data: T[] = [];
  protected nextId = 1;

  constructor(initialData: T[] = []) {
    this.data = initialData;
    if (initialData.length > 0) {
      const maxId = Math.max(...initialData.map(item => {
        const id = item.id;
        return typeof id === 'string' ? parseInt(id, 10) : (id as number);
      }).filter((id): id is number => !isNaN(id)));
      this.nextId = maxId + 1;
    }
  }

  // 获取所有数据
  async getAll(params?: Record<string, unknown>): Promise<ApiResponse<T[]>> {
    try {
      let result = [...this.data];
      
      // 应用过滤参数
      if (params) {
        result = result.filter(item => {
          return Object.entries(params).every(([key, value]) => {
            const itemValue = (item as Record<string, unknown>)[key];
            return itemValue === value;
          });
        });
      }
      
      return {
        code: 200,
        message: '获取数据成功',
        data: result
      };
    } catch {
      return {
        code: 500,
        message: '获取数据失败',
        data: []
      };
    }
  }

  // 分页获取数据
  async getPaginated(page: number, pageSize: number, params?: Record<string, unknown>): Promise<ApiResponse<PaginatedResponse<T>>> {
    try {
      let filteredData = [...this.data];
      
      // 应用过滤参数
      if (params) {
        filteredData = filteredData.filter(item => {
          return Object.entries(params).every(([key, value]) => {
            const itemValue = (item as Record<string, unknown>)[key];
            return itemValue === value;
          });
        });
      }
      
      // 计算分页
      const total = filteredData.length;
      const startIndex = (page - 1) * pageSize;
      const endIndex = startIndex + pageSize;
      const items = filteredData.slice(startIndex, endIndex);
      const totalPages = Math.ceil(total / pageSize);
      
      return {
        code: 200,
        message: '获取分页数据成功',
        data: {
          items,
          total,
          page,
          pageSize,
          totalPages
        }
      };
    } catch {
      return {
        code: 500,
        message: '获取分页数据失败',
        data: {
          items: [],
          total: 0,
          page: 1,
          pageSize: 10,
          totalPages: 0
        }
      };
    }
  }

  // 根据ID获取单个数据
  async getById(id: string): Promise<ApiResponse<T>> {
    try {
      const item = this.data.find(item => item.id === id);
      if (!item) {
        return {
          code: 404,
          message: '数据不存在',
          data: {} as T
        };
      }
      return {
        code: 200,
        message: '获取数据成功',
        data: item
      };
    } catch {
      return {
        code: 500,
        message: '获取数据失败',
        data: {} as T
      };
    }
  }

  // 创建数据
  async create(data: CreateDto): Promise<ApiResponse<T>> {
    try {
      const newItem = {
        ...data,
        id: String(this.nextId++)
      } as unknown as T;
      
      this.data.push(newItem);
      
      return {
        code: 201,
        message: '创建数据成功',
        data: newItem
      };
    } catch {
      return {
        code: 500,
        message: '创建数据失败',
        data: {} as T
      };
    }
  }

  // 更新数据
  async update(id: string, data: UpdateDto): Promise<ApiResponse<T>> {
    try {
      const index = this.data.findIndex(item => item.id === id);
      if (index === -1) {
        return {
          code: 404,
          message: '数据不存在',
          data: {} as T
        };
      }
      
      const updatedItem = {
        ...this.data[index],
        ...data
      } as T;
      
      this.data[index] = updatedItem;
      
      return {
        code: 200,
        message: '更新数据成功',
        data: updatedItem
      };
    } catch {
      return {
        code: 500,
        message: '更新数据失败',
        data: {} as T
      };
    }
  }

  // 删除数据
  async delete(id: string): Promise<ApiResponse<boolean>> {
    try {
      const index = this.data.findIndex(item => item.id === id);
      if (index === -1) {
        return {
          code: 404,
          message: '数据不存在',
          data: false
        };
      }
      
      this.data.splice(index, 1);
      
      return {
        code: 200,
        message: '删除数据成功',
        data: true
      };
    } catch {
      return {
        code: 500,
        message: '删除数据失败',
        data: false
      };
    }
  }

  // 搜索数据
  async search(query: string, params?: Record<string, unknown>): Promise<ApiResponse<T[]>> {
    try {
      let result = [...this.data];
      
      // 应用过滤参数
      if (params) {
        result = result.filter(item => {
          return Object.entries(params).every(([key, value]) => {
            const itemValue = (item as Record<string, unknown>)[key];
            return itemValue === value;
          });
        });
      }
      
      // 应用搜索查询
      if (query) {
        const lowerQuery = query.toLowerCase();
        result = result.filter(item => {
          // 搜索所有字符串属性
          return Object.entries(item).some(([_, value]) => {
            if (typeof value === 'string') {
              return value.toLowerCase().includes(lowerQuery);
            }
            return false;
          });
        });
      }
      
      return {
        code: 200,
        message: '搜索数据成功',
        data: result
      };
    } catch {
      return {
        code: 500,
        message: '搜索数据失败',
        data: []
      };
    }
  }
}

// API响应工具函数
export function createApiResponse<T>(code: number, message: string, data: T): ApiResponse<T> {
  return {
    code,
    message,
    data
  };
}

// 成功响应
export function successResponse<T>(data: T, message: string = '操作成功'): ApiResponse<T> {
  return createApiResponse(200, message, data);
}

// 创建成功响应
export function createSuccessResponse<T>(data: T, message: string = '创建成功'): ApiResponse<T> {
  return createApiResponse(201, message, data);
}

// 错误响应
export function errorResponse<T>(code: number, message: string, data: T): ApiResponse<T> {
  return createApiResponse(code, message, data);
}
