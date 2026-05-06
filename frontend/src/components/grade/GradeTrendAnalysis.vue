<template>
  <div class="grade-trend-analysis">
    <div class="section-header">
      <h3>成绩趋势分析</h3>
      <div class="subject-selector" v-if="availableSubjects.length > 0">
        <label class="selector-label">选择科目:</label>
        <select 
          v-model="selectedSubject" 
          @change="handleSubjectChange"
          class="filter-select"
        >
          <option value="all">全科综合分析</option>
          <option v-for="subject in availableSubjects" :key="subject" :value="subject">
            {{ subject }}
          </option>
        </select>
      </div>
    </div>
    
    <div v-if="data" class="analysis-content">
      <div class="analysis-type-badge" v-if="analysisType">
        {{ analysisType }}
      </div>
      
      <div class="chart-container">
        <BaseECharts
          chart-type="line"
          :data="chartData"
          :options="chartOptions"
          :loading="loading"
          :error="error"
          height="400px"
        />
      </div>
      
      <div class="trend-stats">
        <div class="stat-item">
          <span class="label">最近成绩:</span>
          <span class="value">{{ latestScore }}</span>
        </div>
        <div class="stat-item">
          <span class="label">平均成绩:</span>
          <span class="value">{{ averageScore }}</span>
        </div>
        <div class="stat-item">
          <span class="label">趋势:</span>
          <span class="value" :class="trendClass">{{ trendText }}</span>
        </div>
      </div>
    </div>
    
    <div v-else-if="loading" class="loading">
      <i class="fa fa-spinner fa-spin"></i>
      <span>加载中...</span>
    </div>
    
    <div v-else-if="error" class="error">
      <i class="fa fa-exclamation-circle"></i>
      <span>{{ error }}</span>
    </div>
    
    <div v-else class="empty">
      <i class="fa fa-bar-chart"></i>
      <span>暂无成绩数据</span>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../common/BaseECharts.vue';
import { computed, defineProps, defineEmits, ref, watch } from 'vue';

export default {
  name: 'GradeTrendAnalysis',
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
    availableSubjects: {
      type: Array,
      default: () => []
    },
    modelValue: {
      type: String,
      default: 'all'
    }
  },
  emits: ['update:modelValue', 'subject-change'],
  setup(props, { emit }) {
    const selectedSubject = ref(props.modelValue || 'all');
    
    watch(() => props.modelValue, (newVal) => {
      selectedSubject.value = newVal || 'all';
    });
    
    const handleSubjectChange = () => {
      emit('update:modelValue', selectedSubject.value);
      emit('subject-change', selectedSubject.value);
    };
    
    const getYAxisMax = (subject, averages) => {
      const highScoreSubjects = ['语文', '数学', '英语'];
      if (highScoreSubjects.includes(subject)) {
        return 150;
      }
      if (subject === 'all') {
        const maxScore = Math.max(...averages, 0);
        if (maxScore > 100) {
          return 150;
        }
        return Math.min(Math.max(maxScore * 1.1, 100), 100);
      }
      const maxScore = Math.max(...averages, 0);
      return Math.min(Math.max(maxScore * 1.1, 100), 100);
    };
    
    const analysisType = computed(() => {
      if (!props.data) return '';
      return props.data.analysis_type || (selectedSubject.value === 'all' ? '全科分析' : '单科分析');
    });
    
    const latestScore = computed(() => {
      if (!props.data || !props.data.exam_trend) return 'N/A';
      const averages = props.data.exam_trend.averages;
      if (!averages || averages.length === 0) return 'N/A';
      return averages[averages.length - 1].toFixed(2);
    });
    
    const averageScore = computed(() => {
      if (!props.data || !props.data.exam_trend) return 'N/A';
      const averages = props.data.exam_trend.averages;
      if (!averages || averages.length === 0) return 'N/A';
      const total = averages.reduce((sum, avg) => sum + avg, 0);
      return (total / averages.length).toFixed(2);
    });
    
    const trendClass = computed(() => {
      if (!props.data || !props.data.exam_trend) return '';
      const averages = props.data.exam_trend.averages;
      if (!averages || averages.length < 2) return '';
      
      const firstAvg = averages[0];
      const lastAvg = averages[averages.length - 1];
      
      if (lastAvg > firstAvg) return 'positive';
      if (lastAvg < firstAvg) return 'negative';
      return '';
    });
    
    const trendText = computed(() => {
      if (!props.data || !props.data.exam_trend) return '无数据';
      const averages = props.data.exam_trend.averages;
      if (!averages || averages.length < 2) return '数据不足';
      
      const firstAvg = averages[0];
      const lastAvg = averages[averages.length - 1];
      
      if (lastAvg > firstAvg) return '上升';
      if (lastAvg < firstAvg) return '下降';
      return '稳定';
    });
    
    const chartData = computed(() => {
      if (!props.data) return {};
      if (!props.data.exam_trend) return {};
      if (!props.data.exam_trend.exam_names || !props.data.exam_trend.averages) return {};
      if (props.data.exam_trend.exam_names.length !== props.data.exam_trend.averages.length) {
        console.warn('Exam names and averages length mismatch');
        return {};
      }
      return props.data;
    });
    
    const chartOptions = computed(() => {
      if (!props.data || !props.data.exam_trend) return {};
      
      const examNames = props.data.exam_trend.exam_names || [];
      const averages = props.data.exam_trend.averages || [];
      const selectedSubj = selectedSubject.value;
      
      let seriesData = [];
      let legendData = [];
      
      if (selectedSubj === 'all') {
        legendData = ['平均分数'];
        seriesData = [{
          name: '平均分数',
          type: 'line',
          data: averages,
          smooth: true,
          lineStyle: {
            width: 3
          },
          itemStyle: {
            color: '#5470c6'
          }
        }];
      } else {
        legendData = [selectedSubj];
        seriesData = [{
          name: selectedSubj,
          type: 'line',
          data: averages,
          smooth: true,
          lineStyle: {
            width: 3
          },
          itemStyle: {
            color: '#91cc75'
          }
        }];
      }
      
      return {
        title: {
          text: selectedSubj === 'all' ? '全科成绩趋势' : `${selectedSubj}成绩趋势`,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
            if (!params || params.length === 0) return '';
            const param = params[0];
            return `<div style="padding: 8px;">
              <div style="font-weight: bold; margin-bottom: 8px;">${param.name}</div>
              <div>
                <span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:${param.color};"></span>
                <span>${param.seriesName}: <strong>${param.value}</strong>分</span>
              </div>
            </div>`;
          }
        },
        legend: {
          data: legendData,
          bottom: 10
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: examNames,
          axisLabel: {
            rotate: 30,
            fontSize: 12
          }
        },
        yAxis: {
          type: 'value',
          name: '分数',
          min: 0,
          max: getYAxisMax(selectedSubj, averages),
          axisLabel: {
            formatter: '{value}分'
          }
        },
        series: seriesData
      };
    });
    
    return {
      selectedSubject,
      analysisType,
      latestScore,
      averageScore,
      trendClass,
      trendText,
      chartData,
      chartOptions,
      handleSubjectChange
    };
  }
};
</script>

<style scoped>
.grade-trend-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.subject-selector {
  display: flex;
  align-items: center;
  gap: 10px;
}

.selector-label {
  font-size: 14px;
  color: #666;
}

.filter-select {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  background: #fff;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.filter-select:hover {
  border-color: #409eff;
}

.filter-select:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.analysis-type-badge {
  display: inline-block;
  padding: 4px 12px;
  background: #e8f4fd;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 15px;
}

.analysis-content {
  min-height: 450px;
}

.loading, .error, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;
}

.loading i, .error i, .empty i {
  font-size: 32px;
  margin-bottom: 10px;
}

.loading {
  color: #409eff;
}

.error {
  color: #f56c6c;
  background: #fef0f0;
  border-radius: 4px;
}

.chart-container {
  margin-bottom: 20px;
}

.trend-stats {
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

.stat-item .value.positive {
  color: #67c23a;
}

.stat-item .value.negative {
  color: #f56c6c;
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .trend-stats {
    grid-template-columns: 1fr;
  }
}
</style>