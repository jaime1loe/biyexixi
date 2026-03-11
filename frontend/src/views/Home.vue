<template>
  <div class="home-container">
    <!-- 头部横幅 -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">智能问答</span>
          <span class="normal-text">知识库系统</span>
        </h1>
        <p class="hero-subtitle">基于大模型的高校智能答疑平台，助您快速获取答案</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" :icon="ChatLineRound" @click="goToChat">
            开始提问
          </el-button>
          <el-button size="large" :icon="Document" @click="goToKnowledge">
            浏览知识库
          </el-button>
        </div>
      </div>
      <div class="hero-illustration">
        <div class="floating-card card-1">
          <el-icon><QuestionFilled /></el-icon>
          <span>智能问答</span>
        </div>
        <div class="floating-card card-2">
          <el-icon><Reading /></el-icon>
          <span>知识检索</span>
        </div>
        <div class="floating-card card-3">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据分析</span>
        </div>
      </div>
    </div>

    <!-- 快速入口 -->
    <div class="quick-access-section">
      <h2 class="section-title">
        <el-icon><Grid /></el-icon>
        快速入口
      </h2>
      <div class="quick-access-grid">
        <div class="quick-access-item" @click="goToPath('/chat')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <h3>智能问答</h3>
          <p>AI智能回答您的问题</p>
        </div>
        <div class="quick-access-item" @click="goToPath('/history')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <el-icon><Clock /></el-icon>
          </div>
          <h3>问答历史</h3>
          <p>查看历史提问记录</p>
        </div>
        <div class="quick-access-item" @click="goToPath('/knowledge')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <el-icon><Collection /></el-icon>
          </div>
          <h3>知识库</h3>
          <p>浏览和管理知识文档</p>
        </div>
        <div class="quick-access-item" @click="goToPath('/dashboard')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <el-icon><DataLine /></el-icon>
          </div>
          <h3>数据统计</h3>
          <p>查看系统使用统计</p>
        </div>
        <div class="quick-access-item" @click="goToPath('/favorites')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <el-icon><StarFilled /></el-icon>
          </div>
          <h3>我的收藏</h3>
          <p>收藏的问题和回答</p>
        </div>
        <div class="quick-access-item" @click="goToPath('/campus')">
          <div class="quick-icon" style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);">
            <el-icon><School /></el-icon>
          </div>
          <h3>校园服务</h3>
          <p>空教室、成绩查询等</p>
        </div>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="stats-section">
      <h2 class="section-title">
        <el-icon><DataBoard /></el-icon>
        系统概况
      </h2>
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.userCount }}</div>
              <div class="stat-label">注册用户</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.questionCount }}</div>
              <div class="stat-label">问答数量</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.knowledgeCount }}</div>
              <div class="stat-label">知识文档</div>
            </div>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6">
          <div class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.avgRating }}</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 最新通知 -->
    <div class="notifications-section">
      <h2 class="section-title">
        <el-icon><Bell /></el-icon>
        最新通知
      </h2>
      <el-empty v-if="notifications.length === 0" description="暂无通知" />
      <div v-else class="notification-list">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification-item"
        >
          <div class="notification-icon" :class="{ important: notification.is_important }">
            <el-icon><Document /></el-icon>
          </div>
          <div class="notification-content">
            <h4>{{ notification.title }}</h4>
            <p>{{ notification.content }}</p>
            <span class="notification-meta">
              <el-tag v-if="notification.is_important" type="danger" size="small">重要</el-tag>
              <el-tag v-if="notification.category" size="small">{{ notification.category }}</el-tag>
              <span class="time">{{ formatTime(notification.created_at) }}</span>
            </span>
          </div>
          <div v-if="notification.file_path" class="notification-action">
            <el-button link type="primary" size="small" @click="downloadNotification(notification)">
              下载附件
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ChatLineRound,
  Document,
  ChatDotRound,
  Clock,
  Collection,
  DataLine,
  StarFilled,
  School,
  User,
  DataBoard,
  Star,
  Bell,
  Grid,
  QuestionFilled,
  Reading,
  DataAnalysis
} from '@element-plus/icons-vue'
import { dashboardApi } from '@/api/dashboard'
import { notificationApi } from '@/api/notifications'

const router = useRouter()

const stats = ref({
  userCount: 0,
  questionCount: 0,
  knowledgeCount: 0,
  avgRating: 0
})

const notifications = ref<any[]>([])

function goToChat() {
  router.push('/chat')
}

function goToKnowledge() {
  router.push('/knowledge')
}

function goToPath(path: string) {
  router.push(path)
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN')
}

async function downloadNotification(notification: any) {
  // 实现下载逻辑
  console.log('下载通知附件:', notification)
}

async function loadStats() {
  try {
    const data = await dashboardApi.getOverview()
    stats.value = {
      userCount: data.user_count || 0,
      questionCount: data.question_count || 0,
      knowledgeCount: data.knowledge_count || 0,
      avgRating: (data.avg_rating || 0).toFixed(1)
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

async function loadNotifications() {
  try {
    const data = await notificationApi.getList({ skip: 0, limit: 5 })
    notifications.value = data
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

onMounted(() => {
  loadStats()
  loadNotifications()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 头部横幅 */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 60px 40px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 400px;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 100%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
  flex: 1;
  max-width: 600px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: #fff;
}

.gradient-text {
  background: linear-gradient(90deg, #fff, #e0e7ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.normal-text {
  color: #fff;
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 40px 0;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.hero-illustration {
  position: relative;
  width: 400px;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: float 3s ease-in-out infinite;
}

.floating-card .el-icon {
  font-size: 24px;
}

.card-1 {
  top: 20px;
  right: 20px;
  animation-delay: 0s;
}

.card-2 {
  top: 120px;
  right: 100px;
  animation-delay: 1s;
}

.card-3 {
  top: 220px;
  right: 40px;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* 快速入口 */
.quick-access-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.quick-access-item {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.quick-access-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.quick-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 32px;
}

.quick-access-item h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.quick-access-item p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

/* 数据统计 */
.stats-section {
  margin-bottom: 40px;
}

.stat-card {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

/* 通知 */
.notifications-section {
  margin-bottom: 40px;
}

.notification-list {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f5f7fa;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #e0e7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #667eea;
  font-size: 20px;
  margin-right: 16px;
  flex-shrink: 0;
}

.notification-icon.important {
  background: #fee2e2;
  color: #ef4444;
}

.notification-content {
  flex: 1;
}

.notification-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.notification-content p {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.notification-meta .time {
  font-size: 12px;
  color: #909399;
}

.notification-action {
  margin-left: 16px;
  flex-shrink: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
    padding: 40px 20px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-actions {
    justify-content: center;
  }

  .hero-illustration {
    display: none;
  }

  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
