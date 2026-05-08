from app import db

class SubjectConfig(db.Model):
    """学科配置模型"""
    __tablename__ = 'subject_config'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(20), unique=True, nullable=False, comment='学科名称')
    full_score = db.Column(db.Integer, nullable=False, comment='满分值')
    subject_type = db.Column(db.String(10), nullable=False, comment='学科类型（文科/理科）')
    enabled = db.Column(db.Boolean, default=True, comment='是否启用')
    
    def __repr__(self):
        return f"<SubjectConfig {self.subject_name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'full_score': self.full_score,
            'subject_type': self.subject_type,
            'enabled': self.enabled
        }

# 学科配置初始化数据
INITIAL_SUBJECT_CONFIG = [
    {'subject_name': '语文', 'full_score': 150, 'subject_type': '文科', 'enabled': True},
    {'subject_name': '数学', 'full_score': 150, 'subject_type': '理科', 'enabled': True},
    {'subject_name': '英语', 'full_score': 150, 'subject_type': '文科', 'enabled': True},
    {'subject_name': '物理', 'full_score': 100, 'subject_type': '理科', 'enabled': True},
    {'subject_name': '化学', 'full_score': 100, 'subject_type': '理科', 'enabled': True},
    {'subject_name': '生物', 'full_score': 100, 'subject_type': '理科', 'enabled': True},
    {'subject_name': '历史', 'full_score': 100, 'subject_type': '文科', 'enabled': True},
    {'subject_name': '地理', 'full_score': 100, 'subject_type': '文科', 'enabled': True},
    {'subject_name': '政治', 'full_score': 100, 'subject_type': '文科', 'enabled': True},
]
