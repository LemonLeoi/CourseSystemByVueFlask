<template>
  <div class="individual-analysis">
    <h3>个人成绩分析</h3>
    <div class="student-input">
      <select 
        v-model="studentId" 
        class="filter-select"
      >
        <option value="">请选择学生</option>
        <option v-for="student in students" :key="student.id" :value="student.id">
            {{ student.name }} ({{ student.id }})
          </option>
      </select>
      <button @click="loadStudents">加载学生</button>
      <button @click="analyzeStudent">分析</button>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>正在分析 {{ selectedStudentName }} 的成绩...</p>
      <p class="loading-detail">正在获取各科成绩数据，请稍候...</p>
    </div>
    <div v-else-if="studentError" class="error">{{ studentError }}</div>
    <div v-else-if="studentAnalysis && studentAnalysis.student_info" class="student-analysis">
      <div class="student-info">
        <div class="info-header">
          <h4>学生信息</h4>
          <div class="info-icon">📊</div>
        </div>
        <p>姓名: {{ studentAnalysis.student_info.name }}</p>
        <p>性别: {{ studentAnalysis.student_info.gender }}</p>
        <p>班级: {{ studentAnalysis.student_info.class }}</p>
        <p>年级: {{ studentAnalysis.student_info.grade }}</p>
      </div>
      
      <div class="overall-performance">
        <div class="info-header">
          <h4>整体表现</h4>
          <div class="info-icon">📈</div>
        </div>
        <p>个人平均: {{ studentAnalysis.overall.personal_avg }}</p>
        <p>班级平均: {{ studentAnalysis.overall.class_avg }}</p>
        <p>差异: {{ studentAnalysis.overall.diff > 0 ? '+' + studentAnalysis.overall.diff : studentAnalysis.overall.diff }}</p>
        <p>评估: {{ studentAnalysis.overall.evaluation }}</p>
      </div>
      
      <div class="subject-analysis">
        <div class="info-header">
          <h4>学科分析</h4>
          <div class="info-icon">📊</div>
        </div>
        <div ref="studentSubjectChart" class="chart"></div>
      </div>
      
      <div class="strengths-weaknesses">
        <div class="strengths">
          <div class="info-header">
            <h4>学科强项</h4>
            <div class="info-icon">👍</div>
          </div>
          <ul>
            <li v-for="(item, index) in studentAnalysis.strengths" :key="index">
              {{ item.subject }}: {{ item.avg_score }} (班级平均: {{ item.class_avg }}, +{{ item.diff }})
            </li>
          </ul>
        </div>
        <div class="weaknesses">
          <div class="info-header">
            <h4>学科弱项</h4>
            <div class="info-icon">👎</div>
          </div>
          <ul>
            <li v-for="(item, index) in studentAnalysis.weaknesses" :key="index">
              {{ item.subject }}: {{ item.avg_score }} (班级平均: {{ item.class_avg }}, -{{ item.diff }})
            </li>
          </ul>
        </div>
      </div>
      
      <!-- 新增：科目选择下拉菜单 -->
      <div class="subject-selector">
        <h4>科目分析</h4>
        <select v-model="selectedSubject" class="filter-select" @change="analyzeSubject">
          <option value="">请选择科目</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
        </select>
      </div>
      
      <!-- 新增：具体科目分析模块 -->
      <div v-if="subjectAnalysis" class="specific-subject-analysis">
        <div class="info-header">
          <h4>{{ selectedSubject }} 科目分析</h4>
          <div class="info-icon">📊</div>
        </div>
        <div class="subject-stats">
          <div class="stat-item">
            <span class="stat-label">平均成绩:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.average }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">中位数:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.median }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">标准差:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.std_deviation }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最高分:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.max_score }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最低分:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.min_score }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">班级平均:</span>
            <span class="stat-value">{{ subjectAnalysis.class_average }}</span>
          </div>
        </div>
        <div ref="subjectDistributionChart" class="chart"></div>
        <div ref="subjectBoxPlotChart" class="chart"></div>
      </div>
      
      <!-- 新增：历次考试趋势图表 -->
      <div class="exam-trend-analysis">
        <div class="info-header">
          <h4>历次考试趋势</h4>
          <div class="info-icon">📈</div>
        </div>
        <div ref="examTrendChart" class="chart"></div>
      </div>
      
      <!-- 新增：课程安排与成绩关系散点图 -->
      <div class="schedule-analysis">
        <div class="info-header">
          <h4>课程安排与成绩关系</h4>
          <div class="info-icon">📅</div>
        </div>
        <div ref="scheduleScatterChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useIndividualGrade } from '../../composables/grade/useIndividualGrade'

export default {
  name: 'IndividualAnalysis',
  setup() {
    const {
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
      getStudentScheduleAnalysis
    } = useIndividualGrade()
    
    const studentId = ref('')
    const students = ref([])
    const isLoadingStudents = ref(false)
    const selectedStudentName = ref('')
    const selectedSubject = ref('')
    const subjects = ref([])
    
    // 图表引用
    const studentSubjectChart = ref(null)
    const subjectDistributionChart = ref(null)
    const subjectBoxPlotChart = ref(null)
    const examTrendChart = ref(null)
    const scheduleScatterChart = ref(null)
    
    // 图表实例
    let studentSubjectChartInstance = null
    let subjectDistributionChartInstance = null
    let subjectBoxPlotChartInstance = null
    let examTrendChartInstance = null
    let scheduleScatterChartInstance = null
    
    // 加载学生列表
    const loadStudents = async () => {
      console.log('开始加载学生列表')
      isLoadingStudents.value = true
      try {
        console.log('发起API请求')
        const response = await fetch('http://localhost:5000/api/students/')
        console.log('API请求返回:', response)
        if (response.ok) {
          const data = await response.json()
          console.log('获取到学生数据:', data)
          students.value = data
        } else {
          console.error('API请求失败:', response.status)
        }
      } catch (error) {
        console.error('获取学生列表失败:', error)
      } finally {
        isLoadingStudents.value = false
        console.log('加载学生列表完成')
      }
    }
    
    // 分析学生成绩
    const analyzeStudent = async () => {
      if (studentId.value) {
        // 查找选中的学生姓名
        const selectedStudent = students.value.find(student => student.id === studentId.value)
        if (selectedStudent) {
          selectedStudentName.value = selectedStudent.name
        }
        await getStudentAnalysis(studentId.value)
        // 加载考试趋势
        await getStudentTrend(studentId.value)
        // 加载课程安排分析
        await getStudentScheduleAnalysis(studentId.value)
        // 提取科目列表
        if (subjectAverages.value) {
          subjects.value = Object.keys(subjectAverages.value)
        }
      }
    }
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (studentId.value && selectedSubject.value) {
        await getStudentSubjectAnalysis(studentId.value, selectedSubject.value)
      }
    }
    
    // 监听学生分析数据变化，更新图表
    watch([subjectAverages, classAverages], () => {
      if (subjectAverages.value && Object.keys(subjectAverages.value).length > 0) {
        // 使用nextTick确保DOM渲染完成后再初始化图表
        setTimeout(() => {
          initStudentSubjectChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听科目分析数据变化，更新图表
    watch(subjectAnalysis, () => {
      if (subjectAnalysis.value) {
        setTimeout(() => {
          initSubjectDistributionChart()
          initSubjectBoxPlotChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听考试趋势数据变化，更新图表
    watch(examTrend, () => {
      if (examTrend.value) {
        setTimeout(() => {
          initExamTrendChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听课程安排分析数据变化，更新图表
    watch(scheduleAnalysis, () => {
      if (scheduleAnalysis.value) {
        setTimeout(() => {
          initScheduleScatterChart()
        }, 0)
      }
    }, { deep: true })
    
    // 初始化学生学科成绩图表
    const initStudentSubjectChart = () => {
      if (studentSubjectChart.value && subjectAverages.value) {
        if (studentSubjectChartInstance) {
          studentSubjectChartInstance.dispose()
        }
        studentSubjectChartInstance = echarts.init(studentSubjectChart.value)
        
        const subjects = Object.keys(subjectAverages.value)
        const personalAverages = subjects.map(subject => subjectAverages.value[subject])
        const classAverages = subjects.map(subject => classAverages.value[subject] || 0)
        
        const option = {
          title: {
            text: '个人与班级学科成绩对比',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['个人平均', '班级平均'],
            bottom: 0
          },
          xAxis: {
            type: 'category',
            data: subjects,
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value',
            name: '分数'
          },
          series: [
            {
              name: '个人平均',
              type: 'bar',
              data: personalAverages,
              itemStyle: {
                color: '#5470c6'
              }
            },
            {
              name: '班级平均',
              type: 'bar',
              data: classAverages,
              itemStyle: {
                color: '#91cc75'
              }
            }
          ]
        }
        
        studentSubjectChartInstance.setOption(option)
      }
    }
    
    // 初始化科目分布图表
    const initSubjectDistributionChart = () => {
      if (subjectDistributionChart.value && subjectAnalysis.value) {
        if (subjectDistributionChartInstance) {
          subjectDistributionChartInstance.dispose()
        }
        subjectDistributionChartInstance = echarts.init(subjectDistributionChart.value)
        
        const distribution = subjectAnalysis.value.statistics.distribution
        const categories = ['优秀', '良好', '中等', '及格', '不及格']
        const data = [
          distribution.excellent,
          distribution.good,
          distribution.average,
          distribution.pass,
          distribution.fail
        ]
        
        const option = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: categories
          },
          yAxis: {
            type: 'value',
            name: '人数'
          },
          series: [
            {
              name: '人数',
              type: 'bar',
              data: data,
              itemStyle: {
                color: '#5470c6'
              }
            }
          ]
        }
        
        subjectDistributionChartInstance.setOption(option)
      }
    }
    
    // 初始化科目箱线图
    const initSubjectBoxPlotChart = () => {
      if (subjectBoxPlotChart.value && subjectAnalysis.value) {
        if (subjectBoxPlotChartInstance) {
          subjectBoxPlotChartInstance.dispose()
        }
        subjectBoxPlotChartInstance = echarts.init(subjectBoxPlotChart.value)
        
        // 模拟箱线图数据（实际项目中应该从API获取）
        const boxData = [
          [subjectAnalysis.value.statistics.min_score, 
           subjectAnalysis.value.statistics.min_score + 10, 
           subjectAnalysis.value.statistics.median, 
           subjectAnalysis.value.statistics.median + 10, 
           subjectAnalysis.value.statistics.max_score]
        ]
        
        const option = {
          title: {
            text: '成绩分布箱线图',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
          },
          xAxis: {
            type: 'category',
            data: [subjectAnalysis.value.subject],
            boundaryGap: true,
            nameGap: 30,
            splitArea: {
              show: false
            },
            splitLine: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            name: '分数',
            splitArea: {
              show: true
            }
          },
          series: [
            {
              name: '成绩分布',
              type: 'boxplot',
              data: boxData,
              itemStyle: {
                color: '#5470c6'
              }
            }
          ]
        }
        
        subjectBoxPlotChartInstance.setOption(option)
      }
    }
    
    // 初始化考试趋势图表
    const initExamTrendChart = () => {
      if (examTrendChart.value && examTrend.value) {
        if (examTrendChartInstance) {
          examTrendChartInstance.dispose()
        }
        examTrendChartInstance = echarts.init(examTrendChart.value)
        
        const examNames = examTrend.value.exam_trend.exam_names
        const averages = examTrend.value.exam_trend.averages
        
        const option = {
          title: {
            text: '历次考试趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: examNames,
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value',
            name: '平均分数'
          },
          series: [
            {
              name: '平均分数',
              type: 'line',
              data: averages,
              smooth: true,
              itemStyle: {
                color: '#5470c6'
              },
              areaStyle: {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [{
                    offset: 0, color: 'rgba(84, 112, 198, 0.3)'
                  }, {
                    offset: 1, color: 'rgba(84, 112, 198, 0.1)'
                  }]
                }
              }
            }
          ]
        }
        
        examTrendChartInstance.setOption(option)
      }
    }
    
    // 初始化课程安排与成绩关系散点图
    const initScheduleScatterChart = () => {
      if (scheduleScatterChart.value && scheduleAnalysis.value) {
        if (scheduleScatterChartInstance) {
          scheduleScatterChartInstance.dispose()
        }
        scheduleScatterChartInstance = echarts.init(scheduleScatterChart.value)
        
        // 处理散点图数据
        const scatterData = []
        if (scheduleAnalysis.value.schedule_analysis) {
          for (const key in scheduleAnalysis.value.schedule_analysis) {
            const item = scheduleAnalysis.value.schedule_analysis[key]
            if (item.score) {
              // 使用周几和节次作为x和y坐标，成绩作为点的大小和颜色
              scatterData.push([
                item.day_of_week,
                item.period,
                item.score
              ])
            }
          }
        }
        
        const option = {
          title: {
            text: '课程安排与成绩关系',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              return `周${params.value[0]} 第${params.value[1]}节<br/>成绩: ${params.value[2]}`
            }
          },
          xAxis: {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7'],
            name: '周几'
          },
          yAxis: {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7', '8'],
            name: '节次'
          },
          series: [
            {
              name: '成绩',
              type: 'scatter',
              data: scatterData,
              symbolSize: function(val) {
                return val[2] / 10
              },
              itemStyle: {
                color: function(params) {
                  const score = params.value[2]
                  if (score >= 90) return '#52c41a'
                  if (score >= 80) return '#1890ff'
                  if (score >= 70) return '#faad14'
                  if (score >= 60) return '#fa8c16'
                  return '#f5222d'
                }
              }
            }
          ]
        }
        
        scheduleScatterChartInstance.setOption(option)
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      studentSubjectChartInstance?.resize()
      subjectDistributionChartInstance?.resize()
      subjectBoxPlotChartInstance?.resize()
      examTrendChartInstance?.resize()
      scheduleScatterChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadStudents()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      studentSubjectChartInstance?.dispose()
      subjectDistributionChartInstance?.dispose()
      subjectBoxPlotChartInstance?.dispose()
      examTrendChartInstance?.dispose()
      scheduleScatterChartInstance?.dispose()
    })
    
    return {
      studentId,
      students,
      isLoadingStudents,
      selectedStudentName,
      selectedSubject,
      subjects,
      studentAnalysis: {
        student_info: studentInfo.value,
        overall: overall.value,
        subject_averages: subjectAverages.value,
        class_averages: classAverages.value,
        strengths: strengths.value,
        weaknesses: weaknesses.value
      },
      subjectAnalysis,
      examTrend,
      scheduleAnalysis,
      loading,
      studentError: error.value,
      studentSubjectChart,
      subjectDistributionChart,
      subjectBoxPlotChart,
      examTrendChart,
      scheduleScatterChart,
      analyzeStudent,
      analyzeSubject
    }
  }
}
</script>

<style scoped>
.individual-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.student-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.student-input select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
}

.filter-select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.student-input button {
  padding: 10px 20px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-detail {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.error {
  text-align: center;
  padding: 40px;
  color: #f56c6c;
  background: #fef0f0;
  border-radius: 4px;
}

.student-analysis {
  margin-top: 20px;
}

.student-info {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.info-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.info-header h4 {
  margin: 0;
  color: #333;
}

.info-icon {
  font-size: 20px;
  margin-left: 10px;
}

.student-info p {
  margin: 8px 0;
  color: #666;
}

.overall-performance {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.overall-performance h4 {
  margin-bottom: 15px;
  color: #333;
}

.overall-performance p {
  margin: 8px 0;
  color: #666;
}

.subject-analysis {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.subject-analysis h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.chart {
  width: 100%;
  height: 400px;
  display: block;
  position: relative;
}

.strengths-weaknesses {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.strengths,
.weaknesses {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.strengths h4,
.weaknesses h4 {
  margin-bottom: 15px;
  color: #333;
}

.strengths ul,
.weaknesses ul {
  list-style: none;
  padding: 0;
}

.strengths li,
.weaknesses li {
  margin: 8px 0;
  color: #666;
}

.subject-selector {
  margin: 20px 0;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.subject-selector h4 {
  margin-bottom: 10px;
  color: #333;
}

.specific-subject-analysis {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.subject-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.exam-trend-analysis {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.exam-trend-analysis h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

@media (max-width: 768px) {
  .student-input {
    flex-direction: column;
  }
  
  .strengths-weaknesses {
    grid-template-columns: 1fr;
  }
  
  .subject-stats {
    grid-template-columns: 1fr 1fr;
  }
}
</style>