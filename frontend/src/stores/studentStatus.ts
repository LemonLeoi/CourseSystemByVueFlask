import { defineStore } from 'pinia';
import type { StudentStatus } from '../types';

// 学籍存储
export const useStudentStatusStore = defineStore('studentStatus', {
  state: () => ({
    students: [] as StudentStatus[],
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

    getStudentsByStatus: (state) => (status: string) => {
      return state.students.filter(student => student.status === status);
    },

    getActiveStudents: (state) => {
      return state.students.filter(student => student.status === 'active');
    },

    getSuspendedStudents: (state) => {
      return state.students.filter(student => student.status === 'suspended');
    },

    getGraduatedStudents: (state) => {
      return state.students.filter(student => student.status === 'graduated');
    },

    getDroppedStudents: (state) => {
      return state.students.filter(student => student.status === 'dropped');
    },

    getArchivedStudents: (state) => {
      return state.students.filter(student => student.status === 'graduated');
    },
  },

  actions: {
    // 初始化学籍数据
    initializeStudents(students: StudentStatus[]) {
      this.students = students;
    },

    // 添加学生
    addStudent(student: StudentStatus) {
      this.students.push(student);
    },

    // 更新学生
    updateStudent(updatedStudent: StudentStatus) {
      const index = this.students.findIndex(s => s.id === updatedStudent.id);
      if (index !== -1) {
        this.students[index] = updatedStudent;
      }
    },

    // 删除学生
    deleteStudent(id: string) {
      this.students = this.students.filter(student => student.id !== id);
    },

    // 更新学籍状态
    updateStudentStatus(studentId: string, status: 'active' | 'suspended' | 'graduated' | 'dropped') {
      const student = this.getStudentById(studentId);
      if (student) {
        student.status = status;
        student.statusText = this.getStatusText(status);
        this.updateStudent(student);
      }
    },

    // 归档学生（设置为毕业状态）
    archiveStudent(studentId: string) {
      this.updateStudentStatus(studentId, 'graduated');
    },

    // 取消归档学生（设置为在校状态）
    unarchiveStudent(studentId: string) {
      this.updateStudentStatus(studentId, 'active');
    },

    // 获取状态文本
    getStatusText(status: string): string {
      const statusMap: Record<string, string> = {
        'active': '在校',
        'suspended': '休学',
        'graduated': '毕业',
        'dropped': '退学'
      };
      return statusMap[status] || status;
    },

    // 清除所有学籍数据
    clearStudents() {
      this.students = [];
    },
  },
});
