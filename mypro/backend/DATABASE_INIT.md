# 数据库初始化说明

## 方法一：使用批处理脚本（推荐）

双击运行 `init_db_with_pwd.bat`，然后输入MySQL root密码。

## 方法二：使用MySQL命令行

```bash
cd backend
mysql -u root -p < init_database.sql
```

输入密码后即可自动创建数据库和表。

## 方法三：使用MySQL Workbench

1. 打开MySQL Workbench
2. 连接到本地MySQL服务器
3. File -> Open SQL Script
4. 选择 `backend/init_database.sql`
5. 点击执行（闪电图标）

## 方法四：在MySQL客户端中手动执行

```bash
mysql -u root -p
```

然后复制粘贴 `init_database.sql` 的内容执行。

---

## 数据库创建成功后

### 初始化测试数据（可选）

```bash
cd backend
pip install pymysql passlib python-jose bcrypt
python init_data.py
```

这将创建以下测试账号：
- 管理员: admin / admin123
- 教师: teacher / 123456
- 学生1: student1 / 123456
- 学生2: student2 / 123456

### 启动后端服务

```bash
cd backend
pip install -r requirements.txt
python main.py
```

或使用启动脚本：
```bash
cd backend
start.bat
```

---

## 已创建的表结构

| 表名 | 说明 |
|------|------|
| users | 用户表 |
| questions | 问题表 |
| feedbacks | 反馈评价表 |
| knowledge | 知识库表 |
| statistics | 统计表 |

---

## MySQL密码相关

如果忘记了MySQL密码，可以重置：

1. 停止MySQL服务
2. 以安全模式启动：`mysqld --skip-grant-tables`
3. 连接并重置密码：`mysql -u root`
4. 在MySQL中执行：
```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```
5. 重启MySQL服务
