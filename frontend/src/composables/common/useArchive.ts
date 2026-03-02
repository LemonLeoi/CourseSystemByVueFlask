import { ref } from 'vue';

// 归档操作的配置选项
interface ArchiveOptions<T> {
  // 归档状态值
  archiveStatus: string;
  // 取消归档状态值
  unarchiveStatus: string;
  // 状态字段名
  statusField: keyof T;
  // 状态文本字段名（可选）
  statusTextField?: keyof T;
  // 状态文本映射
  statusTextMap?: Record<string, string>;
}

/**
 * 归档逻辑组合式函数
 * @param items 数据数组
 * @param options 归档配置选项
 * @returns 归档相关的方法
 */
export function useArchive<T>(
  items: Ref<T[]>,
  options: ArchiveOptions<T>
) {
  // 归档加载状态
  const isArchiving = ref(false);

  /**
   * 归档指定项
   * @param item 要归档的项
   * @param confirmMessage 确认消息
   * @returns 是否归档成功
   */
  const archiveItem = async (
    item: T,
    confirmMessage: string = '确定要归档该项吗？'
  ): Promise<boolean> => {
    if (!confirm(confirmMessage)) {
      return false;
    }

    isArchiving.value = true;

    try {
      const index = items.value.findIndex(i => i === item);
      if (index === -1) {
        throw new Error('未找到要归档的项');
      }

      // 更新状态字段
      items.value[index][options.statusField] = options.archiveStatus as any;

      // 如果有状态文本字段，也更新它
      if (options.statusTextField && options.statusTextMap) {
        items.value[index][options.statusTextField] = options.statusTextMap[options.archiveStatus] as any;
      }

      return true;
    } catch (error) {
      console.error('归档失败:', error);
      return false;
    } finally {
      isArchiving.value = false;
    }
  };

  /**
   * 取消归档指定项
   * @param item 要取消归档的项
   * @param confirmMessage 确认消息
   * @returns 是否取消归档成功
   */
  const unarchiveItem = async (
    item: T,
    confirmMessage: string = '确定要取消归档该项吗？'
  ): Promise<boolean> => {
    if (!confirm(confirmMessage)) {
      return false;
    }

    isArchiving.value = true;

    try {
      const index = items.value.findIndex(i => i === item);
      if (index === -1) {
        throw new Error('未找到要取消归档的项');
      }

      // 更新状态字段
      items.value[index][options.statusField] = options.unarchiveStatus as any;

      // 如果有状态文本字段，也更新它
      if (options.statusTextField && options.statusTextMap) {
        items.value[index][options.statusTextField] = options.statusTextMap[options.unarchiveStatus] as any;
      }

      return true;
    } catch (error) {
      console.error('取消归档失败:', error);
      return false;
    } finally {
      isArchiving.value = false;
    }
  };

  /**
   * 批量归档项
   * @param selectedItems 要归档的项数组
   * @param confirmMessage 确认消息
   * @returns 归档成功的项数
   */
  const batchArchiveItems = async (
    selectedItems: T[],
    confirmMessage: string = `确定要归档选中的 ${selectedItems.length} 项吗？`
  ): Promise<number> => {
    if (!selectedItems.length) {
      return 0;
    }

    if (!confirm(confirmMessage)) {
      return 0;
    }

    isArchiving.value = true;
    let successCount = 0;

    try {
      for (const item of selectedItems) {
        const index = items.value.findIndex(i => i === item);
        if (index !== -1) {
          // 更新状态字段
          items.value[index][options.statusField] = options.archiveStatus as any;

          // 如果有状态文本字段，也更新它
          if (options.statusTextField && options.statusTextMap) {
            items.value[index][options.statusTextField] = options.statusTextMap[options.archiveStatus] as any;
          }

          successCount++;
        }
      }

      return successCount;
    } catch (error) {
      console.error('批量归档失败:', error);
      return successCount;
    } finally {
      isArchiving.value = false;
    }
  };

  /**
   * 筛选归档项
   * @returns 归档的项数组
   */
  const getArchivedItems = (): T[] => {
    return items.value.filter(item => {
      return item[options.statusField] === options.archiveStatus;
    });
  };

  /**
   * 筛选未归档项
   * @returns 未归档的项数组
   */
  const getUnarchivedItems = (): T[] => {
    return items.value.filter(item => {
      return item[options.statusField] !== options.archiveStatus;
    });
  };

  return {
    isArchiving,
    archiveItem,
    unarchiveItem,
    batchArchiveItems,
    getArchivedItems,
    getUnarchivedItems
  };
}

// 类型定义
type Ref<T> = {
  value: T;
};
