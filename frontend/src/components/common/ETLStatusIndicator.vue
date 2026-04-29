<template>
  <div class="etl-status-indicator">
    <div class="etl-header">
      <div class="etl-icon">⚙️</div>
      <div class="etl-title">数据处理进度</div>
      <div v-if="status === 'running'" class="etl-refresh">
        <span class="refresh-dot"></span>
      </div>
    </div>
    
    <!-- 总体进度条 -->
    <div class="overall-progress">
      <div class="progress-bar">
        <div 
          class="progress-fill" 
          :class="status"
          :style="{ width: progress + '%' }"
        ></div>
      </div>
      <div class="progress-info">
        <span class="progress-percentage">{{ progress }}%</span>
        <span class="progress-status">{{ statusText }}</span>
      </div>
    </div>
    
    <!-- 步骤详情 -->
    <div class="steps-container">
      <div 
        v-for="(step, key) in steps" 
        :key="key"
        class="step-item"
        :class="step.status"
      >
        <div class="step-icon">
          <span v-if="step.status === 'completed'">✓</span>
          <span v-else-if="step.status === 'running'">◐</span>
          <span v-else-if="step.status === 'failed'">✗</span>
          <span v-else>○</span>
        </div>
        <div class="step-content">
          <div class="step-header">
            <span class="step-name">{{ step.step_name }}</span>
            <span class="step-progress">{{ step.progress }}%</span>
          </div>
          <div class="step-message">{{ step.message }}</div>
        </div>
        <div class="step-progress-bar">
          <div 
            class="step-progress-fill"
            :style="{ width: step.progress + '%' }"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- 错误信息 -->
    <div v-if="errorMessage" class="error-section">
      <div class="error-icon">⚠️</div>
      <div class="error-content">
        <div class="error-title">处理失败</div>
        <div class="error-text">{{ errorMessage }}</div>
      </div>
    </div>
    
    <!-- 完成提示 -->
    <div v-if="status === 'completed'" class="success-section">
      <div class="success-icon">🎉</div>
      <div class="success-text">数据处理完成！</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { gradeService, type ETLStatusResponse } from '../../services/gradeService';

const props = defineProps<{
  analysisId?: string;
  autoRefresh?: boolean;
}>();

const emit = defineEmits<{
  (e: 'complete'): void;
  (e: 'error', error: string): void;
}>();

const status = ref<'pending' | 'running' | 'completed' | 'failed'>('pending');
const progress = ref(0);
const currentStep = ref('');
const errorMessage = ref('');
const steps = ref<Record<string, any>>({
  extract: { step_name: '数据提取', status: 'pending' as const, progress: 0, message: '等待开始' },
  transform: { step_name: '数据转换', status: 'pending' as const, progress: 0, message: '等待开始' },
  load: { step_name: '数据加载', status: 'pending' as const, progress: 0, message: '等待开始' },
  mining: { step_name: '数据挖掘', status: 'pending' as const, progress: 0, message: '等待开始' }
});

let refreshInterval: number | null = null;

const statusText = computed(() => {
  switch (status.value) {
    case 'pending': return '等待开始';
    case 'running': return '处理中...';
    case 'completed': return '已完成';
    case 'failed': return '失败';
    default: return '';
  }
});

const fetchStatus = async () => {
  if (!props.analysisId) return;
  
  try {
    const response = await gradeService.getETLStatus(props.analysisId);
    
    status.value = response.status;
    progress.value = response.progress;
    currentStep.value = response.current_step;
    errorMessage.value = response.error_message || '';
    steps.value = response.steps;
    
    if (status.value === 'completed') {
      stopRefresh();
      emit('complete');
    } else if (status.value === 'failed') {
      stopRefresh();
      emit('error', errorMessage.value);
    }
  } catch (e) {
    console.error('Failed to fetch ETL status:', e);
  }
};

const startRefresh = () => {
  if (refreshInterval) return;
  refreshInterval = window.setInterval(fetchStatus, 1000);
};

const stopRefresh = () => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
    refreshInterval = null;
  }
};

watch(() => props.analysisId, (newId) => {
  if (newId) {
    fetchStatus();
    if (props.autoRefresh !== false) {
      startRefresh();
    }
  }
});

onMounted(() => {
  if (props.analysisId) {
    fetchStatus();
    if (props.autoRefresh !== false) {
      startRefresh();
    }
  }
});

onUnmounted(() => {
  stopRefresh();
});
</script>

<style scoped>
.etl-status-indicator {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.etl-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.etl-icon {
  font-size: 20px;
  margin-right: 8px;
}

.etl-title {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.etl-refresh {
  display: flex;
  align-items: center;
}

.refresh-dot {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 总体进度条 */
.overall-progress {
  margin-bottom: 20px;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.progress-fill.completed {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.progress-fill.failed {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-percentage {
  font-size: 18px;
  font-weight: 600;
  color: #667eea;
}

.progress-status {
  font-size: 13px;
  color: #6b7280;
}

/* 步骤详情 */
.steps-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-item {
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #e5e7eb;
  transition: all 0.3s ease;
}

.step-item.pending {
  border-left-color: #9ca3af;
}

.step-item.running {
  border-left-color: #667eea;
  background: #f0f5ff;
}

.step-item.completed {
  border-left-color: #10b981;
  background: #f0fdf4;
}

.step-item.failed {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.step-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
  margin-right: 10px;
  float: left;
}

.step-item.pending .step-icon {
  background: #e5e7eb;
  color: #6b7280;
}

.step-item.running .step-icon {
  background: #667eea;
  color: white;
  animation: spin 1s linear infinite;
}

.step-item.completed .step-icon {
  background: #10b981;
  color: white;
}

.step-item.failed .step-icon {
  background: #ef4444;
  color: white;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.step-content {
  overflow: hidden;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.step-name {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.step-progress {
  font-size: 12px;
  font-weight: 600;
  color: #667eea;
}

.step-message {
  font-size: 12px;
  color: #6b7280;
}

.step-progress-bar {
  margin-top: 8px;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.step-progress-fill {
  height: 100%;
  background: #667eea;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.step-item.completed .step-progress-fill {
  background: #10b981;
}

.step-item.failed .step-progress-fill {
  background: #ef4444;
}

/* 错误信息 */
.error-section {
  margin-top: 16px;
  padding: 12px;
  background: #fef2f2;
  border-radius: 8px;
  display: flex;
  align-items: flex-start;
}

.error-icon {
  font-size: 20px;
  margin-right: 10px;
}

.error-content {
  flex: 1;
}

.error-title {
  font-size: 14px;
  font-weight: 600;
  color: #dc2626;
  margin-bottom: 4px;
}

.error-text {
  font-size: 13px;
  color: #b91c1c;
}

/* 完成提示 */
.success-section {
  margin-top: 16px;
  padding: 16px;
  background: #f0fdf4;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-icon {
  font-size: 24px;
  margin-right: 10px;
}

.success-text {
  font-size: 16px;
  font-weight: 600;
  color: #059669;
}

/* 响应式 */
@media (max-width: 768px) {
  .etl-status-indicator {
    padding: 16px;
  }
  
  .step-item {
    padding: 10px;
  }
  
  .step-icon {
    width: 20px;
    height: 20px;
    font-size: 10px;
  }
}
</style>