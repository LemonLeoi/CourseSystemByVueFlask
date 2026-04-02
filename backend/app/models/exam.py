from .. import db

class Exam(db.Model):
    __tablename__ = 'exams'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam_code = db.Column(db.String(20), unique=True, nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    academic_year = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='准备中')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.exam_code,
            'name': self.exam_name,
            'academicYear': self.academic_year,
            'semester': self.semester,
            'grade': self.grade,
            'type': self.exam_type,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Exam {self.exam_name} ({self.exam_code})>'
