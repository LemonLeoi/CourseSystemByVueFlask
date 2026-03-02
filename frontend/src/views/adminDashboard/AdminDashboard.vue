<template>
  <Layout activePath="/admin">
    <div class="admin-dashboard">
      <!-- 页面标题和搜索栏 -->
      <div class="header-section">
        <h1>教务管理</h1>
        <div class="search-section">
          <input 
            type="text" 
            placeholder="搜索考试通知" 
            v-model="searchQuery" 
            class="search-input"
            @keyup.enter="handleSearch"
            :disabled="isLoading"
          >
          <button @click="handleSearch" class="search-button" :disabled="isLoading">
            <i class="fa-solid fa-magnifying-glass"></i> 搜索
          </button>
          <button @click="refreshData" class="refresh-button" :disabled="isLoading">
            <i class="fa-solid fa-refresh"></i> 刷新
          </button>
        </div>
      </div>
      
      <!-- 错误提示 -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-overlay">
        <div class="loading-spinner">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <p>加载中...</p>
        </div>
      </div>
      
      <!-- 统计数据展示 -->
      <div class="statistic-section">
        <div 
          v-for="stat in statistics" 
          :key="stat.title"
          class="statistic-card"
        >
          <i :class="stat.icon"></i>
          <h3>{{ stat.title }}</h3>
          <p>{{ stat.value }}</p>
        </div>
      </div>
      
      <!-- 考试安排通知 -->
      <h3 class="section-title">考试安排通知</h3>
      <div class="notice-container">
        <div 
          v-for="notice in paginatedNotices" 
          :key="notice.date + notice.content"
          class="notice-item"
        >
          <span class="notice-date">{{ notice.date }}</span>
          <p class="notice-content">{{ notice.content }}</p>
        </div>
      </div>
      
      <!-- 分页控件 -->
      <div class="pagination" v-if="totalPages > 1">
        <button 
          @click="handlePageChange(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-button"
        >
          <i class="fa-solid fa-angle-left"></i>
        </button>
        
        <button 
          v-for="page in totalPages" 
          :key="page"
          @click="handlePageChange(page)"
          :class="['pagination-button', { active: currentPage === page }]"
        >
          {{ page }}
        </button>
        
        <button 
          @click="handlePageChange(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-button"
        >
          <i class="fa-solid fa-angle-right"></i>
        </button>
      </div>
      
      <!-- 待办事项列表 -->
      <div class="todo-list">
        <h3 class="section-title">待办事项</h3>
        <ul>
          <li v-for="(todo, index) in todos" :key="index">
            <i class="fa-solid fa-clipboard-check"></i> {{ todo }}
          </li>
        </ul>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
/**
 * AdminDashboard.vue
 * 教务管理系统首页
 * 功能：展示统计数据、考试通知、待办事项，支持搜索和分页
 */

import { ref, computed, onMounted } from 'vue';
import Layout from '@/components/layout/Layout.vue';
import notificationService from '@/services/ui/uiNotificationService';

/**
 * 类型定义
 */
interface Statistic {
  title: string;
  value: number;
  icon: string;
}

interface Notice {
  date: string;
  content: string;
}

/**
 * 状态管理
 */
const statistics = ref<Statistic[]>([
  { title: '学生总数', value: 0, icon: 'fa-solid fa-users' },
  { title: '教师总数', value: 0, icon: 'fa-solid fa-chalkboard-user' },
  { title: '课程总数', value: 0, icon: 'fa-solid fa-book-open' },
  { title: '近期考试数量', value: 0, icon: 'fa-solid fa-file-invoice' }
]);

const allNotices = ref<Notice[]>([]);
const todos = ref<string[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

/**
 * 从后端API获取统计数据
 */
const fetchStatistics = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    
    const response = await fetch('/api/admin/dashboard/statistics');
    if (!response.ok) {
      throw new Error('获取统计数据失败');
    }
    
    const data = await response.json();
    statistics.value = data;
  } catch (err) {
    console.error('获取统计数据失败:', err);
    error.value = '获取统计数据失败，请稍后重试';
    notificationService.error('获取统计数据失败');
  } finally {
    isLoading.value = false;
  }
};

/**
 * 从后端API获取通知数据
 */
const fetchNotifications = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    
    const response = await fetch('/api/admin/dashboard/notifications');
    if (!response.ok) {
      throw new Error('获取通知数据失败');
    }
    
    const data = await response.json();
    allNotices.value = data;
  } catch (err) {
    console.error('获取通知数据失败:', err);
    error.value = '获取通知数据失败，请稍后重试';
    notificationService.error('获取通知数据失败');
    // 使用默认通知数据
    allNotices.value = [
      { date: "2025-05-01", content: "测验：历史科目安排" },
      { date: "2025-04-30", content: "测试：地理科目安排" },
      { date: "2025-04-29", content: "考试：历史科目安排" }
    ];
  } finally {
    isLoading.value = false;
  }
};

/**
 * 从后端API获取待办事项
 */
const fetchTodos = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    
    const response = await fetch('/api/admin/dashboard/todos');
    if (!response.ok) {
      throw new Error('获取待办事项失败');
    }
    
    const data = await response.json();
    todos.value = data;
  } catch (err) {
    console.error('获取待办事项失败:', err);
    error.value = '获取待办事项失败，请稍后重试';
    notificationService.error('获取待办事项失败');
    // 使用默认待办事项
    todos.value = [
      "审批学生请假申请",
      "审核教师课程申请"
    ];
  } finally {
    isLoading.value = false;
  }
};

/**
 * 初始化数据
 * 组件挂载时调用，确保数据正确加载
 */
onMounted(async () => {
  await Promise.all([
    fetchStatistics(),
    fetchNotifications(),
    fetchTodos()
  ]);
});

/**
 * 搜索相关
 * searchQuery: 搜索关键词
 * filteredNotices: 过滤后的通知列表
 */
const searchQuery = ref('');
const filteredNotices = computed(() => {
  if (!searchQuery.value) {
    return allNotices.value;
  }
  const query = searchQuery.value.toLowerCase();
  return allNotices.value.filter(notice => 
    notice.content.toLowerCase().includes(query) || 
    notice.date.includes(query)
  );
});

/**
 * 处理搜索事件
 * 重置分页到第一页，确保搜索结果从第一页开始显示
 */
const handleSearch = () => {
  currentPage.value = 1;
};

/**
 * 分页相关
 * currentPage: 当前页码
 * noticesPerPage: 每页显示的通知数量
 * totalPages: 总页数
 * paginatedNotices: 分页后的通知列表
 */
const currentPage = ref(1);
const noticesPerPage = 5;
const totalPages = computed(() => {
  return Math.ceil(filteredNotices.value.length / noticesPerPage);
});

const paginatedNotices = computed(() => {
  const startIndex = (currentPage.value - 1) * noticesPerPage;
  const endIndex = startIndex + noticesPerPage;
  return filteredNotices.value.slice(startIndex, endIndex);
});

/**
 * 处理分页变更
 * @param page 目标页码
 */
const handlePageChange = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

/**
 * 刷新数据
 */
const refreshData = async () => {
  await Promise.all([
    fetchStatistics(),
    fetchNotifications(),
    fetchTodos()
  ]);
  notificationService.success('数据刷新成功');
};
</script>

<style>
/* 引入外部样式文件 */
@import '../../styles/adminDashboard/AdminDashboard.css';
</style>