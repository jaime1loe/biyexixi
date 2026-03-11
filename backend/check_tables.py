import pymysql

conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()
cursor.execute('SHOW TABLES')
tables = cursor.fetchall()
print('数据库表:')
for t in tables:
    print(f'  - {t[0]}')
conn.close()

if not tables:
    print('\n数据库中没有表！需要运行初始化脚本')
    print('运行: python reset_data_auto.py && python init_data.py')
