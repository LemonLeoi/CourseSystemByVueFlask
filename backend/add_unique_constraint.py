import sys
import os
import sqlite3

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 数据库路径
database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'database.db')

print("开始为grade表添加唯一约束...")
print("-" * 100)

# 连接到SQLite数据库
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# 检查是否已经存在唯一约束
try:
    # 尝试添加唯一约束
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS _student_subject_exam_uc
        ON student_grades (student_id, subject, exam_type)
    ''')
    conn.commit()
    print("成功添加唯一约束")
except sqlite3.Error as e:
    print(f"添加唯一约束时出错: {e}")

# 验证唯一约束是否存在
cursor.execute('''
    PRAGMA index_list(student_grades)
''')
indexes = cursor.fetchall()
print("\n表中的索引:")
for index in indexes:
    print(f"- {index[1]}")

# 关闭连接
conn.close()

print("-" * 100)
print("操作完成")
