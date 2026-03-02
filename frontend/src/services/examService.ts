// 考试服务

import { BaseService } from './baseService';
import { mockExams } from './data/mockData';
import type { Exam } from '../types';

// 考试创建DTO
export interface CreateExamDto {
  name: string;
  type: string;
  grade: string;
  startDate: string;
  endDate: string;
  status: '已发布' | '准备中' | '已归档';
}

// 考试更新DTO
export interface UpdateExamDto {
  name?: string;
  type?: string;
  grade?: string;
  startDate?: string;
  endDate?: string;
  status?: '已发布' | '准备中' | '已归档';
}

// 考试服务类
export class ExamService extends BaseService<Exam, CreateExamDto, UpdateExamDto> {
  constructor() {
    super(mockExams);
  }

  // 自定义方法：根据类型获取考试
  async getByType(type: string): Promise<{ code: number; message: string; data: Exam[] }> {
    try {
      const exams = this.data.filter(exam => exam.type === type);
      return {
        code: 200,
        message: '获取类型考试成功',
        data: exams
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取类型考试失败',
        data: []
      };
    }
  }

  // 自定义方法：根据年级获取考试
  async getByGrade(grade: string): Promise<{ code: number; message: string; data: Exam[] }> {
    try {
      const exams = this.data.filter(exam => exam.grade === grade);
      return {
        code: 200,
        message: '获取年级考试成功',
        data: exams
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取年级考试失败',
        data: []
      };
    }
  }

  // 自定义方法：获取即将到来的考试
  async getUpcoming(days: number = 7): Promise<{ code: number; message: string; data: Exam[] }> {
    try {
      const today = new Date();
      const futureDate = new Date();
      futureDate.setDate(today.getDate() + days);

      const exams = this.data.filter(exam => {
        const examDate = new Date(exam.startDate);
        return examDate >= today && examDate <= futureDate;
      }).sort((a, b) => new Date(a.startDate).getTime() - new Date(b.startDate).getTime());

      return {
        code: 200,
        message: '获取即将到来的考试成功',
        data: exams
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取即将到来的考试失败',
        data: []
      };
    }
  }
}

// 导出单例实例
export const examService = new ExamService();
