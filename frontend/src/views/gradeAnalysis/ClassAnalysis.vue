<template>
  <div class="class-analysis">
    <h3>班级成绩分析</h3>
    <div class="class-input">
      <select 
        v-model="className" 
        class="filter-select"
      >
        <option value="">请选择班级</option>
        <option v-for="classItem in classes" :key="classItem" :value="classItem">
          {{ classItem }}
        </option>
      </select>
      <button @click="analyzeClass">分析</button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="classError" class="error">{{ classError }}</div>
    <div v-else-if="classAnalysis" class="class-analysis-result">
      <div class="class-info">
        <div class="info-header">
          <h4>班级信息</h4>
          <div class="info-icon">🏫</div>
        </div>
        <p>班级名称: {{ classAnalysis.class_info.class_name }}</p>
        <p>年级: {{ classAnalysis.class_info.grade }}</p>
        <p>学生人数: {{ classAnalysis.class_info.student_count }}</p>
        <p>班级平均成绩: {{ classAnalysis.overall_average }}</p>
      </div>
      
      <div class="chart-container">
        <div class="info-header">
          <h4>学科平均成绩</h4>
          <div class="info-icon">📊</div>
        </div>
        <div ref="classSubjectChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useGradeAnalysis } from '../../composables/grade/useGradeAnalysis'

export default {
  name: 'ClassAnalysis',
  setup() {
    const { 
      classAnalysis, 
      loading, 
      classError,
      getClassAnalysis 
    } = useGradeAnalysis()
    
    const className = ref('')
    const classes = ref([])
    const grades = ref([])
    const isLoadingOptions = ref(false)
    
    // 图表引用
    const classSubjectChart = ref(null)
    
    // 图表实例
    let classSubjectChartInstance = null
    
    // 加载班级和年级列表
    const loadClassOptions = async () => {
      isLoadingOptions.value = true
      try {
        const response = await fetch('http://localhost:5000/api/students/classes')
        if (response.ok) {
          const data = await response.json()
          grades.value = data.grades || []
          classes.value = data.classes || []
          
          // 生成完整的班级名称（如：高一(1)）
          const fullClasses = []
          grades.value.forEach(grade => {
            classes.value.forEach(classNum => {
              fullClasses.push(`${grade}(${classNum})`)
            })
          })
          classes.value = fullClasses
        }
      } catch (error) {
        console.error('获取班级和年级列表失败:', error)
        // 失败时使用默认值，确保系统能正常运行
        grades.value = ['高一', '高二', '高三']
        classes.value = ['1班', '2班', '3班', '4班', '5班']
        
        // 生成完整的班级名称（如：高一(1)）
        const fullClasses = []
        grades.value.forEach(grade => {
          classes.value.forEach(classNum => {
            // 提取班级数字，如 '1班' -> '1'
            const classNumMatch = classNum.match(/\d+/)
            const num = classNumMatch ? classNumMatch[0] : classNum
            fullClasses.push(`${grade}(${num})`)
          })
        })
        classes.value = fullClasses
      } finally {
        isLoadingOptions.value = false
      }
    }
    
    // 分析班级成绩
    const analyzeClass = async () => {
      if (className.value) {
        await getClassAnalysis(className.value)
      }
    }
    
    // 监听班级分析数据变化，更新图表
    watch(classAnalysis, (newAnalysis) => {
      if (newAnalysis && Object.keys(newAnalysis).length > 0) {
        initClassSubjectChart()
      }
    }, { deep: true })
    
    // 初始化班级学科成绩图表
    const initClassSubjectChart = () => {
      if (classSubjectChart.value && classAnalysis.value) {
        if (classSubjectChartInstance) {
          classSubjectChartInstance.dispose()
        }
        classSubjectChartInstance = echarts.init(classSubjectChart.value)
        
        const subjects = Object.keys(classAnalysis.value.subject_averages)
        const averages = subjects.map(subject => classAnalysis.value.subject_averages[subject])
        
        const option = {
          title: {
            text: '班级各学科平均成绩',
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
                color: '#fac858'
              }
            }
          ]
        }
        
        classSubjectChartInstance.setOption(option)
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      classSubjectChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadClassOptions()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      classSubjectChartInstance?.dispose()
    })
    
    return {
      className,
      classes,
      grades,
      isLoadingOptions,
      classAnalysis,
      loading,
      classError,
      classSubjectChart,
      analyzeClass
    }
  }
}
</script>

<style scoped>
.class-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.class-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.class-input select {
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

.class-input button {
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

.class-analysis-result {
  margin-top: 20px;
}

.class-info {
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

.class-info p {
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
  .class-input {
    flex-direction: column;
  }
}
</style>