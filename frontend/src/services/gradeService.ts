// Grade analysis service

import { fetchApi } from './api/apiService';

// 成绩分析服务类
export class GradeService {
  // 获取整体成绩分析
  async getOverallAnalysis() {
    return await fetchApi('/grades/analysis');
  }
  
  // 获取个人成绩分析
  async getStudentAnalysis(studentId: string) {
    return await fetchApi(`/grades/analysis/${studentId}`);
  }
  
  // 获取班级成绩分析
  async getClassAnalysis(className: string) {
    return await fetchApi(`/grades/analysis/class/${encodeURIComponent(className)}`);
  }
  
  // 获取年级成绩分析
  async getGradeAnalysis(gradeName: string) {
    return await fetchApi(`/grades/analysis/grade/${encodeURIComponent(gradeName)}`);
  }
  
  // 获取个人科目分析
  async getStudentSubjectAnalysis(studentId: string, subject: string) {
    return await fetchApi(`/grades/analysis/subject/${studentId}/${encodeURIComponent(subject)}`);
  }
  
  // 获取班级科目分析
  async getClassSubjectAnalysis(className: string, subject: string) {
    return await fetchApi(`/grades/analysis/class/${encodeURIComponent(className)}/${encodeURIComponent(subject)}`);
  }
  
  // 获取年级科目分析
  async getGradeSubjectAnalysis(gradeName: string, subject: string) {
    return await fetchApi(`/grades/analysis/grade/${encodeURIComponent(gradeName)}/${encodeURIComponent(subject)}`);
  }
  
  // 获取个人考试趋势
  async getStudentTrend(studentId: string) {
    return await fetchApi(`/grades/analysis/trend/${studentId}`);
  }
  
  // 获取班级考试趋势
  async getClassTrend(className: string) {
    return await fetchApi(`/grades/analysis/class/trend/${encodeURIComponent(className)}`);
  }
  
  // 获取年级考试趋势
  async getGradeTrend(gradeName: string) {
    return await fetchApi(`/grades/analysis/grade/trend/${encodeURIComponent(gradeName)}`);
  }
  
  // 获取教师成绩对比
  async getTeacherPerformance(subject: string) {
    return await fetchApi(`/grades/analysis/teacher/${encodeURIComponent(subject)}`);
  }
  
  // 获取个人课程安排与成绩关系
  async getStudentScheduleAnalysis(studentId: string) {
    return await fetchApi(`/grades/analysis/schedule/${studentId}`);
  }
  
  // 获取班级课程安排与成绩关系
  async getClassScheduleAnalysis(className: string) {
    return await fetchApi(`/grades/analysis/class/schedule/${encodeURIComponent(className)}`);
  }
}

// 导出单例实例
export const gradeService = new GradeService();