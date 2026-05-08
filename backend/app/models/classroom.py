from .. import db

class Classroom(db.Model):
    __tablename__ = 'classroom'
    
    room_id = db.Column(db.String(10), primary_key=True)
    grade = db.Column(db.String(20), nullable=False)
    class_ = db.Column('class', db.String(20), nullable=False)
    building = db.Column(db.String(10), nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, default=45)
    status = db.Column(db.String(20), default='available')
    
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'grade': self.grade,
            'class': self.class_,
            'building': self.building,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<Classroom {self.room_id} Grade:{self.grade} Class:{self.class_}>'