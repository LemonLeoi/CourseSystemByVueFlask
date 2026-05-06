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
            Exam.start_date,
            Grade.subject,
            Grade.score,
            Grade.grade_level
        ).join(
            Exam, Grade.exam_code == Exam.exam_code
        ).filter(
            Grade.student_id == student_id
        ).order_by(
            Exam.start_date.asc()
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
                    grade[5],  # subject (注意：grade[4] 是 start_date)
                    grade[6],  # score
                    grade[7]   # grade_level
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
            Exam.start_date.asc()
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
            Exam.start_date.asc()
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
        """获取年级指定科目的成绩（按学生去重，取每个学生该科目的最高成绩）"""
        from sqlalchemy import func, and_, or_

        subquery = db.session.query(
            Grade.student_id,
            func.max(Grade.score).label('max_score')
        ).filter(
            Grade.subject == subject
        ).group_by(
            Grade.student_id
        ).subquery()

        grades = db.session.query(
            Student.class_,
            subquery.c.max_score
        ).join(
            subquery, Student.student_id == subquery.c.student_id
        ).filter(
            Student.grade == grade
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

    @staticmethod
    def check_duplicate_grades(student_id, exam_code, subject):
        """检查是否存在重复成绩记录"""
        duplicates = Grade.query.filter(
            Grade.student_id == student_id,
            Grade.exam_code == exam_code,
            Grade.subject == subject
        ).all()
        return len(duplicates) > 1, duplicates

    @staticmethod
    def get_grade_statistics():
        """获取成绩数据统计信息，用于数据校验"""
        total_records = Grade.query.count()
        unique_students = db.session.query(db.func.count(db.func.distinct(Grade.student_id))).scalar()
        unique_exams = db.session.query(db.func.count(db.func.distinct(Grade.exam_code))).scalar()
        unique_subjects = db.session.query(db.func.count(db.func.distinct(Grade.subject))).scalar()

        potential_duplicates = db.session.query(
            Grade.student_id,
            Grade.exam_code,
            Grade.subject,
            db.func.count(Grade.student_id).label('count')
        ).group_by(
            Grade.student_id,
            Grade.exam_code,
            Grade.subject
        ).having(
            db.func.count(Grade.student_id) > 1
        ).all()

        return {
            'total_records': total_records,
            'unique_students': unique_students,
            'unique_exams': unique_exams,
            'unique_subjects': unique_subjects,
            'potential_duplicates_count': len(potential_duplicates),
            'potential_duplicates': [
                {
                    'student_id': d[0],
                    'exam_code': d[1],
                    'subject': d[2],
                    'count': d[3]
                } for d in potential_duplicates[:10]
            ]
        }
    
    @staticmethod
    def get_class_subject_statistics(class_name, grade, subject=None):
        """获取班级学科成绩统计（按学生去重，取每个学生该科的最高分）
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            subject: 学科名称（可选，如None则获取所有学科）
        
        Returns:
            dict: 学科统计信息
        """
        # 构建查询，获取每个学生该科的最高分
        from sqlalchemy import func
        
        # 子查询：获取每个学生该科的最高分
        max_score_subq = db.session.query(
            Grade.student_id,
            Grade.subject,
            func.max(Grade.score).label('max_score')
        ).filter(
            (Grade.subject == subject) if subject else True
        ).group_by(
            Grade.student_id,
            Grade.subject
        ).subquery()
        
        # 连接学生表，获取对应班级的学生
        query = db.session.query(
            max_score_subq.c.subject,
            max_score_subq.c.max_score
        ).join(
            Student, Student.student_id == max_score_subq.c.student_id
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade
        )
        
        results = query.all()
        
        # 按学科分组统计
        subject_stats = {}
        for subj, score in results:
            if subj not in subject_stats:
                subject_stats[subj] = []
            subject_stats[subj].append(score)
        
        # 计算各学科的统计指标
        stats_result = {}
        for subj, scores in subject_stats.items():
            n = len(scores)
            if n == 0:
                continue
            
            avg_score = sum(scores) / n
            max_score = max(scores)
            min_score = min(scores)
            
            # 计算中位数
            sorted_scores = sorted(scores)
            if n % 2 == 1:
                median = sorted_scores[n // 2]
            else:
                median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
            
            # 计算标准差
            variance = sum((s - avg_score) ** 2 for s in scores) / n
            std_dev = variance ** 0.5
            
            # 计算优秀率和及格率（优秀>=90，及格>=60）
            excellent_count = sum(1 for s in scores if s >= 90)
            pass_count = sum(1 for s in scores if s >= 60)
            excellent_rate = (excellent_count / n) * 100
            pass_rate = (pass_count / n) * 100
            
            # 计算分数分布
            distribution = {
                'excellent': excellent_count,
                'good': sum(1 for s in scores if 80 <= s < 90),
                'average': sum(1 for s in scores if 70 <= s < 80),
                'pass': sum(1 for s in scores if 60 <= s < 70),
                'fail': sum(1 for s in scores if s < 60)
            }
            
            stats_result[subj] = {
                'subject': subj,
                'average_score': round(avg_score, 2),
                'excellent_rate': round(excellent_rate, 2),
                'pass_rate': round(pass_rate, 2),
                'std_deviation': round(std_dev, 2),
                'max_score': max_score,
                'min_score': min_score,
                'median': round(median, 2),
                'distribution': distribution,
                'student_count': n
            }
        
        return stats_result
    
    @staticmethod
    def get_single_class_statistics(class_name, grade, subject=None, exam_code=None):
        """获取单个班级的详细统计数据
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            subject: 学科名称（可选）
            exam_code: 考试代码（可选）
            
        Returns:
            dict: 班级统计数据
        """
        from ..models import Grade, Student
        import re
        
        # 从class_name中提取数字部分
        match = re.search(r'(\d+)', class_name)
        class_num = int(match.group(1)) if match else 1
        
        # 构建查询
        query = db.session.query(
            Grade,
            Student
        ).join(
            Student, Grade.student_id == Student.student_id
        ).filter(
            Student.class_ == class_name,
            Student.grade == grade
        )
        
        # 如果指定了考试代码
        if exam_code and exam_code != 'all':
            query = query.filter(Grade.exam_code == exam_code)
        
        # 如果指定了学科
        if subject:
            query = query.filter(Grade.subject == subject)
        
        grades = query.all()
        
        if not grades:
            return None
        
        # 按学生去重，每个学生只保留最高成绩
        student_data = {}
        for grade_record, student in grades:
            student_id = student.student_id
            if student_id not in student_data or grade_record.score > student_data[student_id]['score']:
                student_data[student_id] = {
                    'score': grade_record.score,
                    'subject': grade_record.subject
                }
        
        scores = [data['score'] for data in student_data.values() if data['score'] is not None]
        
        if not scores:
            return None
        
        # 计算统计数据
        n = len(scores)
        avg_score = sum(scores) / n
        max_score = max(scores)
        min_score = min(scores)
        
        # 计算中位数
        sorted_scores = sorted(scores)
        if n % 2 == 1:
            median = sorted_scores[n // 2]
        else:
            median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) / 2
        
        # 计算标准差
        variance = sum((s - avg_score) ** 2 for s in scores) / n
        std_dev = variance ** 0.5
        
        # 获取grade settings
        from .grade_settings_data_access import GradeSettingsDataAccess
        settings = GradeSettingsDataAccess.get_settings()
        
        # 确定学科满分和阈值
        full_score = 100
        if subject and subject in ['语文', '数学', '英语']:
            full_score = 150
        elif subject and subject in ['物理', '化学', '生物', '历史', '地理', '政治']:
            full_score = 100
        
        # 使用percentage rule
        excellent_threshold = (settings.percentage_rule_a / 100) * full_score
        pass_threshold = (settings.percentage_rule_d / 100) * full_score
        
        excellent_count = sum(1 for s in scores if s >= excellent_threshold)
        pass_count = sum(1 for s in scores if s >= pass_threshold)
        
        excellent_rate = (excellent_count / n) * 100
        pass_rate = (pass_count / n) * 100
        
        # 计算分数分布
        distribution = {
            'excellent': excellent_count,
            'good': sum(1 for s in scores if (settings.percentage_rule_b / 100 * full_score) <= s < excellent_threshold),
            'average': sum(1 for s in scores if (settings.percentage_rule_c / 100 * full_score) <= s < (settings.percentage_rule_b / 100 * full_score)),
            'pass': sum(1 for s in scores if pass_threshold <= s < (settings.percentage_rule_c / 100 * full_score)),
            'fail': sum(1 for s in scores if s < pass_threshold)
        }
        
        # 获取教师信息（简单模拟，实际需要从数据库获取）
        teacher_group = (class_num - 1) // 2
        teacher_names = {
            0: ('王老师', '教师组1'),
            1: ('李老师', '教师组2'), 
            2: ('张老师', '教师组3')
        }
        teacher_name, group_name = teacher_names.get(teacher_group, ('王老师', '教师组1'))
        
        return {
            'class_id': f"{grade}{class_name}",
            'class_name': f"{grade}{class_name}",
            'grade': grade,
            'teacher_group': group_name,
            'teacher_name': teacher_name,
            'student_count': n,
            'metrics': {
                'average_score': round(avg_score, 2),
                'pass_rate': round(pass_rate, 2),
                'excellent_rate': round(excellent_rate, 2),
                'improvement_rate': 0.0,  # 暂时设为0
                'std_deviation': round(std_dev, 2),
                'median_score': round(median, 2)
            },
            'scores': scores
        }
    
