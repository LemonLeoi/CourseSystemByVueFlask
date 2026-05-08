<template>
  <div class="base-manage-page">
    <!-- 页面标题 -->
    <h1>{{ title }}</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section" v-if="showSearch || showFilter">
      <SearchBar 
        v-if="showSearch"
        :placeholder="searchPlaceholder" 
        :button-text="searchButtonText"
        @search="handleSearch"
      />
      <div class="filter-section" v-if="showFilter">
        <slot name="filter"></slot>
      </div>
    </div>
    
    <!-- 数据列表/表格 -->
    <div class="data-container">
      <slot name="data"></slot>
    </div>
    
    <!-- 分页控件 -->
    <Pagination 
      v-if="showPagination"
      :current-page="currentPage || 1"
      :total-items="totalItems"
      :items-per-page="itemsPerPage || 10"
      @pageChange="handlePageChange"
    />
    
    <!-- 添加按钮 -->
    <div v-if="showAddButton" class="action-button-container">
      <button
        class="btn btn-success btn-lg"
        style="position: fixed; bottom: 30px; right: 30px; z-index: var(--z-index-fixed); box-shadow: var(--shadow-md);"
        @click="handleAdd"
      >
        <i class="fa-solid fa-plus"></i> {{ addButtonText }}
      </button>
    </div>
    
    <!-- 模态框 -->
    <slot name="modal"></slot>
  </div>
</template>

<script setup lang="ts">
import SearchBar from './SearchBar.vue';
import Pagination from './Pagination.vue';

const props = defineProps<{
  title: string;
  showSearch?: boolean;
  showFilter?: boolean;
  showPagination?: boolean;
  showAddButton?: boolean;
  searchPlaceholder?: string;
  searchButtonText?: string;
  addButtonText?: string;
  totalItems: number;
  itemsPerPage?: number;
  currentPage?: number;
}>();

const emit = defineEmits<{
  (e: 'search', query: string): void;
  (e: 'pageChange', page: number): void;
  (e: 'add'): void;
}>();

const handleSearch = (query: string) => {
  emit('search', query);
};

const handlePageChange = (page: number) => {
  emit('pageChange', page);
};

const handleAdd = () => {
  emit('add');
};
</script>

<style scoped>
.base-manage-page {
  width: 100%;
}

h1 {
  text-align: left;
  margin-bottom: 20px;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.search-filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-section {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.data-container {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .search-filter-section {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-section {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>