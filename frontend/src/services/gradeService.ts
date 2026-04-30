import { fetchApi } from './api/apiService';
import type { StudentAnalysisData, ClassAnalysisData, GradeAnalysisData } from '../stores/grades';
import type { SubjectAnalysisData, ExamTrendData, TeacherPerformanceData } from '../composables/grade/useGradeAnalysis';

export interface IntermediateResult {
  analysis_id: string;
  step: string;
  data: Record<string, unknown>;
  timestamp: string;
}

export interface ModelState {
  analysis_id: string;
  model_name: string;
  state: Record<string, unknown>;
}

export interface Conclusion {
  analysis_id: string;
  level: string;
  conclusion: string;
  confidence: number;
}

export interface AnalysisLog {
  id: string;
  analysis_type: string;
  message: string;
  timestamp: string;
  level: 'info' | 'warning' | 'error';
}

export interface ProcessVisualizationData {
  analysis_id: string;
  process_type: string;
  steps: {
    id: string;
    name: string;
    status: 'completed' | 'running' | 'pending';
    data?: Record<string, unknown>;
  }[];
}

export interface AnalysisHistory {
  id: string;
  analysis_type: string;
  params: Record<string, unknown>;
  result_summary: string;
  created_at: string;
}

// 挖掘发现相关类型
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

export interface KnowledgeDiscoveryResponse {
  discoveries: KnowledgeDiscovery[];
  total: number;
  algorithm: string;
  method: string;
}

// 特征重要性相关类型
export interface FeatureImportanceItem {
  name: string;
  value: number;
  description: string;
  theoreticalBasis: string;
}

export interface FeatureImportanceResponse {
  feature_importance: FeatureImportanceItem[];
  algorithm: string;
  method: string;
  explanation: string;
}

// 决策树路径相关类型
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

export interface DecisionTreePathResponse {
  paths: DecisionTreeBranch[];
  class_name?: string;
  student_id?: string;
  algorithm: string;
  total_paths: number;
}

// 影响因素量化评估相关类型
export interface FactorImpact {
  factor: string;
  weight: number;
  impactScore: number;
  significance: string;
  positive: boolean | null;
  description: string;
}

export interface FactorImpactResponse {
  factor_impact: FactorImpact[];
  algorithm: string;
  method: string;
  analysis_type: string;
}

// ETL状态相关类型
export interface ETLStepStatus {
  step_name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string;
  start_time?: string;
  end_time?: string;
  error?: string;
}

export interface ETLStatusResponse {
  analysis_id: string;
  class_ids: string[];
  analysis_type: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  current_step: string;
  progress: number;
  created_at: string;
  updated_at: string;
  error_message?: string;
  steps: Record<string, ETLStepStatus>;
}

export interface ExecuteAnalysisResponse {
  analysis_id: string;
  message: string;
  status: string;
}

// 班级对比相关类型
export interface ClassMetrics {
  average_score: number;
  pass_rate: number;
  excellent_rate: number;
  improvement_rate: number;
}

export interface ClassData {
  class_id: string;
  class_name: string;
  teacher_group: string;
  metrics: ClassMetrics;
  student_count: number;
  teacher_name: string;
}

export interface MetricDifference {
  base_value: number;
  compare_value: number;
  difference: number;
  percentage: number;
}

export interface ClassComparison {
  class_id: string;
  class_name: string;
  differences: Record<string, MetricDifference>;
}

export interface ClassCompareResponse {
  class_ids: string[];
  base_class: ClassData;
  comparisons: ClassComparison[];
  metrics: string[];
  teacher_comparison: {
    same_group: boolean;
    groups: string[];
  };
  statistical_significance: {
    p_value: number;
    significant: boolean;
  };
}

// 实时挖掘发现响应
export interface RealtimeDiscoveriesResponse {
  discoveries: KnowledgeDiscovery[];
  total: number;
  class_id?: string;
  algorithm: string;
  method: string;
  generated_at: string;
}

export class GradeService {
  async getStudentAnalysis(studentId: string): Promise<StudentAnalysisData> {
    return await fetchApi<StudentAnalysisData>(`/grades/analysis/${studentId}`);
  }

  async getClassAnalysis(className: string): Promise<ClassAnalysisData> {
    return await fetchApi<ClassAnalysisData>(`/grades/analysis/class/${encodeURIComponent(className)}`);
  }

  async getGradeAnalysis(gradeName: string): Promise<GradeAnalysisData> {
    return await fetchApi<GradeAnalysisData>(`/grades/analysis/grade/${encodeURIComponent(gradeName)}`);
  }

  async getStudentSubjectAnalysis(studentId: string, subject: string): Promise<StudentAnalysisData> {
    return await fetchApi<StudentAnalysisData>(`/grades/analysis/subject/${studentId}/${encodeURIComponent(subject)}`);
  }

  async getClassSubjectAnalysis(className: string, subject: string): Promise<ClassAnalysisData> {
    return await fetchApi<ClassAnalysisData>(`/grades/analysis/class/${encodeURIComponent(className)}/${encodeURIComponent(subject)}`);
  }

  async getGradeSubjectAnalysis(gradeName: string, subject: string): Promise<SubjectAnalysisData> {
    return await fetchApi<SubjectAnalysisData>(`/grades/analysis/grade/${encodeURIComponent(gradeName)}/${encodeURIComponent(subject)}`);
  }

  async getStudentTrend(studentId: string): Promise<ExamTrendData> {
    return await fetchApi<ExamTrendData>(`/grades/analysis/trend/${studentId}`);
  }

  async getClassTrend(className: string): Promise<ExamTrendData> {
    return await fetchApi<ExamTrendData>(`/grades/analysis/class/trend/${encodeURIComponent(className)}`);
  }

  async getGradeTrend(gradeName: string): Promise<ExamTrendData> {
    return await fetchApi<ExamTrendData>(`/grades/analysis/grade/trend/${encodeURIComponent(gradeName)}`);
  }

  async getTeacherPerformance(subject: string): Promise<TeacherPerformanceData> {
    return await fetchApi<TeacherPerformanceData>(`/grades/analysis/teacher/${encodeURIComponent(subject)}`);
  }

  async getStudentScheduleAnalysis(studentId: string): Promise<Record<string, unknown>> {
    return await fetchApi<Record<string, unknown>>(`/grades/analysis/schedule/${studentId}`);
  }

  async getClassScheduleAnalysis(className: string): Promise<Record<string, unknown>> {
    return await fetchApi<Record<string, unknown>>(`/grades/analysis/class/schedule/${encodeURIComponent(className)}`);
  }

  async getIntermediateResults(analysisId: string, step?: string): Promise<IntermediateResult[]> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (step) {
      params.append('step', step);
    }
    return await fetchApi<IntermediateResult[]>(`/analysis/intermediate-results?${params.toString()}`);
  }

  async getModelState(analysisId: string, modelName?: string): Promise<ModelState> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (modelName) {
      params.append('model_name', modelName);
    }
    return await fetchApi<ModelState>(`/analysis/model-state?${params.toString()}`);
  }

  async getConclusions(analysisId: string, level?: string): Promise<Conclusion[]> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (level) {
      params.append('level', level);
    }
    return await fetchApi<Conclusion[]>(`/analysis/conclusions?${params.toString()}`);
  }

  async getAnalysisLogs(analysisType?: string, startTime?: string, endTime?: string): Promise<AnalysisLog[]> {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    if (startTime) {
      params.append('start_time', startTime);
    }
    if (endTime) {
      params.append('end_time', endTime);
    }
    return await fetchApi<AnalysisLog[]>(`/analysis/logs?${params.toString()}`);
  }

  async getProcessVisualization(analysisId: string, processType: string): Promise<ProcessVisualizationData> {
    return await fetchApi<ProcessVisualizationData>('/analysis/process-visualization', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ analysis_id: analysisId, process_type: processType })
    });
  }

  async getAnalysisHistory(analysisType?: string, limit?: number): Promise<AnalysisHistory[]> {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    if (limit) {
      params.append('limit', limit.toString());
    }
    return await fetchApi<AnalysisHistory[]>(`/analysis/history?${params.toString()}`);
  }

  // 决策可视化相关API

  async getKnowledgeDiscoveries(classId?: string, limit?: number): Promise<KnowledgeDiscoveryResponse> {
    const params = new URLSearchParams();
    if (classId) {
      params.append('class_id', classId);
    }
    if (limit) {
      params.append('limit', limit.toString());
    }
    return await fetchApi<KnowledgeDiscoveryResponse>(`/analysis/knowledge-discoveries?${params.toString()}`);
  }

  async getFeatureImportance(classId?: string, analysisType?: string): Promise<FeatureImportanceResponse> {
    const params = new URLSearchParams();
    if (classId) {
      params.append('class_id', classId);
    }
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    return await fetchApi<FeatureImportanceResponse>(`/analysis/feature-importance?${params.toString()}`);
  }

  async getDecisionTreePath(classId?: string, studentId?: string, analysisType?: string): Promise<DecisionTreePathResponse> {
    return await fetchApi<DecisionTreePathResponse>('/analysis/decision-tree-path', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        class_id: classId,
        student_id: studentId,
        analysis_type: analysisType || 'class'
      })
    });
  }

  async getFactorImpact(classId?: string, analysisType?: string): Promise<FactorImpactResponse> {
    const params = new URLSearchParams();
    if (classId) {
      params.append('class_id', classId);
    }
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    return await fetchApi<FactorImpactResponse>(`/analysis/factor-impact?${params.toString()}`);
  }

  // 新增API方法

  async executeAnalysis(classIds: string[], analysisType: string = 'class'): Promise<ExecuteAnalysisResponse> {
    return await fetchApi<ExecuteAnalysisResponse>('/analysis/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ class_ids: classIds, analysis_type: analysisType })
    });
  }

  async getETLStatus(analysisId: string): Promise<ETLStatusResponse> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    return await fetchApi<ETLStatusResponse>(`/analysis/etl-status?${params.toString()}`);
  }

  async compareClasses(classIds: string[], metrics?: string[], examId?: string, subject?: string): Promise<ClassCompareResponse> {
    const body: Record<string, unknown> = { class_ids: classIds };
    if (metrics) body.metrics = metrics;
    if (examId) body.exam_id = examId;
    if (subject) body.subject = subject;

    return await fetchApi<ClassCompareResponse>('/analysis/class-compare', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
  }

  async getRealtimeDiscoveries(classId?: string, limit?: number): Promise<RealtimeDiscoveriesResponse> {
    const params = new URLSearchParams();
    if (classId) {
      params.append('class_id', classId);
    }
    if (limit) {
      params.append('limit', limit.toString());
    }
    return await fetchApi<RealtimeDiscoveriesResponse>(`/analysis/discoveries/realtime?${params.toString()}`);
  }

  // 学科分析API

  async getSubjectAnalysis(classId: string, subjects?: string[]): Promise<SubjectAnalysisResponse> {
    const params = new URLSearchParams();
    params.append('class_id', classId);
    if (subjects && subjects.length > 0) {
      params.append('subjects', subjects.join(','));
    }
    return await fetchApi<SubjectAnalysisResponse>(`/analysis/subject-analysis?${params.toString()}`);
  }

  async compareSubjects(classId: string, subjects: string[]): Promise<SubjectComparisonResponse> {
    return await fetchApi<SubjectComparisonResponse>('/analysis/subject-comparison', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ class_id: classId, subjects })
    });
  }

  // 获取班级教师信息
  async getClassTeachers(classId: string): Promise<ClassTeachersResponse> {
    const params = new URLSearchParams();
    params.append('class_id', classId);
    return await fetchApi<ClassTeachersResponse>(`/analysis/class-teachers?${params.toString()}`);
  }

  // 获取班级详细成绩分析
  async getClassGradeDetail(classId: string, subject?: string, examId?: string, displayMode?: string): Promise<ClassGradeDetailResponse> {
    const params = new URLSearchParams();
    params.append('class_id', classId);
    if (subject) {
      params.append('subject', subject);
    }
    if (examId) {
      params.append('exam_id', examId);
    }
    if (displayMode) {
      params.append('display_mode', displayMode);
    }
    return await fetchApi<ClassGradeDetailResponse>(`/analysis/class-grade-detail?${params.toString()}`);
  }

  // 获取考试列表
  async getExamList(grade?: string): Promise<ExamInfo[]> {
    const params = new URLSearchParams();
    if (grade) {
      params.append('grade', grade);
    }
    const response = await fetchApi<ExamInfo[]>(`/exams/?${params.toString()}`);
    return response;
  }

  // 获取学生参与的所有考试列表
  async getStudentExamList(studentId: string, examCode?: string): Promise<StudentExamListResponse> {
    const params = new URLSearchParams();
    params.append('student_id', studentId);
    if (examCode) {
      params.append('exam_code', examCode);
    }
    return await fetchApi<StudentExamListResponse>(`/exams/student-exams?${params.toString()}`);
  }

  // 获取学生特定考试的详细成绩信息
  async getStudentExamDetail(studentId: string, examCode: string): Promise<StudentExamDetailResponse> {
    const params = new URLSearchParams();
    params.append('student_id', studentId);
    params.append('exam_code', examCode);
    return await fetchApi<StudentExamDetailResponse>(`/exams/student-exams/detail?${params.toString()}`);
  }
}

// 学科分析相关类型
export interface SubjectDistribution {
  excellent: number;
  good: number;
  average: number;
  pass: number;
  fail: number;
}

export interface SubjectDetail {
  subject: string;
  average_score: number;
  excellent_rate: number;
  pass_rate: number;
  std_deviation: number;
  max_score: number;
  min_score: number;
  median: number;
  distribution: SubjectDistribution;
}

export interface StrengthSubject {
  subject: string;
  average: number;
  reason: string;
}

export interface WeaknessSubject {
  subject: string;
  average: number;
  reason: string;
}

export interface AnalysisSummary {
  class_id: string;
  overall_average: number;
  subject_count: number;
  strong_subjects: StrengthSubject[];
  weak_subjects: WeaknessSubject[];
  suggestions: string[];
}

export interface SubjectAnalysisResponse {
  analysis_summary: AnalysisSummary;
  subject_details: SubjectDetail[];
  algorithm: string;
  method: string;
  generated_at: string;
}

export interface SubjectComparison {
  subject: string;
  average_diff: number;
  average_percentage: number;
  excellent_diff: number;
  pass_diff: number;
}

export interface SubjectComparisonResponse {
  class_id: string;
  base_subject: SubjectDetail;
  comparisons: SubjectComparison[];
  subjects: string[];
  generated_at: string;
}

// 班级教师信息相关类型
export interface TeacherInfo {
  teacher_id: string;
  name: string;
  title: string;
  subject?: string;
  is_homeroom?: boolean;
}

export interface ClassTeachersResponse {
  class_id: string;
  teachers: TeacherInfo[];
  homeroom_teacher: TeacherInfo | null;
  generated_at: string;
}

// 考试相关类型
export interface ExamInfo {
  id: string;
  code: string;
  name: string;
  type: string;
  grade: string;
  academicYear: string;
  semester: string;
  startDate?: string;
  endDate?: string;
  status: string;
}

export interface ExamListResponse {
  exams: ExamInfo[];
  total: number;
}

// 学生考试信息相关类型
export interface StudentExamInfo {
  examCode: string;
  examName: string;
  academicYear: string;
  semester: string;
  grade: string;
  examType: string;
  startDate: string;
  endDate: string;
  status: string;
  subjects: string[];
  averageScore: number | null;
  totalSubjects: number;
  examLocation: string | null;
  specialNotes: string | null;
}

export interface StudentExamListResponse {
  studentId: string;
  studentName: string;
  studentClass: string;
  grade: string;
  exams: StudentExamInfo[];
  totalExams: number;
}

export interface StudentGradeDetail {
  subject: string;
  score: number;
  gradeLevel: string;
  pass: boolean;
  excellent: boolean;
}

export interface StudentExamStatistics {
  totalSubjects: number;
  averageScore: number;
  maxScore: number;
  minScore: number;
  passRate: number;
  excellentRate: number;
  passCount: number;
  excellentCount: number;
}

export interface StudentExamDetail {
  studentId: string;
  studentName: string;
  studentClass: string;
  exam: ExamInfo;
  grades: StudentGradeDetail[];
  statistics: StudentExamStatistics;
}

export interface StudentExamDetailResponse extends StudentExamDetail {
  message?: string;
}

// 班级详细成绩分析相关类型
export interface ClassGradeDistribution {
  excellent: number;
  good: number;
  average: number;
  pass: number;
  fail: number;
}

export interface ClassGradeDetail {
  class_id: string;
  subject: string;
  total_students: number;
  total_scores: number;
  average_score: number;
  max_score: number;
  min_score: number;
  std_deviation: number;
  pass_rate: number;
  excellent_rate: number;
  distribution: ClassGradeDistribution;
  rule_type?: string;
  thresholds?: {
    excellent: number;
    good: number;
    average: number;
    pass: number;
  };
}

export interface ClassGradeDetailResponse {
  detail: ClassGradeDetail | null;
  error?: string;
  generated_at: string;
}

export const gradeService = new GradeService();
