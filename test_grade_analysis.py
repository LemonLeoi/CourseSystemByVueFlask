#!/usr/bin/env python3
"""
测试成绩分析模块
"""

import requests
import json

# 后端服务地址
BASE_URL = 'http://localhost:5000/api'

# 测试个人分析
print("=== 测试个人分析 ===")
student_id = 'STU20240001'
response = requests.get(f'{BASE_URL}/grades/analysis/{student_id}')
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
print()

# 测试班级分析
print("=== 测试班级分析 ===")
class_name = '高三1班'
response = requests.get(f'{BASE_URL}/grades/analysis/class/{class_name}')
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
print()

# 测试年级分析
print("=== 测试年级分析 ===")
grade_name = '高三'
response = requests.get(f'{BASE_URL}/grades/analysis/grade/{grade_name}')
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
print()

# 测试个人考试趋势
print("=== 测试个人考试趋势 ===")
student_id = 'STU20240001'
response = requests.get(f'{BASE_URL}/grades/analysis/trend/{student_id}')
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
print()

# 测试班级考试趋势
print("=== 测试班级考试趋势 ===")
class_name = '高三1班'
response = requests.get(f'{BASE_URL}/grades/analysis/class/trend/{class_name}')
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
