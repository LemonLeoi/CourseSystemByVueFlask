import { ref, computed } from 'vue';
import type { Ref } from 'vue';

export function usePagination(
  totalItems: Ref<number>,
  initialPageSize: number = 10,
  initialPage: number = 1
) {
  const currentPage = ref(initialPage);
  const pageSize = ref(initialPageSize);

  const totalPages = computed(() => {
    return Math.ceil(totalItems.value / pageSize.value);
  });

  const startIndex = computed(() => {
    return (currentPage.value - 1) * pageSize.value;
  });

  const endIndex = computed(() => {
    return Math.min(startIndex.value + pageSize.value, totalItems.value);
  });

  const setPage = (page: number) => {
    currentPage.value = Math.max(1, Math.min(page, totalPages.value));
  };

  const setPageSize = (size: number) => {
    pageSize.value = size;
    currentPage.value = 1;
  };

  const previousPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
    }
  };

  const reset = () => {
    currentPage.value = 1;
    pageSize.value = initialPageSize;
  };

  return {
    currentPage,
    pageSize,
    totalPages,
    startIndex,
    endIndex,
    setPage,
    setPageSize,
    previousPage,
    nextPage,
    reset
  };
}
