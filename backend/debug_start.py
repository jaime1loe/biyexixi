#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端启动调试脚本
用于诊断后端启动失败的具体原因
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖包是否安装"""
    print("=" * 60)
    print("1. 检查Python依赖包...")
    
    dependencies = [
        'fastapi', 'uvicorn', 'pydantic', 'pydantic-settings',
        'sqlalchemy', 'pymysql', 'python-jose', 'passlib'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✓ {dep}")
        except ImportError:
            missing.append(dep)
            print(f"   ✗ {dep} - 未安装")
    
    if missing:
        print(f"\n[警告] 缺少依赖包: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))
    else:
        print("\n[成功] 所有依赖包已安装")

def check_python_path():
    """检查Python路径设置"""
    print("\n" + "=" * 60)
    print("2. 检查Python路径...")
    
    # 添加项目根目录到Python路径
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    print(f"   项目根目录: {project_root}")
    print(f"   Python路径: {sys.path[:3]}...")
    
    # 测试导入
    try:
        from app.config import settings
        print(f"   ✓ 配置导入成功: {settings.APP_NAME}")
    except Exception as e:
        print(f"   ✗ 配置导入失败: {e}")
        return False
    
    return True

def check_database_connection():
    """检查数据库连接"""
    print("\n" + "=" * 60)
    print("3. 检查数据库连接...")
    
    try:
        from app.database import engine
        
        # 测试连接
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print(f"   ✓ 数据库连接成功")
            
            # 检查表是否存在
            result = conn.execute("SHOW TABLES LIKE 'users'")
            if result.fetchone():
                print(f"   ✓ 用户表存在")
            else:
                print(f"   ✗ 用户表不存在，需要初始化数据库")
                
    except Exception as e:
        print(f"   ✗ 数据库连接失败: {e}")
        return False
    
    return True

def test_imports():
    """测试所有模块导入"""
    print("\n" + "=" * 60)
    print("4. 测试模块导入...")
    
    modules_to_test = [
        'app.routers.auth',
        'app.routers.questions', 
        'app.routers.knowledge',
        'app.routers.feedback',
        'app.routers.statistics',
        'app.routers.users',
        'app.routers.favorites',
        'app.routers.notifications',
        'app.routers.campus',
        'app.exceptions'
    ]
    
    failed = []
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✓ {module}")
        except Exception as e:
            failed.append((module, str(e)))
            print(f"   ✗ {module}: {e}")
    
    if failed:
        print(f"\n[警告] {len(failed)} 个模块导入失败")
        for module, error in failed:
            print(f"   {module}: {error}")
        return False
    else:
        print("\n[成功] 所有模块导入正常")
        return True

def main():
    """主函数"""
    print("后端启动调试诊断")
    print("=" * 60)
    
    # 检查依赖
    check_dependencies()
    
    # 检查路径
    if not check_python_path():
        print("\n[错误] Python路径设置失败，无法继续")
        return
    
    # 检查数据库
    if not check_database_connection():
        print("\n[错误] 数据库连接失败，无法启动")
        return
    
    # 测试导入
    if not test_imports():
        print("\n[错误] 模块导入失败，无法启动")
        return
    
    print("\n" + "=" * 60)
    print("诊断完成！")
    print("如果所有检查都通过，可以尝试启动后端服务")
    print("启动命令: python main.py")
    
    # 询问是否尝试启动
    try:
        choice = input("\n是否尝试启动后端服务？(y/n): ")
        if choice.lower() in ['y', 'yes']:
            print("\n启动后端服务...")
            import subprocess
            subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n用户取消启动")

if __name__ == "__main__":
    main()