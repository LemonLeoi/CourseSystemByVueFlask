import { defineStore } from 'pinia';
import type { Student, Score } from '../types';

// 学生存储
export const useStudentStore = defineStore('students', {
  state: () => ({
    students: [] as Student[],
    loading: false,
    error: null as string | null,
  }),

  getters: {
    getStudentById: (state) => (id: string) => {
      return state.students.find(student => student.id === id);
    },

    getStudentsByGrade: (state) => (grade: string) => {
      return state.students.filter(student => student.grade === grade);
    },

    getStudentsByClass: (state) => (grade: string, className: string) => {
      return state.students.filter(student => student.grade === grade && student.class === className);
    },
  },

  actions: {
    // 初始化学生数据
    initializeStudents(students: Student[]) {
      this.students = students;
    },

    // 添加学生
    addStudent(student: Student) {
      this.students.push(student);
    },

    // 更新学生
    updateStudent(updatedStudent: Student) {
      const index = this.students.findIndex(s => s.id === updatedStudent.id);
      if (index !== -1) {
        this.students[index] = updatedStudent;
      }
    },

    // 删除学生
    deleteStudent(id: string) {
      this.students = this.students.filter(student => student.id !== id);
    },

    // 更新学生成绩
    updateStudentScores(studentId: string, scores: Score[]) {
      const student = this.getStudentById(studentId);
      if (student) {
        student.scores = scores;
        this.updateStudent(student);
      }
    },

    // 清除所有学生数据
    clearStudents() {
      this.students = [];
    },
  },
});
