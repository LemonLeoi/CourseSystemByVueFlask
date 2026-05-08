import { ref, computed, onMounted } from 'vue';
import { useStudentStatusStore } from '@/stores/studentStatus';
import type { StudentStatus } from '@/types';
import { studentApi } from '@/services/api/apiService';

export function useStudentStatusManage() {
  const studentStatusStore = useStudentStatusStore();
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref('');
  const currentPage = ref(1);
  const itemsPerPage = ref(10);
  const gradeFilter = ref('');
  const classFilter = ref('');

  // 初始化学生状态数据
  const initializeStudents = async () => {
    try {
      loading.value = true;
      error.value = null;
      // 从API获取数据
      const students = await studentApi.getStudents();
      // 转换为StudentStatus类型
      const studentStatuses = students.map(student => ({
        ...student,
        status: 'active' as const,
        statusText: '在校'
      }));
      studentStatusStore.initializeStudents(studentStatuses);
    } catch (err) {
      error.value = '加载学生状态数据失败';
      console.error('Error loading student status:', err);
    } finally {
      loading.value = false;
    }
  };

  // 获取所有学生状态
  const allStudents = computed(() => studentStatusStore.students);

  // 搜索学生状态
  const filteredStudents = computed(() => {
    let result = allStudents.value;

    // 按年级筛选
    if (gradeFilter.value) {
      result = result.filter(student => student.grade === gradeFilter.value);
    }

    // 按班级筛选
    if (classFilter.value) {
      result = result.filter(student => student.class === classFilter.value);
    }

    // 按搜索词搜索
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      result = result.filter(student => 
        student.name.toLowerCase().includes(query) ||
        student.id.includes(query) ||
        student.grade.includes(query) ||
        student.class.includes(query)
      );
    }

    return result;
  });

  // 分页后的学生状态
  const paginatedStudents = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return filteredStudents.value.slice(startIndex, endIndex);
  });

  // 总学生数
  const totalStudents = computed(() => filteredStudents.value.length);

  // 添加学生状态
  const addStudent = async (student: StudentStatus) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API添加学生
      const newStudent = await studentApi.addStudent({
        name: student.name,
        gender: student.gender,
        grade: student.grade,
        class: student.class
      });
      // 转换为StudentStatus类型
      const newStudentStatus = {
        ...newStudent,
        status: student.status,
        statusText: student.statusText
      };
      // 添加到存储
      studentStatusStore.addStudent(newStudentStatus);
      return true;
    } catch (err) {
      error.value = '添加学生状态失败';
      console.error('Error adding student status:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 更新学生状态
  const updateStudent = async (student: StudentStatus) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API更新学生
      const updatedStudent = await studentApi.updateStudent(student.id, {
        name: student.name,
        gender: student.gender,
        grade: student.grade,
        class: student.class
      });
      // 转换为StudentStatus类型
      const updatedStudentStatus = {
        ...updatedStudent,
        status: student.status,
        statusText: student.statusText
      };
      // 更新存储
      studentStatusStore.updateStudent(updatedStudentStatus);
      return true;
    } catch (err) {
      error.value = '更新学生状态失败';
      console.error('Error updating student status:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 删除学生状态
  const deleteStudent = async (id: string) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API删除学生状态
      await studentApi.deleteStudent(id);
      // 从存储中删除
      studentStatusStore.deleteStudent(id);
      return true;
    } catch (err) {
      error.value = '删除学生状态失败';
      console.error('Error deleting student status:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 根据ID获取学生状态
  const getStudentById = (id: string) => {
    return studentStatusStore.getStudentById(id);
  };

  // 根据年级获取学生状态
  const getStudentsByGrade = (grade: string) => {
    return studentStatusStore.getStudentsByGrade(grade);
  };

  // 根据班级获取学生状态
  const getStudentsByClass = (grade: string, className: string) => {
    return studentStatusStore.getStudentsByClass(grade, className);
  };

  // 根据状态获取学生
  const getStudentsByStatus = (status: string) => {
    return studentStatusStore.getStudentsByStatus(status);
  };

  // 归档学生（设置为毕业状态）
  const archiveStudent = async (student: StudentStatus) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API更新学生基本信息
      const updatedStudent = await studentApi.updateStudent(student.id, {
        name: student.name,
        gender: student.gender,
        grade: student.grade,
        class: student.class
      });
      // 转换为StudentStatus类型并更新状态
      const updatedStudentStatus = {
        ...updatedStudent,
        status: 'graduated' as const,
        statusText: '毕业'
      };
      // 更新存储
      studentStatusStore.updateStudent(updatedStudentStatus);
      return true;
    } catch (err) {
      error.value = '归档学生失败';
      console.error('Error archiving student:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 取消归档学生（设置为在校状态）
  const unarchiveStudent = async (student: StudentStatus) => {
    try {
      loading.value = true;
      error.value = null;
      // 调用API更新学生基本信息
      const updatedStudent = await studentApi.updateStudent(student.id, {
        name: student.name,
        gender: student.gender,
        grade: student.grade,
        class: student.class
      });
      // 转换为StudentStatus类型并更新状态
      const updatedStudentStatus = {
        ...updatedStudent,
        status: 'active' as const,
        statusText: '在校'
      };
      // 更新存储
      studentStatusStore.updateStudent(updatedStudentStatus);
      return true;
    } catch (err) {
      error.value = '取消归档学生失败';
      console.error('Error unarchiving student:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 处理搜索
  const handleSearch = (query: string) => {
    searchQuery.value = query;
    currentPage.value = 1;
  };

  // 处理年级筛选变化
  const handleGradeFilterChange = (grade: string) => {
    gradeFilter.value = grade;
    currentPage.value = 1;
  };

  // 处理班级筛选变化
  const handleClassFilterChange = (className: string) => {
    classFilter.value = className;
    currentPage.value = 1;
  };

  // 处理分页
  const handlePageChange = (page: number) => {
    currentPage.value = page;
  };

  // 初始化数据
  onMounted(() => {
    if (studentStatusStore.students.length === 0) {
      initializeStudents();
    }
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
    initializeStudents,
    addStudent,
    updateStudent,
    deleteStudent,
    getStudentById,
    getStudentsByGrade,
    getStudentsByClass,
    getStudentsByStatus,
    archiveStudent,
    unarchiveStudent,
    handleSearch,
    handleGradeFilterChange,
    handleClassFilterChange,
    handlePageChange
  };
}
