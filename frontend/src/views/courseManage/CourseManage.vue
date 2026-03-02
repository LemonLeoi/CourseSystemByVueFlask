<template>
  <Layout activePath="/courses">
    <BaseManagePage 
      title="课程管理"
      :totalItems="0"
      :showAddButton="false"
    >
      <template #data>
        <div class="course-manage">
          <!-- 路由导航选项卡 -->
          <div class="course-tabs">
            <router-link 
              to="/courses/student" 
              class="course-tab"
              active-class="active"
            >
              学生课程表
            </router-link>
            <router-link 
              to="/courses/teacher" 
              class="course-tab"
              active-class="active"
            >
              教师课程表
            </router-link>
            <router-link 
              to="/courses/progress" 
              class="course-tab"
              active-class="active"
            >
              教学进度管理
            </router-link>
          </div>

          <!-- 子路由内容 -->
          <div class="course-content">
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
@import '@/styles/course/CourseManage.css';

/* 路由导航选项卡样式 */
.course-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.course-tab {
  padding: 12px 24px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  border-bottom: 2px solid transparent;
  text-decoration: none;
  transition: all 0.3s ease;
}

.course-tab:hover {
  color: #007bff;
}

.course-tab.active {
  color: #007bff;
  border-bottom-color: #007bff;
  background-color: rgba(0, 123, 255, 0.05);
}

.course-content {
  min-height: 600px;
}
</style>