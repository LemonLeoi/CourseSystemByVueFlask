import { ref } from 'vue';

// 课程类型定义
export interface Course {
  id?: string;
  day: string;
  timeSlot: number;
  name: string;
  teacher?: string;
  className?: string;
  classroom: string;
}

// 时间段类型定义
export interface TimeSlot {
  id: number;
  name: string;
}

// 课程表配置选项
interface CourseTableOptions {
  weekDays: string[];
  timeSlots: TimeSlot[];
  mode: 'student' | 'teacher';
}

/**
 * 课程表逻辑组合式函数
 * @param initialCourses 初始课程数据
 * @param options 课程表配置选项
 * @returns 课程表相关的方法和状态
 */
export function useCourseTable(
  initialCourses: Course[] = [],
  options: CourseTableOptions
) {
  // 课程数据
  const courses = ref<Course[]>([...initialCourses]);
  
  // 加载状态
  const isLoading = ref(false);

  /**
   * 获取指定天和时间段的课程
   * @param day 星期
   * @param timeSlotId 时间段ID
   * @returns 课程对象或undefined
   */
  const getCourse = (day: string, timeSlotId: number): Course | undefined => {
    return courses.value.find(course => {
      return course.day === day && course.timeSlot === timeSlotId;
    });
  };

  /**
   * 添加课程
   * @param course 课程对象
   * @returns 是否添加成功
   */
  const addCourse = (course: Course): boolean => {
    // 检查是否已存在相同时间段的课程
    const existingCourse = getCourse(course.day, course.timeSlot);
    if (existingCourse) {
      console.error('该时间段已存在课程');
      return false;
    }

    // 生成课程ID
    if (!course.id) {
      course.id = generateCourseId(course);
    }

    courses.value.push(course);
    return true;
  };

  /**
   * 更新课程
   * @param course 课程对象
   * @returns 是否更新成功
   */
  const updateCourse = (course: Course): boolean => {
    if (!course.id) {
      console.error('课程ID不能为空');
      return false;
    }

    const index = courses.value.findIndex(c => c.id === course.id);
    if (index === -1) {
      console.error('未找到要更新的课程');
      return false;
    }

    courses.value[index] = course;
    return true;
  };

  /**
   * 删除课程
   * @param day 星期
   * @param timeSlotId 时间段ID
   * @returns 是否删除成功
   */
  const deleteCourse = (day: string, timeSlotId: number): boolean => {
    const index = courses.value.findIndex(course => {
      return course.day === day && course.timeSlot === timeSlotId;
    });

    if (index === -1) {
      console.error('未找到要删除的课程');
      return false;
    }

    courses.value.splice(index, 1);
    return true;
  };

  /**
   * 检查课程冲突
   * @param course 课程对象
   * @param excludeId 排除的课程ID（用于更新操作）
   * @returns 是否存在冲突
   */
  const checkCourseConflict = (course: Course, excludeId?: string): boolean => {
    return courses.value.some(existingCourse => {
      // 排除当前课程（用于更新操作）
      if (excludeId && existingCourse.id === excludeId) {
        return false;
      }
      // 检查是否在同一时间段
      return existingCourse.day === course.day && existingCourse.timeSlot === course.timeSlot;
    });
  };

  /**
   * 生成课程ID
   * @param course 课程对象
   * @returns 课程ID
   */
  const generateCourseId = (course: Course): string => {
    return `${course.day}_${course.timeSlot}_${Date.now()}`;
  };

  /**
   * 按天分组课程
   * @returns 按天分组的课程对象
   */
  const getCoursesByDay = (): Record<string, Course[]> => {
    const coursesByDay: Record<string, Course[]> = {};

    options.weekDays.forEach(day => {
      coursesByDay[day] = [];
    });

    courses.value.forEach(course => {
      if (coursesByDay[course.day]) {
        coursesByDay[course.day].push(course);
      }
    });

    return coursesByDay;
  };

  /**
   * 统计课程信息
   * @returns 课程统计信息
   */
  const getCourseStatistics = () => {
    const totalCourses = courses.value.length;
    const coursesByDay = getCoursesByDay();
    
    // 计算每天的课程数量
    const coursesPerDay = Object.entries(coursesByDay).map(([day, dayCourses]) => ({
      day,
      count: dayCourses.length
    }));

    // 找出最忙的天
    const busiestDay = coursesPerDay.reduce((max, current) => {
      return current.count > max.count ? current : max;
    }, coursesPerDay[0] || { day: '', count: 0 });

    // 计算平均每天的课程数量
    const avgCoursesPerDay = totalCourses / options.weekDays.length;

    return {
      totalCourses,
      coursesPerDay,
      busiestDay,
      avgCoursesPerDay: Math.round(avgCoursesPerDay * 10) / 10
    };
  };

  /**
   * 清空课程表
   */
  const clearCourses = () => {
    courses.value = [];
  };

  /**
   * 导入课程数据
   * @param newCourses 新的课程数据
   */
  const importCourses = (newCourses: Course[]) => {
    courses.value = [...newCourses];
  };

  /**
   * 导出课程数据
   * @returns 课程数据数组
   */
  const exportCourses = (): Course[] => {
    return [...courses.value];
  };

  return {
    // 状态
    courses,
    isLoading,
    
    // 方法
    getCourse,
    addCourse,
    updateCourse,
    deleteCourse,
    checkCourseConflict,
    getCoursesByDay,
    getCourseStatistics,
    clearCourses,
    importCourses,
    exportCourses
  };
}

/**
 * 获取默认的时间段
 * @returns 时间段数组
 */
export function getDefaultTimeSlots(): TimeSlot[] {
  return [
    { id: 1, name: '第1节 (08:00-08:45)' },
    { id: 2, name: '第2节 (08:55-09:40)' },
    { id: 3, name: '第3节 (10:00-10:45)' },
    { id: 4, name: '第4节 (10:55-11:40)' },
    { id: 5, name: '第5节 (14:00-14:45)' },
    { id: 6, name: '第6节 (14:55-15:40)' },
    { id: 7, name: '第7节 (16:00-16:45)' },
    { id: 8, name: '第8节 (16:55-17:40)' }
  ];
}

/**
 * 获取默认的星期
 * @returns 星期数组
 */
export function getDefaultWeekDays(): string[] {
  return ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
}
