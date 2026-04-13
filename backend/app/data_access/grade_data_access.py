from ..models import Grade, Student, Exam, Teacher, TeacherCourse, StudentCourse, Course
from .. import db

class GradeDataAccess:
    @staticmethod
    def get_student_grades(student_id):
        """获取学生个人成绩"""
        # 获取学生信息
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return None, None
        
        # 获取学生成绩，使用左连接以处理exam_id为None的情况
        grades = db.session.query(
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).filter(
            Grade.student_id == student_id
        ).all()
        
        # 转换为与原有格式兼容的结构
        formatted_grades = []
        for grade in grades:
            # 由于exam_id为None，我们使用默认值
            formatted_grades.append((
                '未知考试',  # exam_name
                '2024-2025学年',  # academic_year
                '第一学期',  # semester
                student.grade,  # grade
                '期中考试',  # exam_type
                grade[0],  # subject
                grade[1],  # score
                grade[2]   # grade_level
            ))
        
        student_info = (student.name, student.gender, student.class_, student.grade)
        return student_info, formatted_grades
    
    @staticmethod
    def get_class_average(student_class, student_grade):
        """获取班级平均成绩"""
        # 查询班级学科平均成绩
        class_avgs = db.session.query(
            Grade.subject,
            db.func.avg(Grade.score).label('avg_score')
        ).join(
            Student, Grade.student_id == Student.student_id
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Student.class_ == student_class,
            Student.grade == student_grade
        ).group_by(
            Grade.subject
        ).all()
        
        # 转换为字典
        avg_dict = {}
        for subject, avg_score in class_avgs:
            avg_dict[subject] = round(avg_score, 2)
        
        return avg_dict
    
    @staticmethod
    def get_class_students(class_name, grade):
        """获取班级学生"""
        students = Student.query.filter_by(
            class_=class_name,
            grade=grade
        ).all()
        
        return [(student.student_id, student.name) for student in students]
    
    @staticmethod
    def get_class_grades(class_name, grade):
        """获取班级所有成绩"""
        grades = db.session.query(
            Grade.student_id,
            Exam.exam_name,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Student, Grade.student_id == Student.student_id
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade
        ).order_by(
            Grade.student_id,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type
        ).all()
        
        return grades
    
    @staticmethod
    def get_grade_classes(grade):
        """获取年级所有班级"""
        classes = db.session.query(
            db.distinct(Student.class_)
        ).filter(
            Student.grade == grade
        ).all()
        
        return [class_[0] for class_ in classes]
    
    @staticmethod
    def get_grade_grades(grade):
        """获取年级所有成绩"""
        grades = db.session.query(
            Student.class_,
            Exam.exam_name,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Student, Grade.student_id == Student.student_id
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Student.grade == grade
        ).order_by(
            Student.class_,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type
        ).all()
        
        return grades
    
    @staticmethod
    def get_class_subject_grades(class_name, grade, subject):
        """获取班级指定科目的成绩"""
        grades = db.session.query(
            Grade.student_id,
            Student.name,
            Grade.score
        ).join(
            Student, Grade.student_id == Student.student_id
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade,
            Grade.subject == subject
        ).all()
        
        return grades
    
    @staticmethod
    def get_grade_subject_grades(grade, subject):
        """获取年级指定科目的成绩"""
        grades = db.session.query(
            Student.class_,
            Grade.score
        ).join(
            Student, Grade.student_id == Student.student_id
        ).filter(
            Student.grade == grade,
            Grade.subject == subject
        ).all()
        
        return grades
    
    @staticmethod
    def get_teacher_subject_grades(subject):
        """获取教师指定科目的成绩"""
        grades = db.session.query(
            Teacher.name,
            Student.class_,
            Student.grade,
            Grade.score
        ).join(
            TeacherCourse, Teacher.teacher_id == TeacherCourse.teacher_id
        ).join(
            Course, TeacherCourse.course_code == Course.course_code
        ).join(
            Student, TeacherCourse.class_ == Student.class_ and TeacherCourse.grade == Student.grade
        ).join(
            Grade, Student.student_id == Grade.student_id
        ).filter(
            Course.course_name == subject,
            Grade.subject == subject
        ).all()
        
        return grades
    
    @staticmethod
    def get_student_schedule_grades(student_id):
        """获取学生课程安排和成绩"""
        # 获取学生信息
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return []
        
        # 获取学生课程安排和成绩
        from sqlalchemy import and_
        schedule_grades = db.session.query(
            StudentCourse.day_of_week,
            StudentCourse.period,
            Course.course_name,
            Teacher.name,
            Grade.score
        ).join(
            Course, StudentCourse.course_code == Course.course_code
        ).join(
            Teacher, StudentCourse.teacher_id == Teacher.teacher_id
        ).join(
            Grade, and_(
                StudentCourse.grade == Student.grade,
                StudentCourse.class_ == Student.class_,
                Course.course_name == Grade.subject
            )
        ).join(
            Student, and_(
                Student.grade == StudentCourse.grade,
                Student.class_ == StudentCourse.class_
            )
        ).filter(
            Student.student_id == student_id
        ).all()
        
        # 转换结果格式，确保与预期一致
        formatted_result = []
        for day_of_week, period, subject, teacher, score in schedule_grades:
            formatted_result.append((day_of_week, period, subject, teacher, score))
        
        return formatted_result
    
    @staticmethod
    def get_class_schedule_grades(class_name, grade):
        """获取班级课程安排和成绩"""
        # 获取班级课程安排和成绩
        from sqlalchemy import and_
        schedule_grades = db.session.query(
            StudentCourse.day_of_week,
            StudentCourse.period,
            Course.course_name,
            Teacher.name,
            Grade.score
        ).join(
            Course, StudentCourse.course_code == Course.course_code
        ).join(
            Teacher, StudentCourse.teacher_id == Teacher.teacher_id
        ).join(
            Student, and_(
                Student.grade == StudentCourse.grade,
                Student.class_ == StudentCourse.class_
            )
        ).join(
            Grade, and_(
                Student.student_id == Grade.student_id,
                Course.course_name == Grade.subject
            )
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade
        ).all()
        
        # 转换结果格式，确保与预期一致
        formatted_result = []
        for day_of_week, period, subject, teacher, score in schedule_grades:
            formatted_result.append((day_of_week, period, subject, teacher, score))
        
        return formatted_result
