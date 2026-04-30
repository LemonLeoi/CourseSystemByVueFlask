from ..models import Grade, Student, Exam, Teacher, TeacherCourse, StudentCourse, Course
from .. import db

class GradeDataAccess:
    @staticmethod
    def get_student_grades(student_id):
        """获取学生个人成绩"""
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return None, None
        
        grades = db.session.query(
            Exam.exam_name,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Grade.student_id == student_id
        ).all()
        
        formatted_grades = []
        if grades:
            for grade in grades:
                formatted_grades.append((
                    grade[0],  # exam_name
                    grade[1],  # academic_year
                    grade[2],  # semester
                    student.grade,
                    grade[3],  # exam_type
                    grade[4],  # subject
                    grade[5],  # score
                    grade[6]   # grade_level
                ))
        else:
            # 如果没有找到考试记录，使用默认值
            grades = db.session.query(
                Grade.subject,
                Grade.score,
                Grade.grade_level
            ).filter(
                Grade.student_id == student_id
            ).all()
            for grade in grades:
                formatted_grades.append((
                    '未知考试',
                    '2024-2025学年',
                    '第一学期',
                    student.grade,
                    '期中考试',
                    grade[0],
                    grade[1],
                    grade[2]
                ))
        
        student_info = (student.name, student.gender, student.class_, student.grade)
        return student_info, formatted_grades
    
    @staticmethod
    def get_class_average(student_class, student_grade):
        """获取班级平均成绩"""
        class_avgs = db.session.query(
            Grade.subject,
            db.func.avg(Grade.score).label('avg_score')
        ).join(
            Student, Grade.student_id == Student.student_id
        ).filter(
            Student.class_ == student_class,
            Student.grade == student_grade
        ).group_by(
            Grade.subject
        ).all()
        
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
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return []
        
        # 获取班级的课程安排
        from sqlalchemy import and_, func
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
        ).outerjoin(
            Grade, and_(
                Grade.student_id == student_id,
                # 使用子字符串匹配科目名称，如"语文高一上"匹配"语文"
                func.substr(Course.course_name, 1, 2) == Grade.subject
            )
        ).filter(
            StudentCourse.grade == student.grade,
            StudentCourse.class_ == student.class_
        ).all()
        
        formatted_result = []
        for day_of_week, period, subject, teacher, score in schedule_grades:
            formatted_result.append((day_of_week, period, subject, teacher, score))
        
        return formatted_result
    
    @staticmethod
    def get_class_schedule_grades(class_name, grade):
        """获取班级课程安排和成绩"""
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
        
        formatted_result = []
        for day_of_week, period, subject, teacher, score in schedule_grades:
            formatted_result.append((day_of_week, period, subject, teacher, score))
        
        return formatted_result
    
    @staticmethod
    def delete_student_grade(student_id, exam_code, subject):
        """删除学生指定考试的指定科目成绩"""
        try:
            grade = Grade.query.filter_by(
                student_id=student_id,
                exam_code=exam_code,
                subject=subject
            ).first()
            
            if grade:
                db.session.delete(grade)
                db.session.commit()
                return True, "删除成功"
            else:
                return False, "成绩记录不存在"
        except Exception as e:
            db.session.rollback()
            return False, f"删除失败: {str(e)}"
    
    @staticmethod
    def delete_student_exam_grades(student_id, exam_code):
        """删除学生指定考试的所有科目成绩"""
        try:
            grades = Grade.query.filter_by(
                student_id=student_id,
                exam_code=exam_code
            ).all()
            
            if grades:
                for grade in grades:
                    db.session.delete(grade)
                db.session.commit()
                return True, f"成功删除 {len(grades)} 条成绩记录"
            else:
                return False, "没有找到该考试的成绩记录"
        except Exception as e:
            db.session.rollback()
            return False, f"删除失败: {str(e)}"
    
    @staticmethod
    def delete_exam_all_grades(exam_code):
        """删除指定考试的所有学生成绩"""
        try:
            grades = Grade.query.filter_by(exam_code=exam_code).all()
            
            if grades:
                count = len(grades)
                for grade in grades:
                    db.session.delete(grade)
                db.session.commit()
                return True, f"成功删除 {count} 条成绩记录"
            else:
                return False, "没有找到该考试的成绩记录"
        except Exception as e:
            db.session.rollback()
            return False, f"删除失败: {str(e)}"
    
    @staticmethod
    def get_class_teachers(class_name, grade):
        """获取班级的所有任课教师"""
        from sqlalchemy import distinct
        teachers = db.session.query(
            distinct(Teacher.teacher_id),
            Teacher.name,
            Teacher.title,
            Course.course_name
        ).join(
            TeacherCourse, Teacher.teacher_id == TeacherCourse.teacher_id
        ).join(
            Course, TeacherCourse.course_code == Course.course_code
        ).filter(
            TeacherCourse.class_ == class_name,
            TeacherCourse.grade == grade
        ).all()
        
        result = []
        for teacher_id, name, title, course_name in teachers:
            result.append({
                'teacher_id': teacher_id,
                'name': name,
                'title': title,
                'subject': course_name
            })
        
        return result
    
    @staticmethod
    def get_class_grades_by_exam(class_name, grade, exam_code):
        """获取指定考试的班级所有成绩"""
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
            Student.grade == grade,
            Grade.exam_code == exam_code
        ).order_by(
            Grade.student_id,
            Grade.subject
        ).all()
        
        return grades
    
    @staticmethod
    def get_class_subject_grades_by_exam(class_name, grade, subject, exam_code):
        """获取指定考试的班级指定科目成绩"""
        grades = db.session.query(
            Grade.student_id,
            Student.name,
            Grade.score
        ).join(
            Student, Grade.student_id == Student.student_id
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade,
            Grade.subject == subject,
            Grade.exam_code == exam_code
        ).all()
        
        return grades
    
    @staticmethod
    def get_student_grades_by_exam(student_id, exam_code):
        """获取指定考试的学生成绩"""
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return None, None
        
        grades = db.session.query(
            Exam.exam_name,
            Exam.academic_year,
            Exam.semester,
            Exam.exam_type,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Grade.student_id == student_id,
            Grade.exam_code == exam_code
        ).all()
        
        formatted_grades = []
        if grades:
            for grade in grades:
                formatted_grades.append((
                    grade[0],  # exam_name
                    grade[1],  # academic_year
                    grade[2],  # semester
                    student.grade,
                    grade[3],  # exam_type
                    grade[4],  # subject
                    grade[5],  # score
                    grade[6]   # grade_level
                ))
        
        student_info = (student.name, student.gender, student.class_, student.grade)
        return student_info, formatted_grades
    
    @staticmethod
    def get_exam_list():
        """获取所有考试列表"""
        exams = Exam.query.all()
        
        result = []
        for exam in exams:
            result.append({
                'exam_code': exam.exam_code,
                'exam_name': exam.exam_name,
                'exam_type': exam.exam_type,
                'grade': exam.grade,
                'academic_year': exam.academic_year,
                'semester': exam.semester,
                'start_date': exam.start_date.isoformat() if exam.start_date else None,
                'end_date': exam.end_date.isoformat() if exam.end_date else None,
                'status': exam.status
            })
        
        return result    
    
