<template>
  <div class="course-tab-content">
    <!-- 筛选器 -->
    <div class="course-filter">
      <div class="filter-group">
        <label>教师:</label>
        <select v-model="localSelectedTeacher" @change="handleTeacherChange">
          <option value="">请选择教师</option>
          <option v-for="teacher in teachers" :key="teacher.teacher_id" :value="teacher.teacher_id">
            {{ teacher.name }} ({{ teacher.subject || teacher.department }})
          </option>
        </select>
        <!-- 显示任教班级 -->
        <div class="teacher-classes" v-if="selectedTeacherClasses.length > 0">
          <span class="classes-label">任教班级:</span>
          <span class="classes-list">{{ selectedTeacherClasses.join(', ') }}</span>
        </div>
      </div>
      <div class="filter-actions">
        <button class="btn btn-primary" @click="$emit('refreshTeacherSchedule')">
          刷新
        </button>
      </div>
    </div>

    <!-- 消息提示 -->
    <div v-if="successMessage" class="message success">
      {{ successMessage }}
      <button class="message-close" @click="$props.successMessage = null">&times;</button>
    </div>
    <div v-if="error" class="message error">
      {{ error }}
      <button class="message-close" @click="$props.error = null">&times;</button>
    </div>

    <!-- 教师统计信息 -->
    <div class="teacher-stats" v-if="teacherStats">
      <div class="stat-card">
        <div class="stat-value">{{ teacherStats.totalClasses }}</div>
        <div class="stat-label">总课时</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ teacherStats.mostClass }}</div>
        <div class="stat-label">最多班级</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ teacherStats.busiestDay }}</div>
        <div class="stat-label">最忙日期</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ teacherStats.avgClasses }}节/天</div>
        <div class="stat-label">日均课时</div>
      </div>
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
                <div class="course-content" @click="$emit('openEditTeacherCourseModal', day, slot.id)">
                  <div class="course-name">{{ getCourse(day, slot.id)?.name }}</div>
                  <div class="course-class">{{ getCourse(day, slot.id)?.className }}</div>
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
              <div v-else class="course-empty" @click="$emit('openEditTeacherCourseModal', day, slot.id)">
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
import { ref, computed, watch } from 'vue';

const props = defineProps<{
  selectedTeacher: string;
  teachers: Array<{
    id?: string;
    teacher_id?: string;
    name: string;
    subject?: string;
    department?: string;
    gender?: string;
    title?: string;
    contact?: string;
    teachingClasses?: string[];
    isHomeroomTeacher?: boolean;
    homeroomClass?: string;
  }>;
  teacherCourses: Array<{
    day: string;
    timeSlot: number;
    name: string;
    className: string;
    classroom: string;
  }>;
  teacherStats: {
    totalClasses: number;
    mostClass: string;
    busiestDay: string;
    avgClasses: string;
  };
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
  'update:selectedTeacher': [value: string];
  'refreshTeacherSchedule': [];
  'openAddTeacherCourseModal': [];
  'openEditTeacherCourseModal': [day: string, timeSlot: number];
  'deleteTeacherCourse': [day: string, timeSlot: number];
}>();

const localSelectedTeacher = ref(props.selectedTeacher);
const showDeleteConfirm = ref(false);
const deleteDay = ref('');
const deleteTimeSlot = ref(0);

// 获取当前选中教师的任教班级
const selectedTeacherClasses = computed(() => {
  if (!localSelectedTeacher.value) return [];
  const teacher = props.teachers.find(t => t.teacher_id === localSelectedTeacher.value);
  return teacher?.teachingClasses || [];
});

// 监听 props 变化
watch(() => props.selectedTeacher, (newValue) => {
  localSelectedTeacher.value = newValue;
});

// 处理教师变化
const handleTeacherChange = () => {
  emit('update:selectedTeacher', localSelectedTeacher.value);
};

// 获取指定天和时间段的课程
const getCourse = (day: string, timeSlot: number) => {
  return props.teacherCourses.find(course => course.day === day && course.timeSlot === timeSlot);
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
  if (deleteDay.value && deleteTimeSlot.value) {
    emit('deleteTeacherCourse', deleteDay.value, deleteTimeSlot.value);
    showDeleteConfirm.value = false;
    deleteDay.value = '';
    deleteTimeSlot.value = 0;
  }
};
</script>

<style scoped>
/* 引用共享样式 */
@import '@/styles/course/CourseManage.css';

/* 教师选择器特殊样式 */
.filter-group select {
  min-width: 180px;
}

/* 任教班级显示样式 */
.teacher-classes {
  margin-top: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-sm);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
}

.classes-label {
  font-weight: var(--font-weight-medium);
  margin-right: var(--spacing-xs);
  color: var(--text-secondary);
}

.classes-list {
  color: var(--text-primary);
}

/* 课程内容和操作区域样式 */
.course-item {
}

.course-content {
  cursor: pointer;
  transition: background-color var(--transition-fast);
  padding: var(--spacing-xs);
  border-radius: var(--border-radius-sm);
}

.course-content:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.course-actions {
  margin-top: var(--spacing-xs);
  display: flex;
  justify-content: flex-end;
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