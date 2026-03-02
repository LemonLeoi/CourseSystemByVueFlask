<template>
  <div class="pagination" v-if="totalPages > 1">
    <button 
      @click="handlePrev" 
      :disabled="currentPage === 1"
    >
      <i class="fa-solid fa-angle-left"></i>
    </button>
    
    <button 
      v-for="page in totalPages" 
      :key="page"
      @click="handlePageChange(page)"
      :class="{ active: currentPage === page }"
    >
      {{ page }}
    </button>
    
    <button 
      @click="handleNext" 
      :disabled="currentPage === totalPages"
    >
      <i class="fa-solid fa-angle-right"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  currentPage: number;
  totalItems: number;
  itemsPerPage: number;
}>();

const emit = defineEmits<{
  (e: 'pageChange', page: number): void;
}>();

const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.itemsPerPage);
});

const handlePageChange = (page: number) => {
  emit('pageChange', page);
};

const handlePrev = () => {
  if (props.currentPage > 1) {
    emit('pageChange', props.currentPage - 1);
  }
};

const handleNext = () => {
  if (props.currentPage < totalPages.value) {
    emit('pageChange', props.currentPage + 1);
  }
};
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  margin: 0 5px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button:hover:not(:disabled) {
  background-color: #f0f0f0;
}

.pagination button.active {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>