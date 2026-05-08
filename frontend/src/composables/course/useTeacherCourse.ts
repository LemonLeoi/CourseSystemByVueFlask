import { ref, computed, onMounted, watch } from 'vue';
import { courseApi, teacherApi } from '@/services/api/apiService';
import type { TeacherCourse, TeacherStats } from '@/types/course';
import type { Teacher } from '@/types';
import { useTeacherStore } from '@/stores/teachers';

export function useTeacherCourse() {
  // 状态
  const selectedTeacher = ref('');
  const teacherCourses = ref<TeacherCourse[]>([]);

  // 教师数据
  const teachers = ref<Teacher[]>([]);

  // 操作状态
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const successMessage = ref<string | null>(null);

  // 教师存储
  const teacherStore = useTeacherStore();

  // 当前选中教师的名称
  const selectedTeacherName = computed(() => {
    const teacher = teachers.value.find(t => t.teacher_id === selectedTeacher.value);
    return teacher?.name || '';
  });

  // 教师课程统计
  const teacherStats = computed<TeacherStats>(() => {
    const courses = teacherCourses.value;
    const totalClasses = courses.length;
    
    const classCount: { [key: string]: number } = {};
    courses.forEach(c => {
      classCount[c.className] = (classCount[c.className] || 0) + 1;
    });
    
    const mostClass = Object.entries(classCount).sort((a, b) => b[1] - a[1])[0]?.[0] || '-';
    
    const dayCount: { [key: string]: number } = {};
    courses.forEach(c => {
      dayCount[c.day] = (dayCount[c.day] || 0) + 1;
    });
    
    const busiestDay = Object.entries(dayCount).sort((a, b) => b[1] - a[1])[0]?.[0] || '-';
    
    const avgClasses = totalClasses > 0 ? (totalClasses / 6).toFixed(1) : '0';
    
    return {
      totalClasses,
      mostClass,
      busiestDay,
      avgClasses
    };
  });

  // 模态框状态
  const showTeacherCourseModal = ref(false);
  const editingTeacherCourse = ref(false);
  const teacherCourseForm = ref<TeacherCourse>({
    day: '',
    timeSlot: 1,
    name: '',
    className: '',
    classroom: ''
  });

  // 加载教师列表
  const loadTeachers = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('=== 加载教师列表 ===');
      const teacherData = await teacherApi.getTeachers();
      console.log('获取到的教师数据:', teacherData);
      
      teachers.value = teacherData;
      teacherStore.initializeTeachers(teacherData);
      
      // 如果有教师，默认选择第一个（使用teacher_id而不是id）
      if (teachers.value.length > 0) {
        selectedTeacher.value = teachers.value[0].teacher_id;
        await loadTeacherCourses();
      }
    } catch (err) {
      error.value = '获取教师列表失败';
      console.error('Error loading teachers:', err);
      teachers.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // 加载教师课程数据
  const loadTeacherCourses = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      
      if (selectedTeacher.value) {
        console.log('=== 加载教师课程表 ===');
        console.log('教师ID:', selectedTeacher.value);
        const courses = await courseApi.getTeacherCourses(selectedTeacher.value);
        console.log('获取到的教师课程表数据:', courses);
        
        // 转换数据格式，确保与前端期望的格式一致
        teacherCourses.value = courses.map((course: any) => {
          // 转换星期格式
          const dayMap: { [key: string]: string } = {
            '周一': '星期一',
            '周二': '星期二',
            '周三': '星期三',
            '周四': '星期四',
            '周五': '星期五',
            '周六': '星期六',
            '周日': '星期日'
          };
          
          return {
            day: dayMap[course.day] || course.day,
            timeSlot: course.timeSlot,
            name: course.name || '',
            className: course.className || '',
            classroom: course.classroom || ''
          };
        });
      } else {
        teacherCourses.value = [];
      }
    } catch (err) {
      error.value = '加载课程表失败';
      console.error('Error loading teacher courses:', err);
      // 出错时使用默认数据
      teacherCourses.value = [
        { day: '星期一', timeSlot: 1, name: '语文', className: '高一1班', classroom: 'A101' },
        { day: '星期一', timeSlot: 2, name: '语文', className: '高一2班', classroom: 'A102' },
        { day: '星期一', timeSlot: 3, name: '语文', className: '高一3班', classroom: 'A103' },
        { day: '星期二', timeSlot: 1, name: '语文', className: '高二1班', classroom: 'B101' },
        { day: '星期二', timeSlot: 2, name: '语文', className: '高二2班', classroom: 'B102' },
        { day: '星期三', timeSlot: 1, name: '语文', className: '高三1班', classroom: 'C101' },
        { day: '星期三', timeSlot: 2, name: '语文', className: '高三2班', classroom: 'C102' }
      ];
    } finally {
      isLoading.value = false;
    }
  };

  // 辅助方法：将星期字符串转换为数字
  const getDayOfWeek = (day: string): number => {
    const dayMap: { [key: string]: number } = {
      '星期一': 1,
      '星期二': 2,
      '星期三': 3,
      '星期四': 4,
      '星期五': 5,
      '星期六': 6,
      '星期日': 7
    };
    return dayMap[day] || 1;
  };

  // 辅助方法：获取课程ID（暂时未使用）
  // const getCourseIdByName = async (courseName: string): Promise<number> => {
  //   try {
  //     const courses = await courseApi.getCourses();
  //     const matchedCourse = courses.find((c: any) => c.course_name === courseName);
  //     return matchedCourse ? Number(matchedCourse.id) : 1;
  //   } catch (error) {
  //     console.warn('获取课程ID失败，使用默认值:', error);
  //     return 1;
  //   }
  // };

  // 辅助方法：将className拆分为grade和class（暂时未使用）
  // const splitClassName = (className: string) => {
  //   // 假设className格式为 "高一1班"、"高二3班" 等
  //   if (className.length >= 3) {
  //     const grade = className.substring(0, 2); // 取前两个字符作为年级
  //     const class_ = className.substring(2); // 剩余部分作为班级
  //     return { grade, class: class_ };
  //   }
  //   return { grade: '', class: className };
  // };

  // 添加教师课程
  const addTeacherCourse = async (course: TeacherCourse) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      // 验证教室是否已选择
      const roomId = (course as any).room_id;
      if (!roomId) {
        error.value = '请选择教室';
        return false;
      }
      
      // 验证教师是否已选择
      if (!selectedTeacher.value) {
        error.value = '请选择任课教师';
        return false;
      }
      
      // 课程ID获取（暂时未使用）
      // const courseId = await getCourseIdByName(course.name);
      
      // 转换星期为数字（1-7）
      const dayMap: { [key: string]: number } = {
        '星期一': 1,
        '星期二': 2,
        '星期三': 3,
        '星期四': 4,
        '星期五': 5,
        '星期六': 6,
        '星期日': 7
      };
      const dayOfWeek = dayMap[course.day] || 1;
      
      // 转换为API需要的格式
      const backendCourse = {
        course_code: (course as any).course_code,
        day_of_week: dayOfWeek,
        period: course.timeSlot,
        classroom: (course as any).room_id || course.classroom,
        teacher: selectedTeacher.value,
        className: course.className
      };
      
      console.log('=== 添加教师课程 ===');
      console.log('课程数据:', backendCourse);
      await courseApi.addTeacherCourse(backendCourse);
      await loadTeacherCourses();
      successMessage.value = '课程添加成功';
      return true;
    } catch (err) {
      error.value = '添加课程失败';
      console.error('Error adding teacher course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 更新教师课程
  const updateTeacherCourse = async (course: TeacherCourse) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      // 验证教室是否已选择
      const roomId = (course as any).room_id;
      if (!roomId) {
        error.value = '请选择教室';
        return false;
      }
      
      // 验证教师是否已选择
      if (!selectedTeacher.value) {
        error.value = '请选择任课教师';
        return false;
      }
      
      // 课程ID获取（暂时未使用）
      // const courseId = await getCourseIdByName(course.name);
      
      // 转换星期为数字（1-7）
      const dayMap: { [key: string]: number } = {
        '星期一': 1,
        '星期二': 2,
        '星期三': 3,
        '星期四': 4,
        '星期五': 5,
        '星期六': 6,
        '星期日': 7
      };
      const dayOfWeek = dayMap[course.day] || 1;
      
      // 转换为API需要的格式
      const backendCourse = {
        course_code: (course as any).course_code,
        day_of_week: dayOfWeek,
        period: course.timeSlot,
        classroom: (course as any).room_id || course.classroom,
        teacher: selectedTeacher.value,
        className: course.className
      };
      
      console.log('=== 更新教师课程 ===');
      console.log('课程数据:', backendCourse);
      
      // 查找要更新的课程
      const existingCourse = teacherCourses.value.find(
        c => c.day === course.day && c.timeSlot === course.timeSlot
      );
      
      if (existingCourse) {
        // 这里简化处理，实际应该根据ID更新
        // 由于我们没有课程ID，这里先删除旧课程，再添加新课程
        await deleteTeacherCourse(course.day, course.timeSlot);
        await addTeacherCourse(course);
      }
      
      await loadTeacherCourses();
      successMessage.value = '课程更新成功';
      return true;
    } catch (err) {
      error.value = '更新课程失败';
      console.error('Error updating teacher course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 删除教师课程
  const deleteTeacherCourse = async (day: string, timeSlot: number) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('=== 删除教师课程 ===');
      console.log('删除信息:', { day, timeSlot });
      
      // 获取所有教师课程，找到对应的课程ID
      const courses = await courseApi.getTeacherCourses(selectedTeacher.value);
      
      // 找到对应的课程
      const dayOfWeek = getDayOfWeek(day);
      const targetCourse = courses.find((course: any) => {
        const courseDay = course.day_of_week || getDayOfWeek(course.day);
        return courseDay === dayOfWeek && course.period === timeSlot;
      });
      
      if (targetCourse && targetCourse.id) {
        await courseApi.deleteTeacherCourse(Number(targetCourse.id));
        await loadTeacherCourses();
        successMessage.value = '课程删除成功';
        return true;
      } else {
        error.value = '未找到对应的课程';
        return false;
      }
    } catch (err) {
      error.value = '删除课程失败';
      console.error('Error deleting teacher course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 根据教师更新课程表
  const updateTeacherCoursesByTeacher = async () => {
    await loadTeacherCourses();
  };

  // 刷新教师课程表
  const refreshTeacherSchedule = async () => {
    await loadTeacherCourses();
  };

  // 获取指定天和时间段的课程
  const getTeacherCourse = (day: string, timeSlot: number) => {
    return teacherCourses.value.find(c => c.day === day && c.timeSlot === timeSlot);
  };

  // 模态框相关方法
  const openAddTeacherCourseModal = (day: string = '星期一', timeSlot: number = 1) => {
    editingTeacherCourse.value = false;
    teacherCourseForm.value = {
      day: day,
      timeSlot: timeSlot,
      name: '',
      className: '',
      classroom: ''
    };
    showTeacherCourseModal.value = true;
  };

  const openEditTeacherCourseModal = (day: string, timeSlot: number) => {
    const existingCourse = getTeacherCourse(day, timeSlot);
    if (existingCourse) {
      teacherCourseForm.value = { ...existingCourse };
      editingTeacherCourse.value = true;
    } else {
      teacherCourseForm.value = {
        day,
        timeSlot,
        name: '',
        className: '',
        classroom: ''
      };
      editingTeacherCourse.value = false;
    }
    showTeacherCourseModal.value = true;
  };

  const closeTeacherCourseModal = () => {
    showTeacherCourseModal.value = false;
    editingTeacherCourse.value = false;
  };

  const saveTeacherCourse = async () => {
    if (editingTeacherCourse.value) {
      await updateTeacherCourse(teacherCourseForm.value);
    } else {
      await addTeacherCourse(teacherCourseForm.value);
    }
    closeTeacherCourseModal();
  };

  // 监听selectedTeacher变化，自动加载对应教师的课程
  watch(selectedTeacher, async (newTeacherId) => {
    if (newTeacherId) {
      await loadTeacherCourses();
    } else {
      teacherCourses.value = [];
    }
  });

  // 初始化数据
  onMounted(() => {
    loadTeachers();
  });

  return {
    // 状态
    selectedTeacher,
    teachers,
    teacherCourses,
    teacherStats,
    
    // 模态框状态
    showTeacherCourseModal,
    editingTeacherCourse,
    teacherCourseForm,
    
    // 操作状态
    isLoading,
    error,
    successMessage,
    
    // 方法
    getTeacherCourse,
    refreshTeacherSchedule,
    updateTeacherCoursesByTeacher,
    openAddTeacherCourseModal,
    openEditTeacherCourseModal,
    closeTeacherCourseModal,
    saveTeacherCourse,
    deleteTeacherCourse
  };
}
