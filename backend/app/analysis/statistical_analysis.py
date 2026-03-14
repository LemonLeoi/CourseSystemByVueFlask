# Statistical analysis tools
import sqlite3
import math

# 计算平均值
def calculate_average(scores):
    if not scores:
        return 0
    return round(sum(scores) / len(scores), 2)

# 计算标准差
def calculate_std_deviation(scores):
    if len(scores) <= 1:
        return 0
    avg = calculate_average(scores)
    variance = sum((x - avg) ** 2 for x in scores) / (len(scores) - 1)
    return round(math.sqrt(variance), 2)

# 计算中位数
def calculate_median(scores):
    if not scores:
        return 0
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    if n % 2 == 0:
        return round((sorted_scores[n//2 - 1] + sorted_scores[n//2]) / 2, 2)
    else:
        return round(sorted_scores[n//2], 2)

# 计算最高分和最低分
def calculate_min_max(scores):
    if not scores:
        return 0, 0
    return min(scores), max(scores)

# 计算成绩分布
def calculate_score_distribution(scores):
    if not scores:
        return {
            "excellent": 0,
            "good": 0,
            "average": 0,
            "pass": 0,
            "fail": 0
        }
    
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
    
    return distribution

# 获取整体成绩统计
def get_overall_statistics():
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
    cursor = conn.cursor()
    
    # 查询所有成绩
    cursor.execute("SELECT score FROM student_grades")
    scores = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not scores:
        return {"error": "暂无成绩数据"}
    
    # 计算统计指标
    avg = calculate_average(scores)
    std_dev = calculate_std_deviation(scores)
    median = calculate_median(scores)
    min_score, max_score = calculate_min_max(scores)
    distribution = calculate_score_distribution(scores)
    
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
    
    return result

# 获取学科成绩统计
def get_subject_statistics():
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
    cursor = conn.cursor()
    
    # 查询所有学科
    cursor.execute("SELECT DISTINCT subject FROM student_grades")
    subjects = [row[0] for row in cursor.fetchall()]
    
    subject_stats = {}
    for subject in subjects:
        cursor.execute("SELECT score FROM student_grades WHERE subject = ?", (subject,))
        scores = [row[0] for row in cursor.fetchall()]
        
        if scores:
            avg = calculate_average(scores)
            std_dev = calculate_std_deviation(scores)
            median = calculate_median(scores)
            min_score, max_score = calculate_min_max(scores)
            distribution = calculate_score_distribution(scores)
            
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
    return subject_stats

# 获取考试类型成绩统计
def get_exam_type_statistics():
    conn = sqlite3.connect('e:/A_Course/backend/data/database.db')
    cursor = conn.cursor()
    
    # 查询所有考试类型
    cursor.execute("SELECT DISTINCT exam_type FROM student_grades")
    exam_types = [row[0] for row in cursor.fetchall()]
    
    exam_stats = {}
    for exam_type in exam_types:
        cursor.execute("SELECT score FROM student_grades WHERE exam_type = ?", (exam_type,))
        scores = [row[0] for row in cursor.fetchall()]
        
        if scores:
            avg = calculate_average(scores)
            std_dev = calculate_std_deviation(scores)
            median = calculate_median(scores)
            min_score, max_score = calculate_min_max(scores)
            distribution = calculate_score_distribution(scores)
            
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
    return exam_stats