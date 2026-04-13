// Grade analysis composable
import { ref } from 'vue'
import { gradeService } from '../../services/gradeService'

export function useGradeAnalysis() {
  const overallStats = ref({})
  const studentAnalysis = ref(null)
  const classAnalysis = ref(null)
  const gradeAnalysis = ref(null)
  const subjectAnalysis = ref(null)
  const examTrend = ref(null)
  const teacherPerformance = ref(null)
  const loading = ref(false)
  const error = ref('')
  const studentError = ref('')
  const classError = ref('')
  const gradeError = ref('')
  const subjectError = ref('')
  const trendError = ref('')
  const teacherError = ref('')
  
  // 获取整体成绩分析
  const getOverallAnalysis = async () => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getOverallAnalysis()
      overallStats.value = response
    } catch (err) {
      error.value = err.message || '获取整体分析失败'
    } finally {
      loading.value = false
    }
  }
  
  // 获取个人成绩分析
  const getStudentAnalysis = async (studentId: string) => {
    loading.value = true
    studentError.value = ''
    try {
      const response = await gradeService.getStudentAnalysis(studentId)
      studentAnalysis.value = response
    } catch (err) {
      studentError.value = err.message || '获取个人分析失败'
      studentAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取班级成绩分析
  const getClassAnalysis = async (className: string) => {
    loading.value = true
    classError.value = ''
    try {
      const response = await gradeService.getClassAnalysis(className)
      classAnalysis.value = response
    } catch (err) {
      classError.value = err.message || '获取班级分析失败'
      classAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取年级成绩分析
  const getGradeAnalysis = async (gradeName: string) => {
    loading.value = true
    gradeError.value = ''
    try {
      const response = await gradeService.getGradeAnalysis(gradeName)
      gradeAnalysis.value = response
    } catch (err) {
      gradeError.value = err.message || '获取年级分析失败'
      gradeAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取年级科目分析
  const getGradeSubjectAnalysis = async (gradeName: string, subject: string) => {
    loading.value = true
    subjectError.value = ''
    try {
      const response = await gradeService.getGradeSubjectAnalysis(gradeName, subject)
      subjectAnalysis.value = response
    } catch (err) {
      subjectError.value = err.message || '获取年级科目分析失败'
      subjectAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取年级考试趋势
  const getGradeTrend = async (gradeName: string) => {
    loading.value = true
    trendError.value = ''
    try {
      const response = await gradeService.getGradeTrend(gradeName)
      examTrend.value = response
    } catch (err) {
      trendError.value = err.message || '获取年级考试趋势失败'
      examTrend.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取教师成绩对比
  const getTeacherPerformance = async (subject: string) => {
    loading.value = true
    teacherError.value = ''
    try {
      const response = await gradeService.getTeacherPerformance(subject)
      teacherPerformance.value = response
    } catch (err) {
      teacherError.value = err.message || '获取教师成绩对比失败'
      teacherPerformance.value = null
    } finally {
      loading.value = false
    }
  }
  
  return {
    overallStats,
    studentAnalysis,
    classAnalysis,
    gradeAnalysis,
    subjectAnalysis,
    examTrend,
    teacherPerformance,
    loading,
    error,
    studentError,
    classError,
    gradeError,
    subjectError,
    trendError,
    teacherError,
    getOverallAnalysis,
    getStudentAnalysis,
    getClassAnalysis,
    getGradeAnalysis,
    getGradeSubjectAnalysis,
    getGradeTrend,
    getTeacherPerformance
  }
}