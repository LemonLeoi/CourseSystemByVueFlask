from ..models import GradeSettings
from .. import db


class GradeSettingsDataAccess:
    @staticmethod
    def get_settings():
        """获取成绩分级设置，如果不存在则创建默认设置"""
        settings = GradeSettings.query.first()
        if not settings:
            # 创建默认设置
            settings = GradeSettings()
            db.session.add(settings)
            db.session.commit()
        return settings
    
    @staticmethod
    def update_settings(rule_type, score_rules, percentage_rules):
        """更新成绩分级设置"""
        try:
            settings = GradeSettingsDataAccess.get_settings()
            
            # 更新设置
            settings.rule_type = rule_type
            settings.score_rule_a = score_rules.get('A', 90)
            settings.score_rule_b = score_rules.get('B', 80)
            settings.score_rule_c = score_rules.get('C', 70)
            settings.score_rule_d = score_rules.get('D', 60)
            settings.percentage_rule_a = percentage_rules.get('A', 90)
            settings.percentage_rule_b = percentage_rules.get('B', 85)
            settings.percentage_rule_c = percentage_rules.get('C', 75)
            settings.percentage_rule_d = percentage_rules.get('D', 60)
            settings.percentage_rule_e = percentage_rules.get('E', 50)
            
            db.session.commit()
            return True, settings, "更新成功"
        except Exception as e:
            db.session.rollback()
            return False, None, f"更新失败: {str(e)}"
