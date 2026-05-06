from .. import db


class GradeSettings(db.Model):
    __tablename__ = 'grade_settings'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rule_type = db.Column(db.VARCHAR(20), nullable=False, default='score')
    # 按具体分数的规则
    score_rule_a = db.Column(db.Integer, nullable=False, default=90)
    score_rule_b = db.Column(db.Integer, nullable=False, default=80)
    score_rule_c = db.Column(db.Integer, nullable=False, default=70)
    score_rule_d = db.Column(db.Integer, nullable=False, default=60)
    # 按得分率百分比的规则
    percentage_rule_a = db.Column(db.Integer, nullable=False, default=90)
    percentage_rule_b = db.Column(db.Integer, nullable=False, default=85)
    percentage_rule_c = db.Column(db.Integer, nullable=False, default=75)
    percentage_rule_d = db.Column(db.Integer, nullable=False, default=60)
    percentage_rule_e = db.Column(db.Integer, nullable=False, default=50)
    
    # 决策树参数配置
    dt_min_samples_split = db.Column(db.Integer, nullable=False, default=2)
    dt_max_depth = db.Column(db.Integer, nullable=False, default=5)
    dt_threshold = db.Column(db.FLOAT, nullable=False, default=0.0001)
    dt_algorithm = db.Column(db.VARCHAR(20), nullable=False, default='C4.5')
    
    # 班级类型分类配置
    class_type_threshold_low = db.Column(db.DECIMAL(5,2), nullable=False, default=60)
    class_type_threshold_high = db.Column(db.DECIMAL(5,2), nullable=False, default=80)
    class_type_method = db.Column(db.VARCHAR(20), nullable=False, default='average')
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'ruleType': self.rule_type,
            'scoreRules': {
                'A': self.score_rule_a,
                'B': self.score_rule_b,
                'C': self.score_rule_c,
                'D': self.score_rule_d
            },
            'percentageRules': {
                'A': self.percentage_rule_a,
                'B': self.percentage_rule_b,
                'C': self.percentage_rule_c,
                'D': self.percentage_rule_d,
                'E': self.percentage_rule_e
            },
            'decisionTreeParams': {
                'minSamplesSplit': self.dt_min_samples_split,
                'maxDepth': self.dt_max_depth,
                'threshold': self.dt_threshold,
                'algorithm': self.dt_algorithm
            },
            'classTypeConfig': {
                'thresholdLow': float(self.class_type_threshold_low),
                'thresholdHigh': float(self.class_type_threshold_high),
                'method': self.class_type_method
            }
        }
    
    def __repr__(self):
        return f'<GradeSettings {self.id}>'
