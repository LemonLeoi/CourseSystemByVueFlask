<template>
  <div class="grade-analysis">
    <h3>年级成绩分析</h3>
    <div class="grade-input">
      <select 
        v-model="gradeName" 
        class="filter-select"
      >
        <option value="">请选择年级</option>
        <option v-for="grade in grades" :key="grade" :value="grade">
          {{ grade }}
        </option>
      </select>
      <button @click="analyzeGrade">分析</button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="gradeError" class="error">{{ gradeError }}</div>
    <div v-else-if="gradeAnalysis && gradeAnalysis.grade_info" class="grade-analysis-result">
      <CollapsibleSection 
        title="年级信息" 
        icon="🎓" 
        :default-collapsed="false"
        storage-key="grade_info"
      >
        <p>年级: {{ gradeAnalysis.grade_info.grade }}</p>
        <p>班级数量: {{ gradeAnalysis.grade_info.class_count }}</p>
        <p>年级平均成绩: {{ gradeAnalysis.overall_average }}</p>
      </CollapsibleSection>
      
      <CollapsibleSection 
        title="学科平均成绩" 
        icon="📊"
        storage-key="grade_subject_analysis"
      >
        <BaseECharts
          chart-type="bar"
          :data="gradeSubjectData"
          :options="gradeSubjectOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <CollapsibleSection 
        title="班级平均成绩对比" 
        icon="📈"
        storage-key="class_comparison_analysis"
      >
        <BaseECharts
          chart-type="bar"
          :data="classComparisonData"
          :options="classComparisonOptions"
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
        storage-key="specific_grade_subject_analysis"
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
          :data="subjectDistributionData"
          :options="subjectDistributionOptions"
          height="400px"
        />
        <BaseECharts
          chart-type="boxplot"
          :data="subjectBoxPlotData"
          :options="subjectBoxPlotOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：历次考试趋势图表 -->
      <CollapsibleSection 
        title="年级历次考试趋势" 
        icon="📈"
        storage-key="grade_exam_trend"
      >
        <BaseECharts
          chart-type="line"
          :data="examTrendData"
          :options="examTrendOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：教师成绩对比模块 -->
      <CollapsibleSection 
        v-if="teacherPerformance" 
        title="教师成绩对比" 
        icon="👨‍🏫"
        storage-key="teacher_performance"
      >
        <BaseECharts
          chart-type="bar"
          :data="teacherComparisonData"
          :options="teacherComparisonOptions"
          height="400px"
        />
      </CollapsibleSection>
      
      <!-- 新增：教师与成绩关系热力图 -->
      <CollapsibleSection 
        v-if="teacherPerformance" 
        title="教师与成绩关系热力图" 
        icon="🔥"
        storage-key="teacher_heatmap"
      >
        <BaseECharts
          chart-type="heatmap"
          :data="teacherHeatmapData"
          :options="teacherHeatmapOptions"
          height="400px"
        />
      </CollapsibleSection>
    </div>
  </div>
</template>

<script>
import BaseECharts from '../../components/common/BaseECharts.vue'
import CollapsibleSection from '../../components/common/CollapsibleSection.vue'
import { ref, onMounted, computed, watch } from 'vue'
import { useGradeAnalysis } from '../../composables/grade/useGradeAnalysis'

export default {
  name: 'GradeLevelAnalysis',
  components: {
    BaseECharts,
    CollapsibleSection
  },
  setup() {
    const { 
      gradeAnalysis, 
      subjectAnalysis,
      examTrend,
      teacherPerformance,
      loading, 
      gradeError,
      subjectError,
      trendError,
      teacherError,
      getGradeAnalysis,
      getGradeSubjectAnalysis,
      getGradeTrend,
      getTeacherPerformance
    } = useGradeAnalysis()
    
    const gradeName = ref('')
    const grades = ref([])
    const isLoadingOptions = ref(false)
    const selectedSubject = ref('')
    const subjects = ref([])
    
    // 加载年级列表
    const loadGradeOptions = async () => {
      isLoadingOptions.value = true
      try {
        const response = await fetch('/api/students/classes')
        if (response.ok) {
          const data = await response.json()
          grades.value = data.grades || []
        }
      } catch (error) {
        console.error('获取年级列表失败:', error)
      } finally {
        isLoadingOptions.value = false
      }
    }
    
    // 分析年级成绩
    const analyzeGrade = async () => {
      if (gradeName.value) {
        await getGradeAnalysis(gradeName.value)
        // 加载考试趋势
        await getGradeTrend(gradeName.value)
        // 提取科目列表
        if (gradeAnalysis.value && gradeAnalysis.value.subject_averages) {
          subjects.value = Object.keys(gradeAnalysis.value.subject_averages)
        }
      }
    }
    
    // 分析学科成绩
    const analyzeSubject = async () => {
      if (gradeName.value && selectedSubject.value) {
        await getGradeSubjectAnalysis(gradeName.value, selectedSubject.value)
        // 加载教师成绩对比，即使失败也不影响页面显示
        try {
          await getTeacherPerformance(selectedSubject.value)
        } catch (error) {
          console.log('教师成绩对比数据暂时不可用，将继续显示其他分析结果')
        }
      }
    }
    
    // 年级学科成绩数据
    const gradeSubjectData = computed(() => {
      return gradeAnalysis.value || {}
    })
    
    // 年级学科成绩配置
    const gradeSubjectOptions = computed(() => {
      if (!gradeAnalysis.value || !gradeAnalysis.value.subject_averages) return {}
      
      const subjects = Object.keys(gradeAnalysis.value.subject_averages)
      const averages = subjects.map(subject => gradeAnalysis.value.subject_averages[subject])
      
      return {
        title: {
          text: '年级各学科平均成绩',
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
              color: '#ee6666'
            }
          }
        ]
      }
    })
    
    // 班级对比数据
    const classComparisonData = computed(() => {
      return gradeAnalysis.value || {}
    })
    
    // 班级对比配置
    const classComparisonOptions = computed(() => {
      if (!gradeAnalysis.value || !gradeAnalysis.value.class_averages || !gradeAnalysis.value.subject_averages) return {}
      
      const classes = Object.keys(gradeAnalysis.value.class_averages)
      const subjects = Object.keys(gradeAnalysis.value.subject_averages)
      
      // 使用柱状图展示班级间的成绩对比
      const series = classes.map((className) => {
        const data = subjects.map(subject => {
          return gradeAnalysis.value.class_averages[className][subject] || 0
        })
        
        return {
          name: className,
          type: 'bar',
          data: data,
          barWidth: '15%'
        }
      })
      
      return {
        title: {
          text: '班级成绩对比',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: classes,
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
          name: '平均分'
        },
        series: series
      }
    })
    
    // 科目分布数据
    const subjectDistributionData = computed(() => {
      return subjectAnalysis.value || {}
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
      }
    })
    
    // 科目箱线图数据
    const subjectBoxPlotData = computed(() => {
      return subjectAnalysis.value || {}
    })
    
    // 科目箱线图配置
    const subjectBoxPlotOptions = computed(() => {
      if (!subjectAnalysis.value || !subjectAnalysis.value.statistics) return {}
      
      // 模拟箱线图数据（实际项目中应该从API获取）
      const boxData = [
        [subjectAnalysis.value.statistics.min_score, 
         subjectAnalysis.value.statistics.min_score + 10, 
         subjectAnalysis.value.statistics.median, 
         subjectAnalysis.value.statistics.median + 10, 
         subjectAnalysis.value.statistics.max_score]
      ]
      
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
      }
    })
    
    // 考试趋势数据
    const examTrendData = computed(() => {
      return examTrend.value || {}
    })
    
    // 考试趋势配置
    const examTrendOptions = computed(() => {
      if (!examTrend.value || !examTrend.value.exam_trend) return {}
      
      const examNames = examTrend.value.exam_trend.exam_names
      const averages = examTrend.value.exam_trend.averages
      
      return {
        title: {
          text: '年级历次考试趋势',
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
    })
    
    // 教师对比数据
    const teacherComparisonData = computed(() => {
      return teacherPerformance.value || {}
    })
    
    // 教师对比配置
    const teacherComparisonOptions = computed(() => {
      if (!teacherPerformance.value || !teacherPerformance.value.teacher_performance) return {}
      
      const teachers = Object.keys(teacherPerformance.value.teacher_performance)
      const data = teachers.map(teacher => teacherPerformance.value.teacher_performance[teacher].average)
      
      return {
        title: {
          text: '教师成绩对比',
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
          data: teachers,
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
            type: 'bar',
            data: data,
            itemStyle: {
              color: '#91cc75'
            }
          }
        ]
      }
    })
    
    // 教师热力图数据
    const teacherHeatmapData = computed(() => {
      return teacherPerformance.value || {}
    })
    
    // 教师热力图配置
    const teacherHeatmapOptions = computed(() => {
      if (!teacherPerformance.value || !teacherPerformance.value.teacher_performance) return {}
      
      // 处理热力图数据
      const heatmapData = []
      const teachers = Object.keys(teacherPerformance.value.teacher_performance)
      let index = 0
      
      teachers.forEach(teacher => {
        const teacherData = teacherPerformance.value.teacher_performance[teacher]
        // 为每个教师创建一个数据点，使用教师索引作为x轴，平均分为y轴，分数作为热力值
        heatmapData.push([index, 0, teacherData.average])
        index++
      })
      
      return {
        title: {
          text: '教师与成绩关系热力图',
          left: 'center'
        },
        tooltip: {
          position: 'top'
        },
        grid: {
          height: '60%',
          top: '10%'
        },
        xAxis: {
          type: 'category',
          data: teachers,
          splitArea: {
            show: true
          },
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'category',
          data: ['平均成绩'],
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 60,
          max: 100,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%',
          inRange: {
            color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
          }
        },
        series: [
          {
            name: '平均成绩',
            type: 'heatmap',
            data: heatmapData,
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    })
    
    onMounted(() => {
      loadGradeOptions()
    })
    
    return {
      gradeName,
      grades,
      isLoadingOptions,
      selectedSubject,
      subjects,
      gradeAnalysis,
      subjectAnalysis,
      examTrend,
      teacherPerformance,
      loading,
      gradeError,
      gradeSubjectData,
      gradeSubjectOptions,
      classComparisonData,
      classComparisonOptions,
      subjectDistributionData,
      subjectDistributionOptions,
      subjectBoxPlotData,
      subjectBoxPlotOptions,
      examTrendData,
      examTrendOptions,
      teacherComparisonData,
      teacherComparisonOptions,
      teacherHeatmapData,
      teacherHeatmapOptions,
      analyzeGrade,
      analyzeSubject
    }
  }
}
</script>

<style scoped>
.grade-analysis {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
  margin-bottom: 20px;
  color: #333;
}

.grade-input {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.grade-input select {
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

.grade-input button {
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

.grade-input button:hover {
  background: #66b1ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.grade-input button:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  animation: fadeIn 0.5s ease-out;
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

.grade-analysis-result {
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
  .grade-analysis {
    padding: 15px;
  }
  
  .grade-input {
    flex-wrap: wrap;
  }
  
  .grade-input select {
    flex: 1 1 200px;
  }
  
  .grade-input button {
    flex: 1 1 100px;
  }
}

@media (max-width: 768px) {
  .grade-analysis {
    padding: 10px;
  }
  
  .grade-input {
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
</style>