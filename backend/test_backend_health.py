"""测试后端健康状态"""
import requests

try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"后端健康检查: {response.status_code}")
    print(f"响应内容: {response.json()}")
except Exception as e:
    print(f"无法连接到后端: {e}")

try:
    # 尝试访问API文档
    response = requests.get("http://localhost:8000/docs", timeout=5)
    print(f"\nAPI文档: {response.status_code}")
except Exception as e:
    print(f"无法访问API文档: {e}")
