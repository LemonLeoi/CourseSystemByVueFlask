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
  
  // 获取分析过程数据
  
  // 获取中间结果
  async getIntermediateResults(analysisId: string, step?: string) {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (step) {
      params.append('step', step);
    }
    return await fetchApi(`/api/analysis/intermediate-results?${params.toString()}`);
  }
  
  // 获取模型状态
  async getModelState(analysisId: string, modelName?: string) {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (modelName) {
      params.append('model_name', modelName);
    }
    return await fetchApi(`/api/analysis/model-state?${params.toString()}`);
  }
  
  // 获取阶段性结论
  async getConclusions(analysisId: string, level?: string) {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (level) {
      params.append('level', level);
    }
    return await fetchApi(`/api/analysis/conclusions?${params.toString()}`);
  }
  
  // 获取分析日志
  async getAnalysisLogs(analysisType?: string, startTime?: string, endTime?: string) {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    if (startTime) {
      params.append('start_time', startTime);
    }
    if (endTime) {
      params.append('end_time', endTime);
    }
    return await fetchApi(`/api/analysis/logs?${params.toString()}`);
  }
  
  // 获取过程可视化数据
  async getProcessVisualization(analysisId: string, processType: string) {
    return await fetchApi('/api/analysis/process-visualization', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ analysis_id: analysisId, process_type: processType })
    });
  }
  
  // 获取历史分析记录
  async getAnalysisHistory(analysisType?: string, limit?: number) {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    if (limit) {
      params.append('limit', limit.toString());
    }
    return await fetchApi(`/api/analysis/history?${params.toString()}`);
  }
}

// 导出单例实例
export const gradeService = new GradeService();