<template>
  <div class="log-container">
    <div class="log-header">
      <h3 class="log-title">信息增益计算日志</h3>
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索日志..." 
          class="search-input"
        />
        <button class="search-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.35-4.35"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <div class="log-body">
      <div v-if="loading" class="loading-state">
        <svg class="loading-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="logs.length === 0" class="empty-state">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="16" y1="13" x2="8" y2="13"></line>
          <line x1="16" y1="17" x2="8" y2="17"></line>
          <polyline points="10 9 9 9 8 9"></polyline>
        </svg>
        <p>暂无日志记录</p>
      </div>
      
      <div v-else class="log-list">
        <div 
          v-for="(log, index) in filteredLogs" 
          :key="index" 
          class="log-item"
          @click="toggleLogDetail(log)"
        >
          <div class="log-header-row">
            <span class="log-time">{{ formatTime(log.timestamp) }}</span>
            <span class="log-type">{{ log.analysis_type }}</span>
            <span class="log-status" :class="log.result">
              {{ log.result === 'success' ? '成功' : '失败' }}
            </span>
          </div>
          
          <div v-if="expandedLog === log" class="log-detail">
            <div class="detail-section">
              <h4>参数配置</h4>
              <pre class="code-block">{{ JSON.stringify(log.params, null, 2) }}</pre>
            </div>
            
            <div v-if="log.calculation_steps && log.calculation_steps.length > 0" class="detail-section">
              <h4>计算步骤</h4>
              <div class="steps-list">
                <div v-for="(step, stepIndex) in log.calculation_steps" :key="stepIndex" class="step-item">
                  <div class="step-header">
                    <span class="step-number">{{ stepIndex + 1 }}</span>
                    <span class="step-name">{{ step.step }}</span>
                  </div>
                  <div class="step-details">
                    <div class="detail-row">
                      <span class="detail-label">特征名称:</span>
                      <span class="detail-value">{{ step.feature_name }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">分裂前熵值:</span>
                      <span class="detail-value">{{ step.entropy_before?.toFixed(4) }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">分裂后熵值:</span>
                      <span class="detail-value">{{ step.entropy_after?.toFixed(4) }}</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">信息增益:</span>
                      <span class="detail-value highlight">{{ step.info_gain?.toFixed(4) }}</span>
                    </div>
                    <div v-if="step.gain_ratio" class="detail-row">
                      <span class="detail-label">信息增益比:</span>
                      <span class="detail-value highlight">{{ step.gain_ratio?.toFixed(4) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="log.feature_ranking && log.feature_ranking.length > 0" class="detail-section">
              <h4>特征增益排序</h4>
              <div class="ranking-list">
                <div v-for="(feature, rankIndex) in log.feature_ranking" :key="rankIndex" class="ranking-item">
                  <span class="rank-number">{{ rankIndex + 1 }}</span>
                  <div class="rank-bar-container">
                    <div 
                      class="rank-bar" 
                      :style="{ width: `${(feature.gain / log.feature_ranking[0].gain) * 100}%` }"
                    ></div>
                  </div>
                  <span class="rank-name">{{ feature.attribute_name }}</span>
                  <span class="rank-value">{{ feature.gain.toFixed(4) }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="log-expand">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="14" 
              height="14" 
              viewBox="0 0 24 24" 
              fill="none" 
              stroke="currentColor" 
              stroke-width="2" 
              stroke-linecap="round" 
              stroke-linejoin="round"
              :class="{ 'rotated': expandedLog === log }"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
        </div>
        
        <div v-if="filteredLogs.length === 0" class="empty-filter">
          <p>未找到匹配的日志</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { decisionTreeService } from '@/services/gradeService';
import type { DecisionTreeLog } from '@/services/gradeService';

interface LogEntry extends DecisionTreeLog {}

interface CalculationStep {
  step: string;
  node_id: number;
  feature_id: number;
  feature_name: string;
  entropy_before: number;
  entropy_after: number;
  info_gain: number;
  gain_ratio?: number;
  sample_count: number;
  class_distribution: Record<string, number>;
}

interface FeatureRanking {
  attribute: number;
  attribute_name: string;
  gain: number;
  info_gain: number;
}

interface LogEntryInternal {
  timestamp: string;
  analysis_id: string;
  user_id: string;
  analysis_type: string;
  step: string;
  params: Record<string, unknown>;
  calculation_steps: CalculationStep[];
  feature_ranking: FeatureRanking[];
  result: string;
  operator: string;
}

const logs = ref<LogEntry[]>([]);
const loading = ref(false);
const searchQuery = ref('');
const expandedLog = ref<LogEntry | null>(null);

const filteredLogs = computed(() => {
  if (!searchQuery.value) return logs.value;
  
  const query = searchQuery.value.toLowerCase();
  return logs.value.filter(log => 
    log.analysis_id.toLowerCase().includes(query) ||
    log.user_id.toLowerCase().includes(query) ||
    log.result.toLowerCase().includes(query) ||
    JSON.stringify(log.params).toLowerCase().includes(query)
  );
});

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const toggleLogDetail = (log: LogEntry) => {
  expandedLog.value = expandedLog.value === log ? null : log;
};

const loadLogs = async () => {
  loading.value = true;
  try {
    const response = await decisionTreeService.getDecisionTreeLogs();
    logs.value = response.logs || [];
  } catch (error) {
    console.error('加载日志失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadLogs();
});
</script>

<style scoped>
.log-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.log-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.search-bar {
  display: flex;
  align-items: center;
  background: #f5f5f5;
  border-radius: 6px;
  padding: 6px 12px;
}

.search-input {
  border: none;
  background: none;
  outline: none;
  font-size: 13px;
  width: 150px;
}

.search-btn {
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
}

.log-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.loading-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
}

.loading-icon {
  animation: spin 1s linear infinite;
  color: #1890ff;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.empty-state svg {
  margin-bottom: 12px;
}

.empty-state p, .loading-state p {
  margin: 0;
  font-size: 14px;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log-item {
  background: #fafafa;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.log-item:hover {
  background: #f0f0f0;
}

.log-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-time {
  font-size: 12px;
  color: #666;
}

.log-type {
  font-size: 12px;
  color: #1890ff;
  font-weight: 500;
}

.log-status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.log-status.success {
  background: #f6ffed;
  color: #52c41a;
}

.log-status.failed {
  background: #fff2f0;
  color: #ff4d4f;
}

.log-detail {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e0e0e0;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h4 {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin: 0 0 10px 0;
}

.code-block {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 6px;
  font-size: 12px;
  overflow-x: auto;
  color: #333;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-item {
  background: #fff;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #e8e8e8;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.step-number {
  background: #1890ff;
  color: #fff;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.step-name {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

.step-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.detail-label {
  color: #666;
}

.detail-value {
  color: #333;
  font-weight: 500;
}

.detail-value.highlight {
  color: #1890ff;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rank-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: #666;
}

.rank-bar-container {
  flex: 1;
  height: 12px;
  background: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
}

.rank-bar {
  height: 100%;
  background: linear-gradient(90deg, #1890ff, #40a9ff);
  border-radius: 6px;
  transition: width 0.3s;
}

.rank-name {
  min-width: 80px;
  font-size: 12px;
  color: #333;
}

.rank-value {
  font-size: 12px;
  color: #1890ff;
  font-weight: 500;
  min-width: 60px;
  text-align: right;
}

.log-expand {
  margin-top: 8px;
  display: flex;
  justify-content: center;
  color: #999;
  transition: transform 0.2s;
}

.log-expand svg.rotated {
  transform: rotate(180deg);
}

.empty-filter {
  text-align: center;
  padding: 20px;
  color: #999;
}

.empty-filter p {
  margin: 0;
  font-size: 14px;
}
</style>