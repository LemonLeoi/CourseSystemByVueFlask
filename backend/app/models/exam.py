from .. import db

class Exam(db.Model):
    __tablename__ = 'exams'
    
    exam_code = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    
    def to_dict(self):
        return {
            'code': self.exam_code,
            'name': self.exam_name,
            'type': self.exam_type,
            'grade': self.grade,
            'startDate': self.start_date.isoformat() if self.start_date else None,
            'endDate': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'academicYear': self.academic_year,
            'semester': self.semester
        }
    
    def __repr__(self):
        return f'<Exam {self.exam_name} ({self.exam_code})>'
