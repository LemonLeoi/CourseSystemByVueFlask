<template>
  <div class="overall-analysis">
    <h3>整体成绩分析</h3>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="overall-stats">
      <div class="stat-card">
        <h4>总体统计</h4>
        <p>总记录数: {{ overallStats.total_count }}</p>
        <p>平均成绩: {{ overallStats.average }}</p>
        <p>标准差: {{ overallStats.std_deviation }}</p>
        <p>中位数: {{ overallStats.median }}</p>
        <p>最高分: {{ overallStats.max_score }}</p>
        <p>最低分: {{ overallStats.min_score }}</p>
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
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch } from 'vue'
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
    
    // 初始化整体分析
    onMounted(async () => {
      await getOverallAnalysis()
    })
    
    // 监听整体统计数据变化，更新图表
    watch(overallStats, (newStats) => {
      if (newStats && Object.keys(newStats).length > 0) {
        initDistributionChart()
        initSubjectChart()
      }
    }, { deep: true })
    
    // 初始化成绩分布图表
    const initDistributionChart = () => {
      if (distributionChart.value) {
        if (distributionChartInstance) {
          distributionChartInstance.dispose()
        }
        distributionChartInstance = echarts.init(distributionChart.value)
        
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
                { value: overallStats.value.distribution.excellent, name: '优秀' },
                { value: overallStats.value.distribution.good, name: '良好' },
                { value: overallStats.value.distribution.average, name: '中等' },
                { value: overallStats.value.distribution.pass, name: '及格' },
                { value: overallStats.value.distribution.fail, name: '不及格' }
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
        
        distributionChartInstance.setOption(option)
      }
    }
    
    // 初始化学科平均成绩图表
    const initSubjectChart = () => {
      if (subjectChart.value && overallStats.value.subjects) {
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
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      distributionChartInstance?.resize()
      subjectChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
    })
    
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
}

@media (max-width: 768px) {
  .overall-stats {
    grid-template-columns: 1fr;
  }
}
</style>