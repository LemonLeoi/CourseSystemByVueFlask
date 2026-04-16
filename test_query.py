import sqlite3
import os

# 连接数据库
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'data', 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 测试1: 查询高一1班的学生
print("测试1: 查询高一1班的学生")
cursor.execute("SELECT student_id, name FROM students WHERE grade='高一' AND class='1班'")
students = cursor.fetchall()
print(f"找到 {len(students)} 个学生")
for student in students:
    print(f"  - {student[0]}: {student[1]}")

# 测试2: 查询高一1班的成绩
print("\n测试2: 查询高一1班的成绩")
cursor.execute("""
    SELECT sg.student_id, sg.exam_code, sg.subject, sg.score, e.exam_name 
    FROM student_grades sg 
    JOIN exams e ON sg.exam_code = e.exam_code 
    JOIN students s ON sg.student_id = s.student_id 
    WHERE s.grade='高一' AND s.class='1班' 
    LIMIT 10
""")
grades = cursor.fetchall()
print(f"找到 {len(grades)} 条成绩记录")
for grade in grades:
    print(f"  - {grade[0]}: {grade[2]} = {grade[3]} (考试: {grade[4]})")

# 测试3: 查询STU20240004的成绩
print("\n测试3: 查询STU20240004的成绩")
cursor.execute("""
    SELECT sg.exam_code, sg.subject, sg.score, e.exam_name 
    FROM student_grades sg 
    JOIN exams e ON sg.exam_code = e.exam_code 
    WHERE sg.student_id='STU20240004' 
    LIMIT 10
""")
stu_grades = cursor.fetchall()
print(f"找到 {len(stu_grades)} 条成绩记录")
for grade in stu_grades:
    print(f"  - {grade[1]} = {grade[2]} (考试: {grade[3]})")

# 关闭连接
conn.close()
