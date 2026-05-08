<template>
  <ErrorBoundary>
    <div class="app">
      <OfflineNotification />
      <router-view />
      <Notification />
    </div>
  </ErrorBoundary>
</template>

<script setup lang="ts">
// App.vue - 主应用组件
import { onMounted } from 'vue';
import Notification from '@/components/common/Notification.vue';
import ErrorBoundary from '@/components/common/ErrorBoundary.vue';
import OfflineNotification from '@/components/common/OfflineNotification.vue';
import { clearAllApiCache } from '@/services/api/apiService';

// 应用启动时清除所有API缓存
onMounted(async () => {
  try {
    await clearAllApiCache();
    console.log('API缓存已清除');
  } catch (error) {
    console.warn('清除缓存失败:', error);
  }
});
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}
</style>
