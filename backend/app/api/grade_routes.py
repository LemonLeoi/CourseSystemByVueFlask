# Grade analysis API routes
from flask import Blueprint, jsonify, request
from app.analysis.grade_analyzer import (
    analyze_student_performance, 
    analyze_class_performance, 
    analyze_grade_performance,
    analyze_student_subject,
    analyze_class_subject,
    analyze_grade_subject,
    analyze_student_trend,
    analyze_class_trend,
    analyze_grade_trend,
    analyze_teacher_performance,
    analyze_student_schedule,
    analyze_class_schedule
)
from app.data_access.grade_data_access import GradeDataAccess

# 创建蓝图
bp = Blueprint('grade', __name__, url_prefix='/api/grades')

# 获取个人成绩分析
@bp.route('/analysis/<student_id>', methods=['GET'])
def get_student_analysis(student_id):
    try:
        result = analyze_student_performance(student_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取班级成绩分析
@bp.route('/analysis/class/<class_name>', methods=['GET'])
def get_class_analysis(class_name):
    try:
        # 解码URL编码的班级名称
        import urllib.parse
        class_name = urllib.parse.unquote_plus(class_name)
        
        # 直接打印解码后的班级名称，用于调试
        print(f"解码后的班级名称: {class_name}")
        
        # 从班级名称中提取年级和班级数字
        import re
        # 匹配中文年级 + 数字 + 可选的"班"字
        match = re.search(r'([\u4e00-\u9fa5]+)(\d+)(?:班)?', class_name)
        if not match:
            return jsonify({"error": "班级名称格式不正确，应为'高三1班'这样的形式"}), 400
        
        grade = match.group(1)
        class_num = match.group(2)
        class_name = f"{class_num}班"
        
        # 添加调试信息
        print(f"使用的班级名称: {class_name}, 年级: {grade}")
        
        result = analyze_class_performance(class_name, grade)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取年级成绩分析
@bp.route('/analysis/grade/<grade_name>', methods=['GET'])
def get_grade_analysis(grade_name):
    try:
        result = analyze_grade_performance(grade_name)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取个人科目分析
@bp.route('/analysis/subject/<student_id>/<subject>', methods=['GET'])
def get_student_subject_analysis(student_id, subject):
    try:
        result = analyze_student_subject(student_id, subject)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取班级科目分析
@bp.route('/analysis/class/<class_name>/<subject>', methods=['GET'])
def get_class_subject_analysis(class_name, subject):
    try:
        # 解码URL编码的班级名称
        import urllib.parse
        class_name = urllib.parse.unquote_plus(class_name)
        
        # 从班级名称中提取年级和班级数字
        import re
        # 更宽松的正则表达式，匹配中文年级 + 数字 + 可选的"班"字
        match = re.search(r'(.*?)(\d+)(?:班)?', class_name)
        if not match:
            return jsonify({"error": "班级名称格式不正确，应为'高三1班'这样的形式"}), 400
        
        grade = match.group(1)
        class_num = match.group(2)
        
        result = analyze_class_subject(class_num, grade, subject)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取年级科目分析
@bp.route('/analysis/grade/<grade_name>/<subject>', methods=['GET'])
def get_grade_subject_analysis(grade_name, subject):
    try:
        result = analyze_grade_subject(grade_name, subject)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取个人考试趋势
@bp.route('/analysis/trend/<student_id>', methods=['GET'])
def get_student_trend(student_id):
    try:
        # 获取subject和exam查询参数
        subject = request.args.get('subject')
        exam_code = request.args.get('exam')
        result = analyze_student_trend(student_id, subject, exam_code)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取班级考试趋势
@bp.route('/analysis/class/trend/<class_name>', methods=['GET'])
def get_class_trend(class_name):
    try:
        # 解码URL编码的班级名称
        import urllib.parse
        class_name = urllib.parse.unquote_plus(class_name)
        
        # 获取subject和exam查询参数
        subject = request.args.get('subject')
        exam_code = request.args.get('exam')
        
        # 从班级名称中提取年级和班级数字
        import re
        # 更宽松的正则表达式，匹配中文年级 + 数字 + 可选的"班"字
        match = re.search(r'(.*?)(\d+)(?:班)?', class_name)
        if not match:
            return jsonify({"error": "班级名称格式不正确，应为'高三1班'这样的形式"}), 400
        
        grade = match.group(1)
        class_num = match.group(2)
        
        result = analyze_class_trend(class_num, grade, subject, exam_code)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取年级考试趋势
@bp.route('/analysis/grade/trend/<grade_name>', methods=['GET'])
def get_grade_trend(grade_name):
    try:
        result = analyze_grade_trend(grade_name)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取教师成绩对比
@bp.route('/analysis/teacher/<subject>', methods=['GET'])
def get_teacher_performance(subject):
    try:
        result = analyze_teacher_performance(subject)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取个人课程安排与成绩关系
@bp.route('/analysis/schedule/<student_id>', methods=['GET'])
def get_student_schedule_analysis(student_id):
    try:
        result = analyze_student_schedule(student_id)
        # 即使没有课程安排，也返回 200 状态码，因为这是正常的业务情况
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取班级课程安排与成绩关系
@bp.route('/analysis/class/schedule/<class_name>', methods=['GET'])
def get_class_schedule_analysis(class_name):
    try:
        # 解码URL编码的班级名称
        import urllib.parse
        class_name = urllib.parse.unquote_plus(class_name)
        
        # 从班级名称中提取年级和班级数字
        import re
        # 更宽松的正则表达式，匹配中文年级 + 数字 + 可选的"班"字
        match = re.search(r'(.*?)(\d+)(?:班)?', class_name)
        if not match:
            return jsonify({"error": "班级名称格式不正确，应为'高三1班'这样的形式"}), 400
        
        grade = match.group(1)
        class_num = match.group(2)
        
        result = analyze_class_schedule(class_num, grade)
        # 即使没有课程安排，也返回 200 状态码，因为这是正常的业务情况
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 删除学生指定考试的指定科目成绩
@bp.route('/<student_id>/<exam_code>/<subject>', methods=['DELETE'])
def delete_student_grade(student_id, exam_code, subject):
    try:
        success, message = GradeDataAccess.delete_student_grade(student_id, exam_code, subject)
        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500

# 删除学生指定考试的所有科目成绩
@bp.route('/<student_id>/<exam_code>', methods=['DELETE'])
def delete_student_exam_grades(student_id, exam_code):
    try:
        success, message = GradeDataAccess.delete_student_exam_grades(student_id, exam_code)
        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500

# 删除指定考试的所有学生成绩
@bp.route('/exam/<exam_code>', methods=['DELETE'])
def delete_exam_all_grades(exam_code):
    try:
        success, message = GradeDataAccess.delete_exam_all_grades(exam_code)
        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"删除失败: {str(e)}"}), 500