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
    return await fetchApi<IntermediateResult[]>(`/api/analysis/intermediate-results?${params.toString()}`);
  }
  
  async getModelState(analysisId: string, modelName?: string): Promise<ModelState> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (modelName) {
      params.append('model_name', modelName);
    }
    return await fetchApi<ModelState>(`/api/analysis/model-state?${params.toString()}`);
  }
  
  async getConclusions(analysisId: string, level?: string): Promise<Conclusion[]> {
    const params = new URLSearchParams();
    params.append('analysis_id', analysisId);
    if (level) {
      params.append('level', level);
    }
    return await fetchApi<Conclusion[]>(`/api/analysis/conclusions?${params.toString()}`);
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
    return await fetchApi<AnalysisLog[]>(`/api/analysis/logs?${params.toString()}`);
  }
  
  async getProcessVisualization(analysisId: string, processType: string): Promise<ProcessVisualizationData> {
    return await fetchApi<ProcessVisualizationData>('/api/analysis/process-visualization', {
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
    return await fetchApi<AnalysisHistory[]>(`/api/analysis/history?${params.toString()}`);
  }
  
  // 决策可视化相关API
  
  async getKnowledgeDiscoveries(className?: string, limit?: number): Promise<KnowledgeDiscoveryResponse> {
    const params = new URLSearchParams();
    if (className) {
      params.append('class_name', className);
    }
    if (limit) {
      params.append('limit', limit.toString());
    }
    return await fetchApi<KnowledgeDiscoveryResponse>(`/api/analysis/knowledge-discoveries?${params.toString()}`);
  }
  
  async getFeatureImportance(analysisType?: string): Promise<FeatureImportanceResponse> {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    return await fetchApi<FeatureImportanceResponse>(`/api/analysis/feature-importance?${params.toString()}`);
  }
  
  async getDecisionTreePath(className?: string, studentId?: string, analysisType?: string): Promise<DecisionTreePathResponse> {
    return await fetchApi<DecisionTreePathResponse>('/api/analysis/decision-tree-path', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        class_name: className, 
        student_id: studentId,
        analysis_type: analysisType || 'class'
      })
    });
  }
  
  async getFactorImpact(analysisType?: string): Promise<FactorImpactResponse> {
    const params = new URLSearchParams();
    if (analysisType) {
      params.append('analysis_type', analysisType);
    }
    return await fetchApi<FactorImpactResponse>(`/api/analysis/factor-impact?${params.toString()}`);
  }
}

export const gradeService = new GradeService();
