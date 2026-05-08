#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数值格式化功能
"""

import sys
sys.path.insert(0, 'backend')

from app.utils.response import NumberFormatter


def test_format_number():
    """测试单个数值格式化"""
    print("=" * 60)
    print("测试单个数值格式化")
    print("=" * 60)
    
    test_cases = [
        (61.6, 2, 61.6),
        (61.60000000000001, 2, 61.6),
        (105.4, 2, 105.4),
        (43.8, 2, 43.8),
        (0.1 + 0.2, 2, 0.3),
        (3.1415926, 2, 3.14),
        (3.145926, 2, 3.15),
        (5.0, 2, 5),
        (100, 2, 100),
        ("61.6", 2, 61.6),
        ("abc", 2, "abc"),
        (None, 2, None),
        ([1, 2, 3], 2, [1, 2, 3])
    ]
    
    all_passed = True
    for input_val, decimals, expected in test_cases:
        try:
            result = NumberFormatter.format_number(input_val, decimals)
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
            print(f"{status} format_number({input_val!r}, {decimals}) = {result!r} (期望: {expected!r})")
        except Exception as e:
            print(f"✗ format_number({input_val!r}, {decimals}) 抛出异常: {e}")
            all_passed = False
    
    return all_passed


def test_format_data():
    """测试数据结构格式化"""
    print("\n" + "=" * 60)
    print("测试数据结构格式化")
    print("=" * 60)
    
    # 测试字典
    test_dict = {
        'average_score': 61.60000000000001,
        'excellent_rate': 0.8555555555,
        'pass_rate': 0.9999999999,
        'student_count': 45,
        'name': '物理',
        'data': None
    }
    
    result = NumberFormatter.format_data(test_dict)
    print(f"输入字典:\n  {test_dict}")
    print(f"输出字典:\n  {result}")
    
    # 测试嵌套结构
    nested_data = {
        'class_info': {
            'class_name': '高一1班',
            'grade': '高一',
            'subject_count': 2
        },
        'subject_details': {
            '数学': {
                'raw_score': 105.40000000000001,
                'normalized_score': 70.26666666666667,
                'full_score': 150
            },
            '物理': {
                'raw_score': 61.60000000000001,
                'normalized_score': 61.6,
                'full_score': 100
            }
        },
        'overall': {
            'raw_average': 83.5,
            'normalized_average': 65.93333333333334
        },
        'comparisons': [
            {'subject': '物理', 'average_diff': -43.800000000000004},
            {'subject': '化学', 'average_diff': -20.5}
        ]
    }
    
    formatted = NumberFormatter.format_data(nested_data)
    print("\n嵌套结构格式化结果:")
    print(f"  class_info: {formatted['class_info']}")
    print(f"  subject_details['数学']: {formatted['subject_details']['数学']}")
    print(f"  subject_details['物理']: {formatted['subject_details']['物理']}")
    print(f"  overall: {formatted['overall']}")
    print(f"  comparisons: {formatted['comparisons']}")
    
    return True


def test_real_scenario():
    """测试真实场景数据"""
    print("\n" + "=" * 60)
    print("测试真实场景数据")
    print("=" * 60)
    
    # 模拟从数据库获取的数据
    raw_data = {
        'class_id': '高一1班',
        'base_subject': {
            'subject': '数学',
            'average_score': 105.40000000000001,
            'excellent_rate': 0.2,
            'pass_rate': 0.95,
            'improvement_rate': 0,
            'student_count': 45
        },
        'comparisons': [
            {
                'subject': '物理',
                'average_diff': -43.800000000000004,
                'average_percentage': -41.54,
                'excellent_diff': -0.8,
                'pass_diff': 0.0
            }
        ],
        'subjects': ['数学', '物理'],
        'generated_at': '2026-05-08 10:30:00'
    }
    
    formatted = NumberFormatter.format_data(raw_data)
    
    print("原始数据:")
    print(f"  base_subject.average_score = {raw_data['base_subject']['average_score']}")
    print(f"  comparisons[0].average_diff = {raw_data['comparisons'][0]['average_diff']}")
    
    print("\n格式化后数据:")
    print(f"  base_subject.average_score = {formatted['base_subject']['average_score']}")
    print(f"  comparisons[0].average_diff = {formatted['comparisons'][0]['average_diff']}")
    
    # 验证精度
    assert formatted['base_subject']['average_score'] == 105.4, "数学平均分格式化错误"
    assert formatted['comparisons'][0]['average_diff'] == -43.8, "平均分差异格式化错误"
    assert formatted['base_subject']['excellent_rate'] == 0.2, "优秀率格式化错误"
    
    print("\n✓ 所有精度验证通过")
    return True


def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 16 + "数值格式化工具测试" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    # 运行测试
    test1 = test_format_number()
    test2 = test_format_data()
    test3 = test_real_scenario()
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    if all([test1, test2, test3]):
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1


if __name__ == '__main__':
    sys.exit(main())