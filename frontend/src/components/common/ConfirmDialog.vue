<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="confirm-dialog-overlay" @click.self="handleCancel">
        <div class="confirm-dialog">
          <div class="confirm-dialog-header">
            <div class="dialog-icon" :class="iconClass">
              <i :class="icon"></i>
            </div>
            <h3>{{ title }}</h3>
            <button class="dialog-close" @click="handleCancel">&times;</button>
          </div>
          <div class="confirm-dialog-body">
            <p v-if="message">{{ message }}</p>
            <div v-if="details" class="dialog-details">
              <div v-for="(value, key) in details" :key="key" class="detail-row">
                <span class="detail-label">{{ key }}</span>
                <span class="detail-value">{{ value }}</span>
              </div>
            </div>
            <p v-if="warning" class="dialog-warning">{{ warning }}</p>
          </div>
          <div class="confirm-dialog-footer">
            <button class="btn btn-secondary" @click="handleCancel">{{ cancelText }}</button>
            <button 
              class="btn btn-danger" 
              @click="handleConfirm"
              :disabled="loading"
            >
              <span v-if="loading" class="loading-spinner"></span>
              <span v-else>{{ confirmText }}</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  visible: boolean;
  title?: string;
  message?: string;
  details?: Record<string, any>;
  warning?: string;
  type?: 'warning' | 'error' | 'info';
  confirmText?: string;
  cancelText?: string;
  loading?: boolean;
}>(), {
  title: '确认操作',
  message: '',
  warning: '此操作不可撤销，请谨慎操作。',
  type: 'warning',
  confirmText: '确认',
  cancelText: '取消',
  loading: false
});

const emit = defineEmits<{
  (e: 'confirm'): void;
  (e: 'cancel'): void;
}>();

const icon = computed(() => {
  switch (props.type) {
    case 'error':
      return 'fa-solid fa-exclamation-circle';
    case 'info':
      return 'fa-solid fa-info-circle';
    default:
      return 'fa-solid fa-exclamation-triangle';
  }
});

const iconClass = computed(() => {
  switch (props.type) {
    case 'error':
      return 'icon-error';
    case 'info':
      return 'icon-info';
    default:
      return 'icon-warning';
  }
});

const handleConfirm = () => {
  emit('confirm');
};

const handleCancel = () => {
  emit('cancel');
};
</script>

<style scoped>
.confirm-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-index-modal);
  backdrop-filter: blur(2px);
}

.confirm-dialog {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 420px;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

.confirm-dialog-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  position: relative;
}

.dialog-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.icon-warning {
  background-color: rgba(255, 152, 0, 0.1);
  color: var(--warning-color);
}

.icon-error {
  background-color: rgba(244, 67, 54, 0.1);
  color: var(--error-color);
}

.icon-info {
  background-color: rgba(33, 150, 243, 0.1);
  color: var(--info-color);
}

.confirm-dialog-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  flex: 1;
}

.dialog-close {
  background: none;
  border: none;
  font-size: var(--font-size-xl);
  cursor: pointer;
  color: var(--text-secondary);
  transition: color var(--transition-fast);
  padding: 0;
  line-height: 1;
}

.dialog-close:hover {
  color: var(--text-primary);
}

.confirm-dialog-body {
  padding: var(--spacing-lg);
}

.confirm-dialog-body p {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-secondary);
  line-height: 1.6;
}

.dialog-details {
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-xs) 0;
  border-bottom: 1px solid var(--border-light);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: var(--font-weight-medium);
  color: var(--text-secondary);
}

.detail-value {
  color: var(--text-primary);
  font-weight: var(--font-weight-normal);
}

.dialog-warning {
  background-color: rgba(255, 152, 0, 0.1);
  border-left: 4px solid var(--warning-color);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 0 var(--border-radius-sm) var(--border-radius-sm) 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.confirm-dialog-footer {
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}

.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--bg-tertiary);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background-color: var(--border-color);
}

.btn-danger {
  background-color: var(--error-color);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #d32f2f;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  vertical-align: middle;
  margin-right: 4px;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>