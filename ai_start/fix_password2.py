from passlib.context import CryptContext
import pymysql

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Generate correct hash for '123456'
correct_hash = pwd_context.hash('123456')
print(f"Generated hash: {correct_hash}")

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system',
    charset='utf8mb4'
)

cursor = conn.cursor()

# Update all users with the new hash
cursor.execute("UPDATE users SET password_hash = %s", (correct_hash,))
conn.commit()

# Verify
cursor.execute("SELECT username, password_hash FROM users")
users = cursor.fetchall()

print("\nUpdated users:")
for u in users:
    print(f"  {u[0]}: {u[1]}")

# Test verification
test_hash = users[0][1]
result = pwd_context.verify('123456', test_hash)
print(f"\nVerification test: {result}")

cursor.close()
conn.close()
print("\n[OK] Password hashes fixed!")
