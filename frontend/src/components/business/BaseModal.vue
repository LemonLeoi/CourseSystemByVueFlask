<template>
  <div v-if="visible" class="modal-overlay" @click="handleOverlayClick">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ title }}</h2>
        <button class="modal-close" @click="handleClose">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <slot></slot>
      </div>
      <div class="modal-footer" v-if="showFooter">
        <button 
          v-if="showCancelButton"
          class="btn btn-secondary" 
          @click="handleClose"
        >
          {{ cancelButtonText }}
        </button>
        <button 
          v-if="showSaveButton"
          class="btn btn-success" 
          @click="handleSave"
        >
          {{ saveButtonText }}
        </button>
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  visible: boolean;
  title: string;
  showFooter?: boolean;
  showCancelButton?: boolean;
  showSaveButton?: boolean;
  cancelButtonText?: string;
  saveButtonText?: string;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'save'): void;
  (e: 'overlayClick'): void;
}>();

const handleClose = () => {
  emit('close');
};

const handleSave = () => {
  emit('save');
};

const handleOverlayClick = () => {
  emit('overlayClick');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f8f9fa;
  border-radius: 8px 8px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.3s;
}

.modal-close:hover {
  background-color: #e9ecef;
  color: #333;
}

.modal-body {
  padding: 20px;
  flex: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #e0e0e0;
  background-color: #f8f9fa;
  border-radius: 0 0 8px 8px;
}



@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 20px;
  }
}
</style>