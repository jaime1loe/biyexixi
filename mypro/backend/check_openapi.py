import requests
import json

# 获取OpenAPI文档
response = requests.get("http://localhost:8000/openapi.json")
openapi = response.json()

print("检查所有 profile-changes 路由:")
print()

paths = openapi.get("paths", {})
for path, methods in paths.items():
    if "profile-changes" in path:
        print(f"路径: {path}")
        for method, details in methods.items():
            print(f"  {method.upper()}: {details.get('summary', '')}")
        print()
