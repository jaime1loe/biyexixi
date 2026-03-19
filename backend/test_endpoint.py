"""直接测试API端点"""
import sys

# 模拟FastAPI的get_current_user
from app.models import User
from app.database import SessionLocal
from sqlalchemy.orm import Session

# 创建模拟的student用户
db = SessionLocal()
student = db.query(User).filter(User.role == "student").first()

if not student:
    print("没有找到student角色用户")
    sys.exit(1)

print(f"使用学生用户: {student.username}, ID: {student.id}, 角色: {student.role}")

# 现在导入API模块
try:
    from app.routers import course_selection
    print("导入course_selection模块成功")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 检查路由
print(f"\n路由前缀: {course_selection.router.prefix}")
print(f"路由标签: {course_selection.router.tags}")
print(f"路由数量: {len(course_selection.router.routes)}")

for route in course_selection.router.routes:
    print(f"  {route.methods} {route.path}")

db.close()
print("\n模块加载测试完成！")
