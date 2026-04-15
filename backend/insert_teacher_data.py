import os
import sys
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime

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

# 班级配置
CLASSES = {
    '高一': ['1班', '2班', '3班', '4班', '5班', '6班'],
    '高二': ['1班', '2班', '3班', '4班', '5班', '6班'],
    '高三': ['1班', '2班', '3班', '4班', '5班', '6班']
}

# 高二高三科目配置
GRADE_SUBJECTS = {
    '高二': {
        '1班': ['语文', '数学', '英语', '物理', '化学', '生物'],
        '2班': ['语文', '数学', '英语', '物理', '化学', '生物'],
        '3班': ['语文', '数学', '英语', '物理', '化学', '地理'],
        '4班': ['语文', '数学', '英语', '物理', '化学', '地理'],
        '5班': ['语文', '数学', '英语', '历史', '政治', '地理'],
        '6班': ['语文', '数学', '英语', '历史', '政治', '地理']
    },
    '高三': {
        '1班': ['语文', '数学', '英语', '物理', '化学', '生物'],
        '2班': ['语文', '数学', '英语', '物理', '化学', '生物'],
        '3班': ['语文', '数学', '英语', '物理', '化学', '地理'],
        '4班': ['语文', '数学', '英语', '物理', '化学', '地理'],
        '5班': ['语文', '数学', '英语', '历史', '政治', '地理'],
        '6班': ['语文', '数学', '英语', '历史', '政治', '地理']
    }
}

# 高一所有班级都要九个科目
for class_name in CLASSES['高一']:
    GRADE_SUBJECTS['高一'] = {
        class_name: ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理']
        for class_name in CLASSES['高一']
    }

def generate_teacher_id(subject, index):
    """生成教师工号"""
    subject_code = SUBJECT_CODES[subject]
    return f"2024{subject_code}{index:02d}"

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
            for subject, count in TEACHER_COUNT.items():
                for i in range(1, count + 1):
                    teacher_id = generate_teacher_id(subject, i)
                    # 生成教师姓名（示例）
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
                    # 联系方式
                    contact = f"{teacher_id}@school.edu.cn"
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
            
            # 批量添加教师
            db.session.add_all(teachers)
            db.session.commit()
            print(f"成功创建 {len(teachers)} 个教师")
            
            # 按学科分组教师
            teachers_by_subject = {}
            for teacher in teachers:
                subject = teacher.department
                if subject not in teachers_by_subject:
                    teachers_by_subject[subject] = []
                teachers_by_subject[subject].append(teacher)
            
            # 分配教师到班级
            print("开始分配教师到班级...")
            teacher_classes = []
            for grade, classes in CLASSES.items():
                for class_name in classes:
                    # 获取该班级需要的科目
                    subjects = GRADE_SUBJECTS[grade][class_name]
                    for subject in subjects:
                        # 循环分配教师
                        if subject in teachers_by_subject and teachers_by_subject[subject]:
                            teacher = teachers_by_subject[subject].pop(0)
                            teachers_by_subject[subject].append(teacher)  # 循环使用
                            
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
            
            print("\n教师数据插入成功！")
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
