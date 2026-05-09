#!/usr/bin/env python3
"""
调试查询脚本
检查数据查询是否能正常工作
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

# 导入模型和数据访问层
from app.models import StudentCourse, Grade, Student, Course
from app.data_access.grade_data_access import GradeDataAccess

def debug_query():
    """调试查询"""
    
    with app.app_context():
        print("=" * 60)
        print("数据查询调试")
        print("=" * 60)
        
        # 测试1: 测试calculate_period_statistics
        print("\n1. 测试 calculate_period_statistics('1班', '高一'):")
        print("-" * 40)
        
        try:
            result = GradeDataAccess.calculate_period_statistics('1班', '高一')
            print(f"   返回结果数: {len(result)}")
            print(f"   结果: {result}")
        except Exception as e:
            print(f"   错误: {e}")
            import traceback
            print(f"   堆栈: {traceback.format_exc()}")
        
        # 测试2: 直接查询数据
        print("\n2. 直接查询高一1班的数据:")
        print("-" * 40)
        
        try:
            from sqlalchemy import func, and_
            
            # 查询课程安排和成绩
            query = db.session.query(
                StudentCourse.period,
                Grade.score
            ).join(
                Course, StudentCourse.course_code == Course.course_code
            ).join(
                Student, and_(
                    Student.grade == StudentCourse.grade,
                    Student.class_ == StudentCourse.class_
                )
            ).join(
                Grade, and_(
                    Student.student_id == Grade.student_id,
                    Course.course_name == Grade.subject
                )
            ).filter(
                Student.class_ == '1班',
                Student.grade == '高一',
                Grade.score.isnot(None)
            )
            
            print(f"   SQL查询: {str(query)}")
            
            results = query.all()
            print(f"   查询结果数: {len(results)}")
            
            if len(results) > 0:
                print(f"   前5条结果:")
                for i, r in enumerate(results[:5], 1):
                    print(f"   {i}. 节次: {r.period}, 成绩: {r.score}")
            else:
                print("   没有找到数据！")
                
                # 分步调试
                print("\n   分步调试:")
                
                # 检查课程表
                courses = StudentCourse.query.filter_by(grade='高一', class_='1班').all()
                print(f"   高一1班的课程安排数: {len(courses)}")
                
                # 检查学生
                students = Student.query.filter_by(grade='高一', class_='1班').all()
                print(f"   高一1班的学生数: {len(students)}")
                
                if len(students) > 0:
                    # 检查第一个学生的成绩
                    first_student = students[0]
                    grades = Grade.query.filter_by(student_id=first_student.student_id).all()
                    print(f"   学生 {first_student.name} 的成绩数: {len(grades)}")
                    
                    if len(grades) > 0:
                        print(f"   科目示例: {grades[0].subject}")
                        
                        # 检查是否有对应课程
                        if len(courses) > 0:
                            course = courses[0]
                            course_obj = Course.query.filter_by(course_code=course.course_code).first()
                            if course_obj:
                                print(f"   课程示例: {course_obj.course_name}")
                
        except Exception as e:
            print(f"   错误: {e}")
            import traceback
            print(f"   堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    debug_query()
