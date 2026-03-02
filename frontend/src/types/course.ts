// 学生课程表数据类型
export interface StudentCourse {
  day: string;
  timeSlot: number;
  name: string;
  teacher: string;
  classroom: string;
}

// 教师课程表数据类型
export interface TeacherCourse {
  day: string;
  timeSlot: number;
  name: string;
  className: string;
  classroom: string;
}

// 教学进度数据类型
export interface TeachingProgress {
  id: number;
  chapter: string;
  hours: number;
  objective: string;
  progress: number;
  status: string;
}

// 教师课程统计数据类型
export interface TeacherStats {
  totalClasses: number;
  mostClass: string;
  busiestDay: string;
  avgClasses: string;
}

// 时间段数据类型
export interface TimeSlot {
  id: number;
  name: string;
  startTime: string;
  endTime: string;
}

// 星期数据类型
export type WeekDay = string;

// 课程表单数据类型
export interface CourseForm {
  day: string;
  timeSlot: number;
  name: string;
  teacher?: string;
  className?: string;
  classroom: string;
}

// 进度表单数据类型
export interface ProgressForm {
  id: number;
  chapter: string;
  hours: number;
  objective: string;
  progress: number;
  status: string;
}

// 状态类型
export type CourseStatus = 'completed' | 'in-progress' | 'not-started';

// 标签页类型
export type CourseTabType = 'student' | 'teacher' | 'progress';

// 课程模式类型
export type CourseMode = 'student' | 'teacher';
