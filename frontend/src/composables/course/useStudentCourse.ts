import { ref, onMounted, watch } from 'vue';
import { courseApi, teacherApi } from '@/services/api/apiService';
import type { StudentCourse } from '@/types/course';
import type { Teacher } from '@/types';
import { useTeacherStore } from '@/stores/teachers';

export function useStudentCourse() {
  // 状态
  const studentGrade = ref('高一');
  const studentClass = ref('1班');
  const studentCourses = ref<StudentCourse[]>([]);
  
  // 教师相关状态
  const teachers = ref<Teacher[]>([]);
  const selectedTeacherId = ref('');
  const selectedTeacher = ref<Teacher | null>(null);
  
  // 操作状态
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const successMessage = ref<string | null>(null);
  
  // 教师存储
  const teacherStore = useTeacherStore();
  
  // 模态框状态
  const showStudentCourseModal = ref(false);
  const editingStudentCourse = ref(false);
  const studentCourseForm = ref<StudentCourse>({
    day: '',
    timeSlot: 1,
    name: '',
    teacher: '',
    classroom: ''
  });

  // 监听年级和班级变化，自动更新课程表
  watch(
    [studentGrade, studentClass],
    async () => {
      console.log('=== 年级或班级变化，更新课程表 ===');
      console.log('新年级:', studentGrade.value);
      console.log('新班级:', studentClass.value);
      await loadStudentCourses();
    },
    { immediate: false }
  );

  // 加载教师数据
  const loadTeachers = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('加载教师数据');
      
      const teacherData = await teacherApi.getTeachers();
      console.log('获取到的教师数据:', teacherData);
      
      teachers.value = teacherData;
      teacherStore.initializeTeachers(teacherData);
    } catch (err) {
      error.value = '加载教师数据失败';
      console.error('Error loading teachers:', err);
      teachers.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // 加载学生课程数据
  const loadStudentCourses = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log(`加载${studentGrade.value}${studentClass.value}的课程表`);
      
      const courses = await courseApi.getStudentCourses(studentClass.value, studentGrade.value);
      console.log('获取到的学生课程表数据:', courses);
      
      // 转换数据格式，确保与前端期望的格式一致
      studentCourses.value = courses.map((course: any) => {
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
        
        // 将教师ID转换为教师姓名
        let teacherName = course.teacher || '';
        if (course.teacher) {
          const teacher = teachers.value.find(t => t.id === course.teacher || t.teacher_id === course.teacher);
          if (teacher) {
            teacherName = teacher.name;
          }
        }
        
        return {
          day: dayMap[course.day] || course.day,
          timeSlot: course.timeSlot,
          name: course.name || '',
          teacher: teacherName,
          classroom: course.classroom || ''
        };
      });
    } catch (err) {
      error.value = '加载课程表失败';
      console.error('Error loading student courses:', err);
      // 出错时使用默认数据
      studentCourses.value = [
        { day: '星期一', timeSlot: 1, name: '语文', teacher: '张老师', classroom: 'A101' },
        { day: '星期一', timeSlot: 2, name: '数学', teacher: '李老师', classroom: 'A102' },
        { day: '星期一', timeSlot: 3, name: '英语', teacher: '王老师', classroom: 'A103' },
        { day: '星期一', timeSlot: 4, name: '物理', teacher: '赵老师', classroom: 'B101' },
        { day: '星期一', timeSlot: 5, name: '化学', teacher: '孙老师', classroom: 'B102' },
        { day: '星期一', timeSlot: 6, name: '生物', teacher: '周老师', classroom: 'B103' },
        { day: '星期一', timeSlot: 7, name: '体育', teacher: '郑老师', classroom: '操场' },
        { day: '星期二', timeSlot: 1, name: '数学', teacher: '李老师', classroom: 'A102' },
        { day: '星期二', timeSlot: 2, name: '语文', teacher: '张老师', classroom: 'A101' },
        { day: '星期二', timeSlot: 3, name: '英语', teacher: '王老师', classroom: 'A103' },
        { day: '星期二', timeSlot: 4, name: '化学', teacher: '孙老师', classroom: 'B102' },
        { day: '星期二', timeSlot: 5, name: '物理', teacher: '赵老师', classroom: 'B101' },
        { day: '星期二', timeSlot: 6, name: '历史', teacher: '吴老师', classroom: 'C101' },
        { day: '星期二', timeSlot: 7, name: '政治', teacher: '王老师', classroom: 'C102' }
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
  //     if (matchedCourse) {
  //       return Number(matchedCourse.id);
  //     } else {
  //       console.warn('未找到匹配的课程，使用默认值:', courseName);
  //       return 1;
  //     }
  //   } catch (error) {
  //     console.warn('获取课程ID失败，使用默认值:', error);
  //     return 1;
  //   }
  // };

  // 处理教师选择变化
  const handleTeacherSelect = (teacherId: string) => {
    selectedTeacherId.value = teacherId;
    const teacher = teachers.value.find(t => t.id === teacherId);
    selectedTeacher.value = teacher || null;
    console.log('选择的教师:', selectedTeacher.value);
  };

  // 添加学生课程
  const addStudentCourse = async (course: StudentCourse) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      // 验证教师是否已选择
      if (!selectedTeacherId.value) {
        error.value = '请选择任课教师';
        return false;
      }
      
      // 验证教室是否已选择
      const roomId = (course as any).room_id;
      if (!roomId) {
        error.value = '请选择教室';
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
        name: course.name,
        day_of_week: dayOfWeek,
        period: course.timeSlot,
        classroom: course.classroom,
        teacher_id: selectedTeacherId.value,
        room_id: roomId,
        className: `${studentGrade.value}${studentClass.value}`
      };
      
      console.log('添加学生课程:', backendCourse);
      await courseApi.addStudentCourse(backendCourse);
      await loadStudentCourses();
      successMessage.value = '课程添加成功';
      return true;
    } catch (err) {
      error.value = '添加课程失败';
      console.error('Error adding student course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 更新学生课程
  const updateStudentCourse = async (course: StudentCourse) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      // 验证教师是否已选择
      if (!selectedTeacherId.value) {
        error.value = '请选择任课教师';
        return false;
      }
      
      // 验证教室是否已选择
      const roomId = (course as any).room_id;
      if (!roomId) {
        error.value = '请选择教室';
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
        name: course.name,
        day_of_week: dayOfWeek,
        period: course.timeSlot,
        classroom: course.classroom,
        teacher_id: selectedTeacherId.value,
        room_id: roomId,
        className: `${studentGrade.value}${studentClass.value}`
      };
      
      console.log('更新学生课程:', backendCourse);
      
      // 查找要更新的课程
      const existingCourse = studentCourses.value.find(
        c => c.day === course.day && c.timeSlot === course.timeSlot
      );
      
      if (existingCourse) {
        // 这里简化处理，实际应该根据ID更新
        // 由于我们没有课程ID，这里先删除旧课程，再添加新课程
        await deleteStudentCourse(course.day, course.timeSlot);
        await addStudentCourse(course);
      }
      
      await loadStudentCourses();
      successMessage.value = '课程更新成功';
      return true;
    } catch (err) {
      error.value = '更新课程失败';
      console.error('Error updating student course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 删除学生课程
  const deleteStudentCourse = async (day: string, timeSlot: number) => {
    try {
      isLoading.value = true;
      error.value = null;
      
      console.log('删除学生课程:', { day, timeSlot });
      
      // 获取所有学生课程，找到对应的课程ID
      const courses = await courseApi.getStudentCourses(studentClass.value, studentGrade.value);
      
      // 找到对应的课程
      const dayOfWeek = getDayOfWeek(day);
      const targetCourse = courses.find((course: any) => {
        const courseDay = course.day_of_week || getDayOfWeek(course.day);
        return courseDay === dayOfWeek && course.period === timeSlot;
      });
      
      if (targetCourse && targetCourse.id) {
        await courseApi.deleteStudentCourse(Number(targetCourse.id));
        await loadStudentCourses();
        successMessage.value = '课程删除成功';
        return true;
      } else {
        error.value = '未找到对应的课程';
        return false;
      }
    } catch (err) {
      error.value = '删除课程失败';
      console.error('Error deleting student course:', err);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  // 根据年级和班级更新课程表
  const updateStudentCoursesByGradeClass = async () => {
    await loadStudentCourses();
  };

  // 刷新学生课程表
  const refreshStudentSchedule = async () => {
    await loadStudentCourses();
  };

  // 获取指定天和时间段的课程
  const getStudentCourse = (day: string, timeSlot: number) => {
    return studentCourses.value.find(c => c.day === day && c.timeSlot === timeSlot);
  };

  // 模态框相关方法
  const openAddStudentCourseModal = (weekDays: string[]) => {
    editingStudentCourse.value = false;
    studentCourseForm.value = {
      day: weekDays[0] || '星期一',
      timeSlot: 1,
      name: '',
      teacher: '',
      classroom: ''
    };
    showStudentCourseModal.value = true;
  };

  const openEditStudentCourseModal = (day: string, timeSlot: number) => {
    const existingCourse = getStudentCourse(day, timeSlot);
    if (existingCourse) {
      studentCourseForm.value = { ...existingCourse };
      editingStudentCourse.value = true;
    } else {
      studentCourseForm.value = {
        day,
        timeSlot,
        name: '',
        teacher: '',
        classroom: ''
      };
      editingStudentCourse.value = false;
    }
    showStudentCourseModal.value = true;
  };

  const closeStudentCourseModal = () => {
    showStudentCourseModal.value = false;
    editingStudentCourse.value = false;
  };

  const saveStudentCourse = async () => {
    // 确保 selectedTeacherId 与表单中的教师选择同步
    selectedTeacherId.value = studentCourseForm.value.teacher;
    
    if (editingStudentCourse.value) {
      await updateStudentCourse(studentCourseForm.value);
    } else {
      await addStudentCourse(studentCourseForm.value);
    }
    closeStudentCourseModal();
  };

  // 初始化数据
  onMounted(async () => {
    // 同时加载教师数据和学生课程数据
    await loadTeachers();
    await loadStudentCourses();
  });

  return {
    // 状态
    studentGrade,
    studentClass,
    studentCourses,
    
    // 教师相关状态
    teachers,
    selectedTeacherId,
    selectedTeacher,
    
    // 操作状态
    isLoading,
    error,
    successMessage,
    
    // 模态框状态
    showStudentCourseModal,
    editingStudentCourse,
    studentCourseForm,
    
    // 方法
    getStudentCourse,
    refreshStudentSchedule,
    updateStudentCoursesByGradeClass,
    openAddStudentCourseModal,
    openEditStudentCourseModal,
    closeStudentCourseModal,
    saveStudentCourse,
    deleteStudentCourse,
    loadTeachers,
    handleTeacherSelect
  };
}
