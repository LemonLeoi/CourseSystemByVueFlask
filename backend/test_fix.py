#!/usr/bin/env python3
"""
测试修复后的函数
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

def test_fix():
    """测试修复后的函数"""
    
    with app.app_context():
        print("=" * 60)
        print("测试修复后的函数")
        print("=" * 60)
        
        # 测试1: calculate_period_statistics
        print("\n1. 测试 calculate_period_statistics:")
        print("-" * 40)
        
        try:
            result = GradeDataAccess.calculate_period_statistics('1班', '高一')
            print(f"   返回结果数: {len(result)}")
            for item in result:
                print(f"   - {item}")
        except Exception as e:
            print(f"   错误: {e}")
            import traceback
            print(f"   堆栈: {traceback.format_exc()}")
        
        # 测试2: calculate_double_class_statistics
        print("\n2. 测试 calculate_double_class_statistics:")
        print("-" * 40)
        
        try:
            result = GradeDataAccess.calculate_double_class_statistics('1班', '高一')
            print(f"   返回结果数: {len(result)}")
            for item in result:
                print(f"   - {item}")
        except Exception as e:
            print(f"   错误: {e}")
            import traceback
            print(f"   堆栈: {traceback.format_exc()}")
        
        # 测试3: get_schedule_grade_analysis
        print("\n3. 测试 get_schedule_grade_analysis:")
        print("-" * 40)
        
        try:
            result = GradeDataAccess.get_schedule_grade_analysis('1班', '高一')
            print(f"   day_of_week_scores: {result.get('day_of_week_scores', {})}")
            print(f"   period_scores: {result.get('period_scores', {})}")
        except Exception as e:
            print(f"   错误: {e}")
            import traceback
            print(f"   堆栈: {traceback.format_exc()}")

if __name__ == '__main__':
    test_fix()
