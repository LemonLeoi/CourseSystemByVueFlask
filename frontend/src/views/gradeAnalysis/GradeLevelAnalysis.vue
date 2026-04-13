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
    <div v-else-if="gradeAnalysis && gradeAnalysis.grade_info" class="grade-analysis-result">
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
        </div>
        <div ref="subjectDistributionChart" class="chart"></div>
        <div ref="subjectBoxPlotChart" class="chart"></div>
      </div>
      
      <!-- 新增：历次考试趋势图表 -->
      <div class="exam-trend-analysis">
        <div class="info-header">
          <h4>年级历次考试趋势</h4>
          <div class="info-icon">📈</div>
        </div>
        <div ref="examTrendChart" class="chart"></div>
      </div>
      
      <!-- 新增：教师成绩对比模块 -->
      <div v-if="teacherPerformance" class="teacher-performance-analysis">
        <div class="info-header">
          <h4>教师成绩对比</h4>
          <div class="info-icon">👨‍🏫</div>
        </div>
        <div ref="teacherComparisonChart" class="chart"></div>
      </div>
      
      <!-- 新增：教师与成绩关系热力图 -->
      <div v-if="teacherPerformance" class="teacher-heatmap-analysis">
        <div class="info-header">
          <h4>教师与成绩关系热力图</h4>
          <div class="info-icon">🔥</div>
        </div>
        <div ref="teacherHeatmapChart" class="chart"></div>
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
      subjectAnalysis,
      examTrend,
      teacherPerformance,
      loading, 
      gradeError,
      subjectError,
      trendError,
      teacherError,
      getGradeAnalysis,
      getGradeSubjectAnalysis,
      getGradeTrend,
      getTeacherPerformance
    } = useGradeAnalysis()
    
    const gradeName = ref('')
    const grades = ref([])
    const isLoadingOptions = ref(false)
    const selectedSubject = ref('')
    const subjects = ref([])
    
    // 图表引用
    const gradeSubjectChart = ref(null)
    const classComparisonChart = ref(null)
    const subjectDistributionChart = ref(null)
    const subjectBoxPlotChart = ref(null)
    const examTrendChart = ref(null)
    const teacherComparisonChart = ref(null)
    const teacherHeatmapChart = ref(null)
    
    // 图表实例
    let gradeSubjectChartInstance = null
    let classComparisonChartInstance = null
    let subjectDistributionChartInstance = null
    let subjectBoxPlotChartInstance = null
    let examTrendChartInstance = null
    let teacherComparisonChartInstance = null
    let teacherHeatmapChartInstance = null
    
    // 加载年级列表
    const loadGradeOptions = async () => {
      isLoadingOptions.value = true
      try {
        const response = await fetch('/api/students/classes')
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
        // 加载考试趋势
        await getGradeTrend(gradeName.value)
        // 提取科目列表
        if (gradeAnalysis.value && gradeAnalysis.value.subject_averages) {
          subjects.value = Object.keys(gradeAnalysis.value.subject_averages)
        }
      }
    }
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (gradeName.value && selectedSubject.value) {
        await getGradeSubjectAnalysis(gradeName.value, selectedSubject.value)
        // 加载教师成绩对比
        await getTeacherPerformance(selectedSubject.value)
      }
    }
    
    // 监听年级分析数据变化，更新图表
    watch(gradeAnalysis, (newAnalysis) => {
      if (newAnalysis && Object.keys(newAnalysis).length > 0) {
        // 使用nextTick确保DOM渲染完成后再初始化图表
        setTimeout(() => {
          initGradeSubjectChart()
          initClassComparisonChart()
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
    
    // 监听教师成绩对比数据变化，更新图表
    watch(teacherPerformance, () => {
      if (teacherPerformance.value) {
        setTimeout(() => {
          initTeacherComparisonChart()
          initTeacherHeatmapChart()
        }, 0)
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
        
        // 使用柱状图展示班级间的成绩对比
        const series = classes.map((className, index) => {
          const data = subjects.map(subject => {
            return gradeAnalysis.value.class_averages[className][subject] || 0
          })
          
          return {
            name: className,
            type: 'bar',
            data: data,
            barWidth: '15%'
          }
        })
        
        const option = {
          title: {
            text: '班级成绩对比',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: classes,
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
            name: '平均分'
          },
          series: series
        }
        
        classComparisonChartInstance.setOption(option)
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
            text: '年级历次考试趋势',
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
    
    // 初始化教师对比图表
    const initTeacherComparisonChart = () => {
      if (teacherComparisonChart.value && teacherPerformance.value) {
        if (teacherComparisonChartInstance) {
          teacherComparisonChartInstance.dispose()
        }
        teacherComparisonChartInstance = echarts.init(teacherComparisonChart.value)
        
        const teachers = Object.keys(teacherPerformance.value.teacher_performance)
        const data = teachers.map(teacher => teacherPerformance.value.teacher_performance[teacher].average)
        
        const option = {
          title: {
            text: '教师成绩对比',
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
            data: teachers,
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
              type: 'bar',
              data: data,
              itemStyle: {
                color: '#91cc75'
              }
            }
          ]
        }
        
        teacherComparisonChartInstance.setOption(option)
      }
    }
    
    // 初始化教师与成绩关系热力图
    const initTeacherHeatmapChart = () => {
      if (teacherHeatmapChart.value && teacherPerformance.value) {
        if (teacherHeatmapChartInstance) {
          teacherHeatmapChartInstance.dispose()
        }
        teacherHeatmapChartInstance = echarts.init(teacherHeatmapChart.value)
        
        // 处理热力图数据
        const heatmapData = []
        const teachers = Object.keys(teacherPerformance.value.teacher_performance)
        let index = 0
        
        teachers.forEach(teacher => {
          const teacherData = teacherPerformance.value.teacher_performance[teacher]
          // 为每个教师创建一个数据点，使用教师索引作为x轴，平均分为y轴，分数作为热力值
          heatmapData.push([index, 0, teacherData.average])
          index++
        })
        
        const option = {
          title: {
            text: '教师与成绩关系热力图',
            left: 'center'
          },
          tooltip: {
            position: 'top'
          },
          grid: {
            height: '60%',
            top: '10%'
          },
          xAxis: {
            type: 'category',
            data: teachers,
            splitArea: {
              show: true
            },
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'category',
            data: ['平均成绩'],
            splitArea: {
              show: true
            }
          },
          visualMap: {
            min: 60,
            max: 100,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '15%',
            inRange: {
              color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            }
          },
          series: [
            {
              name: '平均成绩',
              type: 'heatmap',
              data: heatmapData,
              label: {
                show: true
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        
        teacherHeatmapChartInstance.setOption(option)
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      gradeSubjectChartInstance?.resize()
      classComparisonChartInstance?.resize()
      subjectDistributionChartInstance?.resize()
      subjectBoxPlotChartInstance?.resize()
      examTrendChartInstance?.resize()
      teacherComparisonChartInstance?.resize()
      teacherHeatmapChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadGradeOptions()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      gradeSubjectChartInstance?.dispose()
      classComparisonChartInstance?.dispose()
      subjectDistributionChartInstance?.dispose()
      subjectBoxPlotChartInstance?.dispose()
      examTrendChartInstance?.dispose()
      teacherComparisonChartInstance?.dispose()
      teacherHeatmapChartInstance?.dispose()
    })
    
    return {
      gradeName,
      grades,
      isLoadingOptions,
      selectedSubject,
      subjects,
      gradeAnalysis,
      subjectAnalysis,
      examTrend,
      teacherPerformance,
      loading,
      gradeError,
      gradeSubjectChart,
      classComparisonChart,
      subjectDistributionChart,
      subjectBoxPlotChart,
      examTrendChart,
      teacherComparisonChart,
      teacherHeatmapChart,
      analyzeGrade,
      analyzeSubject
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
  display: block;
  position: relative;
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

.teacher-performance-analysis {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.teacher-performance-analysis h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

@media (max-width: 768px) {
  .grade-input {
    flex-direction: column;
  }
  
  .subject-stats {
    grid-template-columns: 1fr 1fr;
  }
}
</style>