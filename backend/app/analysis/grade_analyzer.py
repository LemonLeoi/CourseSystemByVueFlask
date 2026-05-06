# Grade analysis core logic
from ..data_access.grade_data_access import GradeDataAccess
from .statistical_analysis import calculate_average, calculate_std_deviation, calculate_median, calculate_min_max, calculate_score_distribution
from .analysis_explainer import explainer
from .analysis_logger import logger

# 分析学生成绩
def analyze_student_performance(student_id, analysis_id=None):
    # 记录分析开始
    if analysis_id:
        logger.log('personal', 'analysis_start', f'开始分析学生 {student_id} 的成绩', {'student_id': student_id})
    
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
    
    # 记录数据获取完成
    if analysis_id:
        logger.log('personal', 'data_retrieval', f'获取到学生 {name} 的 {len(grades)} 条成绩记录', {'student_id': student_id, 'record_count': len(grades)})
    
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
    
    # 记录数据整理完成
    if analysis_id:
        logger.log('personal', 'data_preprocessing', f'整理完成 {len(exam_grades)} 次考试的成绩数据', {'exam_count': len(exam_grades)})
    
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
    
    # 记录学科平均计算完成
    if analysis_id:
        logger.log('personal', 'statistical_analysis', f'计算完成 {len(subject_averages)} 个学科的平均成绩', {'subject_count': len(subject_averages)})
    
    # 获取班级平均成绩
    class_averages = GradeDataAccess.get_class_average(student_class, student_grade)
    
    # 分析学科强弱项
    strengths = []
    weaknesses = []
    for subject, avg_score in subject_averages.items():
        if subject in class_averages:
            if avg_score > class_averages[subject]:
                strengths.append((subject, avg_score, class_averages[subject]))
            elif avg_score < class_averages[subject]:
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
    
    # 生成分析解释
    explanations = {}
    
    # 分析步骤解释
    analysis_steps = [
        {
            'name': '数据获取',
            'purpose': '从数据库中提取学生的基本信息和成绩记录',
            'method': '通过GradeDataAccess.get_student_grades获取学生成绩数据'
        },
        {
            'name': '数据整理',
            'purpose': '按考试和学科整理成绩数据',
            'method': '将成绩按考试名称分组，记录每个考试的学科成绩'
        },
        {
            'name': '统计分析',
            'purpose': '计算学科平均成绩和整体平均成绩',
            'method': '使用算术平均值计算各学科和整体的平均成绩'
        },
        {
            'name': '比较分析',
            'purpose': '与班级平均成绩比较，分析强弱项',
            'method': '将学生成绩与班级平均成绩对比，识别优势和劣势学科'
        },
        {
            'name': '综合评估',
            'purpose': '生成整体表现评估',
            'method': '基于与班级平均成绩的差异程度，给出相应的评估等级'
        }
    ]
    explanations['analysis_steps'] = explainer.explain_analysis_steps('个人成绩分析', analysis_steps)
    
    # 统计方法解释
    explanations['statistical_methods'] = {
        'average': explainer.explain_statistical_methods('average', list(subject_averages.values())),
        'comparison': '本分析通过将学生成绩与班级平均成绩进行对比，识别学生的优势和劣势学科。比较的理论依据是：当学生某学科成绩高于班级平均水平时，说明该学生在该学科上表现较好；反之，则需要加强。'
    }
    
    # 结果解释
    explanations['result_interpretation'] = {
        'strengths': '优势学科是指学生成绩明显高于班级平均水平的学科，这些学科是学生的特长领域，建议继续保持和发展。',
        'weaknesses': '劣势学科是指学生成绩低于班级平均水平的学科，这些学科需要重点关注和加强，建议制定针对性的学习计划。',
        'overall_evaluation': f'学生整体表现{evaluation}。{"继续保持优良的学习状态，争取更大的进步。" if overall_diff > 0 else "需要更加努力，制定合理的学习计划，逐步提高成绩。"}'
    }
    
    # 记录分析完成
    if analysis_id:
        logger.log('personal', 'analysis_complete', '学生成绩分析完成', {'student_id': student_id, 'evaluation': evaluation})
    
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
        },
        "explanations": explanations
    }
    
    return result

# 分析班级成绩
def analyze_class_performance(class_name, grade, analysis_id=None):
    # 记录分析开始
    if analysis_id:
        logger.log('class', 'analysis_start', f'开始分析班级 {grade}{class_name} 的成绩', {'class_name': class_name, 'grade': grade})
    
    # 直接使用传入的班级名称和年级进行查询
    
    # 查询班级所有成绩
    grades = GradeDataAccess.get_class_grades(class_name, grade)
    
    # 如果没有成绩记录，返回班级信息和错误消息
    if not grades:
        # 直接查询学生表
        from app.models import Student
        from app import db
        students = Student.query.filter_by(class_=class_name, grade=grade).all()
        student_count = len(students)
        return {
            "class_info": {
                "class_name": f"{grade}{class_name}",
                "grade": grade,
                "student_count": student_count
            },
            "error": f"{grade}{class_name} 班级暂无成绩记录，学生数量: {student_count}"
        }
    
    # 记录数据获取完成
    if analysis_id:
        logger.log('class', 'data_retrieval', f'获取到班级 {grade}{class_name} 的 {len(grades)} 条成绩记录', {'class_name': class_name, 'grade': grade, 'record_count': len(grades)})
    
    # 从成绩记录中提取学生ID，获取学生列表
    student_ids = set()
    for student_id, _, _, _, _, _, _, _ in grades:
        student_ids.add(student_id)
    students = [(student_id, "") for student_id in student_ids]
    
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
    
    # 记录数据整理完成
    if analysis_id:
        logger.log('class', 'data_preprocessing', f'整理完成班级 {grade}{class_name} 的成绩数据，涉及 {len(student_grades)} 名学生', {'class_name': class_name, 'grade': grade, 'student_count': len(student_grades)})
    
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
    
    # 记录学科平均计算完成
    if analysis_id:
        logger.log('class', 'statistical_analysis', f'计算完成班级 {grade}{class_name} 的 {len(class_subject_avgs)} 个学科的平均成绩', {'class_name': class_name, 'grade': grade, 'subject_count': len(class_subject_avgs)})
    
    # 计算班级整体平均
    all_scores = []
    for subject, scores in class_subject_avgs.items():
        all_scores.append(scores)
    class_overall_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 生成分析解释
    explanations = {}
    
    # 分析步骤解释
    analysis_steps = [
        {
            'name': '数据获取',
            'purpose': '从数据库中提取班级的成绩记录',
            'method': '通过GradeDataAccess.get_class_grades获取班级成绩数据'
        },
        {
            'name': '数据整理',
            'purpose': '按学生和考试整理成绩数据',
            'method': '将成绩按学生ID和考试名称分组，记录每个学生的考试成绩'
        },
        {
            'name': '统计分析',
            'purpose': '计算班级各学科平均成绩和整体平均成绩',
            'method': '使用算术平均值计算各学科和整体的平均成绩'
        }
    ]
    explanations['analysis_steps'] = explainer.explain_analysis_steps('班级成绩分析', analysis_steps)
    
    # 统计方法解释
    explanations['statistical_methods'] = {
        'average': explainer.explain_statistical_methods('average', list(class_subject_avgs.values())),
        'class_performance': '班级整体平均成绩反映了班级的整体学习水平，学科平均成绩反映了班级在各学科上的表现情况。通过分析班级成绩，可以了解班级的优势和劣势学科，为教学改进提供依据。'
    }
    
    # 结果解释
    explanations['result_interpretation'] = {
        'subject_averages': '各学科的平均成绩反映了班级在该学科上的整体表现，可与年级平均成绩对比，识别班级的优势和劣势学科。',
        'overall_average': f'班级整体平均成绩为 {class_overall_avg}，这是班级所有学科平均成绩的平均值，反映了班级的整体学习水平。'
    }
    
    # 记录分析完成
    if analysis_id:
        logger.log('class', 'analysis_complete', '班级成绩分析完成', {'class_name': class_name, 'grade': grade, 'overall_average': class_overall_avg})
    
    # 构建结果
    result = {
        "class_info": {
            "class_name": f"{grade}{class_name}",
            "grade": grade,
            "student_count": len(students)
        },
        "subject_averages": class_subject_avgs,
        "overall_average": class_overall_avg,
        "student_count": len(students),
        "explanations": explanations
    }
    
    return result

# 分析年级成绩
def analyze_grade_performance(grade, analysis_id=None):
    # 记录分析开始
    if analysis_id:
        logger.log('grade', 'analysis_start', f'开始分析年级 {grade} 的成绩', {'grade': grade})
    
    # 查询年级所有班级
    classes = GradeDataAccess.get_grade_classes(grade)
    
    if not classes:
        return {"error": f"未找到 {grade} 年级的班级"}
    
    # 记录班级获取完成
    if analysis_id:
        logger.log('grade', 'data_retrieval', f'获取到年级 {grade} 的 {len(classes)} 个班级', {'grade': grade, 'class_count': len(classes)})
    
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
    
    # 记录数据整理完成
    if analysis_id:
        logger.log('grade', 'data_preprocessing', f'整理完成年级 {grade} 的成绩数据，涉及 {len(class_grades)} 个班级', {'grade': grade, 'class_count': len(class_grades)})
    
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
    
    # 记录班级学科平均计算完成
    if analysis_id:
        logger.log('grade', 'statistical_analysis', f'计算完成年级 {grade} 各班级的学科平均成绩', {'grade': grade})
    
    # 计算年级学科平均
    grade_subject_avgs = {}
    for class_name, subjects in class_subject_avgs.items():
        for subject, avg_score in subjects.items():
            if subject not in grade_subject_avgs:
                grade_subject_avgs[subject] = []
            grade_subject_avgs[subject].append(avg_score)
    
    for subject, scores in grade_subject_avgs.items():
        grade_subject_avgs[subject] = round(sum(scores) / len(scores), 2)
    
    # 记录年级学科平均计算完成
    if analysis_id:
        logger.log('grade', 'statistical_analysis', f'计算完成年级 {grade} 的 {len(grade_subject_avgs)} 个学科的平均成绩', {'grade': grade, 'subject_count': len(grade_subject_avgs)})
    
    # 计算年级整体平均
    all_scores = []
    for subject, scores in grade_subject_avgs.items():
        all_scores.append(scores)
    grade_overall_avg = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 生成分析解释
    explanations = {}
    
    # 分析步骤解释
    analysis_steps = [
        {
            'name': '数据获取',
            'purpose': '从数据库中提取年级的班级信息和成绩记录',
            'method': '通过GradeDataAccess.get_grade_classes和GradeDataAccess.get_grade_grades获取数据'
        },
        {
            'name': '数据整理',
            'purpose': '按班级和考试整理成绩数据',
            'method': '将成绩按班级名称和考试名称分组，记录每个班级的考试成绩'
        },
        {
            'name': '统计分析',
            'purpose': '计算各班级学科平均成绩、年级学科平均成绩和年级整体平均成绩',
            'method': '使用算术平均值计算各层次的平均成绩'
        }
    ]
    explanations['analysis_steps'] = explainer.explain_analysis_steps('年级成绩分析', analysis_steps)
    
    # 统计方法解释
    explanations['statistical_methods'] = {
        'average': explainer.explain_statistical_methods('average', list(grade_subject_avgs.values())),
        'grade_performance': '年级整体平均成绩反映了年级的整体学习水平，学科平均成绩反映了年级在各学科上的表现情况。通过分析年级成绩，可以了解年级的优势和劣势学科，为教学改进提供依据。'
    }
    
    # 结果解释
    explanations['result_interpretation'] = {
        'class_averages': '各班级的学科平均成绩反映了班级的学习水平，可用于班级间的比较，识别优秀班级和需要改进的班级。',
        'subject_averages': '年级各学科的平均成绩反映了年级在该学科上的整体表现，可与其他年级对比，识别年级的优势和劣势学科。',
        'overall_average': f'年级整体平均成绩为 {grade_overall_avg}，这是年级所有学科平均成绩的平均值，反映了年级的整体学习水平。'
    }
    
    # 记录分析完成
    if analysis_id:
        logger.log('grade', 'analysis_complete', '年级成绩分析完成', {'grade': grade, 'overall_average': grade_overall_avg})
    
    # 构建结果
    result = {
        "grade_info": {
            "grade": grade,
            "class_count": len(classes)
        },
        "class_averages": class_subject_avgs,
        "subject_averages": grade_subject_avgs,
        "overall_average": grade_overall_avg,
        "explanations": explanations
    }
    
    return result

# 分析学生科目成绩
def analyze_student_subject(student_id, subject):
    # 获取学生信息和成绩
    student_info, grades = GradeDataAccess.get_student_grades(student_id)
    
    if not student_info:
        return {"error": f"未找到学号为 {student_id} 的学生"}
    
    name, gender, student_class, student_grade = student_info
    
    # 过滤指定科目的成绩
    subject_grades = []
    exam_names = []
    for exam_name, academic_year, semester, grade, exam_type, subj, score, grade_level in grades:
        if subj == subject:
            subject_grades.append(score)
            exam_names.append(exam_name)
    
    if not subject_grades:
        return {
            "student_info": {
                "name": name,
                "gender": gender,
                "class": f"{student_grade}{student_class}",
                "grade": student_grade
            },
            "error": f"该学生暂无{subject}科目成绩记录"
        }
    
    # 计算统计指标
    avg = calculate_average(subject_grades)
    std_dev = calculate_std_deviation(subject_grades)
    median = calculate_median(subject_grades)
    min_score, max_score = calculate_min_max(subject_grades)
    distribution = calculate_score_distribution(subject_grades)
    
    # 获取班级该科目平均成绩
    class_averages = GradeDataAccess.get_class_average(student_class, student_grade)
    class_subject_avg = class_averages.get(subject, 0)
    
    # 构建结果
    result = {
        "student_info": {
            "name": name,
            "gender": gender,
            "class": f"{student_grade}{student_class}",
            "grade": student_grade
        },
        "subject": subject,
        "statistics": {
            "average": avg,
            "std_deviation": std_dev,
            "median": median,
            "min_score": min_score,
            "max_score": max_score,
            "distribution": distribution
        },
        "class_average": class_subject_avg,
        "exam_grades": {
            "exam_names": exam_names,
            "scores": subject_grades
        }
    }
    
    return result

# 分析班级科目成绩
def analyze_class_subject(class_name, grade, subject):
    # 处理班级格式
    if class_name.isdigit():
        class_name = f"{class_name}班"
    
    # 查询班级学生
    students = GradeDataAccess.get_class_students(class_name, grade)
    
    if not students:
        return {"error": f"未找到 {grade}{class_name} 班级的学生"}
    
    # 查询班级该科目成绩
    grades = GradeDataAccess.get_class_subject_grades(class_name, grade, subject)
    
    if not grades:
        return {"error": f"{grade}{class_name} 班级暂无{subject}科目成绩记录"}
    
    # 整理成绩数据
    student_scores = {}
    all_scores = []
    for student_id, student_name, score in grades:
        student_scores[student_id] = {
            "name": student_name,
            "score": score
        }
        all_scores.append(score)
    
    # 计算统计指标
    avg = calculate_average(all_scores)
    std_dev = calculate_std_deviation(all_scores)
    median = calculate_median(all_scores)
    min_score, max_score = calculate_min_max(all_scores)
    distribution = calculate_score_distribution(all_scores)
    
    # 构建结果
    result = {
        "class_info": {
            "class_name": f"{grade}{class_name}",
            "grade": grade,
            "student_count": len(students)
        },
        "subject": subject,
        "statistics": {
            "average": avg,
            "std_deviation": std_dev,
            "median": median,
            "min_score": min_score,
            "max_score": max_score,
            "distribution": distribution
        },
        "student_scores": student_scores
    }
    
    return result

# 分析年级科目成绩
def analyze_grade_subject(grade, subject):
    # 查询年级所有班级
    classes = GradeDataAccess.get_grade_classes(grade)
    
    if not classes:
        return {"error": f"未找到 {grade} 年级的班级"}
    
    # 查询年级该科目成绩
    grades = GradeDataAccess.get_grade_subject_grades(grade, subject)
    
    if not grades:
        return {"error": f"{grade} 年级暂无{subject}科目成绩记录"}
    
    # 整理成绩数据
    class_scores = {}
    all_scores = []
    for class_name, score in grades:
        if class_name not in class_scores:
            class_scores[class_name] = []
        class_scores[class_name].append(score)
        all_scores.append(score)
    
    # 计算各班级平均
    class_avgs = {}
    for class_name, scores in class_scores.items():
        class_avgs[class_name] = round(sum(scores) / len(scores), 2)
    
    # 计算统计指标
    avg = calculate_average(all_scores)
    std_dev = calculate_std_deviation(all_scores)
    median = calculate_median(all_scores)
    min_score, max_score = calculate_min_max(all_scores)
    distribution = calculate_score_distribution(all_scores)
    
    # 构建结果
    result = {
        "grade_info": {
            "grade": grade,
            "class_count": len(classes)
        },
        "subject": subject,
        "statistics": {
            "average": avg,
            "std_deviation": std_dev,
            "median": median,
            "min_score": min_score,
            "max_score": max_score,
            "distribution": distribution
        },
        "class_averages": class_avgs
    }
    
    return result

# 分析学生考试趋势
def analyze_student_trend(student_id, subject=None, exam_code=None):
    """
    分析学生考试趋势
    
    Args:
        student_id: 学生ID
        subject: 学科名称（可选），为None或'all'时表示全科分析，为具体学科时表示单科分析
        exam_code: 考试代码（可选），为None或'all'时表示所有考试，为具体考试代码时表示特定考试
    
    Returns:
        dict: 包含学生信息和考试趋势数据
    """
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
    
    # 过滤指定考试（如果提供了exam_code参数且不是'all'）
    if exam_code and exam_code != 'all':
        grades = [g for g in grades if g[1] == exam_code]
        if not grades:
            return {
                "student_info": {
                    "name": name,
                    "gender": gender,
                    "class": f"{student_grade}{student_class}",
                    "grade": student_grade
                },
                "error": f"该学生在考试{exam_code}中暂无成绩记录"
            }
    
    # 过滤指定学科（如果提供了subject参数且不是'all'）
    if subject and subject != 'all':
        grades = [g for g in grades if g[5] == subject]
        if not grades:
            return {
                "student_info": {
                    "name": name,
                    "gender": gender,
                    "class": f"{student_grade}{student_class}",
                    "grade": student_grade
                },
                "error": f"该学生在{subject}科目暂无成绩记录"
            }
    
    # 按考试整理成绩
    exam_grades = {}
    all_subjects = set()
    
    for exam_name, academic_year, semester, grade, exam_type, subj, score, grade_level in grades:
        if exam_name not in exam_grades:
            exam_grades[exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'exam_type': exam_type,
                'subjects': {}
            }
        exam_grades[exam_name]['subjects'][subj] = score
        all_subjects.add(subj)
    
    # 计算每次考试的平均成绩（或单科成绩）
    exam_averages = {}
    
    for exam_name, exam_data in exam_grades.items():
        scores = list(exam_data['subjects'].values())
        if subject and subject != 'all':
            # 单科模式：只显示指定科目的成绩
            exam_averages[exam_name] = exam_data['subjects'].get(subject, 0)
        else:
            # 全科模式：计算平均成绩
            exam_averages[exam_name] = round(sum(scores) / len(scores), 2) if scores else 0
    
    # 构建结果
    result = {
        "student_info": {
            "name": name,
            "gender": gender,
            "class": f"{student_grade}{student_class}",
            "grade": student_grade
        },
        "analysis_type": "单科分析" if (subject and subject != 'all') else "全科分析",
        "selected_subject": subject if (subject and subject != 'all') else None,
        "available_subjects": sorted(list(all_subjects)),
        "exam_trend": {
            "exam_names": list(exam_averages.keys()),
            "averages": [round(a, 2) if isinstance(a, float) else a for a in exam_averages.values()]
        },
        "detailed_grades": exam_grades
    }
    
    return result

# 分析班级考试趋势
def analyze_class_trend(class_name, grade, subject=None, exam_code=None):
    """
    分析班级考试趋势
    
    Args:
        class_name: 班级数字（如'1'）
        grade: 年级（如'高一'）
        subject: 学科名称（可选），为None或'all'时表示全科分析，为具体学科时表示单科分析
        exam_code: 考试代码（可选），为None或'all'时表示所有考试，为具体考试代码时表示特定考试
    
    Returns:
        dict: 包含班级信息和考试趋势数据
    """
    # 处理班级格式
    if class_name.isdigit():
        class_name = f"{class_name}班"
    
    students = GradeDataAccess.get_class_students(class_name, grade)
    
    if not students:
        return {"error": f"未找到 {grade}{class_name} 班级的学生"}
    
    # 查询班级所有成绩
    grades = GradeDataAccess.get_class_grades(class_name, grade)
    
    if not grades:
        # 直接查询学生表
        from app.models import Student
        from app import db
        students = Student.query.filter_by(class_=class_name, grade=grade).all()
        student_count = len(students)
        return {
            "class_info": {
                "class_name": f"{grade}{class_name}",
                "grade": grade,
                "student_count": student_count
            },
            "error": f"{grade}{class_name} 班级暂无成绩记录"
        }
    
    # 过滤指定考试（如果提供了exam_code参数且不是'all'）
    if exam_code and exam_code != 'all':
        grades = [(sid, en, ay, se, et, su, sc, gl) for sid, en, ay, se, et, su, sc, gl in grades if en == exam_code]
        if not grades:
            return {
                "class_info": {
                    "class_name": f"{grade}{class_name}",
                    "grade": grade,
                    "student_count": len(students)
                },
                "error": f"{grade}{class_name} 班级在考试{exam_code}中暂无成绩记录"
            }
    
    # 过滤指定学科（如果提供了subject参数且不是'all'）
    if subject and subject != 'all':
        grades = [(sid, en, ay, se, et, su, sc, gl) for sid, en, ay, se, et, su, sc, gl in grades if su == subject]
        if not grades:
            return {
                "class_info": {
                    "class_name": f"{grade}{class_name}",
                    "grade": grade,
                    "student_count": len(students)
                },
                "error": f"{grade}{class_name} 班级在{subject}科目暂无成绩记录"
            }
    
    # 按考试整理成绩
    exam_grades = {}
    all_subjects = set()
    
    for student_id, exam_name, academic_year, semester, exam_type, subj, score, grade_level in grades:
        if exam_name not in exam_grades:
            exam_grades[exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'exam_type': exam_type,
                'subjects': {}
            }
        if subj not in exam_grades[exam_name]['subjects']:
            exam_grades[exam_name]['subjects'][subj] = []
        exam_grades[exam_name]['subjects'][subj].append(score)
        all_subjects.add(subj)
    
    # 计算每次考试的班级平均成绩（或单科平均成绩）
    exam_averages = {}
    
    for exam_name, exam_data in exam_grades.items():
        if subject and subject != 'all':
            # 单科模式：只显示指定科目的平均成绩
            scores = exam_data['subjects'].get(subject, [])
            exam_averages[exam_name] = round(sum(scores) / len(scores), 2) if scores else 0
        else:
            # 全科模式：计算所有科目的平均成绩
            all_scores = []
            for subj, scores in exam_data['subjects'].items():
                all_scores.extend(scores)
            exam_averages[exam_name] = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 构建结果
    result = {
        "class_info": {
            "class_name": f"{grade}{class_name}",
            "grade": grade,
            "student_count": len(students)
        },
        "analysis_type": "单科分析" if (subject and subject != 'all') else "全科分析",
        "selected_subject": subject if (subject and subject != 'all') else None,
        "available_subjects": sorted(list(all_subjects)),
        "exam_trend": {
            "exam_names": list(exam_averages.keys()),
            "averages": [round(a, 2) if isinstance(a, float) else a for a in exam_averages.values()]
        }
    }
    
    return result

# 分析年级考试趋势
def analyze_grade_trend(grade):
    # 查询年级所有班级
    classes = GradeDataAccess.get_grade_classes(grade)
    
    if not classes:
        return {"error": f"未找到 {grade} 年级的班级"}
    
    # 查询年级所有成绩
    grades = GradeDataAccess.get_grade_grades(grade)
    
    if not grades:
        return {"error": f"{grade} 年级暂无成绩记录"}
    
    # 按考试整理成绩
    exam_grades = {}
    for class_name, exam_name, academic_year, semester, exam_type, subject, score, grade_level in grades:
        if exam_name not in exam_grades:
            exam_grades[exam_name] = {
                'academic_year': academic_year,
                'semester': semester,
                'exam_type': exam_type,
                'subjects': {}
            }
        if subject not in exam_grades[exam_name]['subjects']:
            exam_grades[exam_name]['subjects'][subject] = []
        exam_grades[exam_name]['subjects'][subject].append(score)
    
    # 计算每次考试的年级平均成绩
    exam_averages = {}
    for exam_name, exam_data in exam_grades.items():
        all_scores = []
        for subject, scores in exam_data['subjects'].items():
            all_scores.extend(scores)
        exam_averages[exam_name] = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0
    
    # 构建结果
    result = {
        "grade_info": {
            "grade": grade,
            "class_count": len(classes)
        },
        "exam_trend": {
            "exam_names": list(exam_averages.keys()),
            "averages": list(exam_averages.values())
        }
    }
    
    return result

# 分析教师成绩对比
def analyze_teacher_performance(subject):
    # 获取教师授课信息和成绩
    teacher_grades = GradeDataAccess.get_teacher_subject_grades(subject)
    
    if not teacher_grades:
        return {"error": f"暂无{subject}科目教师授课记录"}
    
    # 整理教师成绩数据
    teacher_stats = {}
    for teacher_name, class_name, grade, score in teacher_grades:
        if teacher_name not in teacher_stats:
            teacher_stats[teacher_name] = {
                "classes": {},
                "all_scores": []
            }
        if class_name not in teacher_stats[teacher_name]["classes"]:
            teacher_stats[teacher_name]["classes"][class_name] = []
        teacher_stats[teacher_name]["classes"][class_name].append(score)
        teacher_stats[teacher_name]["all_scores"].append(score)
    
    # 计算每个教师的统计指标
    for teacher_name, data in teacher_stats.items():
        # 计算所有班级的平均
        all_scores = data["all_scores"]
        data["average"] = calculate_average(all_scores)
        data["std_deviation"] = calculate_std_deviation(all_scores)
        data["median"] = calculate_median(all_scores)
        data["min_score"], data["max_score"] = calculate_min_max(all_scores)
        
        # 计算每个班级的平均
        for class_name, scores in data["classes"].items():
            data["classes"][class_name] = round(sum(scores) / len(scores), 2)
    
    # 构建结果
    result = {
        "subject": subject,
        "teacher_performance": teacher_stats
    }
    
    return result

# 分析学生课程安排与成绩关系
def analyze_student_schedule(student_id):
    # 获取学生信息
    student_info, _ = GradeDataAccess.get_student_grades(student_id)
    
    if not student_info:
        return {"error": f"未找到学号为 {student_id} 的学生"}
    
    name, gender, student_class, student_grade = student_info
    
    # 获取学生课程安排和成绩
    schedule_grades = GradeDataAccess.get_student_schedule_grades(student_id)
    
    if not schedule_grades:
        return {
            "student_info": {
                "name": name,
                "gender": gender,
                "class": f"{student_grade}{student_class}",
                "grade": student_grade
            },
            "error": "该学生暂无课程安排或成绩记录"
        }
    
    # 整理数据
    schedule_analysis = {}
    for day_of_week, period, subject, teacher, score in schedule_grades:
        key = f"{day_of_week}-{period}"
        if key not in schedule_analysis:
            schedule_analysis[key] = {
                "day_of_week": day_of_week,
                "period": period,
                "subject": subject,
                "teacher": teacher,
                "score": score
            }
    
    # 构建结果
    result = {
        "student_info": {
            "name": name,
            "gender": gender,
            "class": f"{student_grade}{student_class}",
            "grade": student_grade
        },
        "schedule_analysis": schedule_analysis
    }
    
    return result

# 分析班级课程安排与成绩关系
def analyze_class_schedule(class_name, grade):
    # 处理班级格式
    if class_name.isdigit():
        class_name = f"{class_name}班"
    
    # 查询班级学生
    students = GradeDataAccess.get_class_students(class_name, grade)
    
    if not students:
        return {"error": f"未找到 {grade}{class_name} 班级的学生"}
    
    # 获取班级课程安排和成绩
    schedule_grades = GradeDataAccess.get_class_schedule_grades(class_name, grade)
    
    if not schedule_grades:
        return {"error": f"{grade}{class_name} 班级暂无课程安排或成绩记录"}
    
    # 整理数据
    schedule_analysis = {}
    for day_of_week, period, subject, teacher, score in schedule_grades:
        key = f"{day_of_week}-{period}"
        if key not in schedule_analysis:
            schedule_analysis[key] = {
                "day_of_week": day_of_week,
                "period": period,
                "subject": subject,
                "teacher": teacher,
                "scores": []
            }
        schedule_analysis[key]["scores"].append(score)
    
    # 计算每个时间段的平均成绩
    for key, data in schedule_analysis.items():
        data["average_score"] = calculate_average(data["scores"])
    
    # 构建结果
    result = {
        "class_info": {
            "class_name": f"{grade}{class_name}",
            "grade": grade,
            "student_count": len(students)
        },
        "schedule_analysis": schedule_analysis
    }
    
    return result