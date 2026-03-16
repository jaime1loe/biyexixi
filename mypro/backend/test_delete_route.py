"""
检查profile_changes路由文件中的所有路由
"""
import ast
import inspect

# 读取文件内容
with open('app/routers/profile_changes.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("profile_changes.py 文件中的所有路由")
print("=" * 60)
print()

# 解析文件
tree = ast.parse(content)

# 查找所有装饰器
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        # 获取函数名
        func_name = node.name
        
        # 获取装饰器
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Attribute):
                    method = decorator.func.attr
                    path_parts = []
                    for arg in decorator.args:
                        if isinstance(arg, ast.Constant):
                            path_parts.append(arg.value)
                    path = ''.join(path_parts) if path_parts else 'unknown'
                    decorators.append(f"{method.upper()} {path}")
        
        if decorators:
            print(f"函数名: {func_name}")
            for dec in decorators:
                print(f"  路由: {dec}")
            print()

print("=" * 60)
print("文件最后几行:")
print("=" * 60)
lines = content.split('\n')
for i, line in enumerate(lines[-10:], len(lines)-9):
    print(f"{i}: {line}")
