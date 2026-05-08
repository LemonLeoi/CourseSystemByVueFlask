<template>
  <div class="search-section">
    <input 
      type="text" 
      :placeholder="placeholder" 
      v-model="searchValue" 
      class="search-input"
      @keyup.enter="handleSearch"
    />
    <button @click="handleSearch" class="btn btn-primary">
      <i class="fa-solid fa-magnifying-glass"></i> {{ buttonText }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  placeholder?: string;
  buttonText?: string;
}>();

const emit = defineEmits<{
  (e: 'search', value: string): void;
}>();

const searchValue = ref('');

const handleSearch = () => {
  emit('search', searchValue.value);
};
</script>

<style scoped>
.search-section {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  background: white;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.search-input {
  flex: 1;
  max-width: 400px;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.2);
  outline: none;
}


</style>