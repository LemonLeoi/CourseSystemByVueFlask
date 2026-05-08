from .. import db
from ..models import CourseSchedule, TeacherCourse, Classroom

class ConflictService:
    @staticmethod
    def check_teacher_conflict(teacher_id, day_of_week, period_start, period_end, exclude_id=None):
        query = CourseSchedule.query.filter(
            CourseSchedule.teacher_id == teacher_id,
            CourseSchedule.day_of_week == day_of_week
        )
        
        if exclude_id:
            query = query.filter(CourseSchedule.id != exclude_id)
        
        conflicts = query.filter(
            db.or_(
                db.and_(
                    CourseSchedule.period_start <= period_start,
                    CourseSchedule.period_end >= period_start
                ),
                db.and_(
                    CourseSchedule.period_start <= period_end,
                    CourseSchedule.period_end >= period_end
                ),
                db.and_(
                    CourseSchedule.period_start >= period_start,
                    CourseSchedule.period_end <= period_end
                )
            )
        ).all()
        return conflicts
    
    @staticmethod
    def check_classroom_conflict(classroom_id, day_of_week, period_start, period_end, exclude_id=None):
        query = CourseSchedule.query.filter(
            CourseSchedule.classroom_id == classroom_id,
            CourseSchedule.day_of_week == day_of_week
        )
        
        if exclude_id:
            query = query.filter(CourseSchedule.id != exclude_id)
        
        conflicts = query.filter(
            db.or_(
                db.and_(
                    CourseSchedule.period_start <= period_start,
                    CourseSchedule.period_end >= period_start
                ),
                db.and_(
                    CourseSchedule.period_start <= period_end,
                    CourseSchedule.period_end >= period_end
                ),
                db.and_(
                    CourseSchedule.period_start >= period_start,
                    CourseSchedule.period_end <= period_end
                )
            )
        ).all()
        return conflicts
    
    @staticmethod
    def check_workload(teacher_id, max_hours=18):
        total_periods = db.session.query(db.func.sum(
            CourseSchedule.period_end - CourseSchedule.period_start + 1
        )).filter(CourseSchedule.teacher_id == teacher_id).scalar() or 0
        
        return (total_periods > max_hours, total_periods, max_hours)
    
    @staticmethod
    def check_class_conflict(class_id, day_of_week, period_start, period_end, exclude_id=None):
        query = CourseSchedule.query.filter(
            CourseSchedule.class_id == class_id,
            CourseSchedule.day_of_week == day_of_week
        )
        
        if exclude_id:
            query = query.filter(CourseSchedule.id != exclude_id)
        
        conflicts = query.filter(
            db.or_(
                db.and_(
                    CourseSchedule.period_start <= period_start,
                    CourseSchedule.period_end >= period_start
                ),
                db.and_(
                    CourseSchedule.period_start <= period_end,
                    CourseSchedule.period_end >= period_end
                ),
                db.and_(
                    CourseSchedule.period_start >= period_start,
                    CourseSchedule.period_end <= period_end
                )
            )
        ).all()
        return conflicts
    
    @staticmethod
    def validate_schedule(schedule, exclude_id=None):
        errors = []
        
        class_conflicts = ConflictService.check_class_conflict(
            schedule.class_id,
            schedule.day_of_week,
            schedule.period_start,
            schedule.period_end,
            exclude_id
        )
        if class_conflicts:
            errors.append(f"班级{schedule.class_id}在该时间段已有课程安排")
        
        if schedule.teacher_id:
            teacher_conflicts = ConflictService.check_teacher_conflict(
                schedule.teacher_id,
                schedule.day_of_week,
                schedule.period_start,
                schedule.period_end,
                exclude_id
            )
            if teacher_conflicts:
                errors.append(f"教师{schedule.teacher_id}在该时间段已有课程安排")
        
        if schedule.classroom_id:
            classroom_conflicts = ConflictService.check_classroom_conflict(
                schedule.classroom_id,
                schedule.day_of_week,
                schedule.period_start,
                schedule.period_end,
                exclude_id
            )
            if classroom_conflicts:
                errors.append(f"教室{schedule.classroom_id}在该时间段已被占用")
        
        if schedule.teacher_id:
            over_limit, current, max_hours = ConflictService.check_workload(schedule.teacher_id)
            if over_limit:
                errors.append(f"教师{schedule.teacher_id}周课时已达{current}节，超过上限{max_hours}节")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }