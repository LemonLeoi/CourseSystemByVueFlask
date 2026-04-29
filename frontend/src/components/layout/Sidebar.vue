<template>
  <div class="sidebar" :class="{ collapsed }" id="sidebar">
    <div class="logo">
      <img :src="logoSrc" alt="西十高级中学" class="logo-img"/>
    </div>
    <div class="toggle-sidebar" id="toggleSidebar" @click="toggleSidebar">
      <i class="fa-solid" :class="collapsed ? 'fa-angle-right' : 'fa-angle-left'"></i>
    </div>
    <ul class="sidebar-menu">
      <li v-for="(item, index) in menuItems" :key="item.path" :style="{ animationDelay: `${index * 0.1}s` }">
        <router-link 
          :to="item.path" 
          class="menu-item" 
          :class="{ active: currentPath === item.path }"
        >
          <i :class="item.icon"></i> <span>{{ item.label }}</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps<{
  logoSrc?: string;
  menuItems?: Array<{
    path: string;
    label: string;
    icon: string;
  }>;
}>();

const emit = defineEmits<{
  (e: 'toggle', collapsed: boolean): void;
}>();

const route = useRoute();
const collapsed = ref(false);
const logoSrc = props.logoSrc || '/static/img/logo.png';

const menuItems = props.menuItems || [
  { path: '/admin', label: '首页', icon: 'fa-solid fa-house' },
  { path: '/students', label: '学生管理', icon: 'fa-solid fa-users' },
  { path: '/teachers', label: '教师管理', icon: 'fa-solid fa-chalkboard-user' },
  { path: '/courses', label: '课程管理', icon: 'fa-solid fa-book-open' },
  { path: '/grade-analysis/individual', label: '学生成绩分析', icon: 'fa-solid fa-chart-line' },
  { path: '/exams', label: '考试管理', icon: 'fa-solid fa-file-invoice' },
  { path: '/student-status', label: '学籍管理', icon: 'fa-solid fa-id-card' }
];

const currentPath = computed(() => route.path);

const toggleSidebar = () => {
  collapsed.value = !collapsed.value;
  emit('toggle', collapsed.value);
};
</script>

<style scoped>
.sidebar {
  width: 220px;
  height: 100vh;
  background-color: var(--secondary-color);
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  padding: 20px;
  box-sizing: border-box;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease;
  z-index: 1000;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed .logo-img {
  display: none;
}

.sidebar.collapsed ul li a span {
  display: none;
}

.sidebar.collapsed ul li a i {
  margin-right: 0;
  font-size: 1.2rem;
}

.sidebar .logo {
  width: 100%;
  margin-bottom: 30px;
  text-align: center;
}

.sidebar .logo-img {
  width: 80%;
  margin-bottom: 20px;
  border-radius: 5px;
  transition: transform 0.3s ease;
}

.sidebar .logo-img:hover {
  transform: scale(1.05);
}

.sidebar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  margin-bottom: 8px;
  opacity: 0;
  animation: slideIn 0.3s ease-out forwards;
}

.sidebar ul li a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 5px;
  transition: all 0.3s ease;
  font-size: 15px;
}

.sidebar ul li a i {
  margin-right: 12px;
  font-size: 1rem;
  width: 20px;
  text-align: center;
}

.sidebar ul li a:hover,
.sidebar ul li a.active {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(3px);
}

.toggle-sidebar {
  position: absolute;
  top: 15px;
  right: 15px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.2rem;
  transition: all 0.3s;
  z-index: 1001;
}

.toggle-sidebar:hover {
  color: white;
}

.sidebar.collapsed .toggle-sidebar {
  right: 10px;
}

@keyframes slideIn {
  from { transform: translateX(-10px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>