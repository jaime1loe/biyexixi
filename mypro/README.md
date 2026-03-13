# 基于大模型智能体的高校知识库在线答疑系统

## 项目简介

本项目是一个基于大模型智能体的高校知识库在线答疑系统，使用Vue3 + FastAPI技术栈开发。

## 技术栈

- **后端**: Python + FastAPI + SQLAlchemy + MySQL
- **前端**: Vue3 + Element Plus + TypeScript
- **AI**: LangChain + RAG（待集成）

## 快速开始

### 后端启动

1. **安装依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **初始化数据库**
   
   查看 `backend/DATABASE_INIT.md` 了解详细的数据库初始化方法。
   
   最简单的方式：
   ```bash
   cd backend
   # 双击运行 init_db_with_pwd.bat，输入MySQL密码
   ```

3. **启动服务**
   ```bash
   python main.py
   ```

   访问 http://localhost:8000/docs 查看API文档

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 项目结构

```
├── backend/           # 后端项目
│   ├── app/          # 应用代码
│   │   ├── routers/ # API路由
│   │   ├── models.py # 数据模型
│   │   └── ...
│   ├── main.py      # 入口文件
│   └── requirements.txt
├── frontend/         # 前端项目
│   ├── src/
│   │   ├── views/   # 页面组件
│   │   ├── router/  # 路由配置
│   │   └── ...
│   └── package.json
└── plan.md          # 项目计划
```

## 功能模块

### 已完成

- [x] 用户认证系统（注册、登录、JWT）
- [x] 问答功能（提问、查看历史）
- [x] 知识库管理（管理员）
- [x] 反馈评价功能
- [x] 数据统计看板
- [x] 用户管理（管理员）

### 待开发

- [ ] 前端页面开发
- [ ] RAG问答引擎
- [ ] 大模型集成
- [ ] 向量数据库

## 测试账号

- 管理员: admin / admin123
- 教师: teacher / 123456
- 学生1: student1 / 123456
- 学生2: student2 / 123456

## 文档

- [后端运行指南](backend/README_CN.md)
- [数据库初始化说明](backend/DATABASE_INIT.md)
- [项目计划](plan.md)
- [需求调研报告](基于大模型智能体的高校知识库在线答疑系统项目需求调研报告.md)

## 团队分工

- **李佳敏**: 后端开发
- **刘佳欣**: 前端开发
- **欧阳格**: AI/大模型
