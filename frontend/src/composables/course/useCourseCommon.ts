import { ref } from 'vue';
import { courseService } from '@/services/data/courseService';
import type { CourseTabType } from '@/types/course';

export function useCourseCommon() {
  // 标签页状态
  const activeTab = ref<CourseTabType>('student');

  // 时间段数据
  const timeSlots = ref(courseService.getTimeSlots());

  // 星期数据
  const weekDays = ref(courseService.getWeekDays());

  // 方法
  const getAddButtonText = (): string => {
    switch (activeTab.value) {
      case 'student':
        return '添加课程';
      case 'teacher':
        return '添加课程';
      case 'progress':
        return '添加章节';
      default:
        return '添加';
    }
  };

  const handleAddClick = (): string => {
    return activeTab.value;
  };

  // 获取时间段名称
  const getSlotName = (slotId: number): string => {
    const slot = timeSlots.value.find(s => s.id === slotId);
    return slot ? slot.name : '';
  };

  return {
    // 状态
    activeTab,
    timeSlots,
    weekDays,
    
    // 方法
    getAddButtonText,
    handleAddClick,
    getSlotName
  };
}
