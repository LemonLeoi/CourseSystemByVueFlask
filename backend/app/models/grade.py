from .. import db
from .student import Student
from .exam import Exam

class Grade(db.Model):
    __tablename__ = 'student_grades'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    grade_level = db.Column(db.String(1), nullable=False)
    exam_date = db.Column(db.Date)
    
    # 添加唯一约束，确保每个学生的每个学科在每次考试下只有一条记录
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject', 'exam_id', name='_student_subject_exam_uc'),
    )
    
    # 关联关系
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
    exam = db.relationship('Exam', backref=db.backref('grades', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'exam_id': self.exam_id,
            'subject': self.subject,
            'score': self.score,
            'grade': self.grade_level,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None
        }
    
    def __repr__(self):
        return f'<Grade {self.subject}: {self.score} ({self.student_id})>'
