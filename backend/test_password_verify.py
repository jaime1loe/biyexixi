"""
测试密码验证
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.utils import verify_password

# 测试 pbkdf2_sha256 哈希验证
hashed_password = "$pbkdf2-sha256$29000$zDlnTAlhjLF2zrk3prSWsg$Fur4BxcLQXABHHLhxCmyDmtRdjn1PQFKJaBG8qrNQd8"
test_password = "admin123"

print("测试密码验证")
print("=" * 60)
print(f"哈希密码: {hashed_password[:50]}...")
print(f"测试密码: {test_password}")

result = verify_password(test_password, hashed_password)
print(f"验证结果: {result}")

if result:
    print("\n[成功] 密码验证通过!")
else:
    print("\n[失败] 密码验证失败!")
