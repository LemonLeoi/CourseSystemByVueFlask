from ..models import Grade, Student, Exam, Teacher, TeacherCourse, StudentCourse, Course, GradeSettings
from .. import db
import logging

# 配置日志
logger = logging.getLogger(__name__)

class GradeDataAccess:
    # 缓存百分比规则设置，有效期5分钟
    _cached_percentage_rules = None
    _cache_timestamp = None
    _cache_expire_seconds = 300  # 5分钟缓存
    
    @staticmethod
    def _get_cached_percentage_rules():
        """获取缓存的百分比规则，如果缓存过期则返回None"""
        import time
        if GradeDataAccess._cached_percentage_rules is not None:
            if GradeDataAccess._cache_timestamp is not None:
                if (time.time() - GradeDataAccess._cache_timestamp) < GradeDataAccess._cache_expire_seconds:
                    return GradeDataAccess._cached_percentage_rules
        return None
    
    @staticmethod
    def _set_cached_percentage_rules(rules):
        """设置百分比规则缓存"""
        import time
        GradeDataAccess._cached_percentage_rules = rules
        GradeDataAccess._cache_timestamp = time.time()
    
    @staticmethod
    def _clear_percentage_rules_cache():
        """清除百分比规则缓存"""
        GradeDataAccess._cached_percentage_rules = None
        GradeDataAccess._cache_timestamp = None
    
    @staticmethod
    def get_percentage_rules():
        """
        从数据库动态获取百分比规则设置
        
        Returns:
            dict: 包含百分比规则的字典，键为规则名称，值为规则值
                  包含以下字段: percentage_rule_a, percentage_rule_b, 
                  percentage_rule_c, percentage_rule_d, percentage_rule_e
        
        Raises:
            Exception: 当数据库查询失败时抛出异常
        """
        # 先检查缓存
        cached_rules = GradeDataAccess._get_cached_percentage_rules()
        if cached_rules is not None:
            logger.debug("使用缓存的百分比规则")
            return cached_rules
        
        try:
            # 查询数据库获取最新设置
            settings = GradeSettings.query.first()
            
            if settings is None:
                # 如果没有找到设置记录，使用默认值
                logger.warning("grade_settings表中未找到记录，使用默认值")
                rules = {
                    'percentage_rule_a': 90,
                    'percentage_rule_b': 85,
                    'percentage_rule_c': 75,
                    'percentage_rule_d': 60,
                    'percentage_rule_e': 50
                }
            else:
                # 从数据库获取值，缺失字段使用默认值
                rules = {
                    'percentage_rule_a': GradeDataAccess._validate_percentage_value(
                        getattr(settings, 'percentage_rule_a', None), 90, 'percentage_rule_a'
                    ),
                    'percentage_rule_b': GradeDataAccess._validate_percentage_value(
                        getattr(settings, 'percentage_rule_b', None), 85, 'percentage_rule_b'
                    ),
                    'percentage_rule_c': GradeDataAccess._validate_percentage_value(
                        getattr(settings, 'percentage_rule_c', None), 75, 'percentage_rule_c'
                    ),
                    'percentage_rule_d': GradeDataAccess._validate_percentage_value(
                        getattr(settings, 'percentage_rule_d', None), 60, 'percentage_rule_d'
                    ),
                    'percentage_rule_e': GradeDataAccess._validate_percentage_value(
                        getattr(settings, 'percentage_rule_e', None), 50, 'percentage_rule_e'
                    )
                }
            
            # 设置缓存
            GradeDataAccess._set_cached_percentage_rules(rules)
            logger.info("成功获取百分比规则: %s", rules)
            
            return rules
            
        except Exception as e:
            logger.error("获取百分比规则失败: %s", str(e))
            # 返回默认值作为降级方案
            return {
                'percentage_rule_a': 90,
                'percentage_rule_b': 85,
                'percentage_rule_c': 75,
                'percentage_rule_d': 60,
                'percentage_rule_e': 50
            }
    
    @staticmethod
    def _validate_percentage_value(value, default, field_name):
        """
        验证百分比规则值的有效性
        
        Args:
            value: 待验证的值
            default: 默认值
            field_name: 字段名称，用于日志记录
        
        Returns:
            float: 验证后的有效百分比值
        """
        # 检查值是否存在
        if value is None:
            logger.warning("字段 %s 为None，使用默认值 %d", field_name, default)
            return default
        
        # 尝试转换为数值类型
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            logger.warning("字段 %s 值 %s 不是有效数值，使用默认值 %d", field_name, str(value), default)
            return default
        
        # 验证数值范围（0-100）
        if num_value < 0 or num_value > 100:
            logger.warning("字段 %s 值 %.2f 超出有效范围(0-100)，使用默认值 %d", field_name, num_value, default)
            return default
        
        return num_value
    
    @staticmethod
    def refresh_percentage_rules():
        """
        强制刷新百分比规则缓存，从数据库重新获取最新值
        
        Returns:
            dict: 最新的百分比规则
        """
        GradeDataAccess._clear_percentage_rules_cache()
        return GradeDataAccess.get_percentage_rules()
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
            subject: 学科名称（可选，不指定时计算综合平均分）
            exam_code: 考试代码（可选）
            
        Returns:
            dict: 班级统计数据
        """
        from ..models import Grade, Student
        import re
        
        # 从class_name中提取数字部分
        match = re.search(r'(\d+)', class_name)
        class_num = int(match.group(1)) if match else 1
        
        if subject:
            # ====================
            # 情况1：指定了学科
            # ====================
            # 计算该学科的平均分（这部分是正确的）
            query = db.session.query(
                Grade,
                Student
            ).join(
                Student, Grade.student_id == Student.student_id
            ).filter(
                Student.class_ == class_name,
                Student.grade == grade,
                Grade.subject == subject
            )
            
            if exam_code and exam_code != 'all':
                query = query.filter(Grade.exam_code == exam_code)
            
            grades = query.all()
            
            if not grades:
                return None
            
            # 按学生去重，每个学生只保留该学科的最高成绩
            student_data = {}
            for grade_record, student in grades:
                student_id = student.student_id
                if student_id not in student_data or grade_record.score > student_data[student_id]['score']:
                    student_data[student_id] = {
                        'score': grade_record.score,
                        'subject': grade_record.subject
                    }
            
            scores = [data['score'] for data in student_data.values() if data['score'] is not None]
            full_score = 150 if subject in ['语文', '数学', '英语'] else 100
        elif exam_code and exam_code != 'all':
            # ====================
            # 情况2：指定了考试但没有指定学科
            # ====================
            # 计算该考试中所有学科的平均分
            # 策略：对每个学生计算其在该考试中所有学科的平均分，然后再计算全班学生的平均分
            query = db.session.query(
                Grade,
                Student
            ).join(
                Student, Grade.student_id == Student.student_id
            ).filter(
                Student.class_ == class_name,
                Student.grade == grade,
                Grade.exam_code == exam_code
            )
            
            grades = query.all()
            
            if not grades:
                return None
            
            # 按学生分组，计算每个学生的平均分
            student_scores = {}
            for grade_record, student in grades:
                student_id = student.student_id
                if student_id not in student_scores:
                    student_scores[student_id] = []
                if grade_record.score is not None:
                    student_scores[student_id].append(grade_record.score)
            
            # 计算每个学生的平均分，然后计算这些平均分的平均值
            scores = []
            for student_score_list in student_scores.values():
                if student_score_list:
                    avg_score_for_student = sum(student_score_list) / len(student_score_list)
                    scores.append(avg_score_for_student)
            full_score = 100  # 综合情况默认满分100
        else:
            # ====================
            # 情况3：既没有指定学科也没有指定考试
            # ====================
            # 计算综合平均分
            # 策略：按学科分别计算平均分，然后再计算这些学科平均分的平均值
            # 这样可以保证每个学科的权重相同，不会因为某个学科记录多而被过度影响
            
            subject_stats = GradeDataAccess.get_class_subject_statistics(class_name, grade)
            
            if not subject_stats:
                return None
            
            # 综合平均分是各学科平均分的平均
            subject_avg_scores = [stats['average_score'] for stats in subject_stats.values()]
            avg_score = sum(subject_avg_scores) / len(subject_avg_scores)
            
            # 为了计算其他统计指标（如标准差、分布等），我们需要所有学科的分数
            all_scores = []
            for subj, stats in subject_stats.items():
                # 查询该学科的所有学生成绩
                subj_grades_with_student = db.session.query(
                    Grade.student_id,
                    Grade.score
                ).join(
                    Student, Grade.student_id == Student.student_id
                ).filter(
                    Student.class_ == class_name,
                    Student.grade == grade,
                    Grade.subject == subj
                ).all()
                
                # 去重，每个学生只保留该学科的最高分
                student_max_scores = {}
                for student_id, score in subj_grades_with_student:
                    if score is not None:
                        if student_id not in student_max_scores or score > student_max_scores[student_id]:
                            student_max_scores[student_id] = score
                
                all_scores.extend(student_max_scores.values())
            
            scores = all_scores
            full_score = 100  # 综合情况默认满分100
        
        if not scores:
            return None
        
        # ====================
        # 计算统计数据
        # ====================
        n = len(scores)
        avg_score = sum(scores) / n if (subject or exam_code) else sum(subject_avg_scores) / len(subject_avg_scores)
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
        
        # 从数据库动态获取百分比规则设置
        rules = GradeDataAccess.get_percentage_rules()
        
        # 使用动态获取的percentage rule计算及格率和优秀率
        excellent_threshold = (rules['percentage_rule_a'] / 100) * full_score
        pass_threshold = (rules['percentage_rule_d'] / 100) * full_score
        good_threshold = (rules['percentage_rule_b'] / 100) * full_score
        average_threshold = (rules['percentage_rule_c'] / 100) * full_score
        
        excellent_count = sum(1 for s in scores if s >= excellent_threshold)
        pass_count = sum(1 for s in scores if s >= pass_threshold)
        
        excellent_rate = (excellent_count / n) * 100
        pass_rate = (pass_count / n) * 100
        
        # 计算分数分布
        distribution = {
            'excellent': excellent_count,
            'good': sum(1 for s in scores if good_threshold <= s < excellent_threshold),
            'average': sum(1 for s in scores if average_threshold <= s < good_threshold),
            'pass': sum(1 for s in scores if pass_threshold <= s < average_threshold),
            'fail': sum(1 for s in scores if s < pass_threshold)
        }
        
        # 获取教师信息（简单模拟）
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
    
    @staticmethod
    def get_subject_full_score(subject):
        """获取学科满分值
        
        Args:
            subject: 学科名称
            
        Returns:
            int: 该学科的满分值，默认为100
        """
        from ..models import SubjectConfig
        
        config = SubjectConfig.query.filter_by(subject_name=subject).first()
        if config and config.enabled:
            return config.full_score
        
        # 如果数据库中没有配置，返回默认值
        if subject in ['语文', '数学', '英语']:
            return 150
        return 100
    
    @staticmethod
    def calculate_score_rate(score, subject):
        """计算得分率（标准化分数）
        
        Args:
            score: 原始分数
            subject: 学科名称
            
        Returns:
            float: 得分率（0-100之间的百分比）
        """
        full_score = GradeDataAccess.get_subject_full_score(subject)
        if full_score == 0:
            return 0.0
        return round((score / full_score) * 100, 2)
    
    @staticmethod
    def calculate_period_statistics(class_name, grade):
        """
        按课程节次统计成绩数据
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            
        Returns:
            list: 按节次分组的统计数据，每个元素包含period, average_score, student_count, score_impact
        """
        from sqlalchemy import func, and_
        
        try:
            # 先获取该班级所有课程安排和学生
            course_schedules = db.session.query(
                StudentCourse.period,
                StudentCourse.course_code
            ).filter(
                StudentCourse.grade == grade,
                StudentCourse.class_ == class_name
            ).all()
            
            students = Student.query.filter(Student.grade == grade, Student.class_ == class_name).all()
            
            if not course_schedules or not students:
                return []
            
            # 建立课程代码到课程名称的映射
            course_code_to_name = {}
            for course_code in set(c.course_code for c in course_schedules):
                course = Course.query.filter_by(course_code=course_code).first()
                if course:
                    # 提取课程的基础名（如"语文高一上" -> "语文"）
                    base_name = course.course_name
                    # 查找年级关键词，然后取前面部分
                    for keyword in ['高一', '高二', '高三']:
                        if keyword in base_name:
                            idx = base_name.find(keyword)
                            base_name = base_name[:idx]
                            break
                    course_code_to_name[course_code] = base_name
            
            # 获取学生成绩
            student_grades = {}
            for student in students:
                grades = Grade.query.filter_by(student_id=student.student_id).all()
                for g in grades:
                    if g.score is not None:
                        if student.student_id not in student_grades:
                            student_grades[student.student_id] = {}
                        student_grades[student.student_id][g.subject] = g.score
            
            # 匹配课程安排和成绩
            period_data = {}
            period_scores = []
            
            for period, course_code in course_schedules:
                subject_name = course_code_to_name.get(course_code)
                if subject_name:
                    # 查找有这个科目成绩的学生
                    for student_id, subject_scores in student_grades.items():
                        if subject_name in subject_scores:
                            if period not in period_data:
                                period_data[period] = []
                            period_data[period].append(subject_scores[subject_name])
                            period_scores.append(subject_scores[subject_name])
            
            if not period_scores:
                return []
            
            # 计算整体平均分作为基准
            overall_avg = sum(period_scores) / len(period_scores)
            
            # 生成结果列表
            result = []
            for period, scores in sorted(period_data.items()):
                if scores:
                    avg_score = sum(scores) / len(scores)
                    score_impact = avg_score - overall_avg
                
                    result.append({
                        'period': f"第{period}节",
                        'average_score': round(avg_score, 2),
                        'student_count': len(scores),
                        'score_impact': round(score_impact, 2),
                        'description': f"第{period}节平均成绩"
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"计算节次统计失败: {str(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            return []
    
    @staticmethod
    def calculate_double_class_statistics(class_name, grade):
        """
        分析连堂课对成绩的影响
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            
        Returns:
            list: 连堂课统计数据，每个元素包含double_class, average_score, score_impact
        """
        from sqlalchemy import func, and_
        
        try:
            # 先获取该班级所有课程安排和学生
            course_schedules = db.session.query(
                StudentCourse.day_of_week,
                StudentCourse.period,
                StudentCourse.course_code
            ).filter(
                StudentCourse.grade == grade,
                StudentCourse.class_ == class_name
            ).order_by(
                StudentCourse.day_of_week,
                StudentCourse.period
            ).all()
            
            students = Student.query.filter(Student.grade == grade, Student.class_ == class_name).all()
            
            if not course_schedules or not students:
                return []
            
            # 建立课程代码到课程名称的映射
            course_code_to_name = {}
            for course_code in set(c.course_code for c in course_schedules):
                course = Course.query.filter_by(course_code=course_code).first()
                if course:
                    # 提取课程的基础名（如"语文高一上" -> "语文"）
                    base_name = course.course_name
                    # 查找年级关键词，然后取前面部分
                    for keyword in ['高一', '高二', '高三']:
                        if keyword in base_name:
                            idx = base_name.find(keyword)
                            base_name = base_name[:idx]
                            break
                    course_code_to_name[course_code] = base_name
            
            # 获取学生成绩
            student_grades = {}
            for student in students:
                grades = Grade.query.filter_by(student_id=student.student_id).all()
                for g in grades:
                    if g.score is not None:
                        if student.student_id not in student_grades:
                            student_grades[student.student_id] = {}
                        student_grades[student.student_id][g.subject] = g.score
            
            # 匹配课程安排和成绩
            day_course_scores = {}
            all_scores = []
            
            for day, period, course_code in course_schedules:
                subject_name = course_code_to_name.get(course_code)
                if subject_name:
                    # 查找有这个科目成绩的学生
                    for student_id, subject_scores in student_grades.items():
                        if subject_name in subject_scores:
                            key = (day, subject_name)
                            if key not in day_course_scores:
                                day_course_scores[key] = {'periods': [], 'scores': []}
                            day_course_scores[key]['periods'].append(period)
                            day_course_scores[key]['scores'].append(subject_scores[subject_name])
                            all_scores.append(subject_scores[subject_name])
            
            if not all_scores:
                return []
            
            # 统计不同连堂数量的成绩
            double_class_data = {}
            for key, data in day_course_scores.items():
                # 计算连堂节数（连续的节次）
                periods = sorted(data['periods'])
                consecutive_count = 1
                max_consecutive = 1
                for i in range(1, len(periods)):
                    if periods[i] == periods[i-1] + 1:
                        consecutive_count += 1
                        max_consecutive = max(max_consecutive, consecutive_count)
                    else:
                        consecutive_count = 1
                
                double_class_count = max_consecutive
                
                if double_class_count not in double_class_data:
                    double_class_data[double_class_count] = []
                double_class_data[double_class_count].extend(data['scores'])
            
            # 计算整体平均分
            overall_avg = sum(all_scores) / len(all_scores)
            
            # 生成结果
            result = []
            for double_class, scores in sorted(double_class_data.items()):
                avg_score = sum(scores) / len(scores)
                score_impact = avg_score - overall_avg
                
                result.append({
                    'double_class': f"{double_class}节",
                    'average_score': round(avg_score, 2),
                    'student_count': len(scores),
                    'score_impact': round(score_impact, 2),
                    'description': f"{double_class}节连堂"
                })
            
            return result
            
        except Exception as e:
            logger.error(f"计算连堂统计失败: {str(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            return []
    
    @staticmethod
    def calculate_gender_statistics(class_name, grade):
        """
        按性别和学科统计成绩差异
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            
        Returns:
            list: 性别×学科的统计数据
        """
        from sqlalchemy import func, and_
        
        try:
            # 查询学生性别、科目和成绩
            gender_subject_scores = db.session.query(
                Student.gender,
                Grade.subject,
                Grade.score
            ).join(
                Student, Grade.student_id == Student.student_id
            ).filter(
                Student.class_ == class_name,
                Student.grade == grade,
                Student.gender.isnot(None),
                Grade.score.isnot(None)
            ).all()
            
            if not gender_subject_scores:
                return []
            
            # 按性别和科目分组
            subject_gender_data = {}
            for gender, subject, score in gender_subject_scores:
                if subject not in subject_gender_data:
                    subject_gender_data[subject] = {'男': [], '女': []}
                if gender in subject_gender_data[subject]:
                    subject_gender_data[subject][gender].append(score)
            
            # 生成结果
            result = []
            for subject, gender_scores in subject_gender_data.items():
                male_scores = gender_scores['男']
                female_scores = gender_scores['女']
                
                male_avg = sum(male_scores) / len(male_scores) if male_scores else None
                female_avg = sum(female_scores) / len(female_scores) if female_scores else None
                
                result.append({
                    'subject': subject,
                    'male_avg': round(male_avg, 2) if male_scores else None,
                    'female_avg': round(female_avg, 2) if female_scores else None,
                    'diff': round(male_avg - female_avg, 2) if (male_scores and female_scores) else None,
                    'male_count': len(male_scores),
                    'female_count': len(female_scores)
                })
            
            return result
            
        except Exception as e:
            logger.error(f"计算性别统计失败: {str(e)}")
            return []
    
    @staticmethod
    def get_schedule_grade_analysis(class_name, grade):
        """
        获取排课和成绩联合分析数据，用于path-1分析
        
        Args:
            class_name: 班级名称（如'1班'）
            grade: 年级（如'高一'）
            
        Returns:
            dict: 包含day_of_week_scores, period_scores等分析数据
        """
        from sqlalchemy import func, and_
        
        try:
            # 先获取该班级所有课程安排和学生
            course_schedules = db.session.query(
                StudentCourse.day_of_week,
                StudentCourse.period,
                StudentCourse.course_code
            ).filter(
                StudentCourse.grade == grade,
                StudentCourse.class_ == class_name
            ).all()
            
            students = Student.query.filter(Student.grade == grade, Student.class_ == class_name).all()
            
            if not course_schedules or not students:
                return {'day_of_week_scores': {}, 'period_scores': {}}
            
            # 建立课程代码到课程名称的映射
            course_code_to_name = {}
            for course_code in set(c.course_code for c in course_schedules):
                course = Course.query.filter_by(course_code=course_code).first()
                if course:
                    # 提取课程的基础名（如"语文高一上" -> "语文"）
                    base_name = course.course_name
                    # 查找年级关键词，然后取前面部分
                    for keyword in ['高一', '高二', '高三']:
                        if keyword in base_name:
                            idx = base_name.find(keyword)
                            base_name = base_name[:idx]
                            break
                    course_code_to_name[course_code] = base_name
            
            # 获取学生成绩
            student_grades = {}
            for student in students:
                grades = Grade.query.filter_by(student_id=student.student_id).all()
                for g in grades:
                    if g.score is not None:
                        if student.student_id not in student_grades:
                            student_grades[student.student_id] = {}
                        student_grades[student.student_id][g.subject] = g.score
            
            # 匹配课程安排和成绩
            day_scores = {}
            period_scores = {}
            
            for day, period, course_code in course_schedules:
                subject_name = course_code_to_name.get(course_code)
                if subject_name:
                    # 查找有这个科目成绩的学生
                    for student_id, subject_scores in student_grades.items():
                        if subject_name in subject_scores:
                            # 按星期几分组
                            if day not in day_scores:
                                day_scores[day] = []
                            day_scores[day].append(subject_scores[subject_name])
                            
                            # 按节次分组
                            if period not in period_scores:
                                period_scores[period] = []
                            period_scores[period].append(subject_scores[subject_name])
            
            # 计算统计数据
            day_of_week_stats = {}
            day_names = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}
            for day, scores in day_scores.items():
                day_name = day_names.get(day, f"周{day}")
                day_of_week_stats[day] = {
                    'day_name': day_name,
                    'average_score': round(sum(scores) / len(scores), 2),
                    'count': len(scores)
                }
            
            period_stats = {}
            for period, scores in period_scores.items():
                period_stats[period] = {
                    'average_score': round(sum(scores) / len(scores), 2),
                    'count': len(scores)
                }
            
            return {
                'day_of_week_scores': day_of_week_stats,
                'period_scores': period_stats
            }
            
        except Exception as e:
            logger.error(f"获取排课成绩分析失败: {str(e)}")
            return {'day_of_week_scores': {}, 'period_scores': {}}

