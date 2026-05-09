#!/usr/bin/env python3
"""
详细调试
"""

import sys
import os
import re

# 添加应用路径
sys.path.insert(0, os.path.dirname(__file__))

# 初始化Flask应用
from flask import Flask
from flask_cors import CORS
from app import db

# 创建Flask应用实例
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 配置SQLite数据库
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 导入模型
from app.models import StudentCourse, Grade, Student, Course

def debug_detail():
    """详细调试"""
    
    with app.app_context():
        print("=" * 60)
        print("详细调试")
        print("=" * 60)
        
        # 1. 获取课程安排
        print("\n1. 获取课程安排:")
        print("-" * 40)
        
        course_schedules = db.session.query(
            StudentCourse.period,
            StudentCourse.course_code,
            StudentCourse.class_,
            StudentCourse.grade
        ).filter(
            StudentCourse.grade == '高一',
            StudentCourse.class_ == '1班'
        ).all()
        
        print(f"   课程安排数: {len(course_schedules)}")
        if course_schedules[:3]:
            for i, sched in enumerate(course_schedules[:3]):
                print(f"   - 节次: {sched.period}, 课程代码: {sched.course_code}")
        
        # 2. 获取课程信息
        print("\n2. 获取课程信息:")
        print("-" * 40)
        
        course_codes = set([s.course_code for s in course_schedules])
        for code in course_codes:
            course = Course.query.filter_by(course_code=code).first()
            if course:
                print(f"   代码: {code}, 名称: {course.course_name}")
                
                # 测试提取基础名
                base_name = course.course_name
                match = re.match(r'([\u4e00-\u9fa5]+)', base_name)
                if match:
                    base_name = match.group(1)
                print(f"     -> 基础名: {base_name}")
        
        # 3. 获取学生
        print("\n3. 获取学生:")
        print("-" * 40)
        
        students = Student.query.filter(Student.grade == '高一', Student.class_ == '1班').all()
        print(f"   学生数: {len(students)}")
        for s in students[:3]:
            print(f"   - {s.name} ({s.student_id})")
        
        # 4. 获取学生成绩
        print("\n4. 获取学生成绩:")
        print("-" * 40)
        
        student = students[0] if students else None
        if student:
            grades = Grade.query.filter_by(student_id=student.student_id).all()
            print(f"   学生 {student.name} 的成绩数: {len(grades)}")
            subjects = set()
            for g in grades:
                print(f"   - {g.subject}: {g.score}")
                subjects.add(g.subject)
            print(f"   科目列表: {subjects}")
        
        # 5. 看看课程名和成绩科目的匹配
        print("\n5. 课程名和成绩科目的匹配:")
        print("-" * 40)
        
        print("\n匹配关系:")
        for sched in course_schedules[:5]:
            course = Course.query.filter_by(course_code=sched.course_code).first()
            if course:
                base_name = course.course_name
                match = re.match(r'([\u4e00-\u9fa5]+)', base_name)
                if match:
                    base_name = match.group(1)
                print(f"   课程: {course.course_name} -> 基础名: {base_name}")
        
        print("\n是否在成绩科目中:")
        for sched in course_schedules[:5]:
            course = Course.query.filter_by(course_code=sched.course_code).first()
            if course:
                base_name = course.course_name
                match = re.match(r'([\u4e00-\u9fa5]+)', base_name)
                if match:
                    base_name = match.group(1)
                if student:
                    grades = Grade.query.filter_by(student_id=student.student_id).all()
                    has_subject = any(g.subject == base_name for g in grades)
                    print(f"   {base_name}: {'有' if has_subject else '无'}")

if __name__ == '__main__':
    debug_detail()
