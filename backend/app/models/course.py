from .. import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.teacher_id'), nullable=True)
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    period = db.Column(db.Integer)
    
    # 关系
    teacher = db.relationship('Teacher', backref=db.backref('courses', lazy=True))
    
    def to_dict(self):
        return {
            'course_name': self.course_name,
            'course_code': self.course_code,
            'teacher_id': self.teacher_id,
            'subject': self.subject,
            'grade': self.grade,
            'semester': self.semester,
            'year': self.year,
            'period': self.period,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Course {self.course_name} ({self.course_code})>'
