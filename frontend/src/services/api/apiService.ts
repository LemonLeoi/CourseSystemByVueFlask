// API基础配置
const API_BASE_URL = '/api';

// 导入类型定义
import type { Student, Teacher, Course, Score, ApiResponse } from '@/types';
// 导入通知服务
import notificationService from '@/services/ui/uiNotificationService';

// 通用请求函数
async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  console.log('API请求:', url);
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, mergedOptions);
    console.log('API响应状态:', response.status);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.error || `API请求失败: ${response.status}`;
      notificationService.error(errorMessage);
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    console.log('API响应数据:', data);
    
    // 对于成功的POST、PUT、DELETE请求显示成功消息
    if (['POST', 'PUT', 'DELETE'].includes(mergedOptions.method || '')) {
      notificationService.success('操作成功');
    }
    
    return data;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : '网络请求失败，请稍后重试';
    notificationService.error(errorMessage);
    console.error('API请求错误:', error);
    throw error;
  }
}

// 学生相关API
export const studentApi = {
  // 获取学生列表
  getStudents: async (grade?: string, class_name?: string): Promise<Student[]> => {
    let endpoint = '/students/';
    if (grade || class_name) {
      const query = new URLSearchParams();
      if (grade) query.append('grade', grade);
      if (class_name) query.append('class', class_name);
      endpoint += `?${query.toString()}`;
    }
    console.log('=== 调用getStudents API ===');
    console.log('API端点:', endpoint);
    const students = await fetchApi<Student[]>(endpoint);
    console.log('=== getStudents API响应 ===');
    console.log('学生数据:', students);
    return students;
  },
  
  // 获取单个学生信息
  getStudent: async (studentId: string): Promise<Student> => {
    return await fetchApi<Student>(`/students/${studentId}`);
  },
  
  // 添加学生
  addStudent: async (student: Omit<Student, 'id'>): Promise<Student> => {
    return await fetchApi<Student>('/students/', {
      method: 'POST',
      body: JSON.stringify(student),
    });
  },
  
  // 更新学生
  updateStudent: async (studentId: string, student: Partial<Student>): Promise<Student> => {
    return await fetchApi<Student>(`/students/${studentId}`, {
      method: 'PUT',
      body: JSON.stringify(student),
    });
  },
  
  // 删除学生
  deleteStudent: async (studentId: string): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/students/${studentId}`, {
      method: 'DELETE',
    });
  },
  
  // 更新学生成绩
  updateStudentGrades: async (studentId: string, scores: Score[]): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/students/${studentId}/grades`, {
      method: 'PUT',
      body: JSON.stringify({ scores }),
    });
  },
};

// 认证相关API
export const authApi = {
  // 登录
  login: async (username: string, password: string): Promise<any> => {
    return await fetchApi('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },
  
  // 登出
  logout: async (): Promise<any> => {
    return await fetchApi('/auth/logout', {
      method: 'POST',
    });
  },
};

// 教师相关API
export const teacherApi = {
  // 获取教师列表
  getTeachers: async (status?: string, department?: string): Promise<Teacher[]> => {
    let endpoint = '/teachers/';
    if (status || department) {
      const query = new URLSearchParams();
      if (status) query.append('status', status);
      if (department) query.append('department', department);
      endpoint += `?${query.toString()}`;
    }
    return await fetchApi<Teacher[]>(endpoint);
  },
  
  // 获取单个教师信息
  getTeacher: async (teacherId: string): Promise<Teacher> => {
    return await fetchApi<Teacher>(`/teachers/${teacherId}`);
  },
  
  // 添加教师
  addTeacher: async (teacher: Omit<Teacher, 'id'>): Promise<Teacher> => {
    return await fetchApi<Teacher>('/teachers/', {
      method: 'POST',
      body: JSON.stringify(teacher),
    });
  },
  
  // 更新教师
  updateTeacher: async (teacherId: string, teacher: Partial<Teacher>): Promise<Teacher> => {
    return await fetchApi<Teacher>(`/teachers/${teacherId}`, {
      method: 'PUT',
      body: JSON.stringify(teacher),
    });
  },
  
  // 删除教师
  deleteTeacher: async (teacherId: string): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/teachers/${teacherId}`, {
      method: 'DELETE',
    });
  },
};

// 课程相关API
export const courseApi = {
  // 获取课程列表
  getCourses: async (teacher_id?: string): Promise<Course[]> => {
    let endpoint = '/courses/';
    if (teacher_id) {
      endpoint += `?teacher_id=${teacher_id}`;
    }
    return await fetchApi<Course[]>(endpoint);
  },
  
  // 获取单个课程信息
  getCourse: async (courseId: number): Promise<Course> => {
    return await fetchApi<Course>(`/courses/${courseId}`);
  },
  
  // 添加课程
  addCourse: async (course: Omit<Course, 'id'>): Promise<Course> => {
    return await fetchApi<Course>('/courses/', {
      method: 'POST',
      body: JSON.stringify(course),
    });
  },
  
  // 更新课程
  updateCourse: async (courseId: number, course: Partial<Course>): Promise<Course> => {
    return await fetchApi<Course>(`/courses/${courseId}`, {
      method: 'PUT',
      body: JSON.stringify(course),
    });
  },
  
  // 删除课程
  deleteCourse: async (courseId: number): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/courses/${courseId}`, {
      method: 'DELETE',
    });
  },
  
  // 获取学生课程表
  getStudentCourses: async (class_?: string, grade?: string): Promise<Course[]> => {
    let endpoint = '/courses/student-courses';
    const query = new URLSearchParams();
    if (class_) query.append('class', class_);
    if (grade) query.append('grade', grade);
    if (query.toString()) {
      endpoint += `?${query.toString()}`;
    }
    return await fetchApi<Course[]>(endpoint);
  },
  
  // 添加学生课程
  addStudentCourse: async (course: Omit<Course, 'id'>): Promise<Course> => {
    return await fetchApi<Course>('/courses/student-courses', {
      method: 'POST',
      body: JSON.stringify(course),
    });
  },
  
  // 更新学生课程
  updateStudentCourse: async (courseId: number, course: Partial<Course>): Promise<Course> => {
    return await fetchApi<Course>(`/courses/student-courses/${courseId}`, {
      method: 'PUT',
      body: JSON.stringify(course),
    });
  },
  
  // 删除学生课程
  deleteStudentCourse: async (courseId: number): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/courses/student-courses/${courseId}`, {
      method: 'DELETE',
    });
  },
  
  // 获取教师课程表
  getTeacherCourses: async (teacher_id?: string): Promise<Course[]> => {
    let endpoint = '/courses/teacher-courses';
    if (teacher_id) {
      endpoint += `?teacher_id=${teacher_id}`;
    }
    return await fetchApi<Course[]>(endpoint);
  },
  
  // 添加教师课程
  addTeacherCourse: async (course: Omit<Course, 'id'>): Promise<Course> => {
    return await fetchApi<Course>('/courses/teacher-courses', {
      method: 'POST',
      body: JSON.stringify(course),
    });
  },
  
  // 更新教师课程
  updateTeacherCourse: async (courseId: number, course: Partial<Course>): Promise<Course> => {
    return await fetchApi<Course>(`/courses/teacher-courses/${courseId}`, {
      method: 'PUT',
      body: JSON.stringify(course),
    });
  },
  
  // 删除教师课程
  deleteTeacherCourse: async (courseId: number): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/courses/teacher-courses/${courseId}`, {
      method: 'DELETE',
    });
  },
  
  // 获取教学进度
  getTeachingProgress: async (course_id?: number): Promise<any[]> => {
    let endpoint = '/courses/teaching-progress';
    if (course_id) {
      endpoint += `?course_id=${course_id}`;
    }
    return await fetchApi<any[]>(endpoint);
  },
  
  // 根据科目和年级获取教学进度
  getTeachingProgressBySubjectGrade: async (subject: string, grade: string): Promise<any[]> => {
    let endpoint = '/courses/teaching-progress';
    const query = new URLSearchParams();
    if (subject) query.append('subject', subject);
    if (grade) query.append('grade', grade);
    if (query.toString()) {
      endpoint += `?${query.toString()}`;
    }
    return await fetchApi<any[]>(endpoint);
  },
  
  // 添加教学进度
  addTeachingProgress: async (progress: any): Promise<any> => {
    return await fetchApi<any>('/courses/teaching-progress', {
      method: 'POST',
      body: JSON.stringify(progress),
    });
  },
  
  // 更新教学进度
  updateTeachingProgress: async (progressId: number, progress: any): Promise<any> => {
    return await fetchApi<any>(`/courses/teaching-progress/${progressId}`, {
      method: 'PUT',
      body: JSON.stringify(progress),
    });
  },
  
  // 删除教学进度
  deleteTeachingProgress: async (progressId: number): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/courses/teaching-progress/${progressId}`, {
      method: 'DELETE',
    });
  },
  
  // 获取教室列表
  getClassrooms: async (): Promise<string[]> => {
    return await fetchApi<string[]>('/courses/classrooms');
  },
  
  // 获取科目列表
  getSubjects: async (): Promise<string[]> => {
    console.log('调用getSubjects方法');
    try {
      const subjects = await fetchApi<string[]>('/courses/subjects');
      console.log('getSubjects返回:', subjects);
      return subjects;
    } catch (error) {
      console.error('getSubjects错误:', error);
      throw error;
    }
  },
};

// 健康检查
export const healthApi = {
  check: async (): Promise<any> => {
    return await fetchApi('/health');
  },
};

export default {
  student: studentApi,
  teacher: teacherApi,
  course: courseApi,
  auth: authApi,
  health: healthApi,
};