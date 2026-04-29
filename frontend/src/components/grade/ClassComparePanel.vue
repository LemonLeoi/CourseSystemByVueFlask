<template>
  <div class="class-compare-panel">
    <div class="panel-header">
      <div class="header-icon">📊</div>
      <div class="header-content">
        <h3 class="panel-title">班级对比分析</h3>
        <p class="panel-subtitle">Class Comparison Analysis</p>
      </div>
    </div>
    
    <!-- 班级选择 -->
    <div class="class-selector">
      <div class="selector-label">选择对比班级:</div>
      <div class="class-tags">
        <div 
          v-for="cls in availableClasses" 
          :key="cls"
          class="class-tag"
          :class="{ selected: selectedClasses.includes(cls) }"
          @click="toggleClass(cls)"
        >
          {{ cls }}
        </div>
      </div>
      <button 
        class="compare-btn" 
        :disabled="selectedClasses.length < 2"
        @click="executeCompare"
      >
        {{ isLoading ? '对比中...' : '开始对比' }}
      </button>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在进行班级对比...</p>
    </div>
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
      <button class="retry-btn" @click="executeCompare">重试</button>
    </div>
    
    <!-- 对比结果 -->
    <div v-else-if="comparisonData" class="comparison-result">
      <!-- 教师组信息 -->
      <div class="teacher-info">
        <div class="info-badge" :class="comparisonData.teacher_comparison.same_group ? 'same-group' : 'diff-group'">
          <span>
            {{ comparisonData.teacher_comparison.same_group 
              ? '同教师组对比' 
              : '跨教师组对比' 
            }}
          </span>
        </div>
        <div class="group-list">
          <span v-for="group in comparisonData.teacher_comparison.groups" :key="group" class="group-tag">
            {{ group }}
          </span>
        </div>
      </div>
      
      <!-- 基准班级 -->
      <div class="base-class-card">
        <div class="card-header">
          <span class="card-label">基准班级</span>
          <span class="class-name">{{ comparisonData.base_class.class_name }}</span>
        </div>
        <div class="metrics-grid">
          <div v-for="metric in displayMetrics" :key="metric.key" class="metric-item">
            <div class="metric-label">{{ metric.label }}</div>
            <div class="metric-value">{{ formatValue(comparisonData.base_class.metrics[metric.key as keyof typeof comparisonData.base_class.metrics]) }}</div>
            <div class="metric-unit">{{ metric.unit }}</div>
          </div>
        </div>
        <div class="student-count">
          学生人数: {{ comparisonData.base_class.student_count }} 人
        </div>
      </div>
      
      <!-- 对比班级列表 -->
      <div class="compare-classes">
        <div 
          v-for="compare in comparisonData.comparisons" 
          :key="compare.class_id"
          class="compare-class-card"
        >
          <div class="card-header">
            <span class="card-label">对比班级</span>
            <span class="class-name">{{ compare.class_name }}</span>
          </div>
          <div class="metrics-grid comparison">
            <div v-for="metric in displayMetrics" :key="metric.key" class="metric-item">
              <div class="metric-label">{{ metric.label }}</div>
              <div class="metric-value-row">
                <span class="compare-value">{{ formatValue(compare.differences[metric.key].compare_value) }}</span>
                <span 
                  class="difference" 
                  :class="compare.differences[metric.key].difference >= 0 ? 'positive' : 'negative'"
                >
                  {{ compare.differences[metric.key].difference >= 0 ? '+' : '' }}{{ compare.differences[metric.key].difference.toFixed(1) }}
                </span>
              </div>
              <div class="change-bar">
                <div 
                  class="change-fill" 
                  :class="compare.differences[metric.key].difference >= 0 ? 'positive' : 'negative'"
                  :style="{ width: Math.abs(compare.differences[metric.key].percentage) + '%' }"
                ></div>
              </div>
              <div class="change-percentage">
                {{ compare.differences[metric.key].percentage >= 0 ? '+' : '' }}{{ compare.differences[metric.key].percentage }}%
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 统计显著性 -->
      <div class="significance-info">
        <div class="significance-label">统计显著性:</div>
        <div class="significance-value" :class="comparisonData.statistical_significance.significant ? 'significant' : 'not-significant'">
          <span>p-value = {{ comparisonData.statistical_significance.p_value.toFixed(4) }}</span>
          <span class="significance-status">
            {{ comparisonData.statistical_significance.significant ? '差异显著' : '差异不显著' }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">👆</div>
      <p>请选择至少2个班级进行对比分析</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { gradeService, type ClassCompareResponse } from '../../services/gradeService';

interface Props {
  currentClass?: string;
}

const props = defineProps<Props>();

// 根据当前班级动态生成同年级班级列表
const availableClasses = computed(() => {
  if (!props.currentClass) {
    return ['高一1班', '高一2班', '高一3班', '高一4班', '高一5班', '高一6班'];
  }
  
  const grade = props.currentClass.slice(0, 2);
  return [`${grade}1班`, `${grade}2班`, `${grade}3班`, `${grade}4班`, `${grade}5班`, `${grade}6班`];
});

const selectedClasses = ref<string[]>([]);
const isLoading = ref(false);
const error = ref('');
const comparisonData = ref<ClassCompareResponse | null>(null);

const displayMetrics = [
  { key: 'average_score', label: '平均分', unit: '分' },
  { key: 'pass_rate', label: '及格率', unit: '%' },
  { key: 'excellent_rate', label: '优秀率', unit: '%' },
  { key: 'improvement_rate', label: '提分率', unit: '%' }
];

const toggleClass = (cls: string) => {
  const index = selectedClasses.value.indexOf(cls);
  if (index > -1) {
    selectedClasses.value.splice(index, 1);
  } else if (selectedClasses.value.length < 4) {
    selectedClasses.value.push(cls);
  }
};

const formatValue = (value: number | undefined): string => {
  if (value === undefined) return '-';
  return value.toFixed(1);
};

const executeCompare = async () => {
  if (selectedClasses.value.length < 2) return;
  
  isLoading.value = true;
  error.value = '';
  comparisonData.value = null;
  
  try {
    const response = await gradeService.compareClasses(selectedClasses.value);
    
    // 过滤掉同教师组的对比选项
    if (response && response.comparisons && response.base_class) {
      const baseTeacherGroup = response.base_class.teacher_group;
      response.comparisons = response.comparisons.filter((cmp) => {
        // 从后端返回的数据中获取对比班级的教师组
        const compareTeacherGroup = getTeacherGroupFromClassId(cmp.class_id);
        return baseTeacherGroup !== compareTeacherGroup;
      });
    }
    
    comparisonData.value = response;
  } catch (e) {
    error.value = '班级对比失败，请稍后重试';
    console.error('Failed to compare classes:', e);
  } finally {
    isLoading.value = false;
  }
};

const getTeacherGroupFromClassId = (classId: string): string => {
  // 根据班级编号获取教师组
  // 规则：1班和2班为相同教师组，3班和4班为一个组，5班和6班为一个组
  const match = classId.match(/(\d+)/);
  if (match) {
    const classNum = parseInt(match[1]);
    const teacherGroup = (classNum - 1) // 2;
    const teacherGroups = {
      0: '教师组1',
      1: '教师组2', 
      2: '教师组3'
    };
    return teacherGroups[teacherGroup] || '教师组1';
  }
  return '教师组1';
};
</script>

<style scoped>
.class-compare-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.panel-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.header-icon {
  font-size: 24px;
  margin-right: 10px;
}

.header-content {
  flex: 1;
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.panel-subtitle {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #9ca3af;
}

/* 班级选择器 */
.class-selector {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.selector-label {
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 10px;
}

.class-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.class-tag {
  padding: 6px 12px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.class-tag:hover {
  background: #e5e7eb;
}

.class-tag.selected {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.compare-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.compare-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.compare-btn:disabled {
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

/* 错误状态 */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  background: #fef2f2;
  border-radius: 8px;
}

.error-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.error-state p {
  margin: 0 0 12px 0;
  color: #dc2626;
}

.retry-btn {
  padding: 6px 16px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

/* 对比结果 */
.comparison-result {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 教师组信息 */
.teacher-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.info-badge.same-group {
  background: #d1fae5;
  color: #059669;
}

.info-badge.diff-group {
  background: #fef3c7;
  color: #d97706;
}

.group-list {
  display: flex;
  gap: 6px;
}

.group-tag {
  padding: 2px 8px;
  background: #f3f4f6;
  border-radius: 4px;
  font-size: 11px;
  color: #6b7280;
}

/* 班级卡片 */
.base-class-card,
.compare-class-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
}

.card-label {
  font-size: 11px;
  color: #9ca3af;
  padding: 2px 6px;
  background: #e5e7eb;
  border-radius: 4px;
  margin-right: 8px;
}

.class-name {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
}

.teacher-group {
  margin-left: auto;
  font-size: 12px;
  padding: 3px 8px;
  background: #e0e7ff;
  border-radius: 4px;
}

/* 指标网格 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.metric-item {
  text-align: center;
}

.metric-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 20px;
  font-weight: 600;
  color: #374151;
}

.metric-unit {
  font-size: 11px;
  color: #9ca3af;
}

.student-count {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
  font-size: 13px;
  color: #6b7280;
  text-align: center;
}

/* 对比指标 */
.metrics-grid.comparison .metric-item {
  display: flex;
  flex-direction: column;
}

.metric-value-row {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 8px;
}

.compare-value {
  font-size: 18px;
  font-weight: 600;
  color: #374151;
}

.difference {
  font-size: 14px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.difference.positive {
  background: #d1fae5;
  color: #059669;
}

.difference.negative {
  background: #fee2e2;
  color: #dc2626;
}

.change-bar {
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  margin: 4px 0;
  overflow: hidden;
}

.change-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.change-fill.positive {
  background: #10b981;
}

.change-fill.negative {
  background: #ef4444;
}

.change-percentage {
  font-size: 11px;
  color: #6b7280;
}

/* 统计显著性 */
.significance-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.significance-label {
  font-size: 13px;
  color: #6b7280;
}

.significance-value {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.significance-value.significant {
  color: #059669;
}

.significance-value.not-significant {
  color: #6b7280;
}

.significance-status {
  padding: 2px 6px;
  background: #e5e7eb;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.significance-value.significant .significance-status {
  background: #d1fae5;
  color: #059669;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-state p {
  margin: 0;
  color: #6b7280;
}

/* 响应式 */
@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .teacher-info {
    flex-wrap: wrap;
  }
  
  .card-header {
    flex-wrap: wrap;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .class-tags {
    justify-content: center;
  }
}
</style>