<template>
  <div v-if="hasError" class="error-boundary">
    <h2>发生了错误</h2>
    <p>{{ errorMessage }}</p>
    <button @click="resetError" class="btn btn-primary">
      重新加载
    </button>
  </div>
  <div v-else-if="isReady" class="error-boundary-content">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const hasError = ref(false);
const errorMessage = ref('');
const isReady = ref(false);

const resetError = () => {
  hasError.value = false;
  errorMessage.value = '';
  window.location.reload();
};

onMounted(() => {
  isReady.value = true;
});

window.addEventListener('error', (event) => {
  if (event.error && event.error.message) {
    hasError.value = true;
    errorMessage.value = event.error.message;
  }
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

.error-boundary-content {
  width: 100%;
  height: 100%;
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