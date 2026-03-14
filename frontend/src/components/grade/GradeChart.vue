<template>
  <div class="grade-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
    </div>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { ref, onMounted, onUnmounted, watch, defineProps } from 'vue'

export default {
  name: 'GradeChart',
  props: {
    title: {
      type: String,
      default: '成绩图表'
    },
    chartType: {
      type: String,
      default: 'bar',
      validator: (value) => ['bar', 'line', 'pie', 'radar'].includes(value)
    },
    data: {
      type: Object,
      default: () => ({})
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const chartRef = ref(null)
    let chartInstance = null
    
    // 初始化图表
    const initChart = () => {
      if (chartRef.value) {
        if (chartInstance) {
          chartInstance.dispose()
        }
        chartInstance = echarts.init(chartRef.value)
        
        const option = getChartOption()
        chartInstance.setOption(option)
      }
    }
    
    // 获取图表配置
    const getChartOption = () => {
      const baseOption = {
        title: {
          text: props.title,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        ...props.options
      }
      
      switch (props.chartType) {
        case 'bar':
          return {
            ...baseOption,
            xAxis: {
              type: 'category',
              data: props.data.labels || [],
              axisLabel: {
                rotate: 45
              }
            },
            yAxis: {
              type: 'value',
              name: props.data.yAxisName || '分数'
            },
            series: props.data.series || []
          }
        case 'line':
          return {
            ...baseOption,
            xAxis: {
              type: 'category',
              data: props.data.labels || []
            },
            yAxis: {
              type: 'value',
              name: props.data.yAxisName || '分数'
            },
            series: props.data.series || []
          }
        case 'pie':
          return {
            ...baseOption,
            tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            legend: {
              orient: 'vertical',
              left: 'left',
              data: props.data.labels || []
            },
            series: props.data.series || []
          }
        case 'radar':
          return {
            ...baseOption,
            radar: {
              indicator: props.data.indicator || []
            },
            series: props.data.series || []
          }
        default:
          return baseOption
      }
    }
    
    // 监听数据变化
    watch(() => props.data, () => {
      initChart()
    }, { deep: true })
    
    // 监听图表类型变化
    watch(() => props.chartType, () => {
      initChart()
    })
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      chartInstance?.resize()
    }
    
    onMounted(() => {
      initChart()
      window.addEventListener('resize', handleResize)
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      chartInstance?.dispose()
    })
    
    return {
      chartRef
    }
  }
}
</script>

<style scoped>
.grade-chart {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h3 {
  margin: 0;
  color: #333;
  text-align: center;
}

.chart {
  width: 100%;
  height: 400px;
}
</style>