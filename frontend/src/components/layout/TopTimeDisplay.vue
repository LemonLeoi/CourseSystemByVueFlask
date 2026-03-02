<template>
  <div id="current-time" class="time-display"></div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';

let timer: number | undefined;

const updateTime = () => {
  const currentTimeElement = document.getElementById('current-time');
  if (currentTimeElement) {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    currentTimeElement.textContent = timeString;
  }
};

onMounted(() => {
  updateTime();
  timer = window.setInterval(updateTime, 1000);
});

onUnmounted(() => {
  if (timer) {
    clearInterval(timer);
  }
});
</script>

<style scoped>
.time-display {
  position: fixed;
  top: 15px;
  right: 20px;
  background-color: var(--primary-color);
  color: white;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Courier New', Courier, monospace;
  z-index: 999;
}
</style>