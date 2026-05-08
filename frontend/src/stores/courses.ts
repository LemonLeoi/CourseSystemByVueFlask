import { defineStore } from 'pinia';

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

// 时间段数据类型
export interface TimeSlot {
  id: number;
  name: string;
}

// 教学进度数据类型
export interface TeachingProgress {
  id: number;
  chapter: string;
  hours: number;
  objective: string;
  progress: number;
  status: 'not-started' | 'in-progress' | 'completed';
  grade: string;
  subject: string;
}

// 课程存储
export const useCourseStore = defineStore('courses', {
  state: () => ({
    studentCourses: [] as Course[],
    teacherCourses: [] as Course[],
    teachingProgress: [] as TeachingProgress[],
    timeSlots: [] as TimeSlot[],
    weekDays: [] as string[],
    loading: false,
    error: null as string | null,
  }),

  getters: {
    // 获取学生课程
    getStudentCourse: (state) => (day: string, timeSlotId: number) => {
      return state.studentCourses.find(course => {
        return course.day === day && course.timeSlot === timeSlotId;
      });
    },

    // 获取教师课程
    getTeacherCourse: (state) => (day: string, timeSlotId: number) => {
      return state.teacherCourses.find(course => {
        return course.day === day && course.timeSlot === timeSlotId;
      });
    },

    // 获取教学进度
    getTeachingProgress: (state) => (grade: string, subject: string) => {
      return state.teachingProgress.filter(progress => {
        return progress.grade === grade && progress.subject === subject;
      });
    },

    // 获取按天分组的学生课程
    getStudentCoursesByDay: (state) => {
      const coursesByDay: Record<string, Course[]> = {};
      state.weekDays.forEach(day => {
        coursesByDay[day] = [];
      });
      state.studentCourses.forEach(course => {
        const day = course.day;
        if (day && coursesByDay[day]) {
          coursesByDay[day].push(course);
        }
      });
      return coursesByDay;
    },

    // 获取按天分组的教师课程
    getTeacherCoursesByDay: (state) => {
      const coursesByDay: Record<string, Course[]> = {};
      state.weekDays.forEach(day => {
        coursesByDay[day] = [];
      });
      state.teacherCourses.forEach(course => {
        const day = course.day;
        if (day && coursesByDay[day]) {
          coursesByDay[day].push(course);
        }
      });
      return coursesByDay;
    },
  },

  actions: {
    // 初始化时间槽和星期
    initializeScheduleConfig(timeSlots: TimeSlot[], weekDays: string[]) {
      this.timeSlots = timeSlots;
      this.weekDays = weekDays;
    },

    // 初始化学生课程
    initializeStudentCourses(courses: Course[]) {
      this.studentCourses = courses;
    },

    // 初始化教师课程
    initializeTeacherCourses(courses: Course[]) {
      this.teacherCourses = courses;
    },

    // 初始化教学进度
    initializeTeachingProgress(progress: TeachingProgress[]) {
      this.teachingProgress = progress;
    },

    // 添加学生课程
    addStudentCourse(course: Course) {
      this.studentCourses.push(course);
    },

    // 更新学生课程
    updateStudentCourse(updatedCourse: Course) {
      const index = this.studentCourses.findIndex(c => {
        return c.day === updatedCourse.day && c.timeSlot === updatedCourse.timeSlot;
      });
      if (index !== -1) {
        this.studentCourses[index] = updatedCourse;
      }
    },

    // 删除学生课程
    deleteStudentCourse(day: string, timeSlotId: number) {
      this.studentCourses = this.studentCourses.filter(course => {
        return !(course.day === day && course.timeSlot === timeSlotId);
      });
    },

    // 添加教师课程
    addTeacherCourse(course: Course) {
      this.teacherCourses.push(course);
    },

    // 更新教师课程
    updateTeacherCourse(updatedCourse: Course) {
      const index = this.teacherCourses.findIndex(c => {
        return c.day === updatedCourse.day && c.timeSlot === updatedCourse.timeSlot;
      });
      if (index !== -1) {
        this.teacherCourses[index] = updatedCourse;
      }
    },

    // 删除教师课程
    deleteTeacherCourse(day: string, timeSlotId: number) {
      this.teacherCourses = this.teacherCourses.filter(course => {
        return !(course.day === day && course.timeSlot === timeSlotId);
      });
    },

    // 添加教学进度
    addTeachingProgress(progress: TeachingProgress) {
      this.teachingProgress.push(progress);
    },

    // 更新教学进度
    updateTeachingProgress(updatedProgress: TeachingProgress) {
      const index = this.teachingProgress.findIndex(p => p.id === updatedProgress.id);
      if (index !== -1) {
        this.teachingProgress[index] = updatedProgress;
      }
    },

    // 删除教学进度
    deleteTeachingProgress(id: number) {
      this.teachingProgress = this.teachingProgress.filter(progress => progress.id !== id);
    },

    // 清除所有数据
    clearAll() {
      this.studentCourses = [];
      this.teacherCourses = [];
      this.teachingProgress = [];
    },
  },
});
