<template>
  <div class="teacher-course-page">
    <BaseManagePage 
      title="教师课程表"
      :totalItems="0"
      :showAddButton="true"
      :addButtonText="'添加课程'"
      @add="openAddTeacherCourseModal"
    >
      <template #data>
        <TeacherCourseTab 
          v-model:selectedTeacher="selectedTeacher"
          :teachers="teachers"
          :teacherCourses="teacherCourses"
          :teacherStats="teacherStats"
          :timeSlots="timeSlots"
          :weekDays="weekDays"
          :isLoading="isLoading"
          :error="error"
          :successMessage="successMessage"
          @refreshTeacherSchedule="refreshTeacherSchedule"
          @openAddTeacherCourseModal="openAddTeacherCourseModal"
          @openEditTeacherCourseModal="openEditTeacherCourseModal"
          @deleteTeacherCourse="deleteTeacherCourse"
        />
      </template>
    </BaseManagePage>

    <!-- 教师课程模态框 -->
    <CourseModal
      :visible="showTeacherCourseModal"
      :editingCourse="editingTeacherCourse"
      :formData="teacherCourseForm"
      :type="'teacher'"
      :classrooms="classrooms"
      :courses="courses"
      :classes="classes"
      @close="closeTeacherCourseModal"
      @save="saveTeacherCourse"
    />
  </div>
</template>

<script setup lang="ts">
import BaseManagePage from '@/components/business/BaseManagePage.vue';
import TeacherCourseTab from '@/components/course/TeacherCourseTab.vue';
import CourseModal from '@/components/course/CourseModal.vue';
import { useTeacherCourse } from '@/composables/course/useTeacherCourse';
import { useCourseCommon } from '@/composables/course/useCourseCommon';
import { ref, onMounted } from 'vue';
import { courseApi } from '@/services/api/apiService';

// 使用课程公共composable
const { timeSlots, weekDays } = useCourseCommon();

// 教室数据
const classrooms = ref<any[]>([]);
const loadingClassrooms = ref(false);
const classroomError = ref<string | null>(null);

// 课程数据
const courses = ref<any[]>([]);
const loadingCourses = ref(false);
const courseError = ref<string | null>(null);

// 班级数据
const classes = ref<string[]>([]);
const loadingClassesList = ref(false);
const classesError = ref<string | null>(null);

// 加载教室数据
const loadClassrooms = async () => {
  try {
    loadingClassrooms.value = true;
    classroomError.value = null;
    const data = await courseApi.getClassrooms();
    classrooms.value = data;
  } catch (error) {
    classroomError.value = '加载教室数据失败';
    console.error('Error loading classrooms:', error);
    classrooms.value = [];
  } finally {
    loadingClassrooms.value = false;
  }
};

// 加载课程数据
const loadCourses = async () => {
  try {
    loadingCourses.value = true;
    courseError.value = null;
    const data = await courseApi.getCourses();
    courses.value = data;
  } catch (error) {
    courseError.value = '加载课程数据失败';
    console.error('Error loading courses:', error);
    courses.value = [];
  } finally {
    loadingCourses.value = false;
  }
};

// 加载班级列表数据
const loadClassesList = async () => {
  try {
    loadingClassesList.value = true;
    classesError.value = null;
    // 从后端获取教师选项，其中包含班级列表
    const teacherOptions = await teacherApi.getTeachers();
    // 提取所有教师的任教班级并去重
    const allClasses = new Set<string>();
    teacherOptions.forEach(teacher => {
      if (teacher.teachingClasses) {
        teacher.teachingClasses.forEach(className => {
          allClasses.add(className);
        });
      }
    });
    classes.value = Array.from(allClasses).sort();
  } catch (error) {
    classesError.value = '加载班级数据失败';
    console.error('Error loading classes:', error);
    // 使用默认班级列表
    classes.value = ['高一1班', '高一2班', '高一3班', '高一4班', '高一5班', '高一6班', '高二1班', '高二2班', '高二3班', '高二4班', '高二5班', '高二6班', '高三1班', '高三2班', '高三3班', '高三4班', '高三5班', '高三6班'];
  } finally {
    loadingClassesList.value = false;
  }
};

// 使用教师课程composable
const {
  // 状态
  selectedTeacher,
  teachers,
  teacherCourses,
  teacherStats,
  
  // 模态框状态
  showTeacherCourseModal,
  editingTeacherCourse,
  teacherCourseForm,
  
  // 操作状态
  isLoading,
  error,
  successMessage,
  
  // 方法
  refreshTeacherSchedule,
  openAddTeacherCourseModal,
  openEditTeacherCourseModal,
  closeTeacherCourseModal,
  saveTeacherCourse,
  deleteTeacherCourse
} = useTeacherCourse();

// 初始化数据
onMounted(async () => {
  await Promise.all([
    loadClassrooms(),
    loadCourses(),
    loadClassesList()
  ]);
});
</script>

<style scoped>
.teacher-course-page {
  padding: 20px;
}
</style>