#!/usr/bin/env python3
"""
调试科目匹配问题
"""

import sys
import os

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

def debug_subject_match():
    """调试科目匹配"""
    
    with app.app_context():
        print("=" * 60)
        print("科目匹配调试")
        print("=" * 60)
        
        # 获取高一1班的数据
        print("\n1. 获取高一1班的课程和成绩:")
        print("-" * 40)
        
        # 获取学生
        student = Student.query.filter_by(grade='高一', class_='1班').first()
        print(f"   学生: {student.name} ({student.student_id})")
        
        # 获取该学生的成绩
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        print(f"\n   成绩科目列表:")
        subject_set = set()
        for g in grades:
            print(f"   - {g.subject}")
            subject_set.add(g.subject)
        
        # 获取该班级的课程
        courses = StudentCourse.query.filter_by(grade='高一', class_='1班').all()
        print(f"\n   课程列表 (前10条):")
        course_names = set()
        for c in courses[:10]:
            course_obj = Course.query.filter_by(course_code=c.course_code).first()
            if course_obj:
                print(f"   - {course_obj.course_name} (code: {c.course_code})")
                course_names.add(course_obj.course_name)
        
        # 检查匹配
        print("\n2. 检查科目匹配:")
        print("-" * 40)
        
        print(f"   成绩科目数: {len(subject_set)}")
        print(f"   课程科目数: {len(course_names)}")
        
        print("\n   匹配的科目:")
        matches = subject_set & course_names
        if matches:
            for m in matches:
                print(f"   ✓ {m}")
        else:
            print("   ✗ 没有匹配的科目!")
        
        print("\n   成绩有但课程没有的科目:")
        only_in_grades = subject_set - course_names
        if only_in_grades:
            for s in only_in_grades:
                print(f"   - {s}")
        
        print("\n   课程有但成绩没有的科目:")
        only_in_courses = course_names - subject_set
        if only_in_courses:
            for s in only_in_courses:
                print(f"   - {s}")

if __name__ == '__main__':
    debug_subject_match()
