<template>
  <div class="section admission-line-config">
    <div class="section-header">
      <h4 class="section-title">
        <span class="section-icon">🎯</span> 分数线设置
      </h4>
      <span class="section-hint">配置重本线和本科线两个关键阈值</span>
    </div>

    <!-- 重本线 -->
    <div class="param-item">
      <div class="param-header">
        <label class="param-label">重本线</label>
        <div class="param-value-wrapper">
          <span class="param-value">{{ localConfig.key_university_line }}</span>
          <span class="param-unit">分</span>
        </div>
        <span class="tooltip-wrapper">
          <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
          </svg>
          <span class="tooltip-text">高于此分数的学生视为达到重本线</span>
        </span>
      </div>
      <div class="param-controls">
        <input type="number" min="0" max="750" v-model.number="localConfig.key_university_line" class="number-input-small" />
        <input type="range" min="0" max="750" v-model.number="localConfig.key_university_line" class="slider" />
      </div>
      <div class="range-labels">
        <span>0</span>
        <span>750</span>
      </div>
    </div>

    <!-- 本科线 -->
    <div class="param-item">
      <div class="param-header">
        <label class="param-label">本科线</label>
        <div class="param-value-wrapper">
          <span class="param-value">{{ localConfig.undergraduate_line }}</span>
          <span class="param-unit">分</span>
        </div>
        <span class="tooltip-wrapper">
          <svg class="tooltip-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
          </svg>
          <span class="tooltip-text">高于此分数的学生视为达到本科线</span>
        </span>
      </div>
      <div class="param-controls">
        <input type="number" min="0" max="750" v-model.number="localConfig.undergraduate_line" class="number-input-small" />
        <input type="range" min="0" max="750" v-model.number="localConfig.undergraduate_line" class="slider" />
      </div>
      <div class="range-labels">
        <span>0</span>
        <span>750</span>
      </div>
    </div>

    <!-- 验证提示 -->
    <div v-if="localConfig.key_university_line <= localConfig.undergraduate_line" class="validation-error">
      ⚠️ 重本线必须大于本科线
    </div>

    <!-- 保存按钮 -->
    <div class="section-actions">
      <button 
        class="btn btn-primary" 
        @click="saveConfig" 
        :disabled="!hasChanges || localConfig.key_university_line <= localConfig.undergraduate_line"
      >
        保存配置
      </button>
    </div>

    <!-- 上线率计算公式说明 -->
    <div class="info-card small">
      <h5 class="info-title">📈 上线率计算公式</h5>
      <div class="formula-list">
        <p><strong>重本上线率</strong> = (重本线以上人数 ÷ 班级总人数) × 100%</p>
        <p><strong>本科上线率</strong> = (本科线以上人数 ÷ 班级总人数) × 100%</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { gradeService } from '@/services/gradeService'

const emit = defineEmits(['config-updated'])

const config = reactive({
  key_university_line: 520,
  undergraduate_line: 430
})

const localConfig = reactive({
  key_university_line: 520,
  undergraduate_line: 430
})

const hasChanges = ref(false)

watch(localConfig, (newVal) => {
  hasChanges.value = 
    newVal.key_university_line !== config.key_university_line ||
    newVal.undergraduate_line !== config.undergraduate_line
}, { deep: true })

const loadConfig = async () => {
  try {
    const response = await gradeService.getAdmissionLineConfig()
    config.key_university_line = response.key_university_line
    config.undergraduate_line = response.undergraduate_line
    
    localConfig.key_university_line = config.key_university_line
    localConfig.undergraduate_line = config.undergraduate_line
  } catch (error) {
    console.error('获取分数线配置失败:', error)
  }
}

const saveConfig = async () => {
  try {
    const response = await gradeService.updateAdmissionLineConfig(localConfig)
    if (response.success) {
      config.key_university_line = localConfig.key_university_line
      config.undergraduate_line = localConfig.undergraduate_line
      hasChanges.value = false
      emit('config-updated', localConfig)
    }
  } catch (error) {
    console.error('更新分数线配置失败:', error)
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.admission-line-config {
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
  color: #52c41a;
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

.validation-error {
  background: #fff2f0;
  border: 1px solid #ffccc7;
  color: #d93026;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  margin-bottom: 16px;
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
  background-color: #52c41a;
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

.formula-list p {
  margin: 4px 0;
  font-size: 13px;
  font-family: monospace;
}

.formula-list strong {
  color: #52c41a;
}
</style>