<template>
  <div class="home-container">
    <!-- 顶部大图背景区域 -->
    <div
      class="hero-section"
      :style="{
        backgroundImage: `url('https://images.unsplash.com/photo-1770368437389-86bde15fcb33?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1920')`
      }"
    >
      <!-- 渐变遮罩层 -->
      <div class="hero-overlay"></div>

      <!-- 内容层 -->
      <div class="hero-content-wrapper">
        <!-- 英雄内容 -->
        <div class="hero-main">
          <div class="hero-left">
            <h2 class="hero-title">智能问答知识库系统</h2>
            <p class="hero-subtitle">基于大模型的高效智能答疑平台，助您快速获取答案</p>
            
            <!-- 顶部提问栏 -->
            <div class="hero-quick-ask">
              <div class="ask-input-wrapper">
                <el-input
                  v-model="quickQuestion"
                  placeholder="在这里输入您的问题，快速获取答案..."
                  maxlength="200"
                  show-word-limit
                  class="ask-input"
                />
                <el-button type="primary" @click="handleQuickAsk" class="ask-submit-btn">
                  立即提问
                </el-button>
              </div>
            </div>
          </div>

          <div class="hero-right">
            <div class="floating-btn floating-btn-1">
              <el-icon><ChatDotRound /></el-icon>
              <span>智能问答</span>
            </div>
            <div class="floating-btn floating-btn-2">
              <el-icon><Collection /></el-icon>
              <span>知识检索</span>
            </div>
            <div class="floating-btn floating-btn-3">
              <el-icon><DataLine /></el-icon>
              <span>数据分析</span>
            </div>
          </div>
        </div>
      </div>
    </div>



    <div class="main-content">
      <!-- 快速入口 -->
      <div class="section">
        <div class="section-header">
          <div class="section-line"></div>
          <h3 class="section-title">快速入口</h3>
        </div>
        <div class="quick-access-grid">
          <div class="quick-access-item" @click="goToPath('/chat')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
              <el-icon><ChatDotRound /></el-icon>
            </div>
            <h3>智能问答</h3>
            <p>AI智能在线咨询问题</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/history')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);">
              <el-icon><Clock /></el-icon>
            </div>
            <h3>问答历史</h3>
            <p>查看历史问题记录</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/knowledge')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);">
              <el-icon><Collection /></el-icon>
            </div>
            <h3>知识库</h3>
            <p>浏览知识库知识点</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/dashboard')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #0d9488 0%, #115e59 100%);">
              <el-icon><DataLine /></el-icon>
            </div>
            <h3>数据统计</h3>
            <p>查看系统使用统计</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/favorites')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #d97706 0%, #b45309 100%);">
              <el-icon><StarFilled /></el-icon>
            </div>
            <h3>我的收藏</h3>
            <p>收藏的问题和回答</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/campus')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #475569 0%, #334155 100%);">
              <el-icon><School /></el-icon>
            </div>
            <h3>校园服务</h3>
            <p>公寓、校园通知等</p>
          </div>
          <div class="quick-access-item" @click="goToPath('/notifications')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);">
              <el-icon><Bell /></el-icon>
            </div>
            <h3>通知公告</h3>
            <p>查看学校最新通知</p>
          </div>
          <div class="quick-access-item" v-if="isTeacher" @click="goToPath('/evaluations')">
            <div class="quick-icon" style="background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%);">
              <el-icon><EditPen /></el-icon>
            </div>
            <h3>学生评价查询</h3>
            <p>查询和评价学生成绩</p>
          </div>
        </div>
      </div>

      <div class="content-grid">
        <!-- 左侧主内容区 -->
        <div class="left-content">
          <!-- 系统概况 -->
          <div class="section">
            <div class="section-header">
              <div class="section-line"></div>
              <h3 class="section-title">系统概况</h3>
            </div>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
                  <el-icon><User /></el-icon>
                </div>
                <div class="stat-value">{{ stats.userCount }}</div>
                <div class="stat-label">注册用户</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);">
                  <el-icon><ChatDotRound /></el-icon>
                </div>
                <div class="stat-value">{{ stats.questionCount }}</div>
                <div class="stat-label">问答数量</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-value">{{ stats.knowledgeCount }}</div>
                <div class="stat-label">知识文档数量</div>
              </div>
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #0d9488 0%, #115e59 100%);">
                  <el-icon><Star /></el-icon>
                </div>
                <div class="stat-value">{{ stats.avgRating }}</div>
                <div class="stat-label">平均分</div>
              </div>
            </div>
          </div>

          <!-- 热门问题 -->
          <div class="section">
            <div class="section-header">
              <div class="section-line"></div>
              <h3 class="section-title">热门问题</h3>
            </div>
            <el-empty v-if="popularQuestions.length === 0" description="暂无热门问题" />
            <div v-else class="popular-grid">
              <div
                v-for="question in popularQuestions"
                :key="question.id"
                class="popular-card"
                @click="viewQuestion(question)"
              >
                <div class="popular-icon">
                  <el-icon><ChatDotRound /></el-icon>
                </div>
                <div class="popular-content">
                  <h4>{{ question.question }}</h4>
                  <div class="popular-meta">
                    <span class="views">
                      <View class="meta-icon" />
                      {{ question.ask_count || question.views || 0 }} 次提问
                    </span>
                    <span class="time">{{ formatTime(question.created_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>



          <!-- 功能特色 -->
          <div class="section">
            <div class="section-header">
              <TrendCharts class="section-icon" />
              <h3 class="section-title">功能特色</h3>
            </div>
            <div class="features-grid">
              <div class="feature-item">
                <div class="feature-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
                  <el-icon><ChatLineRound /></el-icon>
                </div>
                <h3>智能问答</h3>
                <p>基于大规模AI，快速准确回答问题</p>
              </div>
              <div class="feature-item">
                <div class="feature-icon" style="background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);">
                  <el-icon><Collection /></el-icon>
                </div>
                <h3>知识库管理</h3>
                <p>上传管理知识文档，构建专属知识库</p>
              </div>
              <div class="feature-item">
                <div class="feature-icon" style="background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%);">
                  <el-icon><School /></el-icon>
                </div>
                <h3>校园服务</h3>
                <p>宿舍查询、成绩查询、图书馆一体化服务</p>
              </div>
              <div class="feature-item">
                <div class="feature-icon" style="background: linear-gradient(135deg, #0d9488 0%, #115e59 100%);">
                  <el-icon><StarFilled /></el-icon>
                </div>
                <h3>收藏管理</h3>
                <p>收藏有价值的问题答案，随时回顾</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧边栏 -->
        <div class="right-sidebar">
          <!-- 通知公告 -->
          <div class="sidebar-card" @click="goToPath('/notifications')">
            <div class="notice-icon" style="background: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);">
              <el-icon><Bell /></el-icon>
            </div>
            <div class="notice-info">
              <h4>通知公告</h4>
              <p>查看学校最新通知</p>
            </div>
          </div>

          <!-- 最新通知 -->
          <div class="section">
            <div class="section-header">
              <Bell class="section-icon" />
              <h3 class="section-title">最新通知</h3>
            </div>
            <el-empty v-if="notifications.length === 0" description="暂无通知" />
            <div v-else class="notification-list">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="notification-item"
                @click="viewNotificationDetail(notification.id)"
              >
                <div class="notification-icon" :class="{ important: notification.is_important }">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="notification-content">
                  <h4>{{ notification.title }}</h4>
                  <p>{{ notification.content }}</p>
                  <div class="notification-tags">
                    <span v-if="notification.is_important" class="tag-new">新通知</span>
                    <span v-if="notification.category" class="tag-category">{{ notification.category }}</span>
                    <span class="tag-time">{{ formatTime(notification.created_at) }}</span>
                  </div>
                </div>
                <div class="notification-arrow">
                  <ChevronRight class="arrow-icon" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
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
  DataAnalysis,
  TrendCharts,
  View,
  Position,
  List,
  MagicStick,
  EditPen,
  Trophy,
  ArrowRight as ChevronRight
} from '@element-plus/icons-vue'
import { statisticsApi } from '@/api/dashboard'
import { notificationApi } from '@/api/notifications'
import { useUserStore } from '@/store/user'
import { computed } from 'vue'

const router = useRouter()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const isTeacher = computed(() => userInfo.value?.role === 'teacher')
const isStudent = computed(() => userInfo.value?.role === 'student')

const stats = ref({
  userCount: 0,
  questionCount: 0,
  knowledgeCount: 0,
  avgRating: 0
})

const notifications = ref<any[]>([])
const popularQuestions = ref<any[]>([])
const quickQuestion = ref('')

function goToChat() {
  router.push('/chat')
}

function goToKnowledge() {
  router.push('/knowledge')
}

function goToPath(path: string) {
  router.push(path)
}

function viewQuestion(question: any) {
  router.push({ path: '/chat', query: { q: question.question } })
}

function handleQuickAsk() {
  if (!quickQuestion.value.trim()) {
    ElMessage.warning('请输入问题内容')
    return
  }
  
  // 检查用户是否登录
  let token = sessionStorage.getItem('token')
  if (!token) token = localStorage.getItem('token')
  
  if (!token) {
    ElMessage.warning('您当前未登录，问题将不会被保存到问答历史中。建议先登录以获得完整功能。')
  }
  
  router.push({ path: '/chat', query: { q: quickQuestion.value.trim() } })
}

function viewNotificationDetail(id: number) {
  router.push(`/notification/${id}`)
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
  console.log('下载通知附件:', notification)
}

async function loadStats() {
  try {
    const data = await statisticsApi.getOverview()
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
    const data = await notificationApi.getList()
    notifications.value = Array.isArray(data) ? data.slice(0, 5) : []
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

async function loadPopularQuestions() {
  try {
    const data = await statisticsApi.getPopularQuestions(8)
    console.log('加载热门问题成功，数量:', data?.length || 0)
    
    // 确保数据是数组
    if (Array.isArray(data) && data.length > 0) {
      // 转换数据，确保有必要的字段
      popularQuestions.value = data.map(item => ({
        ...item,
        // 确保ask_count有值，如果没有则使用views或默认值1
        ask_count: item.ask_count || item.views || 1
      }))
      
      // 调试：查看第一个问题的字段
      console.log('热门问题示例:', {
        id: popularQuestions.value[0].id,
        question: popularQuestions.value[0].question,
        ask_count: popularQuestions.value[0].ask_count,
        views: popularQuestions.value[0].views
      })
    } else {
      console.log('热门问题数据为空，使用演示数据')
      popularQuestions.value = [
        {
          id: 1,
          question: '如何申请奖学金？',
          ask_count: 1256,
          created_at: new Date(Date.now() - 86400000 * 2).toISOString()
        },
        {
          id: 2,
          question: '图书馆开放时间是什么时候？',
          ask_count: 987,
          created_at: new Date(Date.now() - 86400000 * 3).toISOString()
        },
        {
          id: 3,
          question: '如何查询期末考试成绩？',
          ask_count: 854,
          created_at: new Date(Date.now() - 86400000 * 5).toISOString()
        },
        {
          id: 4,
          question: '选课系统什么时候开放？',
          ask_count: 723,
          created_at: new Date(Date.now() - 86400000 * 7).toISOString()
        }
      ]
    }
  } catch (error) {
    console.error('加载热门问题失败:', error)
    // 设置一些演示数据，使用ask_count字段
    popularQuestions.value = [
      {
        id: 1,
        question: '如何申请奖学金？',
        ask_count: 1256,
        created_at: new Date(Date.now() - 86400000 * 2).toISOString()
      },
      {
        id: 2,
        question: '图书馆开放时间是什么时候？',
        ask_count: 987,
        created_at: new Date(Date.now() - 86400000 * 3).toISOString()
      },
      {
        id: 3,
        question: '如何查询期末考试成绩？',
        ask_count: 854,
        created_at: new Date(Date.now() - 86400000 * 5).toISOString()
      },
      {
        id: 4,
        question: '选课系统什么时候开放？',
        ask_count: 723,
        created_at: new Date(Date.now() - 86400000 * 7).toISOString()
      }
    ]
  }
}

onMounted(() => {
  loadStats()
  loadNotifications()
  loadPopularQuestions()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(180deg, rgba(239, 246, 255, 0.5) 0%, rgba(248, 250, 252, 1) 50%, rgba(238, 242, 255, 0.3) 100%);
}

/* 顶部大图背景区域 */
.hero-section {
  position: relative;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 420px;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(30, 58, 138, 0.9) 0%, rgba(67, 56, 202, 0.85) 50%, rgba(180, 83, 9, 0.8) 100%);
}

.hero-content-wrapper {
  position: relative;
  z-index: 10;
}

/* 顶部导航 */
.hero-header {
  padding: 16px 24px;
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.system-title {
  font-size: 20px;
  color: #fff;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  backdrop-filter: blur(8px);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
}

.user-info span {
  color: #fff;
}

/* 英雄内容 */
.hero-main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 64px 24px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero-left {
  flex: 1;
}

/* 顶部提问栏 */
.hero-quick-ask {
  margin-top: 32px;
  width: 100%;
}

.ask-input-wrapper {
  display: flex;
  max-width: 1280px;
  margin: 0 auto;
}

.ask-input {
  flex: 1;
  margin-right: 0;
}

.ask-input :deep(.el-input__wrapper) {
  background: #fff;
  border-radius: 8px 0 0 8px;
  border: 1px solid #e2e8f0;
  border-right: none;
  height: 48px;
  box-shadow: none;
}

.ask-input :deep(.el-input__wrapper:hover) {
  border-color: #cbd5e1;
}

.ask-input :deep(.el-input__wrapper.is-focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.ask-input :deep(.el-input__inner) {
  font-size: 15px;
  padding: 0 16px;
  color: #1e293b;
}

.ask-input :deep(.el-input__inner::placeholder) {
  color: #94a3b8;
}

.ask-submit-btn {
  height: 48px;
  padding: 0 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%) !important;
  border: none !important;
  border-radius: 0 8px 8px 0 !important;
  color: #fff !important;
  font-weight: 500;
  font-size: 15px;
  transition: all 0.3s;
}

.ask-submit-btn:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.ask-input-wrapper :deep(.el-input__suffix) {
  padding-right: 8px;
  color: #94a3b8;
  font-size: 12px;
}

.hero-title {
  font-size: 48px;
  color: #fff;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 32px 0;
  max-width: 560px;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 16px;
}

.btn-primary {
  padding: 12px 24px;
  background: #fff !important;
  color: #1d4ed8 !important;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background: #eff6ff !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.1) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  border-radius: 8px;
  color: #fff !important;
  display: flex;
  align-items: center;
  gap: 8px;
  backdrop-filter: blur(8px);
  transition: all 0.3s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2) !important;
}

.hero-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: flex-end;
}

/* 浮动装饰按钮 */
.floating-btn {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
  padding: 16px 48px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
  color: #fff;
  backdrop-filter: blur(8px);
  cursor: default;
  user-select: none;
  transition: transform 0.3s ease;
}

.floating-btn .el-icon {
  font-size: 32px;
}

.floating-btn span {
  font-size: 20px;
  font-weight: 500;
}

/* 左右错落 - 不同按钮不同位置 */
.floating-btn-1 {
  margin-right: 0;
  animation: float1 3s ease-in-out infinite;
}

.floating-btn-2 {
  margin-right: -30px;
  animation: float2 3.5s ease-in-out infinite;
  animation-delay: 0.5s;
}

.floating-btn-3 {
  margin-right: -15px;
  animation: float3 4s ease-in-out infinite;
  animation-delay: 1s;
}

/* 上下浮动动画 */
@keyframes float1 {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

@keyframes float2 {
  0%, 100% { transform: translateY(-10px); }
  50% { transform: translateY(0px); }
}

@keyframes float3 {
  0%, 100% { transform: translateY(-8px); }
  50% { transform: translateY(8px); }
}



/* 主内容区 */
.main-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 24px;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.section-line {
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, #3b82f6 0%, #4f46e5 100%);
  border-radius: 9999px;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

.section-title {
  font-size: 20px;
  color: #1e293b;
  margin: 0;
}

/* 快速入口 */
.quick-access-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.quick-access-item {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.quick-access-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.quick-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
}

.quick-access-item h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.quick-access-item p {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

/* 内容网格 */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.left-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  border: 1px solid #f1f5f9;
  transition: all 0.3s;
}

.stat-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  margin: 0 auto 12px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
}

/* 热门问题 */
.popular-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.popular-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.popular-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.popular-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  flex-shrink: 0;
}

.popular-content {
  flex: 1;
  min-width: 0;
}

.popular-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.popular-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: #94a3b8;
}

.popular-meta .views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon {
  width: 12px;
  height: 12px;
}

.popular-meta .time {
  margin-left: auto;
}

/* 快速提问 */
.ask-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #f1f5f9;
}

.ask-card :deep(.el-textarea__inner) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  line-height: 1.6;
}

.ask-card :deep(.el-textarea__inner:focus) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.ask-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.word-count {
  font-size: 12px;
  color: #94a3b8;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-text {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #64748b !important;
}

.btn-text:hover {
  background: #f8fafc !important;
}

.btn-icon-small {
  width: 14px;
  height: 14px;
}

.btn-submit {
  padding: 8px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #4f46e5 100%) !important;
  border: none !important;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s;
}

.btn-submit:hover {
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* 功能特色 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.feature-item {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #f1f5f9;
  transition: all 0.3s;
}

.feature-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.feature-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
  margin-bottom: 16px;
}

.feature-item h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.feature-item p {
  font-size: 14px;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

/* 右侧边栏 */
.sidebar-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  border: 1px solid #f1f5f9;
  transition: all 0.3s;
}

.sidebar-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.notice-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
}

.notice-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.notice-info p {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* 通知列表 */
.notification-list {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background 0.3s;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item:hover {
  background: #f8fafc;
}

.notification-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #fff1f2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e11d48;
  font-size: 18px;
  margin-right: 12px;
  flex-shrink: 0;
}

.notification-icon.important {
  background: #fee2e2;
  color: #dc2626;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.notification-content p {
  font-size: 12px;
  color: #64748b;
  margin: 0 0 12px 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.notification-tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tag-new {
  padding: 2px 8px;
  background: #fff1f2;
  color: #e11d48;
  border-radius: 4px;
  font-size: 11px;
}

.tag-category {
  padding: 2px 8px;
  background: #eff6ff;
  color: #2563eb;
  border-radius: 4px;
  font-size: 11px;
}

.tag-time {
  padding: 2px 8px;
  background: #f1f5f9;
  color: #64748b;
  border-radius: 4px;
  font-size: 11px;
}

.notification-arrow {
  margin-left: 8px;
  flex-shrink: 0;
}

.arrow-icon {
  width: 16px;
  height: 16px;
  color: #3b82f6;
}

/* 响应式 */
@media (max-width: 1200px) {
  .quick-access-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-main {
    flex-direction: column;
    text-align: center;
    padding: 40px 20px;
  }

  .hero-left {
    margin-bottom: 32px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    max-width: 100%;
  }

  .hero-actions {
    justify-content: center;
    flex-wrap: wrap;
  }

  .hero-right {
    flex-direction: row;
    justify-content: center;
  }

  .quick-access-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .popular-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .header-inner {
    flex-direction: column;
    gap: 12px;
  }

  /* 移动端顶部提问栏响应式样式 */
  .hero-quick-ask {
    margin-top: 24px;
  }

  .ask-input-wrapper {
    flex-direction: column;
    gap: 12px;
  }

  .ask-input :deep(.el-input__wrapper) {
    border-radius: 8px;
    border-right: 1px solid #e2e8f0;
    width: 100%;
  }

  .ask-submit-btn {
    border-radius: 8px !important;
    width: 100%;
    height: 44px;
  }

  .ask-input-wrapper :deep(.el-input__suffix) {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 11px;
  }
}
</style>
