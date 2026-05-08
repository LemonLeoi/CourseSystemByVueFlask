import fs from 'fs';
import path from 'path';

// 读取所有Vue文件
const vueFiles = [
  'src/views/studentManage/StudentStatus.vue',
  'src/views/studentManage/StudentManage.vue',
  'src/views/examManage/ExamAffairs.vue',
  'src/components/layout/Sidebar.vue',
  'src/views/teacherManage/TeacherManage.vue',
  'src/views/adminDashboard/AdminDashboard.vue',
  'src/components/course/ProgressTab.vue',
  'src/views/course/TeacherCoursePage.vue',
  'src/views/course/ProgressPage.vue',
  'src/components/course/StudentCourseTab.vue',
  'src/views/courseManage/CourseManage.vue',
  'src/components/common/Notification.vue',
  'src/App.vue',
  'src/components/common/ErrorBoundary.vue',
  'src/components/course/CourseTable.vue',
  'src/views/course/StudentCoursePage.vue',
  'src/components/course/TeacherCourseTab.vue',
  'src/components/course/CourseModal.vue',
  'src/components/business/BaseCrudPage.vue',
  'src/components/course/ProgressModal.vue',
  'src/components/course/TeacherCourseModal.vue',
  'src/components/course/StudentCourseModal.vue',
  'src/components/business/BaseManagePage.vue',
  'src/components/dashboard/StatisticCard.vue',
  'src/components/dashboard/NoticeItem.vue',
  'src/components/dashboard/TodoItem.vue',
  'src/views/login/login.vue',
  'src/components/layout/Layout.vue',
  'src/components/business/SearchBar.vue',
  'src/components/business/BaseModal.vue',
  'src/components/layout/TopTimeDisplay.vue',
  'src/components/business/Pagination.vue'
];

// 提取样式的函数
function extractStyles(vueFile) {
  const content = fs.readFileSync(vueFile, 'utf8');
  
  // 匹配<style>标签内容
  const styleMatch = content.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
  
  if (styleMatch) {
    return styleMatch[1].trim();
  }
  
  return '';
}

// 处理每个Vue文件
vueFiles.forEach(vueFile => {
  console.log(`Processing ${vueFile}...`);
  
  const styles = extractStyles(vueFile);
  
  if (styles) {
    // 生成对应的CSS文件名
    const fileName = path.basename(vueFile, '.vue');
    const cssFile = path.join('plan', `${fileName}.css`);
    
    // 写入样式文件
    fs.writeFileSync(cssFile, styles);
    console.log(`Extracted styles to ${cssFile}`);
  } else {
    console.log(`No styles found in ${vueFile}`);
  }
});

console.log('\nStyle extraction completed!');
