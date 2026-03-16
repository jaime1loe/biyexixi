# -*- coding: utf-8 -*-
import pymysql
conn = pymysql.connect(host='localhost', user='root', password='12345678', database='qa_system')
cursor = conn.cursor()
cursor.execute("DELETE FROM users WHERE username='debug_test'")
conn.commit()
print("清理完成")
conn.close()
