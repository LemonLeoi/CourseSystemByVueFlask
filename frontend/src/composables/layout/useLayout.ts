import { ref } from 'vue';

// 菜单项接口
// interface MenuItem {
//   path: string;
//   label: string;
//   icon: string;
//   isActive?: boolean;
// }

export function useLayout() {
  const sidebarCollapsed = ref(false);

  const handleSidebarToggle = (collapsed: boolean) => {
    sidebarCollapsed.value = collapsed;
  };

  const createMenuItems = (activePath: string) => {
    return [
      { path: '/admin', label: '首页', icon: 'fa-solid fa-house', isActive: activePath === '/admin' },
      { path: '/students', label: '学生管理', icon: 'fa-solid fa-users', isActive: activePath === '/students' },
      { path: '/teachers', label: '教师管理', icon: 'fa-solid fa-chalkboard-user', isActive: activePath === '/teachers' },
      { path: '/courses', label: '课程管理', icon: 'fa-solid fa-book-open', isActive: activePath === '/courses' },
      { path: '/grade-analysis/individual', label: '学生成绩分析', icon: 'fa-solid fa-chart-line', isActive: activePath === '/grade-analysis' || activePath === '/grade-analysis/individual' },
      { path: '/exams', label: '考试管理', icon: 'fa-solid fa-file-invoice', isActive: activePath === '/exams' },
      { path: '/student-status', label: '学籍管理', icon: 'fa-solid fa-id-card', isActive: activePath === '/student-status' }
    ];
  };

  return {
    sidebarCollapsed,
    handleSidebarToggle,
    createMenuItems
  };
}
