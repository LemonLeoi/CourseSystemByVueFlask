<template>
  <div class="grade-trend-analysis">
    <h3>成绩趋势分析</h3>
    <div v-if="data" class="analysis-content">
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
  </div>
</template>

<script>
import BaseECharts from '../common/BaseECharts.vue';
import { computed, defineProps } from 'vue';

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
    }
  },
  setup(props) {
    // 计算最近成绩
    const latestScore = computed(() => {
      if (!props.data || !props.data.exam_grades) return 'N/A';
      const examTypes = Object.keys(props.data.exam_grades);
      if (examTypes.length === 0) return 'N/A';
      
      // 假设考试类型是按时间顺序排列的，取最后一个
      const latestExam = examTypes[examTypes.length - 1];
      const subjects = Object.keys(props.data.exam_grades[latestExam]);
      if (subjects.length === 0) return 'N/A';
      
      // 计算最新考试的平均成绩
      let total = 0;
      let count = 0;
      for (const subject in props.data.exam_grades[latestExam]) {
        total += props.data.exam_grades[latestExam][subject][0];
        count++;
      }
      return (total / count).toFixed(2);
    });
    
    // 计算平均成绩
    const averageScore = computed(() => {
      if (!props.data || !props.data.subject_averages) return 'N/A';
      const averages = Object.values(props.data.subject_averages);
      if (averages.length === 0) return 'N/A';
      const total = averages.reduce((sum, avg) => sum + avg, 0);
      return (total / averages.length).toFixed(2);
    });
    
    // 计算趋势
    const trendClass = computed(() => {
      if (!props.data || !props.data.exam_grades) return '';
      const examTypes = Object.keys(props.data.exam_grades);
      if (examTypes.length < 2) return '';
      
      // 计算第一个和最后一个考试的平均成绩
      const firstExam = examTypes[0];
      const lastExam = examTypes[examTypes.length - 1];
      
      let firstTotal = 0;
      let firstCount = 0;
      for (const subject in props.data.exam_grades[firstExam]) {
        firstTotal += props.data.exam_grades[firstExam][subject][0];
        firstCount++;
      }
      
      let lastTotal = 0;
      let lastCount = 0;
      for (const subject in props.data.exam_grades[lastExam]) {
        lastTotal += props.data.exam_grades[lastExam][subject][0];
        lastCount++;
      }
      
      const firstAvg = firstCount > 0 ? firstTotal / firstCount : 0;
      const lastAvg = lastCount > 0 ? lastTotal / lastCount : 0;
      
      if (lastAvg > firstAvg) return 'positive';
      if (lastAvg < firstAvg) return 'negative';
      return '';
    });
    
    const trendText = computed(() => {
      if (!props.data || !props.data.exam_grades) return '无数据';
      const examTypes = Object.keys(props.data.exam_grades);
      if (examTypes.length < 2) return '数据不足';
      
      const firstExam = examTypes[0];
      const lastExam = examTypes[examTypes.length - 1];
      
      let firstTotal = 0;
      let firstCount = 0;
      for (const subject in props.data.exam_grades[firstExam]) {
        firstTotal += props.data.exam_grades[firstExam][subject][0];
        firstCount++;
      }
      
      let lastTotal = 0;
      let lastCount = 0;
      for (const subject in props.data.exam_grades[lastExam]) {
        lastTotal += props.data.exam_grades[lastExam][subject][0];
        lastCount++;
      }
      
      const firstAvg = firstCount > 0 ? firstTotal / firstCount : 0;
      const lastAvg = lastCount > 0 ? lastTotal / lastCount : 0;
      
      if (lastAvg > firstAvg) return '上升';
      if (lastAvg < firstAvg) return '下降';
      return '稳定';
    });
    
    // 计算图表数据
    const chartData = computed(() => {
      return props.data || {};
    });
    
    // 计算图表配置
    const chartOptions = computed(() => {
      if (!props.data || !props.data.exam_grades) return {};
      
      const examTypes = Object.keys(props.data.exam_grades);
      const subjects = new Set();
      
      // 收集所有学科
      examTypes.forEach(exam => {
        Object.keys(props.data.exam_grades[exam]).forEach(subject => {
          subjects.add(subject);
        });
      });
      
      const subjectList = Array.from(subjects);
      
      // 准备数据
      const series = subjectList.map(subject => {
        const data = examTypes.map(exam => {
          return props.data.exam_grades[exam][subject] ? props.data.exam_grades[exam][subject][0] : 0;
        });
        
        return {
          name: subject,
          type: 'line',
          data: data,
          smooth: true
        };
      });
      
      return {
        title: {
          text: '成绩趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: subjectList,
          bottom: 0
        },
        xAxis: {
          type: 'category',
          data: examTypes
        },
        yAxis: {
          type: 'value',
          name: '分数',
          min: 0,
          max: 100
        },
        series: series
      };
    });
    
    return {
      latestScore,
      averageScore,
      trendClass,
      trendText,
      chartData,
      chartOptions
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
  .trend-stats {
    grid-template-columns: 1fr;
  }
}
</style>