<template>
  <div class="knowledge-discovery-list">
    <div class="section-header">
      <div class="header-icon">💡</div>
      <div class="header-content">
        <h3 class="section-title">挖掘发现</h3>
        <p class="section-subtitle">Knowledge Discovery</p>
      </div>
      <div class="header-actions">
        <div class="academic-badge">
          <span>C4.5算法</span>
        </div>
        <button 
          v-if="!isLoading" 
          class="refresh-btn" 
          @click="refreshData"
          :disabled="isLoading"
        >
          <span>{{ isLoading ? '刷新中...' : '↻' }}</span>
        </button>
      </div>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p class="loading-text">正在获取挖掘发现数据...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p class="error-text">{{ error }}</p>
      <button class="retry-btn" @click="refreshData">重试</button>
    </div>
    
    <!-- 数据列表 -->
    <div v-else class="discovery-list">
      <div 
        v-for="(discovery, index) in discoveries" 
        :key="index"
        class="discovery-card"
        :class="{ 'highlight': discovery.isHighlight }"
      >
        <div class="discovery-header">
          <div class="discovery-number">
            <span class="number-icon">🔍</span>
            <span class="number-text">算法发现 {{ String(index + 1).padStart(2, '0') }}</span>
          </div>
          <div v-if="discovery.confidence" class="confidence-badge">
            <span>置信度: {{ discovery.confidence }}%</span>
          </div>
        </div>
        
        <div class="discovery-content">
          <div class="discovery-rule">
            <span class="rule-prefix">如果</span>
            <div class="conditions">
              <span 
                v-for="(condition, condIndex) in discovery.conditions" 
                :key="condIndex"
                class="condition-item"
              >
                <span class="condition-feature">【{{ condition.feature }}】</span>
                <span class="condition-operator">{{ condition.operator }}</span>
                <span class="condition-value">"{{ condition.value }}"</span>
                <span v-if="condIndex < discovery.conditions.length - 1" class="condition-conjunction">且</span>
              </span>
            </div>
            <span class="rule-suffix">，则</span>
          </div>
          
          <div class="discovery-result">
            <span class="result-target">【{{ discovery.result.target }}】</span>
            <span class="result-effect">{{ discovery.result.effect }}</span>
            <span v-if="discovery.result.change" class="result-change">
              {{ discovery.result.change > 0 ? '上升' : '下降' }} {{ Math.abs(discovery.result.change) }}%
            </span>
          </div>
        </div>
        
        <div v-if="discovery.insight" class="discovery-insight">
          <span class="insight-icon">💡</span>
          <span class="insight-text">{{ discovery.insight }}</span>
        </div>
        
        <div v-if="discovery.statisticalSignificance" class="significance-info">
          <span class="significance-label">统计显著性:</span>
          <span class="significance-value">{{ discovery.statisticalSignificance }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="!isLoading && !error && discoveries.length === 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <p class="empty-text">暂无挖掘发现数据</p>
      <p class="empty-hint">请先进行成绩分析以获取挖掘发现</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { gradeService } from '../../services/gradeService';

export interface DiscoveryCondition {
  feature: string;
  operator: string;
  value: string | number;
}

export interface DiscoveryResult {
  target: string;
  effect: string;
  change?: number;
}

export interface KnowledgeDiscovery {
  conditions: DiscoveryCondition[];
  result: DiscoveryResult;
  insight?: string;
  confidence?: number;
  isHighlight?: boolean;
  statisticalSignificance?: string;
}

const props = defineProps<{
  classId?: string;
}>();

const discoveries = ref<KnowledgeDiscovery[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

const loadData = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const params: Record<string, string> = {};
    if (props.classId) {
      params.class_id = props.classId;
    }
    
    const response = await gradeService.getRealtimeDiscoveries(props.classId);
    discoveries.value = response.discoveries || [];
  } catch (e) {
    error.value = '获取挖掘发现数据失败，请稍后重试';
    console.error('Failed to load discoveries:', e);
  } finally {
    isLoading.value = false;
  }
};

const refreshData = () => {
  loadData();
};

onMounted(() => {
  loadData();
});

watch(() => props.classId, () => {
  loadData();
});
</script>

<style scoped>
.knowledge-discovery-list {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.header-icon {
  font-size: 28px;
  margin-right: 12px;
}

.header-content {
  flex: 1;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.section-subtitle {
  margin: 4px 0 0 0;
  font-size: 12px;
  opacity: 0.8;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.academic-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.refresh-btn {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  background: #fef2f2;
}

.error-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.error-text {
  margin: 0 0 12px 0;
  color: #dc2626;
  font-size: 14px;
}

.retry-btn {
  padding: 8px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.discovery-list {
  padding: 16px;
}

.discovery-card {
  background: #fafafa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.discovery-card:hover {
  background: #f5f5f5;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.discovery-card.highlight {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.discovery-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.discovery-number {
  display: flex;
  align-items: center;
  color: #667eea;
  font-weight: 600;
  font-size: 14px;
}

.number-icon {
  margin-right: 6px;
}

.confidence-badge {
  background: #dcfce7;
  color: #16a34a;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.discovery-content {
  font-size: 14px;
  line-height: 1.8;
}

.discovery-rule {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  color: #374151;
}

.rule-prefix {
  font-weight: 500;
  margin-right: 4px;
}

.conditions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.condition-item {
  display: flex;
  align-items: center;
}

.condition-feature {
  background: #e0e7ff;
  color: #4338ca;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.condition-operator {
  margin: 0 6px;
  color: #6b7280;
}

.condition-value {
  color: #dc2626;
  font-weight: 500;
}

.condition-conjunction {
  margin: 0 8px;
  color: #6b7280;
  font-weight: 500;
}

.rule-suffix {
  margin-left: 4px;
}

.discovery-result {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #e5e7eb;
}

.result-target {
  background: #d1fae5;
  color: #059669;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.result-effect {
  margin-left: 8px;
  color: #374151;
}

.result-change {
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.result-change:contains('上升') {
  background: #dcfce7;
  color: #16a34a;
}

.result-change:contains('下降') {
  background: #fee2e2;
  color: #dc2626;
}

.discovery-insight {
  margin-top: 12px;
  padding: 10px 12px;
  background: #fef9c3;
  border-radius: 6px;
  display: flex;
  align-items: flex-start;
}

.insight-icon {
  font-size: 16px;
  margin-right: 8px;
}

.insight-text {
  font-size: 13px;
  color: #92400e;
  line-height: 1.5;
}

.significance-info {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
}

.significance-label {
  margin-right: 6px;
}

.significance-value {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #6b7280;
}

.empty-hint {
  margin: 0;
  font-size: 14px;
  color: #9ca3af;
}

@media (max-width: 768px) {
  .section-header {
    padding: 16px;
  }
  
  .section-title {
    font-size: 16px;
  }
  
  .discovery-card {
    padding: 12px;
  }
  
  .discovery-rule {
    flex-direction: column;
  }
  
  .conditions {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .condition-item {
    margin-bottom: 6px;
  }
  
  .condition-conjunction {
    display: none;
  }
}

@media (max-width: 480px) {
  .discovery-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .confidence-badge {
    margin-top: 8px;
  }
  
  .discovery-content {
    font-size: 13px;
  }
}
</style>