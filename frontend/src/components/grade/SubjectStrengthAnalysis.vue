<template>
  <div class="subject-strength-analysis">
    <h3>学科强弱分析</h3>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="data" class="analysis-content">
      <div class="strengths-weaknesses">
        <div class="strengths">
          <h4>学科强项</h4>
          <ul v-if="data.strengths && data.strengths.length > 0">
            <li v-for="(item, index) in data.strengths" :key="index" class="strength-item">
              <div class="subject-name">{{ item.subject }}</div>
              <div class="score-info">
                <span class="personal-score">{{ item.avg_score }}</span>
                <span class="class-score">(班级: {{ item.class_avg }})</span>
                <span class="diff positive">+{{ item.diff }}</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress" 
                  :style="{ width: Math.min((item.avg_score / 100) * 100, 100) + '%' }"
                ></div>
              </div>
            </li>
          </ul>
          <p v-else class="no-data">暂无明显强项</p>
        </div>
        
        <div class="weaknesses">
          <h4>学科弱项</h4>
          <ul v-if="data.weaknesses && data.weaknesses.length > 0">
            <li v-for="(item, index) in data.weaknesses" :key="index" class="weakness-item">
              <div class="subject-name">{{ item.subject }}</div>
              <div class="score-info">
                <span class="personal-score">{{ item.avg_score }}</span>
                <span class="class-score">(班级: {{ item.class_avg }})</span>
                <span class="diff negative">{{ item.diff }}</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress" 
                  :style="{ width: Math.min((item.avg_score / 100) * 100, 100) + '%' }"
                ></div>
              </div>
            </li>
          </ul>
          <p v-else class="no-data">暂无明显弱项</p>
        </div>
      </div>
      
      <div class="overall-evaluation">
        <h4>整体评估</h4>
        <div class="evaluation-content">
          <div class="evaluation-item">
            <span class="label">个人平均:</span>
            <span class="value">{{ data.overall.personal_avg }}</span>
          </div>
          <div class="evaluation-item">
            <span class="label">班级平均:</span>
            <span class="value">{{ data.overall.class_avg }}</span>
          </div>
          <div class="evaluation-item">
            <span class="label">差异:</span>
            <span class="value" :class="data.overall.diff >= 0 ? 'positive' : 'negative'">
              {{ data.overall.diff >= 0 ? '+' + data.overall.diff : data.overall.diff }}
            </span>
          </div>
          <div class="evaluation-item">
            <span class="label">评估:</span>
            <span class="value evaluation-text">{{ data.overall.evaluation }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineProps } from 'vue'

export default {
  name: 'SubjectStrengthAnalysis',
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
  }
}
</script>

<style scoped>
.subject-strength-analysis {
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

.strengths-weaknesses {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.strengths,
.weaknesses {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.strengths h4,
.weaknesses h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.strength-item,
.weakness-item {
  margin-bottom: 15px;
  padding: 10px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.subject-name {
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

.score-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  font-size: 14px;
}

.personal-score {
  font-weight: bold;
  color: #409eff;
}

.class-score {
  color: #999;
}

.diff {
  font-weight: bold;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
}

.diff.positive {
  color: #67c23a;
  background: #f0f9eb;
}

.diff.negative {
  color: #f56c6c;
  background: #fef0f0;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background: #409eff;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.no-data {
  text-align: center;
  color: #999;
  padding: 20px;
}

.overall-evaluation {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #eee;
}

.overall-evaluation h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.evaluation-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.evaluation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.evaluation-item .label {
  color: #666;
}

.evaluation-item .value {
  font-weight: bold;
  color: #333;
}

.evaluation-item .value.positive {
  color: #67c23a;
}

.evaluation-item .value.negative {
  color: #f56c6c;
}

.evaluation-text {
  color: #409eff !important;
}

@media (max-width: 768px) {
  .strengths-weaknesses {
    grid-template-columns: 1fr;
  }
  
  .evaluation-content {
    grid-template-columns: 1fr;
  }
}
</style>