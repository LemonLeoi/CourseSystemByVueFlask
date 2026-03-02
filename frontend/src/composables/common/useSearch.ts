import { ref } from 'vue';

interface SearchOptions {
  debounceDelay?: number;
  initialKeywords?: string;
  initialFilters?: Record<string, any>;
}

export function useSearch<T>(
  searchFunction: (keywords: string, filters: Record<string, any>) => Promise<T[]>,
  options: SearchOptions = {}
) {
  const keywords = ref(options.initialKeywords || '');
  const filters = ref<Record<string, any>>(options.initialFilters || {});
  const results = ref<T[]>([]);
  const loading = ref(false);
  const error = ref<any>(null);

  let debounceTimer: number | null = null;

  const performSearch = async () => {
    loading.value = true;
    error.value = null;
    try {
      results.value = await searchFunction(keywords.value, filters.value);
    } catch (err) {
      error.value = err;
      results.value = [];
    } finally {
      loading.value = false;
    }
  };

  const handleSearch = (query: string) => {
    keywords.value = query;
    
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    debounceTimer = window.setTimeout(() => {
      performSearch();
    }, options.debounceDelay || 300);
  };

  const resetFilters = () => {
    filters.value = options.initialFilters || {};
    performSearch();
  };

  const updateFilters = (newFilters: Record<string, any>) => {
    filters.value = { ...filters.value, ...newFilters };
    performSearch();
  };

  const resetSearch = () => {
    keywords.value = options.initialKeywords || '';
    filters.value = options.initialFilters || {};
    performSearch();
  };

  // 清理函数
  const cleanup = () => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
  };

  return {
    keywords,
    filters,
    results,
    loading,
    error,
    handleSearch,
    resetFilters,
    updateFilters,
    resetSearch,
    cleanup
  };
}
