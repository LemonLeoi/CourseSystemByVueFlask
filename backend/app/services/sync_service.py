from .. import db
from ..models import CourseSchedule, TeacherCourse, StudentCourse

class SyncService:
    @staticmethod
    def sync_to_teacher_courses(schedule):
        if not schedule.teacher_id:
            return None
        
        grade = schedule.class_id[:2]
        class_ = schedule.class_id[2:] if len(schedule.class_id) > 2 else ''
        
        old_records = TeacherCourse.query.filter(
            TeacherCourse.teacher_id == schedule.teacher_id,
            TeacherCourse.grade == grade,
            TeacherCourse.class_ == class_,
            TeacherCourse.day_of_week == schedule.day_of_week,
            TeacherCourse.period >= schedule.period_start,
            TeacherCourse.period <= schedule.period_end
        ).all()
        
        for record in old_records:
            db.session.delete(record)
        
        for period in range(schedule.period_start, schedule.period_end + 1):
            new_record = TeacherCourse(
                teacher_id=schedule.teacher_id,
                course_code=schedule.course_code,
                grade=grade,
                class_=class_,
                day_of_week=schedule.day_of_week,
                period=period,
                classroom=schedule.classroom_id or '',
                status='active'
            )
            db.session.add(new_record)
        
        db.session.commit()
        return True
    
    @staticmethod
    def sync_to_student_courses(schedule):
        grade = schedule.class_id[:2]
        class_ = schedule.class_id[2:] if len(schedule.class_id) > 2 else ''
        
        old_records = StudentCourse.query.filter(
            StudentCourse.grade == grade,
            StudentCourse.class_ == class_,
            StudentCourse.day_of_week == schedule.day_of_week,
            StudentCourse.period >= schedule.period_start,
            StudentCourse.period <= schedule.period_end
        ).all()
        
        for record in old_records:
            db.session.delete(record)
        
        for period in range(schedule.period_start, schedule.period_end + 1):
            new_record = StudentCourse(
                grade=grade,
                class_=class_,
                course_code=schedule.course_code,
                teacher_id=schedule.teacher_id,
                day_of_week=schedule.day_of_week,
                period=period,
                classroom=schedule.classroom_id or '',
                room_id=schedule.classroom_id,
                status='active'
            )
            db.session.add(new_record)
        
        db.session.commit()
        return True
    
    @staticmethod
    def sync_all():
        schedules = CourseSchedule.query.all()
        for schedule in schedules:
            SyncService.sync_to_teacher_courses(schedule)
            SyncService.sync_to_student_courses(schedule)
        return len(schedules)