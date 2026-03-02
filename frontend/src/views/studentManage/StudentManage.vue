<template>
  <Layout activePath="/students">
    <BaseManagePage 
      title="学生管理"
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
          @change="loadStudents"
        >
          <option value="">全年级</option>
          <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}</option>
        </select>
        <select 
          v-model="classFilter" 
          class="filter-select"
          @change="loadStudents"
        >
          <option value="">全班级</option>
          <option v-for="classItem in classes" :key="classItem" :value="classItem">{{ classItem }}</option>
        </select>
      </template>
      
      <!-- 学生列表 -->
      <template #data>
        <div class="student-table-container">
          <!-- 加载状态 -->
          <div v-if="loading" class="loading-container">
            <div class="loading-spinner"></div>
            <p>加载中，请稍候...</p>
          </div>
          
          <!-- 错误信息 -->
          <div v-else-if="error" class="error-container">
            <div class="error-icon">⚠️</div>
            <p class="error-message">{{ error }}</p>
            <button class="btn btn-primary" @click="loadStudents">重试</button>
          </div>
          
          <!-- 空数据状态 -->
          <div v-else-if="paginatedStudents.length === 0" class="empty-container">
            <div class="empty-icon">📋</div>
            <p>暂无学生数据</p>
            <button class="btn btn-primary" @click="openAddModal">添加学生</button>
          </div>
          
          <!-- 学生表格 -->
          <table v-else class="student-table">
            <thead>
              <tr>
                <th>学号</th>
                <th>姓名</th>
                <th>性别</th>
                <th>年级</th>
                <th>班级</th>
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
                  <button class="btn btn-primary btn-sm mr-2" @click="editStudent(student)">编辑</button>
                  <button class="btn btn-error btn-sm mr-2" @click="handleDelete(student)">删除</button>
                  <button class="btn btn-secondary btn-sm" @click="manageScores(student)">成绩</button>
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
          :title="editingStudent ? '编辑学生' : '添加学生'"
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
              <label for="studentId">学号</label>
              <input 
                type="text" 
                id="studentId" 
                v-model="formData.id" 
                :disabled="!!editingStudent"
                required
              >
            </div>
            <div class="form-group">
              <label for="studentName">姓名</label>
              <input 
                type="text" 
                id="studentName" 
                v-model="formData.name" 
                required
              >
            </div>
            <div class="form-group">
              <label for="studentGender">性别</label>
              <select 
                id="studentGender" 
                v-model="formData.gender" 
                required
              >
                <option value="">请选择</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
            <div class="form-group">
              <label for="studentGrade">年级</label>
              <select 
                id="studentGrade" 
                v-model="formData.grade" 
                required
              >
                <option value="">请选择</option>
                <option v-for="grade in grades" :key="grade" :value="grade">{{ grade }}</option>
              </select>
            </div>
            <div class="form-group">
              <label for="studentClass">班级</label>
              <select 
                id="studentClass" 
                v-model="formData.class" 
                required
              >
                <option value="">请选择</option>
                <option v-for="classItem in classes" :key="classItem" :value="classItem">{{ classItem }}</option>
              </select>
            </div>
          </form>
        </BaseModal>
        
        <!-- 成绩管理模态框 -->
        <BaseModal 
          :visible="showScoreModal"
          :title="selectedStudent ? selectedStudent.name + '的成绩管理' : '成绩管理'"
          :showFooter="true"
          :showCancelButton="true"
          :showSaveButton="true"
          :cancelButtonText="'取消'"
          :saveButtonText="'确定修改'"
          @close="closeScoreModal"
          @save="saveAllScores"
        >
          <!-- 考试信息选择 -->
          <div class="exam-info-section">
            <h4>考试信息</h4>
            <div class="form-row">
              <div class="form-group">
                <label for="examType">考试类型</label>
                <select v-model="examInfo.examType" id="examType" class="form-control" required>
                  <option value="">请选择考试类型</option>
                  <option value="期中考试">期中考试</option>
                  <option value="期末考试">期末考试</option>
                  <option value="月考">月考</option>
                  <option value="模拟考试">模拟考试</option>
                </select>
              </div>
              <div class="form-group">
                <label for="semester">学期</label>
                <select v-model="examInfo.semester" id="semester" class="form-control" required>
                  <option value="">请选择学期</option>
                  <option value="上学期">上学期</option>
                  <option value="下学期">下学期</option>
                </select>
              </div>
              <div class="form-group">
                <label for="examDate">考试日期</label>
                <input type="date" v-model="examInfo.examDate" id="examDate" class="form-control" required>
              </div>
              <div class="form-group">
                <label for="period">考试周期</label>
                <input type="text" v-model="examInfo.period" id="period" class="form-control" placeholder="例如：2024-2025学年第一学期">
              </div>
            </div>
          </div>
          
          <!-- 成绩表格 -->
          <div class="score-table-container">
            <h4>成绩详情</h4>
            <table class="score-table">
              <thead>
                <tr>
                  <th>学科</th>
                  <th>成绩</th>
                  <th>等级</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in studentScores" :key="score.subject">
                  <td>{{ score.subject }}</td>
                  <td>
                    <input 
                      type="number" 
                      v-model.number="score.score" 
                      class="score-input"
                      min="0" 
                      max="100"
                    >
                  </td>
                  <td :class="getGradeClass(score.score)">{{ getGrade(score.score) }}</td>
                  <td>
                    <button class="btn btn-success btn-sm" @click="saveScore(score)">保存</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-success" @click="saveAllScores">保存所有成绩</button>
          </div>
        </BaseModal>
      </template>
    </BaseManagePage>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Layout from '@/components/layout/Layout.vue';
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import BaseModal from '@/components/business/BaseModal.vue';
import { useStudentManage } from '@/composables/student/useStudentManage';
import type { Student, Score } from '@/types';

// 班级和年级列表（从后端API获取）
const grades = ref<string[]>([]);
const classes = ref<string[]>([]);
const isLoadingOptions = ref(false);

// 从后端API获取班级和年级列表
const loadClassOptions = async () => {
  try {
    isLoadingOptions.value = true;
    console.log('=== 开始获取班级和年级列表 ===');
    const response = await fetch('/api/students/classes');
    if (!response.ok) {
      throw new Error('获取班级和年级列表失败');
    }
    const data = await response.json();
    console.log('=== API响应成功 ===');
    console.log('获取到的班级和年级列表:', data);
    grades.value = data.grades || [];
    classes.value = data.classes || [];
    console.log('=== 选项卡数据更新完成 ===');
  } catch (error) {
    console.error('=== 获取班级和年级列表失败 ===');
    console.error('错误信息:', error);
    // 失败时使用默认值，确保系统能正常运行
    grades.value = ['高一', '高二', '高三'];
    classes.value = ['1班', '2班', '3班', '4班', '5班'];
  } finally {
    isLoadingOptions.value = false;
  }
};

// 使用学生管理composable
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
  loadStudents,
  addStudent,
  updateStudent,
  deleteStudent,
  updateStudentScores,
  getStudentById,
  handleSearch,
  handlePageChange
} = useStudentManage();

// 模态框相关
const showModal = ref(false);
const editingStudent = ref<Student | null>(null);
const formData = ref<Student>({
  id: '',
  name: '',
  gender: '',
  grade: '',
  class: ''
});

const openAddModal = () => {
  editingStudent.value = null;
  formData.value = {
    id: '',
    name: '',
    gender: '',
    grade: '',
    class: ''
  };
  showModal.value = true;
};

const editStudent = (student: Student) => {
  editingStudent.value = student;
  formData.value = { ...student };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingStudent.value = null;
};

const saveStudent = async () => {
  // 验证提交的年级和班级值是否在有效范围内
  if (formData.grade && !grades.value.includes(formData.grade)) {
    alert('错误：所选年级不在有效范围内');
    return;
  }
  if (formData.class && !classes.value.includes(formData.class)) {
    alert('错误：所选班级不在有效范围内');
    return;
  }
  
  if (editingStudent.value) {
    // 编辑现有学生
    await updateStudent(formData.value);
  } else {
    // 添加新学生
    await addStudent(formData.value);
  }
  // 操作完成后刷新选项卡数据
  await loadClassOptions();
  closeModal();
  currentPage.value = 1;
};

// 成绩管理相关
const showScoreModal = ref(false);
const selectedStudent = ref<Student | null>(null);
const studentScores = ref<Score[]>([]);
const examInfo = ref({
  examType: '',
  semester: '',
  examDate: '',
  period: ''
});

const manageScores = (student: Student) => {
  selectedStudent.value = student;
  // 初始化考试信息
  examInfo.value = {
    examType: '期中考试',
    semester: '上学期',
    examDate: new Date().toISOString().split('T')[0],
    period: ''
  };
  // 初始化成绩数据
  if (!student.scores) {
    student.scores = [
      { subject: '语文', score: 0 },
      { subject: '数学', score: 0 },
      { subject: '英语', score: 0 },
      { subject: '物理', score: 0 },
      { subject: '化学', score: 0 },
      { subject: '生物', score: 0 },
      { subject: '历史', score: 0 },
      { subject: '地理', score: 0 },
      { subject: '政治', score: 0 }
    ];
  }
  studentScores.value = [...student.scores];
  showScoreModal.value = true;
};

const closeScoreModal = () => {
  showScoreModal.value = false;
  selectedStudent.value = null;
  // 重置考试信息
  examInfo.value = {
    examType: '',
    semester: '',
    examDate: '',
    period: ''
  };
};

const getGrade = (score: number): string => {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'E';
};

const getGradeClass = (score: number): string => {
  if (score >= 90) return 'grade-a';
  if (score >= 80) return 'grade-b';
  if (score >= 70) return 'grade-c';
  if (score >= 60) return 'grade-d';
  return 'grade-e';
};

const saveScore = (score: Score) => {
  if (selectedStudent.value) {
    const student = getStudentById(selectedStudent.value.id);
    if (student) {
      const existingScore = student.scores?.find(s => s.subject === score.subject);
      if (existingScore) {
        existingScore.score = score.score;
        // 添加考试信息
        existingScore.examType = examInfo.value.examType;
        existingScore.semester = examInfo.value.semester;
        existingScore.examDate = examInfo.value.examDate;
        existingScore.period = examInfo.value.period;
      }
    }
  }
};

const saveAllScores = async () => {
  if (selectedStudent.value) {
    console.log('=== 开始保存所有成绩 ===');
    console.log('学生ID:', selectedStudent.value.id);
    console.log('考试信息:', examInfo.value);
    console.log('成绩数据:', studentScores.value);
    
    // 为每个成绩添加考试信息
    const scoresWithExamInfo = studentScores.value.map(score => ({
      ...score,
      examType: examInfo.value.examType,
      semester: examInfo.value.semester,
      examDate: examInfo.value.examDate,
      period: examInfo.value.period
    }));
    
    // 等待成绩更新完成
    const success = await updateStudentScores(selectedStudent.value.id, scoresWithExamInfo);
    
    if (success) {
      console.log('=== 成绩更新成功，开始获取最新学生数据 ===');
      // 直接调用getStudentById获取最新的学生数据，确保数据的实时性
      const updatedStudent = await getStudentById(selectedStudent.value.id);
      console.log('=== 最新学生数据获取成功 ===');
      console.log('更新后的学生数据:', updatedStudent);
      
      if (updatedStudent) {
        selectedStudent.value = updatedStudent;
        studentScores.value = [...updatedStudent.scores];
        console.log('=== 前端状态更新完成 ===');
      }
    }
  }
  closeScoreModal();
};

// 处理删除操作，添加二次确认
const handleDelete = async (student: any) => {
  if (confirm(`确定要删除学生 ${student.name} 吗？此操作不可恢复。`)) {
    await deleteStudent(student.id);
  }
};

// 处理筛选变化
const handleFilterChange = () => {
  console.log('=== 筛选条件变化 ===');
  console.log('年级筛选:', gradeFilter.value);
  console.log('班级筛选:', classFilter.value);
  // 筛选条件变化时，useStudentManage中的watch会自动触发loadStudents
  // 这里可以添加额外的处理逻辑 if needed
};

// 初始化数据
onMounted(async () => {
  // 数据初始化已在useStudentManage中处理
  // 加载班级和年级列表
  await loadClassOptions();
  
  // 设置定时刷新机制，每5分钟刷新一次选项卡数据
  const refreshInterval = setInterval(async () => {
    console.log('=== 定时刷新班级和年级列表 ===');
    await loadClassOptions();
  }, 5 * 60 * 1000);
  
  // 组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(refreshInterval);
  });
});
</script>

<style>
@import '../../styles/common/main.css';

/* 加载状态样式 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误信息样式 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  background-color: #fff5f5;
  border: 1px solid #ffdddd;
  border-radius: 8px;
  margin: 20px 0;
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-message {
  color: #d32f2f;
  margin-bottom: 20px;
  font-size: 16px;
}

/* 空数据状态样式 */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin: 20px 0;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-container p {
  color: #6c757d;
  margin-bottom: 20px;
  font-size: 16px;
}

/* 按钮样式增强 */
.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 表格样式增强 */
.student-table-container {
  margin: 20px 0;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.student-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #e9ecef;
}

.student-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #e9ecef;
}

.student-table tr:hover {
  background-color: #f8f9fa;
}

/* 筛选器样式 */
.filter-select {
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  margin-right: 10px;
  font-size: 14px;
  min-width: 100px;
}

.filter-select:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* 考试信息区域样式 */
.exam-info-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
}

.exam-info-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #495057;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.form-group {
  flex: 1;
  min-width: 150px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #495057;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.score-table-container h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #495057;
}

/* 成绩输入框样式 */
.score-input {
  width: 80px;
  padding: 4px 8px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  text-align: center;
}

.score-input:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* 成绩等级样式 */
.grade-a {
  color: #28a745;
  font-weight: 600;
}

.grade-b {
  color: #17a2b8;
  font-weight: 600;
}

.grade-c {
  color: #ffc107;
  font-weight: 600;
}

.grade-d {
  color: #fd7e14;
  font-weight: 600;
}

.grade-e {
  color: #dc3545;
  font-weight: 600;
}
</style>