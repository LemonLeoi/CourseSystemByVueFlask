<template>
  <div class="grade-comparison">
    <h3>成绩对比分析</h3>
    <div v-if="data" class="analysis-content">
      <div class="chart-container">
        <BaseECharts
          :chart-type="chartType"
          :data="chartData"
          :options="chartOptions"
          :loading="loading"
          :error="error"
          height="400px"
        />
      </div>
      <div class="comparison-stats">
        <div class="stat-item">
          <span class="label">对比项:</span>
          <span class="value">{{ comparisonType }}</span>
        </div>
        <div class="stat-item">
          <span class="label">参与数量:</span>
          <span class="value">{{ participantCount }}</span>
        </div>
        <div class="stat-item">
          <span class="label">平均水平:</span>
          <span class="value">{{ averageLevel }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../common/BaseECharts.vue';
import { computed, defineProps } from 'vue';

export default {
  name: 'GradeComparison',
  components: {
    BaseECharts
  },
  props: {
    data: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    },
    comparisonType: {
      type: String,
      default: '班级'
    }
  },
  setup(props) {
    // 计算参与数量
    const participantCount = computed(() => {
      if (!props.data) return 0;
      if (props.comparisonType === '班级' && props.data.class_averages) {
        return Object.keys(props.data.class_averages).length;
      }
      if (props.comparisonType === '学科' && props.data.subject_averages) {
        return Object.keys(props.data.subject_averages).length;
      }
      return 0;
    });
    
    // 计算平均水平
    const averageLevel = computed(() => {
      if (!props.data) return 'N/A';
      if (props.data.overall_average) {
        return props.data.overall_average.toFixed(2);
      }
      return 'N/A';
    });
    
    // 计算图表类型
    const chartType = computed(() => {
      return props.comparisonType === '班级' ? 'radar' : 'bar';
    });
    
    // 计算图表数据
    const chartData = computed(() => {
      return props.data || {};
    });
    
    // 计算图表配置
    const chartOptions = computed(() => {
      if (!props.data) return {};
      
      if (props.comparisonType === '班级' && props.data.class_averages) {
        const classes = Object.keys(props.data.class_averages);
        const subjects = props.data.subject_averages ? Object.keys(props.data.subject_averages) : [];
        
        const series = subjects.map((subject) => {
          const data = classes.map(className => {
            return props.data.class_averages[className][subject] || 0;
          });
          
          return {
            name: subject,
            type: 'radar',
            data: [{
              value: data,
              name: subject
            }]
          };
        });
        
        return {
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
        };
      } else if (props.comparisonType === '学科' && props.data.subject_averages) {
        const subjects = Object.keys(props.data.subject_averages);
        const averages = subjects.map(subject => props.data.subject_averages[subject]);
        
        return {
          title: {
            text: '学科平均成绩对比',
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
            name: '平均分',
            min: 0,
            max: 100
          },
          series: [{
            data: averages,
            type: 'bar',
            itemStyle: {
              color: '#5470c6'
            }
          }]
        };
      }
      
      return {};
    });
    
    return {
      participantCount,
      averageLevel,
      chartType,
      chartData,
      chartOptions,
      comparisonType: props.comparisonType
    };
  }
};
</script>

<style scoped>
.grade-comparison {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
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

.chart-container {
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  height: 400px;
}

.comparison-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.stat-item .label {
  color: #666;
}

.stat-item .value {
  font-weight: bold;
  color: #333;
}

@media (max-width: 768px) {
  .comparison-stats {
    grid-template-columns: 1fr;
  }
}
</style>