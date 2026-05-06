// Individual grade analysis composable
import { ref } from 'vue'
import { gradeService } from '../../services/gradeService'

export function useIndividualGrade() {
  const studentInfo = ref(null)
  const examGrades = ref({})
  const subjectAverages = ref({})
  const classAverages = ref({})
  const strengths = ref([])
  const weaknesses = ref([])
  const overall = ref({})
  const subjectAnalysis = ref(null)
  const examTrend = ref(null)
  const scheduleAnalysis = ref(null)
  const loading = ref(false)
  const error = ref('')
  
  // 获取个人成绩分析
  const getStudentAnalysis = async (studentId: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getStudentAnalysis(studentId)
      if (response.error) {
        throw new Error(response.error)
      }
      studentInfo.value = response.student_info
      examGrades.value = response.exam_grades
      subjectAverages.value = response.subject_averages
      classAverages.value = response.class_averages
      strengths.value = response.strengths
      weaknesses.value = response.weaknesses
      overall.value = response.overall
    } catch (err) {
      error.value = err.message || '获取个人分析失败'
      resetData()
    } finally {
      loading.value = false
    }
  }
  
  // 获取个人科目分析
  const getStudentSubjectAnalysis = async (studentId: string, subject: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getStudentSubjectAnalysis(studentId, subject)
      if (response.error) {
        throw new Error(response.error)
      }
      subjectAnalysis.value = response
    } catch (err) {
      error.value = err.message || '获取个人科目分析失败'
      subjectAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取个人考试趋势
  const getStudentTrend = async (studentId: string, subject?: string, examCode?: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getStudentTrend(studentId, subject, examCode)
      if (response.error) {
        throw new Error(response.error)
      }
      examTrend.value = response
    } catch (err) {
      error.value = err.message || '获取个人考试趋势失败'
      examTrend.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取个人课程安排与成绩关系
  const getStudentScheduleAnalysis = async (studentId: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getStudentScheduleAnalysis(studentId)
      if (response.error) {
        throw new Error(response.error)
      }
      scheduleAnalysis.value = response
    } catch (err) {
      error.value = err.message || '获取个人课程安排与成绩关系失败'
      scheduleAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 重置数据
  const resetData = () => {
    studentInfo.value = null
    examGrades.value = {}
    subjectAverages.value = {}
    classAverages.value = {}
    strengths.value = []
    weaknesses.value = []
    overall.value = {}
    subjectAnalysis.value = null
    examTrend.value = null
    scheduleAnalysis.value = null
  }
  
  // 计算学科差异
  const calculateSubjectDifference = (subject: string) => {
    if (!subjectAverages.value[subject] || !classAverages.value[subject]) {
      return 0
    }
    return subjectAverages.value[subject] - classAverages.value[subject]
  }
  
  // 获取学科等级
  const getSubjectLevel = (score: number) => {
    if (score >= 90) return '优秀'
    if (score >= 80) return '良好'
    if (score >= 70) return '中等'
    if (score >= 60) return '及格'
    return '不及格'
  }
  
  return {
    studentInfo,
    examGrades,
    subjectAverages,
    classAverages,
    strengths,
    weaknesses,
    overall,
    subjectAnalysis,
    examTrend,
    scheduleAnalysis,
    loading,
    error,
    getStudentAnalysis,
    getStudentSubjectAnalysis,
    getStudentTrend,
    getStudentScheduleAnalysis,
    resetData,
    calculateSubjectDifference,
    getSubjectLevel
  }
}