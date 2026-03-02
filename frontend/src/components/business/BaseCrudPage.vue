<template>
  <div class="base-crud-page">
    <!-- 页面标题 -->
    <h1>{{ title }}</h1>
    
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section" v-if="showSearch || showFilter">
      <SearchBar 
        v-if="showSearch"
        :placeholder="searchPlaceholder" 
        :buttonText="searchButtonText"
        @search="handleSearch"
      />
      <div class="filter-section" v-if="showFilter">
        <slot name="filter"></slot>
      </div>
    </div>
    
    <!-- 数据操作工具栏 -->
    <div class="toolbar" v-if="showToolbar">
      <slot name="toolbar"></slot>
    </div>
    
    <!-- 数据列表/表格 -->
    <div class="data-container">
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>{{ loadingText }}</p>
      </div>
      <div v-else-if="error" class="error-state">
        <p class="error-message">{{ error }}</p>
        <button class="btn-retry" @click="handleRetry">重试</button>
      </div>
      <div v-else-if="emptyState" class="empty-state">
        <p>{{ emptyText }}</p>
        <button v-if="showAddButton" class="btn-add" @click="handleAdd">
          <i class="fa-solid fa-plus"></i> {{ addButtonText }}
        </button>
      </div>
      <slot name="data"></slot>
    </div>
    
    <!-- 分页控件 -->
    <Pagination 
      v-if="showPagination && !loading && !error && !emptyState"
      :currentPage="currentPage"
      :totalItems="totalItems"
      :itemsPerPage="itemsPerPage || 10"
      @pageChange="handlePageChange"
    />
    
    <!-- 添加按钮 -->
    <button 
      v-if="showAddButton && !emptyState"
      class="btn-add"
      @click="handleAdd"
    >
      <i class="fa-solid fa-plus"></i> {{ addButtonText }}
    </button>
    
    <!-- 操作确认对话框 -->
    <div v-if="confirmDialog.visible" class="confirm-dialog-overlay">
      <div class="confirm-dialog">
        <h3>{{ confirmDialog.title }}</h3>
        <p>{{ confirmDialog.message }}</p>
        <div class="confirm-dialog-buttons">
          <button class="btn-cancel" @click="confirmDialog.visible = false">取消</button>
          <button class="btn-confirm" @click="handleConfirm">确认</button>
        </div>
      </div>
    </div>
    
    <!-- 模态框 -->
    <slot name="modal"></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import SearchBar from './SearchBar.vue';
import Pagination from './Pagination.vue';

const props = defineProps<{
  title: string;
  showSearch?: boolean;
  showFilter?: boolean;
  showToolbar?: boolean;
  showPagination?: boolean;
  showAddButton?: boolean;
  searchPlaceholder?: string;
  searchButtonText?: string;
  addButtonText?: string;
  loadingText?: string;
  emptyText?: string;
  totalItems: number;
  itemsPerPage?: number;
  currentPage: number;
  loading?: boolean;
  error?: string | null;
  items?: any[];
}>();

const emit = defineEmits<{
  (e: 'search', query: string): void;
  (e: 'pageChange', page: number): void;
  (e: 'add'): void;
  (e: 'edit', item: any): void;
  (e: 'delete', item: any): void;
  (e: 'retry'): void;
  (e: 'confirm'): void;
}>();


const confirmDialog = reactive({
  visible: false,
  title: '',
  message: '',
  callback: null as (() => void) | null
});

const emptyState = computed(() => {
  return props.items && props.items.length === 0;
});

const handleSearch = (query: string) => {
  currentPage.value = 1;
  emit('search', query);
};

const handlePageChange = (page: number) => {
  emit('pageChange', page);
};

const handleAdd = () => {
  emit('add');
};

const handleRetry = () => {
  emit('retry');
};

const handleConfirm = () => {
  if (confirmDialog.callback) {
    confirmDialog.callback();
  }
  confirmDialog.visible = false;
  confirmDialog.callback = null;
  emit('confirm');
};

const showConfirmDialog = (title: string, message: string, callback: () => void) => {
  confirmDialog.title = title;
  confirmDialog.message = message;
  confirmDialog.callback = callback;
  confirmDialog.visible = true;
};

const handleEdit = (item: any) => {
  emit('edit', item);
};

const handleDelete = (item: any) => {
  showConfirmDialog('删除确认', `确定要删除 ${item.name || item.id} 吗？`, () => {
    emit('delete', item);
  });
};

defineExpose({
  showConfirmDialog,
  handleEdit,
  handleDelete,
  currentPage
});
</script>

<style scoped>
.base-crud-page {
  width: 100%;
}
</style>