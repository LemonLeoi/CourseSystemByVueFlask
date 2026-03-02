// 学生服务

import { BaseService } from './baseService';
import { mockStudents } from './data/mockData';
import type { Student, Score } from '../types';

// 学生创建DTO
export interface CreateStudentDto {
  name: string;
  gender: string;
  grade: string;
  class: string;
  contact: string;
  scores?: Score[];
}

// 学生更新DTO
export interface UpdateStudentDto {
  name?: string;
  gender?: string;
  grade?: string;
  class?: string;
  contact?: string;
  scores?: Score[];
}

// 学生服务类
export class StudentService extends BaseService<Student, CreateStudentDto, UpdateStudentDto> {
  constructor() {
    super(mockStudents);
  }

  // 自定义方法：更新学生成绩
  async updateScores(id: string, scores: Score[]): Promise<{ code: number; message: string; data: Student | null }> {
    try {
      const student = this.data.find(item => item.id === id);
      if (!student) {
        return {
          code: 404,
          message: '学生不存在',
          data: null
        };
      }

      student.scores = scores;

      return {
        code: 200,
        message: '更新成绩成功',
        data: student
      };
    } catch (error) {
      return {
        code: 500,
        message: '更新成绩失败',
        data: null
      };
    }
  }

  // 自定义方法：根据年级获取学生
  async getByGrade(grade: string): Promise<{ code: number; message: string; data: Student[] }> {
    try {
      const students = this.data.filter(student => student.grade === grade);
      return {
        code: 200,
        message: '获取年级学生成功',
        data: students
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取年级学生失败',
        data: []
      };
    }
  }

  // 自定义方法：根据班级获取学生
  async getByClass(grade: string, className: string): Promise<{ code: number; message: string; data: Student[] }> {
    try {
      const students = this.data.filter(student => student.grade === grade && student.class === className);
      return {
        code: 200,
        message: '获取班级学生成功',
        data: students
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取班级学生失败',
        data: []
      };
    }
  }

  // 自定义方法：计算学生平均成绩
  calculateAverageScore(student: Student): number {
    if (!student.scores || student.scores.length === 0) {
      return 0;
    }
    const total = student.scores.reduce((sum, score) => sum + score.score, 0);
    return Math.round(total / student.scores.length);
  }

  // 自定义方法：检查学生是否及格
  checkIfPassed(student: Student): boolean {
    if (!student.scores || student.scores.length === 0) {
      return false;
    }
    return student.scores.every(score => score.score >= 60);
  }
}

// 导出单例实例
export const studentService = new StudentService();
