// API基础配置
const API_BASE_URL = 'http://localhost:5000/api';

// 导入类型定义
import type { Student, Teacher, Course, Score, ApiResponse, Exam } from '@/types';
// 导入通知服务
import notificationService from '@/services/ui/uiNotificationService';
// 导入离线存储服务
import { offlineStorageService } from '@/services/data/offlineStorageService';

// 教学进度类型
export interface TeachingProgress {
  id?: number;
  course_id: number;
  subject: string;
  grade: string;
  progress: number;
  note?: string;
  updated_at?: string;
}

// 成绩分级设置类型
export interface GradeSettings {
  id?: number;
  excellent_min: number;
  good_min: number;
  average_min: number;
  pass_min: number;
  updated_at?: string;
}

// 登录响应类型
export interface LoginResponse {
  token: string;
  user: {
    id: string;
    username: string;
    name: string;
    role: string;
  };
}

// 健康检查响应类型
export interface HealthResponse {
  status: string;
  timestamp: string;
}

// 检查网络状态
function isOnline(): boolean {
  return navigator.onLine;
}

// 生成缓存键
function generateCacheKey(endpoint: string, options: RequestInit = {}): string {
  const method = options.method || 'GET';
  const body = options.body ? JSON.stringify(options.body) : '';
  // 将endpoint（包含查询参数）也包含在缓存键中
  return `${method}:${endpoint}:${body}`;
}


// 通用请求函数
export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
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
  
  // 生成缓存键
  const cacheKey = generateCacheKey(endpoint, mergedOptions);
  
  try {
    if (isOnline()) {
      // 网络在线时，从服务器获取数据
      const response = await fetch(url, mergedOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.message || errorData.error || `API请求失败: ${response.status}`;
        notificationService.error(errorMessage);
        
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      
      // 对于成功的POST、PUT、DELETE请求显示成功消息
      if (['POST', 'PUT', 'DELETE'].includes(mergedOptions.method || '')) {
        notificationService.success(data.message || '操作成功');
      }
      
      // 检查响应数据是否包含data字段
      const result = data && typeof data === 'object' && 'data' in data ? data.data : data;
      
      // 缓存响应数据
      await offlineStorageService.storeAppState(cacheKey, result);
      
      return result as T;
    } else {
      // 网络离线时，从本地存储获取数据
      
      // 对于GET请求，尝试从本地缓存获取数据
      if (mergedOptions.method === 'GET' || !mergedOptions.method) {
        const cachedData = await offlineStorageService.getAppState(cacheKey);
        if (cachedData) {
          return cachedData as T;
        }
      }
      
      // 对于非GET请求，添加到同步队列
      if (['POST', 'PUT', 'DELETE'].includes(mergedOptions.method || '')) {
        await offlineStorageService.addToSyncQueue({
          url: endpoint,
          method: mergedOptions.method || 'POST',
          data: mergedOptions.body ? JSON.parse(mergedOptions.body as string) : {}
        });
        
        // 模拟成功响应
        notificationService.success('操作已添加到同步队列，网络恢复后将自动同步');
        return {} as T;
      }
      
      throw new Error('网络离线且无缓存数据');
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : '网络请求失败，请稍后重试';
    notificationService.error(errorMessage);
    
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
    const students = await fetchApi<Student[]>(endpoint);
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
  
  // 删除学生指定考试的指定科目成绩
  deleteStudentGrade: async (studentId: string, examCode: string, subject: string): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/grades/${studentId}/${examCode}/${subject}`, {
      method: 'DELETE',
    });
  },
  
  // 删除学生指定考试的所有科目成绩
  deleteStudentExamGrades: async (studentId: string, examCode: string): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/grades/${studentId}/${examCode}`, {
      method: 'DELETE',
    });
  },
  
  // 删除指定考试的所有学生成绩
  deleteExamAllGrades: async (examCode: string): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>(`/grades/exam/${examCode}`, {
      method: 'DELETE',
    });
  },
  
  // 获取班级和年级列表
  getClasses: async (): Promise<{ grades: string[], classes: string[] }> => {
    return await fetchApi<{ grades: string[], classes: string[] }>('/students/classes');
  },
};

// 认证相关API
export const authApi = {
  // 登录
  login: async (username: string, password: string): Promise<LoginResponse> => {
    return await fetchApi<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },
  
  // 登出
  logout: async (): Promise<ApiResponse<boolean>> => {
    return await fetchApi<ApiResponse<boolean>>('/auth/logout', {
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
  getTeachingProgress: async (course_id?: number): Promise<TeachingProgress[]> => {
    let endpoint = '/courses/teaching-progress';
    if (course_id) {
      endpoint += `?course_id=${course_id}`;
    }
    return await fetchApi<TeachingProgress[]>(endpoint);
  },
  
  // 根据科目和年级获取教学进度
  getTeachingProgressBySubjectGrade: async (subject: string, grade: string): Promise<TeachingProgress[]> => {
    let endpoint = '/courses/teaching-progress';
    const query = new URLSearchParams();
    if (subject) query.append('subject', subject);
    if (grade) query.append('grade', grade);
    if (query.toString()) {
      endpoint += `?${query.toString()}`;
    }
    return await fetchApi<TeachingProgress[]>(endpoint);
  },
  
  // 添加教学进度
  addTeachingProgress: async (progress: Omit<TeachingProgress, 'id'>): Promise<TeachingProgress> => {
    return await fetchApi<TeachingProgress>('/courses/teaching-progress', {
      method: 'POST',
      body: JSON.stringify(progress),
    });
  },
  
  // 更新教学进度
  updateTeachingProgress: async (progressId: number, progress: Partial<TeachingProgress>): Promise<TeachingProgress> => {
    return await fetchApi<TeachingProgress>(`/courses/teaching-progress/${progressId}`, {
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
    return await fetchApi<string[]>('/courses/subjects');
  },
  
  // 获取考试列表
  getExams: async (): Promise<Exam[]> => {
    return await fetchApi<Exam[]>('/exams/');
  },
};

// 健康检查
export const healthApi = {
  check: async (): Promise<HealthResponse> => {
    return await fetchApi<HealthResponse>('/health');
  },
};

// 成绩分级设置相关API
export const gradeSettingsApi = {
  // 获取成绩分级设置
  getGradeSettings: async (): Promise<GradeSettings> => {
    return await fetchApi<GradeSettings>('/grade-settings/');
  },
  
  // 更新成绩分级设置
  updateGradeSettings: async (settings: Partial<GradeSettings>): Promise<GradeSettings> => {
    return await fetchApi<GradeSettings>('/grade-settings/', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  },
};

export default {
  student: studentApi,
  teacher: teacherApi,
  course: courseApi,
  auth: authApi,
  health: healthApi,
  gradeSettings: gradeSettingsApi,
};
