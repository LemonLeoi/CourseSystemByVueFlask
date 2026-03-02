import { defineStore } from 'pinia';
import type { Teacher } from '../types';

// 教师存储
export const useTeacherStore = defineStore('teachers', {
  state: () => ({
    teachers: [] as Teacher[],
    loading: false,
    error: null as string | null,
  }),

  getters: {
    getTeacherById: (state) => (id: string) => {
      return state.teachers.find(teacher => teacher.id === id);
    },

    getTeachersBySubject: (state) => (subject: string) => {
      return state.teachers.filter(teacher => teacher.subject === subject);
    },

    getHomeroomTeachers: (state) => {
      return state.teachers.filter(teacher => teacher.isHomeroomTeacher);
    },

    getTeachersByGrade: (state) => (grade: string) => {
      return state.teachers.filter(teacher => 
        teacher.teachingClasses.some(className => className.startsWith(grade))
      );
    },
  },

  actions: {
    // 初始化教师数据
    initializeTeachers(teachers: Teacher[]) {
      this.teachers = teachers;
    },

    // 添加教师
    addTeacher(teacher: Teacher) {
      this.teachers.push(teacher);
    },

    // 更新教师
    updateTeacher(updatedTeacher: Teacher) {
      const index = this.teachers.findIndex(t => t.id === updatedTeacher.id);
      if (index !== -1) {
        this.teachers[index] = updatedTeacher;
      }
    },

    // 删除教师
    deleteTeacher(id: string) {
      this.teachers = this.teachers.filter(teacher => teacher.id !== id);
    },

    // 更新教师任教班级
    updateTeachingClasses(teacherId: string, teachingClasses: string[]) {
      const teacher = this.getTeacherById(teacherId);
      if (teacher) {
        teacher.teachingClasses = teachingClasses;
        this.updateTeacher(teacher);
      }
    },

    // 更新班主任状态
    updateHomeroomStatus(teacherId: string, isHomeroomTeacher: boolean, homeroomClass: string = '') {
      const teacher = this.getTeacherById(teacherId);
      if (teacher) {
        teacher.isHomeroomTeacher = isHomeroomTeacher;
        teacher.homeroomClass = homeroomClass;
        this.updateTeacher(teacher);
      }
    },

    // 清除所有教师数据
    clearTeachers() {
      this.teachers = [];
    },
  },
});
