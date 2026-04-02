# Grade analysis core logic
from ..data_access.grade_data_access import GradeDataAccess

# 分析学生成绩
def analyze_student_performance(student_id):
    # 获取学生信息和成绩
    student_info, grades = GradeDataAccess.get_student_grades(student_id)
    
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
    
    # 按考试名称和学科整理成绩
    exam_grades = {}
    for exam_name, academic_year, semester, grade, exam_type, subject, score, grade_level in grades:
        if exam_name not in exam_grades:
            exam_grades[exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'grade': grade,
                'exam_type': exam_type,
                'subjects': {}
            }
        exam_grades[exam_name]['subjects'][subject] = (score, grade_level)
    
    # 计算各学科平均成绩
    subject_averages = {}
    for exam_data in exam_grades.values():
        for subject, (score, _) in exam_data['subjects'].items():
            if subject not in subject_averages:
                subject_averages[subject] = []
            subject_averages[subject].append(score)
    
    # 计算平均值
    for subject, scores in subject_averages.items():
        subject_averages[subject] = round(sum(scores) / len(scores), 2)
    
    # 获取班级平均成绩
    class_averages = GradeDataAccess.get_class_average(student_class, student_grade)
    
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
    # 处理班级格式，确保与数据库匹配
    # 如果class_name是数字，添加"班"字
    if class_name.isdigit():
        class_name = f"{class_name}班"
    
    # 查询班级学生
    students = GradeDataAccess.get_class_students(class_name, grade)
    
    if not students:
        return {"error": f"未找到 {grade}{class_name} 班级的学生"}
    
    # 查询班级所有成绩
    grades = GradeDataAccess.get_class_grades(class_name, grade)
    
    # 整理成绩数据
    student_grades = {}
    for student_id, exam_name, academic_year, semester, exam_type, subject, score, grade_level in grades:
        if student_id not in student_grades:
            student_grades[student_id] = {}
        if exam_name not in student_grades[student_id]:
            student_grades[student_id][exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'exam_type': exam_type,
                'subjects': {}
            }
        student_grades[student_id][exam_name]['subjects'][subject] = (score, grade_level)
    
    # 计算班级学科平均
    class_subject_avgs = {}
    for student_id, exam_data in student_grades.items():
        for exam_info in exam_data.values():
            for subject, (score, _) in exam_info['subjects'].items():
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
    # 查询年级所有班级
    classes = GradeDataAccess.get_grade_classes(grade)
    
    if not classes:
        return {"error": f"未找到 {grade} 年级的班级"}
    
    # 查询年级所有成绩
    grades = GradeDataAccess.get_grade_grades(grade)
    
    # 整理成绩数据
    class_grades = {}
    for class_name, exam_name, academic_year, semester, exam_type, subject, score, grade_level in grades:
        if class_name not in class_grades:
            class_grades[class_name] = {}
        if exam_name not in class_grades[class_name]:
            class_grades[class_name][exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'exam_type': exam_type,
                'subjects': {}
            }
        if subject not in class_grades[class_name][exam_name]['subjects']:
            class_grades[class_name][exam_name]['subjects'][subject] = []
        class_grades[class_name][exam_name]['subjects'][subject].append(score)
    
    # 计算各班级学科平均
    class_subject_avgs = {}
    for class_name, exam_data in class_grades.items():
        class_subject_avgs[class_name] = {}
        for exam_info in exam_data.values():
            for subject, scores in exam_info['subjects'].items():
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