// 课程数据服务

class CourseService {
  private timeSlots = [
    { id: 1, name: '第一节 (8:00-8:45)' },
    { id: 2, name: '第二节 (8:55-9:40)' },
    { id: 3, name: '第三节 (10:00-10:45)' },
    { id: 4, name: '第四节 (10:55-11:40)' },
    { id: 5, name: '第五节 (14:00-14:45)' },
    { id: 6, name: '第六节 (14:55-15:40)' },
    { id: 7, name: '第七节 (16:00-16:45)' },
    { id: 8, name: '第八节 (16:55-17:40)' }
  ];

  private weekDays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];

  // 获取时间段
  getTimeSlots() {
    return this.timeSlots;
  }

  // 获取星期数据
  getWeekDays() {
    return this.weekDays;
  }

  // 辅助方法：将星期格式从"周一"转换为"星期一"
  convertDayFormat(day: string): string {
    const dayMap: { [key: string]: string } = {
      '周一': '星期一',
      '周二': '星期二',
      '周三': '星期三',
      '周四': '星期四',
      '周五': '星期五',
      '周六': '星期六',
      '周日': '星期日'
    };
    return dayMap[day] || day;
  }

  // 辅助方法：将星期字符串转换为数字
  getDayOfWeek(day: string): number {
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
  }
}

// 导出单例实例
export const courseService = new CourseService();
