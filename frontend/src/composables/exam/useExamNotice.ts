import { ref, computed } from 'vue';
import type { Notice } from '@/types';

export function useExamNotice() {
  const searchQuery = ref('');
  const currentPage = ref(1);
  const itemsPerPage = ref(5);

  // 通知数据
  const notices = ref<Notice[]>([
    {
      id: 1,
      title: '关于2025年春季期中考试的通知',
      content: '2025年春季期中考试将于5月1日至5月3日举行，请各位教师做好考前准备工作，学生做好复习备考。具体考试安排将另行通知。',
      date: '2025-04-15',
      author: '教务处'
    },
    {
      id: 2,
      title: '关于2025年春季期末考试的通知',
      content: '2025年春季期末考试将于6月20日至6月23日举行，请各位教师做好考前准备工作，学生做好复习备考。具体考试安排将另行通知。',
      date: '2025-05-20',
      author: '教务处'
    },
    {
      id: 3,
      title: '关于2025年高考模拟考试的通知',
      content: '2025年高考模拟考试将于2月20日至2月22日举行，高三年级全体学生必须参加。请各位教师做好考前准备工作，学生做好复习备考。具体考试安排将另行通知。',
      date: '2025-02-10',
      author: '教务处'
    },
    {
      id: 4,
      title: '关于2025年春季第一次月考的通知',
      content: '2025年春季第一次月考将于3月15日至3月16日举行，请各位教师做好考前准备工作，学生做好复习备考。具体考试安排将另行通知。',
      date: '2025-03-01',
      author: '教务处'
    },
    {
      id: 5,
      title: '关于2025年春季第二次月考的通知',
      content: '2025年春季第二次月考将于4月15日至4月16日举行，请各位教师做好考前准备工作，学生做好复习备考。具体考试安排将另行通知。',
      date: '2025-04-01',
      author: '教务处'
    },
    {
      id: 6,
      title: '关于调整2025年春季期中考试时间的通知',
      content: '因特殊原因，2025年春季期中考试时间调整为5月5日至5月7日，特此通知。',
      date: '2025-04-20',
      author: '教务处'
    },
    {
      id: 7,
      title: '关于2025年春季期中考试考场安排的通知',
      content: '2025年春季期中考试考场安排已发布，请各位教师和学生查看。',
      date: '2025-04-25',
      author: '教务处'
    },
    {
      id: 8,
      title: '关于2025年春季期中考试监考安排的通知',
      content: '2025年春季期中考试监考安排已发布，请各位教师查看并按时参加监考。',
      date: '2025-04-26',
      author: '教务处'
    },
    {
      id: 9,
      title: '关于2025年春季期中考试阅卷安排的通知',
      content: '2025年春季期中考试阅卷安排已发布，请各位教师查看并按时参加阅卷。',
      date: '2025-04-27',
      author: '教务处'
    },
    {
      id: 10,
      title: '关于2025年春季期中考试成绩发布的通知',
      content: '2025年春季期中考试成绩将于5月10日发布，请各位教师和学生关注。',
      date: '2025-04-28',
      author: '教务处'
    }
  ]);

  // 筛选通知
  const filteredNotices = computed(() => {
    if (!searchQuery.value) {
      return notices.value;
    }
    const query = searchQuery.value.toLowerCase();
    return notices.value.filter(notice => 
      notice.title.toLowerCase().includes(query) || 
      notice.content.toLowerCase().includes(query)
    );
  });

  // 分页后的通知
  const paginatedNotices = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage.value;
    const endIndex = startIndex + itemsPerPage.value;
    return filteredNotices.value.slice(startIndex, endIndex);
  });

  // 总通知数
  const totalNotices = computed(() => filteredNotices.value.length);

  // 处理搜索
  const handleSearch = (query: string) => {
    searchQuery.value = query;
    currentPage.value = 1;
  };

  // 处理分页
  const handlePageChange = (page: number) => {
    currentPage.value = page;
  };

  // 打开添加通知模态框
  const openAddModal = () => {
    // 这里可以实现打开添加通知模态框的逻辑
    console.log('打开添加通知模态框');
  };

  // 添加通知
  const addNotice = (notice: Omit<Notice, 'id'>) => {
    const newNotice: Notice = {
      ...notice,
      id: notices.value.length + 1
    };
    notices.value.unshift(newNotice);
  };

  return {
    // 状态
    searchQuery,
    currentPage,
    itemsPerPage,
    
    // 数据
    notices,
    filteredNotices,
    paginatedNotices,
    totalNotices,
    
    // 方法
    handleSearch,
    handlePageChange,
    openAddModal,
    addNotice
  };
}
