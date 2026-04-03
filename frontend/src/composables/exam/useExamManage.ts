import { ref, computed, onMounted } from 'vue';
import { useExamStore } from '@/stores/exams';
import type { Exam } from '@/types';

export function useExamManage() {
  const examStore = useExamStore();
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref('');
  const currentPage = ref(1);
  const itemsPerPage = ref(10);
  const examTypeFilter = ref('');
  const gradeFilter = ref('');

  // 初始化考试数据
  const initializeExams = async () => {
    try {
      loading.value = true;
      error.value = null;
      // 从API获取数据
      const response = await fetch('http://localhost:5000/api/exams/');
      if (!response.ok) {
        throw new Error('Failed to fetch exams');
      }
      const responseData = await response.json();
      // 从响应中提取 data 字段
      const exams = responseData.data || [];
      // 确保 exams 是一个数组
      const examsArray = Array.isArray(exams) ? exams : [];
      examStore.initializeExams(examsArray);
    } catch (err) {
      error.value = '加载考试数据失败';
      console.error('Error loading exams:', err);
    } finally {
      loading.value = false;
    }
  };

  // 获取所有考试
  const allExams = computed(() => examStore.exams);

  // 筛选和搜索考试
  const filteredExams = computed(() => {
    let result = Array.isArray(allExams.value) ? allExams.value : [];

    // 按考试类型筛选
    if (examTypeFilter.value) {
      result = result.filter(exam => exam.type === examTypeFilter.value);
    }

    // 按年级筛选
    if (gradeFilter.value) {
      result = result.filter(exam => exam.grade === gradeFilter.value);
    }

    // 按搜索词搜索
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      result = result.filter(exam => 
        exam.name.toLowerCase().includes(query) ||
        exam.code.includes(query) ||
        exam.grade.includes(query) ||
        exam.startDate.includes(query)
      );
    }

    return result;
  });

  // 分页后的考试
  const paginatedExams = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return Array.isArray(filteredExams.value) ? filteredExams.value.slice(startIndex, endIndex) : [];
  });

  // 总考试数
  const totalExams = computed(() => Array.isArray(filteredExams.value) ? filteredExams.value.length : 0);

  // 添加考试
  const addExam = async (exam: Exam) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API添加考试
      const response = await fetch('http://localhost:5000/api/exams/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(exam)
      });
      if (!response.ok) {
        throw new Error('Failed to add exam');
      }
      const newExam = await response.json();
      // 更新本地存储
      examStore.addExam(newExam);
      return true;
    } catch (err) {
      error.value = '添加考试失败';
      console.error('Error adding exam:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 更新考试
  const updateExam = async (exam: Exam) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API更新考试
      const response = await fetch(`http://localhost:5000/api/exams/${exam.code}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(exam)
      });
      if (!response.ok) {
        throw new Error('Failed to update exam');
      }
      const updatedExam = await response.json();
      // 更新本地存储
      examStore.updateExam(updatedExam);
      return true;
    } catch (err) {
      error.value = '更新考试失败';
      console.error('Error updating exam:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 删除考试
  const deleteExam = async (code: string) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API删除考试
      const response = await fetch(`http://localhost:5000/api/exams/${code}`, {
        method: 'DELETE'
      });
      if (!response.ok) {
        throw new Error('Failed to delete exam');
      }
      // 更新本地存储
      examStore.deleteExam(code);
      return true;
    } catch (err) {
      error.value = '删除考试失败';
      console.error('Error deleting exam:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 根据Code获取考试
  const getExamByCode = (code: string) => {
    return examStore.getExamByCode(code);
  };

  // 根据类型获取考试
  const getExamsByType = (type: string) => {
    return examStore.getExamsByType(type);
  };

  // 根据年级获取考试
  const getExamsByGrade = (grade: string) => {
    return examStore.getExamsByGrade(grade);
  };

  // 获取即将到来的考试
  const getUpcomingExams = (days: number = 7) => {
    const today = new Date();
    const futureDate = new Date();
    futureDate.setDate(today.getDate() + days);

    return allExams.value.filter(exam => {
      const examDate = new Date(exam.startDate);
      return examDate >= today && examDate <= futureDate && exam.status !== '已归档';
    }).sort((a, b) => new Date(a.startDate).getTime() - new Date(b.startDate).getTime());
  };

  // 处理搜索
  const handleSearch = (query: string) => {
    searchQuery.value = query;
    currentPage.value = 1;
  };

  // 处理考试类型筛选变化
  const handleExamTypeFilterChange = (type: string) => {
    examTypeFilter.value = type;
    currentPage.value = 1;
  };

  // 处理年级筛选变化
  const handleGradeFilterChange = (grade: string) => {
    gradeFilter.value = grade;
    currentPage.value = 1;
  };

  // 处理分页
  const handlePageChange = (page: number) => {
    currentPage.value = page;
  };

  // 初始化数据
  onMounted(() => {
    if (examStore.exams.length === 0) {
      initializeExams();
    }
  });

  return {
    // 状态
    loading,
    error,
    searchQuery,
    currentPage,
    itemsPerPage,
    examTypeFilter,
    gradeFilter,
    
    // 数据
    allExams,
    filteredExams,
    paginatedExams,
    totalExams,
    
    // 方法
    initializeExams,
    addExam,
    updateExam,
    deleteExam,
    getExamByCode,
    getExamsByType,
    getExamsByGrade,
    getUpcomingExams,
    handleSearch,
    handleExamTypeFilterChange,
    handleGradeFilterChange,
    handlePageChange
  };
}
