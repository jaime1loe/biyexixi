#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复问答历史数据问题
"""

from backend.app.database import SessionLocal
from backend.app.models import Question, User

def fix_qa_history():
    """修复问答历史数据问题"""
    
    print("=== 修复问答历史数据问题 ===\n")
    
    db = SessionLocal()
    
    try:
        # 1. 检查当前用户数据
        print("1. 检查用户数据:")
        users = db.query(User).all()
        for user in users:
            question_count = db.query(Question).filter(Question.user_id == user.id).count()
            print(f"   - 用户: {user.username} (ID: {user.id}), 问题数量: {question_count}")
        
        # 2. 为admin用户添加示例问题（如果问题较少）
        print("\n2. 为admin用户添加示例问题:")
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            existing_questions = db.query(Question).filter(Question.user_id == admin_user.id).count()
            
            if existing_questions < 5:
                # 添加示例问题
                sample_questions = [
                    {
                        "question": "Python中的列表和元组有什么区别？",
                        "answer": "列表和元组的主要区别：1）可变性：列表可修改，元组不可修改；2）语法：列表用[]，元组用()；3）性能：元组比列表更高效；4）使用场景：列表用于可变序列，元组用于固定数据。元组可以作为字典的键，列表则不行。",
                        "category": "Python"
                    },
                    {
                        "question": "如何学习编程？",
                        "answer": "学习编程的建议：1）选择一门语言开始；2）掌握基础语法；3）多做练习项目；4）阅读优秀代码；5）参与开源项目；6）持续学习和实践。",
                        "category": "学习指导"
                    },
                    {
                        "question": "什么是面向对象编程？",
                        "answer": "面向对象编程（OOP）是一种编程范式，主要特点：1）封装：将数据和方法封装在类中；2）继承：子类可以继承父类的属性和方法；3）多态：同一操作作用于不同对象可以有不同的行为；4）抽象：提取对象的共同特征。",
                        "category": "编程基础"
                    },
                    {
                        "question": "如何调试代码？",
                        "answer": "代码调试技巧：1）使用断点调试；2）打印日志信息；3）使用调试工具；4）逐步执行代码；5）检查变量值；6）理解错误信息；7）单元测试。",
                        "category": "开发技巧"
                    },
                    {
                        "question": "前端和后端有什么区别？",
                        "answer": "前端和后端的区别：1）前端：用户界面和交互，使用HTML/CSS/JavaScript；2）后端：服务器逻辑和数据处理，使用Python/Java/PHP等；3）前端关注用户体验，后端关注业务逻辑和数据处理。",
                        "category": "Web开发"
                    }
                ]
                
                added_count = 0
                for q_data in sample_questions:
                    # 检查是否已存在相同问题
                    existing = db.query(Question).filter(
                        Question.user_id == admin_user.id,
                        Question.question == q_data["question"]
                    ).first()
                    
                    if not existing:
                        question = Question(
                            user_id=admin_user.id,
                            question=q_data["question"],
                            answer=q_data["answer"],
                            category=q_data["category"]
                        )
                        db.add(question)
                        added_count += 1
                        print(f"   添加问题: {q_data['question']}")
                
                db.commit()
                print(f"   [OK] 为admin用户添加了 {added_count} 个示例问题")
            else:
                print(f"   [INFO] admin用户已有 {existing_questions} 个问题，无需添加")
        
        # 3. 验证修复结果
        print("\n3. 验证修复结果:")
        admin_questions = db.query(Question).filter(Question.user_id == admin_user.id).all()
        print(f"   admin用户现在有 {len(admin_questions)} 个问题")
        
        for i, q in enumerate(admin_questions[:3], 1):
            print(f"   {i}. {q.question}")
            print(f"      答案: {q.answer[:50]}...")
        
        print("\n[OK] 修复完成！现在请使用admin用户登录查看问答历史。")
        print("   用户名: admin")
        print("   密码: admin123")
        
    except Exception as e:
        print(f"[ERROR] 修复失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_qa_history()