<template>
  <div class="feature-importance-chart">
    <div class="chart-header">
      <div class="header-icon">📊</div>
      <div class="header-content">
        <h3 class="chart-title">特征重要性分析</h3>
        <p class="chart-subtitle">Feature Importance Analysis</p>
      </div>
    </div>
    
    <div class="academic-note">
      <span class="note-icon">📚</span>
      <span class="note-text">排序基于 <strong>C4.5算法的信息增益比(Gain Ratio)</strong> 计算</span>
    </div>
    
    <div ref="chartRef" class="chart-container"></div>
    
    <div class="chart-legend">
      <div class="legend-item">
        <span class="legend-color" style="background: linear-gradient(90deg, #667eea, #764ba2);"></span>
        <span class="legend-text">信息增益比</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';

export interface FeatureImportanceItem {
  name: string;
  value: number;
  description: string;
  theoreticalBasis: string;
}

const props = defineProps<{
  data: FeatureImportanceItem[];
}>();

const chartRef = ref<HTMLElement | null>(null);
let chartInstance: any = null;
let handleResize: (() => void) | null = null;

const initChart = async () => {
  if (!chartRef.value) return;
  
  try {
    const echartsCore = await import('echarts/core');
    const charts = await import('echarts/charts');
    const components = await import('echarts/components');
    const renderers = await import('echarts/renderers');
    
    const { use, init } = echartsCore;
    const { BarChart } = charts;
    const { 
      TitleComponent, TooltipComponent, LegendComponent, 
      GridComponent
    } = components;
    const { CanvasRenderer } = renderers;
    
    use([
      BarChart,
      TitleComponent, TooltipComponent, LegendComponent, GridComponent,
      CanvasRenderer
    ]);
    
    if (chartInstance) {
      chartInstance.dispose();
    }
    
    chartInstance = init(chartRef.value);
    
    const sortedData = [...props.data].sort((a, b) => b.value - a.value);
    const names = sortedData.map(item => item.name);
    const values = sortedData.map(item => item.value);
    
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: 'rgba(255, 255, 255, 0.98)',
        borderColor: '#d1d5db',
        borderWidth: 1,
        padding: [12, 16],
        textStyle: { color: '#374151', fontSize: 14 },
        extraCssText: 'overflow: visible; z-index: 9999; pointer-events: none;',
        appendToBody: true,
        formatter: (params: any) => {
          const dataIndex = params.dataIndex;
          if (!sortedData || !sortedData[dataIndex]) {
            return '';
          }
          const data = sortedData[dataIndex];
          return `<div style="padding: 8px;">
            <div style="font-weight: 600; margin-bottom: 8px; color: #1f2937;">${data.name || '未知'}</div>
            <div style="color: #667eea; font-size: 16px; font-weight: 600;">信息增益比: ${data.value ? data.value.toFixed(4) : '0.0000'}</div>
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #6b7280;">${data.description || ''}</div>
            <div style="margin-top: 4px; font-size: 11px; color: #9ca3af; font-style: italic;">${data.theoreticalBasis || ''}</div>
          </div>`;
        }
      },
      grid: {
        left: '3%',
        right: '8%',
        bottom: '3%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'value',
        name: '信息增益比',
        nameTextStyle: {
          color: '#6b7280',
          fontSize: 12
        },
        axisLine: {
          lineStyle: { color: '#e5e7eb' }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#6b7280',
          fontSize: 12,
          formatter: (value: number) => value.toFixed(3)
        },
        splitLine: {
          lineStyle: {
            color: '#f3f4f6',
            type: 'dashed'
          }
        }
      },
      yAxis: {
        type: 'category',
        data: names.reverse(),
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#374151',
          fontSize: 13,
          fontWeight: 500
        }
      },
      series: [
        {
          name: '信息增益比',
          type: 'bar',
          data: values.reverse(),
          barWidth: '60%',
          itemStyle: {
            borderRadius: [0, 4, 4, 0],
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: '#667eea' },
                { offset: 1, color: '#764ba2' }
              ]
            }
          },
          emphasis: {
            itemStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 1,
                y2: 0,
                colorStops: [
                  { offset: 0, color: '#5a6fd6' },
                  { offset: 1, color: '#6a4190' }
                ]
              }
            }
          },
          label: {
            show: true,
            position: 'right',
            formatter: (params: any) => params.value.toFixed(4),
            color: '#6b7280',
            fontSize: 12,
            fontWeight: 500
          }
        }
      ],
      animationDuration: 1000,
      animationEasing: 'cubicOut'
    };
    
    chartInstance.setOption(option);
    
    handleResize = () => {
      chartInstance?.resize();
    };
    
    window.addEventListener('resize', handleResize);
  } catch (error) {
    console.error('Failed to load ECharts:', error);
  }
};

const cleanupChart = () => {
  if (handleResize) {
    window.removeEventListener('resize', handleResize);
    handleResize = null;
  }
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
};

onUnmounted(() => {
  cleanupChart();
});

onMounted(() => {
  initChart();
});

watch(() => props.data, () => {
  initChart();
}, { deep: true });
</script>

<style scoped>
.feature-importance-chart {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
  position: relative;
  overflow: visible;
}

.chart-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.header-icon {
  font-size: 24px;
  margin-right: 10px;
}

.header-content {
  flex: 1;
}

.chart-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.chart-subtitle {
  margin: 2px 0 0 0;
  font-size: 12px;
  color: #9ca3af;
}

.academic-note {
  display: flex;
  align-items: center;
  padding: 10px 14px;
  background: #f0fdf4;
  border-radius: 6px;
  margin-bottom: 16px;
  border-left: 3px solid #10b981;
}

.note-icon {
  font-size: 14px;
  margin-right: 8px;
}

.note-text {
  font-size: 13px;
  color: #065f46;
  line-height: 1.5;
}

.note-text strong {
  color: #059669;
}

.chart-container {
  height: 300px;
  width: 100%;
  position: relative;
  overflow: visible;
}

.chart-legend {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
}

.legend-color {
  width: 24px;
  height: 12px;
  border-radius: 2px;
  margin-right: 8px;
}

.legend-text {
  font-size: 12px;
  color: #6b7280;
}

@media (max-width: 768px) {
  .feature-importance-chart {
    padding: 16px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .academic-note {
    padding: 8px 12px;
  }
  
  .note-text {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .chart-container {
    height: 200px;
  }
  
  .chart-title {
    font-size: 14px;
  }
  
  .academic-note {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .note-icon {
    margin-bottom: 4px;
  }
}
</style>