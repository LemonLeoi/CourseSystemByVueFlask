from .. import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    def to_dict(self):
        # 获取教师的任教班级
        teaching_classes = db.session.query(TeacherClass.grade, TeacherClass.class_).filter_by(teacher_id=self.teacher_id).all()
        teaching_classes_list = [f"{tc[0]}{tc[1]}" for tc in teaching_classes]
        
        # 获取教师的班主任信息
        homeroom_teacher = db.session.query(HomeroomTeacher).filter_by(teacher_id=self.teacher_id).first()
        is_homeroom_teacher = homeroom_teacher is not None
        homeroom_class = f"{homeroom_teacher.grade}{homeroom_teacher.class_}" if homeroom_teacher else ''
        
        return {
            'name': self.name,
            'teacher_id': self.teacher_id,
            'gender': self.gender,
            'age': self.age,
            'title': self.title,
            'department': self.department,
            'subject': self.department,  # 添加subject字段，与department值相同
            'contact': self.contact or '',
            'status': self.status,
            'teachingClasses': teaching_classes_list,
            'isHomeroomTeacher': is_homeroom_teacher,
            'homeroomClass': homeroom_class,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Teacher {self.name} ({self.teacher_id})>'

class TeacherClass(db.Model):
    __tablename__ = 'teacher_classes'
    
    teacher_id = db.Column(db.Text, db.ForeignKey('teachers.teacher_id'), nullable=False, primary_key=True)
    grade = db.Column(db.Text, nullable=False, primary_key=True)
    class_ = db.Column(db.Text, nullable=False, name='class', primary_key=True)
    
    def __repr__(self):
        return f'<TeacherClass {self.teacher_id} - {self.grade}班{self.class_}>'

class HomeroomTeacher(db.Model):
    __tablename__ = 'homeroom_teachers'
    
    teacher_id = db.Column(db.Text, db.ForeignKey('teachers.teacher_id'), nullable=False, primary_key=True)
    grade = db.Column(db.Text, nullable=False, primary_key=True)
    class_ = db.Column(db.Text, nullable=False, name='class', primary_key=True)
    
    def __repr__(self):
        return f'<HomeroomTeacher {self.teacher_id} - {self.grade}班{self.class_}>'