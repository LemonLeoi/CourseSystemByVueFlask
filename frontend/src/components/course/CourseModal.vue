<template>
  <BaseModal 
    :visible="visible"
    :title="editingCourse ? '编辑课程' : '添加课程'"
    :showFooter="true"
    :showCancelButton="true"
    :showSaveButton="true"
    :cancelButtonText="'取消'"
    :saveButtonText="'确定修改'"
    @close="$emit('close')"
    @save="$emit('save', formData)"
  >
    <form @submit.prevent="$emit('save', formData)">
      <div class="form-group">
        <label>星期:</label>
        <select v-model="formData.day" required>
          <option value="">请选择星期</option>
          <option value="星期一">星期一</option>
          <option value="星期二">星期二</option>
          <option value="星期三">星期三</option>
          <option value="星期四">星期四</option>
          <option value="星期五">星期五</option>
          <option value="星期六">星期六</option>
          <option value="星期日">星期日</option>
        </select>
      </div>
      <div class="form-group">
        <label>节次:</label>
        <select v-model="formData.timeSlot" required>
          <option value="">请选择节次</option>
          <option value="1">第一节</option>
          <option value="2">第二节</option>
          <option value="3">第三节</option>
          <option value="4">第四节</option>
          <option value="5">第五节</option>
          <option value="6">第六节</option>
          <option value="7">第七节</option>
          <option value="8">第八节</option>
        </select>
      </div>
      <div class="form-group">
        <label>课程名称:</label>
        <select v-model="(formData as any).course_id" required>
          <option value="">请选择课程</option>
          <option v-for="course in courses" :key="course.id" :value="course.id">
            {{ course.course_name }} ({{ course.course_code }})
          </option>
        </select>
      </div>
      
      <!-- 学生课程特有字段：教师选择 -->
      <div v-if="type === 'student'" class="form-group">
        <label>任课教师:</label>
        <select v-model="(formData as any).teacher" required>
          <option value="">请选择教师</option>
          <option v-for="teacher in teachers" :key="teacher.teacher_id || teacher.id" :value="teacher.teacher_id || teacher.id">
            {{ teacher.teacher_id || teacher.id }} - {{ teacher.name }} ({{ teacher.subject || teacher.department }})
          </option>
        </select>
      </div>
      
      <!-- 教师详细信息显示 -->
      <div v-if="type === 'student' && selectedTeacher" class="teacher-info">
        <h4>教师信息</h4>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">姓名:</span>
            <span class="info-value">{{ selectedTeacher.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">性别:</span>
            <span class="info-value">{{ selectedTeacher.gender }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">学科:</span>
            <span class="info-value">{{ selectedTeacher.subject || selectedTeacher.department }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">职称:</span>
            <span class="info-value">{{ selectedTeacher.title }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">联系方式:</span>
            <span class="info-value">{{ selectedTeacher.contact }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">任教班级:</span>
            <span class="info-value">{{ selectedTeacher.teachingClasses && Array.isArray(selectedTeacher.teachingClasses) ? selectedTeacher.teachingClasses.join(', ') : '无' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">是否班主任:</span>
            <span class="info-value">{{ selectedTeacher.isHomeroomTeacher ? '是' : '否' }}</span>
          </div>
          <div v-if="selectedTeacher.isHomeroomTeacher" class="info-item">
            <span class="info-label">班主任班级:</span>
            <span class="info-value">{{ selectedTeacher.homeroomClass }}</span>
          </div>
        </div>
      </div>
      
      <!-- 教师课程特有字段：班级 -->
      <div v-if="type === 'teacher'" class="form-group">
        <label>班级:</label>
        <select v-model="(formData as any).className" required>
          <option value="">请选择班级</option>
          <option v-for="className in classes" :key="className" :value="className">
            {{ className }}
          </option>
        </select>
      </div>
      
      <!-- 教室选择 - 只在教师课程中显示 -->
      <div v-if="type === 'teacher'" class="form-group">
        <label>教室:</label>
        <select v-model="(formData as any).room_id" required>
          <option value="">请选择教室</option>
          <option v-for="room in classrooms" :key="room.room_id" :value="room.room_id">
            {{ room.room_id }} ({{ room.grade }}{{ room.class }})
          </option>
        </select>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import BaseModal from '@/components/business/BaseModal.vue';
import type { StudentCourse, TeacherCourse } from '@/types/course';
import type { Teacher } from '@/types';

const props = defineProps<{
  visible: boolean;
  editingCourse: boolean;
  formData: StudentCourse | TeacherCourse;
  type: 'student' | 'teacher';
  teachers?: Teacher[];
  courses?: Array<{
    id: number;
    course_name: string;
    course_code: string;
  }>;
  classrooms?: Array<{
    room_id: string;
    grade: string;
    class: string;
    building: string;
    room_number: number;
  }>;
  classes?: Array<string>;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save', formData: StudentCourse | TeacherCourse): void;
}>();

// 获取节次名称
const getSlotName = (slot: number): string => {
  const slotMap: Record<number, string> = {
    1: '第一节',
    2: '第二节',
    3: '第三节',
    4: '第四节',
    5: '第五节',
    6: '第六节',
    7: '第七节',
    8: '第八节'
  };
  return slotMap[slot] || `第${slot}节`;
};

// 获取选中的教师信息
const selectedTeacher = computed(() => {
  if (props.type === 'student' && props.teachers) {
    return props.teachers.find(teacher => teacher.teacher_id === (props.formData as StudentCourse).teacher) || null;
  }
  return null;
});
</script>

<style scoped>
/* 教师信息显示样式 */
.teacher-info {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.teacher-info h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-label {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
}

.info-value {
  font-size: 0.9rem;
  color: #333;
}

/* 表单样式 */
.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}
</style>