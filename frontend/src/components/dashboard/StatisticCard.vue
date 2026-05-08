<template>
  <div class="statistic-card" @click="$emit('click')">
    <h3>{{ title }}</h3>
    <p>{{ value }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  title: string;
  value: string | number;
  icon: string;
}>();

defineEmits<{
  (e: 'click'): void;
}>();
</script>

<style scoped>
.statistic-card {
  background-color: white;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  text-align: center;
  cursor: pointer;
  border: 1px solid #e0e0e0;
}

.statistic-card:hover {
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}

.statistic-card h3 {
  margin: 0;
  font-size: 14px;
  color: #666;
  font-weight: normal;
}

.statistic-card p {
  margin: 10px 0 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
</style>