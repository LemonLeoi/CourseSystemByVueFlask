# Grade analysis API routes
from flask import Blueprint, jsonify
from app.analysis.grade_analyzer import analyze_student_performance, analyze_class_performance, analyze_grade_performance
from app.analysis.statistical_analysis import get_overall_statistics, get_subject_statistics, get_exam_type_statistics

# 创建蓝图
grade_bp = Blueprint('grade', __name__, url_prefix='/api/grades')

# 获取整体成绩分析
@grade_bp.route('/analysis', methods=['GET'])
def get_overall_analysis():
    try:
        # 获取整体统计数据
        overall_stats = get_overall_statistics()
        subject_stats = get_subject_statistics()
        exam_stats = get_exam_type_statistics()
        
        result = {
            "overall": overall_stats,
            "subjects": subject_stats,
            "exam_types": exam_stats
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取个人成绩分析
@grade_bp.route('/analysis/<student_id>', methods=['GET'])
def get_student_analysis(student_id):
    try:
        result = analyze_student_performance(student_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取班级成绩分析
@grade_bp.route('/analysis/class/<class_name>', methods=['GET'])
def get_class_analysis(class_name):
    try:
        # 从班级名称中提取年级信息（例如：高三1班 -> 年级：高三，班级：1）
        # 这里简化处理，假设班级名称格式为"高三1班"这样的形式
        import re
        match = re.match(r'(.*?)(\d+)班', class_name)
        if not match:
            return jsonify({"error": "班级名称格式不正确，应为'高三1班'这样的形式"}), 400
        
        grade = match.group(1)
        class_num = match.group(2)
        
        result = analyze_class_performance(class_num, grade)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 获取年级成绩分析
@grade_bp.route('/analysis/grade/<grade_name>', methods=['GET'])
def get_grade_analysis(grade_name):
    try:
        result = analyze_grade_performance(grade_name)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500