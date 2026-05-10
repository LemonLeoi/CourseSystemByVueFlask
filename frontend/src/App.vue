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
import { onMounted } from 'vue';
import Notification from '@/components/common/Notification.vue';
import ErrorBoundary from '@/components/common/ErrorBoundary.vue';
import OfflineNotification from '@/components/common/OfflineNotification.vue';
import { clearAllApiCache } from '@/services/api/apiService';

// Clear API cache when the app starts.
onMounted(async () => {
  try {
    await clearAllApiCache();
    console.log('API cache cleared');
  } catch (error) {
    console.warn('Failed to clear API cache:', error);
  }
});
</script>

<style>
/* Global reset */
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
