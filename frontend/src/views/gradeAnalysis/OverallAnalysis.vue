<template>
  <div class="overall-analysis">
    <h3>整体成绩分析</h3>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="overall-stats">
      <div class="stat-card">
        <h4>总体统计</h4>
        <p>总记录数: {{ overallStats.overall?.total_count || 0 }}</p>
        <p>平均成绩: {{ overallStats.overall?.average || 0 }}</p>
        <p>标准差: {{ overallStats.overall?.std_deviation || 0 }}</p>
        <p>中位数: {{ overallStats.overall?.median || 0 }}</p>
        <p>最高分: {{ overallStats.overall?.max_score || 0 }}</p>
        <p>最低分: {{ overallStats.overall?.min_score || 0 }}</p>
        
      </div>
      
      <div class="chart-container">
        <h4>成绩分布</h4>
        <div ref="distributionChart" class="chart"></div>
      </div>
      
      <div class="chart-container">
        <h4>学科平均成绩</h4>
        <div ref="subjectChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useGradeAnalysis } from '../../composables/grade/useGradeAnalysis'

export default {
  name: 'OverallAnalysis',
  setup() {
    const { 
      overallStats, 
      loading, 
      error,
      getOverallAnalysis 
    } = useGradeAnalysis()
    
    // 图表引用
    const distributionChart = ref(null)
    const subjectChart = ref(null)
    
    // 图表实例
    let distributionChartInstance = null
    let subjectChartInstance = null
    
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
        const { BarChart, PieChart } = charts
        const { 
          TitleComponent, TooltipComponent, LegendComponent, 
          GridComponent
        } = components
        const { CanvasRenderer } = renderers
        
        use([
          BarChart, PieChart,
          TitleComponent, TooltipComponent, LegendComponent, GridComponent,
          CanvasRenderer
        ])
        
        echarts = echartsCore
        return true
      } catch (err) {
        console.error('加载 ECharts 失败:', err)
        return false
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      distributionChartInstance?.resize()
      subjectChartInstance?.resize()
    }
    
    // 初始化成绩分布图表
    const initDistributionChart = async () => {
      console.log('initDistributionChart called')
      console.log('distributionChart.value:', distributionChart.value)
      console.log('overallStats.value.overall:', overallStats.value.overall)
      if (distributionChart.value && overallStats.value.overall) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        console.log('Creating ECharts instance')
        if (distributionChartInstance) {
          distributionChartInstance.dispose()
        }
        distributionChartInstance = echarts.init(distributionChart.value)
        console.log('ECharts instance created:', distributionChartInstance)
        
        const option = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: ['优秀', '良好', '中等', '及格', '不及格']
          },
          series: [
            {
              name: '成绩等级',
              type: 'pie',
              radius: '50%',
              data: [
                { value: overallStats.value.overall.distribution.excellent, name: '优秀' },
                { value: overallStats.value.overall.distribution.good, name: '良好' },
                { value: overallStats.value.overall.distribution.average, name: '中等' },
                { value: overallStats.value.overall.distribution.pass, name: '及格' },
                { value: overallStats.value.overall.distribution.fail, name: '不及格' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        
        console.log('Setting option:', option)
        distributionChartInstance.setOption(option)
        console.log('Option set')
      } else {
        console.log('Initialization conditions not met')
      }
    }
    
    // 初始化学科平均成绩图表
    const initSubjectChart = async () => {
      if (subjectChart.value && overallStats.value.subjects) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (subjectChartInstance) {
          subjectChartInstance.dispose()
        }
        subjectChartInstance = echarts.init(subjectChart.value)
        
        const subjects = Object.keys(overallStats.value.subjects)
        const averages = subjects.map(subject => overallStats.value.subjects[subject].average)
        
        const option = {
          title: {
            text: '各学科平均成绩',
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
                color: '#5470c6'
              }
            }
          ]
        }
        
        subjectChartInstance.setOption(option)
      }
    }
    
    // 初始化整体分析
    onMounted(async () => {
      console.log('onMounted called')
      try {
        await getOverallAnalysis()
        console.log('getOverallAnalysis completed')
        console.log('overallStats.value:', overallStats.value)
        // 使用nextTick确保DOM已经渲染完成
        nextTick(async () => {
          console.log('nextTick called')
          await initDistributionChart()
          await initSubjectChart()
        })
      } catch (error) {
        console.error('Error in onMounted:', error)
      }
      // 添加窗口大小变化监听
      window.addEventListener('resize', handleResize)
    })
    
    // 监听整体统计数据变化，更新图表
    watch(overallStats, async (newStats) => {
      if (newStats && Object.keys(newStats).length > 0) {
        // 使用nextTick确保DOM已经渲染完成
        nextTick(async () => {
          await initDistributionChart()
          await initSubjectChart()
        })
      }
    }, { deep: true })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      distributionChartInstance?.dispose()
      subjectChartInstance?.dispose()
    })
    
    return {
      overallStats,
      loading,
      error,
      distributionChart,
      subjectChart
    }
  }
}
</script>

<style scoped>
.overall-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
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

.overall-stats {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
  margin-top: 20px;
}

.stat-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.stat-card h4 {
  margin-bottom: 15px;
  color: #333;
}

.stat-card p {
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
  min-width: 400px;
  min-height: 400px;
  border: 1px solid #eee;
  background-color: white;
  display: block;
  position: relative;
}

@media (max-width: 768px) {
  .overall-stats {
    grid-template-columns: 1fr;
  }
}
</style>