<template>
  <li class="todo-item">
    <i class="fa-solid fa-clipboard-check"></i>
    <span>{{ content }}</span>
  </li>
</template>

<script setup lang="ts">
const props = defineProps<{
  content: string;
}>();
</script>

<style scoped>
.todo-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-item:hover {
  background-color: #f9f9f9;
}

.todo-item i {
  margin-right: 10px;
  color: var(--primary-color);
}

.todo-item span {
  font-size: 14px;
  color: #333;
}
</style>