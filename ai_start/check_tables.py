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

# Check questions table structure
cursor.execute("DESCRIBE questions")
columns = cursor.fetchall()

print("Questions table structure:")
for col in columns:
    print(f"  {col[0]}: {col[1]}")

cursor.close()
conn.close()
