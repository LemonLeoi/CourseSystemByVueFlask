// Class grade analysis composable
import { ref } from 'vue'
import { gradeService } from '../../services/gradeService'

export function useClassGrade() {
  const classInfo = ref(null)
  const subjectAverages = ref({})
  const overallAverage = ref(0)
  const studentCount = ref(0)
  const subjectAnalysis = ref(null)
  const examTrend = ref(null)
  const scheduleAnalysis = ref(null)
  const loading = ref(false)
  const error = ref('')
  
  // 获取班级成绩分析
  const getClassAnalysis = async (className: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getClassAnalysis(className)
      if (response.error) {
        throw new Error(response.error)
      }
      classInfo.value = response.class_info
      subjectAverages.value = response.subject_averages
      overallAverage.value = response.overall_average
      studentCount.value = response.student_count
    } catch (err) {
      error.value = err.message || '获取班级分析失败'
      resetData()
    } finally {
      loading.value = false
    }
  }
  
  // 获取班级科目分析
  const getClassSubjectAnalysis = async (className: string, subject: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getClassSubjectAnalysis(className, subject)
      if (response.error) {
        throw new Error(response.error)
      }
      subjectAnalysis.value = response
    } catch (err) {
      error.value = err.message || '获取班级科目分析失败'
      subjectAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取班级考试趋势
  const getClassTrend = async (className: string, subject?: string, examCode?: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getClassTrend(className, subject, examCode)
      if (response.error) {
        throw new Error(response.error)
      }
      examTrend.value = response
    } catch (err) {
      error.value = err.message || '获取班级考试趋势失败'
      examTrend.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 获取班级课程安排与成绩关系
  const getClassScheduleAnalysis = async (className: string) => {
    loading.value = true
    error.value = ''
    try {
      const response = await gradeService.getClassScheduleAnalysis(className)
      if (response.error) {
        throw new Error(response.error)
      }
      scheduleAnalysis.value = response
    } catch (err) {
      error.value = err.message || '获取班级课程安排与成绩关系失败'
      scheduleAnalysis.value = null
    } finally {
      loading.value = false
    }
  }
  
  // 重置数据
  const resetData = () => {
    classInfo.value = null
    subjectAverages.value = {}
    overallAverage.value = 0
    studentCount.value = 0
    subjectAnalysis.value = null
    examTrend.value = null
    scheduleAnalysis.value = null
  }
  
  // 获取学科平均成绩排名
  const getSubjectRanking = () => {
    if (!subjectAverages.value) return []
    return Object.entries(subjectAverages.value)
      .map(([subject, avg]) => ({ subject, avg }))
      .sort((a, b) => b.avg - a.avg)
  }
  
  // 获取班级整体水平评估
  const getClassEvaluation = () => {
    if (overallAverage.value >= 90) return '优秀'
    if (overallAverage.value >= 80) return '良好'
    if (overallAverage.value >= 70) return '中等'
    if (overallAverage.value >= 60) return '及格'
    return '需要提高'
  }
  
  // 计算学科与班级平均的差异
  const calculateSubjectDifference = (subject: string) => {
    if (!subjectAverages.value[subject] || !overallAverage.value) {
      return 0
    }
    return subjectAverages.value[subject] - overallAverage.value
  }
  
  return {
    classInfo,
    subjectAverages,
    overallAverage,
    studentCount,
    subjectAnalysis,
    examTrend,
    scheduleAnalysis,
    loading,
    error,
    getClassAnalysis,
    getClassSubjectAnalysis,
    getClassTrend,
    getClassScheduleAnalysis,
    resetData,
    getSubjectRanking,
    getClassEvaluation,
    calculateSubjectDifference
  }
}