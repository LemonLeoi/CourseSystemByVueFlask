<template>
  <div class="course-tab-content">
    <!-- 筛选器 -->
    <div class="course-filter">
      <div class="filter-group">
        <label>年级:</label>
        <select v-model="localStudentGrade" @change="handleGradeChange" :disabled="isLoadingOptions">
          <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>班级:</label>
        <select v-model="localStudentClass" @change="handleClassChange" :disabled="isLoadingOptions">
          <option v-for="classItem in classes" :key="classItem" :value="classItem">{{ classItem }}</option>
        </select>
      </div>
      <div class="filter-actions">
        <button class="btn btn-primary" @click="$emit('refreshStudentSchedule')">
          刷新
        </button>
      </div>
    </div>

    <!-- 消息提示 -->
    <div v-if="successMessage" class="message success">
      {{ successMessage }}
      <button class="message-close" @click="$emit('update:successMessage', null)">&times;</button>
    </div>
    <div v-if="error" class="message error">
      {{ error }}
      <button class="message-close" @click="$emit('update:error', null)">&times;</button>
    </div>

    <!-- 课程表 -->
    <div class="course-table-container">
      <table class="course-table">
        <thead>
          <tr>
            <th class="time-slot-header">节次</th>
            <th v-for="day in weekDays" :key="day" class="day-header">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="slot in timeSlots" :key="slot.id">
            <td class="time-slot-cell">{{ slot.name }}</td>
            <td 
              v-for="day in weekDays" 
              :key="`${day}-${slot.id}`"
              class="course-cell"
            >
              <div v-if="getCourse(day, slot.id)" class="course-item">
                <div class="course-content" @click="$emit('openEditStudentCourseModal', day, slot.id)">
                  <div class="course-name">{{ getCourse(day, slot.id)?.name }}</div>
                  <div class="course-teacher">{{ getCourse(day, slot.id)?.teacher }}</div>
                  <div class="course-classroom">{{ getCourse(day, slot.id)?.classroom }}</div>
                </div>
                <div class="course-actions">
                  <button 
                    class="btn btn-sm btn-danger" 
                    @click.stop="confirmDelete(day, slot.id)"
                    :disabled="isLoading"
                  >
                    <span v-if="isLoading" class="loading-spinner"></span>
                    <span v-else>删除</span>
                  </button>
                </div>
              </div>
              <div v-else class="course-empty" @click="$emit('openEditStudentCourseModal', day, slot.id)">
                <span>+ 添加课程</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 确认对话框 -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="modal-close" @click="cancelDelete">&times;</button>
        </div>
        <div class="modal-body">
          <p>确定要删除这节课吗？此操作不可撤销。</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="cancelDelete">取消</button>
          <button 
            class="btn btn-danger" 
            @click="performDelete"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="loading-spinner"></span>
            <span v-else>确认删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  studentGrade: string;
  studentClass: string;
  studentCourses: Array<{
    day: string;
    timeSlot: number;
    name: string;
    teacher: string;
    classroom: string;
  }>;
  timeSlots: Array<{
    id: number;
    name: string;
  }>;
  weekDays: string[];
  isLoading?: boolean;
  error?: string | null;
  successMessage?: string | null;
}>();

const emit = defineEmits<{
  'update:studentGrade': [value: string];
  'update:studentClass': [value: string];
  'update:successMessage': [value: string | null];
  'update:error': [value: string | null];
  'refreshStudentSchedule': [];
  'openAddStudentCourseModal': [];
  'openEditStudentCourseModal': [day: string, timeSlot: number];
  'deleteStudentCourse': [day: string, timeSlot: number];
}>();

const localStudentGrade = ref(props.studentGrade);
const localStudentClass = ref(props.studentClass);
const showDeleteConfirm = ref(false);
const deleteDay = ref('');
const deleteTimeSlot = ref(0);

// 班级和年级列表（从后端API获取）
const grades = ref<string[]>([]);
const classes = ref<string[]>([]);
const isLoadingOptions = ref(false);

// 从后端API获取班级和年级列表
const loadClassOptions = async () => {
  try {
    isLoadingOptions.value = true;
    console.log('=== 开始获取班级和年级列表 ===');
    const response = await fetch('/api/students/classes');
    if (!response.ok) {
      throw new Error('获取班级和年级列表失败');
    }
    const data = await response.json();
    console.log('=== API响应成功 ===');
    console.log('获取到的班级和年级列表:', data);
    grades.value = data.grades || [];
    classes.value = data.classes || [];
    console.log('=== 选项卡数据更新完成 ===');
  } catch (error) {
    console.error('=== 获取班级和年级列表失败 ===');
    console.error('错误信息:', error);
    // 失败时使用默认值，确保系统能正常运行
    grades.value = ['高一', '高二', '高三'];
    classes.value = ['1班', '2班', '3班', '4班', '5班', '6班'];
  } finally {
    isLoadingOptions.value = false;
  }
};

// 监听 props 变化
watch(() => props.studentGrade, (newValue) => {
  localStudentGrade.value = newValue;
});

watch(() => props.studentClass, (newValue) => {
  localStudentClass.value = newValue;
});

// 处理年级变化
const handleGradeChange = () => {
  emit('update:studentGrade', localStudentGrade.value);
};

// 处理班级变化
const handleClassChange = () => {
  emit('update:studentClass', localStudentClass.value);
};

// 获取指定天和时间段的课程
const getCourse = (day: string, timeSlot: number) => {
  return props.studentCourses.find(course => course.day === day && course.timeSlot === timeSlot);
};

// 确认删除
const confirmDelete = (day: string, timeSlot: number) => {
  deleteDay.value = day;
  deleteTimeSlot.value = timeSlot;
  showDeleteConfirm.value = true;
};

// 取消删除
const cancelDelete = () => {
  showDeleteConfirm.value = false;
  deleteDay.value = '';
  deleteTimeSlot.value = 0;
};

// 执行删除
const performDelete = () => {
  if (deleteDay.value && deleteTimeSlot.value !== undefined && deleteTimeSlot.value !== null) {
    emit('deleteStudentCourse', deleteDay.value, deleteTimeSlot.value);
    showDeleteConfirm.value = false;
    deleteDay.value = '';
    deleteTimeSlot.value = 0;
  }
};

// 初始化数据
onMounted(async () => {
  // 加载班级和年级列表
  await loadClassOptions();
  
  // 设置定时刷新机制，每5分钟刷新一次选项卡数据
  const refreshInterval = setInterval(async () => {
    console.log('=== 定时刷新班级和年级列表 ===');
    await loadClassOptions();
  }, 5 * 60 * 1000);
  
  // 组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(refreshInterval);
  });
});
</script>

<style scoped>
/* 引用共享样式 */
@import '@/styles/course/CourseManage.css';

/* 课程内容和操作区域样式 */
.course-item {
  position: relative;
  z-index: 1;
}

.course-content {
  cursor: pointer;
  transition: background-color var(--transition-fast);
  padding: var(--spacing-xs);
  border-radius: var(--border-radius-sm);
  z-index: 2;
}

.course-content:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.course-actions {
  margin-top: var(--spacing-xs);
  display: flex;
  justify-content: flex-end;
  z-index: 3;
  position: relative;
}

/* 按钮样式 */
.btn-sm {
  padding: 2px 8px;
  font-size: 12px;
}

/* 消息提示样式 */
.message {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-sm);
  margin-bottom: var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease-out;
}

.message.success {
  background-color: #d4edda;
  color: #155724;
  border-left: 4px solid #28a745;
}

.message.error {
  background-color: #f8d7da;
  color: #721c24;
  border-left: 4px solid #dc3545;
}

.message-close {
  background: none;
  border: none;
  font-size: var(--font-size-lg);
  cursor: pointer;
  color: inherit;
  padding: 0;
  margin-left: var(--spacing-sm);
}

/* 确认对话框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 400px;
  animation: slideUp 0.3s ease-out;
}

.modal-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  font-size: var(--font-size-lg);
  cursor: pointer;
  color: var(--text-secondary);
  transition: color var(--transition-fast);
}

.modal-close:hover {
  color: var(--text-primary);
}

.modal-body {
  padding: var(--spacing-md);
}

.modal-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}

/* 加载状态样式 */
.loading-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

/* 动画效果 */
@keyframes slideIn {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>