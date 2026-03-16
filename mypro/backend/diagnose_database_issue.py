#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
诊断数据库操作失败问题
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
print("诊断数据库操作失败问题")
print("=" * 60)

try:
    # 导入配置
    from app.config import settings
    print(f"数据库URL: {settings.DATABASE_URL}")
    
    # 导入数据库模块
    from app.database import engine, Base, SessionLocal
    from app.models import User, Question
    from app.schemas import QuestionCreate
    
    print("\n[1/5] 检查数据库连接...")
    with engine.connect() as conn:
        print("  ✓ 数据库连接成功")
        
        from sqlalchemy import text
        
        # 检查表结构
        result = conn.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        print(f"  ✓ 发现 {len(tables)} 张表: {', '.join(tables)}")
        
        # 检查 questions 表结构
        if 'questions' in tables:
            print("\n[2/5] 检查 questions 表结构...")
            result = conn.execute(text("DESCRIBE questions"))
            columns = result.fetchall()
            print(f"  ✓ questions 表有 {len(columns)} 个字段:")
            for col in columns:
                print(f"    - {col[0]}: {col[1]} ({col[2]})")
            
            # 检查关键字段是否存在
            required_fields = ['id', 'user_id', 'question', 'answer', 'category', 'ask_count']
            existing_fields = [col[0] for col in columns]
            
            missing_fields = [field for field in required_fields if field not in existing_fields]
            if missing_fields:
                print(f"  ✗ 缺少字段: {', '.join(missing_fields)}")
            else:
                print("  ✓ 所有必需字段都存在")
        
        # 检查外键约束
        print("\n[3/5] 检查外键约束...")
        result = conn.execute(text("""
            SELECT 
                TABLE_NAME, 
                COLUMN_NAME, 
                CONSTRAINT_NAME, 
                REFERENCED_TABLE_NAME, 
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'qa_system' 
            AND REFERENCED_TABLE_NAME IS NOT NULL
            AND TABLE_NAME = 'questions'
        """))
        foreign_keys = result.fetchall()
        
        if foreign_keys:
            print("  ✓ questions 表外键约束:")
            for fk in foreign_keys:
                print(f"    - {fk[1]} -> {fk[3]}.{fk[4]}")
        else:
            print("  ⚠ questions 表无外键约束")
    
    print("\n[4/5] 测试数据操作...")
    db = SessionLocal()
    try:
        # 检查是否有用户数据
        user_count = db.query(User).count()
        print(f"  ✓ 用户表中有 {user_count} 条记录")
        
        if user_count == 0:
            print("  ⚠ 用户表中无数据，需要先创建用户")
            print("  运行: python init_data.py")
        else:
            # 获取一个用户用于测试
            test_user = db.query(User).first()
            print(f"  ✓ 找到测试用户: {test_user.username} (ID: {test_user.id})")
            
            # 测试创建问题
            print("\n[5/5] 模拟问题创建...")
            try:
                # 创建测试问题
                test_question = QuestionCreate(
                    question="测试问题: 数据库操作失败怎么办？",
                    category="技术问题"
                )
                
                # 模拟问题创建逻辑
                existing_question = db.query(Question).filter(
                    Question.question == test_question.question
                ).first()
                
                if existing_question:
                    print("  ✓ 问题已存在逻辑测试通过")
                    existing_question.ask_count += 1
                    db.commit()
                    print(f"  ✓ 提问次数更新: {existing_question.ask_count}")
                else:
                    print("  ✓ 新问题创建逻辑测试通过")
                    db_question = Question(
                        user_id=test_user.id,
                        question=test_question.question,
                        category=test_question.category,
                        ask_count=1
                    )
                    db.add(db_question)
                    db.commit()
                    db.refresh(db_question)
                    print(f"  ✓ 问题创建成功, ID: {db_question.id}")
                    
                    # 添加答案
                    db_question.answer = "这是一个测试答案"
                    db.commit()
                    db.refresh(db_question)
                    print(f"  ✓ 答案添加成功")
                
                print("\n" + "=" * 60)
                print("测试通过！数据库操作正常")
                print("=" * 60)
                
            except Exception as e:
                print(f"  ✗ 问题创建失败: {e}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"  ✗ 数据操作测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        
except Exception as e:
    print(f"\n诊断失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)