<template>
  <div v-if="hasError" class="error-boundary">
    <h2>发生了错误</h2>
    <p>{{ errorMessage }}</p>
    <button @click="resetError" class="btn btn-primary">
      重新加载
    </button>
  </div>
  <slot v-else></slot>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';

const hasError = ref(false);
const errorMessage = ref('');

const resetError = () => {
  hasError.value = false;
  errorMessage.value = '';
  // 触发组件重新渲染
  window.location.reload();
};

onErrorCaptured((error, instance, info) => {
  hasError.value = true;
  errorMessage.value = error instanceof Error ? error.message : '未知错误';
  console.error('组件错误:', error);
  console.error('错误信息:', info);
  return false; // 阻止错误继续向上传播
});
</script>

<style scoped>
.error-boundary {
  padding: 40px;
  text-align: center;
  background-color: #fef0f0;
  border: 1px solid #f56c6c;
  border-radius: 4px;
  margin: 20px;
}

.error-boundary h2 {
  color: #f56c6c;
  margin-bottom: 16px;
}

.error-boundary p {
  margin-bottom: 24px;
  color: #606266;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #409eff;
  color: white;
}

.btn-primary:hover {
  background-color: #66b1ff;
}
</style>