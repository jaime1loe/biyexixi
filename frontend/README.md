# 高校知识库智能答疑系统 - 前端项目

## 项目概述

基于 Vue3 + Element Plus + TypeScript 开发的智能答疑系统前端界面,包含智能问答、问答历史、知识库管理、数据统计看板等功能模块。

## 技术栈

- Vue 3.4+
- TypeScript
- Vite 5.0
- Element Plus 2.5+
- Vue Router 4.2+
- Pinia 2.1+
- Axios 1.6+

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/               # API接口
│   │   ├── index.ts      # Axios封装
│   │   ├── chat.ts       # 聊天相关API
│   │   ├── dashboard.ts  # 看板统计API
│   │   └── knowledge.ts  # 知识库管理API
│   ├── components/       # 公共组件
│   │   └── Layout.vue    # 主布局组件
│   ├── views/            # 页面组件
│   │   ├── Login.vue     # 登录注册页面
│   │   ├── Chat.vue      # 智能问答页面
│   │   ├── History.vue   # 问答历史页面
│   │   ├── Knowledge.vue # 知识库管理页面
│   │   └── Dashboard.vue # 数据统计看板
│   ├── router/           # 路由配置
│   │   └── index.ts
│   ├── store/            # 状态管理
│   │   └── user.ts       # 用户状态
│   ├── styles/           # 全局样式
│   │   └── global.css
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── index.html            # HTML模板
├── package.json          # 项目配置
├── tsconfig.json         # TypeScript配置
├── vite.config.ts        # Vite配置
└── README.md             # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 `http://localhost:5173`

### 3. 构建生产版本

```bash
npm run build
```

## 功能模块

### 1. 登录注册 (Login.vue)
- 登录/注册切换
- 表单验证
- 用户身份选择(学生/教师/管理员)
- 记住密码
- 用户协议确认
- 登录状态管理

### 2. 智能问答 (Chat.vue)
- 实时对话界面
- 消息展示与格式化
- 评价打星功能
- 热门问题推荐
- 相关问题推荐
- 打字动画效果

### 3. 问答历史 (History.vue)
- 历史记录列表
- 关键词搜索
- 日期范围筛选
- 查看详情
- 删除记录
- 导出功能

### 4. 知识库管理 (Knowledge.vue)
- 文档上传功能
- 文档状态管理
- 分类管理
- 数据统计卡片
- 文档列表展示

### 5. 数据统计看板 (Dashboard.vue)
- 核心指标卡片
- 提问趋势图表
- 问题分类统计
- 热门问题TOP5
- 最近活动记录

### 6. 用户管理
- 用户信息展示
- 个人中心(开发中)
- 系统设置(开发中)
- 退出登录

## API 接口

### 聊天接口
- `POST /api/chat/ask` - 发送问题
- `GET /api/chat/history` - 获取历史记录
- `POST /api/chat/feedback` - 提交评价

### 看板接口
- `GET /api/dashboard/stats` - 获取统计数据

### 知识库接口
- `POST /api/knowledge/upload` - 上传文档
- `GET /api/knowledge/list` - 获取文档列表
- `DELETE /api/knowledge/:id` - 删除文档

## 设计规范

### 颜色系统
- 主色: #1890FF
- 辅助色: #40A9FF
- 背景色: #F5F7FA
- 文字色: #303133
- 成功色: #67C23A
- 警告色: #F56C6C

### 字体系统
- 字体: PingFang SC, Microsoft YaHei
- 标题: 24px / 18px
- 正文: 14px

## 开发说明

### 环境要求
- Node.js >= 16
- npm >= 8

### 代码规范
- 使用 TypeScript 类型检查
- 遵循 Vue 3 Composition API
- 组件命名使用 PascalCase
- 文件命名使用 kebab-case

### 后端联调
后端服务地址默认为 `http://localhost:8080`,可在 `vite.config.ts` 中修改代理配置。

## 注意事项

1. 所有页面都需要在 Layout 布局组件内展示
2. API请求已配置拦截器,自动添加token和错误处理
3. 使用 Pinia 进行状态管理
4. Element Plus 图标需手动注册(已在 main.ts 中完成)

## 开发者

- 刘佳欣 (前端开发)
- 项目时间: 2026年毕业实习
