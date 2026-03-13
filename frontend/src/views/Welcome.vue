<template>
  <div class="welcome-container">
    <div class="welcome-content">
      <div class="welcome-header">
        <div class="welcome-logo">
          <el-icon size="64" color="#409eff"><ChatLineSquare /></el-icon>
        </div>
        <h1>高校知识库智能答疑系统</h1>
        <p>基于大模型的智能问答平台</p>
      </div>

      <div class="welcome-cards">
        <div class="welcome-card user-card" @click="gotoUserLogin">
          <div class="card-icon">
            <el-icon size="48" color="#409eff"><User /></el-icon>
          </div>
          <div class="card-content">
            <h3>学生/教师登录</h3>
            <p>进入智能问答系统，体验AI助教服务</p>
            <ul>
              <li>智能问答对话</li>
              <li>知识库查询</li>
              <li>问答历史记录</li>
              <li>校园服务</li>
            </ul>
          </div>
          <div class="card-action">
            <el-button type="primary" size="large">
              进入系统 <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>

        <div class="welcome-card admin-card" @click="gotoAdminLogin">
          <div class="card-icon">
            <el-icon size="48" color="#f56c6c"><Setting /></el-icon>
          </div>
          <div class="card-content">
            <h3>管理员登录</h3>
            <p>进入管理后台，管理系统数据</p>
            <ul>
              <li>用户管理</li>
              <li>问答管理</li>
              <li>知识库审核</li>
              <li>数据统计</li>
            </ul>
          </div>
          <div class="card-action">
            <el-button type="danger" size="large">
              管理后台 <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </div>

      <div class="welcome-footer">
        <p>© 2026 高校知识库智能答疑系统 | 毕业设计项目</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ChatLineSquare, User, Setting, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

function gotoUserLogin() {
  router.push('/login')
}

function gotoAdminLogin() {
  router.push('/admin/login')
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.welcome-content {
  width: 100%;
  max-width: 900px;
  text-align: center;
}

.welcome-header {
  margin-bottom: 60px;
}

.welcome-logo {
  margin-bottom: 24px;
}

.welcome-header h1 {
  margin: 0 0 12px;
  font-size: 36px;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.welcome-header p {
  margin: 0;
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
}

.welcome-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.welcome-card {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 380px;
}

.welcome-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
}

.user-card {
  border-top: 4px solid #409eff;
}

.admin-card {
  border-top: 4px solid #f56c6c;
}

.card-icon {
  margin-bottom: 24px;
}

.card-content {
  flex: 1;
  text-align: left;
}

.card-content h3 {
  margin: 0 0 12px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.card-content p {
  margin: 0 0 16px;
  font-size: 16px;
  color: #606266;
  line-height: 1.5;
}

.card-content ul {
  margin: 0;
  padding-left: 16px;
  color: #909399;
  line-height: 1.6;
}

.card-content li {
  margin-bottom: 4px;
}

.card-action {
  margin-top: auto;
}

.card-action .el-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.welcome-footer {
  text-align: center;
}

.welcome-footer p {
  margin: 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-cards {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  .welcome-card {
    height: auto;
    padding: 30px;
  }
  
  .welcome-header h1 {
    font-size: 28px;
  }
}
</style>