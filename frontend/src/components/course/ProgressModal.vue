<template>
  <BaseModal 
    :visible="visible"
    :title="editingProgress ? '编辑进度' : '添加进度'"
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
        <label>章节:</label>
        <input type="text" v-model="formData.chapter" required>
      </div>
      <div class="form-group">
        <label>课时:</label>
        <input type="number" v-model.number="formData.hours" min="1" required>
      </div>
      <div class="form-group">
        <label>教学目标:</label>
        <textarea v-model="formData.objective" rows="3" required></textarea>
      </div>
      <div class="form-group">
        <label>进度:</label>
        <div class="progress-input">
          <input type="range" v-model.number="formData.progress" min="0" max="100" step="1">
          <span>{{ formData.progress }}%</span>
        </div>
      </div>
      <div class="form-group">
        <label>状态:</label>
        <select v-model="formData.status">
          <option value="not-started">未开始</option>
          <option value="in-progress">进行中</option>
          <option value="completed">已完成</option>
        </select>
      </div>
    </form>
  </BaseModal>
</template>

<script setup lang="ts">
import BaseModal from '@/components/business/BaseModal.vue';
import type { TeachingProgress } from '@/types/course';

const props = defineProps<{
  visible: boolean;
  editingProgress: boolean;
  formData: TeachingProgress;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save', formData: TeachingProgress): void;
}>();
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
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

/* 进度条样式 */
.progress-input {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-input input[type="range"] {
  flex: 1;
}

.progress-input span {
  min-width: 50px;
  text-align: right;
  font-weight: 500;
}
</style>