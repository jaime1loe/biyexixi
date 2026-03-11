#!/usr/bin/env python3
"""
启动后端服务的脚本
"""
import subprocess
import sys
import os
import time

def start_backend():
    """启动后端服务"""
    print("正在启动后端服务...")
    
    # 切换到backend目录
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    
    try:
        # 启动FastAPI服务
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务启动
        print("等待后端服务启动...")
        time.sleep(5)
        
        # 检查服务是否正常启动
        import requests
        try:
            response = requests.get("http://localhost:8000/docs", timeout=10)
            if response.status_code == 200:
                print("✓ 后端服务启动成功")
                print("API文档地址: http://localhost:8000/docs")
                
                # 测试通知API
                print("\n测试通知API...")
                response = requests.get("http://localhost:8000/api/notifications/")
                if response.status_code == 200:
                    notifications = response.json()
                    print(f"✓ 通知API测试成功，获取到 {len(notifications)} 条通知")
                    for notif in notifications[:3]:  # 显示前3条
                        importance = "重要" if notif.get("is_important") == 1 else "普通"
                        print(f"  - [{notif.get('category')}] {notif.get('title')} ({importance})")
                else:
                    print(f"✗ 通知API测试失败，状态码: {response.status_code}")
                    
            else:
                print(f"✗ 后端服务启动异常，状态码: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ 后端服务启动失败: {e}")
            
        return process
        
    except Exception as e:
        print(f"启动后端服务时出错: {e}")
        return None

if __name__ == "__main__":
    process = start_backend()
    if process:
        print("\n后端服务正在运行...")
        print("按 Ctrl+C 停止服务")
        
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n正在停止后端服务...")
            process.terminate()
            process.wait()
            print("后端服务已停止")
    else:
        print("后端服务启动失败")