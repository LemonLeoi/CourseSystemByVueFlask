from .. import db
from .student import Student
from .course import Course
from .teacher import Teacher

class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    
    grade = db.Column(db.Text, nullable=False, primary_key=True)
    class_ = db.Column(db.Text, nullable=False, name='class', primary_key=True)
    course_code = db.Column(db.VARCHAR(20), db.ForeignKey('courses.course_code'), nullable=True)
    teacher_id = db.Column(db.VARCHAR(20), nullable=True)
    day_of_week = db.Column(db.Integer, nullable=False, primary_key=True)
    period = db.Column(db.Integer, nullable=False, primary_key=True)
    classroom = db.Column(db.VARCHAR(50), nullable=False)
    status = db.Column(db.VARCHAR(20), nullable=False)
    room_id = db.Column(db.VARCHAR(10), nullable=True)
    
    # 关联关系
    course = db.relationship('Course', backref=db.backref('student_courses', lazy=True), primaryjoin='StudentCourse.course_code == Course.course_code')
    
    def to_dict(self):
        week_days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return {
            'day': week_days[self.day_of_week - 1] if 1 <= self.day_of_week <= 7 else str(self.day_of_week),
            'timeSlot': self.period,
            'name': self.course.course_name if self.course else '',
            'teacher': self.teacher_id if self.teacher_id else '',
            'classroom': self.classroom,
            'grade': self.grade,
            'class': self.class_,
            'day_of_week': self.day_of_week,
            'period': self.period,
            'course_code': self.course_code
        }
    
    def __repr__(self):
        return f'<StudentCourse Grade:{self.grade} Class:{self.class_} Day:{self.day_of_week} Period:{self.period}>'
