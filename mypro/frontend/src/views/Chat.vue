<template>
  <div class="chat-container">
    <div class="chat-header">
      <h3><el-icon><ChatDotRound /></el-icon>智能问答</h3>
    </div>
    
    <div class="chat-content">
      <div class="chat-main">
        <div class="chat-messages" ref="messagesRef">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="['message', message.role]"
          >
            <div class="message-avatar">
              <el-icon v-if="message.role === 'user'"><User /></el-icon>
              <el-icon v-else><Service /></el-icon>
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(message.content)"></div>
              <div class="message-footer">
                <span class="message-time">{{ formatTime(message.timestamp) }}</span>
                <div v-if="message.role === 'assistant'" class="message-actions">
                  <el-button
                    link
                    :type="message.isFavorited ? 'warning' : 'primary'"
                    :icon="message.isFavorited ? BookmarkFilled : Bookmark"
                    :loading="message.favoriteLoading"
                    @click="handleFavorite(index)"
                    :title="message.isFavorited ? '已收藏' : '收藏问题'"
                  />
                  <el-button
                    link
                    type="primary"
                    :icon="message.rating >= 1 ? StarFilled : Star"
                    @click="handleRating(index, 1)"
                  />
                  <el-button
                    link
                    type="primary"
                    :icon="message.rating >= 2 ? StarFilled : Star"
                    @click="handleRating(index, 2)"
                  />
                  <el-button
                    link
                    type="primary"
                    :icon="message.rating >= 3 ? StarFilled : Star"
                    @click="handleRating(index, 3)"
                  />
                  <el-button
                    link
                    type="primary"
                    :icon="message.rating >= 4 ? StarFilled : Star"
                    @click="handleRating(index, 4)"
                  />
                  <el-button
                    link
                    type="primary"
                    :icon="message.rating >= 5 ? StarFilled : Star"
                    @click="handleRating(index, 5)"
                  />
                </div>
              </div>
            </div>
          </div>
          <div v-if="loading" class="message assistant">
            <div class="message-avatar">
              <el-icon><Service /></el-icon>
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            @keydown.enter.prevent="handleSend"
            :disabled="loading"
          />
          <el-button
            type="primary"
            :icon="Position"
            :loading="loading"
            @click="handleSend"
            class="send-button"
          >
            发送
          </el-button>
        </div>
      </div>

      <div class="chat-sidebar">
        <div class="sidebar-section">
          <h4><el-icon><ChatDotRound /></el-icon>热门问题</h4>
          <ul class="hot-questions">
            <li v-for="(question, index) in hotQuestions" :key="index" @click="handleQuickQuestion(question)">
              <el-icon><ChatLineRound /></el-icon>
              {{ question }}
            </li>
          </ul>
        </div>

        <div class="sidebar-section">
          <h4><el-icon><ChatLineRound /></el-icon>相关问题</h4>
          <ul class="related-questions">
            <li v-for="(question, index) in relatedQuestions" :key="index" @click="handleQuickQuestion(question)">
              {{ question }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Service, Position, ChatDotRound, ChatLineRound, StarFilled, Star, StarFilled as BookmarkFilled, Star as Bookmark } from '@element-plus/icons-vue'
import { chatApi, Question } from '@/api/chat'
import { useUserStore } from '@/store/user'
import { favoritesApi } from '@/api/favorites'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  rating?: number
  questionId?: number
  isFavorited?: boolean
  favoriteLoading?: boolean
}

const userStore = useUserStore()
const route = useRoute()

const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '您好！我是高校知识库智能答疑助手。请问有什么可以帮助您的？',
    timestamp: Date.now()
  }
])

const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref<HTMLElement>()

const hotQuestions = ref([
  '如何申请奖学金？',
  '图书馆开放时间是什么？',
  '课程重修怎么办理？',
  '如何办理校园卡？'
])

const relatedQuestions = ref([
  '课程表查询方式',
  '成绩查询流程',
  '选修课选课规则',
  '学分要求说明'
])

async function handleSend() {
  if (!inputMessage.value.trim()) return

  const userMessage = inputMessage.value
  // 先添加用户消息
  const userMessageObj: ChatMessage = {
    role: 'user',
    content: userMessage,
    timestamp: Date.now()
  }
  messages.value.push(userMessageObj)
  inputMessage.value = ''
  loading.value = true

  await scrollToBottom()

  try {
    const response: Question = await chatApi.sendMessage({
      question: userMessage,
      category: ''
    })

    // 如果API调用成功且有返回ID，更新用户消息也包含questionId
    if (response.id) {
      userMessageObj.questionId = response.id
    }

    const assistantMessage: ChatMessage = {
      role: 'assistant',
      content: response.answer || '抱歉，暂时无法回答您的问题。',
      timestamp: Date.now(),
      questionId: response.id,
      isFavorited: false,
      favoriteLoading: false
    }
    messages.value.push(assistantMessage)
  } catch (error: any) {
    console.error('回答错误:', error)
    // 如果API调用失败，仍然添加一个AI响应消息
    const errorMessage: ChatMessage = {
      role: 'assistant',
      content: '抱歉，回答问题时出现错误。请检查网络连接或稍后重试。',
      timestamp: Date.now()
    }
    messages.value.push(errorMessage)
    
    // 根据错误类型显示不同的提示
    if (error.response?.status === 401) {
      ElMessage.warning('请先登录后再提问，问题将不会被保存到历史记录')
    } else {
      ElMessage.error(error.response?.data?.detail || '抱歉，回答问题时出现错误，请稍后重试')
    }
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

function handleQuickQuestion(question: string) {
  inputMessage.value = question
  handleSend()
}

async function handleRating(index: number, rating: number) {
  const message = messages.value[index]
  if (message.role === 'assistant' && message.rating !== rating && message.questionId) {
    message.rating = rating
    try {
      await chatApi.submitFeedback({
        question_id: message.questionId,
        rating
      })
      ElMessage.success('感谢您的评价！')
    } catch (error) {
      ElMessage.error('评价提交失败')
    }
  }
}

async function handleFavorite(index: number) {
  // 检查用户是否登录
  let token = sessionStorage.getItem('token')
  if (!token) token = localStorage.getItem('token')
  if (!token) {
    ElMessage.warning('请先登录后再使用收藏功能')
    return
  }

  const message = messages.value[index]
  if (message.role === 'assistant' && message.questionId) {
    message.favoriteLoading = true
    try {
      if (message.isFavorited) {
        // 取消收藏
        const favorites = await favoritesApi.getAll()
        const favorite = favorites.find(f => f.question_id === message.questionId)
        if (favorite) {
          await favoritesApi.remove(favorite.id)
          message.isFavorited = false
          ElMessage.success('已取消收藏')
        }
      } else {
        // 添加收藏
        await favoritesApi.add({ question_id: message.questionId })
        message.isFavorited = true
        ElMessage.success('收藏成功！您可以在"我的收藏"页面查看')
      }
    } catch (error: any) {
      console.error('收藏操作失败:', error)
      ElMessage.error(error.response?.data?.detail || '操作失败')
    } finally {
      message.favoriteLoading = false
    }
  }
}

async function scrollToBottom() {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

function formatTime(timestamp: number): string {
  const date = new Date(timestamp)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}

function formatMessage(content: string): string {
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
}

// 处理从查询参数中自动发送的问题
async function processQueryQuestion() {
  const queryQuestion = route.query.q as string
  if (queryQuestion && queryQuestion.trim()) {
    // 检查是否已经处理过这个问题（避免重复发送）
    const hasProcessed = messages.value.some(msg => 
      msg.role === 'user' && msg.content === queryQuestion.trim()
    )
    
    if (!hasProcessed) {
      // 设置输入框内容
      inputMessage.value = queryQuestion.trim()
      
      // 等待一下让UI更新
      await nextTick()
      
      // 自动发送消息
      await handleSend()
    }
  }
}

// 监听路由查询参数变化
watch(() => route.query.q, (newQuestion) => {
  if (newQuestion) {
    processQueryQuestion()
  }
})

onMounted(() => {
  scrollToBottom()
  processQueryQuestion()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chat-header {
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 8px 8px 0 0;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.chat-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #ebeef5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
}

.message {
  display: flex;
  margin-bottom: 20px;
  gap: 12px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 20px;
}

.message.user .message-avatar {
  background: #409eff;
  color: #fff;
}

.message.assistant .message-avatar {
  background: #67c23a;
  color: #fff;
}

.message-content {
  max-width: 70%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.6;
  word-wrap: break-word;
}

.message.user .message-text {
  background: #409eff;
  color: #fff;
}

.message.assistant .message-text {
  background: #fff;
  color: #303133;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.message-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  font-size: 12px;
  color: #909399;
}

.message-actions {
  display: flex;
  gap: 4px;
}

.typing-indicator {
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #909399;
  border-radius: 50%;
  margin: 0 2px;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

.chat-input {
  padding: 16px;
  background: #fff;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chat-input .el-textarea {
  flex: 1;
}

.send-button {
  height: 76px;
  padding: 0 24px;
}

.chat-sidebar {
  width: 280px;
  padding: 20px;
  background: #fafafa;
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 24px;
}

.sidebar-section h4 {
  font-size: 14px;
  color: #303133;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.hot-questions li,
.related-questions li {
  padding: 10px 12px;
  margin-bottom: 8px;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
}

.hot-questions li:hover,
.related-questions li:hover {
  background: #409eff;
  color: #fff;
  transform: translateX(4px);
}

.related-questions li {
  font-size: 13px;
  padding: 8px 10px;
}
</style>
