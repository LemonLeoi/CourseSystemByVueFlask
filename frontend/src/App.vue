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
import Notification from '@/components/common/Notification.vue';
import ErrorBoundary from '@/components/common/ErrorBoundary.vue';
import OfflineNotification from '@/components/common/OfflineNotification.vue';
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
