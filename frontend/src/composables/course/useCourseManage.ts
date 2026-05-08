import { useCourseCommon } from './useCourseCommon';
import { useStudentCourse } from './useStudentCourse';
import { useTeacherCourse } from './useTeacherCourse';
import { useTeachingProgress } from './useTeachingProgress';

export function useCourseManage() {
  // 使用公共逻辑
  const common = useCourseCommon();
  
  // 使用学生课程逻辑
  const studentCourse = useStudentCourse();
  
  // 使用教师课程逻辑
  const teacherCourse = useTeacherCourse();
  
  // 使用教学进度逻辑
  const teachingProgress = useTeachingProgress();

  // 处理添加按钮点击
  const handleAddClick = () => {
    switch (common.activeTab.value) {
      case 'student':
        studentCourse.openAddStudentCourseModal(common.weekDays.value);
        break;
      case 'teacher':
        teacherCourse.openAddTeacherCourseModal(common.weekDays.value);
        break;
      case 'progress':
        teachingProgress.openAddProgressModal();
        break;
    }
  };

  return {
    // 公共状态
    activeTab: common.activeTab,
    timeSlots: common.timeSlots,
    weekDays: common.weekDays,
    
    // 学生课程状态
    studentGrade: studentCourse.studentGrade,
    studentClass: studentCourse.studentClass,
    studentCourses: studentCourse.studentCourses,
    showStudentCourseModal: studentCourse.showStudentCourseModal,
    editingStudentCourse: studentCourse.editingStudentCourse,
    studentCourseForm: studentCourse.studentCourseForm,
    studentIsLoading: studentCourse.isLoading,
    studentError: studentCourse.error,
    studentSuccessMessage: studentCourse.successMessage,
    
    // 教师相关状态
    teachers: studentCourse.teachers,
    selectedTeacherId: studentCourse.selectedTeacherId,
    selectedTeacher: studentCourse.selectedTeacher,
    
    // 教师课程状态
    selectedTeacherForCourses: teacherCourse.selectedTeacher,
    courseTeachers: teacherCourse.teachers,
    teacherCourses: teacherCourse.teacherCourses,
    teacherStats: teacherCourse.teacherStats,
    showTeacherCourseModal: teacherCourse.showTeacherCourseModal,
    editingTeacherCourse: teacherCourse.editingTeacherCourse,
    teacherCourseForm: teacherCourse.teacherCourseForm,
    teacherIsLoading: teacherCourse.isLoading,
    teacherError: teacherCourse.error,
    teacherSuccessMessage: teacherCourse.successMessage,
    
    // 教学进度状态
    progressSubject: teachingProgress.progressSubject,
    progressGrade: teachingProgress.progressGrade,
    teachingProgress: teachingProgress.teachingProgress,
    teachingProgressIsLoading: teachingProgress.isLoading,
    teachingProgressError: teachingProgress.error,
    teachingProgressSuccessMessage: teachingProgress.successMessage,
    showProgressModal: teachingProgress.showProgressModal,
    editingProgress: teachingProgress.editingProgress,
    progressForm: teachingProgress.progressForm,
    
    // 公共方法
    getAddButtonText: common.getAddButtonText,
    handleAddClick,
    getSlotName: common.getSlotName,
    
    // 学生课程方法
    getStudentCourse: studentCourse.getStudentCourse,
    refreshStudentSchedule: studentCourse.refreshStudentSchedule,
    updateStudentCoursesByGradeClass: studentCourse.updateStudentCoursesByGradeClass,
    openAddStudentCourseModal: () => studentCourse.openAddStudentCourseModal(common.weekDays.value),
    openEditStudentCourseModal: studentCourse.openEditStudentCourseModal,
    closeStudentCourseModal: studentCourse.closeStudentCourseModal,
    saveStudentCourse: studentCourse.saveStudentCourse,
    deleteStudentCourse: studentCourse.deleteStudentCourse,
    loadTeachers: studentCourse.loadTeachers,
    handleTeacherSelect: studentCourse.handleTeacherSelect,
    
    // 教师课程方法
    getTeacherCourse: teacherCourse.getTeacherCourse,
    refreshTeacherSchedule: teacherCourse.refreshTeacherSchedule,
    updateTeacherCoursesByTeacher: teacherCourse.updateTeacherCoursesByTeacher,
    openAddTeacherCourseModal: () => teacherCourse.openAddTeacherCourseModal(common.weekDays.value),
    openEditTeacherCourseModal: teacherCourse.openEditTeacherCourseModal,
    closeTeacherCourseModal: teacherCourse.closeTeacherCourseModal,
    saveTeacherCourse: teacherCourse.saveTeacherCourse,
    deleteTeacherCourse: teacherCourse.deleteTeacherCourse,
    
    // 教学进度方法
    getStatusText: teachingProgress.getStatusText,
    refreshProgress: teachingProgress.refreshProgress,
    deleteProgress: teachingProgress.deleteTeachingProgress,
    openAddProgressModal: teachingProgress.openAddProgressModal,
    editProgress: teachingProgress.editProgress,
    closeProgressModal: teachingProgress.closeProgressModal,
    saveProgress: teachingProgress.saveProgress
  };
}
