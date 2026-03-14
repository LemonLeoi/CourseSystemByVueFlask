import { defineStore } from 'pinia';

// 成绩分析存储
export const useGradeStore = defineStore('grades', {
  state: () => ({
    // 整体分析数据
    overallAnalysis: null as any,
    // 个人分析数据
    studentAnalysis: null as any,
    // 班级分析数据
    classAnalysis: null as any,
    // 年级分析数据
    gradeAnalysis: null as any,
    // 加载状态
    loading: false,
    // 错误状态
    error: null as string | null,
    studentError: null as string | null,
    classError: null as string | null,
    gradeError: null as string | null,
  }),

  getters: {
    // 获取整体分析数据
    getOverallAnalysis: (state) => state.overallAnalysis,
    
    // 获取个人分析数据
    getStudentAnalysis: (state) => state.studentAnalysis,
    
    // 获取班级分析数据
    getClassAnalysis: (state) => state.classAnalysis,
    
    // 获取年级分析数据
    getGradeAnalysis: (state) => state.gradeAnalysis,
    
    // 获取加载状态
    isLoading: (state) => state.loading,
    
    // 获取错误信息
    getError: (state) => state.error,
    getStudentError: (state) => state.studentError,
    getClassError: (state) => state.classError,
    getGradeError: (state) => state.gradeError,
  },

  actions: {
    // 设置整体分析数据
    setOverallAnalysis(data: any) {
      this.overallAnalysis = data;
    },
    
    // 设置个人分析数据
    setStudentAnalysis(data: any) {
      this.studentAnalysis = data;
    },
    
    // 设置班级分析数据
    setClassAnalysis(data: any) {
      this.classAnalysis = data;
    },
    
    // 设置年级分析数据
    setGradeAnalysis(data: any) {
      this.gradeAnalysis = data;
    },
    
    // 设置加载状态
    setLoading(loading: boolean) {
      this.loading = loading;
    },
    
    // 设置错误信息
    setError(error: string | null) {
      this.error = error;
    },
    
    setStudentError(error: string | null) {
      this.studentError = error;
    },
    
    setClassError(error: string | null) {
      this.classError = error;
    },
    
    setGradeError(error: string | null) {
      this.gradeError = error;
    },
    
    // 清除所有分析数据
    clearAllAnalysis() {
      this.overallAnalysis = null;
      this.studentAnalysis = null;
      this.classAnalysis = null;
      this.gradeAnalysis = null;
      this.error = null;
      this.studentError = null;
      this.classError = null;
      this.gradeError = null;
    },
    
    // 清除个人分析数据
    clearStudentAnalysis() {
      this.studentAnalysis = null;
      this.studentError = null;
    },
    
    // 清除班级分析数据
    clearClassAnalysis() {
      this.classAnalysis = null;
      this.classError = null;
    },
    
    // 清除年级分析数据
    clearGradeAnalysis() {
      this.gradeAnalysis = null;
      this.gradeError = null;
    },
  },
});