import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='12345678',
    database='qa_system',
    charset='utf8mb4'
)

cursor = conn.cursor()

# Correct password hash for '123456' using sha256_crypt
# This is the same hash from init_test_data.sql
correct_hash = '$5$rounds=535000$Xkg4VvIF5yTX9WFx$R.z2qxr1F0f4oBuCb8WCV2LPEBjfCJpG6h1.zfECrC8'

# Update admin
cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'admin'", (correct_hash,))

# Update student
cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'student'", (correct_hash,))

# Update teacher
cursor.execute("UPDATE users SET password_hash = %s WHERE username = 'teacher'", (correct_hash,))

conn.commit()

# Verify
cursor.execute("SELECT username, password_hash FROM users")
users = cursor.fetchall()

print("Updated users:")
for u in users:
    print(f"  {u[0]}: {u[1][:50]}...")

cursor.close()
conn.close()

print("\n[OK] Password hashes fixed!")
