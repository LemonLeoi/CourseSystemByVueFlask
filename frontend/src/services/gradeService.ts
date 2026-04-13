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
      const response = await fetch('/api/grades/analysis');
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
      const response = await fetch(`/api/grades/analysis/${studentId}`);
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
      const response = await fetch(`/api/grades/analysis/class/${encodeURIComponent(className)}`);
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
      const response = await fetch(`/api/grades/analysis/grade/${encodeURIComponent(gradeName)}`);
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
  
  // 获取个人科目分析
  async getStudentSubjectAnalysis(studentId: string, subject: string) {
    try {
      const response = await fetch(`/api/grades/analysis/subject/${studentId}/${encodeURIComponent(subject)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取个人科目分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取个人科目分析失败:', error);
      throw error;
    }
  }
  
  // 获取班级科目分析
  async getClassSubjectAnalysis(className: string, subject: string) {
    try {
      const response = await fetch(`/api/grades/analysis/class/${encodeURIComponent(className)}/${encodeURIComponent(subject)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取班级科目分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取班级科目分析失败:', error);
      throw error;
    }
  }
  
  // 获取年级科目分析
  async getGradeSubjectAnalysis(gradeName: string, subject: string) {
    try {
      const response = await fetch(`/api/grades/analysis/grade/${encodeURIComponent(gradeName)}/${encodeURIComponent(subject)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取年级科目分析失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取年级科目分析失败:', error);
      throw error;
    }
  }
  
  // 获取个人考试趋势
  async getStudentTrend(studentId: string) {
    try {
      const response = await fetch(`/api/grades/analysis/trend/${studentId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取个人考试趋势失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取个人考试趋势失败:', error);
      throw error;
    }
  }
  
  // 获取班级考试趋势
  async getClassTrend(className: string) {
    try {
      const response = await fetch(`/api/grades/analysis/class/trend/${encodeURIComponent(className)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取班级考试趋势失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取班级考试趋势失败:', error);
      throw error;
    }
  }
  
  // 获取年级考试趋势
  async getGradeTrend(gradeName: string) {
    try {
      const response = await fetch(`/api/grades/analysis/grade/trend/${encodeURIComponent(gradeName)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取年级考试趋势失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取年级考试趋势失败:', error);
      throw error;
    }
  }
  
  // 获取教师成绩对比
  async getTeacherPerformance(subject: string) {
    try {
      const response = await fetch(`/api/grades/analysis/teacher/${encodeURIComponent(subject)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取教师成绩对比失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取教师成绩对比失败:', error);
      throw error;
    }
  }
  
  // 获取个人课程安排与成绩关系
  async getStudentScheduleAnalysis(studentId: string) {
    try {
      const response = await fetch(`/api/grades/analysis/schedule/${studentId}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取个人课程安排与成绩关系失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取个人课程安排与成绩关系失败:', error);
      throw error;
    }
  }
  
  // 获取班级课程安排与成绩关系
  async getClassScheduleAnalysis(className: string) {
    try {
      const response = await fetch(`/api/grades/analysis/class/schedule/${encodeURIComponent(className)}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || '获取班级课程安排与成绩关系失败');
      }
      return await response.json();
    } catch (error) {
      console.error('获取班级课程安排与成绩关系失败:', error);
      throw error;
    }
  }
}

// 导出单例实例
export const gradeService = new GradeService();