import sys
import os
import requests

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 导入app和db
from app import db
from flask import Flask
from dotenv import load_dotenv
from app.models import Student, Grade

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置SQLite数据库
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

print("开始验证成绩模块修复结果...")
print("-" * 100)

# 测试1：验证数据库中是否还有重复的成绩记录
print("测试1：验证数据库中是否还有重复的成绩记录")
with app.app_context():
    students = Student.query.all()
    duplicate_count = 0
    for student in students:
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        subject_exam_map = {}
        for grade in grades:
            key = f"{grade.subject}-{grade.exam_type}"
            if key in subject_exam_map:
                duplicate_count += 1
                print(f"学生 {student.name} (ID: {student.student_id}) 有重复的 {grade.subject} 成绩记录")
            else:
                subject_exam_map[key] = True
    if duplicate_count == 0:
        print("✓ 数据库中没有重复的成绩记录")
    else:
        print(f"✗ 数据库中还有 {duplicate_count} 条重复的成绩记录")

# 测试2：验证后端API是否能够正确处理成绩更新
print("\n测试2：验证后端API是否能够正确处理成绩更新")
test_student_id = "STU20240001"
test_scores = [
    {"subject": "语文", "score": 85},
    {"subject": "数学", "score": 92},
    {"subject": "英语", "score": 78},
    {"subject": "物理", "score": 65},
    {"subject": "化学", "score": 72},
    {"subject": "生物", "score": 68},
    {"subject": "历史", "score": 80},
    {"subject": "地理", "score": 75},
    {"subject": "政治", "score": 82}
]

try:
    response = requests.put(f"http://localhost:5000/api/students/{test_student_id}/grades", json={"scores": test_scores})
    if response.status_code == 200:
        print("✓ 后端API能够正确处理成绩更新")
    else:
        print(f"✗ 后端API处理成绩更新失败: {response.status_code}")
except Exception as e:
    print(f"✗ 测试后端API时出错: {str(e)}")

# 测试3：验证后端API是否能够正确验证成绩范围
print("\n测试3：验证后端API是否能够正确验证成绩范围")
test_scores_invalid = [
    {"subject": "语文", "score": 155},  # 超出范围
    {"subject": "数学", "score": -5},   # 负数
    {"subject": "物理", "score": 105}  # 超出范围
]

try:
    response = requests.put(f"http://localhost:5000/api/students/{test_student_id}/grades", json={"scores": test_scores_invalid})
    if response.status_code == 400:
        print("✓ 后端API能够正确验证成绩范围")
    else:
        print(f"✗ 后端API验证成绩范围失败: {response.status_code}")
except Exception as e:
    print(f"✗ 测试后端API时出错: {str(e)}")

# 测试4：验证数据库表是否有唯一约束
print("\n测试4：验证数据库表是否有唯一约束")
try:
    import sqlite3
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('PRAGMA index_list(student_grades)')
    indexes = cursor.fetchall()
    has_unique_index = any(index[1] == '_student_subject_exam_uc' for index in indexes)
    if has_unique_index:
        print("✓ 数据库表有唯一约束")
    else:
        print("✗ 数据库表缺少唯一约束")
    conn.close()
except Exception as e:
    print(f"✗ 测试数据库约束时出错: {str(e)}")

print("-" * 100)
print("验证完成")
