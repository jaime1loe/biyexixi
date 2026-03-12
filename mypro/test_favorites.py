#!/usr/bin/env python3
"""
测试收藏功能的完整流程
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_favorites_api():
    """测试收藏API功能"""
    try:
        # 导入必要的模块
        from backend.app.database import get_db
        from backend.app.models import Favorite, Question, User
        
        # 获取数据库会话
        db = next(get_db())
        
        print("=== 收藏功能测试 ===")
        
        # 1. 检查收藏表结构
        print("\n1. 检查收藏表结构...")
        favorites = db.query(Favorite).all()
        print(f"收藏表中有 {len(favorites)} 条记录")
        
        # 2. 检查用户和问题数据
        print("\n2. 检查用户和问题数据...")
        users = db.query(User).limit(3).all()
        questions = db.query(Question).limit(3).all()
        
        print(f"用户数量: {len(users)}")
        print(f"问题数量: {len(questions)}")
        
        if users and questions:
            # 3. 测试收藏功能
            print("\n3. 测试收藏功能...")
            
            # 检查第一个用户和第一个问题
            test_user = users[0]
            test_question = questions[0]
            
            print(f"测试用户: {test_user.username} (ID: {test_user.id})")
            print(f"测试问题: {test_question.question[:50]}... (ID: {test_question.id})")
            
            # 检查是否已收藏
            existing_favorite = db.query(Favorite).filter(
                Favorite.user_id == test_user.id,
                Favorite.knowledge_id == test_question.id
            ).first()
                
            if existing_favorite:
                print(f"[OK] 问题已被收藏 (收藏ID: {existing_favorite.id})")
            else:
                print("[OK] 问题尚未被收藏")
                
                # 创建测试收藏
                new_favorite = Favorite(
                    user_id=test_user.id,
                    knowledge_id=test_question.id
                )
                db.add(new_favorite)
                db.commit()
                print(f"[OK] 已创建测试收藏 (ID: {new_favorite.id})")
        
        # 4. 检查收藏与问题的关联
        print("\n4. 检查收藏与问题的关联...")
        for fav in favorites[:3]:  # 只显示前3条
            question = db.query(Question).filter(Question.id == fav.knowledge_id).first()
            user = db.query(User).filter(User.id == fav.user_id).first()
            
            if question and user:
                print(f"收藏ID: {fav.id} | 用户: {user.username} | 问题: {question.question[:30]}...")
        
        print("\n=== 收藏功能测试完成 ===")
        
    except Exception as e:
        print(f"[ERROR] 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_favorites_api()