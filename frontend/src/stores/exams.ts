import { defineStore } from 'pinia';
import type { Exam } from '../types';

// 考试存储
export const useExamStore = defineStore('exams', {
  state: () => ({
    exams: [] as Exam[],
    loading: false,
    error: null as string | null,
  }),

  getters: {
    getExamByCode: (state) => (code: string) => {
      return state.exams.find(exam => exam.code === code);
    },

    getExamsByType: (state) => (type: string) => {
      return state.exams.filter(exam => exam.type === type);
    },

    getExamsByGrade: (state) => (grade: string) => {
      return state.exams.filter(exam => exam.grade === grade);
    },

    getExamsByStatus: (state) => (status: string) => {
      return state.exams.filter(exam => exam.status === status);
    },

    getActiveExams: (state) => {
      return state.exams.filter(exam => exam.status !== '已归档');
    },

    getArchivedExams: (state) => {
      return state.exams.filter(exam => exam.status === '已归档');
    },
  },

  actions: {
    // 初始化考试数据
    initializeExams(exams: Exam[]) {
      this.exams = exams;
    },

    // 添加考试
    addExam(exam: Exam) {
      this.exams.push(exam);
    },

    // 更新考试
    updateExam(updatedExam: Exam) {
      const index = this.exams.findIndex(e => e.code === updatedExam.code);
      if (index !== -1) {
        this.exams[index] = updatedExam;
      }
    },

    // 删除考试
    deleteExam(code: string) {
      this.exams = this.exams.filter(exam => exam.code !== code);
    },

    // 归档考试
    archiveExam(code: string) {
      const exam = this.getExamByCode(code);
      if (exam) {
        exam.status = '已归档';
        this.updateExam(exam);
      }
    },

    // 取消归档考试
    unarchiveExam(code: string) {
      const exam = this.getExamByCode(code);
      if (exam) {
        exam.status = '已发布';
        this.updateExam(exam);
      }
    },

    // 发布考试
    publishExam(code: string) {
      const exam = this.getExamByCode(code);
      if (exam) {
        exam.status = '已发布';
        this.updateExam(exam);
      }
    },

    // 清除所有考试数据
    clearExams() {
      this.exams = [];
    },
  },
});
