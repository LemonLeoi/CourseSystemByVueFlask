import { ref, computed, onMounted } from 'vue';
import { teacherApi } from '@/services/api/apiService';
import type { Teacher } from '@/types';

export function useTeacherManage(subjectFilter = ref('')) {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const searchQuery = ref('');
  const currentPage = ref(1);
  const itemsPerPage = ref(10);
  const allTeachers = ref<Teacher[]>([]);

  // 加载教师数据
  const loadTeachers = async () => {
    try {
      loading.value = true;
      error.value = null;
      const teachers = await teacherApi.getTeachers();
      // 转换后端数据格式以匹配前端类型
      allTeachers.value = teachers.map((teacher: any) => ({
        id: teacher.id || '',
        teacher_id: teacher.teacher_id || '',
        name: teacher.name,
        gender: teacher.gender,
        age: teacher.age || 0,
        subject: teacher.subject || teacher.department, // 后端的department对应前端的subject
        title: teacher.title,
        contact: teacher.contact || '',
        teachingClasses: teacher.teachingClasses || teacher.teaching_classes || [], // 处理不同的字段名
        isHomeroomTeacher: teacher.isHomeroomTeacher || teacher.is_homeroom_teacher || false, // 处理不同的字段名
        homeroomClass: teacher.homeroomClass || teacher.homeroom_class || '' // 处理不同的字段名
      }));
    } catch (err) {
      error.value = '加载教师数据失败';
      console.error('Error loading teachers:', err);
    } finally {
      loading.value = false;
    }
  };

  // 搜索教师
  const filteredTeachers = computed(() => {
    return allTeachers.value.filter(teacher => {
      // 搜索查询筛选
      const query = searchQuery.value.toLowerCase();
      const matchesSearch = !query || 
        teacher.name.toLowerCase().includes(query) ||
        teacher.teacher_id.includes(query) ||
        teacher.subject.includes(query) ||
        teacher.title.includes(query);
      
      // 学科筛选
      const matchesSubject = !subjectFilter.value || teacher.subject === subjectFilter.value;
      
      return matchesSearch && matchesSubject;
    });
  });

  // 分页后的教师
  const paginatedTeachers = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return filteredTeachers.value.slice(startIndex, endIndex);
  });

  // 总教师数
  const totalTeachers = computed(() => filteredTeachers.value.length);

  // 添加教师
  const addTeacher = async (teacher: Teacher) => {
    try {
      loading.value = true;
      error.value = null;
      // 转换前端数据格式以匹配后端模型
      const teacherData = {
        teacher_id: teacher.teacher_id,
        name: teacher.name,
        gender: teacher.gender,
        age: teacher.age,
        subject: teacher.subject,
        title: teacher.title,
        contact: teacher.contact,
        teachingClasses: teacher.teachingClasses,
        isHomeroomTeacher: teacher.isHomeroomTeacher,
        homeroomClass: teacher.homeroomClass
      };
      await teacherApi.addTeacher(teacherData);
      await loadTeachers();
      return true;
    } catch (err) {
      error.value = '添加教师失败';
      console.error('Error adding teacher:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 更新教师
  const updateTeacher = async (teacher: Teacher) => {
    try {
      loading.value = true;
      error.value = null;
      // 转换前端数据格式以匹配后端模型
      const teacherData = {
        name: teacher.name,
        gender: teacher.gender,
        age: teacher.age,
        title: teacher.title,
        department: teacher.subject, // 前端的subject对应后端的department
        contact: teacher.contact,
        teaching_classes: teacher.teachingClasses,
        is_homeroom_teacher: teacher.isHomeroomTeacher,
        homeroom_class: teacher.homeroomClass
      };
      await teacherApi.updateTeacher(teacher.teacher_id, teacherData);
      await loadTeachers();
      return true;
    } catch (err) {
      error.value = '更新教师失败';
      console.error('Error updating teacher:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 删除教师
  const deleteTeacher = async (teacher_id: string) => {
    try {
      loading.value = true;
      error.value = null;
      await teacherApi.deleteTeacher(teacher_id);
      await loadTeachers();
      return true;
    } catch (err) {
      error.value = '删除教师失败';
      console.error('Error deleting teacher:', err);
      return false;
    } finally {
      loading.value = false;
    }
  };

  // 根据ID获取教师
  const getTeacherById = async (id: string): Promise<Teacher | null> => {
    try {
      const teacher = await teacherApi.getTeacher(id) as any;
      // 转换后端数据格式以匹配前端类型
      return {
        id: teacher.id || '',
        teacher_id: teacher.teacher_id || '',
        name: teacher.name,
        gender: teacher.gender,
        age: teacher.age || 0,
        subject: teacher.subject || teacher.department, // 后端的department对应前端的subject
        title: teacher.title,
        contact: teacher.contact || '',
        teachingClasses: teacher.teachingClasses || teacher.teaching_classes || [], // 处理不同的字段名
        isHomeroomTeacher: teacher.isHomeroomTeacher || teacher.is_homeroom_teacher || false, // 处理不同的字段名
        homeroomClass: teacher.homeroomClass || teacher.homeroom_class || '' // 处理不同的字段名
      };
    } catch (err) {
      console.error('Error getting teacher by id:', err);
      return null;
    }
  };

  // 根据科目获取教师
  const getTeachersBySubject = (subject: string) => {
    return allTeachers.value.filter(teacher => teacher.subject === subject);
  };

  // 根据职称获取教师
  const getTeachersByTitle = (title: string) => {
    return allTeachers.value.filter(teacher => teacher.title === title);
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

  // 初始化数据
  onMounted(() => {
    loadTeachers();
  });

  return {
    // 状态
    loading,
    error,
    searchQuery,
    currentPage,
    itemsPerPage,
    
    // 数据
    allTeachers,
    filteredTeachers,
    paginatedTeachers,
    totalTeachers,
    
    // 方法
    loadTeachers,
    addTeacher,
    updateTeacher,
    deleteTeacher,
    getTeacherById,
    getTeachersBySubject,
    getTeachersByTitle,
    handleSearch,
    handlePageChange
  };
}
