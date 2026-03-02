from flask import Blueprint, jsonify
from app import db
from app.models import Student, Teacher, Course, Exam

# 创建Blueprint
bp = Blueprint('admin', __name__)

@bp.route('/dashboard/statistics', methods=['GET'])
def get_dashboard_statistics():
    """获取仪表板统计数据"""
    try:
        # 计算各项统计数据
        total_students = Student.query.count()
        total_teachers = Teacher.query.count()
        total_courses = Course.query.count()
        # 获取近期考试数量（例如未来30天内的考试）
        from datetime import datetime, timedelta
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        upcoming_exams = Exam.query.filter(
            Exam.start_date >= today,
            Exam.start_date <= thirty_days_later
        ).count()
        
        # 构建统计数据
        statistics = [
            {"title": "学生总数", "value": total_students, "icon": "fa-solid fa-users"},
            {"title": "教师总数", "value": total_teachers, "icon": "fa-solid fa-chalkboard-user"},
            {"title": "课程总数", "value": total_courses, "icon": "fa-solid fa-book-open"},
            {"title": "近期考试数量", "value": upcoming_exams, "icon": "fa-solid fa-file-invoice"}
        ]
        
        return jsonify(statistics)
    except Exception as e:
        print(f"获取统计数据失败: {e}")
        # 失败时返回默认数据
        return jsonify([
            {"title": "学生总数", "value": 0, "icon": "fa-solid fa-users"},
            {"title": "教师总数", "value": 0, "icon": "fa-solid fa-chalkboard-user"},
            {"title": "课程总数", "value": 0, "icon": "fa-solid fa-book-open"},
            {"title": "近期考试数量", "value": 0, "icon": "fa-solid fa-file-invoice"}
        ])

@bp.route('/dashboard/notifications', methods=['GET'])
def get_dashboard_notifications():
    """获取仪表板通知"""
    try:
        # 从Exam表中获取考试安排作为通知
        exams = Exam.query.order_by(Exam.start_date.desc()).limit(10).all()
        
        # 转换为通知格式
        notifications = []
        for exam in exams:
            notifications.append({
                "date": exam.start_date.isoformat() if exam.start_date else "",
                "content": f"{exam.exam_type}：{exam.exam_name}安排"
            })
        
        # 如果没有考试数据，返回默认通知
        if not notifications:
            notifications = [
                {"date": "2025-05-01", "content": "测验：历史科目安排"},
                {"date": "2025-04-30", "content": "测试：地理科目安排"},
                {"date": "2025-04-29", "content": "考试：历史科目安排"}
            ]
        
        return jsonify(notifications)
    except Exception as e:
        print(f"获取通知数据失败: {e}")
        # 失败时返回默认通知
        return jsonify([
            {"date": "2025-05-01", "content": "测验：历史科目安排"},
            {"date": "2025-04-30", "content": "测试：地理科目安排"},
            {"date": "2025-04-29", "content": "考试：历史科目安排"}
        ])

@bp.route('/dashboard/todos', methods=['GET'])
def get_dashboard_todos():
    """获取仪表板待办事项"""
    try:
        # 这里可以根据实际业务逻辑从数据库获取待办事项
        # 目前返回默认的待办事项
        todos = [
            "审批学生请假申请",
            "审核教师课程申请"
        ]
        
        return jsonify(todos)
    except Exception as e:
        print(f"获取待办事项失败: {e}")
        # 失败时返回默认待办事项
        return jsonify([
            "审批学生请假申请",
            "审核教师课程申请"
        ])
