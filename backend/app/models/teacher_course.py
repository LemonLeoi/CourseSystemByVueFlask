from .. import db
from .teacher import Teacher
from .course import Course

class TeacherCourse(db.Model):
    __tablename__ = 'teacher_courses'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.teacher_id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True)
    grade = db.Column(db.String(20), nullable=False)
    class_ = db.Column(db.String(20), nullable=False, name='class')
    day_of_week = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')
    
    # 关联关系
    teacher = db.relationship('Teacher', backref=db.backref('teaching_courses', lazy=True))
    course = db.relationship('Course', backref=db.backref('teaching_teachers', lazy=True))
    
    def to_dict(self):
        week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return {
            'id': self.id,
            'day': week_days[self.day_of_week - 1] if 1 <= self.day_of_week <= 7 else str(self.day_of_week),
            'timeSlot': self.period,
            'name': self.course.course_name if self.course else '',
            'className': f"{self.grade}{self.class_}",
            'classroom': self.classroom,
            'grade': self.grade,
            'class': self.class_,
            'day_of_week': self.day_of_week,
            'period': self.period
        }
    
    def __repr__(self):
        return f'<TeacherCourse Teacher:{self.teacher_id} Class:{self.grade}{self.class_}班 Day:{self.day_of_week} Period:{self.period}>'
