from ..models import Grade, Student, Exam
from .. import db

class GradeDataAccess:
    @staticmethod
    def get_student_grades(student_id):
        """获取学生个人成绩"""
        # 获取学生信息
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return None, None
        
        # 获取学生成绩，通过关联查询获取考试信息
        grades = db.session.query(
            Exam.exam_name,
            Exam.academic_year,
            Exam.semester,
            Exam.grade,
            Exam.exam_type,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Grade, Grade.exam_id == Exam.id
        ).filter(
            Grade.student_id == student_id
        ).order_by(
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type
        ).all()
        
        student_info = (student.name, student.gender, student.class_, student.grade)
        return student_info, grades
    
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
            Exam, Grade.exam_id == Exam.id
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
            Exam, Grade.exam_id == Exam.id
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
            Exam, Grade.exam_id == Exam.id
        ).filter(
            Student.grade == grade
        ).order_by(
            Student.class_,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type
        ).all()
        
        return grades
