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
    print("开始清理数据库中的重复成绩记录...")
    print("-" * 100)
    
    # 查询所有学生
    students = Student.query.all()
    print(f"数据库中共有 {len(students)} 个学生")
    print("-" * 100)
    
    total_duplicates = 0
    
    for student in students:
        # 查询学生的所有成绩记录
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        
        # 按学科和考试类型分组
        subject_exam_map = {}
        for grade in grades:
            key = f"{grade.subject}-{grade.exam_type}"
            if key not in subject_exam_map:
                subject_exam_map[key] = []
            subject_exam_map[key].append(grade)
        
        # 处理每个分组，只保留最新的一条记录
        for key, grade_list in subject_exam_map.items():
            if len(grade_list) > 1:
                # 按ID降序排序，保留最新的一条记录
                grade_list.sort(key=lambda x: x.id, reverse=True)
                # 保留第一条（最新的），删除其他
                for grade in grade_list[1:]:
                    db.session.delete(grade)
                    total_duplicates += 1
                    print(f"删除学生 {student.name} (ID: {student.student_id}) 的重复 {grade.subject} 成绩记录")
    
    # 提交删除操作
    db.session.commit()
    
    print("-" * 100)
    print(f"清理完成，共删除了 {total_duplicates} 条重复的成绩记录")
    
    # 验证清理结果
    total_grades = 0
    for student in students:
        grades = Grade.query.filter_by(student_id=student.student_id).all()
        total_grades += len(grades)
    
    print(f"清理后，数据库中共有 {total_grades} 条成绩记录")
    print(f"每个学生平均有 {total_grades / len(students):.2f} 条成绩记录")
    
    print("-" * 100)
