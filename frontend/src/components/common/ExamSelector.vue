<template>
  <div class="exam-selector">
    <select
      v-model="selectedExam"
      class="filter-select exam-select"
      :disabled="!isEnabled || isLoading"
    >
      <option value="">请选择考试场次</option>
      <option value="all">所有考试综合分析</option>
      <option v-for="exam in examList" :key="getExamKey(exam)" :value="getExamValue(exam)">
        {{ getExamName(exam) }} ({{ getExamAcademicYear(exam) }} {{ getExamSemester(exam) }})
      </option>
    </select>
  </div>
</template>

<script>
import { ref, watch, computed } from 'vue';
import { gradeService } from '../../services/gradeService';

export default {
  name: 'ExamSelector',
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    parentValue: {
      type: String,
      default: ''
    },
    studentId: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const selectedExam = ref(props.modelValue);
    const examList = ref([]);
    const isLoading = ref(false);

    const isEnabled = computed(() => {
      if (props.studentId) {
        return true;
      }
      return !!props.parentValue;
    });

    // 兼容两种数据类型：ExamInfo 和 StudentExamInfo
    const getExamKey = (exam) => {
      return exam.examCode || exam.code || exam.id || Math.random().toString(36).substr(2, 9);
    };

    const getExamValue = (exam) => {
      return exam.examCode || exam.code || exam.id || '';
    };

    const getExamName = (exam) => {
      return exam.examName || exam.name || '未知考试';
    };

    const getExamAcademicYear = (exam) => {
      return exam.academicYear || exam.academic_year || '';
    };

    const getExamSemester = (exam) => {
      return exam.semester || '';
    };

    const loadExamsByGrade = async (grade) => {
      if (!grade) {
        examList.value = [];
        return;
      }

      isLoading.value = true;
      try {
        const examData = await gradeService.getExamList(grade);
        examList.value = examData || [];
      } catch (error) {
        console.error('按年级获取考试列表失败:', error);
        examList.value = [];
      } finally {
        isLoading.value = false;
      }
    };

    const loadExamsByStudent = async (studentId) => {
      if (!studentId) {
        examList.value = [];
        return;
      }

      isLoading.value = true;
      try {
        const response = await gradeService.getStudentExamList(studentId);
        if (response && response.exams) {
          examList.value = response.exams;
        } else {
          examList.value = [];
        }
      } catch (error) {
        console.error('按学生ID获取考试列表失败:', error);
        examList.value = [];
      } finally {
        isLoading.value = false;
      }
    };

    const loadExams = async () => {
      if (props.studentId) {
        await loadExamsByStudent(props.studentId);
      } else if (props.parentValue) {
        const grade = props.parentValue.slice(0, 2);
        await loadExamsByGrade(grade);
      } else {
        examList.value = [];
      }
    };

    watch(selectedExam, (newVal) => {
      emit('update:modelValue', newVal);
    });

    watch(() => props.parentValue, () => {
      selectedExam.value = '';
      loadExams();
    });

    watch(() => props.studentId, () => {
      selectedExam.value = '';
      loadExams();
    });

    watch(() => props.modelValue, (newVal) => {
      selectedExam.value = newVal;
    });

    return {
      selectedExam,
      examList,
      isLoading,
      isEnabled,
      loadExams,
      getExamKey,
      getExamValue,
      getExamName,
      getExamAcademicYear,
      getExamSemester
    };
  }
};
</script>

<style scoped>
.exam-selector {
  display: inline-block;
}

.exam-select {
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 220px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.exam-select:focus {
  border-color: #409eff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(64, 158, 255, 0.25);
}

.exam-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>