// 通知数据服务

interface Notification {
  date: string;
  content: string;
}

class NotificationService {
  private notifications: Notification[] = [
    { date: "2025-05-01", content: "测验：历史科目安排" },
    { date: "2025-04-30", content: "测试：地理科目安排" },
    { date: "2025-04-29", content: "考试：历史科目安排" },
    { date: "2025-04-28", content: "测验：语文科目安排" },
    { date: "2025-04-27", content: "测验：历史科目安排" },
    { date: "2025-04-26", content: "考试：语文科目安排" },
    { date: "2025-04-25", content: "测试：生物科目安排" },
    { date: "2025-04-24", content: "测试：历史科目安排" },
    { date: "2025-04-23", content: "考试：地理科目安排" },
    { date: "2025-04-22", content: "考试：历史科目安排" }
  ];

  // 获取所有通知
  getAllNotifications(): Notification[] {
    return this.notifications;
  }

  // 根据日期获取通知
  getNotificationsByDate(date: string): Notification[] {
    return this.notifications.filter(notification => notification.date === date);
  }

  // 添加通知
  addNotification(notification: Omit<Notification, 'date'>): Notification {
    const newNotification: Notification = {
      ...notification,
      date: (new Date().toISOString().split('T')[0]) as string
    };
    this.notifications.unshift(newNotification);
    return newNotification;
  }

  // 删除通知
  deleteNotification(index: number): void {
    if (index >= 0 && index < this.notifications.length) {
      this.notifications.splice(index, 1);
    }
  }
}

// 导出单例实例
export const notificationService = new NotificationService();
