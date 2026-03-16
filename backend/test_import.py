"""
测试导入profile_changes模块，看是否有错误
"""
import sys
import traceback

print("测试导入 profile_changes 路由模块...")
print()

try:
    from app.routers import profile_changes
    print("[OK] 导入成功")

    # 检查路由
    print(f"\n路由前缀: {profile_changes.router.prefix}")
    print(f"路由标签: {profile_changes.router.tags}")

    # 检查所有路由
    print("\n模块中的所有路由:")
    for route in profile_changes.router.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = [m for m in route.methods if m != 'HEAD']
            print(f"  {methods} {route.path}")

except Exception as e:
    print(f"[ERROR] 导入失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n测试完成")
