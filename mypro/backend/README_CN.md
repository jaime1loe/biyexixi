# 后端运行指南

## 前置要求

1. **Python 3.8+**
2. **MySQL 5.7+**

## 快速开始

### 1. 安装依赖

#### 方式一：安装核心依赖（推荐，当前阶段必需）
```bash
cd backend
pip install -r requirements-core.txt
```

#### 方式二：安装完整依赖（包含AI相关包）
```bash
pip install -r requirements.txt
```

**说明**：
- `requirements-core.txt` - 只包含后端基础功能所需的包
- `requirements-ai.txt` - AI相关依赖（RAG、LLM等，后续阶段使用）
- `requirements.txt` - 完整依赖（上述两者合并）

#### 使用国内镜像加速
```bash
pip install -r requirements-core.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置环境变量

`.env` 文件已创建，如需修改数据库密码，编辑 `backend/.env` 文件：

```env
DB_PASSWORD=你的MySQL密码
```

### 3. 创建数据库

**推荐方式：使用批处理脚本**
```bash
# 双击运行 init_db_with_pwd.bat，输入MySQL密码
```

**或使用命令行：**
```bash
mysql -u root -p < init_database.sql
```

**或使用Python脚本：**
```bash
python create_db.py
```

**手动创建数据库：**
```sql
CREATE DATABASE qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

详细说明请查看 `DATABASE_INIT.md`

### 4. 启动服务

#### Windows:
```bash
start.bat
```

#### Linux/Mac:
```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

启动成功后访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 6. 初始化测试数据（可选）

```bash
python init_data.py
```

这会创建测试用户：
- 管理员: admin / admin123
- 学生: student / 123456

## API端点

### 认证
- POST /api/auth/register - 注册
- POST /api/auth/login - 登录
- GET /api/auth/me - 获取当前用户

### 问答
- POST /api/questions/ - 提问
- GET /api/questions/my - 我的问题
- GET /api/questions/ - 问题列表

### 知识库（管理员）
- POST /api/knowledge/ - 添加知识
- GET /api/knowledge/ - 知识列表
- DELETE /api/knowledge/{id} - 删除知识

### 反馈
- POST /api/feedback/ - 提交评价
- GET /api/feedback/my - 我的反馈

### 统计（管理员）
- GET /api/statistics/overview - 数据概览
- GET /api/statistics/daily - 每日统计

## 故障排除

### 数据库连接失败
1. 检查MySQL是否启动
2. 检查 `.env` 中的数据库配置
3. 确认数据库用户权限

### 端口占用
修改 `.env` 中的 `PORT` 配置

### 依赖安装失败
使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
