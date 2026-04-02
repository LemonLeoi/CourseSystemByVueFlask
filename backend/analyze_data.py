import sqlite3
import pandas as pd
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'database.db')

# 连接数据库
conn = sqlite3.connect(DATABASE_PATH)

# 查看学生表数据
print("学生表数据:")
students_df = pd.read_sql_query("SELECT * FROM students LIMIT 10", conn)
print(students_df)
print()

# 查看成绩表数据
print("成绩表数据:")
grades_df = pd.read_sql_query("SELECT * FROM student_grades LIMIT 10", conn)
print(grades_df)
print()

# 查看课程表数据
print("课程表数据:")
courses_df = pd.read_sql_query("SELECT * FROM courses LIMIT 10", conn)
print(courses_df)
print()

# 查看考试表数据
print("考试表数据:")
exams_df = pd.read_sql_query("SELECT * FROM exams LIMIT 10", conn)
print(exams_df)
print()

# 统计数据量
print("数据量统计:")
tables = ['students', 'student_grades', 'courses', 'exams', 'teachers']
for table in tables:
    count = pd.read_sql_query(f"SELECT COUNT(*) as count FROM {table}", conn).iloc[0]['count']
    print(f"{table}: {count} 条记录")

# 关闭连接
conn.close()