import requests
import json

# 后端服务地址
BASE_URL = 'http://localhost:5000/api'

# 测试学生ID
TEST_STUDENT_ID = 'STU20240001'

# 测试考试代码
EXAM_1_CODE = 'EXAM202401'
EXAM_2_CODE = 'EXAM202402'

# 创建考试函数
def create_exam(exam_code, exam_name):
    exam_data = {
        "code": exam_code,
        "name": exam_name,
        "grade": "高一",
        "type": "月考",
        "startDate": "2024-01-01",
        "endDate": "2024-01-02",
        "status": "已完成",
        "academicYear": "2023-2024学年",
        "semester": "第一学期"
    }
    response = requests.post(f'{BASE_URL}/exams/', json=exam_data)
    return response

# 测试函数
def test_student_grades():
    print("=== 测试学生成绩管理 ===")
    
    # 1. 先创建考试1
    print("\n1. 创建考试1")
    response = create_exam(EXAM_1_CODE, "2024年1月月考")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 2. 创建考试2
    print("\n2. 创建考试2")
    response = create_exam(EXAM_2_CODE, "2024年2月月考")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 3. 添加考试1的成绩
    print("\n3. 添加考试1的成绩")
    exam1_scores = [
        {
            "subject": "语文",
            "score": 95,
            "exam_id": EXAM_1_CODE
        },
        {
            "subject": "数学",
            "score": 88,
            "exam_id": EXAM_1_CODE
        },
        {
            "subject": "英语",
            "score": 92,
            "exam_id": EXAM_1_CODE
        }
    ]
    
    response = requests.put(f'{BASE_URL}/students/{TEST_STUDENT_ID}/grades', json={'scores': exam1_scores})
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 4. 再添加考试2的成绩
    print("\n4. 添加考试2的成绩")
    exam2_scores = [
        {
            "subject": "语文",
            "score": 90,
            "exam_id": EXAM_2_CODE
        },
        {
            "subject": "数学",
            "score": 95,
            "exam_id": EXAM_2_CODE
        },
        {
            "subject": "英语",
            "score": 85,
            "exam_id": EXAM_2_CODE
        }
    ]
    
    response = requests.put(f'{BASE_URL}/students/{TEST_STUDENT_ID}/grades', json={'scores': exam2_scores})
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.json()}")
    
    # 5. 获取学生成绩，验证两个考试的成绩都存在
    print("\n5. 获取学生成绩，验证两个考试的成绩都存在")
    response = requests.get(f'{BASE_URL}/students/{TEST_STUDENT_ID}')
    print(f"响应状态码: {response.status_code}")
    student_data = response.json()
    
    print(f"学生姓名: {student_data.get('name')}")
    print(f"总成绩条数: {len(student_data.get('scores', []))}")
    
    # 统计每个考试的成绩
    exam1_count = 0
    exam2_count = 0
    
    for score in student_data.get('scores', []):
        print(f"科目: {score['subject']}, 成绩: {score['score']}, 考试类型: {score.get('examType')}, 学期: {score.get('semester')}, 考试代码: {score.get('exam_code')}")
        if score.get('exam_code') == EXAM_1_CODE:
            exam1_count += 1
        elif score.get('exam_code') == EXAM_2_CODE:
            exam2_count += 1
    
    print(f"\n考试1的成绩条数: {exam1_count}")
    print(f"考试2的成绩条数: {exam2_count}")
    
    # 验证结果
    if exam1_count == 3 and exam2_count == 3:
        print("\n✅ 测试通过！两个考试的成绩都正确保存，没有相互覆盖")
        return True
    else:
        print("\n❌ 测试失败！成绩可能被覆盖了")
        return False

if __name__ == "__main__":
    test_student_grades()
