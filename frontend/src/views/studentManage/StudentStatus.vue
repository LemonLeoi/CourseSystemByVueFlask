<template>
  <Layout activePath="/student-status">
    <BaseManagePage 
      title="学籍管理"
      :showSearch="true"
      :showFilter="true"
      :showPagination="true"
      :showAddButton="true"
      :searchPlaceholder="'搜索学生姓名或学号'"
      :searchButtonText="'搜索'"
      :addButtonText="'添加学生'"
      :totalItems="totalStudents"
      :itemsPerPage="itemsPerPage"
      :currentPage="currentPage"
      @search="handleSearch"
      @pageChange="handlePageChange"
      @add="openAddModal"
    >
      <!-- 筛选区域 -->
      <template #filter>
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
        <select 
          v-model="classFilter" 
          class="filter-select"
          @change="handleClassFilterChange(classFilter)"
        >
          <option value="">全班级</option>
          <option value="1班">1班</option>
          <option value="2班">2班</option>
          <option value="3班">3班</option>
          <option value="4班">4班</option>
          <option value="5班">5班</option>
        </select>
      </template>
      
      <!-- 学生学籍列表 -->
      <template #data>
        <div class="status-table-container">
          <table class="status-table">
            <thead>
              <tr>
                <th>学号</th>
                <th>姓名</th>
                <th>性别</th>
                <th>年级</th>
                <th>班级</th>
                <th>学籍状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in paginatedStudents" :key="student.id">
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.gender }}</td>
                <td>{{ student.grade }}</td>
                <td>{{ student.class }}</td>
                <td>
                  <span :class="['status-badge', student.status]">
                    {{ student.statusText }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-primary btn-sm mr-2" @click="editStudent(student)">编辑</button>
                  <button class="btn btn-secondary btn-sm mr-2" @click="viewStudent(student)">查看详情</button>
                  <button class="btn btn-error btn-sm mr-2" @click="deleteStudent(student.id)">删除</button>
                  <button 
                    class="btn btn-warning btn-sm" 
                    @click="archiveStudent(student)"
                    v-if="student.status !== 'graduated'"
                  >
                    归档
                  </button>
                  <button 
                    class="btn btn-success btn-sm" 
                    @click="unarchiveStudent(student)"
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
        <!-- 添加/编辑学生模态框 -->
        <BaseModal 
          :visible="showModal"
          :title="isEditMode ? '编辑学生' : '添加学生'"
          :showFooter="true"
          :showCancelButton="true"
          :showSaveButton="true"
          :cancelButtonText="'取消'"
          :saveButtonText="'确定修改'"
          @close="closeModal"
          @save="saveStudent"
        >
          <form @submit.prevent="saveStudent">
            <div class="form-group">
              <label>学号</label>
              <input v-model="formData.id" type="text" required :disabled="isEditMode" />
            </div>
            <div class="form-group">
              <label>姓名</label>
              <input v-model="formData.name" type="text" required />
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="formData.gender" required>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
            <div class="form-group">
              <label>年级</label>
              <select v-model="formData.grade" required>
                <option value="高一">高一</option>
                <option value="高二">高二</option>
                <option value="高三">高三</option>
              </select>
            </div>
            <div class="form-group">
              <label>班级</label>
              <select v-model="formData.class" required>
                <option value="1班">1班</option>
                <option value="2班">2班</option>
                <option value="3班">3班</option>
                <option value="4班">4班</option>
                <option value="5班">5班</option>
              </select>
            </div>
            <div class="form-group">
              <label>学籍状态</label>
              <select v-model="formData.status" required>
                <option value="active">在校</option>
                <option value="suspended">休学</option>
                <option value="graduated">毕业</option>
                <option value="dropped">退学</option>
              </select>
            </div>
          </form>
        </BaseModal>
        
        <!-- 查看学生详情模态框 -->
        <BaseModal 
          :visible="showDetailModal"
          title="学生详情"
          @close="closeDetailModal"
        >
          <div class="detail-info">
            <div class="detail-item">
              <label>学号：</label>
              <span>{{ selectedStudent?.id }}</span>
            </div>
            <div class="detail-item">
              <label>姓名：</label>
              <span>{{ selectedStudent?.name }}</span>
            </div>
            <div class="detail-item">
              <label>性别：</label>
              <span>{{ selectedStudent?.gender }}</span>
            </div>
            <div class="detail-item">
              <label>年级：</label>
              <span>{{ selectedStudent?.grade }}</span>
            </div>
            <div class="detail-item">
              <label>班级：</label>
              <span>{{ selectedStudent?.class }}</span>
            </div>
            <div class="detail-item">
              <label>学籍状态：</label>
              <span :class="['status-badge', selectedStudent?.status]">{{ selectedStudent?.statusText }}</span>
            </div>
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
import { useStudentStatusManage } from '@/composables/student/useStudentStatusManage';
import type { StudentStatus } from '@/types';

// 使用学籍管理composable
const {
  loading,
  error,
  searchQuery,
  currentPage,
  itemsPerPage,
  gradeFilter,
  classFilter,
  allStudents,
  filteredStudents,
  paginatedStudents,
  totalStudents,
  addStudent,
  updateStudent,
  deleteStudent,
  getStudentById,
  archiveStudent,
  unarchiveStudent,
  handleSearch,
  handleGradeFilterChange,
  handleClassFilterChange,
  handlePageChange
} = useStudentStatusManage();

// 模态框相关
const showModal = ref(false);
const showDetailModal = ref(false);
const isEditMode = ref(false);
const selectedStudent = ref<StudentStatus | null>(null);

// 表单数据
const formData = ref<StudentStatus>({
  id: '',
  name: '',
  gender: '男',
  grade: '高一',
  class: '1班',
  status: 'active',
  statusText: '在校'
});

// 打开添加模态框
const openAddModal = () => {
  isEditMode.value = false;
  formData.value = {
    id: '',
    name: '',
    gender: '男',
    grade: '高一',
    class: '1班',
    status: 'active',
    statusText: '在校'
  };
  showModal.value = true;
};

// 编辑学生
const editStudent = (student: StudentStatus) => {
  isEditMode.value = true;
  formData.value = { ...student };
  showModal.value = true;
};

// 查看学生详情
const viewStudent = (student: StudentStatus) => {
  selectedStudent.value = student;
  showDetailModal.value = true;
};

// 关闭模态框
const closeModal = () => {
  showModal.value = false;
  formData.value = {
    id: '',
    name: '',
    gender: '男',
    grade: '高一',
    class: '1班',
    status: 'active',
    statusText: '在校'
  };
};

// 关闭详情模态框
const closeDetailModal = () => {
  showDetailModal.value = false;
  selectedStudent.value = null;
};

// 保存学生
const saveStudent = async () => {
  // 根据状态值更新状态文本
  const statusMap: { [key: string]: string } = {
    'active': '在校',
    'suspended': '休学',
    'graduated': '毕业',
    'dropped': '退学'
  };
  formData.value.statusText = statusMap[formData.value.status] || '在校';
  
  if (isEditMode.value) {
    // 编辑现有学生
    await updateStudent(formData.value);
  } else {
    // 添加新学生
    await addStudent(formData.value);
  }
  closeModal();
};

// 初始化数据
onMounted(() => {
  // 数据初始化已在useStudentStatusManage中处理
});
</script>