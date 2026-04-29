<template>
  <div class="grade-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
    </div>
    <BaseECharts
      :chart-type="chartType"
      :data="data"
      :options="chartOptions"
      height="400px"
    />
  </div>
</template>

<script>
import BaseECharts from '../common/BaseECharts.vue';
import { computed, defineProps } from 'vue';

export default {
  name: 'GradeChart',
  components: {
    BaseECharts
  },
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
    // 计算图表配置
    const chartOptions = computed(() => {
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
      };
      
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
          };
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
          };
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
          };
        case 'radar':
          return {
            ...baseOption,
            radar: {
              indicator: props.data.indicator || []
            },
            series: props.data.series || []
          };
        default:
          return baseOption;
      }
    });
    
    return {
      chartOptions
    };
  }
};
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