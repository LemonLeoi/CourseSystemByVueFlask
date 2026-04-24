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
    <div v-else-if="classAnalysis && classAnalysis.class_info" class="class-analysis-result">
      <CollapsibleSection 
        title="班级信息" 
        icon="🏫" 
        :default-collapsed="false"
        storage-key="class_info"
      >
        <p>班级名称: {{ classAnalysis.class_info.class_name }}</p>
        <p>年级: {{ classAnalysis.class_info.grade }}</p>
        <p>学生人数: {{ classAnalysis.class_info.student_count }}</p>
        <p>班级平均成绩: {{ classAnalysis.overall_average }}</p>
      </CollapsibleSection>
      
      <CollapsibleSection 
        title="学科平均成绩" 
        icon="📊"
        storage-key="class_subject_analysis"
      >
        <BaseECharts
          chart-type="bar"
          :data="{ subjectAverages }"
          :options="classSubjectOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：科目选择下拉菜单 -->
      <div class="subject-selector">
        <h4>科目分析</h4>
        <select v-model="selectedSubject" class="filter-select" @change="analyzeSubject">
          <option value="">请选择科目</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
        </select>
      </div>
      
      <!-- 新增：具体科目分析模块 -->
      <CollapsibleSection 
        v-if="subjectAnalysis" 
        :title="selectedSubject + ' 科目分析'" 
        icon="📊"
        storage-key="specific_class_subject_analysis"
      >
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
        <BaseECharts
          chart-type="bar"
          :data="subjectAnalysis"
          :options="subjectDistributionOptions"
          height="400px"
        />
        <BaseECharts
          chart-type="boxplot"
          :data="subjectAnalysis"
          :options="subjectBoxPlotOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：历次考试趋势图表 -->
      <CollapsibleSection 
        title="班级历次考试趋势" 
        icon="📈"
        storage-key="class_exam_trend"
      >
        <BaseECharts
          chart-type="line"
          :data="examTrend"
          :options="examTrendOptions"
          height="400px"
        />
      </CollapsibleSection>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../../components/common/BaseECharts.vue'
import CollapsibleSection from '../../components/common/CollapsibleSection.vue'
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useClassGrade } from '../../composables/grade/useClassGrade'

export default {
  name: 'ClassAnalysis',
  components: {
    BaseECharts,
    CollapsibleSection
  },
  setup() {
    const {
      classInfo,
      subjectAverages,
      overallAverage,
      studentCount,
      subjectAnalysis,
      examTrend,
      loading,
      error,
      getClassAnalysis,
      getClassSubjectAnalysis,
      getClassTrend
    } = useClassGrade()
    
    const className = ref('')
    const classes = ref([])
    const grades = ref([])
    const isLoadingOptions = ref(false)
    const selectedSubject = ref('')
    const subjects = ref([])
    
    // 图表引用
    const classSubjectChart = ref(null)
    const subjectDistributionChart = ref(null)
    const subjectBoxPlotChart = ref(null)
    const examTrendChart = ref(null)
    
    // 图表实例
    let classSubjectChartInstance = null
    let subjectDistributionChartInstance = null
    let subjectBoxPlotChartInstance = null
    let examTrendChartInstance = null
    
    // ECharts 实例
    let echarts = null
    
    // 动态导入 ECharts
    const loadECharts = async () => {
      try {
        // 按需导入核心模块和需要的图表类型
        const echartsCore = await import('echarts/core')
        const charts = await import('echarts/charts')
        const components = await import('echarts/components')
        const renderers = await import('echarts/renderers')
        
        // 注册必要的组件
        const { use, init } = echartsCore
        const { BarChart, LineChart, RadarChart, PieChart, BoxplotChart } = charts
        const { 
          TitleComponent, TooltipComponent, LegendComponent, 
          GridComponent, DataZoomComponent, ToolboxComponent,
          VisualMapComponent
        } = components
        const { CanvasRenderer } = renderers
        
        use([
          BarChart, LineChart, RadarChart, PieChart, BoxplotChart,
          TitleComponent, TooltipComponent, LegendComponent, GridComponent,
          DataZoomComponent, ToolboxComponent, VisualMapComponent,
          CanvasRenderer
        ])
        
        echarts = echartsCore
        return true
      } catch (err) {
        console.error('加载 ECharts 失败:', err)
        return false
      }
    }
    
    // 加载班级和年级列表
    const loadClassOptions = async () => {
      isLoadingOptions.value = true
      try {
        const { studentApi } = await import('../../services/api/apiService')
        const data = await studentApi.getClasses()
        grades.value = data.grades || []
        classes.value = data.classes || []
        
        // 生成完整的班级名称（如：高三1班）
        const fullClasses = []
        grades.value.forEach(grade => {
          classes.value.forEach(classNum => {
            // 提取班级数字，如 '1班' -> '1'
            const classNumMatch = classNum.match(/\d+/)
            const num = classNumMatch ? classNumMatch[0] : classNum
            fullClasses.push(`${grade}${num}班`)
          })
        })
        classes.value = fullClasses
      } catch (error) {
        console.error('获取班级和年级列表失败:', error)
        // 失败时使用默认值，确保系统能正常运行
        grades.value = ['高一', '高二', '高三']
        classes.value = ['1班', '2班', '3班', '4班', '5班']
        
        // 生成完整的班级名称（如：高三1班）
        const fullClasses = []
        grades.value.forEach(grade => {
          classes.value.forEach(classNum => {
            // 提取班级数字，如 '1班' -> '1'
            const classNumMatch = classNum.match(/\d+/)
            const num = classNumMatch ? classNumMatch[0] : classNum
            fullClasses.push(`${grade}${num}班`)
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
        // 加载考试趋势
        await getClassTrend(className.value)
        // 提取科目列表
        if (subjectAverages.value) {
          subjects.value = Object.keys(subjectAverages.value)
        }
      }
    }
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (className.value && selectedSubject.value) {
        await getClassSubjectAnalysis(className.value, selectedSubject.value)
      }
    }
    
    // 监听班级分析数据变化，更新图表
    watch(subjectAverages, async () => {
      if (subjectAverages.value && Object.keys(subjectAverages.value).length > 0) {
        // 使用nextTick确保DOM渲染完成后再初始化图表
        setTimeout(async () => {
          await initClassSubjectChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听科目分析数据变化，更新图表
    watch(subjectAnalysis, async () => {
      if (subjectAnalysis.value) {
        setTimeout(async () => {
          await initSubjectDistributionChart()
          await initSubjectBoxPlotChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听考试趋势数据变化，更新图表
    watch(examTrend, async () => {
      if (examTrend.value) {
        setTimeout(async () => {
          await initExamTrendChart()
        }, 0)
      }
    }, { deep: true })
    
    // 初始化班级学科成绩图表
    const initClassSubjectChart = async () => {
      if (classSubjectChart.value && subjectAverages.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (classSubjectChartInstance) {
          classSubjectChartInstance.dispose()
        }
        classSubjectChartInstance = echarts.init(classSubjectChart.value)
        
        const subjects = Object.keys(subjectAverages.value)
        const averages = subjects.map(subject => subjectAverages.value[subject])
        
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
    
    // 初始化科目分布图表
    const initSubjectDistributionChart = async () => {
      if (subjectDistributionChart.value && subjectAnalysis.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
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
    const initSubjectBoxPlotChart = async () => {
      if (subjectBoxPlotChart.value && subjectAnalysis.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
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
    const initExamTrendChart = async () => {
      if (examTrendChart.value && examTrend.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (examTrendChartInstance) {
          examTrendChartInstance.dispose()
        }
        examTrendChartInstance = echarts.init(examTrendChart.value)
        
        const examNames = examTrend.value.exam_trend.exam_names
        const averages = examTrend.value.exam_trend.averages
        
        const option = {
          title: {
            text: '班级历次考试趋势',
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
    
    // 计算属性，实时更新 classAnalysis
    const classAnalysis = computed(() => ({
      class_info: classInfo.value,
      overall_average: overallAverage.value,
      subject_averages: subjectAverages.value,
      student_count: studentCount.value
    }))
    
    // 班级学科成绩配置
    const classSubjectOptions = computed(() => {
      if (!subjectAverages.value) return {}
      
      const subjects = Object.keys(subjectAverages.value)
      const averages = subjects.map(subject => subjectAverages.value[subject])
      
      return {
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
    })
    
    // 科目分布配置
    const subjectDistributionOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics || !subjectAnalysis.value.statistics.distribution) return {}
      
      const distribution = subjectAnalysis.value.statistics.distribution
      const categories = ['优秀', '良好', '中等', '及格', '不及格']
      const data = [
        distribution.excellent,
        distribution.good,
        distribution.average,
        distribution.pass,
        distribution.fail
      ]
      
      return {
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
    })
    
    // 科目箱线图配置
    const subjectBoxPlotOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics) return {}
      
      // 模拟箱线图数据
      const boxData = [
        [subjectAnalysis.value.statistics.min_score, 
         subjectAnalysis.value.statistics.min_score + 10, 
         subjectAnalysis.value.statistics.median, 
         subjectAnalysis.value.statistics.median + 10, 
         subjectAnalysis.value.statistics.max_score]
      ]
      
      return {
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
    })
    
    // 考试趋势配置
    const examTrendOptions = computed(() => {
      if (!examTrend.value || !examTrend.value.exam_trend) return {}
      
      const examNames = examTrend.value.exam_trend.exam_names
      const averages = examTrend.value.exam_trend.averages
      
      return {
        title: {
          text: '班级历次考试趋势',
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
    })
    
    onMounted(() => {
      loadClassOptions()
    })
    
    return {
      className,
      classes,
      grades,
      isLoadingOptions,
      selectedSubject,
      subjects,
      classAnalysis,
      subjectAnalysis,
      examTrend,
      loading,
      classError: error.value,
      subjectAverages,
      classSubjectOptions,
      subjectDistributionOptions,
      subjectBoxPlotOptions,
      examTrendOptions,
      analyzeClass,
      analyzeSubject
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
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.class-input button:hover {
  background: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.class-input button:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error {
  text-align: center;
  padding: 40px;
  color: #f56c6c;
  background: #fef0f0;
  border-radius: 4px;
  border: 1px solid #fbc4c4;
  animation: shake 0.5s ease-in-out;
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.1);
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.filter-select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
  transition: all 0.3s ease;
  background: #fff;
}

.filter-select:focus {
  border-color: #409eff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(64, 158, 255, 0.25);
  transform: translateY(-1px);
}

.class-analysis-result {
  margin-top: 20px;
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

@media (max-width: 1200px) {
  .class-analysis {
    padding: 15px;
  }
  
  .class-input {
    flex-wrap: wrap;
  }
  
  .class-input select {
    flex: 1 1 200px;
  }
  
  .class-input button {
    flex: 1 1 100px;
  }
}

@media (max-width: 768px) {
  .class-analysis {
    padding: 10px;
  }
  
  .class-input {
    flex-direction: column;
  }
  
  .subject-stats {
    grid-template-columns: 1fr 1fr;
  }
  
  h3 {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .subject-stats {
    grid-template-columns: 1fr;
  }
  
  h3 {
    font-size: 16px;
  }
  
  .loading {
    padding: 20px;
  }
}
</style>