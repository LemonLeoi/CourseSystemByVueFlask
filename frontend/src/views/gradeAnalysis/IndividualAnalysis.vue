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
    <div v-else-if="studentAnalysis" class="student-analysis">
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
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useGradeAnalysis } from '../../composables/grade/useGradeAnalysis'

export default {
  name: 'IndividualAnalysis',
  setup() {
    const { 
      studentAnalysis, 
      loading, 
      studentError,
      getStudentAnalysis 
    } = useGradeAnalysis()
    
    const studentId = ref('')
    const students = ref([])
    const isLoadingStudents = ref(false)
    const selectedStudentName = ref('')
    
    // 图表引用
    const studentSubjectChart = ref(null)
    
    // 图表实例
    let studentSubjectChartInstance = null
    
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
      }
    }
    
    // 监听学生分析数据变化，更新图表
    watch(studentAnalysis, (newAnalysis) => {
      if (newAnalysis && Object.keys(newAnalysis).length > 0) {
        initStudentSubjectChart()
      }
    }, { deep: true })
    
    // 初始化学生学科成绩图表
    const initStudentSubjectChart = () => {
      if (studentSubjectChart.value && studentAnalysis.value) {
        if (studentSubjectChartInstance) {
          studentSubjectChartInstance.dispose()
        }
        studentSubjectChartInstance = echarts.init(studentSubjectChart.value)
        
        const subjects = Object.keys(studentAnalysis.value.subject_averages)
        const personalAverages = subjects.map(subject => studentAnalysis.value.subject_averages[subject])
        const classAverages = subjects.map(subject => studentAnalysis.value.class_averages[subject] || 0)
        
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
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      studentSubjectChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadStudents()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      studentSubjectChartInstance?.dispose()
    })
    
    return {
      studentId,
      students,
      isLoadingStudents,
      selectedStudentName,
      studentAnalysis,
      loading,
      studentError,
      studentSubjectChart,
      analyzeStudent
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
}

.strengths-weaknesses {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
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

@media (max-width: 768px) {
  .student-input {
    flex-direction: column;
  }
  
  .strengths-weaknesses {
    grid-template-columns: 1fr;
  }
}
</style>