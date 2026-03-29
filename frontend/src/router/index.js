import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login/login.vue';
import AdminDashboard from '../views/adminDashboard/AdminDashboard.vue';
import StudentManage from '../views/studentManage/StudentManage.vue';
import TeacherManage from '../views/teacherManage/TeacherManage.vue';
import CourseManage from '../views/courseManage/CourseManage.vue';
import StudentCoursePage from '../views/course/StudentCoursePage.vue';
import TeacherCoursePage from '../views/course/TeacherCoursePage.vue';
import ProgressPage from '../views/course/ProgressPage.vue';
import ExamAffairs from '../views/examManage/ExamAffairs.vue';
import StudentStatus from '../views/studentManage/StudentStatus.vue';
import GradeAnalysis from '../views/gradeAnalysis/GradeAnalysis.vue';


const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/overall',
    redirect: '/grade-analysis/overall'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminDashboard
  },
  {
    path: '/students',
    name: 'StudentManage',
    component: StudentManage
  },
  {
    path: '/teachers',
    name: 'TeacherManage',
    component: TeacherManage
  },
  {
    path: '/courses',
    name: 'CourseManage',
    component: CourseManage,
    children: [
      {
        path: 'student',
        name: 'StudentCourse',
        component: StudentCoursePage
      },
      {
        path: 'teacher',
        name: 'TeacherCourse',
        component: TeacherCoursePage
      },
      {
        path: 'progress',
        name: 'TeachingProgress',
        component: ProgressPage
      },
      {
        path: 'overall',
        redirect: '/grade-analysis/overall'
      }
    ]
  },
  {
    path: '/exams',
    name: 'ExamAffairs',
    component: ExamAffairs
  },
  {
    path: '/student-status',
    name: 'StudentStatus',
    component: StudentStatus
  },
  {
    path: '/grade-analysis',
    name: 'GradeAnalysis',
    component: GradeAnalysis,
    children: [
      {
        path: 'overall',
        name: 'OverallAnalysis',
        component: () => import('../views/gradeAnalysis/OverallAnalysis.vue')
      },
      {
        path: 'individual',
        name: 'IndividualAnalysis',
        component: () => import('../views/gradeAnalysis/IndividualAnalysis.vue')
      },
      {
        path: 'class',
        name: 'ClassAnalysis',
        component: () => import('../views/gradeAnalysis/ClassAnalysis.vue')
      },
      {
        path: 'grade',
        name: 'GradeLevelAnalysis',
        component: () => import('../views/gradeAnalysis/GradeLevelAnalysis.vue')
      },
      {
        path: '',
        redirect: 'overall'
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;