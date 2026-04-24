import { ref, watch } from 'vue';

export function useLocalStorage<T>(key: string, initialValue: T) {
  // 从localStorage读取初始值
  const readValue = (): T => {
    if (typeof window === 'undefined') {
      return initialValue;
    }

    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  };

  // 创建响应式ref
  const storedValue = ref<T>(readValue());

  // 监听值的变化，自动更新localStorage
  watch(
    storedValue,
    (value) => {
      if (typeof window === 'undefined') {
        console.warn(`Tried setting localStorage key "${key}" in SSR environment`);
        return;
      }

      try {
        window.localStorage.setItem(key, JSON.stringify(value));
      } catch (error) {
        console.warn(`Error setting localStorage key "${key}":`, error);
      }
    },
    { deep: true }
  );

  return storedValue;
}

// 用于管理多个折叠状态的组合函数
export function useCollapsibleStates() {
  const getCollapsedState = (key: string, defaultState: boolean = false): boolean => {
    if (typeof window === 'undefined') {
      return defaultState;
    }

    try {
      const item = window.localStorage.getItem(`collapsible_${key}`);
      return item ? item === 'true' : defaultState;
    } catch (error) {
      console.warn(`Error reading collapsible state for key "${key}":`, error);
      return defaultState;
    }
  };

  const setCollapsedState = (key: string, state: boolean): void => {
    if (typeof window === 'undefined') {
      return;
    }

    try {
      window.localStorage.setItem(`collapsible_${key}`, state.toString());
    } catch (error) {
      console.warn(`Error setting collapsible state for key "${key}":`, error);
    }
  };

  return {
    getCollapsedState,
    setCollapsedState
  };
}