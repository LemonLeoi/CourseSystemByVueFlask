// 集中管理所有类型定义

// 成绩数据类型
export interface Score {
  subject: string;
  score: number;
  examType?: string;
  semester?: string;
  examDate?: string;
  period?: string;
  exam_id?: number;
}

// 学生数据类型
export interface Student {
  id: string;
  name: string;
  gender: string;
  grade: string;
  class: string;
  scores?: Score[];
}

// 教师数据类型
export interface Teacher {
  id: string;
  teacher_id: string;
  name: string;
  gender: string;
  age: number;
  subject: string;
  title: string;
  contact: string;
  teachingClasses: string[];
  isHomeroomTeacher: boolean;
  homeroomClass: string;
}

// 课程数据类型
export interface Course {
  id?: string;
  day: string;
  timeSlot: number;
  name: string;
  teacher?: string;
  className?: string;
  classroom: string;
}

// 考试数据类型
export interface Exam {
  code: string;
  name: string;
  academicYear: string;
  semester: string;
  type: string;
  grade: string;
  startDate: string;
  endDate: string;
  status: '已发布' | '准备中' | '已归档';
}

// 学生状态数据类型
export interface StudentStatus {
  id: string;
  name: string;
  gender: string;
  grade: string;
  class: string;
  contact?: string;
  status: 'active' | 'suspended' | 'graduated' | 'dropped';
  statusText: string;
}

// 分页参数类型
export interface PaginationParams {
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
}

// 搜索参数类型
export interface SearchParams {
  query: string;
  filters?: Record<string, unknown>;
}

// 响应数据类型
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

// 分页响应数据类型
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// 用户类型
export interface User {
  id: string;
  username: string;
  name: string;
  role: string;
  avatar?: string;
}

// 菜单类型
export interface MenuItem {
  id: string;
  label: string;
  path: string;
  icon?: string;
  children?: MenuItem[];
}

// 通知类型
export interface Notification {
  id: string;
  title: string;
  content: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  createdAt: string;
}

// 考试通知类型
export interface Notice {
  id: number;
  title: string;
  content: string;
  date: string;
  author: string;
}
