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

// 挖掘发现模拟数据（包含极端显著性案例）
export interface DiscoveryCondition {
  feature: string;
  operator: string;
  value: string | number;
}

export interface DiscoveryResult {
  target: string;
  effect: string;
  change?: number;
}

export interface KnowledgeDiscovery {
  conditions: DiscoveryCondition[];
  result: DiscoveryResult;
  insight?: string;
  confidence?: number;
  isHighlight?: boolean;
  statisticalSignificance?: string;
}

export const mockKnowledgeDiscoveries: KnowledgeDiscovery[] = [
  {
    conditions: [
      { feature: '排课时间', operator: '位于', value: '周五下午' },
      { feature: '课程节次', operator: '=', value: '第5-6节' }
    ],
    result: {
      target: '该课及格率',
      effect: '预测显著下降',
      change: -28
    },
    insight: '周五下午最后一节课学生注意力明显下降，建议调整课程安排',
    confidence: 95,
    isHighlight: true,
    statisticalSignificance: 'p-value < 0.001'
  },
  {
    conditions: [
      { feature: '排课时间', operator: '位于', value: '周二上午' },
      { feature: '课程节次', operator: '=', value: '第1-2节' }
    ],
    result: {
      target: '该课及格率',
      effect: '预测显著上升',
      change: 18
    },
    insight: '周二上午学生精神状态最佳，是安排重要课程的黄金时段',
    confidence: 92,
    isHighlight: true,
    statisticalSignificance: 'p-value < 0.01'
  },
  {
    conditions: [
      { feature: '教师职称', operator: '=', value: '高级教师' },
      { feature: '班级类型', operator: '=', value: '基础薄弱班' }
    ],
    result: {
      target: '学生提分率',
      effect: '比普通教师高出',
      change: 15
    },
    insight: '高级教师在基础薄弱班的教学效果更显著，建议优化师资配置',
    confidence: 88,
    statisticalSignificance: 'p-value < 0.05'
  },
  {
    conditions: [
      { feature: '前序课程分数', operator: '<', value: 75 },
      { feature: '排课时间', operator: '位于', value: '周一上午' }
    ],
    result: {
      target: '该课及格率',
      effect: '预测下降',
      change: -15
    },
    insight: '基础薄弱学生在周一上午课程表现较差，建议提供课前辅导',
    confidence: 85,
    statisticalSignificance: 'p-value < 0.05'
  },
  {
    conditions: [
      { feature: '班级', operator: '=', value: '数学A班' },
      { feature: '教师', operator: '=', value: '教师A' }
    ],
    result: {
      target: '基础薄弱生提分率',
      effect: '比教师B高出',
      change: 12
    },
    insight: '教师A在数学基础薄弱生的教学方法更有效',
    confidence: 82,
    statisticalSignificance: 'p-value < 0.05'
  }
];

// 特征重要性模拟数据
export interface FeatureImportanceItem {
  name: string;
  value: number;
  description: string;
  theoreticalBasis: string;
}

export const mockFeatureImportance: FeatureImportanceItem[] = [
  {
    name: '排课时间',
    value: 0.4521,
    description: '课程安排的时间段对学生成绩的影响',
    theoreticalBasis: '基于C4.5算法的信息增益比计算，排课时间是影响成绩的最关键因素。信息增益比考虑了特征的固有信息，避免了偏向于取值较多特征的问题。'
  },
  {
    name: '教师水平',
    value: 0.3287,
    description: '教师职称和教学经验对学生成绩的影响',
    theoreticalBasis: '教师水平通过信息增益比评估，高级教师与一级教师在教学效果上存在显著差异，信息增益比为0.3287。'
  },
  {
    name: '前序课程分数',
    value: 0.1563,
    description: '学生在前置课程中的表现对当前课程的影响',
    theoreticalBasis: '前序课程分数反映了学生的知识基础，信息增益比为0.1563，表明其对后续课程成绩有中等程度的预测能力。'
  },
  {
    name: '班级类型',
    value: 0.0429,
    description: '重点班与普通班的差异对成绩的影响',
    theoreticalBasis: '班级类型的信息增益比较低(0.0429)，说明在本数据集中，班级类型不是影响成绩的主要因素。'
  },
  {
    name: '学生性别',
    value: 0.0199,
    description: '学生性别对成绩的影响',
    theoreticalBasis: '性别的信息增益比最低(0.0199)，表明在本分析中，性别不是影响成绩的显著因素。'
  }
];

// 决策树路径模拟数据
export interface TreePathNode {
  label: string;
  value?: string;
  isLeaf: boolean;
  splitCriteria?: string;
  branchOptions?: { value: string; nextNodeId?: number }[];
  infoGain?: number;
  significance?: string;
}

export interface DecisionTreeBranch {
  id: string;
  name: string;
  description: string;
  path: TreePathNode[];
  confidence: number;
  impact: string;
  recommendation: string;
}

// 多路径决策树数据 - 支持多条分析路径
export const mockDecisionTreePaths: DecisionTreeBranch[] = [
  {
    id: 'path-1',
    name: '排课时间影响路径',
    description: '分析排课时间对学生成绩的影响',
    confidence: 95,
    impact: '高',
    recommendation: '建议避免在周五下午安排重要课程',
    path: [
      {
        label: '排课时间',
        value: '信息增益: 0.4521',
        isLeaf: false,
        splitCriteria: '',
        infoGain: 0.4521,
        significance: 'p < 0.001',
        branchOptions: [
          { value: '周五下午', nextNodeId: 1 },
          { value: '周二上午', nextNodeId: 10 },
          { value: '其他时间', nextNodeId: 20 }
        ]
      },
      {
        label: '周五下午?',
        value: '是',
        isLeaf: false,
        splitCriteria: '排课时间 = "周五下午"',
        branchOptions: [
          { value: '第5-6节', nextNodeId: 2 },
          { value: '第1-2节', nextNodeId: 5 }
        ]
      },
      {
        label: '课程节次',
        value: '第5-6节',
        isLeaf: false,
        splitCriteria: '课程节次 = "第5-6节"',
        infoGain: 0.3287,
        significance: 'p < 0.01'
      },
      {
        label: '预测结果',
        value: '及格率下降28%',
        isLeaf: true,
        splitCriteria: '最终判定',
        significance: '高度显著'
      }
    ]
  },
  {
    id: 'path-2',
    name: '教师水平影响路径',
    description: '分析教师职称对学生成绩的影响',
    confidence: 88,
    impact: '中高',
    recommendation: '建议为基础薄弱班配置高级教师',
    path: [
      {
        label: '教师职称',
        value: '信息增益: 0.3287',
        isLeaf: false,
        splitCriteria: '',
        infoGain: 0.3287,
        significance: 'p < 0.01',
        branchOptions: [
          { value: '高级教师', nextNodeId: 1 },
          { value: '一级教师', nextNodeId: 1 },
          { value: '二级教师', nextNodeId: 1 }
        ]
      },
      {
        label: '班级类型',
        value: '基础薄弱班',
        isLeaf: false,
        splitCriteria: '班级类型 = "基础薄弱班"',
        branchOptions: [
          { value: '基础薄弱班', nextNodeId: 2 },
          { value: '普通班', nextNodeId: 5 },
          { value: '重点班', nextNodeId: 6 }
        ]
      },
      {
        label: '提分效果',
        value: '高级教师 +15%',
        isLeaf: false,
        splitCriteria: '教师水平 × 班级类型交互效应',
        infoGain: 0.1856,
        significance: 'p < 0.05'
      },
      {
        label: '预测结果',
        value: '提分率提升15%',
        isLeaf: true,
        splitCriteria: '最终判定',
        significance: '显著'
      }
    ]
  },
  {
    id: 'path-3',
    name: '前序课程影响路径',
    description: '分析前序课程成绩对当前课程的影响',
    confidence: 82,
    impact: '中等',
    recommendation: '建议为前序课程成绩较低的学生提供补习',
    path: [
      {
        label: '前序课程分数',
        value: '信息增益: 0.1563',
        isLeaf: false,
        splitCriteria: '',
        infoGain: 0.1563,
        significance: 'p < 0.05',
        branchOptions: [
          { value: '< 75分', nextNodeId: 1 },
          { value: '75-85分', nextNodeId: 1 },
          { value: '> 85分', nextNodeId: 1 }
        ]
      },
      {
        label: '当前课程难度',
        value: '高难度',
        isLeaf: false,
        splitCriteria: '课程难度 = "高"',
        branchOptions: [
          { value: '高难度', nextNodeId: 2 },
          { value: '中难度', nextNodeId: 5 },
          { value: '低难度', nextNodeId: 6 }
        ]
      },
      {
        label: '学习状态',
        value: '需要额外辅导',
        isLeaf: false,
        splitCriteria: '综合评估',
        infoGain: 0.1245,
        significance: 'p < 0.05'
      },
      {
        label: '预测结果',
        value: '及格风险+22%',
        isLeaf: true,
        splitCriteria: '最终判定',
        significance: '中等显著'
      }
    ]
  }
];

// 单路径数据（保持向后兼容）
export const mockDecisionTreePath: TreePathNode[] = mockDecisionTreePaths[0].path;

// 影响因素量化评估数据
export interface FactorImpact {
  factor: string;
  weight: number;
  impactScore: number;
  significance: string;
  positive: boolean;
  description: string;
}

export const mockFactorImpactAnalysis: FactorImpact[] = [
  {
    factor: '排课时间',
    weight: 0.4521,
    impactScore: 85,
    significance: 'p < 0.001',
    positive: false,
    description: '周五下午课程及格率比周二上午低28%'
  },
  {
    factor: '教师职称',
    weight: 0.3287,
    impactScore: 72,
    significance: 'p < 0.01',
    positive: true,
    description: '高级教师授课班级平均提分率高出15%'
  },
  {
    factor: '前序课程成绩',
    weight: 0.1563,
    impactScore: 58,
    significance: 'p < 0.05',
    positive: true,
    description: '前序课程分数每提高10分，当前课程及格率提升8%'
  },
  {
    factor: '班级类型',
    weight: 0.0429,
    impactScore: 35,
    significance: 'p = 0.12',
    positive: true,
    description: '重点班平均成绩略高于普通班，但差异不显著'
  },
  {
    factor: '学生性别',
    weight: 0.0199,
    impactScore: 18,
    significance: 'p = 0.45',
    positive: null,
    description: '性别对成绩无显著影响'
  }
];

// 导出所有模拟数据
export const mockData = {
  students: mockStudents,
  teachers: mockTeachers,
  courses: mockCourses,
  exams: mockExams,
  studentStatus: mockStudentStatus,
  knowledgeDiscoveries: mockKnowledgeDiscoveries,
  featureImportance: mockFeatureImportance,
  decisionTreePath: mockDecisionTreePath
};

export default mockData;