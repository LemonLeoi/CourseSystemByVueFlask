from .. import db
from .course import Course

class TeachingProgress(db.Model):
    __tablename__ = 'teaching_progress'
    
    course_id = db.Column(db.INTEGER, nullable=False, primary_key=True)
    teacher_id = db.Column(db.VARCHAR(20), db.ForeignKey('teachers.teacher_id'), nullable=True)
    chapter = db.Column(db.VARCHAR(100), nullable=False, primary_key=True)
    hours = db.Column(db.INTEGER, nullable=False)
    objective = db.Column(db.TEXT, nullable=False)
    progress = db.Column(db.INTEGER, nullable=False)
    status = db.Column(db.VARCHAR(20), nullable=False)
    period = db.Column(db.INTEGER, nullable=True)
    
    # 关联关系
    teacher = db.relationship('Teacher', backref=db.backref('teaching_progress', lazy=True))
    
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'teacher_id': self.teacher_id,
            'chapter': self.chapter,
            'hours': self.hours,
            'objective': self.objective,
            'progress': self.progress,
            'status': self.status,
            'period': self.period
        }
    
    def __repr__(self):
        return f'<TeachingProgress Course:{self.course_id} Chapter:{self.chapter}>'
