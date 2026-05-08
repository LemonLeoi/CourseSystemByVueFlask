// 通知服务

// 通知类型
export interface Notification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}

// 通知状态管理
class NotificationService {
  private notifications: Notification[] = [];
  private listeners: ((notifications: Notification[]) => void)[] = [];

  // 添加通知
  addNotification(message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info', duration: number = 3000) {
    const id = Date.now().toString();
    const notification: Notification = {
      id,
      message,
      type,
      duration
    };

    this.notifications.push(notification);
    this.notifyListeners();

    // 自动移除通知
    if (duration > 0) {
      setTimeout(() => {
        this.removeNotification(id);
      }, duration);
    }

    return id;
  }

  // 移除通知
  removeNotification(id: string) {
    this.notifications = this.notifications.filter(notification => notification.id !== id);
    this.notifyListeners();
  }

  // 获取所有通知
  getNotifications() {
    return [...this.notifications];
  }

  // 添加监听器
  addListener(listener: (notifications: Notification[]) => void) {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  // 通知所有监听器
  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.getNotifications()));
  }

  // 快捷方法
  success(message: string, duration?: number) {
    return this.addNotification(message, 'success', duration);
  }

  error(message: string, duration?: number) {
    return this.addNotification(message, 'error', duration);
  }

  warning(message: string, duration?: number) {
    return this.addNotification(message, 'warning', duration);
  }

  info(message: string, duration?: number) {
    return this.addNotification(message, 'info', duration);
  }
}

// 导出单例
export default new NotificationService();