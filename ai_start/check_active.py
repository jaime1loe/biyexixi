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

cursor.execute("SELECT id, username, is_active, role FROM users")
users = cursor.fetchall()

print("Users status:")
for u in users:
    print(f"  {u[1]}: is_active={u[2]}, role={u[3]}")

cursor.close()
conn.close()
