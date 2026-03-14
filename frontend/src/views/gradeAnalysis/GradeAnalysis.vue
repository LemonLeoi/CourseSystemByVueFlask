<template>
  <Layout activePath="/grade-analysis">
    <BaseManagePage 
      title="成绩分析系统"
      :totalItems="0"
      :showAddButton="false"
    >
      <template #data>
        <div class="grade-analysis">
          <!-- 路由导航选项卡 -->
          <div class="analysis-tabs">
            <router-link 
              to="/grade-analysis/overall" 
              class="analysis-tab"
              active-class="active"
            >
              整体分析
            </router-link>
            <router-link 
              to="/grade-analysis/individual" 
              class="analysis-tab"
              active-class="active"
            >
              个人分析
            </router-link>
            <router-link 
              to="/grade-analysis/class" 
              class="analysis-tab"
              active-class="active"
            >
              班级分析
            </router-link>
            <router-link 
              to="/grade-analysis/grade" 
              class="analysis-tab"
              active-class="active"
            >
              年级分析
            </router-link>
          </div>

          <!-- 子路由内容 -->
          <div class="analysis-content">
            <router-view />
          </div>
        </div>
      </template>
    </BaseManagePage>
  </Layout>
</template>

<script setup lang="ts">
import Layout from '@/components/layout/Layout.vue';
import BaseManagePage from '@/components/business/BaseManagePage.vue';
</script>

<style>
@import '@/styles/common/main.css';

/* 路由导航选项卡样式 */
.analysis-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.analysis-tab {
  padding: 12px 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  border-bottom: 2px solid transparent;
  text-decoration: none;
  transition: all 0.3s ease;
}

.analysis-tab:hover {
  color: #007bff;
}

.analysis-tab.active {
  color: #007bff;
  border-bottom-color: #007bff;
  background-color: rgba(0, 123, 255, 0.05);
}

.analysis-content {
  min-height: 600px;
}
</style>