---
name: 基于大模型智能体的高校知识库在线答疑系统
overview: 构建一个本科毕业设计级别的智能答疑系统，使用Vue+Python(FastAPI)技术栈，整合开源大模型（ChatGLM/Qwen）实现智能问答，核心功能包括RAG知识库问答、启发式学习引导、个性化推荐等。
design:
  styleKeywords:
    - 简洁
    - 现代
    - 教育
  fontSystem:
    fontFamily: PingFang-SC
    heading:
      size: 24px
      weight: 600
    subheading:
      size: 18px
      weight: 500
    body:
      size: 14px
      weight: 400
  colorSystem:
    primary:
      - "#1890FF"
      - "#40A9FF"
    background:
      - "#F5F7FA"
      - "#FFFFFF"
    text:
      - "#303133"
    functional:
      - "#67C23A"
      - "#F56C6C"
todos:
  - id: setup-backend
    content: 创建Python FastAPI后端项目，配置MySQL数据库连接
    status: completed
  - id: setup-frontend
    content: 创建Vue3前端项目，集成Element Plus组件库
    status: in_progress
  - id: deploy-llm
    content: 部署开源大模型（ChatGLM或Qwen）
    status: pending
  - id: user-auth
    content: 实现用户登录注册功能
    status: pending
  dependencies:
    - setup-backend
  - id: qa-interface
    content: 开发智能问答前端界面
    status: pending
  dependencies:
    - setup-frontend
    - user-auth
  - id: qa-api
    content: 开发智能问答后端API
    status: pending
  dependencies:
    - setup-backend
  - id: rag-engine
    content: 实现RAG问答引擎（向量化+检索+生成）
    status: pending
  dependencies:
    - deploy-llm
  - id: knowledge-mgmt
    content: 开发知识库管理功能（文档上传、向量化存储）
    status: pending
  dependencies:
    - qa-api
    - rag-engine
  - id: mock-data
    content: 构建模拟高校知识库数据（50-100条QA）
    status: pending
  dependencies:
    - knowledge-mgmt
  - id: qa-history
    content: 实现问答历史记录功能
    status: pending
  dependencies:
    - qa-api
  - id: feedback
    content: 开发问答评价反馈功能
    status: pending
  dependencies:
    - qa-api
  - id: dashboard
    content: 实现基础数据统计看板
    status: pending
  dependencies:
    - qa-api
  - id: test-optimize
    content: 系统测试与性能优化
    status: pending
  dependencies:
    - qa-history
    - feedback
    - dashboard
---

## 产品概述

基于大模型智能体的高校知识库在线答疑系统，旨在为高校学生提供智能问答服务。

## 核心功能（精简至6个）

1. **智能问答**: 基于RAG技术的高校知识问答
2. **知识库管理**: 管理员维护知识库（文档上传+向量存储）
3. **问答历史**: 用户查看历史问答记录
4. **反馈评价**: 用户对答案进行星级评价
5. **个性化推荐**: 根据用户身份推荐相关内容
6. **数据统计看板**: 问答数量、满意度等基础统计

## 技术栈选择

- **后端**: Python + FastAPI + SQLAlchemy
- **前端**: Vue3 + Element Plus
- **数据库**: MySQL + SQLite(简化向量存储)
- **AI**: Python + LangChain + ChatGLM/Qwen开源模型
- **通信**: RESTful API

## 系统架构

前后端分离架构：

- 前端：Vue3单页应用
- 后端：FastAPI提供API服务和AI智能问答接口

## RAG问答流程

1. 用户输入问题 → 2. 问题向量化 → 3. 向量相似度检索 → 4. 召回相关文档作为上下文 → 5. 调用大模型生成答案

## 设计风格

采用简洁现代的设计风格，使用Element Plus组件库实现基础管理界面。

## 任务列表



- [x] 1. 创建Python FastAPI后端项目，配置MySQL数据库连接
- [ ] 2. 创建Vue3前端项目，集成Element Plus组件库
- [ ] 3. 部署开源大模型（ChatGLM或Qwen）
- [ ] 4. 实现用户登录注册功能
- [ ] 5. 开发智能问答前端界面
- [ ] 6. 开发智能问答后端API
- [ ] 7. 实现RAG问答引擎（向量化+检索+生成）
- [ ] 8. 开发知识库管理功能（文档上传、向量化存储）
- [ ] 9. 构建模拟高校知识库数据（50-100条QA）
- [ ] 10. 实现问答历史记录功能
- [ ] 11. 开发问答评价反馈功能
- [ ] 12. 实现基础数据统计看板
- [ ] 13. 系统测试与性能优化



## 项目计划概要

### 第一阶段：环境搭建

1. **创建Python FastAPI后端项目** - 配置MySQL数据库连接
2. **创建Vue3前端项目** - 集成Element Plus组件库

### 第二阶段：大模型部署

1. **部署开源大模型** - ChatGLM3-6B或Qwen2-7B（本地部署）

### 第三阶段：核心功能开发

1. **实现用户登录注册功能**
2. **开发智能问答前端界面**
3. **开发智能问答后端API**
4. **实现RAG问答引擎** - 向量化+检索+生成
5. **开发知识库管理功能** - 文档上传、向量化存储

### 第四阶段：数据与扩展功能

1. **构建模拟高校知识库数据** - 50-100条QA
2. **实现问答历史记录功能**
3. **开发问答评价反馈功能**
4. **实现基础数据统计看板**

### 第五阶段：收尾

1. **系统测试与性能优化**



## 技术架构说明

| 层级   | 技术选型                           |
| ------ | ---------------------------------- |
| 前端   | Vue3 + Element Plus                |
| 后端   | FastAPI + SQLAlchemy + MySQL       |
| AI服务 | Python + LangChain + RAG           |
| 大模型 | ChatGLM3-6B / Qwen2-7B（本地部署） |



## 团队分工方案

### 李佳敏：后端开发（5个任务）

| 任务ID         | 任务内容                                    | 优先级 |
| -------------- | ------------------------------------------- | ------ |
| setup-backend  | 创建Python FastAPI后端项目，配置MySQL数据库连接 | 高     |
| user-auth      | 实现用户登录注册功能                        | 高     |
| qa-api         | 开发智能问答后端API                         | 高     |
| knowledge-mgmt | 开发知识库管理功能（后端接口）              | 高     |
| qa-history     | 实现问答历史记录功能                        | 中     |

------

### 刘佳欣：前端开发（5个任务）

| 任务ID         | 任务内容                                 | 优先级 |
| -------------- | ---------------------------------------- | ------ |
| setup-frontend | 创建Vue3前端项目，集成Element Plus组件库 | 高     |
| qa-interface   | 开发智能问答前端界面                     | 高     |
| dashboard      | 实现基础数据统计看板                     | 中     |
| feedback       | 开发问答评价反馈功能（前端界面）         | 中     |
| link           | 前后端连接                               | 高     |

------

### 欧阳格：AI/大模型（4个任务）

| 任务ID       | 任务内容                                   | 优先级 |
| ------------ | ------------------------------------------ | ------ |
| setup-ai-env | 搭建Python AI服务环境，安装LangChain等依赖 | 高     |
| deploy-llm   | 部署开源大模型（ChatGLM3-6B或Qwen2-7B）    | 高     |
| rag-engine   | 实现RAG问答引擎（向量化+检索+生成）        | 高     |
| mock-data    | 构建模拟高校知识库数据（50-100条QA）       | 中     |

------

### 公共任务：全员参与

| 任务ID        | 任务内容           |
| ------------- | ------------------ |
| test-optimize | 系统测试与性能优化 |

------

## 分工说明

| 成员       | 技术栈                    | 主要职责                           | 工作占比 |
| ---------- | ------------------------- | ---------------------------------- | -------- |
| **李佳敏** | Python + FastAPI + MySQL | 后端API开发、数据库设计            | ~33%     |
| **刘佳欣** | Vue3 + Element Plus       | 前端界面开发、用户交互、前后端连接 | ~33%     |
| **欧阳格** | Python + LangChain + LLM  | AI引擎、大模型部署、RAG            | ~33%     |