<template>
  <div class="grade-analysis">
    <h3>年级成绩分析</h3>
    <div class="grade-input">
      <select 
        v-model="gradeName" 
        class="filter-select"
      >
        <option value="">请选择年级</option>
        <option v-for="grade in grades" :key="grade" :value="grade">
          {{ grade }}
        </option>
      </select>
      <button @click="analyzeGrade">分析</button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="gradeError" class="error">{{ gradeError }}</div>
    <div v-else-if="gradeAnalysis" class="grade-analysis-result">
      <div class="grade-info">
        <div class="info-header">
          <h4>年级信息</h4>
          <div class="info-icon">🎓</div>
        </div>
        <p>年级: {{ gradeAnalysis.grade_info.grade }}</p>
        <p>班级数量: {{ gradeAnalysis.grade_info.class_count }}</p>
        <p>年级平均成绩: {{ gradeAnalysis.overall_average }}</p>
      </div>
      
      <div class="chart-container">
        <div class="info-header">
          <h4>学科平均成绩</h4>
          <div class="info-icon">📊</div>
        </div>
        <div ref="gradeSubjectChart" class="chart"></div>
      </div>
      
      <div class="chart-container">
        <div class="info-header">
          <h4>班级平均成绩对比</h4>
          <div class="info-icon">📈</div>
        </div>
        <div ref="classComparisonChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useGradeAnalysis } from '../../composables/grade/useGradeAnalysis'

export default {
  name: 'GradeLevelAnalysis',
  setup() {
    const { 
      gradeAnalysis, 
      loading, 
      gradeError,
      getGradeAnalysis 
    } = useGradeAnalysis()
    
    const gradeName = ref('')
    const grades = ref([])
    const isLoadingOptions = ref(false)
    
    // 图表引用
    const gradeSubjectChart = ref(null)
    const classComparisonChart = ref(null)
    
    // 图表实例
    let gradeSubjectChartInstance = null
    let classComparisonChartInstance = null
    
    // 加载年级列表
    const loadGradeOptions = async () => {
      isLoadingOptions.value = true
      try {
        const response = await fetch('http://localhost:5000/api/students/classes')
        if (response.ok) {
          const data = await response.json()
          grades.value = data.grades || []
        }
      } catch (error) {
        console.error('获取年级列表失败:', error)
      } finally {
        isLoadingOptions.value = false
      }
    }
    
    // 分析年级成绩
    const analyzeGrade = async () => {
      if (gradeName.value) {
        await getGradeAnalysis(gradeName.value)
      }
    }
    
    // 监听年级分析数据变化，更新图表
    watch(gradeAnalysis, (newAnalysis) => {
      if (newAnalysis && Object.keys(newAnalysis).length > 0) {
        initGradeSubjectChart()
        initClassComparisonChart()
      }
    }, { deep: true })
    
    // 初始化年级学科成绩图表
    const initGradeSubjectChart = () => {
      if (gradeSubjectChart.value && gradeAnalysis.value) {
        if (gradeSubjectChartInstance) {
          gradeSubjectChartInstance.dispose()
        }
        gradeSubjectChartInstance = echarts.init(gradeSubjectChart.value)
        
        const subjects = Object.keys(gradeAnalysis.value.subject_averages)
        const averages = subjects.map(subject => gradeAnalysis.value.subject_averages[subject])
        
        const option = {
          title: {
            text: '年级各学科平均成绩',
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
            data: subjects,
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value',
            name: '平均分'
          },
          series: [
            {
              data: averages,
              type: 'bar',
              itemStyle: {
                color: '#ee6666'
              }
            }
          ]
        }
        
        gradeSubjectChartInstance.setOption(option)
      }
    }
    
    // 初始化班级对比图表
    const initClassComparisonChart = () => {
      if (classComparisonChart.value && gradeAnalysis.value) {
        if (classComparisonChartInstance) {
          classComparisonChartInstance.dispose()
        }
        classComparisonChartInstance = echarts.init(classComparisonChart.value)
        
        const classes = Object.keys(gradeAnalysis.value.class_averages)
        const subjects = Object.keys(gradeAnalysis.value.subject_averages)
        
        const series = subjects.map((subject, index) => {
          const data = classes.map(className => {
            return gradeAnalysis.value.class_averages[className][subject] || 0
          })
          
          return {
            name: subject,
            type: 'radar',
            data: [{
              value: data,
              name: subject
            }]
          }
        })
        
        const option = {
          title: {
            text: '班级成绩对比',
            left: 'center'
          },
          tooltip: {},
          legend: {
            data: subjects,
            bottom: 0
          },
          radar: {
            indicator: classes.map(className => ({
              name: className,
              max: 100
            }))
          },
          series: series
        }
        
        classComparisonChartInstance.setOption(option)
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      gradeSubjectChartInstance?.resize()
      classComparisonChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadGradeOptions()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      gradeSubjectChartInstance?.dispose()
      classComparisonChartInstance?.dispose()
    })
    
    return {
      gradeName,
      grades,
      isLoadingOptions,
      gradeAnalysis,
      loading,
      gradeError,
      gradeSubjectChart,
      classComparisonChart,
      analyzeGrade
    }
  }
}
</script>

<style scoped>
.grade-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.grade-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.grade-input select {
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

.grade-input button {
  padding: 10px 20px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.error {
  text-align: center;
  padding: 40px;
  color: #f56c6c;
  background: #fef0f0;
  border-radius: 4px;
}

.grade-analysis-result {
  margin-top: 20px;
}

.grade-info {
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

.grade-info p {
  margin: 8px 0;
  color: #666;
}

.chart-container {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.chart-container h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.chart {
  width: 100%;
  height: 400px;
}

@media (max-width: 768px) {
  .grade-input {
    flex-direction: column;
  }
}
</style>