import os
import sys
from flask import Flask
from dotenv import load_dotenv

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

def clean_teacher_data():
    """清理教师相关数据"""
    with app.app_context():
        try:
            print("开始清理教师相关数据...")
            
            # 暂时禁用外键约束（SQLite特定）
            db.session.execute('PRAGMA foreign_keys = OFF')
            
            # 按照依赖关系顺序删除数据
            # 1. 删除教师课程表数据
            print("删除教师课程表数据...")
            db.session.query(TeacherCourse).delete()
            db.session.commit()
            print("教师课程表数据删除成功")
            
            # 2. 删除教师任教班级表数据
            print("删除教师任教班级表数据...")
            db.session.query(TeacherClass).delete()
            db.session.commit()
            print("教师任教班级表数据删除成功")
            
            # 3. 删除班主任表数据
            print("删除班主任表数据...")
            db.session.query(HomeroomTeacher).delete()
            db.session.commit()
            print("班主任表数据删除成功")
            
            # 4. 删除教师表数据
            print("删除教师表数据...")
            db.session.query(Teacher).delete()
            db.session.commit()
            print("教师表数据删除成功")
            
            # 重新启用外键约束
            db.session.execute('PRAGMA foreign_keys = ON')
            
            print("\n数据清理完成！")
            print("所有教师相关表的数据已被清除。")
            print("表结构、字段属性、约束条件及索引配置保持不变。")
            
        except Exception as e:
            print(f"清理过程中发生错误: {str(e)}")
            db.session.rollback()
            # 确保外键约束重新启用
            db.session.execute('PRAGMA foreign_keys = ON')
            return False
        finally:
            db.session.close()
    return True

if __name__ == '__main__':
    success = clean_teacher_data()
    if success:
        print("\n数据清理操作执行成功！")
    else:
        print("\n数据清理操作执行失败！")
        sys.exit(1)
