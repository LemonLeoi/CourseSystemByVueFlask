import { ref, watch } from 'vue';

export function useLocalStorage<T>(key: string, initialValue: T) {
  // 从本地存储中获取初始值
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

  const storedValue = ref<T>(readValue());

  // 保存值到本地存储
  const saveValue = (value: T) => {
    if (typeof window === 'undefined') {
      console.warn(`Tried setting localStorage key "${key}" in SSR environment`);
      return;
    }

    try {
      // 允许值是一个函数，类似于React的setState
      const valueToStore =
        value instanceof Function ? value(storedValue.value) : value;
      
      storedValue.value = valueToStore;
      
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.warn(`Error setting localStorage key "${key}":`, error);
    }
  };

  // 监听值的变化并保存到本地存储
  watch(
    storedValue,
    (newValue) => {
      saveValue(newValue);
    },
    { deep: true }
  );

  // 移除本地存储中的值
  const removeValue = () => {
    if (typeof window === 'undefined') {
      console.warn(`Tried removing localStorage key "${key}" in SSR environment`);
      return;
    }

    try {
      storedValue.value = initialValue;
      window.localStorage.removeItem(key);
    } catch (error) {
      console.warn(`Error removing localStorage key "${key}":`, error);
    }
  };

  return {
    value: storedValue,
    setValue: saveValue,
    removeValue,
    resetValue: () => saveValue(initialValue)
  };
}
