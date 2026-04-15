import os
import sys
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime
import random

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置SQLite数据库
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入db实例和模型
from app import db
from app.models.teacher import Teacher, TeacherClass, HomeroomTeacher
from app.models.teacher_course import TeacherCourse

# 初始化数据库
db.init_app(app)

# 学科代码映射
SUBJECT_CODES = {
    '语文': '01',
    '数学': '02',
    '英语': '03',
    '物理': '14',
    '化学': '15',
    '生物': '16',
    '历史': '24',
    '政治': '25',
    '地理': '26'
}

# 教师分配表
TEACHER_ASSIGNMENT = {
    '高一': {
        '1班': {'语文': '1', '数学': '1', '英语': '1', '物理': '1', '化学': '1', '生物': '1', '历史': '1', '政治': '1', '地理': '1'},
        '2班': {'语文': '1', '数学': '1', '英语': '1', '物理': '1', '化学': '1', '生物': '1', '历史': '1', '政治': '1', '地理': '1'},
        '3班': {'语文': '2', '数学': '2', '英语': '2', '物理': '2', '化学': '2', '生物': '2', '历史': '2', '政治': '2', '地理': '2'},
        '4班': {'语文': '2', '数学': '2', '英语': '2', '物理': '2', '化学': '2', '生物': '2', '历史': '2', '政治': '2', '地理': '2'},
        '5班': {'语文': '3', '数学': '3', '英语': '3', '物理': '3', '化学': '3', '生物': '3', '历史': '3', '政治': '3', '地理': '3'},
        '6班': {'语文': '3', '数学': '3', '英语': '3', '物理': '3', '化学': '3', '生物': '3', '历史': '3', '政治': '3', '地理': '3'}
    },
    '高二': {
        '1班': {'语文': '4', '数学': '4', '英语': '4', '物理': '4', '化学': '4', '生物': '4'},
        '2班': {'语文': '4', '数学': '4', '英语': '4', '物理': '4', '化学': '4', '生物': '4'},
        '3班': {'语文': '5', '数学': '5', '英语': '5', '物理': '5', '化学': '5', '地理': '4'},
        '4班': {'语文': '5', '数学': '5', '英语': '5', '物理': '5', '化学': '5', '地理': '4'},
        '5班': {'语文': '6', '数学': '6', '英语': '6', '历史': '4', '政治': '4', '地理': '5'},
        '6班': {'语文': '6', '数学': '6', '英语': '6', '历史': '4', '政治': '4', '地理': '5'}
    },
    '高三': {
        '1班': {'语文': '7', '数学': '7', '英语': '7', '物理': '6', '化学': '6', '生物': '5'},
        '2班': {'语文': '7', '数学': '7', '英语': '7', '物理': '6', '化学': '6', '生物': '5'},
        '3班': {'语文': '8', '数学': '8', '英语': '8', '物理': '7', '化学': '7', '地理': '6'},
        '4班': {'语文': '8', '数学': '8', '英语': '8', '物理': '7', '化学': '7', '地理': '6'},
        '5班': {'语文': '9', '数学': '9', '英语': '9', '历史': '5', '政治': '5', '地理': '7'},
        '6班': {'语文': '9', '数学': '9', '英语': '9', '历史': '5', '政治': '5', '地理': '7'}
    }
}

# 各学科需要的老师数量
TEACHER_COUNT = {
    '语文': 9,
    '数学': 9,
    '英语': 9,
    '物理': 7,
    '化学': 7,
    '地理': 7,
    '生物': 5,
    '历史': 5,
    '政治': 5
}

def generate_teacher_id(subject, index):
    """生成教师工号"""
    subject_code = SUBJECT_CODES[subject]
    return f"2024{subject_code}{index:02d}"

def generate_phone_number():
    """生成随机电话号码"""
    # 生成11位随机电话号码，以13开头
    return f"13{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"

def main():
    """主函数"""
    with app.app_context():
        try:
            print("开始创建教师数据...")
            
            # 暂时禁用外键约束
            db.session.execute('PRAGMA foreign_keys = OFF')
            
            # 删除现有的教师数据
            print("删除现有教师数据...")
            db.session.query(TeacherClass).delete()
            db.session.query(HomeroomTeacher).delete()
            db.session.query(TeacherCourse).delete()
            db.session.query(Teacher).delete()
            db.session.commit()
            print("现有教师数据删除成功")
            
            # 为每个学科创建指定数量的老师
            teachers = []
            teacher_map = {}  # 用于存储教师对象，方便后续分配
            
            for subject, count in TEACHER_COUNT.items():
                for i in range(1, count + 1):
                    teacher_id = generate_teacher_id(subject, i)
                    # 生成教师姓名
                    name = f"{subject}老师{i}"
                    # 性别随机分配
                    gender = "男" if i % 2 == 0 else "女"
                    # 年龄随机分配（30-50岁）
                    age = 30 + (i % 21)
                    # 职称（高中教师职称：高级教师、一级教师、二级教师）
                    if i <= count // 3:
                        title = "高级教师"
                    elif i <= 2 * count // 3:
                        title = "一级教师"
                    else:
                        title = "二级教师"
                    # 部门（学科）
                    department = subject
                    # 联系方式（随机电话号码）
                    contact = generate_phone_number()
                    # 状态
                    status = "active"
                    # 创建时间
                    created_at = datetime.now()
                    updated_at = datetime.now()
                    
                    # 创建教师对象
                    teacher = Teacher(
                        teacher_id=teacher_id,
                        name=name,
                        gender=gender,
                        age=age,
                        title=title,
                        department=department,
                        contact=contact,
                        status=status,
                        created_at=created_at,
                        updated_at=updated_at
                    )
                    teachers.append(teacher)
                    # 存储到教师映射中，格式：{subject: {index: teacher}}
                    if subject not in teacher_map:
                        teacher_map[subject] = {}
                    teacher_map[subject][str(i)] = teacher
            
            # 批量添加教师
            db.session.add_all(teachers)
            db.session.commit()
            print(f"成功创建 {len(teachers)} 个教师")
            
            # 分配教师到班级
            print("开始分配教师到班级...")
            teacher_classes = []
            
            for grade, classes in TEACHER_ASSIGNMENT.items():
                for class_name, subjects in classes.items():
                    for subject, teacher_index in subjects.items():
                        # 获取对应的教师
                        if subject in teacher_map and teacher_index in teacher_map[subject]:
                            teacher = teacher_map[subject][teacher_index]
                            # 创建教师班级关联
                            teacher_class = TeacherClass(
                                teacher_id=teacher.teacher_id,
                                grade=grade,
                                class_=class_name
                            )
                            teacher_classes.append(teacher_class)
            
            # 批量添加教师班级关联
            db.session.add_all(teacher_classes)
            db.session.commit()
            print(f"成功分配 {len(teacher_classes)} 个教师班级关联")
            
            # 重新启用外键约束
            db.session.execute('PRAGMA foreign_keys = ON')
            
            # 验证外键约束状态
            result = db.session.execute('PRAGMA foreign_keys').fetchone()
            print(f"外键约束状态: {'启用' if result[0] else '未启用'}")
            
            # 验证数据完整性
            teacher_count = db.session.query(Teacher).count()
            teacher_class_count = db.session.query(TeacherClass).count()
            print(f"教师表记录数: {teacher_count}")
            print(f"教师班级表记录数: {teacher_class_count}")
            
            print("\n教师数据插入成功！")
            print("- 所有教师已按照表格要求分配到对应班级")
            print("- 教师职称只有高级教师、一级教师、二级教师")
            print("- 教师联系方式为随机生成的电话号码")
            return True
            
        except Exception as e:
            print(f"执行过程中发生错误: {str(e)}")
            db.session.rollback()
            # 确保外键约束重新启用
            db.session.execute('PRAGMA foreign_keys = ON')
            return False
        finally:
            db.session.close()

if __name__ == '__main__':
    success = main()
    if success:
        print("\n任务执行成功！")
    else:
        print("\n任务执行失败！")
        sys.exit(1)
