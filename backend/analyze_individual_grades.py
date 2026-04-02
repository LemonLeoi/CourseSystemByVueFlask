import sqlite3
import sys
import os

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'database.db')

# 从数据库获取学生个人成绩
def get_student_grades(student_id):
    # 连接数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 查询学生信息
    cursor.execute("SELECT name, gender, class, grade FROM students WHERE student_id = ?", (student_id,))
    student_info = cursor.fetchone()
    
    if not student_info:
        conn.close()
        return None, None
    
    # 查询学生成绩
    query = """
    SELECT g.exam_type, g.subject, g.score, g.grade_level
    FROM student_grades g
    WHERE g.student_id = ?
    ORDER BY g.exam_type, g.subject
    """
    
    cursor.execute(query, (student_id,))
    grades = cursor.fetchall()
    conn.close()
    
    return student_info, grades

# 获取班级平均成绩
def get_class_average(student_class, student_grade):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = """
    SELECT g.subject, AVG(g.score) as avg_score
    FROM student_grades g
    JOIN students s ON g.student_id = s.student_id
    WHERE s.class = ? AND s.grade = ?
    GROUP BY g.subject
    """
    
    cursor.execute(query, (student_class, student_grade))
    class_averages = cursor.fetchall()
    conn.close()
    
    # 转换为字典
    avg_dict = {}
    for subject, avg_score in class_averages:
        avg_dict[subject] = round(avg_score, 2)
    
    return avg_dict

# 分析学生成绩
def analyze_student_performance(student_id):
    print(f"正在分析学生 {student_id} 的成绩...")
    
    # 获取学生信息和成绩
    student_info, grades = get_student_grades(student_id)
    
    if not student_info:
        print(f"未找到学号为 {student_id} 的学生")
        return
    
    name, gender, student_class, student_grade = student_info
    print(f"\n学生信息:")
    print(f"姓名: {name}")
    print(f"性别: {gender}")
    print(f"班级: {student_grade}{student_class}")
    print(f"年级: {student_grade}")
    
    if not grades:
        print("\n该学生暂无成绩记录")
        return
    
    # 按考试类型和学科整理成绩
    exam_grades = {}
    for exam_type, subject, score, grade_level in grades:
        if exam_type not in exam_grades:
            exam_grades[exam_type] = {}
        exam_grades[exam_type][subject] = (score, grade_level)
    
    # 计算各学科平均成绩
    subject_averages = {}
    for exam_type, subjects in exam_grades.items():
        for subject, (score, _) in subjects.items():
            if subject not in subject_averages:
                subject_averages[subject] = []
            subject_averages[subject].append(score)
    
    # 计算平均值
    for subject, scores in subject_averages.items():
        subject_averages[subject] = round(sum(scores) / len(scores), 2)
    
    # 获取班级平均成绩
    class_averages = get_class_average(student_class, student_grade)
    
    # 分析学科强弱项
    strengths = []
    weaknesses = []
    for subject, avg_score in subject_averages.items():
        if subject in class_averages:
            if avg_score > class_averages[subject]:
                strengths.append((subject, avg_score, class_averages[subject]))
            else:
                weaknesses.append((subject, avg_score, class_averages[subject]))
    
    # 按成绩差异排序
    strengths.sort(key=lambda x: x[1] - x[2], reverse=True)
    weaknesses.sort(key=lambda x: x[2] - x[1], reverse=True)
    
    # 输出分析结果
    print("\n成绩分析:")
    
    # 各考试类型成绩
    for exam_type, subjects in exam_grades.items():
        print(f"\n{exam_type}:")
        print("-" * 40)
        print("学科\t\t分数\t等级")
        print("-" * 40)
        for subject, (score, grade_level) in subjects.items():
            print(f"{subject}\t\t{score}\t{grade_level}")
    
    # 学科平均成绩
    print("\n学科平均成绩:")
    print("-" * 50)
    print("学科\t\t个人平均\t班级平均\t差异")
    print("-" * 50)
    for subject, avg_score in subject_averages.items():
        class_avg = class_averages.get(subject, 0)
        diff = round(avg_score - class_avg, 2)
        print(f"{subject}\t\t{avg_score}\t\t{class_avg}\t\t{diff:+}")
    
    # 学科强弱项
    print("\n学科强项:")
    print("-" * 50)
    if strengths:
        for subject, avg_score, class_avg in strengths[:3]:  # 显示前3个强项
            diff = round(avg_score - class_avg, 2)
            print(f"{subject}: {avg_score} (班级平均: {class_avg}, +{diff})")
    else:
        print("暂无明显强项")
    
    print("\n学科弱项:")
    print("-" * 50)
    if weaknesses:
        for subject, avg_score, class_avg in weaknesses[:3]:  # 显示前3个弱项
            diff = round(class_avg - avg_score, 2)
            print(f"{subject}: {avg_score} (班级平均: {class_avg}, -{diff})")
    else:
        print("暂无明显弱项")
    
    # 整体表现评估
    overall_avg = round(sum(subject_averages.values()) / len(subject_averages), 2)
    class_overall_avg = round(sum(class_averages.values()) / len(class_averages), 2) if class_averages else 0
    overall_diff = round(overall_avg - class_overall_avg, 2)
    
    print("\n整体表现:")
    print("-" * 50)
    print(f"个人平均成绩: {overall_avg}")
    print(f"班级平均成绩: {class_overall_avg}")
    print(f"与班级平均差异: {overall_diff:+}")
    
    if overall_diff > 10:
        print("评估: 优秀，明显高于班级平均水平")
    elif overall_diff > 0:
        print("评估: 良好，高于班级平均水平")
    elif overall_diff > -10:
        print("评估: 中等，接近班级平均水平")
    else:
        print("评估: 需要提高，低于班级平均水平")

# 主函数
def main():
    print("学生个人成绩分析系统")
    print("=" * 50)
    
    # 示例学生ID列表
    print("示例学生ID:")
    print("STU20240001, STU20240002, STU20240003, STU20240004, STU20240005")
    print()
    
    # 输入学生ID
    student_id = input("请输入学生学号: ").strip()
    
    if not student_id:
        print("学号不能为空")
        return
    
    analyze_student_performance(student_id)

if __name__ == "__main__":
    main()