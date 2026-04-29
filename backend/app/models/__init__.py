from .student import Student
from .teacher import Teacher, TeacherClass, HomeroomTeacher
from .course import Course
from .grade import Grade
from .user import User
from .student_course import StudentCourse
from .teacher_course import TeacherCourse
from .teaching_progress import TeachingProgress
from .exam import Exam
from .classroom import Classroom
from .grade_settings import GradeSettings
from .course_schedule import CourseSchedule

__all__ = ['Student', 'Teacher', 'TeacherClass', 'HomeroomTeacher', 'Course', 'Grade', 'User', 'StudentCourse', 'TeacherCourse', 'TeachingProgress', 'Exam', 'Classroom', 'GradeSettings', 'CourseSchedule']

# 有效班级列表常量
VALID_CLASSES = ["1班", "2班", "3班", "4班", "5班", "6班"]

# 有效年级列表常量
VALID_GRADES = ["高一", "高二", "高三"]

# 有效学科列表常量
VALID_SUBJECTS = ["语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "政治", "音乐", "体育"]

# 有效职称列表常量
VALID_TITLES = ["高级教师", "一级教师", "二级教师"]

# 有效班级全称列表常量（用于教师任教班级和班主任班级）
VALID_FULL_CLASSES = [
    "高一1班", "高一2班", "高一3班", "高一4班", "高一5班", "高一6班",
    "高二1班", "高二2班", "高二3班", "高二4班", "高二5班", "高二6班",
    "高三1班", "高三2班", "高三3班", "高三4班", "高三5班", "高三6班"
]