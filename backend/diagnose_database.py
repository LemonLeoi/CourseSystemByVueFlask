#!/usr/bin/env python3
"""
数据库诊断脚本
用于检查student_courses表和相关数据是否存在
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
from app.models import StudentCourse, Grade, Student, Course, Teacher, TeacherCourse

def diagnose_database():
    """诊断数据库中的数据情况"""
    
    with app.app_context():
        print("=" * 60)
        print("数据库诊断报告")
        print("=" * 60)
        
        # 1. 检查student_courses表
        print("\n1. 检查 student_courses 表:")
        print("-" * 40)
        
        student_courses_count = StudentCourse.query.count()
        print(f"   student_courses 表中的记录数: {student_courses_count}")
        
        if student_courses_count > 0:
            # 获取部分样本数据
            samples = StudentCourse.query.limit(5).all()
            print(f"\n   样本数据（前5条）:")
            for i, sc in enumerate(samples, 1):
                print(f"   {i}. 年级: {sc.grade}, 班级: {sc.class_}, 星期: {sc.day_of_week}, 节次: {sc.period}, 课程: {sc.course_code}, 教室: {sc.classroom}")
        else:
            print("   警告: student_courses 表中没有数据！")
        
        # 2. 检查相关表
        print("\n2. 检查相关表:")
        print("-" * 40)
        
        student_count = Student.query.count()
        print(f"   学生记录数: {student_count}")
        
        grade_count = Grade.query.count()
        print(f"   成绩记录数: {grade_count}")
        
        course_count = Course.query.count()
        print(f"   课程记录数: {course_count}")
        
        teacher_count = Teacher.query.count()
        print(f"   教师记录数: {teacher_count}")
        
        teacher_course_count = TeacherCourse.query.count()
        print(f"   教师课程记录数: {teacher_course_count}")
        
        # 3. 检查成绩与课程的关联
        print("\n3. 检查数据关联:")
        print("-" * 40)
        
        if student_count > 0 and course_count > 0:
            # 获取第一个学生和第一个课程的信息
            sample_student = Student.query.first()
            sample_course = Course.query.first()
            print(f"   样例学生: {sample_student.name} ({sample_student.student_id}), {sample_student.grade}{sample_student.class_}")
            print(f"   样例课程: {sample_course.course_name} ({sample_course.course_code})")
            
            # 检查这个学生有没有成绩
            student_grades = Grade.query.filter_by(student_id=sample_student.student_id).count()
            print(f"   该学生的成绩记录数: {student_grades}")
            
            # 检查该班级有没有课程安排
            if sample_student.class_ and sample_student.grade:
                class_courses = StudentCourse.query.filter_by(
                    grade=sample_student.grade,
                    class_=sample_student.class_
                ).count()
                print(f"   该班级的课程安排数: {class_courses}")
        
        # 4. 检查数据完整性
        print("\n4. 检查数据完整性:")
        print("-" * 40)
        
        # 查询有成绩但没有课程安排的学生
        from sqlalchemy import func, distinct
        students_with_grades = db.session.query(distinct(Grade.student_id)).count()
        students_with_courses = db.session.query(distinct(Student.student_id)).join(
            StudentCourse, 
            (Student.grade == StudentCourse.grade) & 
            (Student.class_ == StudentCourse.class_)
        ).count()
        
        print(f"   有成绩的学生数: {students_with_grades}")
        print(f"   有课程安排的学生数: {students_with_courses}")
        
        # 5. 建议
        print("\n5. 问题诊断与建议:")
        print("-" * 40)
        
        if student_courses_count == 0:
            print("   ⚠️  关键问题: student_courses 表中没有数据！")
            print("      需要先导入课程安排数据，才能进行排课时间分析。")
        elif grade_count == 0:
            print("   ⚠️  问题: grade 表中没有成绩数据！")
            print("      需要先导入成绩数据，才能进行分析。")
        else:
            print("   ✅ 数据库中有基础数据，可以进行分析。")

if __name__ == '__main__':
    diagnose_database()
