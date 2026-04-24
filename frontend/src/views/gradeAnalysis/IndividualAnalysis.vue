<template>
  <div class="individual-analysis">
    <h3>个人成绩分析</h3>
    <div class="student-input">
      <select 
        v-model="studentId" 
        class="filter-select"
      >
        <option value="">请选择学生</option>
        <option v-for="student in students" :key="student.id" :value="student.id">
            {{ student.name }} ({{ student.id }})
          </option>
      </select>
      <button @click="loadStudents">加载学生</button>
      <button @click="analyzeStudent">分析</button>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>正在分析 {{ selectedStudentName }} 的成绩...</p>
      <p class="loading-detail">{{ loadingStep }}</p>
    </div>
    <div v-else-if="studentError" class="error">{{ studentError }}</div>
    <div v-else-if="studentAnalysis && studentAnalysis.student_info" class="student-analysis">
      <!-- 分析过程展示 -->
      <CollapsibleSection 
        title="分析过程" 
        icon="🔍" 
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
      
      <div class="module-row">
        <CollapsibleSection 
          title="学生信息" 
          icon="📊" 
          :default-collapsed="false"
          storage-key="student_info"
          class="module-item"
        >
          <p>姓名: {{ studentAnalysis.student_info.name }}</p>
          <p>性别: {{ studentAnalysis.student_info.gender }}</p>
          <p>班级: {{ studentAnalysis.student_info.class }}</p>
          <p>年级: {{ studentAnalysis.student_info.grade }}</p>
        </CollapsibleSection>
        
        <CollapsibleSection 
          title="整体表现" 
          icon="📈" 
          :default-collapsed="false"
          storage-key="overall_performance"
          class="module-item"
        >
          <p>个人平均: {{ studentAnalysis.overall.personal_avg }}</p>
          <p>班级平均: {{ studentAnalysis.overall.class_avg }}</p>
          <p>差异: {{ studentAnalysis.overall.diff > 0 ? '+' + studentAnalysis.overall.diff : studentAnalysis.overall.diff }}</p>
          <p>评估: {{ studentAnalysis.overall.evaluation }}</p>
        </CollapsibleSection>
        
        <CollapsibleSection 
          title="学科强项与弱项" 
          icon="⚖️"
          storage-key="strengths_weaknesses"
          class="module-item"
        >
          <div class="strengths-weaknesses">
            <div class="strengths">
              <h5>学科强项</h5>
              <ul>
                <li v-for="(item, index) in studentAnalysis.strengths" :key="index">
                  {{ item.subject }}: {{ item.avg_score }} (班级平均: {{ item.class_avg }}, +{{ item.diff }})
                </li>
              </ul>
            </div>
            <div class="weaknesses">
              <h5>学科弱项</h5>
              <ul>
                <li v-for="(item, index) in studentAnalysis.weaknesses" :key="index">
                  {{ item.subject }}: {{ item.avg_score }} (班级平均: {{ item.class_avg }}, -{{ item.diff }})
                </li>
              </ul>
            </div>
          </div>
        </CollapsibleSection>
      </div>
      
      <CollapsibleSection 
        title="学科分析" 
        icon="📊"
        storage-key="subject_analysis"
      >
        <BaseECharts
          chart-type="bar"
          :data="{ subjectAverages, classAverages }"
          :options="studentSubjectOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：科目选择下拉菜单 -->
      <div class="subject-selector">
        <h4>科目分析</h4>
        <select v-model="selectedSubject" class="filter-select" @change="analyzeSubject">
          <option value="">请选择科目</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
        </select>
      </div>
      
      <!-- 新增：具体科目分析模块 -->
      <CollapsibleSection 
        v-if="subjectAnalysis" 
        :title="selectedSubject + ' 科目分析'" 
        icon="📊"
        storage-key="specific_subject_analysis"
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
          <div class="stat-item">
            <span class="stat-label">班级平均:</span>
            <span class="stat-value">{{ subjectAnalysis.class_average }}</span>
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
        title="历次考试趋势" 
        icon="📈"
        storage-key="exam_trend"
      >
        <BaseECharts
          chart-type="line"
          :data="examTrend"
          :options="examTrendOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：课程安排与成绩关系散点图 -->
      <CollapsibleSection 
        title="课程安排与成绩关系" 
        icon="📅"
        storage-key="schedule_analysis"
      >
        <BaseECharts
          chart-type="scatter"
          :data="scheduleAnalysis"
          :options="scheduleScatterOptions"
          height="400px"
        />
      </CollapsibleSection>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../../components/common/BaseECharts.vue'
import CollapsibleSection from '../../components/common/CollapsibleSection.vue'
import AnalysisProcessVisualizer from '../../components/common/AnalysisProcessVisualizer.vue'
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useIndividualGrade } from '../../composables/grade/useIndividualGrade'

export default {
  name: 'IndividualAnalysis',
  components: {
    BaseECharts,
    CollapsibleSection,
    AnalysisProcessVisualizer
  },
  setup() {
    const {
      studentInfo,
      examGrades,
      subjectAverages,
      classAverages,
      strengths,
      weaknesses,
      overall,
      subjectAnalysis,
      examTrend,
      scheduleAnalysis,
      loading,
      error,
      getStudentAnalysis,
      getStudentSubjectAnalysis,
      getStudentTrend,
      getStudentScheduleAnalysis
    } = useIndividualGrade()
    
    const studentId = ref('')
    const students = ref([])
    const isLoadingStudents = ref(false)
    const selectedStudentName = ref('')
    const selectedSubject = ref('')
    const subjects = ref([])
    
    // 分析过程相关状态
    const loadingStep = ref('正在获取各科成绩数据，请稍候...')
    const analysisProcessSteps = ref([
      {
        title: '数据获取',
        description: '从数据库中提取学生的基本信息和成绩记录',
        details: {
          data_source: '学生成绩数据库',
          tables: ['students', 'grades', 'exams'],
          method: '通过GradeDataAccess.get_student_grades获取学生成绩数据'
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
        description: '计算各项统计指标，如平均分、中位数、标准差等',
        details: {
          metrics: ['平均分', '中位数', '标准差', '最高分', '最低分'],
          method: '使用statistical_analysis.py中的函数进行计算'
        }
      },
      {
        title: '学科分析',
        description: '分析学生各学科的表现，识别强项和弱项',
        details: {
          method: '比较学生各学科成绩与班级平均成绩',
          criteria: '高于班级平均为强项，低于为弱项'
        }
      },
      {
        title: '趋势分析',
        description: '分析学生历次考试的成绩变化趋势',
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
          output: '学生成绩分析报告'
        }
      }
    ])
    const currentAnalysisStep = ref(0)
    const analysisDataFlow = ref({
      nodes: [
        { name: '原始数据', type: 'source', description: '从数据库提取的原始成绩数据' },
        { name: '数据处理', type: 'process', description: '清洗、整理和标准化数据' },
        { name: '分析结果', type: 'result', description: '生成最终分析报告' }
      ],
      connections: [
        { from: 0, to: 1 },
        { from: 1, to: 2 }
      ]
    })
    const analysisCalculations = ref([
      {
        name: '个人平均分计算',
        formula: '总分 / 科目数',
        result: '计算学生所有科目的平均分数'
      },
      {
        name: '班级平均分计算',
        formula: '班级总分 / 班级总人数',
        result: '计算班级所有学生的平均分数'
      },
      {
        name: '差异计算',
        formula: '个人平均分 - 班级平均分',
        result: '计算学生与班级平均的差异'
      },
      {
        name: '标准差计算',
        formula: 'sqrt(sum((x - μ)^2) / n)',
        result: '计算成绩的离散程度'
      }
    ])
    
    // 图表引用
    const studentSubjectChart = ref(null)
    const subjectDistributionChart = ref(null)
    const subjectBoxPlotChart = ref(null)
    const examTrendChart = ref(null)
    const scheduleScatterChart = ref(null)
    
    // 图表实例
    let studentSubjectChartInstance = null
    let subjectDistributionChartInstance = null
    let subjectBoxPlotChartInstance = null
    let examTrendChartInstance = null
    let scheduleScatterChartInstance = null
    
    // ECharts 实例
    let echarts = null
    
    // 动态导入 ECharts
    const loadECharts = async () => {
      try {
        // 按需导入核心模块和需要的图表类型
        const echartsCore = await import('echarts/core')
        const charts = await import('echarts/charts')
        const components = await import('echarts/components')
        const renderers = await import('echarts/renderers')
        
        // 注册必要的组件
        const { use, init } = echartsCore
        const { BarChart, LineChart, RadarChart, PieChart, BoxplotChart, ScatterChart } = charts
        const { 
          TitleComponent, TooltipComponent, LegendComponent, 
          GridComponent, DataZoomComponent, ToolboxComponent,
          VisualMapComponent
        } = components
        const { CanvasRenderer } = renderers
        
        use([
          BarChart, LineChart, RadarChart, PieChart, BoxplotChart, ScatterChart,
          TitleComponent, TooltipComponent, LegendComponent, GridComponent,
          DataZoomComponent, ToolboxComponent, VisualMapComponent,
          CanvasRenderer
        ])
        
        echarts = echartsCore
        return true
      } catch (err) {
        console.error('加载 ECharts 失败:', err)
        return false
      }
    }
    
    // 加载学生列表
    const loadStudents = async () => {
      console.log('开始加载学生列表')
      isLoadingStudents.value = true
      try {
        console.log('发起API请求')
        const { studentApi } = await import('../../services/api/apiService')
        const data = await studentApi.getStudents()
        console.log('获取到学生数据:', data)
        students.value = data
      } catch (error) {
        console.error('获取学生列表失败:', error)
      } finally {
        isLoadingStudents.value = false
        console.log('加载学生列表完成')
      }
    }
    
    // 分析学生成绩
    const analyzeStudent = async () => {
      if (studentId.value) {
        // 查找选中的学生姓名
        const selectedStudent = students.value.find(student => student.id === studentId.value)
        if (selectedStudent) {
          selectedStudentName.value = selectedStudent.name
        }
        
        // 重置分析步骤
        currentAnalysisStep.value = 0
        
        // 步骤1：数据获取
        loadingStep.value = '正在获取学生基本信息和成绩数据...'
        currentAnalysisStep.value = 0
        await getStudentAnalysis(studentId.value)
        
        // 步骤2：数据预处理
        loadingStep.value = '正在预处理数据，确保数据质量...'
        currentAnalysisStep.value = 1
        // 模拟预处理时间
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 步骤3：统计分析
        loadingStep.value = '正在计算统计指标，如平均分、中位数、标准差等...'
        currentAnalysisStep.value = 2
        // 模拟统计分析时间
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 步骤4：学科分析
        loadingStep.value = '正在分析学生各学科表现，识别强项和弱项...'
        currentAnalysisStep.value = 3
        // 提取科目列表
        if (subjectAverages.value) {
          subjects.value = Object.keys(subjectAverages.value)
        }
        
        // 步骤5：趋势分析
        loadingStep.value = '正在分析学生历次考试的成绩变化趋势...'
        currentAnalysisStep.value = 4
        await getStudentTrend(studentId.value)
        
        // 步骤6：结果生成
        loadingStep.value = '正在生成分析报告...'
        currentAnalysisStep.value = 5
        await getStudentScheduleAnalysis(studentId.value)
        
        // 完成分析
        currentAnalysisStep.value = 6
      }
    }
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (studentId.value && selectedSubject.value) {
        await getStudentSubjectAnalysis(studentId.value, selectedSubject.value)
      }
    }
    
    // 监听学生分析数据变化，更新图表
    watch([subjectAverages, classAverages], async () => {
      if (subjectAverages.value && Object.keys(subjectAverages.value).length > 0) {
        // 使用nextTick确保DOM渲染完成后再初始化图表
        setTimeout(async () => {
          await initStudentSubjectChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听科目分析数据变化，更新图表
    watch(subjectAnalysis, async () => {
      if (subjectAnalysis.value) {
        setTimeout(async () => {
          await initSubjectDistributionChart()
          await initSubjectBoxPlotChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听考试趋势数据变化，更新图表
    watch(examTrend, async () => {
      if (examTrend.value) {
        setTimeout(async () => {
          await initExamTrendChart()
        }, 0)
      }
    }, { deep: true })
    
    // 监听课程安排分析数据变化，更新图表
    watch(scheduleAnalysis, async () => {
      if (scheduleAnalysis.value) {
        setTimeout(async () => {
          await initScheduleScatterChart()
        }, 0)
      }
    }, { deep: true })
    
    // 初始化学生学科成绩图表
    const initStudentSubjectChart = async () => {
      if (studentSubjectChart.value && subjectAverages.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (studentSubjectChartInstance) {
          studentSubjectChartInstance.dispose()
        }
        studentSubjectChartInstance = echarts.init(studentSubjectChart.value)
        
        const subjects = Object.keys(subjectAverages.value)
        const personalAverages = subjects.map(subject => subjectAverages.value[subject])
        const classAverages = subjects.map(subject => classAverages.value[subject] || 0)
        
        const option = {
          title: {
            text: '个人与班级学科成绩对比',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          legend: {
            data: ['个人平均', '班级平均'],
            bottom: 0
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
            name: '分数'
          },
          series: [
            {
              name: '个人平均',
              type: 'bar',
              data: personalAverages,
              itemStyle: {
                color: '#5470c6'
              }
            },
            {
              name: '班级平均',
              type: 'bar',
              data: classAverages,
              itemStyle: {
                color: '#91cc75'
              }
            }
          ]
        }
        
        studentSubjectChartInstance.setOption(option)
      }
    }
    
    // 初始化科目分布图表
    const initSubjectDistributionChart = async () => {
      if (subjectDistributionChart.value && subjectAnalysis.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (subjectDistributionChartInstance) {
          subjectDistributionChartInstance.dispose()
        }
        subjectDistributionChartInstance = echarts.init(subjectDistributionChart.value)
        
        const distribution = subjectAnalysis.value.statistics.distribution
        const categories = ['优秀', '良好', '中等', '及格', '不及格']
        const data = [
          distribution.excellent,
          distribution.good,
          distribution.average,
          distribution.pass,
          distribution.fail
        ]
        
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
        }
        
        subjectDistributionChartInstance.setOption(option)
      }
    }
    
    // 初始化科目箱线图
    const initSubjectBoxPlotChart = async () => {
      if (subjectBoxPlotChart.value && subjectAnalysis.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (subjectBoxPlotChartInstance) {
          subjectBoxPlotChartInstance.dispose()
        }
        subjectBoxPlotChartInstance = echarts.init(subjectBoxPlotChart.value)
        
        // 模拟箱线图数据（实际项目中应该从API获取）
        const boxData = [
          [subjectAnalysis.value.statistics.min_score, 
           subjectAnalysis.value.statistics.min_score + 10, 
           subjectAnalysis.value.statistics.median, 
           subjectAnalysis.value.statistics.median + 10, 
           subjectAnalysis.value.statistics.max_score]
        ]
        
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
        }
        
        subjectBoxPlotChartInstance.setOption(option)
      }
    }
    
    // 初始化考试趋势图表
    const initExamTrendChart = async () => {
      if (examTrendChart.value && examTrend.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (examTrendChartInstance) {
          examTrendChartInstance.dispose()
        }
        examTrendChartInstance = echarts.init(examTrendChart.value)
        
        const examNames = examTrend.value.exam_trend.exam_names
        const averages = examTrend.value.exam_trend.averages
        
        const option = {
          title: {
            text: '历次考试趋势',
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
        }
        
        examTrendChartInstance.setOption(option)
      }
    }
    
    // 初始化课程安排与成绩关系散点图
    const initScheduleScatterChart = async () => {
      if (scheduleScatterChart.value && scheduleAnalysis.value) {
        // 确保 ECharts 已加载
        if (!echarts) {
          const loaded = await loadECharts()
          if (!loaded) return
        }
        
        if (scheduleScatterChartInstance) {
          scheduleScatterChartInstance.dispose()
        }
        scheduleScatterChartInstance = echarts.init(scheduleScatterChart.value)
        
        // 处理散点图数据
        const scatterData = []
        if (scheduleAnalysis.value.schedule_analysis) {
          for (const key in scheduleAnalysis.value.schedule_analysis) {
            const item = scheduleAnalysis.value.schedule_analysis[key]
            if (item.score) {
              // 使用周几和节次作为x和y坐标，成绩作为点的大小和颜色
              scatterData.push([
                item.day_of_week,
                item.period,
                item.score
              ])
            }
          }
        }
        
        const option = {
          title: {
            text: '课程安排与成绩关系',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: function(params) {
              return `周${params.value[0]} 第${params.value[1]}节<br/>成绩: ${params.value[2]}`
            }
          },
          xAxis: {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7'],
            name: '周几'
          },
          yAxis: {
            type: 'category',
            data: ['1', '2', '3', '4', '5', '6', '7', '8'],
            name: '节次'
          },
          series: [
            {
              name: '成绩',
              type: 'scatter',
              data: scatterData,
              symbolSize: function(val) {
                return val[2] / 10
              },
              itemStyle: {
                color: function(params) {
                  const score = params.value[2]
                  if (score >= 90) return '#52c41a'
                  if (score >= 80) return '#1890ff'
                  if (score >= 70) return '#faad14'
                  if (score >= 60) return '#fa8c16'
                  return '#f5222d'
                }
              }
            }
          ]
        }
        
        scheduleScatterChartInstance.setOption(option)
      }
    }
    
    // 窗口大小变化时调整图表
    const handleResize = () => {
      studentSubjectChartInstance?.resize()
      subjectDistributionChartInstance?.resize()
      subjectBoxPlotChartInstance?.resize()
      examTrendChartInstance?.resize()
      scheduleScatterChartInstance?.resize()
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
      loadStudents()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      studentSubjectChartInstance?.dispose()
      subjectDistributionChartInstance?.dispose()
      subjectBoxPlotChartInstance?.dispose()
      examTrendChartInstance?.dispose()
      scheduleScatterChartInstance?.dispose()
    })
    
    // 计算属性，实时更新 studentAnalysis
    const studentAnalysis = computed(() => ({
      student_info: studentInfo.value,
      overall: overall.value,
      subject_averages: subjectAverages.value,
      class_averages: classAverages.value,
      strengths: strengths.value,
      weaknesses: weaknesses.value
    }))
    
    // 学生学科成绩配置
    const studentSubjectOptions = computed(() => {
      if (!subjectAverages.value || !classAverages.value) return {}
      
      const subjects = Object.keys(subjectAverages.value)
      const personalAverages = subjects.map(subject => subjectAverages.value[subject])
      const classAvgs = subjects.map(subject => classAverages.value[subject] || 0)
      
      // 响应式配置
      const isSmallScreen = window.innerWidth < 768
      
      return {
        title: {
          text: '个人与班级学科成绩对比',
          left: 'center',
          textStyle: {
            fontSize: isSmallScreen ? 14 : 16
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['个人平均', '班级平均'],
          bottom: 0,
          textStyle: {
            fontSize: isSmallScreen ? 12 : 14
          }
        },
        xAxis: {
          type: 'category',
          data: subjects,
          axisLabel: {
            rotate: isSmallScreen ? 60 : 45,
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        yAxis: {
          type: 'value',
          name: '分数',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        series: [
          {
            name: '个人平均',
            type: 'bar',
            data: personalAverages,
            itemStyle: {
              color: '#5470c6'
            }
          },
          {
            name: '班级平均',
            type: 'bar',
            data: classAvgs,
            itemStyle: {
              color: '#91cc75'
            }
          }
        ],
        grid: {
          left: isSmallScreen ? '3%' : '10%',
          right: isSmallScreen ? '3%' : '10%',
          bottom: isSmallScreen ? '15%' : '10%',
          containLabel: true
        }
      }
    })
    
    // 科目分布配置
    const subjectDistributionOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics || !subjectAnalysis.value.statistics.distribution) return {}
      
      const distribution = subjectAnalysis.value.statistics.distribution
      const categories = ['优秀', '良好', '中等', '及格', '不及格']
      const data = [
        distribution.excellent,
        distribution.good,
        distribution.average,
        distribution.pass,
        distribution.fail
      ]
      
      // 响应式配置
      const isSmallScreen = window.innerWidth < 768
      
      return {
        title: {
          text: '成绩分布',
          left: 'center',
          textStyle: {
            fontSize: isSmallScreen ? 14 : 16
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: categories,
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        yAxis: {
          type: 'value',
          name: '人数',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
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
        ],
        grid: {
          left: isSmallScreen ? '3%' : '10%',
          right: isSmallScreen ? '3%' : '10%',
          bottom: isSmallScreen ? '10%' : '5%',
          containLabel: true
        }
      }
    })
    
    // 科目箱线图配置
    const subjectBoxPlotOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics) return {}
      
      // 模拟箱线图数据
      const boxData = [
        [subjectAnalysis.value.statistics.min_score, 
         subjectAnalysis.value.statistics.min_score + 10, 
         subjectAnalysis.value.statistics.median, 
         subjectAnalysis.value.statistics.median + 10, 
         subjectAnalysis.value.statistics.max_score]
      ]
      
      // 响应式配置
      const isSmallScreen = window.innerWidth < 768
      
      return {
        title: {
          text: '成绩分布箱线图',
          left: 'center',
          textStyle: {
            fontSize: isSmallScreen ? 14 : 16
          }
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: isSmallScreen ? '15%' : '10%',
          right: isSmallScreen ? '10%' : '10%',
          bottom: isSmallScreen ? '15%' : '15%'
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
          },
          axisLabel: {
            fontSize: isSmallScreen ? 12 : 14
          }
        },
        yAxis: {
          type: 'value',
          name: '分数',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          },
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
      }
    })
    
    // 考试趋势配置
    const examTrendOptions = computed(() => {
      if (!examTrend.value || !examTrend.value.exam_trend) return {}
      
      const examNames = examTrend.value.exam_trend.exam_names
      const averages = examTrend.value.exam_trend.averages
      
      // 响应式配置
      const isSmallScreen = window.innerWidth < 768
      
      return {
        title: {
          text: '历次考试趋势',
          left: 'center',
          textStyle: {
            fontSize: isSmallScreen ? 14 : 16
          }
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: examNames,
          axisLabel: {
            rotate: isSmallScreen ? 60 : 45,
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        yAxis: {
          type: 'value',
          name: '平均分数',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
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
        ],
        grid: {
          left: isSmallScreen ? '3%' : '10%',
          right: isSmallScreen ? '3%' : '10%',
          bottom: isSmallScreen ? '15%' : '10%',
          containLabel: true
        }
      }
    })
    
    // 课程安排散点图配置
    const scheduleScatterOptions = computed(() => {
      if (!scheduleAnalysis.value || !scheduleAnalysis.value.schedule_analysis) return {}
      
      // 处理散点图数据
      const scatterData = []
      for (const key in scheduleAnalysis.value.schedule_analysis) {
        const item = scheduleAnalysis.value.schedule_analysis[key]
        if (item.score) {
          scatterData.push([
            item.day_of_week,
            item.period,
            item.score
          ])
        }
      }
      
      // 响应式配置
      const isSmallScreen = window.innerWidth < 768
      
      return {
        title: {
          text: '课程安排与成绩关系',
          left: 'center',
          textStyle: {
            fontSize: isSmallScreen ? 14 : 16
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            return `周${params.value[0]} 第${params.value[1]}节<br/>成绩: ${params.value[2]}`
          }
        },
        xAxis: {
          type: 'category',
          data: ['1', '2', '3', '4', '5', '6', '7'],
          name: '周几',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        yAxis: {
          type: 'category',
          data: ['1', '2', '3', '4', '5', '6', '7', '8'],
          name: '节次',
          nameTextStyle: {
            fontSize: isSmallScreen ? 12 : 14
          },
          axisLabel: {
            fontSize: isSmallScreen ? 10 : 12
          }
        },
        series: [
          {
            name: '成绩',
            type: 'scatter',
            data: scatterData,
            symbolSize: function(val) {
              return isSmallScreen ? val[2] / 12 : val[2] / 10
            },
            itemStyle: {
              color: function(params) {
                const score = params.value[2]
                if (score >= 90) return '#52c41a'
                if (score >= 80) return '#1890ff'
                if (score >= 70) return '#faad14'
                if (score >= 60) return '#fa8c16'
                return '#f5222d'
              }
            }
          }
        ],
        grid: {
          left: isSmallScreen ? '10%' : '15%',
          right: isSmallScreen ? '5%' : '10%',
          bottom: isSmallScreen ? '5%' : '10%',
          top: isSmallScreen ? '15%' : '10%',
          containLabel: true
        }
      }
    })
    
    onMounted(() => {
      loadStudents()
    })
    
    return {
      studentId,
      students,
      isLoadingStudents,
      selectedStudentName,
      selectedSubject,
      subjects,
      studentAnalysis,
      subjectAnalysis,
      examTrend,
      scheduleAnalysis,
      loading,
      studentError: error.value,
      subjectAverages,
      classAverages,
      studentSubjectOptions,
      subjectDistributionOptions,
      subjectBoxPlotOptions,
      examTrendOptions,
      scheduleScatterOptions,
      analyzeStudent,
      analyzeSubject,
      // 分析过程相关
      loadingStep,
      analysisProcessSteps,
      currentAnalysisStep,
      analysisDataFlow,
      analysisCalculations
    }
  }
}
</script>

<style scoped>
.individual-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.student-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.student-input select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
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

.student-input button {
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

.student-input button:hover {
  background: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.student-input button:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.loading-detail {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
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

.student-analysis {
  margin-top: 20px;
}

.module-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.module-item {
  flex: 1;
  min-width: 0;
}

.module-item .collapsible-section {
  height: 100%;
}

.strengths-weaknesses {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.strengths,
.weaknesses {
  padding: 15px;
}

.strengths h5,
.weaknesses h5 {
  margin-bottom: 10px;
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.strengths ul,
.weaknesses ul {
  list-style: none;
  padding: 0;
}

.strengths li,
.weaknesses li {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
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
  .individual-analysis {
    padding: 15px;
  }
  
  .student-input {
    flex-wrap: wrap;
  }
  
  .student-input select {
    flex: 1 1 200px;
  }
  
  .student-input button {
    flex: 1 1 100px;
  }
  
  .module-row {
    flex-wrap: wrap;
  }
  
  .module-item {
    flex: 1 1 calc(50% - 10px);
  }
}

@media (max-width: 768px) {
  .individual-analysis {
    padding: 10px;
  }
  
  .student-input {
    flex-direction: column;
  }
  
  .module-row {
    flex-direction: column;
  }
  
  .module-item {
    flex: 1 1 100%;
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
  
  .loading-spinner {
    width: 30px;
    height: 30px;
  }
}
</style>