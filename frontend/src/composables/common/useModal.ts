import { ref, watch } from 'vue';

export function useModal(initialState: boolean = false) {
  const isOpen = ref(initialState);

  const openModal = () => {
    isOpen.value = true;
  };

  const closeModal = () => {
    isOpen.value = false;
  };

  const toggleModal = () => {
    isOpen.value = !isOpen.value;
  };

  // 监听外部状态变化
  watch(
    () => initialState,
    (newState) => {
      isOpen.value = newState;
    }
  );

  return {
    isOpen,
    openModal,
    closeModal,
    toggleModal
  };
}
