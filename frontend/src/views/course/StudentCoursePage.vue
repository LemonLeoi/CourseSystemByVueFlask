<template>
  <div class="student-course-page">
    <BaseManagePage 
      title="学生课程表"
      :totalItems="0"
      :showAddButton="true"
      :addButtonText="'添加课程'"
      @add="openAddStudentCourseModal"
    >
      <template #data>
        <StudentCourseTab 
          v-model:studentGrade="studentGrade"
          v-model:studentClass="studentClass"
          :studentCourses="studentCourses"
          :timeSlots="timeSlots"
          :weekDays="weekDays"
          :isLoading="isLoading"
          :error="error"
          :successMessage="successMessage"
          @refreshStudentSchedule="refreshStudentSchedule"
          @openAddStudentCourseModal="openAddStudentCourseModal"
          @openEditStudentCourseModal="openEditStudentCourseModal"
          @deleteStudentCourse="deleteStudentCourse"
        />
      </template>
    </BaseManagePage>

    <!-- 学生课程模态框 -->
    <CourseModal
      :visible="showStudentCourseModal"
      :editingCourse="editingStudentCourse"
      :formData="studentCourseForm"
      :type="'student'"
      :teachers="teachers"
      :courses="courses"
      :classrooms="classrooms"
      @close="closeStudentCourseModal"
      @save="saveStudentCourse"
    />
  </div>
</template>

<script setup lang="ts">
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import StudentCourseTab from '@/components/course/StudentCourseTab.vue';
import CourseModal from '@/components/course/CourseModal.vue';
import { useStudentCourse } from '@/composables/course/useStudentCourse';
import { useCourseCommon } from '@/composables/course/useCourseCommon';
import { courseApi } from '@/services/api/apiService';
import { ref, onMounted } from 'vue';

// 使用课程公共composable
const { timeSlots, weekDays } = useCourseCommon();

// 使用学生课程composable
const {
  // 状态
  studentGrade,
  studentClass,
  studentCourses,
  teachers,
  
  // 模态框状态
  showStudentCourseModal,
  editingStudentCourse,
  studentCourseForm,
  
  // 操作状态
  isLoading,
  error,
  successMessage,
  
  // 方法
  refreshStudentSchedule,
  openAddStudentCourseModal,
  openEditStudentCourseModal,
  closeStudentCourseModal,
  saveStudentCourse,
  deleteStudentCourse
} = useStudentCourse();

// 课程列表
const courses = ref<Array<{
  id: number;
  course_name: string;
  course_code: string;
}>>([]);

// 教室列表
const classrooms = ref<Array<{
  room_id: string;
  grade: string;
  class: string;
  building: string;
  room_number: number;
}>>([]);

// 加载课程列表
const loadCourses = async () => {
  try {
    const coursesData = await courseApi.getCourses();
    courses.value = coursesData;
  } catch (err) {
    console.error('Error loading courses:', err);
    courses.value = [];
  }
};

// 加载教室列表
const loadClassrooms = async () => {
  try {
    const classroomsData = await fetch('/api/courses/classrooms');
    if (classroomsData.ok) {
      const data = await classroomsData.json();
      classrooms.value = data;
    } else {
      console.error('Error loading classrooms:', await classroomsData.text());
      classrooms.value = [];
    }
  } catch (err) {
    console.error('Error loading classrooms:', err);
    classrooms.value = [];
  }
};

// 初始化数据
onMounted(async () => {
  await loadCourses();
  await loadClassrooms();
});
</script>

<style scoped>
.student-course-page {
  padding: 20px;
}
</style>