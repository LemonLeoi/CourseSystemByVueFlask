<template>
  <div 
    v-if="!isOnline" 
    class="offline-notification"
  >
    <div class="offline-notification-content">
      <span class="offline-icon">📶</span>
      <span class="offline-message">您当前处于离线状态，部分功能可能无法正常使用</span>
    </div>
  </div>
  <div 
    v-else-if="showOnlineNotification" 
    class="online-notification"
  >
    <div class="online-notification-content">
      <span class="online-icon">✅</span>
      <span class="online-message">网络已恢复，正在同步数据...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { offlineStorageService } from '@/services/data/offlineStorageService';
import notificationService from '@/services/ui/uiNotificationService';
import { fetchApi } from '@/services/api/apiService';

// 网络状态
const isOnline = ref(navigator.onLine);
// 是否显示在线通知
const showOnlineNotification = ref(false);

// 同步数据
async function syncData() {
  try {
    // 获取待同步的数据
    const syncQueue = await offlineStorageService.getSyncQueue();
    
    if (syncQueue.length === 0) {
      return;
    }
    
    // 遍历同步数据并发送请求
    for (const item of syncQueue) {
      await fetchApi(item.url, {
        method: item.method,
        body: JSON.stringify(item.data)
      });
    }
    
    // 清空已同步的数据
    await offlineStorageService.clearSyncQueue();
    
    // 显示同步完成通知
    notificationService.success('数据同步完成');
  } catch (error) {
    console.error('数据同步失败:', error);
    notificationService.error('数据同步失败，请稍后重试');
  }
}

// 处理网络状态变化
const handleOnline = () => {
  isOnline.value = true;
  showOnlineNotification.value = true;
  
  // 触发数据同步
  syncData();
  
  // 3秒后隐藏在线通知
  setTimeout(() => {
    showOnlineNotification.value = false;
  }, 3000);
};

const handleOffline = () => {
  isOnline.value = false;
};

// 组件挂载时添加事件监听
onMounted(() => {
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('online', handleOnline);
  window.removeEventListener('offline', handleOffline);
});
</script>

<style scoped>
.offline-notification {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  text-align: center;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.3s ease-out;
}

.online-notification {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: #d4edda;
  color: #155724;
  padding: 10px;
  text-align: center;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  animation: slideDown 0.3s ease-out;
}

.offline-notification-content,
.online-notification-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  max-width: 1200px;
  margin: 0 auto;
}

.offline-icon,
.online-icon {
  font-size: 18px;
}

.offline-message,
.online-message {
  font-size: 14px;
  font-weight: 500;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
