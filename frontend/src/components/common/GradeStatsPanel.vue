<template>
  <div class="grade-stats-panel" v-if="gradeDetail">
    <div class="panel-header">
      <h4>{{ gradeDetail.subject === '综合' ? '综合成绩分析' : gradeDetail.subject + '学科成绩分析' }}</h4>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-info">
          <span class="stat-label">平均分（分）</span>
          <span class="stat-value">{{ gradeDetail.average_score }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-info">
          <span class="stat-label">最高分（分）</span>
          <span class="stat-value">{{ gradeDetail.max_score }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📉</div>
        <div class="stat-info">
          <span class="stat-label">最低分（分）</span>
          <span class="stat-value">{{ gradeDetail.min_score }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📈</div>
        <div class="stat-info">
          <span class="stat-label">标准差</span>
          <span class="stat-value">{{ gradeDetail.std_deviation }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-label">及格率</span>
          <span class="stat-value">{{ gradeDetail.pass_rate }}%</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⭐</div>
        <div class="stat-info">
          <span class="stat-label">优秀率</span>
          <span class="stat-value">{{ gradeDetail.excellent_rate }}%</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <span class="stat-label">学生人数</span>
          <span class="stat-value">{{ gradeDetail.total_students }}人</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <span class="stat-label">有效成绩数</span>
          <span class="stat-value">{{ gradeDetail.total_scores }}条</span>
        </div>
      </div>
    </div>

    <div class="distribution-section">
      <div class="section-header">
        <h5>分数分布</h5>
        <div class="mode-switch">
          <button 
            @click="toggleDisplayMode"
            :class="{ active: displayMode === 'score' }"
          >
            具体分数模式
          </button>
          <button 
            @click="toggleDisplayMode"
            :class="{ active: displayMode === 'percentage' }"
          >
            得分率模式
          </button>
        </div>
      </div>
      <div class="distribution-bars">
        <div class="dist-bar" v-for="(label, index) in barLabelsArray" :key="index">
          <div class="bar-label">{{ label }}</div>
          <div class="bar-container">
            <div class="bar" :class="getBarClass(index)" :style="getBarStyle(index)"></div>
          </div>
          <div class="bar-value">{{ getDistributionValue(index) }}人</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'GradeStatsPanel',
  props: {
    gradeDetail: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const displayMode = ref('score');

    const toggleDisplayMode = () => {
      displayMode.value = displayMode.value === 'score' ? 'percentage' : 'score';
    };

    const barLabelsArray = computed(() => {
      if (!props.gradeDetail) return [];

      const thresholds = props.gradeDetail.thresholds;
      const percentageThresholds = props.gradeDetail.percentage_thresholds;

      if (displayMode.value === 'percentage') {
        const excellent = percentageThresholds?.excellent || 90;
        const good = percentageThresholds?.good || 85;
        const average = percentageThresholds?.average || 75;
        const pass = percentageThresholds?.pass || 60;

        return [
          `优秀(≥${excellent}%)`,
          `良好(${good}%-${excellent - 1}%)`,
          `中等(${average}%-${good - 1}%)`,
          `及格(${pass}%-${average - 1}%)`,
          `不及格(<${pass}%)`
        ];
      } else {
        const excellent = Math.round(thresholds?.excellent || 90);
        const good = Math.round(thresholds?.good || 80);
        const average = Math.round(thresholds?.average || 70);
        const pass = Math.round(thresholds?.pass || 60);

        return [
          `优秀(≥${excellent})`,
          `良好(${good}-${excellent - 1})`,
          `中等(${average}-${good - 1})`,
          `及格(${pass}-${average - 1})`,
          `不及格(<${pass})`
        ];
      }
    });

    const getDistributionValue = (index) => {
      if (!props.gradeDetail?.distribution) return 0;
      const dist = props.gradeDetail.distribution;
      const keys = ['excellent', 'good', 'average', 'pass', 'fail'];
      return dist[keys[index]] || 0;
    };

    const getBarStyle = (index) => {
      if (!props.gradeDetail) return { width: '0%' };
      const total = props.gradeDetail.total_students;
      const value = getDistributionValue(index);
      return { width: total > 0 ? (value / total * 100) + '%' : '0%' };
    };

    const getBarClass = (index) => {
      const classes = ['excellent', 'good', 'average', 'pass', 'fail'];
      return classes[index];
    };

    return {
      displayMode,
      toggleDisplayMode,
      barLabelsArray,
      getDistributionValue,
      getBarStyle,
      getBarClass
    };
  }
};
</script>

<style scoped>
.grade-stats-panel {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.panel-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.panel-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  padding: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
}

.stat-info {
  flex: 1;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #888;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.distribution-section {
  padding: 20px;
  border-top: 1px solid #eee;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h5 {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.mode-switch {
  display: flex;
  gap: 8px;
}

.mode-switch button {
  padding: 6px 12px;
  font-size: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mode-switch button:hover {
  border-color: #409eff;
}

.mode-switch button.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}

.distribution-bars {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.dist-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bar-label {
  width: 100px;
  font-size: 12px;
  color: #666;
  flex-shrink: 0;
}

.bar-container {
  flex: 1;
  height: 24px;
  background: #f0f0f0;
  border-radius: 12px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 12px;
  transition: width 0.3s ease;
}

.bar.excellent {
  background: linear-gradient(90deg, #52c41a, #73d13d);
}

.bar.good {
  background: linear-gradient(90deg, #1890ff, #40a9ff);
}

.bar.average {
  background: linear-gradient(90deg, #faad14, #ffc53d);
}

.bar.pass {
  background: linear-gradient(90deg, #fa8c16, #ffa940);
}

.bar.fail {
  background: linear-gradient(90deg, #f5222d, #ff4d4f);
}

.bar-value {
  width: 50px;
  font-size: 12px;
  color: #666;
  text-align: right;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    padding: 15px;
  }
  
  .stat-card {
    padding: 12px;
  }
  
  .stat-icon {
    width: 32px;
    height: 32px;
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 16px;
  }
  
  .bar-label {
    width: 80px;
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>