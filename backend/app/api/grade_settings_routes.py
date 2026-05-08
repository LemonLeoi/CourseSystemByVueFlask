from flask import Blueprint, request
from app.data_access.grade_settings_data_access import GradeSettingsDataAccess
from app.utils.response import ResponseUtil

bp = Blueprint('grade_settings', __name__)

@bp.route('/', methods=['GET'])
def get_grade_settings():
    """获取成绩分级设置"""
    try:
        settings = GradeSettingsDataAccess.get_settings()
        return ResponseUtil.success(data=settings.to_dict(), message="获取成绩分级设置成功")
    except Exception as e:
        return ResponseUtil.server_error(message=f"获取成绩分级设置失败: {str(e)}")

@bp.route('/', methods=['PUT'])
def update_grade_settings():
    """更新成绩分级设置"""
    try:
        data = request.get_json()
        
        # 验证数据
        required_fields = ['ruleType', 'scoreRules', 'percentageRules']
        for field in required_fields:
            if field not in data:
                return ResponseUtil.bad_request(message=f'缺少必填字段: {field}')
        
        rule_type = data['ruleType']
        score_rules = data['scoreRules']
        percentage_rules = data['percentageRules']
        
        success, settings, message = GradeSettingsDataAccess.update_settings(
            rule_type, score_rules, percentage_rules
        )
        
        if success:
            return ResponseUtil.success(data=settings.to_dict(), message=message)
        else:
            return ResponseUtil.bad_request(message=message)
    except Exception as e:
        return ResponseUtil.server_error(message=f"更新成绩分级设置失败: {str(e)}")
