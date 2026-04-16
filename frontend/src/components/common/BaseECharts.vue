<template>
  <div class="base-echarts">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <span>{{ loadingText }}</span>
    </div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else ref="chartRef" class="chart"></div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, defineProps, defineEmits } from 'vue'

export default {
  name: 'BaseECharts',
  props: {
    chartType: {
      type: String,
      required: true
    },
    data: {
      type: Object,
      default: () => ({})
    },
    options: {
      type: Object,
      default: () => ({})
    },
    loading: {
      type: Boolean,
      default: false
    },
    loadingText: {
      type: String,
      default: '加载中...'
    },
    error: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: '400px'
    },
    width: {
      type: String,
      default: '100%'
    }
  },
  emits: ['chart-init', 'chart-update', 'chart-error'],
  setup(props, { emit }) {
    const chartRef = ref(null)
    let chartInstance = null
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
        const { BarChart, LineChart, RadarChart, PieChart, BoxplotChart, HeatmapChart, ScatterChart } = charts
        const { 
          TitleComponent, TooltipComponent, LegendComponent, 
          GridComponent, DataZoomComponent, ToolboxComponent,
          VisualMapComponent
        } = components
        const { CanvasRenderer } = renderers
        
        use([
          BarChart, LineChart, RadarChart, PieChart, BoxplotChart, HeatmapChart, ScatterChart,
          TitleComponent, TooltipComponent, LegendComponent, GridComponent,
          DataZoomComponent, ToolboxComponent, VisualMapComponent,
          CanvasRenderer
        ])
        
        echarts = echartsCore
        return true
      } catch (err) {
        emit('chart-error', err.message)
        return false
      }
    }
    
    // 初始化图表
    const initChart = async () => {
      if (!chartRef.value) return
      
      // 确保 ECharts 已加载
      if (!echarts) {
        const loaded = await loadECharts()
        if (!loaded) return
      }
      
      // 销毁现有实例
      if (chartInstance) {
        chartInstance.dispose()
      }
      
      try {
        chartInstance = echarts.init(chartRef.value)
        updateChart()
        emit('chart-init', chartInstance)
      } catch (err) {
        emit('chart-error', err.message)
      }
    }
    
    // 更新图表
    const updateChart = () => {
      if (!chartInstance || !props.data) return
      
      try {
        const option = getChartOption()
        chartInstance.setOption(option)
        emit('chart-update', chartInstance)
      } catch (err) {
        emit('chart-error', err.message)
      }
    }
    
    // 获取图表配置
    const getChartOption = () => {
      const baseOption = {
        ...props.options
      }
      
      return baseOption
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      chartInstance?.resize()
    }
    
    // 监听数据变化
    watch(() => props.data, () => {
      updateChart()
    }, { deep: true })
    
    // 监听选项变化
    watch(() => props.options, () => {
      updateChart()
    }, { deep: true })
    
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
.base-echarts {
  position: relative;
}

.chart {
  width: v-bind(width);
  height: v-bind(height);
}

.loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #5470c6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #fef0f0;
  color: #f56c6c;
  padding: 20px;
  text-align: center;
  z-index: 10;
}
</style>