"""
数据库迁移脚本：添加决策树新参数字段
使用 sqlite3 直接操作数据库，不依赖 Flask
"""

import sqlite3
import os

# 数据库文件路径
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'database.db')

print(f"Database path: {db_path}")

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 1. 检查并添加新字段
    print("\nChecking database structure...")
    
    # 先获取现有列名
    cursor.execute("PRAGMA table_info(grade_settings)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    print(f"Existing columns: {existing_columns}")
    
    # 需要添加的字段
    fields_to_add = [
        ("dt_confidence_threshold", "FLOAT NOT NULL DEFAULT 0.7"),
        ("dt_min_info_gain", "FLOAT NOT NULL DEFAULT 0.01"),
        ("dt_split_direction", "VARCHAR(20) NOT NULL DEFAULT 'max_gain'"),
        ("dt_stop_criteria", "VARCHAR(20) NOT NULL DEFAULT 'all'"),
        ("dt_missing_value_strategy", "VARCHAR(20) NOT NULL DEFAULT 'mean_mode'"),
        ("dt_min_confidence", "FLOAT NOT NULL DEFAULT 0.6")
    ]
    
    for field_name, field_def in fields_to_add:
        if field_name not in existing_columns:
            try:
                sql = f"ALTER TABLE grade_settings ADD COLUMN {field_name} {field_def}"
                cursor.execute(sql)
                print(f"[OK] Added field: {field_name}")
            except Exception as e:
                print(f"[FAIL] Failed to add field {field_name}: {e}")
        else:
            print(f"[SKIP] Field {field_name} already exists")
    
    conn.commit()
    print("\n[OK] Database migration completed!")
    
    # 2. 验证迁移结果
    print("\nVerifying migration results...")
    cursor.execute("SELECT * FROM grade_settings LIMIT 1")
    row = cursor.fetchone()
    if row:
        cursor.execute("PRAGMA table_info(grade_settings)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"[OK] All columns: {columns}")
        
        # 获取最新列名和值
        cursor.execute("SELECT dt_confidence_threshold, dt_min_info_gain, dt_split_direction, dt_stop_criteria, dt_missing_value_strategy, dt_min_confidence FROM grade_settings LIMIT 1")
        params = cursor.fetchone()
        if params:
            print(f"[OK] Decision tree parameters:")
            print(f"  - Confidence threshold: {params[0]}")
            print(f"  - Min info gain: {params[1]}")
            print(f"  - Split direction: {params[2]}")
            print(f"  - Stop criteria: {params[3]}")
            print(f"  - Missing value strategy: {params[4]}")
            print(f"  - Min confidence: {params[5]}")

except Exception as e:
    print(f"\n[FAIL] Migration failed: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()
