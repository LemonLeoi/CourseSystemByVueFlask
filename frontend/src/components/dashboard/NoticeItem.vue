<template>
  <div class="notice-item" @click="$emit('click')">
    <span class="notice-date">{{ date }}</span>
    <p class="notice-content">{{ content }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  date: string;
  content: string;
}>();

defineEmits<{
  (e: 'click'): void;
}>();
</script>

<style scoped>
.notice-item {
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s ease;
  cursor: pointer;
}

.notice-item:last-child {
  border-bottom: none;
}

.notice-item:hover {
  background-color: #f9f9f9;
}

.notice-date {
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
  display: block;
}

.notice-content {
  font-size: 14px;
  color: #333;
  margin: 0;
}
</style>