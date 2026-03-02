from .. import db
from .student import Student

class StudentStatus(db.Model):
    __tablename__ = 'student_status'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    class_ = db.Column('class', db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default='active')
    
    # 关联关系
    student = db.relationship('Student', backref=db.backref('status_info', lazy=True))
    
    def to_dict(self):
        # 状态文本映射
        status_map = {
            'active': '在校',
            'suspended': '休学',
            'graduated': '毕业',
            'dropped': '退学'
        }
        
        return {
            'id': self.student_id,
            'name': self.name,
            'gender': self.gender,
            'class': self.class_,
            'grade': self.grade,
            'contact': self.contact,
            'status': self.status,
            'statusText': status_map.get(self.status, '在校')
        }
    
    def __repr__(self):
        return f'<StudentStatus Student:{self.student_id} Status:{self.status}>'
