<template>
  <div class="notification-container">
    <div 
      v-for="notification in notifications" 
      :key="notification.id"
      :class="['notification', `notification-${notification.type}`]"
    >
      <div class="notification-content">
        {{ notification.message }}
      </div>
      <button 
        class="notification-close"
        @click="removeNotification(notification.id)"
      >
        ×
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import notificationService, { type Notification } from '@/services/ui/uiNotificationService';

const notifications = ref<Notification[]>([]);

const updateNotifications = (newNotifications: Notification[]) => {
  notifications.value = newNotifications;
};

onMounted(() => {
  notifications.value = notificationService.getNotifications();
  notificationService.addListener(updateNotifications);
});

onUnmounted(() => {
  // 监听器会在返回的函数中自动移除
});

const removeNotification = (id: string) => {
  notificationService.removeNotification(id);
};
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}

.notification {
  padding: 12px 16px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: slideIn 0.3s ease-out;
}

.notification-success {
  background-color: #f0f9eb;
  border-left: 4px solid #67c23a;
  color: #67c23a;
}

.notification-error {
  background-color: #fef0f0;
  border-left: 4px solid #f56c6c;
  color: #f56c6c;
}

.notification-warning {
  background-color: #fdf6ec;
  border-left: 4px solid #e6a23c;
  color: #e6a23c;
}

.notification-info {
  background-color: #ecf5ff;
  border-left: 4px solid #409eff;
  color: #409eff;
}

.notification-content {
  flex: 1;
  margin-right: 10px;
}

.notification-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.notification-close:hover {
  opacity: 1;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>