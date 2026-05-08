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
    
    @staticmethod
    def get_class_type_config():
        """获取班级类型分类配置"""
        settings = GradeSettingsDataAccess.get_settings()
        return {
            'thresholdLow': float(settings.class_type_threshold_low),
            'thresholdHigh': float(settings.class_type_threshold_high),
            'method': settings.class_type_method,
            'description': {
                'weakClass': f'平均分低于{settings.class_type_threshold_low}分为基础薄弱班',
                'normalClass': f'平均分{settings.class_type_threshold_low}-{settings.class_type_threshold_high}分为普通班',
                'keyClass': f'平均分高于{settings.class_type_threshold_high}分为重点班'
            }
        }
    
    @staticmethod
    def update_class_type_config(config):
        """更新班级类型分类配置"""
        try:
            # 参数验证
            validation_errors = []
            
            # 验证低阈值
            if 'thresholdLow' in config:
                threshold_low = config['thresholdLow']
                if not isinstance(threshold_low, (int, float)) or threshold_low < 0 or threshold_low > 100:
                    validation_errors.append('基础薄弱班分数线必须是0-100之间的数值')
            
            # 验证高阈值
            if 'thresholdHigh' in config:
                threshold_high = config['thresholdHigh']
                if not isinstance(threshold_high, (int, float)) or threshold_high < 0 or threshold_high > 100:
                    validation_errors.append('重点班分数线必须是0-100之间的数值')
            
            # 验证低阈值小于高阈值
            if 'thresholdLow' in config and 'thresholdHigh' in config:
                if config['thresholdLow'] >= config['thresholdHigh']:
                    validation_errors.append('基础薄弱班分数线必须小于重点班分数线')
            elif 'thresholdLow' in config:
                settings = GradeSettingsDataAccess.get_settings()
                if config['thresholdLow'] >= settings.class_type_threshold_high:
                    validation_errors.append('基础薄弱班分数线必须小于重点班分数线')
            elif 'thresholdHigh' in config:
                settings = GradeSettingsDataAccess.get_settings()
                if config['thresholdHigh'] <= settings.class_type_threshold_low:
                    validation_errors.append('重点班分数线必须大于基础薄弱班分数线')
            
            # 验证分类方法
            if 'method' in config:
                method = config['method']
                if method not in ['average', 'median']:
                    validation_errors.append("分类方法必须是'average'或'median'")
            
            # 如果有验证错误，返回错误信息
            if validation_errors:
                return False, None, '参数验证失败: ' + '; '.join(validation_errors)
            
            # 更新配置
            settings = GradeSettingsDataAccess.get_settings()
            
            if 'thresholdLow' in config:
                settings.class_type_threshold_low = config['thresholdLow']
            if 'thresholdHigh' in config:
                settings.class_type_threshold_high = config['thresholdHigh']
            if 'method' in config:
                settings.class_type_method = config['method']
            
            db.session.commit()
            return True, GradeSettingsDataAccess.get_class_type_config(), "更新成功"
        except Exception as e:
            db.session.rollback()
            return False, None, f"更新失败: {str(e)}"
    
    @staticmethod
    def get_score_rate_config():
        """获取得分率配置"""
        settings = GradeSettingsDataAccess.get_settings()
        return {
            'use_score_rate': settings.use_score_rate,
            'language_total': settings.language_total,
            'science_total': settings.science_total
        }
    
    @staticmethod
    def update_score_rate_config(data):
        """更新得分率配置"""
        try:
            settings = GradeSettingsDataAccess.get_settings()
            
            if 'use_score_rate' in data:
                settings.use_score_rate = data['use_score_rate']
            if 'language_total' in data:
                language_total = data['language_total']
                if not isinstance(language_total, int) or language_total < 0 or language_total > 300:
                    return False, None, '语言科目总分必须是0-300之间的整数'
                settings.language_total = language_total
            if 'science_total' in data:
                science_total = data['science_total']
                if not isinstance(science_total, int) or science_total < 0 or science_total > 300:
                    return False, None, '理科科目总分必须是0-300之间的整数'
                settings.science_total = science_total
            
            db.session.commit()
            return True, GradeSettingsDataAccess.get_score_rate_config(), "更新成功"
        except Exception as e:
            db.session.rollback()
            return False, None, f"更新失败: {str(e)}"
    
    @staticmethod
    def get_admission_line_config():
        """获取分数线配置"""
        settings = GradeSettingsDataAccess.get_settings()
        return {
            'key_university_line': float(settings.key_university_line),
            'undergraduate_line': float(settings.undergraduate_line)
        }
    
    @staticmethod
    def update_admission_line_config(data):
        """更新分数线配置"""
        try:
            settings = GradeSettingsDataAccess.get_settings()
            
            if 'key_university_line' in data:
                key_line = data['key_university_line']
                if not isinstance(key_line, (int, float)) or key_line < 0 or key_line > 750:
                    return False, None, '重本线必须是0-750之间的数值'
                settings.key_university_line = key_line
            
            if 'undergraduate_line' in data:
                undergrad_line = data['undergraduate_line']
                if not isinstance(undergrad_line, (int, float)) or undergrad_line < 0 or undergrad_line > 750:
                    return False, None, '本科线必须是0-750之间的数值'
                settings.undergraduate_line = undergrad_line
            
            # 验证重本线大于本科线
            if settings.key_university_line <= settings.undergraduate_line:
                return False, None, '重本线必须大于本科线'
            
            db.session.commit()
            return True, GradeSettingsDataAccess.get_admission_line_config(), "更新成功"
        except Exception as e:
            db.session.rollback()
            return False, None, f"更新失败: {str(e)}"
