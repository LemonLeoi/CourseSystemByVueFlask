<template>
  <div class="collapsible-section">
    <div class="section-header" @click="toggleCollapse">
      <h4>{{ title }}</h4>
      <div class="header-right">
        <div class="info-icon" v-if="icon">{{ icon }}</div>
        <i class="fa-solid" :class="isCollapsed ? 'fa-chevron-down' : 'fa-chevron-up'"></i>
      </div>
    </div>
    <div class="section-content" :class="{ collapsed: isCollapsed }">
      <slot></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const props = defineProps<{
  title: string;
  icon?: string;
  defaultCollapsed?: boolean;
  storageKey?: string;
}>();

const isCollapsed = ref(props.defaultCollapsed || false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  
  // 存储状态到localStorage
  if (props.storageKey) {
    localStorage.setItem(`collapsible_${props.storageKey}`, isCollapsed.value.toString());
  }
};

// 从localStorage加载状态
onMounted(() => {
  if (props.storageKey) {
    const savedState = localStorage.getItem(`collapsible_${props.storageKey}`);
    if (savedState !== null) {
      isCollapsed.value = savedState === 'true';
    }
  }
});
</script>

<style scoped>
.collapsible-section {
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
}

.collapsible-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
  border-radius: 8px 8px 0 0;
  background: linear-gradient(135deg, #f9f9f9 0%, #f0f0f0 100%);
  position: relative;
}

.section-header:hover {
  background: linear-gradient(135deg, #f0f0f0 0%, #e6e6e6 100%);
  background-color: rgba(0, 123, 255, 0.05);
}

.section-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 3px;
  background: #409eff;
  transition: width 0.3s ease;
}

.section-header:hover::after {
  width: 100%;
}

.section-header h4 {
  margin: 0;
  color: #333;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.info-icon {
  font-size: 20px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.section-header:hover .info-icon {
  opacity: 1;
}

.section-header i {
  color: #666;
  transition: all 0.3s ease;
  font-size: 14px;
  padding: 4px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
}

.section-header:hover i {
  color: #409eff;
  background: rgba(64, 158, 255, 0.1);
  transform: scale(1.1);
}

.section-content {
  padding: 20px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  max-height: 2000px;
  opacity: 1;
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
}

.section-content.collapsed {
  padding: 0;
  max-height: 0;
  opacity: 0;
  border-top: none;
}

/* 加载动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-content {
  animation: fadeInUp 0.5s ease-out;
}

@media (max-width: 768px) {
  .section-header {
    padding: 12px 16px;
  }
  
  .section-header h4 {
    font-size: 14px;
  }
  
  .section-content {
    padding: 16px;
  }
  
  .info-icon {
    font-size: 18px;
  }
  
  .section-header i {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .section-header {
    padding: 10px 12px;
  }
  
  .section-header h4 {
    font-size: 13px;
  }
  
  .section-content {
    padding: 12px;
  }
  
  .info-icon {
    font-size: 16px;
  }
}
</style>