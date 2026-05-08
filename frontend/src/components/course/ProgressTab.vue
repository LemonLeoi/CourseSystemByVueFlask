<template>
  <div class="course-tab-content">
    <!-- 消息提示 -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- 筛选器 -->
    <div class="course-filter">
      <div class="filter-group">
        <label>科目:</label>
        <select v-model="localProgressSubject" @change="handleSubjectChange" :disabled="isLoading || loadingSubjects">
          <option v-if="loadingSubjects" value="">加载中...</option>
          <option v-else-if="subjects.length === 0" value="">暂无科目数据</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">
            {{ subject }}
          </option>
        </select>
      </div>
      <div class="filter-group">
        <label>年级:</label>
        <select v-model="localProgressGrade" @change="handleGradeChange" :disabled="isLoading">
          <option value="高一">高一</option>
          <option value="高二">高二</option>
          <option value="高三">高三</option>
        </select>
      </div>
      <div class="filter-actions">
        <button class="btn btn-primary" @click="$emit('refreshProgress')" :disabled="isLoading">
          {{ isLoading ? '刷新中...' : '刷新' }}
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">
      <p>加载中...</p>
    </div>

    <!-- 教学进度列表 -->
    <div v-else class="progress-list">
      <div class="progress-item" v-for="progress in teachingProgress" :key="progress.id">
        <div class="progress-header">
          <div class="progress-chapter">{{ progress.chapter }}</div>
          <div class="progress-actions">
            <button class="btn btn-secondary" @click="$emit('editProgress', progress)">
              编辑
            </button>
            <button class="btn btn-danger" @click="$emit('deleteProgress', progress.id)">
              删除
            </button>
          </div>
        </div>
        <div class="progress-details">
          <div class="detail-item">
            <span class="detail-label">课时:</span>
            <span class="detail-value">{{ progress.hours }}课时</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">教学目标:</span>
            <span class="detail-value">{{ progress.objective }}</span>
          </div>
        </div>
        <div class="progress-bar-container">
          <div class="progress-info">
            <span>进度: {{ progress.progress }}%</span>
            <span>{{ $emit('getStatusText', progress.status) }}</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :class="`status-${progress.status}`"
              :style="{ width: `${progress.progress}%` }"
            ></div>
          </div>
        </div>
      </div>
      <div class="empty-state" v-if="teachingProgress.length === 0">
        <p>暂无教学进度数据</p>
        <button class="btn btn-primary" @click="$emit('openAddProgressModal')">
          添加进度
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { courseApi } from '@/services/api/apiService';

const props = defineProps<{
  progressSubject: string;
  progressGrade: string;
  teachingProgress: Array<{
    id: number;
    chapter: string;
    hours: number;
    objective: string;
    progress: number;
    status: string;
  }>;
  isLoading?: boolean;
  error?: string | null;
  successMessage?: string | null;
}>();

const emit = defineEmits<{
  'update:progressSubject': [value: string];
  'update:progressGrade': [value: string];
  'refreshProgress': [];
  'openAddProgressModal': [];
  'editProgress': [progress: any];
  'deleteProgress': [id: number];
  'getStatusText': [status: string];
}>();

const localProgressSubject = ref(props.progressSubject);
const localProgressGrade = ref(props.progressGrade);
const subjects = ref<string[]>([]);
const loadingSubjects = ref(false);

// 加载科目列表
const loadSubjects = async () => {
  console.log('开始加载科目列表');
  try {
    loadingSubjects.value = true;
    console.log('调用courseApi.getSubjects()');
    
    // 使用courseApi.getSubjects()方法获取科目列表
    const subjectList = await courseApi.getSubjects();
    console.log('courseApi.getSubjects()获取到的科目列表:', subjectList);
    console.log('科目数量:', subjectList.length);
    
    // 确保subjectList是数组
    if (Array.isArray(subjectList)) {
      subjects.value = subjectList;
      console.log('subjects.value设置后:', subjects.value);
      console.log('subjects.value长度:', subjects.value.length);
      
      // 如果有科目且当前没有选中科目，默认选择第一个
      if (subjectList.length > 0 && !localProgressSubject.value) {
        localProgressSubject.value = subjectList[0];
        emit('update:progressSubject', subjectList[0]);
        console.log('默认选择第一个科目:', subjectList[0]);
      }
    } else {
      console.error('科目列表不是数组:', subjectList);
      // 使用默认科目
      subjects.value = ['语文', '数学', '英语', '物理', '化学', '生物'];
      console.log('使用默认科目:', subjects.value);
    }
  } catch (error) {
    console.error('获取科目列表失败:', error);
    // 失败时使用默认科目
    subjects.value = ['语文', '数学', '英语', '物理', '化学', '生物'];
    console.log('使用默认科目:', subjects.value);
  } finally {
    loadingSubjects.value = false;
    console.log('加载科目列表完成');
  }
};

// 监听 props 变化
watch(() => props.progressSubject, (newValue) => {
  localProgressSubject.value = newValue;
});

watch(() => props.progressGrade, (newValue) => {
  localProgressGrade.value = newValue;
});

// 处理科目变化
const handleSubjectChange = () => {
  emit('update:progressSubject', localProgressSubject.value);
};

// 处理年级变化
const handleGradeChange = () => {
  emit('update:progressGrade', localProgressGrade.value);
};

// 初始化数据
onMounted(() => {
  console.log('ProgressTab组件挂载，调用loadSubjects()');
  loadSubjects();
});
</script>

<style scoped>
/* 引用共享样式 */
@import '@/styles/course/CourseManage.css';
</style>