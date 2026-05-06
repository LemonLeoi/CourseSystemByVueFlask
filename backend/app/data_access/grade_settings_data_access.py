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
    
    @staticmethod
    def get_decision_tree_params():
        """获取决策树参数配置"""
        settings = GradeSettingsDataAccess.get_settings()
        return {
            'minSamplesSplit': settings.dt_min_samples_split,
            'maxDepth': settings.dt_max_depth,
            'threshold': settings.dt_threshold,
            'algorithm': settings.dt_algorithm
        }
    
    @staticmethod
    def update_decision_tree_params(params):
        """更新决策树参数配置"""
        try:
            # 参数验证
            validation_errors = []
            
            # 验证最大树深度
            if 'maxDepth' in params:
                max_depth = params['maxDepth']
                if not isinstance(max_depth, int) or max_depth < 1 or max_depth > 20:
                    validation_errors.append('最大树深度必须是1-20之间的整数')
            
            # 验证最小分裂样本数
            if 'minSamplesSplit' in params:
                min_samples = params['minSamplesSplit']
                if not isinstance(min_samples, int) or min_samples < 2 or min_samples > 100:
                    validation_errors.append('最小分裂样本数必须是2-100之间的整数')
            
            # 验证分裂阈值
            if 'threshold' in params:
                threshold = params['threshold']
                if not isinstance(threshold, float) or threshold <= 0.00001 or threshold > 0.1:
                    validation_errors.append('分裂阈值必须是0.00001-0.1之间的正数')
            
            # 验证算法类型
            if 'algorithm' in params:
                algorithm = params['algorithm']
                if algorithm not in ['ID3', 'C4.5']:
                    validation_errors.append("算法类型必须是'ID3'或'C4.5'")
            
            # 如果有验证错误，返回错误信息
            if validation_errors:
                return False, None, '参数验证失败: ' + '; '.join(validation_errors)
            
            # 更新决策树参数
            settings = GradeSettingsDataAccess.get_settings()
            
            if 'minSamplesSplit' in params:
                settings.dt_min_samples_split = params['minSamplesSplit']
            if 'maxDepth' in params:
                settings.dt_max_depth = params['maxDepth']
            if 'threshold' in params:
                settings.dt_threshold = params['threshold']
            if 'algorithm' in params:
                settings.dt_algorithm = params['algorithm']
            
            db.session.commit()
            return True, settings.to_dict(), "更新成功"
        except Exception as e:
            db.session.rollback()
            return False, None, f"更新失败: {str(e)}"
