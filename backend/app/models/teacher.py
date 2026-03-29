from .. import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def to_dict(self):
        # 获取教师的任教班级
        teaching_classes = db.session.query(TeacherClass.grade, TeacherClass.class_).filter_by(teacher_id=self.teacher_id).all()
        teaching_classes_list = [f"{tc[0]}{tc[1]}" for tc in teaching_classes]
        
        # 获取教师的班主任信息
        homeroom_teacher = db.session.query(HomeroomTeacher).filter_by(teacher_id=self.teacher_id).first()
        is_homeroom_teacher = homeroom_teacher is not None
        homeroom_class = f"{homeroom_teacher.grade}{homeroom_teacher.class_}" if homeroom_teacher else ''
        
        return {
            'id': self.id,
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
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.teacher_id'), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    class_ = db.Column(db.String(20), nullable=False, name='class')
    
    def __repr__(self):
        return f'<TeacherClass {self.teacher_id} - {self.grade}班{self.class_}>'

class HomeroomTeacher(db.Model):
    __tablename__ = 'homeroom_teachers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.String(20), db.ForeignKey('teachers.teacher_id'), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    class_ = db.Column(db.String(20), nullable=False, name='class')
    
    def __repr__(self):
        return f'<HomeroomTeacher {self.teacher_id} - {self.grade}班{self.class_}>'