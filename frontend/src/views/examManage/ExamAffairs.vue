<template>
  <Layout active-path="/exams">
    <BaseManagePage 
      title="考试管理"
      :show-search="true"
      :show-filter="true"
      :show-pagination="true"
      :show-add-button="true"
      :search-placeholder="'搜索考试名称或考试代码'"
      :search-button-text="'搜索'"
      :add-button-text="'添加考试'"
      :total-items="totalExams"
      :items-per-page="itemsPerPage"
      :current-page="currentPage"
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
                  <button class="btn btn-error btn-sm mr-2" @click="confirmDeleteExam(exam)">删除</button>
                  <button class="btn btn-secondary btn-sm mr-2" @click="viewExam(exam)">查看详情</button>
                  <button 
                    class="btn btn-warning btn-sm" 
                    @click="confirmArchiveExam(exam)"
                    v-if="exam.status !== '已归档'"
                  >
                    归档
                  </button>
                  <button 
                    class="btn btn-success btn-sm" 
                    @click="confirmUnarchiveExam(exam)"
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
          :show-footer="true"
          :show-cancel-button="true"
          :show-save-button="true"
          :cancel-button-text="'取消'"
          :save-button-text="'确定修改'"
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
              />
            </div>
            <div class="form-group">
              <label for="examName">考试名称</label>
              <input 
                type="text" 
                id="examName" 
                v-model="formData.name" 
                readonly
                required
              />
            </div>
            <div class="form-group">
              <label for="academicYear">学年</label>
              <select 
                id="academicYear" 
                v-model="formData.academicYear" 
                @change="handleFormChange"
                required
              >
                <option value="">请选择</option>
                <option value="2024-2025学年">2024-2025学年</option>
                <option value="2025-2026学年">2025-2026学年</option>
                <option value="2026-2027学年">2026-2027学年</option>
              </select>
            </div>
            <div class="form-group">
              <label for="semester">学期</label>
              <select 
                id="semester" 
                v-model="formData.semester" 
                @change="handleFormChange"
                required
              >
                <option value="">请选择</option>
                <option value="第一学期">第一学期</option>
                <option value="第二学期">第二学期</option>
              </select>
            </div>
            <div class="form-group">
              <label for="examGrade">年级</label>
              <select 
                id="examGrade" 
                v-model="formData.grade" 
                @change="handleFormChange"
                required
              >
                <option value="">请选择</option>
                <option value="高一">高一</option>
                <option value="高二">高二</option>
                <option value="高三">高三</option>
              </select>
            </div>
            <div class="form-group">
              <label for="examType">考试类型</label>
              <select 
                id="examType" 
                v-model="formData.type" 
                @change="handleFormChange"
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
              <label for="startDate">开始日期</label>
              <input 
                type="date" 
                id="startDate" 
                v-model="formData.startDate" 
                required
              />
            </div>
            <div class="form-group">
              <label for="endDate">结束日期</label>
              <input 
                type="date" 
                id="endDate" 
                v-model="formData.endDate" 
                required
              />
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
          :show-footer="true"
          :show-cancel-button="true"
          :cancel-button-text="'取消'"
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

    <!-- 删除确认对话框 -->
    <ConfirmDialog
      :visible="showDeleteConfirm"
      title="删除考试"
      :message="`确定要删除考试「${deleteExamItem?.name}」吗？`"
      :details="deleteExamItem ? {
        '考试代码': deleteExamItem.code,
        '考试名称': deleteExamItem.name,
        '考试类型': deleteExamItem.type,
        '年级': deleteExamItem.grade
      } : undefined"
      type="error"
      confirm-text="确认删除"
      cancel-text="取消"
      @confirm="performDeleteExam"
      @cancel="cancelDeleteExam"
    />

    <!-- 归档确认对话框 -->
    <ConfirmDialog
      :visible="showArchiveConfirm"
      title="归档考试"
      :message="`确定要归档考试「${archiveExamItem?.name}」吗？归档后将无法修改考试信息。`"
      :details="archiveExamItem ? {
        '考试代码': archiveExamItem.code,
        '考试名称': archiveExamItem.name,
        '当前状态': archiveExamItem.status
      } : undefined"
      type="warning"
      confirm-text="确认归档"
      cancel-text="取消"
      @confirm="performArchiveExam"
      @cancel="cancelArchiveExam"
    />

    <!-- 取消归档确认对话框 -->
    <ConfirmDialog
      :visible="showUnarchiveConfirm"
      title="取消归档考试"
      :message="`确定要取消归档考试「${unarchiveExamItem?.name}」吗？`"
      :details="unarchiveExamItem ? {
        '考试代码': unarchiveExamItem.code,
        '考试名称': unarchiveExamItem.name,
        '当前状态': unarchiveExamItem.status
      } : undefined"
      type="info"
      confirm-text="确认取消归档"
      cancel-text="取消"
      @confirm="performUnarchiveExam"
      @cancel="cancelUnarchiveExam"
    />
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Layout from '@/components/layout/Layout.vue';
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import BaseModal from '@/components/business/BaseModal.vue';
import ConfirmDialog from '@/components/common/ConfirmDialog.vue';
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
  academicYear: '',
  semester: '',
  grade: '',
  type: '',
  startDate: '',
  endDate: '',
  status: '准备中'
});

// 生成考试名称
const generateExamName = () => {
  const { academicYear, semester, grade, type } = formData.value;
  if (academicYear && semester && grade && type) {
    formData.value.name = `${academicYear}${grade}${semester}${type}`;
  }
};

// 生成考试代码
const generateExamCode = () => {
  const { academicYear, semester, grade, type } = formData.value;
  if (academicYear && semester && grade && type) {
    const year = academicYear.substring(0, 4);
    const semesterNum = semester === '第一学期' ? '1' : '2';
    const gradeNum = grade === '高一' ? '1' : grade === '高二' ? '2' : '3';
    
    let typeCode = '';
    switch (type) {
      case '期中考试':
        typeCode = 'MID';
        break;
      case '期末考试':
        typeCode = 'FIN';
        break;
      case '模拟考试':
        typeCode = 'SIM';
        break;
      case '月考':
        typeCode = 'MON';
        break;
      default:
        typeCode = 'OTH';
    }
    
    const sequence = String(Date.now()).slice(-4);
    formData.value.code = `${year}${semesterNum}${gradeNum}${typeCode}${sequence}`;
  }
};

// 处理表单变化
const handleFormChange = () => {
  generateExamName();
  generateExamCode();
};

// 详情模态框
const showDetailModal = ref(false);
const selectedExam = ref<Exam | null>(null);

// 删除确认对话框状态
const showDeleteConfirm = ref(false);
const deleteExamItem = ref<Exam | null>(null);

// 归档确认对话框状态
const showArchiveConfirm = ref(false);
const archiveExamItem = ref<Exam | null>(null);

// 取消归档确认对话框状态
const showUnarchiveConfirm = ref(false);
const unarchiveExamItem = ref<Exam | null>(null);

const openAddModal = () => {
  editingExam.value = null;
  formData.value = {
    code: '',
    name: '',
    academicYear: '',
    semester: '',
    grade: '',
    type: '',
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
    await updateExam(formData.value);
  } else {
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

// 删除考试相关
const confirmDeleteExam = (exam: Exam) => {
  deleteExamItem.value = exam;
  showDeleteConfirm.value = true;
};

const cancelDeleteExam = () => {
  showDeleteConfirm.value = false;
  deleteExamItem.value = null;
};

const performDeleteExam = async () => {
  if (deleteExamItem.value) {
    await deleteExam(deleteExamItem.value.code);
    showDeleteConfirm.value = false;
    deleteExamItem.value = null;
  }
};

// 归档考试相关
const confirmArchiveExam = (exam: Exam) => {
  archiveExamItem.value = exam;
  showArchiveConfirm.value = true;
};

const cancelArchiveExam = () => {
  showArchiveConfirm.value = false;
  archiveExamItem.value = null;
};

const performArchiveExam = async () => {
  if (archiveExamItem.value) {
    const updatedExam = { ...archiveExamItem.value, status: '已归档' };
    await updateExam(updatedExam);
    showArchiveConfirm.value = false;
    archiveExamItem.value = null;
  }
};

// 取消归档考试相关
const confirmUnarchiveExam = (exam: Exam) => {
  unarchiveExamItem.value = exam;
  showUnarchiveConfirm.value = true;
};

const cancelUnarchiveExam = () => {
  showUnarchiveConfirm.value = false;
  unarchiveExamItem.value = null;
};

const performUnarchiveExam = async () => {
  if (unarchiveExamItem.value) {
    const updatedExam = { ...unarchiveExamItem.value, status: '已发布' };
    await updateExam(updatedExam);
    showUnarchiveConfirm.value = false;
    unarchiveExamItem.value = null;
  }
};

// 初始化数据
onMounted(() => {
  // 数据初始化已在useExamManage中处理
});
</script>