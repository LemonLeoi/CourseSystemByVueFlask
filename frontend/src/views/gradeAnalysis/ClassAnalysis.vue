<template>
  <div class="class-analysis">
    <h3>班级成绩分析</h3>
    <div class="class-input">
      <!-- 复用班级选择器组件 -->
      <ClassSelector 
        v-model="className" 
        @change="onClassChange"
      />
      
      <!-- 复用考试选择器组件 -->
      <ExamSelector 
        v-model="selectedExam" 
        :parent-value="className"
        class="exam-select-wrapper"
      />
      
      <button 
        @click="analyzeClass"
        :disabled="!className || !selectedExam || loading"
        :class="{ disabled: !className || !selectedExam || loading }"
      >
        {{ loading ? '分析中...' : '分析' }}
      </button>
    </div>
    
    <LoadingAnimator
      v-if="loading || classError"
      :status="classError ? 'error' : 'loading'"
      :message="`正在分析 ${className} 的成绩...`"
      :loading-step="loadingStep"
      :error-message="'数据加载失败'"
      :error-details="classError"
      :hints="analysisHints"
      :retryable="true"
      size="large"
      @retry="analyzeClass"
    />
    <div v-else-if="classAnalysis && classAnalysis.class_info" class="class-analysis-result">
      <!-- 分析过程展示 -->
      <CollapsibleSection 
        title="分析过程" 
        icon="🏫" 
        :default-collapsed="false"
        storage-key="analysis_process"
      >
        <AnalysisProcessVisualizer
          :process-steps="analysisProcessSteps"
          :current-step="currentAnalysisStep"
          :data-flow="analysisDataFlow"
          :calculations="analysisCalculations"
        />
      </CollapsibleSection>
      
      <!-- 决策树参数配置 -->
      <CollapsibleSection 
        title="决策树参数配置" 
        icon="⚙️"
        :default-collapsed="true"
        storage-key="decision_tree_config"
      >
        <DecisionTreeConfig @config-updated="handleConfigUpdated" />
      </CollapsibleSection>
      
      <CollapsibleSection 
        title="班级信息" 
        icon="🏫" 
        :default-collapsed="false"
        storage-key="class_info"
      >
        <p>班级名称: {{ classAnalysis.class_info.class_name }}</p>
        <p>年级: {{ classAnalysis.class_info.grade }}</p>
        <p>学生人数: {{ classAnalysis.class_info.student_count }}</p>
        <p>班级平均成绩: {{ classAnalysis.overall_average }}</p>
      </CollapsibleSection>
      
      <CollapsibleSection 
        title="学科平均成绩" 
        icon="📊"
        storage-key="class_subject_analysis"
      >
        <BaseECharts
          chart-type="bar"
          :data="{ subjectAverages }"
          :options="classSubjectOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：学科选择模块 -->
      <div class="subject-selector-section">
        <div class="section-header-bar">
          <div class="section-icon">📚</div>
          <div class="section-title-area">
            <h3 class="section-main-title">成绩分析</h3>
            <p class="section-subtitle">Grade Analysis</p>
          </div>
        </div>
        
        <div class="analysis-type-selector">
          <div class="selector-label">分析类型:</div>
          <div class="analysis-type-tabs">
            <button 
              class="tab-btn" 
              :class="{ active: analysisType === 'all' }"
              @click="switchAnalysisType('all')"
            >
              所有学科综合分析
            </button>
            <button 
              class="tab-btn" 
              :class="{ active: analysisType === 'single' }"
              @click="switchAnalysisType('single')"
            >
              特定学科分析
            </button>
          </div>
        </div>
        
        <div v-if="analysisType === 'single'" class="subject-selector">
          <div class="selector-label">选择学科:</div>
          <select v-model="selectedSubject" class="filter-select" @change="analyzeSubject">
            <option value="">请选择科目</option>
            <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
          </select>
        </div>
        
        <!-- 详细成绩指标展示 - 复用GradeStatsPanel组件 -->
        <GradeStatsPanel v-if="gradeDetail" :grade-detail="gradeDetail" />
        
        <!-- 无数据提示 -->
        <div v-if="gradeDetail === null" class="empty-data-panel error">
          <div class="empty-icon">⚠️</div>
          <p>暂无该班级或学科的成绩数据</p>
          <p class="error-hint">请检查数据库中是否存在相关成绩记录</p>
        </div>
      </div>
      
      <!-- 新增：具体科目分析模块 -->
      <CollapsibleSection 
        v-if="subjectAnalysis" 
        :title="selectedSubject + ' 科目分析'" 
        icon="📊"
        storage-key="specific_class_subject_analysis"
      >
        <div class="subject-stats">
          <div class="stat-item">
            <span class="stat-label">平均成绩:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.average }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">中位数:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.median }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">标准差:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.std_deviation }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最高分:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.max_score }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最低分:</span>
            <span class="stat-value">{{ subjectAnalysis.statistics.min_score }}</span>
          </div>
        </div>
        <BaseECharts
          chart-type="bar"
          :data="subjectAnalysis"
          :options="subjectDistributionOptions"
          height="400px"
        />
        <BaseECharts
          chart-type="boxplot"
          :data="subjectAnalysis"
          :options="subjectBoxPlotOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：历次考试趋势图表 -->
      <CollapsibleSection 
        title="班级历次考试趋势" 
        icon="📈"
        storage-key="class_exam_trend"
      >
        <GradeTrendAnalysis
          :data="examTrend"
          :loading="loading"
          :error="error"
          :available-subjects="availableSubjects"
          v-model="selectedTrendSubject"
          @subject-change="handleTrendSubjectChange"
        />
      </CollapsibleSection>
      
      <!-- 决策逻辑可视化模块 -->
      <div class="decision-visualization-section">
        <div class="section-header-bar">
          <div class="section-icon">🔍</div>
          <div class="section-title-area">
            <h3 class="section-main-title">决策逻辑可视化</h3>
            <p class="section-subtitle">Decision Logic Visualization</p>
          </div>
        </div>
        
        <!-- 决策逻辑链条 -->
        <div class="decision-chain">
          <div class="chain-item">
            <div class="chain-node">
              <span class="node-icon">📊</span>
              <span class="node-label">数据输入</span>
            </div>
          </div>
          <div class="chain-arrow">→</div>
          <div class="chain-item">
            <div class="chain-node highlight">
              <span class="node-icon">🌳</span>
              <span class="node-label">C4.5算法运算</span>
            </div>
          </div>
          <div class="chain-arrow">→</div>
          <div class="chain-item">
            <div class="chain-node">
              <span class="node-icon">📈</span>
              <span class="node-label">信息增益比排序</span>
            </div>
          </div>
          <div class="chain-arrow">→</div>
          <div class="chain-item">
            <div class="chain-node">
              <span class="node-icon">💡</span>
              <span class="node-label">决策规则输出</span>
            </div>
          </div>
        </div>
        
        <!-- 特征重要性分析 -->
        <CollapsibleSection 
          title="特征重要性分析" 
          icon="📊"
          :default-collapsed="false"
          storage-key="feature_importance"
        >
          <FeatureImportanceChart :data="featureImportanceData" />
        </CollapsibleSection>
        
        <!-- 决策路径分析 -->
        <CollapsibleSection 
          title="决策路径分析" 
          icon="🌳"
          :default-collapsed="true"
          storage-key="decision_path"
        >
          <DecisionTreePath 
            :paths="decisionTreePathsData" 
            :factor-impact="factorImpactAnalysisData"
            @refresh="refreshDecisionTree"
            ref="decisionTreePathRef"
          />
        </CollapsibleSection>
        
        <!-- 挖掘发现 -->
        <CollapsibleSection 
          title="挖掘发现" 
          icon="💡"
          :default-collapsed="false"
          storage-key="knowledge_discovery"
        >
          <KnowledgeDiscoveryList :class-id="className" />
        </CollapsibleSection>
      </div>
      
      <!-- 学科分析模块 -->
      <div class="subject-analysis-section">
        <div class="section-header-bar">
          <div class="section-icon">📚</div>
          <div class="section-title-area">
            <h3 class="section-main-title">学科分析</h3>
            <p class="section-subtitle">Subject Analysis</p>
          </div>
        </div>
        
        <CollapsibleSection 
          title="学科优劣势分析" 
          icon="📊"
          :default-collapsed="false"
          storage-key="subject_strength_analysis"
        >
          <SubjectStrengthAnalysis 
            :data="subjectStrengthData" 
            :loading="isSubjectAnalysisLoading" 
            :error="subjectAnalysisError"
          />
        </CollapsibleSection>
        
        <!-- 学科对比分析 -->
        <CollapsibleSection 
          title="学科对比分析" 
          icon="🔄"
          :default-collapsed="true"
          storage-key="subject_comparison"
        >
          <div class="subject-comparison-selector">
            <select v-model="subjectCompare1" class="filter-select">
              <option value="">请选择第一个学科</option>
              <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
            </select>
            <span class="comparison-arrow">vs</span>
            <select v-model="subjectCompare2" class="filter-select">
              <option value="">请选择第二个学科</option>
              <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
            </select>
            <button class="compare-subjects-btn" @click="compareSubjects">对比</button>
          </div>
          <div v-if="subjectComparisonData" class="subject-comparison-result">
            <BaseECharts
              chart-type="bar"
              :data="subjectComparisonData"
              :options="subjectComparisonOptions"
              height="300px"
            />
            <div class="comparison-summary">
              <div class="summary-item">
                <span class="summary-label">平均分差异:</span>
                <span class="summary-value" :class="subjectComparisonData.diff >= 0 ? 'positive' : 'negative'">
                  {{ subjectComparisonData.diff >= 0 ? '+' : '' }}{{ subjectComparisonData.diff }}
                </span>
              </div>
              <div class="summary-item">
                <span class="summary-label">优秀率差异:</span>
                <span class="summary-value" :class="subjectComparisonData.excellent_diff >= 0 ? 'positive' : 'negative'">
                  {{ subjectComparisonData.excellent_diff >= 0 ? '+' : '' }}{{ subjectComparisonData.excellent_diff }}%
                </span>
              </div>
              <div class="summary-item">
                <span class="summary-label">及格率差异:</span>
                <span class="summary-value" :class="subjectComparisonData.pass_diff >= 0 ? 'positive' : 'negative'">
                  {{ subjectComparisonData.pass_diff >= 0 ? '+' : '' }}{{ subjectComparisonData.pass_diff }}%
                </span>
              </div>
            </div>
          </div>
        </CollapsibleSection>
      </div>
      
      <!-- 班级对比分析模块 -->
      <div class="class-comparison-section">
        <div class="section-header-bar">
          <div class="section-icon">👥</div>
          <div class="section-title-area">
            <h3 class="section-main-title">班级对比分析</h3>
            <p class="section-subtitle">Class Comparison</p>
          </div>
        </div>
        
        <ClassComparePanel :currentClass="className" />
      </div>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../../components/common/BaseECharts.vue';
import CollapsibleSection from '../../components/common/CollapsibleSection.vue';
import AnalysisProcessVisualizer from '../../components/common/AnalysisProcessVisualizer.vue';
import LoadingAnimator from '../../components/common/LoadingAnimator.vue';
import ClassSelector from '../../components/common/ClassSelector.vue';
import ExamSelector from '../../components/common/ExamSelector.vue';
import GradeStatsPanel from '../../components/common/GradeStatsPanel.vue';
import KnowledgeDiscoveryList from '../../components/grade/KnowledgeDiscoveryList.vue';
import FeatureImportanceChart from '../../components/grade/FeatureImportanceChart.vue';
import DecisionTreePath from '../../components/grade/DecisionTreePath.vue';
import SubjectStrengthAnalysis from '../../components/grade/SubjectStrengthAnalysis.vue';
import ClassComparePanel from '../../components/grade/ClassComparePanel.vue';
import GradeTrendAnalysis from '../../components/grade/GradeTrendAnalysis.vue';
import DecisionTreeConfig from '../../components/grade/DecisionTreeConfig.vue';
import { ref, onMounted, watch, computed } from 'vue';
import { useClassGrade } from '../../composables/grade/useClassGrade';
import { gradeService } from '../../services/gradeService';

export default {
  name: 'ClassAnalysis',
  components: {
    BaseECharts,
    CollapsibleSection,
    AnalysisProcessVisualizer,
    LoadingAnimator,
    ClassSelector,
    ExamSelector,
    GradeStatsPanel,
    KnowledgeDiscoveryList,
    FeatureImportanceChart,
    DecisionTreePath,
    SubjectStrengthAnalysis,
    ClassComparePanel,
    GradeTrendAnalysis,
    DecisionTreeConfig
  },
  setup() {
    const {
      classInfo,
      subjectAverages,
      overallAverage,
      studentCount,
      subjectAnalysis,
      examTrend,
      loading,
      error,
      getClassAnalysis,
      getClassSubjectAnalysis,
      getClassTrend
    } = useClassGrade();
    
    const className = ref('');
    const classes = ref([]);
    const grades = ref([]);
    const isLoadingOptions = ref(false);
    const selectedSubject = ref('');
    const subjects = ref([]);
    
    // 考试相关数据
    const exams = ref([]);
    const selectedExam = ref('');
    
    // 显示模式
    const displayMode = ref('score'); // 'score' 或 'percentage'
    
    // 趋势分析相关
    const selectedTrendSubject = ref('all');
    const availableSubjects = computed(() => {
      if (examTrend.value && examTrend.value.available_subjects) {
        return examTrend.value.available_subjects;
      }
      return [];
    });
    
    // 决策可视化相关数据（从API获取）
    const knowledgeDiscoveriesData = ref([]);
    const featureImportanceData = ref([]);
    const decisionTreePathsData = ref([]);
    const factorImpactAnalysisData = ref([]);
    const decisionTreePathRef = ref();
    
    // 学科分析相关数据
    const subjectStrengthData = ref(null);
    const isSubjectAnalysisLoading = ref(false);
    const subjectAnalysisError = ref('');
    
    // 学科对比相关数据
    const subjectCompare1 = ref('');
    const subjectCompare2 = ref('');
    const subjectComparisonData = ref(null);
    
    // 分析类型（综合分析/单学科分析）
    const analysisType = ref('all');
    
    // 班级详细成绩分析数据
    const gradeDetail = ref(null);
    
    // 班级教师信息
    const classTeachers = ref(null);
    
    // 分析过程相关状态
    const loadingStep = ref('正在获取班级成绩数据，请稍候...');
    const analysisProcessSteps = ref([
      {
        title: '数据获取',
        description: '从数据库中提取班级的基本信息和所有学生的成绩记录',
        details: {
          data_source: '学生成绩数据库',
          tables: ['students', 'grades', 'exams', 'classrooms'],
          method: '通过GradeDataAccess.get_class_grades获取班级成绩数据'
        }
      },
      {
        title: '数据预处理',
        description: '清理和整理原始数据，确保数据质量',
        details: {
          steps: ['数据清洗', '缺失值处理', '数据标准化'],
          method: '使用数据预处理函数处理原始成绩数据'
        }
      },
      {
        title: '统计分析',
        description: '计算班级各项统计指标，如平均分、中位数、标准差等',
        details: {
          metrics: ['班级平均分', '中位数', '标准差', '最高分', '最低分'],
          method: '使用statistical_analysis.py中的函数进行计算'
        }
      },
      {
        title: '学科分析',
        description: '分析班级各学科的表现',
        details: {
          method: '计算各学科的平均成绩和分布情况',
          metrics: ['学科平均分', '成绩分布', '标准差']
        }
      },
      {
        title: '趋势分析',
        description: '分析班级历次考试的成绩变化趋势',
        details: {
          method: '使用时间序列分析方法',
          metrics: ['成绩趋势', '进步幅度', '稳定性']
        }
      },
      {
        title: '结果生成',
        description: '综合分析结果，生成最终报告',
        details: {
          method: '整合各项分析结果',
          output: '班级成绩分析报告'
        }
      }
    ]);
    const currentAnalysisStep = ref(0);
    const analysisDataFlow = ref({
      nodes: [
        { name: '原始数据', type: 'source', description: '从数据库提取的班级原始成绩数据' },
        { name: '数据处理', type: 'process', description: '清洗、整理和标准化数据' },
        { name: '分析结果', type: 'result', description: '生成班级分析报告' }
      ],
      connections: [
        { from: 0, to: 1 },
        { from: 1, to: 2 }
      ]
    });
    const analysisCalculations = ref([
      {
        name: '班级平均分计算',
        formula: '班级总分 / 班级总人数',
        result: '计算班级所有学生的平均分数'
      },
      {
        name: '学科平均分计算',
        formula: '学科总分 / 学生人数',
        result: '计算班级各学科的平均分数'
      },
      {
        name: '标准差计算',
        formula: 'sqrt(sum((x - μ)^2) / n)',
        result: '计算班级成绩的离散程度'
      },
      {
        name: '成绩分布计算',
        formula: '按分数段统计人数',
        result: '计算班级成绩在各分数段的分布情况'
      }
    ]);
    
    // 加载提示数组
    const analysisHints = ref([
      '正在获取班级成绩数据...',
      '正在预处理数据...',
      '正在计算班级统计指标...',
      '正在分析学科表现...',
      '正在生成班级趋势图表...',
      '即将完成分析...'
    ]);
    
    // 图表引用
    const classSubjectChart = ref(null);
    const subjectDistributionChart = ref(null);
    const subjectBoxPlotChart = ref(null);
    const examTrendChart = ref(null);
    
    // 图表实例
    let classSubjectChartInstance = null;
    let subjectDistributionChartInstance = null;
    let subjectBoxPlotChartInstance = null;
    let examTrendChartInstance = null;
    
    // ECharts 实例
    let echarts = null;
    
    // 动态导入 ECharts
    const loadECharts = async () => {
      try {
        const echartsCore = await import('echarts/core');
        const charts = await import('echarts/charts');
        const components = await import('echarts/components');
        const renderers = await import('echarts/renderers');
        
        const { use, init } = echartsCore;
        const { BarChart, LineChart, RadarChart, PieChart, BoxplotChart } = charts;
        const { 
          TitleComponent, TooltipComponent, LegendComponent, 
          GridComponent, DataZoomComponent, ToolboxComponent,
          VisualMapComponent
        } = components;
        const { CanvasRenderer } = renderers;
        
        use([
          BarChart, LineChart, RadarChart, PieChart, BoxplotChart,
          TitleComponent, TooltipComponent, LegendComponent, GridComponent,
          DataZoomComponent, ToolboxComponent, VisualMapComponent,
          CanvasRenderer
        ]);
        
        echarts = echartsCore;
        return true;
      } catch (err) {
        console.error('加载 ECharts 失败:', err);
        return false;
      }
    };
    
    // 获取分析数据（从API）
    const fetchAnalysisData = async (classId) => {
      try {
        // 获取特征重要性
        const featureImportanceResponse = await gradeService.getFeatureImportance(classId);
        featureImportanceData.value = featureImportanceResponse.feature_importance || [];
        
        // 获取决策树配置和路径
        const configResponse = await gradeService.getDecisionTreeConfig();
        const decisionTreeResponse = await gradeService.getDecisionTreePath(
          classId,
          undefined,
          'class',
          configResponse.params
        );
        decisionTreePathsData.value = decisionTreeResponse.paths || [];
        
        // 获取因素影响分析
        const factorImpactResponse = await gradeService.getFactorImpact(classId);
        factorImpactAnalysisData.value = factorImpactResponse.factor_impact || [];
        
        // 获取挖掘发现
        const discoveriesResponse = await gradeService.getKnowledgeDiscoveries(classId);
        knowledgeDiscoveriesData.value = discoveriesResponse.discoveries || [];
        
        // 获取学科分析数据
        await fetchSubjectAnalysis(classId);
      } catch (error) {
        console.error('获取分析数据失败:', error);
      }
    };
    
    // 刷新决策树分析
    const refreshDecisionTree = async () => {
      try {
        const configResponse = await gradeService.getDecisionTreeConfig();
        const decisionTreeResponse = await gradeService.getDecisionTreePath(
          className.value,
          undefined,
          'class',
          configResponse.params
        );
        decisionTreePathsData.value = decisionTreeResponse.paths || [];
        
        const factorImpactResponse = await gradeService.getFactorImpact(className.value);
        factorImpactAnalysisData.value = factorImpactResponse.factor_impact || [];
      } catch (error) {
        console.error('重新分析决策路径失败:', error);
      } finally {
        if (decisionTreePathRef.value) {
          decisionTreePathRef.value.setRefreshing(false);
        }
      }
    };
    
    // 切换分析类型
    const switchAnalysisType = async (type) => {
      analysisType.value = type;
      selectedSubject.value = '';
      await fetchGradeDetail(className.value, type === 'all' ? undefined : undefined);
    };
    
    // 获取班级详细成绩分析数据
    const fetchGradeDetail = async (classId, subject) => {
      try {
        const examId = selectedExam.value === 'all' ? undefined : selectedExam.value;
        const response = await gradeService.getClassGradeDetail(classId, subject, examId, displayMode.value);
        gradeDetail.value = response.detail;
      } catch (error) {
        console.error('获取班级详细成绩分析失败:', error);
        gradeDetail.value = null;
      }
    };
    
    // 切换显示模式
    const toggleDisplayMode = () => {
      displayMode.value = displayMode.value === 'score' ? 'percentage' : 'score';
      if (className.value) {
        fetchGradeDetail(className.value, selectedSubject.value);
      }
    };
    
    // 处理决策树配置更新
    const handleConfigUpdated = async (params) => {
      console.log('决策树配置更新:', params);
      if (className.value) {
        try {
          const decisionTreeResponse = await gradeService.getDecisionTreePath(
            className.value,
            undefined,
            'class',
            params
          );
          decisionTreePathsData.value = decisionTreeResponse.paths || [];
          console.log('决策树路径已更新');
        } catch (error) {
          console.error('更新决策树路径失败:', error);
        }
      }
    };
    
    // 加载考试列表
    const loadExamList = async (grade = '') => {
      try {
        const examList = await gradeService.getExamList(grade);
        exams.value = examList || [];
      } catch (error) {
        console.error('获取考试列表失败:', error);
        exams.value = [];
      }
    };
    
    // 班级变化时重新加载考试列表
    const onClassChange = () => {
      if (className.value) {
        const grade = className.value.slice(0, 2);
        loadExamList(grade);
        selectedExam.value = '';
      } else {
        exams.value = [];
        selectedExam.value = '';
      }
    };
    
    // 获取班级教师信息
    const fetchClassTeachers = async (classId) => {
      try {
        const response = await gradeService.getClassTeachers(classId);
        classTeachers.value = response;
      } catch (error) {
        console.error('获取班级教师信息失败:', error);
        classTeachers.value = null;
      }
    };
    
    // 计算分数分布宽度
    const getDistributionWidth = (value) => {
      if (!gradeDetail.value) return 0;
      const total = gradeDetail.value.total_students;
      return total > 0 ? (value / total) * 100 : 0;
    };
    
    // 动态生成分数分布标签
    const barLabels = computed(() => {
      if (!gradeDetail.value) {
        return {
          excellent: '优秀(≥90)',
          good: '良好(80-89)',
          average: '中等(70-79)',
          pass: '及格(60-69)',
          fail: '不及格(<60)'
        };
      }
      
      const thresholds = gradeDetail.value.thresholds;
      const percentageThresholds = gradeDetail.value.percentage_thresholds;
      
      if (displayMode.value === 'percentage') {
        // 得分率模式
        const excellent = percentageThresholds?.excellent || 90;
        const good = percentageThresholds?.good || 85;
        const average = percentageThresholds?.average || 75;
        const pass = percentageThresholds?.pass || 60;
        
        return {
          excellent: `优秀(≥${excellent}%)`,
          good: `良好(${good}%-${excellent - 1}%)`,
          average: `中等(${average}%-${good - 1}%)`,
          pass: `及格(${pass}%-${average - 1}%)`,
          fail: `不及格(<${pass}%)`
        };
      } else {
        // 具体分数模式
        const excellent = Math.round(thresholds?.excellent || 90);
        const good = Math.round(thresholds?.good || 80);
        const average = Math.round(thresholds?.average || 70);
        const pass = Math.round(thresholds?.pass || 60);
        
        return {
          excellent: `优秀(≥${excellent})`,
          good: `良好(${good}-${excellent - 1})`,
          average: `中等(${average}-${good - 1})`,
          pass: `及格(${pass}-${average - 1})`,
          fail: `不及格(<${pass})`
        };
      }
    });
    
    // 计算分数分布条形图样式
    const distributionBarStyles = computed(() => {
      if (!gradeDetail.value) return [];
      const total = gradeDetail.value.total_students;
      const dist = gradeDetail.value.distribution;
      return [
        { width: total > 0 ? (dist.excellent / total * 100) + '%' : '0%' },
        { width: total > 0 ? (dist.good / total * 100) + '%' : '0%' },
        { width: total > 0 ? (dist.average / total * 100) + '%' : '0%' },
        { width: total > 0 ? (dist.pass / total * 100) + '%' : '0%' },
        { width: total > 0 ? (dist.fail / total * 100) + '%' : '0%' }
      ];
    });
    
    // 获取学科分析数据
    const fetchSubjectAnalysis = async (classId) => {
      try {
        isSubjectAnalysisLoading.value = true;
        subjectAnalysisError.value = '';
        
        const response = await gradeService.getSubjectAnalysis(classId);
        
        if (response && response.analysis_summary) {
          const summary = response.analysis_summary;
          subjectStrengthData.value = {
            strengths: summary.strong_subjects.map(s => ({
              subject: s.subject,
              avg_score: s.average,
              class_avg: summary.overall_average,
              diff: (s.average - summary.overall_average).toFixed(1)
            })),
            weaknesses: summary.weak_subjects.map(w => ({
              subject: w.subject,
              avg_score: w.average,
              class_avg: summary.overall_average,
              diff: (w.average - summary.overall_average).toFixed(1)
            })),
            overall: {
              personal_avg: summary.overall_average,
              class_avg: summary.overall_average,
              diff: 0,
              evaluation: '班级整体成绩分析完成'
            }
          };
        }
      } catch (error) {
        console.error('获取学科分析数据失败:', error);
        subjectAnalysisError.value = '获取学科分析数据失败';
      } finally {
        isSubjectAnalysisLoading.value = false;
      }
    };
    
    // 学科对比
    const compareSubjects = async () => {
      if (!subjectCompare1.value || !subjectCompare2.value) {
        alert('请选择两个学科进行对比');
        return;
      }
      
      try {
        const response = await gradeService.compareSubjects(className.value, [subjectCompare1.value, subjectCompare2.value]);
        if (response && response.comparisons && response.comparisons.length > 0) {
          const comparison = response.comparisons[0];
          subjectComparisonData.value = {
            subjects: [subjectCompare1.value, subjectCompare2.value],
            diff: comparison.average_diff,
            excellent_diff: comparison.excellent_diff,
            pass_diff: comparison.pass_diff
          };
        }
      } catch (error) {
        console.error('学科对比失败:', error);
      }
    };
    
    // 加载班级和年级列表
    const loadClassOptions = async () => {
      isLoadingOptions.value = true;
      try {
        const { studentApi } = await import('../../services/api/apiService');
        const data = await studentApi.getClasses();
        grades.value = data.grades || [];
        classes.value = data.classes || [];
        
        const fullClasses = [];
        grades.value.forEach(grade => {
          classes.value.forEach(classNum => {
            const classNumMatch = classNum.match(/\d+/);
            const num = classNumMatch ? classNumMatch[0] : classNum;
            fullClasses.push(`${grade}${num}班`);
          });
        });
        classes.value = fullClasses;
      } catch (error) {
        console.error('获取班级和年级列表失败:', error);
        grades.value = ['高一', '高二', '高三'];
        classes.value = ['1班', '2班', '3班', '4班', '5班'];
        
        const fullClasses = [];
        grades.value.forEach(grade => {
          classes.value.forEach(classNum => {
            const classNumMatch = classNum.match(/\d+/);
            const num = classNumMatch ? classNumMatch[0] : classNum;
            fullClasses.push(`${grade}${num}班`);
          });
        });
        classes.value = fullClasses;
      } finally {
        isLoadingOptions.value = false;
      }
    };
    
    // 趋势分析科目变化处理
    const handleTrendSubjectChange = async (subject) => {
      if (className.value) {
        await getClassTrend(className.value, subject);
      }
    };
    
    // 分析班级成绩
    const analyzeClass = async () => {
      if (className.value) {
        currentAnalysisStep.value = 0;
        
        // 步骤1：数据获取
        loadingStep.value = '正在获取班级基本信息和学生成绩数据...';
        currentAnalysisStep.value = 0;
        await getClassAnalysis(className.value);
        
        // 步骤2：数据预处理
        loadingStep.value = '正在预处理数据，确保数据质量...';
        currentAnalysisStep.value = 1;
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 步骤3：统计分析
        loadingStep.value = '正在计算班级统计指标，如平均分、中位数、标准差等...';
        currentAnalysisStep.value = 2;
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 步骤4：学科分析
        loadingStep.value = '正在分析班级各学科表现...';
        currentAnalysisStep.value = 3;
        if (subjectAverages.value) {
          subjects.value = Object.keys(subjectAverages.value);
        }
        
        // 步骤5：趋势分析
        loadingStep.value = '正在分析班级历次考试的成绩变化趋势...';
        currentAnalysisStep.value = 4;
        await getClassTrend(className.value, selectedTrendSubject.value);
        
        // 步骤6：获取决策分析数据
        loadingStep.value = '正在获取决策分析数据...';
        currentAnalysisStep.value = 5;
        await fetchAnalysisData(className.value);
        
        // 步骤7：获取详细成绩分析数据
        loadingStep.value = '正在获取详细成绩分析数据...';
        currentAnalysisStep.value = 6;
        await fetchGradeDetail(className.value);
        
        // 步骤8：获取班级教师信息
        loadingStep.value = '正在获取班级教师信息...';
        await fetchClassTeachers(className.value);
        
        // 步骤9：结果生成
        loadingStep.value = '正在生成分析报告...';
        currentAnalysisStep.value = 7;
        await new Promise(resolve => setTimeout(resolve, 300));
        
        currentAnalysisStep.value = 8;
      }
    };
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (className.value && selectedSubject.value) {
        await getClassSubjectAnalysis(className.value, selectedSubject.value);
        // 获取详细成绩分析数据
        await fetchGradeDetail(className.value, selectedSubject.value);
      } else if (className.value && !selectedSubject.value && analysisType.value === 'all') {
        // 如果没有选择学科且是综合分析，获取综合成绩分析
        await fetchGradeDetail(className.value);
      }
    };
    
    // 监听班级分析数据变化，更新图表
    watch(subjectAverages, async () => {
      if (subjectAverages.value && Object.keys(subjectAverages.value).length > 0) {
        setTimeout(async () => {
          await initClassSubjectChart();
        }, 0);
      }
    }, { deep: true });
    
    // 监听科目分析数据变化，更新图表
    watch(subjectAnalysis, async () => {
      if (subjectAnalysis.value) {
        setTimeout(async () => {
          await initSubjectDistributionChart();
          await initSubjectBoxPlotChart();
        }, 0);
      }
    }, { deep: true });
    
    // 监听考试趋势数据变化，更新图表
    watch(examTrend, async () => {
      if (examTrend.value) {
        setTimeout(async () => {
          await initExamTrendChart();
        }, 0);
      }
    }, { deep: true });
    
    // 初始化班级学科成绩图表
    const initClassSubjectChart = async () => {
      if (classSubjectChart.value && subjectAverages.value) {
        if (!echarts) {
          const loaded = await loadECharts();
          if (!loaded) return;
        }
        
        if (classSubjectChartInstance) {
          classSubjectChartInstance.dispose();
        }
        classSubjectChartInstance = echarts.init(classSubjectChart.value);
        
        const subjects = Object.keys(subjectAverages.value);
        const averages = subjects.map(subject => subjectAverages.value[subject]);
        
        const option = {
          title: {
            text: '班级各学科平均成绩',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: subjects,
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value',
            name: '平均分'
          },
          series: [
            {
              data: averages,
              type: 'bar',
              itemStyle: {
                color: '#fac858'
              }
            }
          ]
        };
        
        classSubjectChartInstance.setOption(option);
      }
    };
    
    // 初始化科目分布图表
    const initSubjectDistributionChart = async () => {
      if (subjectDistributionChart.value && subjectAnalysis.value) {
        if (!echarts) {
          const loaded = await loadECharts();
          if (!loaded) return;
        }
        
        if (subjectDistributionChartInstance) {
          subjectDistributionChartInstance.dispose();
        }
        subjectDistributionChartInstance = echarts.init(subjectDistributionChart.value);
        
        const distribution = subjectAnalysis.value.statistics.distribution;
        const categories = ['优秀', '良好', '中等', '及格', '不及格'];
        const data = [
          distribution.excellent,
          distribution.good,
          distribution.average,
          distribution.pass,
          distribution.fail
        ];
        
        const option = {
          title: {
            text: '成绩分布',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: categories
          },
          yAxis: {
            type: 'value',
            name: '人数'
          },
          series: [
            {
              name: '人数',
              type: 'bar',
              data: data,
              itemStyle: {
                color: '#5470c6'
              }
            }
          ]
        };
        
        subjectDistributionChartInstance.setOption(option);
      }
    };
    
    // 初始化科目箱线图
    const initSubjectBoxPlotChart = async () => {
      if (subjectBoxPlotChart.value && subjectAnalysis.value) {
        if (!echarts) {
          const loaded = await loadECharts();
          if (!loaded) return;
        }
        
        if (subjectBoxPlotChartInstance) {
          subjectBoxPlotChartInstance.dispose();
        }
        subjectBoxPlotChartInstance = echarts.init(subjectBoxPlotChart.value);
        
        const boxData = [
          [subjectAnalysis.value.statistics.min_score, 
           subjectAnalysis.value.statistics.min_score + 10, 
           subjectAnalysis.value.statistics.median, 
           subjectAnalysis.value.statistics.median + 10, 
           subjectAnalysis.value.statistics.max_score]
        ];
        
        const option = {
          title: {
            text: '成绩分布箱线图',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
          },
          xAxis: {
            type: 'category',
            data: [subjectAnalysis.value.subject],
            boundaryGap: true,
            nameGap: 30,
            splitArea: {
              show: false
            },
            splitLine: {
              show: false
            }
          },
          yAxis: {
            type: 'value',
            name: '分数',
            splitArea: {
              show: true
            }
          },
          series: [
            {
              name: '成绩分布',
              type: 'boxplot',
              data: boxData,
              itemStyle: {
                color: '#5470c6'
              }
            }
          ]
        };
        
        subjectBoxPlotChartInstance.setOption(option);
      }
    };
    
    // 初始化考试趋势图表
    const initExamTrendChart = async () => {
      if (examTrendChart.value && examTrend.value) {
        if (!echarts) {
          const loaded = await loadECharts();
          if (!loaded) return;
        }
        
        if (examTrendChartInstance) {
          examTrendChartInstance.dispose();
        }
        examTrendChartInstance = echarts.init(examTrendChart.value);
        
        const examNames = examTrend.value.exam_trend.exam_names;
        const averages = examTrend.value.exam_trend.averages;
        
        const option = {
          title: {
            text: '班级历次考试趋势',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: examNames,
            axisLabel: {
              rotate: 45
            }
          },
          yAxis: {
            type: 'value',
            name: '平均分数'
          },
          series: [
            {
              name: '平均分数',
              type: 'line',
              data: averages,
              smooth: true,
              itemStyle: {
                color: '#5470c6'
              },
              areaStyle: {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [{
                    offset: 0, color: 'rgba(84, 112, 198, 0.3)'
                  }, {
                    offset: 1, color: 'rgba(84, 112, 198, 0.1)'
                  }]
                }
              }
            }
          ]
        };
        
        examTrendChartInstance.setOption(option);
      }
    };
    
    // 计算属性，实时更新 classAnalysis
    const classAnalysis = computed(() => ({
      class_info: classInfo.value,
      overall_average: overallAverage.value,
      subject_averages: subjectAverages.value,
      student_count: studentCount.value
    }));
    
    // 班级学科成绩配置
    const classSubjectOptions = computed(() => {
      if (!subjectAverages.value) return {};
      
      const subjects = Object.keys(subjectAverages.value);
      const averages = subjects.map(subject => subjectAverages.value[subject]);
      
      return {
        title: {
          text: '班级各学科平均成绩',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: subjects,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '平均分'
        },
        series: [
          {
            data: averages,
            type: 'bar',
            itemStyle: {
              color: '#fac858'
            }
          }
        ]
      };
    });
    
    // 科目分布配置
    const subjectDistributionOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics || !subjectAnalysis.value.statistics.distribution) return {};
      
      const distribution = subjectAnalysis.value.statistics.distribution;
      const categories = ['优秀', '良好', '中等', '及格', '不及格'];
      const data = [
        distribution.excellent,
        distribution.good,
        distribution.average,
        distribution.pass,
        distribution.fail
      ];
      
      return {
        title: {
          text: '成绩分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: categories
        },
        yAxis: {
          type: 'value',
          name: '人数'
        },
        series: [
          {
            name: '人数',
            type: 'bar',
            data: data,
            itemStyle: {
              color: '#5470c6'
            }
          }
        ]
      };
    });
    
    // 科目箱线图配置
    const subjectBoxPlotOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics) return {};
      
      const boxData = [
        [subjectAnalysis.value.statistics.min_score, 
         subjectAnalysis.value.statistics.min_score + 10, 
         subjectAnalysis.value.statistics.median, 
         subjectAnalysis.value.statistics.median + 10, 
         subjectAnalysis.value.statistics.max_score]
      ];
      
      return {
        title: {
          text: '成绩分布箱线图',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%'
        },
        xAxis: {
          type: 'category',
          data: [subjectAnalysis.value.subject],
          boundaryGap: true,
          nameGap: 30,
          splitArea: {
            show: false
          },
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          name: '分数',
          splitArea: {
            show: true
          }
        },
        series: [
          {
            name: '成绩分布',
            type: 'boxplot',
            data: boxData,
            itemStyle: {
              color: '#5470c6'
            }
          }
        ]
      };
    });
    
    // 考试趋势配置
    const examTrendOptions = computed(() => {
      if (!examTrend.value || !examTrend.value.exam_trend) return {};
      
      const examNames = examTrend.value.exam_trend.exam_names;
      const averages = examTrend.value.exam_trend.averages;
      
      return {
        title: {
          text: '班级历次考试趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: examNames,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '平均分数'
        },
        series: [
          {
            name: '平均分数',
            type: 'line',
            data: averages,
            smooth: true,
            itemStyle: {
              color: '#5470c6'
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [{
                  offset: 0, color: 'rgba(84, 112, 198, 0.3)'
                }, {
                  offset: 1, color: 'rgba(84, 112, 198, 0.1)'
                }]
              }
            }
          }
        ]
      };
    });
    
    // 学科对比图表配置
    const subjectComparisonOptions = computed(() => {
      if (!subjectComparisonData.value) return {};
      
      const { subjects, diff } = subjectComparisonData.value;
      
      return {
        title: {
          text: `${subjects[0]} vs ${subjects[1]} 对比分析`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['平均分', '差异']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: subjects
        },
        yAxis: {
          type: 'value',
          name: '分数'
        },
        series: [
          {
            name: '平均分',
            type: 'bar',
            data: [75, 75 + diff],
            itemStyle: {
              color: ['#5470c6', '#91cc75']
            }
          },
          {
            name: '差异',
            type: 'line',
            data: [0, diff],
            smooth: true,
            itemStyle: {
              color: '#ee6666'
            }
          }
        ]
      };
    });
    
    onMounted(() => {
      loadClassOptions();
      loadExamList();
    });
    
    return {
      className,
      classes,
      grades,
      isLoadingOptions,
      selectedSubject,
      subjects,
      classAnalysis,
      subjectAnalysis,
      examTrend,
      loading,
      classError: error.value,
      subjectAverages,
      classSubjectOptions,
      subjectDistributionOptions,
      subjectBoxPlotOptions,
      examTrendOptions,
      subjectComparisonOptions,
      analyzeClass,
      analyzeSubject,
      loadingStep,
      analysisProcessSteps,
      currentAnalysisStep,
      analysisDataFlow,
      analysisCalculations,
      analysisHints,
      // 决策可视化数据（从API获取）
      knowledgeDiscoveriesData,
      featureImportanceData,
      decisionTreePathsData,
      factorImpactAnalysisData,
      // 学科分析数据
      subjectStrengthData,
      isSubjectAnalysisLoading,
      subjectAnalysisError,
      // 学科对比数据
      subjectCompare1,
      subjectCompare2,
      subjectComparisonData,
      compareSubjects,
      // 分析类型和详细成绩数据
      analysisType,
      gradeDetail,
      classTeachers,
      switchAnalysisType,
      distributionBarStyles,
      barLabels,
      // 考试相关数据
      exams,
      selectedExam,
      // 显示模式相关
      displayMode,
      toggleDisplayMode,
      // 趋势分析相关
      selectedTrendSubject,
      availableSubjects,
      handleTrendSubjectChange
    };
  }
};
</script>

<style scoped>
.class-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.class-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.exam-select-wrapper {
  flex: 1;
  min-width: 220px;
}

.filter-select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
}

.filter-select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.class-input button {
  padding: 10px 20px;
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.class-input button:hover:not(:disabled) {
  background: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.class-input button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

.class-input button:disabled,
.class-input button.disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  animation: fadeIn 0.5s ease-out;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #409eff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.2);
}

.loading-detail {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
  animation: pulse 2s infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error {
  text-align: center;
  padding: 40px;
  color: #f56c6c;
  background: #fef0f0;
  border-radius: 4px;
  border: 1px solid #fbc4c4;
  animation: shake 0.5s ease-in-out;
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.1);
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.filter-select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 150px;
  transition: all 0.3s ease;
  background: #fff;
}

.filter-select:focus {
  border-color: #409eff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(64, 158, 255, 0.25);
  transform: translateY(-1px);
}

.class-analysis-result {
  margin-top: 20px;
}

.subject-selector {
  margin: 20px 0;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.subject-selector h4 {
  margin-bottom: 10px;
  color: #333;
}

.subject-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background: #fff;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

@media (max-width: 1200px) {
  .class-analysis {
    padding: 15px;
  }
  
  .class-input {
    flex-wrap: wrap;
  }
  
  .class-input select {
    flex: 1 1 200px;
  }
  
  .class-input button {
    flex: 1 1 100px;
  }
}

@media (max-width: 768px) {
  .class-analysis {
    padding: 10px;
  }
  
  .class-input {
    flex-direction: column;
  }
  
  .subject-stats {
    grid-template-columns: 1fr 1fr;
  }
  
  h3 {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .subject-stats {
    grid-template-columns: 1fr;
  }
  
  h3 {
    font-size: 16px;
  }
  
  .loading {
    padding: 20px;
  }
}

/* 决策逻辑可视化模块样式 */
.decision-visualization-section {
  margin-top: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.section-header-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e2e8f0;
}

.section-icon {
  font-size: 28px;
  margin-right: 12px;
}

.section-title-area {
  flex: 1;
}

.section-main-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.section-subtitle {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #64748b;
}

/* 决策逻辑链条样式 */
.decision-chain {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.chain-item {
  display: flex;
  align-items: center;
}

.chain-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  border-radius: 8px;
  min-width: 100px;
  transition: all 0.3s ease;
}

.chain-node:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chain-node.highlight {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.chain-node.highlight .node-label {
  color: #fff;
}

.node-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.node-label {
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  text-align: center;
}

.chain-arrow {
  font-size: 20px;
  color: #94a3b8;
  margin: 0 4px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .decision-chain {
    flex-wrap: wrap;
  }
  
  .chain-node {
    min-width: 80px;
    padding: 10px 16px;
  }
}

@media (max-width: 768px) {
  .decision-visualization-section {
    padding: 16px;
  }
  
  .decision-chain {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .chain-arrow {
    transform: rotate(90deg);
    margin: 8px 0;
  }
  
  .chain-node {
    min-width: 100%;
    flex-direction: row;
    justify-content: flex-start;
    gap: 10px;
  }
  
  .node-icon {
    margin-bottom: 0;
  }
  
  .section-main-title {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .decision-visualization-section {
    padding: 12px;
  }
  
  .chain-node {
    padding: 8px 12px;
  }
  
  .node-label {
    font-size: 11px;
  }
}

/* 学科分析模块样式 */
.subject-analysis-section {
  margin-top: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

/* 学科对比选择器样式 */
.subject-comparison-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.subject-comparison-selector .filter-select {
  flex: 1;
  min-width: 120px;
}

.comparison-arrow {
  font-size: 16px;
  font-weight: bold;
  color: #64748b;
}

.compare-subjects-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.compare-subjects-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

/* 学科对比结果样式 */
.subject-comparison-result {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.comparison-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: #f8fafc;
  border-radius: 6px;
}

.summary-label {
  font-size: 14px;
  color: #64748b;
}

.summary-value {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
}

.summary-value.positive {
  color: #059669;
}

.summary-value.negative {
  color: #dc2626;
}

/* 班级对比分析模块样式 */
.class-comparison-section {
  margin-top: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .subject-analysis-section,
  .class-comparison-section {
    padding: 16px;
  }
  
  .subject-comparison-selector {
    flex-direction: column;
  }
  
  .subject-comparison-selector .filter-select {
    width: 100%;
  }
  
  .comparison-summary {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .subject-analysis-section,
  .class-comparison-section {
    padding: 12px;
  }
  
  .compare-subjects-btn {
    width: 100%;
  }
}

/* 学科分析模块样式 */
.subject-selector-section {
  margin-top: 24px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #e2e8f0;
}

.analysis-type-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.selector-label {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
}

.analysis-type-tabs {
  display: flex;
  gap: 8px;
}

.tab-btn {
  padding: 10px 20px;
  background: #fff;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.tab-btn.active {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-color: #6366f1;
  color: white;
}

.subject-selector {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.subject-selector .filter-select {
  flex: 1;
  min-width: 200px;
}

/* 成绩详情面板样式 */
.grade-detail-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  padding: 24px;
}

.grade-detail-panel .panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e2e8f0;
}

.grade-detail-panel .panel-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

/* 统计卡片网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  flex: 1;
}

.stat-info .stat-label {
  display: block;
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-info .stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
}

/* 空数据面板样式 */
.empty-data-panel {
  text-align: center;
  padding: 40px 20px;
  background: #f8fafc;
  border-radius: 12px;
  margin-top: 20px;
}

.empty-data-panel .empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-data-panel p {
  margin: 0;
  font-size: 16px;
  color: #64748b;
}

.empty-data-panel.error {
  background: #fef2f2;
}

.empty-data-panel.error p {
  color: #991b1b;
}

.empty-data-panel.error .error-hint {
  font-size: 14px;
  color: #b91c1c;
  margin-top: 8px;
}

/* 分数分布区域 */
.distribution-section {
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.distribution-section h5 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
  color: #334155;
}

.distribution-bars {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dist-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bar-label {
  width: 100px;
  font-size: 13px;
  color: #64748b;
  text-align: right;
}

.bar-container {
  flex: 1;
  height: 24px;
  background: #f1f5f9;
  border-radius: 12px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 12px;
  transition: width 0.3s ease;
}

.bar.excellent {
  background: linear-gradient(135deg, #10b981, #34d399);
}

.bar.good {
  background: linear-gradient(135deg, #60a5fa, #93c5fd);
}

.bar.average {
  background: linear-gradient(135deg, #fbbf24, #fcd34d);
}

.bar.pass {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
}

.bar.fail {
  background: linear-gradient(135deg, #ef4444, #f87171);
}

.bar-value {
  width: 50px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  text-align: left;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .subject-selector-section {
    padding: 16px;
  }
  
  .analysis-type-selector {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .bar-label {
    width: 80px;
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .subject-selector-section {
    padding: 12px;
  }
  
  .subject-selector {
    flex-direction: column;
  }
  
  .subject-selector .filter-select {
    width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dist-bar {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .bar-label {
    width: 100%;
    text-align: left;
    margin-bottom: 5px;
  }
  
  .bar-value {
    width: 100%;
    text-align: left;
    margin-top: 5px;
  }
}
</style>