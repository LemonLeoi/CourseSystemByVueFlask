from .. import db
from .student import Student
from .exam import Exam
from .course import Course

class Grade(db.Model):
    __tablename__ = 'student_grades'
    
    student_id = db.Column(db.VARCHAR(20), db.ForeignKey('students.student_id'), nullable=False, primary_key=True)
    exam_code = db.Column(db.TEXT, db.ForeignKey('exams.exam_code'), nullable=False, primary_key=True)
    course_code = db.Column(db.TEXT, db.ForeignKey('courses.course_code'), nullable=False, primary_key=True)
    subject = db.Column(db.VARCHAR(50), nullable=False)
    score = db.Column(db.FLOAT, nullable=False)
    grade_level = db.Column(db.VARCHAR(1), nullable=False)
    
    # 添加唯一约束，确保每个学生的每个学科在每次考试下只有一条记录
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject', 'exam_code', name='_student_subject_exam_uc'),
    )
    
    # 关联关系
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
    exam = db.relationship('Exam', backref=db.backref('grades', lazy=True), foreign_keys=[exam_code])
    course = db.relationship('Course', backref=db.backref('grades', lazy=True), foreign_keys=[course_code])
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'exam_code': self.exam_code,
            'course_code': self.course_code,
            'subject': self.subject,
            'score': self.score,
            'grade': self.grade_level
        }
    
    def __repr__(self):
        return f'<Grade {self.subject}: {self.score} ({self.student_id})>'
