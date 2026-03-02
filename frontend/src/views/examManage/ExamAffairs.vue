<template>
  <Layout activePath="/exams">
    <BaseManagePage 
      title="考试管理"
      :showSearch="true"
      :showFilter="true"
      :showPagination="true"
      :showAddButton="true"
      :searchPlaceholder="'搜索考试名称或考试代码'"
      :searchButtonText="'搜索'"
      :addButtonText="'添加考试'"
      :totalItems="totalExams"
      :itemsPerPage="itemsPerPage"
      :currentPage="currentPage"
      @search="handleSearch"
      @pageChange="handlePageChange"
      @add="openAddModal"
    >
      <!-- 筛选区域 -->
      <template #filter>
        <select 
          v-model="examTypeFilter" 
          class="filter-select"
          @change="handleExamTypeFilterChange(examTypeFilter)"
        >
          <option value="">全类型</option>
          <option value="期中考试">期中考试</option>
          <option value="期末考试">期末考试</option>
          <option value="模拟考试">模拟考试</option>
          <option value="月考">月考</option>
        </select>
        <select 
          v-model="gradeFilter" 
          class="filter-select"
          @change="handleGradeFilterChange(gradeFilter)"
        >
          <option value="">全年级</option>
          <option value="高一">高一</option>
          <option value="高二">高二</option>
          <option value="高三">高三</option>
        </select>
      </template>
      
      <!-- 考试列表 -->
      <template #data>
        <div class="exam-table-container">
          <table class="exam-table">
            <thead>
              <tr>
                <th>考试代码</th>
                <th>考试名称</th>
                <th>考试类型</th>
                <th>年级</th>
                <th>开始日期</th>
                <th>结束日期</th>
                <th>发布状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="exam in paginatedExams" :key="exam.code">
                <td>{{ exam.code }}</td>
                <td>{{ exam.name }}</td>
                <td>{{ exam.type }}</td>
                <td>{{ exam.grade }}</td>
                <td>{{ exam.startDate }}</td>
                <td>{{ exam.endDate }}</td>
                <td>
                  <span :class="['status-badge', exam.status]">
                    {{ exam.status }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-primary btn-sm mr-2" @click="editExam(exam)">编辑</button>
                  <button class="btn btn-error btn-sm mr-2" @click="deleteExam(exam.code)">删除</button>
                  <button class="btn btn-secondary btn-sm mr-2" @click="viewExam(exam)">查看详情</button>
                  <button 
                    class="btn btn-warning btn-sm" 
                    @click="archiveExam(exam)"
                    v-if="exam.status !== '已归档'"
                  >
                    归档
                  </button>
                  <button 
                    class="btn btn-success btn-sm" 
                    @click="unarchiveExam(exam)"
                    v-else
                  >
                    取消归档
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
      
      <!-- 模态框 -->
      <template #modal>
        <!-- 添加/编辑考试模态框 -->
        <BaseModal 
          :visible="showModal"
          :title="editingExam ? '编辑考试' : '添加考试'"
          :showFooter="true"
          :showCancelButton="true"
          :showSaveButton="true"
          :cancelButtonText="'取消'"
          :saveButtonText="'确定修改'"
          @close="closeModal"
          @save="saveExam"
        >
          <form @submit.prevent="saveExam">
            <div class="form-group">
              <label for="examCode">考试代码</label>
              <input 
                type="text" 
                id="examCode" 
                v-model="formData.code" 
                :disabled="!!editingExam"
                required
              >
            </div>
            <div class="form-group">
              <label for="examName">考试名称</label>
              <input 
                type="text" 
                id="examName" 
                v-model="formData.name" 
                required
              >
            </div>
            <div class="form-group">
              <label for="examType">考试类型</label>
              <select 
                id="examType" 
                v-model="formData.type" 
                required
              >
                <option value="">请选择</option>
                <option value="期中考试">期中考试</option>
                <option value="期末考试">期末考试</option>
                <option value="模拟考试">模拟考试</option>
                <option value="月考">月考</option>
              </select>
            </div>
            <div class="form-group">
              <label for="examGrade">年级</label>
              <select 
                id="examGrade" 
                v-model="formData.grade" 
                required
              >
                <option value="">请选择</option>
                <option value="高一">高一</option>
                <option value="高二">高二</option>
                <option value="高三">高三</option>
              </select>
            </div>
            <div class="form-group">
              <label for="startDate">开始日期</label>
              <input 
                type="date" 
                id="startDate" 
                v-model="formData.startDate" 
                required
              >
            </div>
            <div class="form-group">
              <label for="endDate">结束日期</label>
              <input 
                type="date" 
                id="endDate" 
                v-model="formData.endDate" 
                required
              >
            </div>
            <div class="form-group">
              <label for="examStatus">发布状态</label>
              <select 
                id="examStatus" 
                v-model="formData.status" 
                required
              >
                <option value="准备中">准备中</option>
                <option value="已发布">已发布</option>
                <option value="已归档">已归档</option>
              </select>
            </div>
          </form>
        </BaseModal>
        
        <!-- 查看考试详情模态框 -->
        <BaseModal 
          :visible="showDetailModal"
          title="考试详情"
          :showFooter="true"
          :showCancelButton="true"
          :cancelButtonText="'取消'"
          @close="closeDetailModal"
        >
          <div class="detail-item">
            <span class="detail-label">考试代码：</span>
            <span class="detail-value">{{ selectedExam?.code }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">考试名称：</span>
            <span class="detail-value">{{ selectedExam?.name }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">考试类型：</span>
            <span class="detail-value">{{ selectedExam?.type }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">年级：</span>
            <span class="detail-value">{{ selectedExam?.grade }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">开始日期：</span>
            <span class="detail-value">{{ selectedExam?.startDate }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">结束日期：</span>
            <span class="detail-value">{{ selectedExam?.endDate }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">发布状态：</span>
            <span class="detail-value">{{ selectedExam?.status }}</span>
          </div>
        </BaseModal>
      </template>
    </BaseManagePage>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Layout from '@/components/layout/Layout.vue';
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import BaseModal from '@/components/business/BaseModal.vue';
import { useExamManage } from '@/composables/exam/useExamManage';
import type { Exam } from '@/types';

// 使用考试管理composable
const {
  loading,
  error,
  searchQuery,
  currentPage,
  itemsPerPage,
  allExams,
  filteredExams,
  paginatedExams,
  totalExams,
  examTypeFilter,
  gradeFilter,
  addExam,
  updateExam,
  deleteExam,
  getExamByCode,
  handleSearch,
  handleExamTypeFilterChange,
  handleGradeFilterChange,
  handlePageChange
} = useExamManage();

// 模态框相关
const showModal = ref(false);
const editingExam = ref<Exam | null>(null);
const formData = ref<Exam>({
  code: '',
  name: '',
  type: '',
  grade: '',
  startDate: '',
  endDate: '',
  status: '准备中'
});

// 详情模态框
const showDetailModal = ref(false);
const selectedExam = ref<Exam | null>(null);

const openAddModal = () => {
  editingExam.value = null;
  formData.value = {
    code: '',
    name: '',
    type: '',
    grade: '',
    startDate: '',
    endDate: '',
    status: '准备中'
  };
  showModal.value = true;
};

const editExam = (exam: Exam) => {
  editingExam.value = exam;
  formData.value = { ...exam };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingExam.value = null;
};

const saveExam = async () => {
  if (editingExam.value) {
    // 编辑现有考试
    await updateExam(formData.value);
  } else {
    // 添加新考试
    await addExam(formData.value);
  }
  closeModal();
  currentPage.value = 1;
};

const viewExam = (exam: Exam) => {
  selectedExam.value = exam;
  showDetailModal.value = true;
};

const closeDetailModal = () => {
  showDetailModal.value = false;
  selectedExam.value = null;
};

// 归档考试
const archiveExam = async (exam: Exam) => {
  if (confirm('确定要归档这场考试吗？')) {
    const updatedExam = { ...exam, status: '已归档' };
    await updateExam(updatedExam);
  }
};

// 取消归档考试
const unarchiveExam = async (exam: Exam) => {
  if (confirm('确定要取消归档这场考试吗？')) {
    const updatedExam = { ...exam, status: '已发布' };
    await updateExam(updatedExam);
  }
};

// 初始化数据
onMounted(() => {
  // 数据初始化已在useExamManage中处理
});
</script>