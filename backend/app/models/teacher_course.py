from .. import db
from .teacher import Teacher
from .course import Course

class TeacherCourse(db.Model):
    __tablename__ = 'teacher_courses'
    
    teacher_id = db.Column(db.VARCHAR(20), db.ForeignKey('teachers.teacher_id'), nullable=True, primary_key=True)
    course_code = db.Column(db.VARCHAR(20), db.ForeignKey('courses.course_code'), nullable=True)
    grade = db.Column(db.TEXT, nullable=False, primary_key=True)
    class_ = db.Column(db.TEXT, nullable=False, name='class', primary_key=True)
    day_of_week = db.Column(db.INTEGER, nullable=False, primary_key=True)
    period = db.Column(db.INTEGER, nullable=False, primary_key=True)
    classroom = db.Column(db.TEXT, nullable=False)
    status = db.Column(db.TEXT, nullable=False)
    
    # 关联关系
    teacher = db.relationship('Teacher', backref=db.backref('teaching_courses', lazy=True))
    course = db.relationship('Course', backref=db.backref('teaching_teachers', lazy=True), primaryjoin='TeacherCourse.course_code == Course.course_code')
    
    def to_dict(self):
        week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return {
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
