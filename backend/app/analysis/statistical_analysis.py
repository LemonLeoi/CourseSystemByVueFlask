# Statistical analysis tools
import sqlite3
import math

# 计算平均值
def calculate_average(scores, analysis_id=None):
    if not scores:
        return 0
    
    # 记录计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'calculate_average',
                'input': scores,
                'steps': [
                    {'step': 'sum', 'value': sum(scores)},
                    {'step': 'count', 'value': len(scores)},
                    {'step': 'average', 'value': sum(scores) / len(scores)}
                ],
                'result': round(sum(scores) / len(scores), 2)
            },
            '计算平均值'
        )
    
    return round(sum(scores) / len(scores), 2)

# 计算标准差
def calculate_std_deviation(scores, analysis_id=None):
    if len(scores) <= 1:
        return 0
    avg = calculate_average(scores, analysis_id)
    variance = sum((x - avg) ** 2 for x in scores) / (len(scores) - 1)
    std_dev = round(math.sqrt(variance), 2)
    
    # 记录计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'calculate_std_deviation',
                'input': scores,
                'steps': [
                    {'step': 'average', 'value': avg},
                    {'step': 'variance', 'value': variance},
                    {'step': 'std_deviation', 'value': std_dev}
                ],
                'result': std_dev
            },
            '计算标准差'
        )
    
    return std_dev

# 计算中位数
def calculate_median(scores, analysis_id=None):
    if not scores:
        return 0
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    if n % 2 == 0:
        median = round((sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2, 2)
    else:
        median = round(sorted_scores[n//2], 2)
    
    # 记录计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'calculate_median',
                'input': scores,
                'steps': [
                    {'step': 'sorted_scores', 'value': sorted_scores},
                    {'step': 'count', 'value': n},
                    {'step': 'median', 'value': median}
                ],
                'result': median
            },
            '计算中位数'
        )
    
    return median

# 计算最高分和最低分
def calculate_min_max(scores, analysis_id=None):
    if not scores:
        return 0, 0
    min_score = min(scores)
    max_score = max(scores)
    
    # 记录计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'calculate_min_max',
                'input': scores,
                'steps': [
                    {'step': 'min', 'value': min_score},
                    {'step': 'max', 'value': max_score}
                ],
                'result': [min_score, max_score]
            },
            '计算最高分和最低分'
        )
    
    return min_score, max_score

# 计算成绩分布
def calculate_score_distribution(scores, analysis_id=None):
    if not scores:
        distribution = {
            "excellent": 0,
            "good": 0,
            "average": 0,
            "pass": 0,
            "fail": 0
        }
    else:
        distribution = {
            "excellent": 0,  # 90-100
            "good": 0,       # 80-89
            "average": 0,    # 70-79
            "pass": 0,       # 60-69
            "fail": 0        # 0-59
        }
        
        for score in scores:
            if score >= 90:
                distribution["excellent"] += 1
            elif score >= 80:
                distribution["good"] += 1
            elif score >= 70:
                distribution["average"] += 1
            elif score >= 60:
                distribution["pass"] += 1
            else:
                distribution["fail"] += 1
    
    # 记录计算过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'calculate_score_distribution',
                'input': scores,
                'steps': [
                    {'step': 'excellent_count', 'value': distribution["excellent"]},
                    {'step': 'good_count', 'value': distribution["good"]},
                    {'step': 'average_count', 'value': distribution["average"]},
                    {'step': 'pass_count', 'value': distribution["pass"]},
                    {'step': 'fail_count', 'value': distribution["fail"]}
                ],
                'result': distribution
            },
            '计算成绩分布'
        )
    
    return distribution

# 获取整体成绩统计
def get_overall_statistics(analysis_id=None):
    import os
    # 使用相对路径连接数据库
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询所有成绩
    cursor.execute("SELECT score FROM student_grades")
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not scores:
        return {"error": "暂无成绩数据"}
    
    # 计算统计指标
    avg = calculate_average(scores, analysis_id)
    std_dev = calculate_std_deviation(scores, analysis_id)
    median = calculate_median(scores, analysis_id)
    min_score, max_score = calculate_min_max(scores, analysis_id)
    distribution = calculate_score_distribution(scores, analysis_id)
    
    # 计算各等级百分比
    total = len(scores)
    distribution_percent = {}
    for key, value in distribution.items():
        distribution_percent[key] = round((value / total) * 100, 2) if total > 0 else 0
    
    result = {
        "total_count": total,
        "average": avg,
        "std_deviation": std_dev,
        "median": median,
        "min_score": min_score,
        "max_score": max_score,
        "distribution": distribution,
        "distribution_percent": distribution_percent
    }
    
    # 记录分析过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'get_overall_statistics',
                'input': {'total_count': total},
                'steps': [
                    {'step': 'data_retrieval', 'value': f'获取了{total}条成绩数据'},
                    {'step': 'statistical_calculation', 'value': '计算了平均值、标准差、中位数、最高分、最低分和成绩分布'},
                    {'step': 'percentage_calculation', 'value': '计算了各等级百分比'}
                ],
                'result': result
            },
            '获取整体成绩统计'
        )
    
    return result

# 获取学科成绩统计
def get_subject_statistics(analysis_id=None):
    import os
    # 使用相对路径连接数据库
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询所有学科
    cursor.execute("SELECT DISTINCT subject FROM student_grades")
    subjects = [row[0] for row in cursor.fetchall()]
    
    subject_stats = {}
    for subject in subjects:
        cursor.execute("SELECT score FROM student_grades WHERE subject = ?", (subject,))
        scores = [row[0] for row in cursor.fetchall()]
        
        if scores:
            avg = calculate_average(scores, analysis_id)
            std_dev = calculate_std_deviation(scores, analysis_id)
            median = calculate_median(scores, analysis_id)
            min_score, max_score = calculate_min_max(scores, analysis_id)
            distribution = calculate_score_distribution(scores, analysis_id)
            
            total = len(scores)
            distribution_percent = {}
            for key, value in distribution.items():
                distribution_percent[key] = round((value / total) * 100, 2) if total > 0 else 0
            
            subject_stats[subject] = {
                "total_count": total,
                "average": avg,
                "std_deviation": std_dev,
                "median": median,
                "min_score": min_score,
                "max_score": max_score,
                "distribution": distribution,
                "distribution_percent": distribution_percent
            }
    
    conn.close()
    
    # 记录分析过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'get_subject_statistics',
                'input': {'subjects': subjects},
                'steps': [
                    {'step': 'data_retrieval', 'value': f'获取了{len(subjects)}个学科的成绩数据'},
                    {'step': 'statistical_calculation', 'value': '为每个学科计算了统计指标'},
                    {'step': 'result_aggregation', 'value': '汇总了所有学科的统计结果'}
                ],
                'result': subject_stats
            },
            '获取学科成绩统计'
        )
    
    return subject_stats

# 获取考试类型成绩统计
def get_exam_type_statistics(analysis_id=None):
    import os
    # 使用相对路径连接数据库
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询所有考试类型（通过连接exams表）
    cursor.execute("SELECT DISTINCT exams.exam_type FROM student_grades JOIN exams ON student_grades.exam_code = exams.exam_code")
    exam_types = [row[0] for row in cursor.fetchall()]
    
    exam_stats = {}
    for exam_type in exam_types:
        # 查询该考试类型的所有成绩（通过连接exams表）
        cursor.execute("SELECT student_grades.score FROM student_grades JOIN exams ON student_grades.exam_code = exams.exam_code WHERE exams.exam_type = ?", (exam_type,))
        scores = [row[0] for row in cursor.fetchall()]
        
        if scores:
            avg = calculate_average(scores, analysis_id)
            std_dev = calculate_std_deviation(scores, analysis_id)
            median = calculate_median(scores, analysis_id)
            min_score, max_score = calculate_min_max(scores, analysis_id)
            distribution = calculate_score_distribution(scores, analysis_id)
            
            total = len(scores)
            distribution_percent = {}
            for key, value in distribution.items():
                distribution_percent[key] = round((value / total) * 100, 2) if total > 0 else 0
            
            exam_stats[exam_type] = {
                "total_count": total,
                "average": avg,
                "std_deviation": std_dev,
                "median": median,
                "min_score": min_score,
                "max_score": max_score,
                "distribution": distribution,
                "distribution_percent": distribution_percent
            }
    
    conn.close()
    
    # 记录分析过程
    if analysis_id:
        from app.analysis.intermediate_results import storage
        storage.save_result(
            analysis_id,
            'statistical_analysis',
            {
                'function': 'get_exam_type_statistics',
                'input': {'exam_types': exam_types},
                'steps': [
                    {'step': 'data_retrieval', 'value': f'获取了{len(exam_types)}种考试类型的成绩数据'},
                    {'step': 'statistical_calculation', 'value': '为每种考试类型计算了统计指标'},
                    {'step': 'result_aggregation', 'value': '汇总了所有考试类型的统计结果'}
                ],
                'result': exam_stats
            },
            '获取考试类型成绩统计'
        )
    
    return exam_stats