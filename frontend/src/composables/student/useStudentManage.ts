import { ref, computed, onMounted, watch } from 'vue';
import { studentApi } from '@/services/api/apiService';
import type { Student, Score } from '@/types';

export function useStudentManage() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref('');
  const currentPage = ref(1);
  const itemsPerPage = ref(10);
  const gradeFilter = ref('');
  const classFilter = ref('');
  const allStudents = ref<Student[]>([]);

  // 加载学生数据
  const loadStudents = async () => {
    try {
      loading.value = true;
      error.value = null;
      console.log('=== 开始加载学生数据 ===');
      console.log('年级筛选:', gradeFilter.value);
      console.log('班级筛选:', classFilter.value);
      const students = await studentApi.getStudents(gradeFilter.value, classFilter.value);
      console.log('=== 学生数据加载成功 ===');
      console.log('学生数据:', students);
      allStudents.value = students;
    } catch (err) {
      error.value = '加载学生数据失败';
      console.error('=== 加载学生数据失败 ===');
      console.error('错误信息:', err);
    } finally {
      loading.value = false;
    }
  };

  // 搜索学生
  const filteredStudents = computed(() => {
    console.log('=== 计算filteredStudents ===');
    console.log('年级筛选:', gradeFilter.value);
    console.log('班级筛选:', classFilter.value);
    console.log('搜索查询:', searchQuery.value);
    console.log('学生总数:', allStudents.value.length);
    
    const result = allStudents.value.filter(student => {
      // 搜索查询筛选
      const query = searchQuery.value.toLowerCase();
      const matchesSearch = !query || 
        student.name.toLowerCase().includes(query) ||
        student.id.includes(query) ||
        student.grade.includes(query) ||
        student.class.includes(query);
      
      // 年级筛选
      const matchesGrade = !gradeFilter.value || student.grade === gradeFilter.value;
      
      // 班级筛选
      const matchesClass = !classFilter.value || student.class === classFilter.value;
      
      return matchesSearch && matchesGrade && matchesClass;
    });
    
    console.log('筛选后学生数:', result.length);
    return result;
  });

  // 分页后的学生
  const paginatedStudents = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return filteredStudents.value.slice(startIndex, endIndex);
  });

  // 总学生数
  const totalStudents = computed(() => filteredStudents.value.length);

  // 添加学生
  const addStudent = async (student: Student) => {
    try {
      loading.value = true;
      error.value = null;
      await studentApi.addStudent(student);
      await loadStudents();
      return true;
    } catch (err) {
      error.value = '添加学生失败';
      console.error('Error adding student:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 更新学生
  const updateStudent = async (student: Student) => {
    try {
      loading.value = true;
      error.value = null;
      await studentApi.updateStudent(student.id, student);
      await loadStudents();
      return true;
    } catch (err) {
      error.value = '更新学生失败';
      console.error('Error updating student:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 删除学生
  const deleteStudent = async (id: string) => {
    try {
      loading.value = true;
      error.value = null;
      await studentApi.deleteStudent(id);
      await loadStudents();
      return true;
    } catch (err) {
      error.value = '删除学生失败';
      console.error('Error deleting student:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 更新学生成绩
  const updateStudentScores = async (studentId: string, scores: Score[]) => {
    try {
      loading.value = true;
      error.value = null;
      console.log('=== 开始更新学生成绩 ===');
      console.log('学生ID:', studentId);
      console.log('成绩数据:', scores);
      
      // 等待API调用完全完成
      const result = await studentApi.updateStudentGrades(studentId, scores);
      console.log('=== API调用成功 ===');
      console.log('API响应:', result);
      
      // 等待数据重新加载完成
      console.log('=== 开始重新加载学生数据 ===');
      await loadStudents();
      console.log('=== 学生数据重新加载完成 ===');
      
      return true;
    } catch (err) {
      error.value = '更新学生成绩失败';
      console.error('=== 更新学生成绩失败 ===');
      console.error('错误信息:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 根据ID获取学生
  const getStudentById = async (id: string): Promise<Student | null> => {
    try {
      const student = await studentApi.getStudent(id);
      return student;
    } catch (err) {
      console.error('Error getting student by id:', err);
      return null;
    }
  };

  // 计算学生平均成绩
  const calculateAverageScore = (student: Student): number => {
    if (!student.scores || student.scores.length === 0) {
      return 0;
    }
    const total = student.scores.reduce((sum, score) => sum + score.score, 0);
    return Math.round(total / student.scores.length);
  };

  // 检查学生是否及格
  const checkIfPassed = (student: Student): boolean => {
    if (!student.scores || student.scores.length === 0) {
      return false;
    }
    return student.scores.every(score => score.score >= 60);
  };

  // 处理搜索
  const handleSearch = (query: string) => {
    searchQuery.value = query;
    currentPage.value = 1;
  };

  // 处理分页
  const handlePageChange = (page: number) => {
    currentPage.value = page;
  };

  // 监听筛选条件变化
  watch([gradeFilter, classFilter], (newValues) => {
    console.log('=== 监听到筛选条件变化 ===');
    console.log('新的筛选值:', newValues);
    currentPage.value = 1;
    loadStudents();
  });

  // 初始化数据
  onMounted(() => {
    loadStudents();
  });

  return {
    // 状态
    loading,
    error,
    searchQuery,
    currentPage,
    itemsPerPage,
    gradeFilter,
    classFilter,
    
    // 数据
    allStudents,
    filteredStudents,
    paginatedStudents,
    totalStudents,
    
    // 方法
    loadStudents,
    addStudent,
    updateStudent,
    deleteStudent,
    updateStudentScores,
    getStudentById,
    calculateAverageScore,
    checkIfPassed,
    handleSearch,
    handlePageChange
  };
}
