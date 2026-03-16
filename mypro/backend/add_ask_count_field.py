#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加 ask_count 字段到 questions 表
"""
import sys
import io

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print("=" * 60)
print("添加 ask_count 字段到 questions 表")
print("=" * 60)

try:
    from app.config import settings
    from app.database import engine
    
    print("数据库URL:", settings.DATABASE_URL)
    
    # 使用直接连接添加字段
    import pymysql
    
    connection = pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        charset='utf8mb4'
    )
    
    cursor = connection.cursor()
    
    print("\n1. 检查当前 questions 表结构...")
    cursor.execute("DESCRIBE questions")
    columns = cursor.fetchall()
    print(f"  当前字段 ({len(columns)}):")
    for col in columns:
        print(f"    - {col[0]}: {col[1]}")
    
    # 检查 ask_count 字段是否存在
    ask_count_exists = any(col[0] == 'ask_count' for col in columns)
    
    if ask_count_exists:
        print("\n2. ask_count 字段已存在，检查字段定义...")
        cursor.execute("DESCRIBE questions ask_count")
        field_info = cursor.fetchone()
        print(f"  字段类型: {field_info[1]}")
        print(f"  是否允许NULL: {field_info[2]}")
        print(f"  默认值: {field_info[4]}")
        
        # 检查是否需要修改
        if field_info[1] != 'int(11)':
            print("\n3. 字段类型不正确，需要修改...")
            cursor.execute("ALTER TABLE questions MODIFY COLUMN ask_count INT DEFAULT 1 COMMENT '提问次数'")
            connection.commit()
            print("  ✓ 已修改 ask_count 字段类型")
        else:
            print("\n3. ask_count 字段类型正确")
    else:
        print("\n2. ask_count 字段不存在，正在添加...")
        cursor.execute("""
            ALTER TABLE questions 
            ADD COLUMN ask_count INT DEFAULT 1 COMMENT '提问次数'
            AFTER views
        """)
        connection.commit()
        print("  ✓ ask_count 字段添加成功")
    
    print("\n3. 验证表结构...")
    cursor.execute("DESCRIBE questions")
    columns = cursor.fetchall()
    print("\n更新后的 questions 表结构:")
    for col in columns:
        print(f"  {col[0]:15s} {col[1]:20s} {col[2]:5s} {col[4] or 'NULL':10s}")
    
    # 检查是否有数据需要更新
    print("\n4. 检查现有数据...")
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_questions = cursor.fetchone()[0]
    print(f"  总问题数: {total_questions}")
    
    if total_questions > 0:
        print("  检查现有问题的 ask_count 值...")
        cursor.execute("SELECT id, question, ask_count FROM questions LIMIT 5")
        questions = cursor.fetchall()
        for q in questions:
            print(f"    ID:{q[0]:3d} - {q[1][:30]:30s}... ask_count:{q[2]}")
        
        # 如果有 NULL 值，更新为 1
        cursor.execute("SELECT COUNT(*) FROM questions WHERE ask_count IS NULL")
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"\n5. 更新 {null_count} 条记录的 ask_count 为默认值 1...")
            cursor.execute("UPDATE questions SET ask_count = 1 WHERE ask_count IS NULL")
            connection.commit()
            print(f"  ✓ 已更新 {cursor.rowcount} 条记录")
    
    cursor.close()
    connection.close()
    
    print("\n" + "=" * 60)
    print("ask_count 字段修复完成！")
    print("=" * 60)
    print("\n测试数据库操作...")
    
    # 测试数据库操作
    from app.database import SessionLocal
    from app.models import Question
    from app.schemas import QuestionCreate
    
    db = SessionLocal()
    try:
        # 测试查询
        test_question = "测试问题: ask_count 字段修复后测试"
        existing_question = db.query(Question).filter(
            Question.question == test_question
        ).first()
        
        print(f"  测试查询: {'✓ 成功' if existing_question else '未找到，正常'}")
        
        # 测试创建新问题
        print("  测试创建新问题...")
        from app.models import User
        test_user = db.query(User).first()
        
        if test_user:
            print(f"  使用测试用户: {test_user.username}")
            
            # 创建测试问题
            db_test_question = Question(
                user_id=test_user.id,
                question=test_question,
                category="测试",
                ask_count=1
            )
            db.add(db_test_question)
            db.commit()
            print(f"  ✓ 测试问题创建成功, ID: {db_test_question.id}")
            print(f"    ask_count 值: {db_test_question.ask_count}")
            
            # 测试更新 ask_count
            db_test_question.ask_count += 1
            db.commit()
            print(f"  ✓ ask_count 更新成功: {db_test_question.ask_count}")
            
            # 清理测试数据
            db.delete(db_test_question)
            db.commit()
            print("  ✓ 测试数据清理完成")
        else:
            print("  ⚠ 无用户数据，请先运行 init_data.py")
            
    except Exception as e:
        print(f"  ✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("数据库操作修复完成！")
    print("现在可以正常运行提问功能了。")
    print("=" * 60)
    
except Exception as e:
    print(f"\n修复失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)