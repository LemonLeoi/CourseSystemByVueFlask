import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
database_path = os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app.models import StudentCourse, TeacherCourse

class SyncLogger:
    def __init__(self):
        self.log_entries = []
    
    def log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f"[{timestamp}] [{level}] {message}"
        self.log_entries.append(entry)
        print(entry)
    
    def info(self, message):
        self.log("INFO", message)
    
    def success(self, message):
        self.log("SUCCESS", message)
    
    def warning(self, message):
        self.log("WARNING", message)
    
    def error(self, message):
        self.log("ERROR", message)
    
    def save_log(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_entries))
        self.info(f"日志已保存至: {filename}")

def sync_student_courses_to_teacher_courses():
    logger = SyncLogger()
    
    logger.info("========== 开始同步 student_courses 到 teacher_courses ==========")
    
    with app.app_context():
        try:
            total_student_courses = StudentCourse.query.count()
            logger.info(f"student_courses表中共有 {total_student_courses} 条记录")
            
            teacher_courses_before = TeacherCourse.query.count()
            logger.info(f"同步前 teacher_courses表中有 {teacher_courses_before} 条记录")
            
            student_courses = StudentCourse.query.all()
            
            success_count = 0
            skip_count = 0
            update_count = 0
            fail_count = 0
            failed_records = []
            
            for sc in student_courses:
                if not sc.teacher_id:
                    logger.warning(f"跳过记录: 教师ID为空 (grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period})")
                    skip_count += 1
                    continue
                
                try:
                    existing_record = TeacherCourse.query.filter(
                        TeacherCourse.teacher_id == sc.teacher_id,
                        TeacherCourse.grade == sc.grade,
                        TeacherCourse.class_ == sc.class_,
                        TeacherCourse.day_of_week == sc.day_of_week,
                        TeacherCourse.period == sc.period
                    ).first()
                    
                    if existing_record:
                        if (existing_record.course_code == sc.course_code and
                            existing_record.classroom == sc.classroom and
                            existing_record.status == sc.status):
                            logger.info(f"跳过重复记录: teacher_id={sc.teacher_id}, grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period}")
                            skip_count += 1
                        else:
                            existing_record.course_code = sc.course_code
                            existing_record.classroom = sc.classroom
                            existing_record.status = sc.status
                            db.session.commit()
                            logger.info(f"更新记录: teacher_id={sc.teacher_id}, grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period}")
                            update_count += 1
                    else:
                        new_record = TeacherCourse(
                            teacher_id=sc.teacher_id,
                            course_code=sc.course_code,
                            grade=sc.grade,
                            class_=sc.class_,
                            day_of_week=sc.day_of_week,
                            period=sc.period,
                            classroom=sc.classroom,
                            status=sc.status
                        )
                        db.session.add(new_record)
                        db.session.commit()
                        logger.info(f"新增记录: teacher_id={sc.teacher_id}, grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period}")
                        success_count += 1
                    
                except Exception as e:
                    db.session.rollback()
                    error_msg = f"同步失败: teacher_id={sc.teacher_id}, grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period}, 原因: {str(e)}"
                    logger.error(error_msg)
                    failed_records.append({
                        'teacher_id': sc.teacher_id,
                        'grade': sc.grade,
                        'class': sc.class_,
                        'day_of_week': sc.day_of_week,
                        'period': sc.period,
                        'error': str(e)
                    })
                    fail_count += 1
            
            logger.info("========== 同步完成 ==========")
            logger.success(f"成功新增: {success_count} 条")
            logger.success(f"更新记录: {update_count} 条")
            logger.info(f"跳过重复: {skip_count} 条")
            logger.error(f"同步失败: {fail_count} 条")
            
            teacher_courses_after = TeacherCourse.query.count()
            logger.info(f"同步后 teacher_courses表中有 {teacher_courses_after} 条记录")
            logger.info(f"净增加记录数: {teacher_courses_after - teacher_courses_before} 条")
            
            validation_result = validate_sync()
            logger.info("========== 数据验证结果 ==========")
            if validation_result['valid']:
                logger.success("数据验证通过: teacher_courses与student_courses数据一致")
            else:
                logger.error(f"数据验证失败: {validation_result['errors']}")
            
            log_filename = f"sync_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            logger.save_log(os.path.join(os.path.dirname(os.path.abspath(__file__)), log_filename))
            
            return {
                'total_student_courses': total_student_courses,
                'success_count': success_count,
                'update_count': update_count,
                'skip_count': skip_count,
                'fail_count': fail_count,
                'failed_records': failed_records,
                'teacher_courses_before': teacher_courses_before,
                'teacher_courses_after': teacher_courses_after,
                'validation_passed': validation_result['valid']
            }
            
        except Exception as e:
            logger.error(f"同步过程发生严重错误: {str(e)}")
            return {'error': str(e)}

def validate_sync():
    try:
        student_records = StudentCourse.query.filter(StudentCourse.teacher_id.isnot(None)).all()
        
        for sc in student_records:
            tc = TeacherCourse.query.filter(
                TeacherCourse.teacher_id == sc.teacher_id,
                TeacherCourse.grade == sc.grade,
                TeacherCourse.class_ == sc.class_,
                TeacherCourse.day_of_week == sc.day_of_week,
                TeacherCourse.period == sc.period
            ).first()
            
            if not tc:
                return {
                    'valid': False,
                    'errors': [f"teacher_courses中缺少对应记录: teacher_id={sc.teacher_id}, grade={sc.grade}, class={sc.class_}, day={sc.day_of_week}, period={sc.period}"]
                }
            
            if tc.course_code != sc.course_code:
                return {
                    'valid': False,
                    'errors': [f"course_code不匹配: teacher_id={sc.teacher_id}, expected={sc.course_code}, actual={tc.course_code}"]
                }
            
            if tc.classroom != sc.classroom:
                return {
                    'valid': False,
                    'errors': [f"classroom不匹配: teacher_id={sc.teacher_id}, expected={sc.classroom}, actual={tc.classroom}"]
                }
            
            if tc.status != sc.status:
                return {
                    'valid': False,
                    'errors': [f"status不匹配: teacher_id={sc.teacher_id}, expected={sc.status}, actual={tc.status}"]
                }
        
        return {'valid': True, 'errors': []}
    
    except Exception as e:
        return {'valid': False, 'errors': [str(e)]}

if __name__ == '__main__':
    result = sync_student_courses_to_teacher_courses()
    print("\n" + "="*60)
    print("同步结果汇总:")
    print("="*60)
    if 'error' in result:
        print(f"错误: {result['error']}")
    else:
        print(f"student_courses总记录数: {result['total_student_courses']}")
        print(f"成功新增: {result['success_count']} 条")
        print(f"更新记录: {result['update_count']} 条")
        print(f"跳过重复: {result['skip_count']} 条")
        print(f"同步失败: {result['fail_count']} 条")
        print(f"同步前teacher_courses记录数: {result['teacher_courses_before']}")
        print(f"同步后teacher_courses记录数: {result['teacher_courses_after']}")
        print(f"数据验证: {'通过' if result['validation_passed'] else '失败'}")
        print("="*60)