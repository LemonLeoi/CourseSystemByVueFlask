// Grade analysis service

import { BaseService } from './baseService';

// 成绩分析服务类
export class GradeService extends BaseService {
  constructor() {
    super([]);
  }

  // 获取整体成绩分析
  async getOverallAnalysis() {
    try {
      const response = await fetch('http://localhost:5000/api/grades/analysis');
      if (!response.ok) {
        throw new Error('获取整体分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取整体分析失败:', error);
      throw error;
    }
  }
  
  // 获取个人成绩分析
  async getStudentAnalysis(studentId: string) {
    try {
      const response = await fetch(`http://localhost:5000/api/grades/analysis/${studentId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取个人分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取个人分析失败:', error);
      throw error;
    }
  }
  
  // 获取班级成绩分析
  async getClassAnalysis(className: string) {
    try {
      const response = await fetch(`http://localhost:5000/api/grades/analysis/class/${encodeURIComponent(className)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取班级分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取班级分析失败:', error);
      throw error;
    }
  }
  
  // 获取年级成绩分析
  async getGradeAnalysis(gradeName: string) {
    try {
      const response = await fetch(`http://localhost:5000/api/grades/analysis/grade/${encodeURIComponent(gradeName)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取年级分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取年级分析失败:', error);
      throw error;
    }
  }
}

// 导出单例实例
export const gradeService = new GradeService();