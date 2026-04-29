import { defineStore } from 'pinia';

// 学科平均成绩类型
export interface SubjectAverage {
  [subject: string]: number;
}

// 学科强弱项类型
export interface SubjectStrength {
  subject: string;
  avg_score: number;
  class_avg: number;
  diff: number;
}

// 整体评估类型
export interface OverallEvaluation {
  personal_avg: number;
  class_avg: number;
  diff: number;
  evaluation: string;
}

// 学生信息类型
export interface StudentInfo {
  name: string;
  gender: string;
  class: string;
  grade: string;
}

// 班级信息类型
export interface ClassInfo {
  class_name: string;
  grade: string;
  student_count: number;
}

// 年级信息类型
export interface GradeInfo {
  grade: string;
  class_count: number;
}

// 考试趋势类型
export interface ExamTrend {
  exam_names: string[];
  averages: number[];
}

// 个人分析数据类型
export interface StudentAnalysisData {
  student_info: StudentInfo;
  exam_grades?: {
    [exam_name: string]: {
      academic_year: string;
      semester: string;
      grade: string;
      exam_type: string;
      subjects: { [subject: string]: [number, string] };
    };
  };
  subject_averages: SubjectAverage;
  class_averages: SubjectAverage;
  strengths: SubjectStrength[];
  weaknesses: SubjectStrength[];
  overall: OverallEvaluation;
  explanations?: {
    analysis_steps?: string;
    statistical_methods?: { [key: string]: string };
    result_interpretation?: { [key: string]: string };
  };
  error?: string;
}

// 班级分析数据类型
export interface ClassAnalysisData {
  class_info: ClassInfo;
  subject_averages: SubjectAverage;
  overall_average: number;
  student_count: number;
  explanations?: {
    analysis_steps?: string;
    statistical_methods?: { [key: string]: string };
    result_interpretation?: { [key: string]: string };
  };
  error?: string;
}

// 年级分析数据类型
export interface GradeAnalysisData {
  grade_info: GradeInfo;
  class_averages: { [class_name: string]: SubjectAverage };
  subject_averages: SubjectAverage;
  overall_average: number;
  explanations?: {
    analysis_steps?: string;
    statistical_methods?: { [key: string]: string };
    result_interpretation?: { [key: string]: string };
  };
  error?: string;
}

// 整体分析数据类型
export interface OverallAnalysisData {
  total_count: number;
  average: number;
  std_deviation: number;
  median: number;
  min_score: number;
  max_score: number;
  distribution: {
    excellent: number;
    good: number;
    average: number;
    pass: number;
    fail: number;
  };
  distribution_percent: {
    excellent: number;
    good: number;
    average: number;
    pass: number;
    fail: number;
  };
  error?: string;
}

// 成绩分析存储
export const useGradeStore = defineStore('grades', {
  state: () => ({
    // 整体分析数据
    overallAnalysis: null as OverallAnalysisData | null,
    // 个人分析数据
    studentAnalysis: null as StudentAnalysisData | null,
    // 班级分析数据
    classAnalysis: null as ClassAnalysisData | null,
    // 年级分析数据
    gradeAnalysis: null as GradeAnalysisData | null,
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
    setOverallAnalysis(data: OverallAnalysisData) {
      this.overallAnalysis = data;
    },
    
    // 设置个人分析数据
    setStudentAnalysis(data: StudentAnalysisData) {
      this.studentAnalysis = data;
    },
    
    // 设置班级分析数据
    setClassAnalysis(data: ClassAnalysisData) {
      this.classAnalysis = data;
    },
    
    // 设置年级分析数据
    setGradeAnalysis(data: GradeAnalysisData) {
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
