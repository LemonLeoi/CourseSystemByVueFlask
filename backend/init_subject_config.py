#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化学科配置表数据
"""

import sys
import os

# 添加后端目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from app.models import SubjectConfig, INITIAL_SUBJECT_CONFIG

def init_subject_config():
    """初始化学科配置表"""
    with app.app_context():
        # 创建表（如果不存在）
        db.create_all()
        
        # 检查是否已存在数据
        existing_count = SubjectConfig.query.count()
        
        if existing_count > 0:
            print(f"学科配置表已存在 {existing_count} 条记录，跳过初始化")
            return
        
        # 插入初始数据
        for config in INITIAL_SUBJECT_CONFIG:
            subject_config = SubjectConfig(**config)
            db.session.add(subject_config)
        
        db.session.commit()
        print(f"成功初始化 {len(INITIAL_SUBJECT_CONFIG)} 条学科配置数据")
        
        # 验证数据
        configs = SubjectConfig.query.all()
        print("\n初始化的学科配置:")
        for config in configs:
            print(f"  {config.subject_name}: 满分{config.full_score}分 ({config.subject_type})")

if __name__ == '__main__':
    init_subject_config()
