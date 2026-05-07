<template>
  <div class="section score-rate-config">
    <div class="section-header">
      <h4 class="section-title">
        <span class="section-icon">📊</span> 得分率设置
      </h4>
      <span class="section-hint">配置各科总分及权重，用于计算得分率</span>
    </div>

    <!-- 是否使用得分率 -->
    <div class="param-item">
      <div class="param-header">
        <label class="param-label">使用得分率评估</label>
      </div>
      <div class="radio-group">
        <label class="radio-label" :class="{ active: config.use_score_rate }">
          <input type="radio" v-model="localConfig.use_score_rate" :value="true" />
          <span class="radio-circle"></span>
          <span class="radio-text">是</span>
          <span class="radio-desc">按得分率进行评估</span>
        </label>
        <label class="radio-label" :class="{ active: !config.use_score_rate }">
          <input type="radio" v-model="localConfig.use_score_rate" :value="false" />
          <span class="radio-circle"></span>
          <span class="radio-text">否</span>
          <span class="radio-desc">按原始分数进行评估</span>
        </label>
      </div>
    </div>

    <!-- 语言科目总分 -->
    <div class="param-item">
      <div class="param-header">
        <label class="param-label">语言科目总分（语文、数学、外语）</label>
        <div class="param-value-wrapper">
          <span class="param-value">{{ localConfig.language_total }}</span>
          <span class="param-unit">分</span>
        </div>
        <span class="tooltip-wrapper">
          <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
          </svg>
          <span class="tooltip-text">语文、数学、外语三科的单科满分分值</span>
        </span>
      </div>
      <div class="param-controls">
        <input type="number" min="0" max="300" v-model.number="localConfig.language_total" class="number-input-small" />
        <input type="range" min="0" max="300" v-model.number="localConfig.language_total" class="slider" />
      </div>
      <div class="range-labels">
        <span>0</span>
        <span>300</span>
      </div>
    </div>

    <!-- 理科科目总分 -->
    <div class="param-item">
      <div class="param-header">
        <label class="param-label">理科科目总分（物理、化学、生物等）</label>
        <div class="param-value-wrapper">
          <span class="param-value">{{ localConfig.science_total }}</span>
          <span class="param-unit">分</span>
        </div>
        <span class="tooltip-wrapper">
          <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
          </svg>
          <span class="tooltip-text">物理、化学、生物等理科科目单科满分分值</span>
        </span>
      </div>
      <div class="param-controls">
        <input type="number" min="0" max="300" v-model.number="localConfig.science_total" class="number-input-small" />
        <input type="range" min="0" max="300" v-model.number="localConfig.science_total" class="slider" />
      </div>
      <div class="range-labels">
        <span>0</span>
        <span>300</span>
      </div>
    </div>

    <!-- 保存按钮 -->
    <div class="section-actions">
      <button class="btn btn-primary" @click="saveConfig" :disabled="!hasChanges">
        保存配置
      </button>
    </div>

    <!-- 得分率计算公式说明 -->
    <div class="info-card small">
      <h5 class="info-title">📝 得分率计算公式</h5>
      <div class="formula">
        <p>得分率 = (实际得分 ÷ 科目总分) × 100%</p>
      </div>
      <div class="example">
        <p><strong>示例：</strong>语文135分（满分150分）→ 得分率 = (135 ÷ 150) × 100% = 90%</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { gradeService } from '@/services/gradeService'

const emit = defineEmits(['config-updated'])

const config = reactive({
  use_score_rate: true,
  language_total: 150,
  science_total: 100
})

const localConfig = reactive({
  use_score_rate: true,
  language_total: 150,
  science_total: 100
})

const hasChanges = ref(false)

watch(localConfig, (newVal) => {
  hasChanges.value = 
    newVal.use_score_rate !== config.use_score_rate ||
    newVal.language_total !== config.language_total ||
    newVal.science_total !== config.science_total
}, { deep: true })

const loadConfig = async () => {
  try {
    const response = await gradeService.getScoreRateConfig()
    config.use_score_rate = response.use_score_rate
    config.language_total = response.language_total
    config.science_total = response.science_total
    
    localConfig.use_score_rate = config.use_score_rate
    localConfig.language_total = config.language_total
    localConfig.science_total = config.science_total
  } catch (error) {
    console.error('获取得分率配置失败:', error)
  }
}

const saveConfig = async () => {
  try {
    const response = await gradeService.updateScoreRateConfig(localConfig)
    if (response.success) {
      config.use_score_rate = localConfig.use_score_rate
      config.language_total = localConfig.language_total
      config.science_total = localConfig.science_total
      hasChanges.value = false
      emit('config-updated', localConfig)
    }
  } catch (error) {
    console.error('更新得分率配置失败:', error)
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.score-rate-config {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

.param-item {
  margin-bottom: 20px;
}

.param-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.param-label {
  font-weight: 500;
  color: #333;
}

.param-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.param-value {
  font-size: 18px;
  font-weight: 600;
  color: #1890ff;
}

.param-unit {
  font-size: 14px;
  color: #999;
}

.tooltip-wrapper {
  position: relative;
  cursor: help;
}

.tooltip-icon {
  color: #999;
}

.tooltip-text {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s, visibility 0.2s;
  z-index: 100;
  margin-bottom: 8px;
}

.tooltip-wrapper:hover .tooltip-text {
  opacity: 1;
  visibility: visible;
}

.param-controls {
  display: flex;
  align-items: center;
  gap: 16px;
}

.number-input-small {
  width: 80px;
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  text-align: center;
}

.slider {
  flex: 1;
  height: 6px;
  cursor: pointer;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.radio-group {
  display: flex;
  gap: 16px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.radio-label:hover {
  background-color: #f5f5f5;
}

.radio-label.active {
  background-color: #e6f7ff;
}

.radio-circle {
  width: 18px;
  height: 18px;
  border: 2px solid #d9d9d9;
  border-radius: 50%;
  position: relative;
}

.radio-label.active .radio-circle {
  border-color: #1890ff;
}

.radio-label.active .radio-circle::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background-color: #1890ff;
  border-radius: 50%;
}

.radio-text {
  font-weight: 500;
}

.radio-desc {
  font-size: 12px;
  color: #999;
}

.section-actions {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-primary {
  background-color: #1890ff;
  color: #fff;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.info-card {
  margin-top: 16px;
  background: #fafafa;
  border-radius: 8px;
  padding: 12px;
}

.info-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.formula {
  background: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.formula p {
  margin: 0;
  font-family: monospace;
  font-size: 13px;
}

.example p {
  margin: 0;
  font-size: 13px;
  color: #666;
}
</style>