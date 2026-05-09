#!/usr/bin/env python3
"""
测试正则表达式
"""

import re

test_cases = [
    '语文高一上',
    '数学高一上', 
    '英语高一上',
    '物理高一上',
    '化学高一上',
    '生物高一上',
    '历史高一上',
    '地理高一上',
    '政治高一上',
    '体育高一上',
]

print("测试正则表达式:")
print("-" * 40)

# 方案1: 查找特定关键词，然后取前面部分
for course_name in test_cases:
    # 查找年级关键词
    for keyword in ['高一', '高二', '高三']:
        if keyword in course_name:
            idx = course_name.find(keyword)
            subject = course_name[:idx]
            print(f"{course_name:12} -> {subject}")
            break
    else:
        print(f"{course_name:12} -> 未匹配")

print("\n" + "=" * 40)

# 方案2: 使用更好的正则表达式
print("\n方案2 - 正则表达式:")
print("-" * 40)

for course_name in test_cases:
    # 匹配2-4个中文字符（科目名），后面紧跟年级信息
    match = re.match(r'^([\u4e00-\u9fa5]{2,4})(?:高[一二三])', course_name)
    if match:
        print(f"{course_name:12} -> {match.group(1)}")
    else:
        # 尝试只匹配2个中文字符
        match2 = re.match(r'^([\u4e00-\u9fa5]{2})', course_name)
        if match2:
            print(f"{course_name:12} -> {match2.group(1)} (fallback)")
        else:
            print(f"{course_name:12} -> 未匹配")

print("\n" + "=" * 40)
print("\n方案3 - 简单取前2字:")
print("-" * 40)
for course_name in test_cases:
    subject = course_name[:2]
    print(f"{course_name:12} -> {subject}")
