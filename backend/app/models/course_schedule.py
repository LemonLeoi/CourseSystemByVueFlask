from .. import db
from .course import Course
from .teacher import Teacher
from .classroom import Classroom

class CourseSchedule(db.Model):
    __tablename__ = 'course_schedules'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.String(20), nullable=False)
    course_code = db.Column(db.String(20), db.ForeignKey('courses.course_code'), nullable=False)
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.teacher_id'))
    day_of_week = db.Column(db.Integer, nullable=False)
    period_start = db.Column(db.Integer, nullable=False)
    period_end = db.Column(db.Integer, nullable=False)
    classroom_id = db.Column(db.String(20), db.ForeignKey('classroom.room_id'))
    
    course = db.relationship('Course', backref=db.backref('schedules', lazy=True))
    teacher = db.relationship('Teacher', backref=db.backref('schedules', lazy=True))
    classroom = db.relationship('Classroom', backref=db.backref('schedules', lazy=True))
    
    __table_args__ = (
        db.UniqueConstraint('class_id', 'day_of_week', 'period_start', name='uq_class_time'),
        db.Index('idx_teacher_schedule', 'teacher_id', 'day_of_week', 'period_start'),
        db.Index('idx_class_schedule', 'class_id', 'day_of_week', 'period_start'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'class_id': self.class_id,
            'course_code': self.course_code,
            'course_name': self.course.course_name if self.course else '',
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else '',
            'day_of_week': self.day_of_week,
            'period_start': self.period_start,
            'period_end': self.period_end,
            'classroom_id': self.classroom_id,
            'classroom_name': self.classroom.room_id if self.classroom else ''
        }
    
    def __repr__(self):
        return f'<CourseSchedule {self.class_id} Day:{self.day_of_week} Period:{self.period_start}-{self.period_end}>'