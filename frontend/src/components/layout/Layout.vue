<template>
  <div class="layout">
    <Sidebar :menuItems="menuItems" @toggle="handleSidebarToggle" />
    <main class="main-content" :class="{ expanded: sidebarCollapsed }">
      <TopTimeDisplay />
      <slot></slot>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import Sidebar from './Sidebar.vue';
import TopTimeDisplay from './TopTimeDisplay.vue';
import { useLayout } from '@/composables/layout/useLayout';

const props = defineProps<{
  activePath?: string;
}>();

const { sidebarCollapsed, handleSidebarToggle, createMenuItems } = useLayout();
const menuItems = computed(() => createMenuItems(props.activePath || '/'));
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 220px;
  padding: 30px;
  transition: margin-left 0.3s ease;
  min-height: 100vh;
  background-color: #f5f7fa;
  flex: 1;
}

.main-content.expanded {
  margin-left: 60px;
}

/* 响应式断点 */
@media (max-width: 1200px) {
  .main-content {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    padding: 15px;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 10px;
  }
}
</style>