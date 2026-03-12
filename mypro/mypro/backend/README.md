# 基于大模型智能体的高校知识库在线答疑系统 - 后端

这是一个基于 Python FastAPI 开发的后端服务，为高校知识库在线答疑系统提供API接口。

## 技术栈

- FastAPI - 高性能Web框架
- SQLAlchemy - ORM框架
- MySQL - 关系型数据库
- JWT - 用户认证
- LangChain - AI功能支持（后续阶段）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接等信息。

### 3. 创建数据库

确保MySQL已安装并运行，然后创建数据库：

```sql
CREATE DATABASE qa_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问API文档

启动后访问 `http://localhost:8000/docs` 查看自动生成的API文档。

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   ├── database.py        # 数据库连接
│   ├── models.py          # 数据库模型
│   ├── schemas.py         # Pydantic模型
│   ├── utils.py           # 工具函数
│   ├── dependencies.py    # 依赖注入
│   └── routers/          # 路由模块
│       ├── __init__.py
│       ├── auth.py        # 认证接口
│       ├── questions.py   # 问答接口
│       ├── knowledge.py   # 知识库接口
│       ├── feedback.py    # 反馈接口
│       └── statistics.py  # 统计接口
├── main.py                # 应用入口
├── requirements.txt       # 依赖列表
├── .env.example           # 环境变量示例
└── .gitignore            # Git忽略文件
```

## API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 问答相关
- `POST /api/questions/` - 提问
- `GET /api/questions/` - 获取问题列表
- `GET /api/questions/{question_id}` - 获取问题详情

### 知识库相关
- `POST /api/knowledge/` - 添加知识
- `GET /api/knowledge/` - 获取知识列表
- `GET /api/knowledge/{knowledge_id}` - 获取知识详情
- `DELETE /api/knowledge/{knowledge_id}` - 删除知识

### 反馈相关
- `POST /api/feedback/` - 提交反馈
- `GET /api/feedback/` - 获取反馈列表

### 统计相关
- `GET /api/statistics/overview` - 获取数据概览
- `GET /api/statistics/daily` - 获取每日统计

## 数据库模型

- User - 用户表
- Question - 问题表
- Feedback - 反馈评价表
- Knowledge - 知识库表
- Statistics - 统计表

## 后续开发计划

- [ ] 实现JWT认证中间件
- [ ] 集成向量数据库
- [ ] 实现RAG问答引擎
- [ ] 集成大模型服务
- [ ] 文件上传功能
- [ ] 数据导出功能
