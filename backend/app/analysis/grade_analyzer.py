# Grade analysis core logic
import sqlite3
import os

# 从数据库获取学生个人成绩
def get_student_grades(student_id):
    # 连接数据库
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
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
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
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
    # 获取学生信息和成绩
    student_info, grades = get_student_grades(student_id)
    
    if not student_info:
        return {"error": f"未找到学号为 {student_id} 的学生"}
    
    name, gender, student_class, student_grade = student_info
    
    if not grades:
        return {
            "student_info": {
                "name": name,
                "gender": gender,
                "class": f"{student_grade}{student_class}",
                "grade": student_grade
            },
            "error": "该学生暂无成绩记录"
        }
    
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
    
    # 整体表现评估
    overall_avg = round(sum(subject_averages.values()) / len(subject_averages), 2)
    class_overall_avg = round(sum(class_averages.values()) / len(class_averages), 2) if class_averages else 0
    overall_diff = round(overall_avg - class_overall_avg, 2)
    
    # 生成评估
    evaluation = ""
    if overall_diff > 10:
        evaluation = "优秀，明显高于班级平均水平"
    elif overall_diff > 0:
        evaluation = "良好，高于班级平均水平"
    elif overall_diff > -10:
        evaluation = "中等，接近班级平均水平"
    else:
        evaluation = "需要提高，低于班级平均水平"
    
    # 构建结果
    result = {
        "student_info": {
            "name": name,
            "gender": gender,
            "class": f"{student_grade}{student_class}",
            "grade": student_grade
        },
        "exam_grades": exam_grades,
        "subject_averages": subject_averages,
        "class_averages": class_averages,
        "strengths": [{
            "subject": s[0],
            "avg_score": s[1],
            "class_avg": s[2],
            "diff": round(s[1] - s[2], 2)
        } for s in strengths[:3]],
        "weaknesses": [{
            "subject": w[0],
            "avg_score": w[1],
            "class_avg": w[2],
            "diff": round(w[2] - w[1], 2)
        } for w in weaknesses[:3]],
        "overall": {
            "personal_avg": overall_avg,
            "class_avg": class_overall_avg,
            "diff": overall_diff,
            "evaluation": evaluation
        }
    }
    
    return result

# 分析班级成绩
def analyze_class_performance(class_name, grade):
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
    cursor = conn.cursor()
    
    # 查询班级学生
    cursor.execute("SELECT student_id, name FROM students WHERE class = ? AND grade = ?", (class_name, grade))
    students = cursor.fetchall()
    
    if not students:
        conn.close()
        return {"error": f"未找到 {grade}{class_name} 班级的学生"}
    
    # 查询班级所有成绩
    query = """
    SELECT g.student_id, g.exam_type, g.subject, g.score, g.grade_level
    FROM student_grades g
    JOIN students s ON g.student_id = s.student_id
    WHERE s.class = ? AND s.grade = ?
    ORDER BY g.student_id, g.exam_type, g.subject
    """
    
    cursor.execute(query, (class_name, grade))
    grades = cursor.fetchall()
    conn.close()
    
    # 整理成绩数据
    student_grades = {}
    for student_id, exam_type, subject, score, grade_level in grades:
        if student_id not in student_grades:
            student_grades[student_id] = {}
        if exam_type not in student_grades[student_id]:
            student_grades[student_id][exam_type] = {}
        student_grades[student_id][exam_type][subject] = (score, grade_level)
    
    # 计算班级学科平均
    class_subject_avgs = {}
    for student_id, exam_data in student_grades.items():
        for exam_type, subjects in exam_data.items():
            for subject, (score, _) in subjects.items():
                if subject not in class_subject_avgs:
                    class_subject_avgs[subject] = []
                class_subject_avgs[subject].append(score)
    
    for subject, scores in class_subject_avgs.items():
        class_subject_avgs[subject] = round(sum(scores) / len(scores), 2)
    
    # 计算班级整体平均
    all_scores = []
    for subject, scores in class_subject_avgs.items():
        all_scores.append(scores)
    class_overall_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 构建结果
    result = {
        "class_info": {
            "class_name": f"{grade}{class_name}",
            "grade": grade,
            "student_count": len(students)
        },
        "subject_averages": class_subject_avgs,
        "overall_average": class_overall_avg,
        "student_count": len(students)
    }
    
    return result

# 分析年级成绩
def analyze_grade_performance(grade):
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
    cursor = conn.cursor()
    
    # 查询年级所有班级
    cursor.execute("SELECT DISTINCT class FROM students WHERE grade = ?", (grade,))
    classes = cursor.fetchall()
    
    if not classes:
        conn.close()
        return {"error": f"未找到 {grade} 年级的班级"}
    
    # 查询年级所有成绩
    query = """
    SELECT s.class, g.exam_type, g.subject, g.score, g.grade_level
    FROM student_grades g
    JOIN students s ON g.student_id = s.student_id
    WHERE s.grade = ?
    ORDER BY s.class, g.exam_type, g.subject
    """
    
    cursor.execute(query, (grade,))
    grades = cursor.fetchall()
    conn.close()
    
    # 整理成绩数据
    class_grades = {}
    for class_name, exam_type, subject, score, grade_level in grades:
        if class_name not in class_grades:
            class_grades[class_name] = {}
        if exam_type not in class_grades[class_name]:
            class_grades[class_name][exam_type] = {}
        if subject not in class_grades[class_name][exam_type]:
            class_grades[class_name][exam_type][subject] = []
        class_grades[class_name][exam_type][subject].append(score)
    
    # 计算各班级学科平均
    class_subject_avgs = {}
    for class_name, exam_data in class_grades.items():
        class_subject_avgs[class_name] = {}
        for exam_type, subjects in exam_data.items():
            for subject, scores in subjects.items():
                if subject not in class_subject_avgs[class_name]:
                    class_subject_avgs[class_name][subject] = []
                class_subject_avgs[class_name][subject].extend(scores)
    
    for class_name, subjects in class_subject_avgs.items():
        for subject, scores in subjects.items():
            class_subject_avgs[class_name][subject] = round(sum(scores) / len(scores), 2)
    
    # 计算年级学科平均
    grade_subject_avgs = {}
    for class_name, subjects in class_subject_avgs.items():
        for subject, avg_score in subjects.items():
            if subject not in grade_subject_avgs:
                grade_subject_avgs[subject] = []
            grade_subject_avgs[subject].append(avg_score)
    
    for subject, scores in grade_subject_avgs.items():
        grade_subject_avgs[subject] = round(sum(scores) / len(scores), 2)
    
    # 计算年级整体平均
    all_scores = []
    for subject, scores in grade_subject_avgs.items():
        all_scores.append(scores)
    grade_overall_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 构建结果
    result = {
        "grade_info": {
            "grade": grade,
            "class_count": len(classes)
        },
        "class_averages": class_subject_avgs,
        "subject_averages": grade_subject_avgs,
        "overall_average": grade_overall_avg
    }
    
    return result