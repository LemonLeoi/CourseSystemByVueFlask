<template>
  <Layout active-path="/teachers">
    <BaseManagePage 
      title="教师管理"
      :show-search="true"
      :show-filter="true"
      :show-pagination="true"
      :show-add-button="true"
      :search-placeholder="'搜索教师姓名或工号'"
      :search-button-text="'搜索'"
      :add-button-text="'添加教师'"
      :total-items="totalTeachers"
      :items-per-page="itemsPerPage"
      :current-page="currentPage"
      @search="handleSearch"
      @pageChange="handlePageChange"
      @add="openAddModal"
    >
      <!-- 筛选区域 -->
      <template #filter>
        <select v-model="subjectFilter" class="filter-select">
          <option value="">全学科</option>
          <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
        </select>
      </template>
      
      <!-- 教师列表 -->
      <template #data>
        <div class="teacher-table-container">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>加载中，请稍候...</p>
          </div>
          
          <!-- 错误信息 -->
          <div v-else-if="error" class="error-container">
            <div class="error-icon">⚠️</div>
            <p class="error-message">{{ error }}</p>
            <button class="btn btn-primary" @click="loadTeachers">重试</button>
          </div>
          
          <!-- 空数据状态 -->
          <div v-else-if="paginatedTeachers.length === 0" class="empty-container">
            <div class="empty-icon">👨‍🏫</div>
            <p>暂无教师数据</p>
            <button class="btn btn-primary" @click="openAddModal">添加教师</button>
          </div>
          
          <!-- 教师表格 -->
          <table v-else class="teacher-table">
            <thead>
              <tr>
                <th>工号</th>
                <th>姓名</th>
                <th>性别</th>
                <th>年龄</th>
                <th>学科</th>
                <th>职称</th>
                <th>联系方式</th>
                <th>任教班级</th>
                <th>班主任状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="teacher in paginatedTeachers" :key="teacher.id">
                <td>{{ teacher.teacher_id }}</td>
                <td>{{ teacher.name }}</td>
                <td>{{ teacher.gender }}</td>
                <td>{{ teacher.age }}</td>
                <td>{{ teacher.subject }}</td>
                <td>{{ teacher.title }}</td>
                <td>{{ teacher.contact }}</td>
                <td>{{ teacher.teachingClasses && Array.isArray(teacher.teachingClasses) ? teacher.teachingClasses.join(', ') : '无' }}</td>
                <td>{{ teacher.isHomeroomTeacher ? teacher.homeroomClass + '班主任' : '无' }}</td>
                <td>
                  <button class="btn btn-primary btn-sm mr-2" @click="editTeacher(teacher)">编辑</button>
                  <button class="btn btn-error btn-sm" @click="handleDelete(teacher)">删除</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
      
      <!-- 模态框 -->
      <template #modal>
        <!-- 添加/编辑教师模态框 -->
        <BaseModal 
          :visible="showModal"
          :title="editingTeacher ? '编辑教师' : '添加教师'"
          :show-footer="true"
          :show-cancel-button="true"
          :show-save-button="true"
          :cancel-button-text="'取消'"
          :save-button-text="'确定修改'"
          @close="closeModal"
          @save="saveTeacher"
        >
          <form @submit.prevent="saveTeacher">
            <div class="form-group">
              <label for="teacherId">工号</label>
              <input 
                type="text" 
                id="teacherId" 
                v-model="formData.teacher_id" 
                :disabled="!!editingTeacher"
                required
              />
            </div>
            <div class="form-group">
              <label for="teacherName">姓名</label>
              <input 
                type="text" 
                id="teacherName" 
                v-model="formData.name" 
                required
              />
            </div>
            <div class="form-group">
              <label for="teacherGender">性别</label>
              <select 
                id="teacherGender" 
                v-model="formData.gender" 
                required
              >
                <option value="">请选择</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
            <div class="form-group">
              <label for="teacherAge">年龄</label>
              <input 
                type="number" 
                id="teacherAge" 
                v-model.number="formData.age" 
                min="20" 
                max="65" 
                required
              />
            </div>
            <div class="form-group">
              <label for="teacherSubject">学科</label>
              <select 
                id="teacherSubject" 
                v-model="formData.subject" 
                required
              >
                <option value="">请选择</option>
                <option v-for="subject in subjects" :key="subject" :value="subject">{{ subject }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="teacherTitle">职称</label>
              <select 
                id="teacherTitle" 
                v-model="formData.title" 
                required
              >
                <option value="">请选择</option>
                <option v-for="title in titles" :key="title" :value="title">{{ title }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="teacherContact">联系方式</label>
              <input 
                type="text" 
                id="teacherContact" 
                v-model="formData.contact" 
                required
              />
            </div>
            <div class="form-group">
              <label for="teacherTeachingClasses">任教班级</label>
              <select 
                id="teacherTeachingClasses" 
                v-model="formData.teachingClasses" 
                multiple
                class="multiselect"
                style="height: 120px;"
              >
                <option v-for="classItem in fullClasses" :key="classItem" :value="classItem">{{ classItem }}</option>
              </select>
              <small class="form-text text-muted">按住Ctrl键可多选</small>
            </div>
            <div class="form-group">
              <label for="teacherIsHomeroomTeacher">是否班主任</label>
              <select 
                id="teacherIsHomeroomTeacher" 
                v-model="formData.isHomeroomTeacher"
              >
                <option value="false">否</option>
                <option value="true">是</option>
              </select>
            </div>
            <div class="form-group" v-if="formData.isHomeroomTeacher">
              <label for="teacherHomeroomClass">班主任班级</label>
              <select 
                id="teacherHomeroomClass" 
                v-model="formData.homeroomClass" 
                required
              >
                <option value="">请选择</option>
                <option v-for="classItem in fullClasses" :key="classItem" :value="classItem">{{ classItem }}</option>
              </select>
            </div>
          </form>
        </BaseModal>
      </template>
    </BaseManagePage>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Layout from '@/components/layout/Layout.vue';
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import BaseModal from '@/components/business/BaseModal.vue';
import { useTeacherManage } from '@/composables/teacher/useTeacherManage';
import type { Teacher } from '@/types';

// 筛选
const subjectFilter = ref('');

// 教师相关选项列表（从后端API获取）
const subjects = ref<string[]>([]);
const titles = ref<string[]>([]);
const fullClasses = ref<string[]>([]);
const isLoadingOptions = ref(false);

// 从后端API获取教师相关选项列表
const loadTeacherOptions = async () => {
  try {
    isLoadingOptions.value = true;
    console.log('=== 开始获取教师相关选项列表 ===');
    const response = await fetch('/api/teachers/options');
    if (!response.ok) {
      throw new Error('获取教师相关选项列表失败');
    }
    const data = await response.json();
    console.log('=== API响应成功 ===');
    console.log('获取到的教师相关选项列表:', data);
    subjects.value = data.subjects || [];
    titles.value = data.titles || [];
    fullClasses.value = data.fullClasses || [];
    console.log('=== 选项卡数据更新完成 ===');
  } catch (error) {
    console.error('=== 获取教师相关选项列表失败 ===');
    console.error('错误信息:', error);
    // 失败时使用默认值，确保系统能正常运行
    subjects.value = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治'];
    titles.value = ['高级教师', '一级教师', '二级教师'];
    fullClasses.value = [
      '高一1班', '高一2班', '高一3班', '高一4班', '高一5班',
      '高二1班', '高二2班', '高二3班', '高二4班', '高二5班',
      '高三1班', '高三2班', '高三3班', '高三4班', '高三5班'
    ];
  } finally {
    isLoadingOptions.value = false;
  }
};

// 使用教师管理composable
const {
  loading,
  error,
  searchQuery,
  currentPage,
  itemsPerPage,
  allTeachers,
  filteredTeachers,
  paginatedTeachers,
  totalTeachers,
  loadTeachers,
  addTeacher,
  updateTeacher,
  deleteTeacher,
  getTeacherById,
  handleSearch,
  handlePageChange
} = useTeacherManage(subjectFilter);

// 模态框相关
const showModal = ref(false);
const editingTeacher = ref<Teacher | null>(null);
const formData = ref<Teacher>({
  id: '',
  teacher_id: '',
  name: '',
  gender: '',
  age: 0,
  subject: '',
  title: '',
  contact: '',
  teachingClasses: [],
  isHomeroomTeacher: false,
  homeroomClass: ''
});

const openAddModal = () => {
  editingTeacher.value = null;
  formData.value = {
    id: '',
    teacher_id: '',
    name: '',
    gender: '',
    age: 0,
    subject: '',
    title: '',
    contact: '',
    teachingClasses: [],
    isHomeroomTeacher: false,
    homeroomClass: ''
  };
  showModal.value = true;
};

const editTeacher = (teacher: Teacher) => {
  editingTeacher.value = teacher;
  formData.value = { ...teacher };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingTeacher.value = null;
};

const saveTeacher = async () => {
  // 确保teachingClasses是数组类型
  if (!Array.isArray(formData.value.teachingClasses)) {
    formData.value.teachingClasses = [];
  }
  
  // 验证提交的学科、职称和班级值是否在有效范围内
  if (formData.value.subject && !subjects.value.includes(formData.value.subject)) {
    alert('错误：所选学科不在有效范围内');
    return;
  }
  if (formData.value.title && !titles.value.includes(formData.value.title)) {
    alert('错误：所选职称不在有效范围内');
    return;
  }
  if (formData.value.teachingClasses) {
    for (const classItem of formData.value.teachingClasses) {
      if (classItem && !fullClasses.value.includes(classItem)) {
        alert(`错误：所选班级 ${classItem} 不在有效范围内`);
        return;
      }
    }
  }
  if (formData.value.isHomeroomTeacher && formData.value.homeroomClass && !fullClasses.value.includes(formData.value.homeroomClass)) {
    alert('错误：所选班主任班级不在有效范围内');
    return;
  }
  
  if (editingTeacher.value) {
    // 编辑现有教师
    await updateTeacher(formData.value);
  } else {
    // 添加新教师
    await addTeacher(formData.value);
  }
  
  // 操作完成后刷新选项卡数据
  await loadTeacherOptions();
  closeModal();
  currentPage.value = 1;
};

// 处理删除操作，添加二次确认
const handleDelete = async (teacher: any) => {
  if (confirm(`确定要删除教师 ${teacher.name} 吗？此操作不可恢复。`)) {
    await deleteTeacher(teacher.teacher_id);
  }
};

// 监听筛选条件变化
watch(subjectFilter, () => {
  currentPage.value = 1;
});

// 初始化数据
onMounted(async () => {
  // 数据初始化已在useTeacherManage中处理
  // 加载教师相关选项列表
  await loadTeacherOptions();
  
  // 设置定时刷新机制，每5分钟刷新一次选项卡数据
  const refreshInterval = setInterval(async () => {
    console.log('=== 定时刷新教师相关选项列表 ===');
    await loadTeacherOptions();
  }, 5 * 60 * 1000);
  
  // 组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(refreshInterval);
  });
});
</script>