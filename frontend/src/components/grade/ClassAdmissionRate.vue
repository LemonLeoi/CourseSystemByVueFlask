<template>
  <div class="section admission-rate">
    <div class="section-header">
      <h4 class="section-title">
        <span class="section-icon">📊</span> 班级上线率统计
      </h4>
      <span class="section-hint">统计班级学生达到重本线和本科线的比例</span>
    </div>

    <!-- 选择班级 -->
    <div class="class-select-wrapper">
      <label class="select-label">选择班级</label>
      <select v-model="selectedClass" @change="loadData" class="class-select">
        <option value="">请选择班级</option>
        <option v-for="cls in classes" :key="cls" :value="cls">{{ cls }}</option>
      </select>
    </div>

    <!-- 统计结果 -->
    <div v-if="statistics" class="statistics">
      <!-- 重本上线率 -->
      <div class="stat-card key">
        <div class="stat-icon">🏆</div>
        <div class="stat-value">{{ statistics.key_university_rate }}%</div>
        <div class="stat-label">重本上线率</div>
        <div class="stat-detail">{{ statistics.key_university_count }}/{{ statistics.total_students }}人</div>
        <div class="stat-line">分数线: {{ statistics.key_university_line }}分</div>
        <div class="stat-bar">
          <div class="stat-bar-fill" :style="{ width: statistics.key_university_rate + '%' }"></div>
        </div>
      </div>

      <!-- 本科上线率 -->
      <div class="stat-card undergrad">
        <div class="stat-icon">📚</div>
        <div class="stat-value">{{ statistics.undergraduate_rate }}%</div>
        <div class="stat-label">本科上线率</div>
        <div class="stat-detail">{{ statistics.undergraduate_count }}/{{ statistics.total_students }}人</div>
        <div class="stat-line">分数线: {{ statistics.undergraduate_line }}分</div>
        <div class="stat-bar">
          <div class="stat-bar-fill" :style="{ width: statistics.undergraduate_rate + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">📝</div>
      <p>请选择班级查看上线率统计</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>正在计算上线率...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { gradeService } from '@/services/gradeService'

const classes = ref<string[]>([])
const selectedClass = ref('')
const statistics = ref<{
  class_id: string
  total_students: number
  key_university_count: number
  undergraduate_count: number
  key_university_rate: number
  undergraduate_rate: number
  key_university_line: number
  undergraduate_line: number
} | null>(null)
const loading = ref(false)

const loadClasses = async () => {
  try {
    const response = await gradeService.getClasses()
    classes.value = response.map((c: any) => c.class_name)
  } catch (error) {
    console.error('获取班级列表失败:', error)
  }
}

const loadData = async () => {
  if (!selectedClass.value) {
    statistics.value = null
    return
  }

  loading.value = true
  try {
    const response = await gradeService.getClassAdmissionRate(selectedClass.value)
    statistics.value = response
  } catch (error) {
    console.error('获取上线率统计失败:', error)
    statistics.value = null
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadClasses()
})
</script>

<style scoped>
.admission-rate {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

.section-header {
  margin-bottom: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.section-icon {
  font-size: 18px;
}

.section-hint {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.class-select-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.select-label {
  font-weight: 500;
  color: #666;
}

.class-select {
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  min-width: 150px;
}

.statistics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: #fff;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.stat-card.key {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
}

.stat-card.undergrad {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.stat-detail {
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.stat-line {
  font-size: 11px;
  opacity: 0.7;
  margin-bottom: 12px;
}

.stat-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.stat-bar-fill {
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-state p {
  margin: 0;
}

.loading-state {
  text-align: center;
  padding: 40px 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1890ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  margin: 0;
  color: #999;
}
</style>