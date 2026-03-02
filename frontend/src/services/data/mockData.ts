// 模拟数据管理

// 从集中的类型定义文件中导入类型
import type { Student, Teacher, Course, Exam, StudentStatus } from '../../types';

// 学生模拟数据
export const mockStudents: Student[] = [
  {
    id: '1',
    name: '张三',
    gender: '男',
    grade: '高一',
    class: '1班',
    scores: [
      { subject: '语文', score: 85 },
      { subject: '数学', score: 92 },
      { subject: '英语', score: 78 },
      { subject: '物理', score: 88 },
      { subject: '化学', score: 90 }
    ]
  },
  {
    id: '2',
    name: '李四',
    gender: '女',
    grade: '高一',
    class: '1班',
    scores: [
      { subject: '语文', score: 90 },
      { subject: '数学', score: 85 },
      { subject: '英语', score: 95 },
      { subject: '物理', score: 82 },
      { subject: '化学', score: 88 }
    ]
  },
  {
    id: '3',
    name: '王五',
    gender: '男',
    grade: '高一',
    class: '2班',
    scores: [
      { subject: '语文', score: 75 },
      { subject: '数学', score: 95 },
      { subject: '英语', score: 80 },
      { subject: '物理', score: 92 },
      { subject: '化学', score: 85 }
    ]
  },
  {
    id: '4',
    name: '赵六',
    gender: '女',
    grade: '高一',
    class: '2班',
    scores: [
      { subject: '语文', score: 88 },
      { subject: '数学', score: 82 },
      { subject: '英语', score: 90 },
      { subject: '物理', score: 78 },
      { subject: '化学', score: 85 }
    ]
  },
  {
    id: '5',
    name: '钱七',
    gender: '男',
    grade: '高二',
    class: '1班',
    scores: [
      { subject: '语文', score: 82 },
      { subject: '数学', score: 88 },
      { subject: '英语', score: 85 },
      { subject: '物理', score: 90 },
      { subject: '化学', score: 92 }
    ]
  },
  {
    id: '6',
    name: '孙八',
    gender: '女',
    grade: '高二',
    class: '1班',
    scores: [
      { subject: '语文', score: 92 },
      { subject: '数学', score: 85 },
      { subject: '英语', score: 88 },
      { subject: '物理', score: 80 },
      { subject: '化学', score: 86 }
    ]
  },
  {
    id: '7',
    name: '周九',
    gender: '男',
    grade: '高二',
    class: '2班',
    scores: [
      { subject: '语文', score: 78 },
      { subject: '数学', score: 92 },
      { subject: '英语', score: 82 },
      { subject: '物理', score: 88 },
      { subject: '化学', score: 84 }
    ]
  },
  {
    id: '8',
    name: '吴十',
    gender: '女',
    grade: '高二',
    class: '2班',
    scores: [
      { subject: '语文', score: 85 },
      { subject: '数学', score: 80 },
      { subject: '英语', score: 92 },
      { subject: '物理', score: 86 },
      { subject: '化学', score: 88 }
    ]
  }
];

// 教师模拟数据
export const mockTeachers: Teacher[] = [
  {
    id: '1',
    name: '王老师',
    gender: '男',
    subject: '数学',
    title: '高级教师',
    contact: '13900139001',
    teachingClasses: ['高一1班', '高一2班'],
    isHomeroomTeacher: true,
    homeroomClass: '高一1班'
  },
  {
    id: '2',
    name: '李老师',
    gender: '女',
    subject: '语文',
    title: '一级教师',
    contact: '13900139002',
    teachingClasses: ['高二1班', '高二2班'],
    isHomeroomTeacher: true,
    homeroomClass: '高二1班'
  },
  {
    id: '3',
    name: '张老师',
    gender: '男',
    subject: '英语',
    title: '一级教师',
    contact: '13900139003',
    teachingClasses: ['高一1班', '高一2班'],
    isHomeroomTeacher: false,
    homeroomClass: ''
  },
  {
    id: '4',
    name: '刘老师',
    gender: '女',
    subject: '物理',
    title: '高级教师',
    contact: '13900139004',
    teachingClasses: ['高二1班', '高二2班'],
    isHomeroomTeacher: false,
    homeroomClass: ''
  },
  {
    id: '5',
    name: '陈老师',
    gender: '男',
    subject: '化学',
    title: '一级教师',
    contact: '13900139005',
    teachingClasses: ['高一1班', '高一2班'],
    isHomeroomTeacher: false,
    homeroomClass: ''
  }
];

// 课程模拟数据
export const mockCourses: Course[] = [
  {
    id: '1',
    name: '高等数学',
    day: '周一',
    timeSlot: 1,
    classroom: 'A101'
  },
  {
    id: '2',
    name: '线性代数',
    day: '周三',
    timeSlot: 3,
    classroom: 'A102'
  },
  {
    id: '3',
    name: '现代文学',
    day: '周二',
    timeSlot: 1,
    classroom: 'A103'
  },
  {
    id: '4',
    name: '古代文学',
    day: '周四',
    timeSlot: 3,
    classroom: 'A104'
  },
  {
    id: '5',
    name: '英语口语',
    day: '周五',
    timeSlot: 1,
    classroom: 'A105'
  },
  {
    id: '6',
    name: '英语写作',
    day: '周五',
    timeSlot: 3,
    classroom: 'A106'
  },
  {
    id: '7',
    name: '力学',
    day: '周一',
    timeSlot: 3,
    classroom: 'B101'
  },
  {
    id: '8',
    name: '电磁学',
    day: '周三',
    timeSlot: 1,
    classroom: 'B102'
  },
  {
    id: '9',
    name: '无机化学',
    day: '周二',
    timeSlot: 3,
    classroom: 'B103'
  },
  {
    id: '10',
    name: '有机化学',
    day: '周四',
    timeSlot: 1,
    classroom: 'B104'
  }
];

// 考试模拟数据
export const mockExams: Exam[] = [
  {
    code: 'MID20231115MATH',
    name: '期中考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2023-11-15',
    endDate: '2023-11-15',
    status: '已发布'
  },
  {
    code: 'MID20231116CHN',
    name: '期中考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2023-11-16',
    endDate: '2023-11-16',
    status: '已发布'
  },
  {
    code: 'MID20231117ENG',
    name: '期中考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2023-11-17',
    endDate: '2023-11-17',
    status: '已发布'
  },
  {
    code: 'MID20231118PHY',
    name: '期中考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2023-11-18',
    endDate: '2023-11-18',
    status: '已发布'
  },
  {
    code: 'MID20231119CHE',
    name: '期中考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2023-11-19',
    endDate: '2023-11-19',
    status: '已发布'
  },
  {
    code: 'FIN20240115MATH',
    name: '期末考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2024-01-15',
    endDate: '2024-01-15',
    status: '准备中'
  },
  {
    code: 'FIN20240116CHN',
    name: '期末考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2024-01-16',
    endDate: '2024-01-16',
    status: '准备中'
  },
  {
    code: 'FIN20240117ENG',
    name: '期末考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2024-01-17',
    endDate: '2024-01-17',
    status: '准备中'
  },
  {
    code: 'FIN20240118PHY',
    name: '期末考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2024-01-18',
    endDate: '2024-01-18',
    status: '准备中'
  },
  {
    code: 'FIN20240119CHE',
    name: '期末考试',
    type: '闭卷',
    grade: '高一',
    startDate: '2024-01-19',
    endDate: '2024-01-19',
    status: '准备中'
  }
];

// 学生状态模拟数据
export const mockStudentStatus: StudentStatus[] = [
  {
    id: '1',
    name: '张三',
    gender: '男',
    grade: '高一',
    class: '1班',
    contact: '13800138001',
    status: 'active',
    statusText: '在校'
  },
  {
    id: '2',
    name: '李四',
    gender: '女',
    grade: '高一',
    class: '1班',
    contact: '13800138002',
    status: 'active',
    statusText: '在校'
  },
  {
    id: '3',
    name: '王五',
    gender: '男',
    grade: '高一',
    class: '2班',
    contact: '13800138003',
    status: 'active',
    statusText: '在校'
  },
  {
    id: '4',
    name: '赵六',
    gender: '女',
    grade: '高一',
    class: '2班',
    contact: '13800138004',
    status: 'active',
    statusText: '在校'
  },
  {
    id: '5',
    name: '钱七',
    gender: '男',
    grade: '高二',
    class: '1班',
    contact: '13800138005',
    status: 'suspended',
    statusText: '休学'
  },
  {
    id: '6',
    name: '孙八',
    gender: '女',
    grade: '高二',
    class: '1班',
    contact: '13800138006',
    status: 'active',
    statusText: '在校'
  },
  {
    id: '7',
    name: '周九',
    gender: '男',
    grade: '高二',
    class: '2班',
    contact: '13800138007',
    status: 'graduated',
    statusText: '毕业'
  },
  {
    id: '8',
    name: '吴十',
    gender: '女',
    grade: '高二',
    class: '2班',
    contact: '13800138008',
    status: 'dropped',
    statusText: '退学'
  }
];

// 导出所有模拟数据
export const mockData = {
  students: mockStudents,
  teachers: mockTeachers,
  courses: mockCourses,
  exams: mockExams,
  studentStatus: mockStudentStatus
};

export default mockData;