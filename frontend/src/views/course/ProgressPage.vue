<template>
  <div class="progress-page">
    <BaseManagePage 
      title="教学进度管理"
      :total-items="0"
      :show-add-button="true"
      :add-button-text="'添加进度'"
      @add="openAddProgressModal"
    >
      <template #data>
        <ProgressTab 
          v-model:progress-subject="progressSubject"
          v-model:progress-grade="progressGrade"
          :teaching-progress="teachingProgress"
          :is-loading="isLoading"
          :error="error"
          :success-message="successMessage"
          @refreshProgress="refreshProgress"
          @openAddProgressModal="openAddProgressModal"
          @editProgress="editProgress"
          @deleteProgress="deleteTeachingProgress"
          @getStatusText="getStatusText"
        />
      </template>
    </BaseManagePage>

    <!-- 教学进度模态框 -->
    <ProgressModal
      :visible="showProgressModal"
      :editing-progress="editingProgress"
      :form-data="progressForm"
      @close="closeProgressModal"
      @save="saveProgress"
    />
  </div>
</template>

<script setup lang="ts">
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import ProgressTab from '@/components/course/ProgressTab.vue';
import ProgressModal from '@/components/course/ProgressModal.vue';
import { useTeachingProgress } from '@/composables/course/useTeachingProgress';

// 使用教学进度composable
const {
  // 状态
  progressSubject,
  progressGrade,
  teachingProgress,
  
  // 模态框状态
  showProgressModal,
  editingProgress,
  progressForm,
  
  // 操作状态
  isLoading,
  error,
  successMessage,
  
  // 方法
  refreshProgress,
  openAddProgressModal,
  editProgress,
  deleteTeachingProgress,
  closeProgressModal,
  saveProgress,
  getStatusText
} = useTeachingProgress();
</script>

<style scoped>
.progress-page {
  padding: 20px;
}
</style>