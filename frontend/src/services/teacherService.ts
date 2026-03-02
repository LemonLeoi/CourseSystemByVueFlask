// 教师服务

import { BaseService } from './baseService';
import { mockTeachers } from './data/mockData';
import type { Teacher } from '../types';

// 教师创建DTO
export interface CreateTeacherDto {
  name: string;
  gender: string;
  subject: string;
  title: string;
  contact: string;
  teachingClasses: string[];
  isHomeroomTeacher: boolean;
  homeroomClass: string;
}

// 教师更新DTO
export interface UpdateTeacherDto {
  name?: string;
  gender?: string;
  subject?: string;
  title?: string;
  contact?: string;
  teachingClasses?: string[];
  isHomeroomTeacher?: boolean;
  homeroomClass?: string;
}

// 教师服务类
export class TeacherService extends BaseService<Teacher, CreateTeacherDto, UpdateTeacherDto> {
  constructor() {
    super(mockTeachers);
  }

  // 自定义方法：根据科目获取教师
  async getBySubject(subject: string): Promise<{ code: number; message: string; data: Teacher[] }> {
    try {
      const teachers = this.data.filter(teacher => teacher.subject === subject);
      return {
        code: 200,
        message: '获取科目教师成功',
        data: teachers
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取科目教师失败',
        data: []
      };
    }
  }

  // 自定义方法：根据职称获取教师
  async getByTitle(title: string): Promise<{ code: number; message: string; data: Teacher[] }> {
    try {
      const teachers = this.data.filter(teacher => teacher.title === title);
      return {
        code: 200,
        message: '获取职称教师成功',
        data: teachers
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取职称教师失败',
        data: []
      };
    }
  }

  // 自定义方法：根据年级获取教师
  async getByGrade(grade: string): Promise<{ code: number; message: string; data: Teacher[] }> {
    try {
      const teachers = this.data.filter(teacher => 
        teacher.teachingClasses.some(className => className.startsWith(grade))
      );
      return {
        code: 200,
        message: '获取年级教师成功',
        data: teachers
      };
    } catch (error) {
      return {
        code: 500,
        message: '获取年级教师失败',
        data: []
      };
    }
  }
}

// 导出单例实例
export const teacherService = new TeacherService();
