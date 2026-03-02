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
        <input type="text" v-model="formData.day" disabled>
      </div>
      <div class="form-group">
        <label>节次:</label>
        <input type="text" :value="getSlotName(formData.timeSlot)" disabled>
      </div>
      <div class="form-group">
        <label>课程名称:</label>
        <input type="text" v-model="formData.name" required>
      </div>
      <div class="form-group">
        <label>班级:</label>
        <input type="text" v-model="formData.className" required>
      </div>
      <div class="form-group">
        <label>教室:</label>
        <input type="text" v-model="formData.classroom" required>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from '@/components/business/BaseModal.vue';
import type { TeacherCourse } from '@/types/course';

const props = defineProps<{
  visible: boolean;
  editingCourse: boolean;
  formData: TeacherCourse;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save', formData: TeacherCourse): void;
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
</script>

<style scoped>
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