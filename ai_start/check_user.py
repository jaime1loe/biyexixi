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

cursor.execute("SELECT id, username, password_hash, role FROM users")
users = cursor.fetchall()

print("Users in database:")
for u in users:
    print(f"  ID: {u[0]}, Username: {u[1]}, Role: {u[3]}")
    print(f"    Hash: {u[2]}")

cursor.close()
conn.close()
