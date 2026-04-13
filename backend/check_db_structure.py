import sqlite3

# 连接数据库
conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# 检查当前数据库结构
try:
    print("=== 当前数据库结构 ===")
    
    # 获取所有表格
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n--- {table_name} ---\n")
        
        # 获取表格结构
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("列信息:")
        for column in columns:
            col_id, col_name, col_type, not_null, default, pk = column
            print(f"  {col_name} ({col_type}) {'NOT NULL' if not_null else ''} {'PRIMARY KEY' if pk else ''}")
        
        # 获取外键约束
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = cursor.fetchall()
        if fks:
            print("\n外键约束:")
            for fk in fks:
                id, seq, table_ref, from_col, to_col, on_update, on_delete, match = fk
                print(f"  {from_col} -> {table_ref}.{to_col}")
        
        # 获取数据量
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\n数据量: {count} 条记录")
    
    print("\n=== 检查完成 ===")

except Exception as e:
    print(f"错误: {e}")
finally:
    conn.close()