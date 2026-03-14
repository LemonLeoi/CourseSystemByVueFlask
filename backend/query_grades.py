import sys
import os

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

with app.app_context():
    print("开始查询数据库中的成绩数据...")
    print("-" * 100)
    
    # 查询所有学生
    students = Student.query.all()
    print(f"数据库中共有 {len(students)} 个学生")
    print("-" * 100)
    
    # 统计每个学生的成绩记录数
    total_grades = 0
    for student in students:
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        total_grades += len(grades)
        if len(grades) > 0:
            print(f"学生 {student.name} (ID: {student.student_id}) 有 {len(grades)} 条成绩记录")
            # 打印前5条成绩记录
            for i, grade in enumerate(grades[:5]):
                print(f"  {i+1}. {grade.subject}: {grade.score} ({grade.grade_level}) - {grade.exam_type}")
            if len(grades) > 5:
                print(f"  ... 还有 {len(grades) - 5} 条记录")
            print()
    
    print("-" * 100)
    print(f"数据库中共有 {total_grades} 条成绩记录")
    
    # 检查是否有重复的成绩记录
    print("\n检查是否有重复的成绩记录...")
    duplicate_count = 0
    for student in students:
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        # 检查是否有相同科目和考试类型的记录
        subject_exam_map = {}
        for grade in grades:
            key = f"{grade.subject}-{grade.exam_type}"
            if key in subject_exam_map:
                duplicate_count += 1
                print(f"学生 {student.name} (ID: {student.student_id}) 有重复的 {grade.subject} 成绩记录")
            else:
                subject_exam_map[key] = True
    
    if duplicate_count == 0:
        print("未发现重复的成绩记录")
    else:
        print(f"发现 {duplicate_count} 条重复的成绩记录")
    
    print("-" * 100)
