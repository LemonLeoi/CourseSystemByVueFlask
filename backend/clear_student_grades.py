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
from app.models.grade import Grade

# 初始化数据库
db.init_app(app)

def clear_student_grades():
    """清空student_grades表数据"""
    with app.app_context():
        try:
            print("开始清空student_grades表数据...")

            # 1. 临时禁用外键约束（SQLite特定）
            print("临时禁用外键约束...")
            db.session.execute('PRAGMA foreign_keys = OFF')

            # 2. 删除student_grades表数据
            print("删除student_grades表数据...")
            db.session.query(Grade).delete()

            # 提交删除操作
            db.session.commit()
            print("数据删除成功")

            # 3. 重新启用外键约束
            print("重新启用外键约束...")
            db.session.execute('PRAGMA foreign_keys = ON')

            # 4. 验证外键约束是否正确启用
            print("验证外键约束状态...")
            result = db.session.execute('PRAGMA foreign_keys').fetchone()
            print(f"外键约束状态: {'启用' if result[0] else '未启用'}")

            # 5. 验证数据删除的完整性
            student_grades_count = db.session.query(Grade).count()
            print(f"student_grades表剩余记录数: {student_grades_count}")

            if student_grades_count == 0:
                print("\n操作成功！")
                print("- student_grades表已成功清空")
                print("- 外键约束已正确恢复")
                print("- 数据删除完整性验证通过")
                return True
            else:
                print("\n操作失败！")
                print("- 数据删除不完整")
                return False

        except Exception as e:
            print(f"执行过程中发生错误: {str(e)}")
            db.session.rollback()
            # 确保外键约束重新启用
            db.session.execute('PRAGMA foreign_keys = ON')
            return False
        finally:
            db.session.close()

def main():
    """主函数"""
    success = clear_student_grades()
    if success:
        print("\n数据库操作流程执行成功！")
    else:
        print("\n数据库操作流程执行失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
