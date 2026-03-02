from .. import db
from .course import Course

class TeachingProgress(db.Model):
    __tablename__ = 'teaching_progress'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    chapter = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    objective = db.Column(db.Text, nullable=False)
    progress = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='not-started')
    
    # 关联关系
    course = db.relationship('Course', backref=db.backref('progress', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'chapter': self.chapter,
            'hours': self.hours,
            'objective': self.objective,
            'progress': self.progress,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<TeachingProgress Course:{self.course_id} Chapter:{self.chapter}>'
