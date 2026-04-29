import { ref } from 'vue';
import { gradeService } from '../../services/gradeService';
import type { StudentAnalysisData, ClassAnalysisData, GradeAnalysisData } from '../../stores/grades';

export interface SubjectAnalysisData {
  subject: string;
  grade: string;
  class_averages: { [class_name: string]: number };
  overall_average: number;
  distribution: {
    excellent: number;
    good: number;
    average: number;
    pass: number;
    fail: number;
  };
}

export interface ExamTrendData {
  grade: string;
  exam_names: string[];
  averages: number[];
  trend: 'up' | 'down' | 'stable';
}

export interface TeacherPerformanceData {
  subject: string;
  teachers: {
    name: string;
    average_score: number;
    student_count: number;
    rank: number;
  }[];
}

export function useGradeAnalysis() {
  const studentAnalysis = ref<StudentAnalysisData | null>(null);
  const classAnalysis = ref<ClassAnalysisData | null>(null);
  const gradeAnalysis = ref<GradeAnalysisData | null>(null);
  const subjectAnalysis = ref<SubjectAnalysisData | null>(null);
  const examTrend = ref<ExamTrendData | null>(null);
  const teacherPerformance = ref<TeacherPerformanceData | null>(null);
  const loading = ref(false);
  const studentError = ref('');
  const classError = ref('');
  const gradeError = ref('');
  const subjectError = ref('');
  const trendError = ref('');
  const teacherError = ref('');
  
  // 获取个人成绩分析
  const getStudentAnalysis = async (studentId: string) => {
    loading.value = true;
    studentError.value = '';
    try {
      const response = await gradeService.getStudentAnalysis(studentId);
      studentAnalysis.value = response;
    } catch (err) {
      studentError.value = err instanceof Error ? err.message : '获取个人分析失败';
      studentAnalysis.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  // 获取班级成绩分析
  const getClassAnalysis = async (className: string) => {
    loading.value = true;
    classError.value = '';
    try {
      const response = await gradeService.getClassAnalysis(className);
      classAnalysis.value = response;
    } catch (err) {
      classError.value = err instanceof Error ? err.message : '获取班级分析失败';
      classAnalysis.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  // 获取年级成绩分析
  const getGradeAnalysis = async (gradeName: string) => {
    loading.value = true;
    gradeError.value = '';
    try {
      const response = await gradeService.getGradeAnalysis(gradeName);
      gradeAnalysis.value = response;
    } catch (err) {
      gradeError.value = err instanceof Error ? err.message : '获取年级分析失败';
      gradeAnalysis.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  // 获取年级科目分析
  const getGradeSubjectAnalysis = async (gradeName: string, subject: string) => {
    loading.value = true;
    subjectError.value = '';
    try {
      const response = await gradeService.getGradeSubjectAnalysis(gradeName, subject);
      subjectAnalysis.value = response;
    } catch (err) {
      subjectError.value = err instanceof Error ? err.message : '获取年级科目分析失败';
      subjectAnalysis.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  // 获取年级考试趋势
  const getGradeTrend = async (gradeName: string) => {
    loading.value = true;
    trendError.value = '';
    try {
      const response = await gradeService.getGradeTrend(gradeName);
      examTrend.value = response;
    } catch (err) {
      trendError.value = err instanceof Error ? err.message : '获取年级考试趋势失败';
      examTrend.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  // 获取教师成绩对比
  const getTeacherPerformance = async (subject: string) => {
    loading.value = true;
    teacherError.value = '';
    try {
      const response = await gradeService.getTeacherPerformance(subject);
      teacherPerformance.value = response;
    } catch (err) {
      teacherError.value = err instanceof Error ? err.message : '获取教师成绩对比失败';
      teacherPerformance.value = null;
    } finally {
      loading.value = false;
    }
  };
  
  return {
    studentAnalysis,
    classAnalysis,
    gradeAnalysis,
    subjectAnalysis,
    examTrend,
    teacherPerformance,
    loading,
    studentError,
    classError,
    gradeError,
    subjectError,
    trendError,
    teacherError,
    getStudentAnalysis,
    getClassAnalysis,
    getGradeAnalysis,
    getGradeSubjectAnalysis,
    getGradeTrend,
    getTeacherPerformance
  };
}
