<template>
  <div class="notification-detail-container">
    <!-- 返回按钮 -->
    <div class="back-section">
      <el-button
        type="primary"
        link
        :icon="ArrowLeft"
        @click="goBack"
        class="back-btn"
      >
        返回通知列表
      </el-button>
    </div>

    <!-- 通知详情内容 -->
    <div class="notification-content">
      <!-- 标题和元信息 -->
      <div class="notification-header">
        <div class="header-top">
          <div class="notification-badge">
            <el-tag v-if="notification.is_important" type="danger" size="large">
              <el-icon><StarFilled /></el-icon>
              重要通知
            </el-tag>
            <el-tag v-else type="info" size="large">
              <el-icon><Document /></el-icon>
              普通通知
            </el-tag>
            <el-tag v-if="notification.category" type="primary" size="large">
              {{ notification.category }}
            </el-tag>
          </div>
          
          <div class="notification-actions">
            <el-button
              type="primary"
              :icon="Share"
              @click="shareNotification"
              size="small"
            >
              分享
            </el-button>
            <el-button
              :icon="Printer"
              @click="printNotification"
              size="small"
            >
              打印
            </el-button>
          </div>
        </div>
        
        <h1 class="notification-title">{{ notification.title }}</h1>
        
        <div class="notification-meta">
          <div class="meta-item">
            <el-icon><User /></el-icon>
            <span>发布单位：{{ notification.publisher || '武汉科技大学' }}</span>
          </div>
          <div class="meta-item">
            <el-icon><Clock /></el-icon>
            <span>发布时间：{{ formatTime(notification.created_at) }}</span>
          </div>
          <div class="meta-item">
            <el-icon><View /></el-icon>
            <span>浏览次数：{{ notification.views || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- 详细内容 -->
      <div class="detail-section">
        <div
          v-if="notification.detail_content"
          class="detail-content"
          v-html="notification.detail_content"
        ></div>
        
        <div v-else class="no-detail">
          <el-empty description="暂无详细内容">
            <p>{{ notification.content }}</p>
          </el-empty>
        </div>
      </div>

      <!-- 附件下载 -->
      <div v-if="notification.file_path" class="attachment-section">
        <h3 class="section-title">
          <el-icon><Paperclip /></el-icon>
          附件下载
        </h3>
        <el-button
          type="primary"
          :icon="Download"
          @click="downloadAttachment"
          size="large"
        >
          下载附件
        </el-button>
      </div>

      <!-- 相关通知 -->
      <div class="related-section">
        <h3 class="section-title">
          <el-icon><Link /></el-icon>
          相关通知
        </h3>
        <div v-if="relatedNotifications.length > 0" class="related-list">
          <div
            v-for="related in relatedNotifications"
            :key="related.id"
            class="related-item"
            @click="viewRelatedNotification(related.id)"
          >
            <div class="related-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="related-content">
              <h4>{{ related.title }}</h4>
              <p>{{ related.content }}</p>
              <span class="related-meta">
                <el-tag v-if="related.is_important" type="danger" size="small">重要</el-tag>
                <el-tag v-if="related.category" size="small">{{ related.category }}</el-tag>
                <span class="time">{{ formatTime(related.created_at) }}</span>
              </span>
            </div>
          </div>
        </div>
        <el-empty v-else description="暂无相关通知" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Share,
  Printer,
  User,
  Clock,
  View,
  Download,
  Paperclip,
  Link,
  Document,
  StarFilled
} from '@element-plus/icons-vue'
import { notificationApi, type Notification } from '@/api/notifications'

const route = useRoute()
const router = useRouter()

const notification = ref<Notification>({
  id: 0,
  title: '',
  content: '',
  is_important: 0,
  created_at: '',
  updated_at: ''
})

const relatedNotifications = ref<Notification[]>([])
const loading = ref(false)

// 获取通知ID
const notificationId = computed(() => {
  return parseInt(route.params.id as string)
})

// 格式化时间
function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 返回上一页
function goBack() {
  router.go(-1)
}

// 分享通知
function shareNotification() {
  if (navigator.share) {
    navigator.share({
      title: notification.value.title,
      text: notification.value.content || notification.value.title,
      url: window.location.href
    }).then(() => {
      ElMessage.success('分享成功')
    }).catch((error) => {
      console.log('分享取消或失败:', error)
    })
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.href).then(() => {
      ElMessage.success('链接已复制到剪贴板')
    }).catch(() => {
      ElMessage.warning('请手动复制链接')
    })
  }
}

// 打印通知
function printNotification() {
  window.print()
}

// 下载附件
async function downloadAttachment() {
  if (!notification.value.file_path) {
    ElMessage.warning('该通知没有附件')
    return
  }

  try {
    const response = await notificationApi.download(notification.value.id)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', notification.value.file_path.split('/').pop() || '附件')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('下载成功')
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败，请稍后重试')
  }
}

// 查看相关通知
function viewRelatedNotification(id: number) {
  router.push(`/notification/${id}`)
}

// 加载通知详情
async function loadNotificationDetail() {
  if (!notificationId.value) {
    ElMessage.error('通知ID无效')
    router.push('/home')
    return
  }

  loading.value = true
  try {
    const data = await notificationApi.getDetail(notificationId.value)
    notification.value = data
    
    // 加载相关通知（同分类的其他通知）
    await loadRelatedNotifications()
  } catch (error) {
    console.error('加载通知详情失败:', error)
    ElMessage.error('加载通知详情失败')
    router.push('/home')
  } finally {
    loading.value = false
  }
}

// 加载相关通知
async function loadRelatedNotifications() {
  try {
    const params = {
      category: notification.value.category,
      limit: 5
    }
    const data = await notificationApi.getList(params)
    // 过滤掉当前通知
    relatedNotifications.value = data.filter(item => item.id !== notification.value.id)
  } catch (error) {
    console.error('加载相关通知失败:', error)
  }
}

onMounted(() => {
  loadNotificationDetail()
})
</script>

<style scoped>
.notification-detail-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 返回按钮 */
.back-section {
  margin-bottom: 20px;
}

.back-btn {
  font-size: 16px;
  font-weight: 500;
}

/* 通知内容 */
.notification-content {
  background: #fff;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* 通知头部 */
.notification-header {
  margin-bottom: 40px;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 30px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.notification-badge {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.notification-actions {
  display: flex;
  gap: 12px;
}

.notification-title {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 24px 0;
  line-height: 1.4;
}

.notification-meta {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.meta-item .el-icon {
  font-size: 16px;
}

/* 详细内容 */
.detail-section {
  margin-bottom: 40px;
}

.detail-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.detail-content :deep(h1),
.detail-content :deep(h2),
.detail-content :deep(h3) {
  color: #303133;
  margin: 24px 0 16px 0;
}

.detail-content :deep(h1) {
  font-size: 24px;
  font-weight: 600;
}

.detail-content :deep(h2) {
  font-size: 20px;
  font-weight: 600;
}

.detail-content :deep(h3) {
  font-size: 18px;
  font-weight: 600;
}

.detail-content :deep(p) {
  margin: 0 0 16px 0;
}

.detail-content :deep(ul),
.detail-content :deep(ol) {
  margin: 16px 0;
  padding-left: 24px;
}

.detail-content :deep(li) {
  margin: 8px 0;
}

.detail-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.detail-content :deep(th),
.detail-content :deep(td) {
  border: 1px solid #ebeef5;
  padding: 12px;
  text-align: left;
}

.detail-content :deep(th) {
  background: #f5f7fa;
  font-weight: 600;
}

.detail-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.detail-content :deep(a:hover) {
  text-decoration: underline;
}

.no-detail {
  text-align: center;
  padding: 40px 0;
}

/* 附件下载 */
.attachment-section {
  margin-bottom: 40px;
  padding: 24px;
  background: #f5f7fa;
  border-radius: 12px;
}

/* 相关通知 */
.related-section {
  border-top: 1px solid #ebeef5;
  padding-top: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.related-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.related-item:hover {
  background: #e0e7ff;
  border-color: #409eff;
  transform: translateX(5px);
}

.related-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #409eff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  margin-right: 16px;
  flex-shrink: 0;
}

.related-content {
  flex: 1;
}

.related-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

        .related-content p {
          font-size: 14px;
          color: #606266;
          margin: 0 0 12px 0;
          line-height: 1.5;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          line-clamp: 2;
        }

.related-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.related-meta .time {
  font-size: 12px;
  color: #909399;
}

/* 响应式 */
@media (max-width: 768px) {
  .notification-detail-container {
    padding: 16px;
  }

  .notification-content {
    padding: 24px;
  }

  .notification-title {
    font-size: 24px;
  }

  .header-top {
    flex-direction: column;
    align-items: flex-start;
  }

  .notification-meta {
    gap: 16px;
  }

  .meta-item {
    font-size: 13px;
  }
}

@media print {
  .back-section,
  .notification-actions,
  .attachment-section,
  .related-section {
    display: none !important;
  }

  .notification-content {
    padding: 0;
    box-shadow: none;
  }
}
</style>