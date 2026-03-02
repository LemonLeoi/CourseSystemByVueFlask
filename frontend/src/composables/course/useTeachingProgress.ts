import { ref, onMounted, watch } from 'vue';
import { courseApi } from '@/services/api/apiService';
import type { TeachingProgress } from '@/types/course';

export function useTeachingProgress() {
  // 状态
  const progressSubject = ref('语文');
  const progressGrade = ref('高一');
  const teachingProgress = ref<TeachingProgress[]>([]);

  // 模态框状态
  const showProgressModal = ref(false);
  const editingProgress = ref<TeachingProgress | null>(null);
  const progressForm = ref<TeachingProgress>({
    id: 0,
    chapter: '',
    hours: 1,
    objective: '',
    progress: 0,
    status: 'not-started'
  });

  // 操作状态
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const successMessage = ref<string | null>(null);

  // 初始化数据
  onMounted(() => {
    loadTeachingProgress();
  });

  // 监听科目和年级变化，自动更新教学进度
  watch(
    [progressSubject, progressGrade],
    async () => {
      console.log('=== 科目或年级变化，更新教学进度 ===');
      console.log('新科目:', progressSubject.value);
      console.log('新年级:', progressGrade.value);
      await loadTeachingProgress();
    },
    { immediate: false }
  );

  // 加载教学进度数据
  const loadTeachingProgress = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('=== 加载教学进度 ===');
      console.log('科目:', progressSubject.value);
      console.log('年级:', progressGrade.value);
      
      // 根据科目和年级获取教学进度
      const progress = await courseApi.getTeachingProgressBySubjectGrade(progressSubject.value, progressGrade.value);
      
      console.log('获取到的教学进度数据:', progress);
      
      if (progress && progress.length > 0) {
        // 转换数据格式，确保与前端期望的格式一致
        teachingProgress.value = progress.map(item => ({
          id: item.id,
          chapter: item.chapter || '',
          hours: item.hours || 1,
          objective: item.objective || '',
          progress: item.progress || 0,
          status: item.status || 'not-started'
        }));
      } else {
        // 如果获取到的数据为空，使用空数组
        teachingProgress.value = [];
      }
    } catch (err) {
      error.value = '获取教学进度失败';
      console.error('Error loading teaching progress:', err);
      // 出错时使用空数组
      teachingProgress.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // 添加教学进度
  const addTeachingProgress = async (progress: TeachingProgress) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('=== 添加教学进度 ===');
      console.log('进度数据:', progress);
      console.log('当前科目:', progressSubject.value);
      console.log('当前年级:', progressGrade.value);
      
      // 获取对应科目和年级的课程ID
      const courseId = await getCourseIdBySubjectGrade(progressSubject.value, progressGrade.value);
      if (!courseId) {
        error.value = '未找到对应科目和年级的课程';
        return false;
      }
      
      // 转换为后端需要的格式
      const backendProgress = {
        ...progress,
        course_id: courseId
      };
      
      console.log('发送到后端的数据:', backendProgress);
      
      await courseApi.addTeachingProgress(backendProgress);
      await loadTeachingProgress();
      successMessage.value = '进度添加成功';
      return true;
    } catch (err) {
      error.value = '添加进度失败';
      console.error('Error adding teaching progress:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 更新教学进度
  const updateTeachingProgress = async (id: number, progress: TeachingProgress) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      await courseApi.updateTeachingProgress(id, progress);
      await loadTeachingProgress();
      successMessage.value = '进度更新成功';
      return true;
    } catch (err) {
      error.value = '更新进度失败';
      console.error('Error updating teaching progress:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 根据科目和年级获取课程ID
  const getCourseIdBySubjectGrade = async (subject: string, grade: string): Promise<number | null> => {
    try {
      console.log('=== 获取课程ID ===');
      console.log('科目:', subject);
      console.log('年级:', grade);
      
      // 获取课程列表
      const courses = await courseApi.getCourses();
      console.log('获取到的课程列表:', courses);
      
      // 查找对应科目和年级的课程
      const course = courses.find((c: any) => c.subject === subject && c.grade === grade);
      
      if (course) {
        console.log('找到对应课程:', course);
        return course.id;
      } else {
        console.log('未找到对应课程');
        return null;
      }
    } catch (err) {
      console.error('Error getting course ID:', err);
      return null;
    }
  };

  // 删除教学进度
  const deleteTeachingProgress = async (id: number) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      await courseApi.deleteTeachingProgress(id);
      await loadTeachingProgress();
      successMessage.value = '进度删除成功';
      return true;
    } catch (err) {
      error.value = '删除进度失败';
      console.error('Error deleting teaching progress:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 刷新教学进度
  const refreshProgress = async () => {
    await loadTeachingProgress();
  };

  // 获取状态文本
  const getStatusText = (status: string): string => {
    const statusMap: { [key: string]: string } = {
      'completed': '已完成',
      'in-progress': '进行中',
      'not-started': '未开始'
    };
    return statusMap[status] || status;
  };

  // 模态框相关方法
  const openAddProgressModal = () => {
    editingProgress.value = null;
    progressForm.value = {
      id: 0,
      chapter: '',
      hours: 1,
      objective: '',
      progress: 0,
      status: 'not-started'
    };
    showProgressModal.value = true;
  };

  const editProgress = (chapter: TeachingProgress) => {
    editingProgress.value = chapter;
    progressForm.value = { ...chapter };
    showProgressModal.value = true;
  };

  const closeProgressModal = () => {
    showProgressModal.value = false;
    editingProgress.value = null;
  };

  const saveProgress = async () => {
    if (editingProgress.value) {
      await updateTeachingProgress(editingProgress.value.id, progressForm.value);
    } else {
      await addTeachingProgress(progressForm.value);
    }
    closeProgressModal();
  };

  return {
    // 状态
    progressSubject,
    progressGrade,
    teachingProgress,
    
    // 模态框状态
    showProgressModal,
    editingProgress,
    progressForm,
    
    // 操作状态
    isLoading,
    error,
    successMessage,
    
    // 方法
    getStatusText,
    loadTeachingProgress,
    addTeachingProgress,
    updateTeachingProgress,
    deleteTeachingProgress,
    refreshProgress,
    openAddProgressModal,
    editProgress,
    closeProgressModal,
    saveProgress
  };
}
