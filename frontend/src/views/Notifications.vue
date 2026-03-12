<template>
  <div class="notifications-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">
        <el-icon><Bell /></el-icon>
        通知公告
      </h1>
      <p class="page-subtitle">查看最新的学校通知和公告信息</p>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="8" :md="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索通知标题或内容..."
            clearable
            :prefix-icon="Search"
            @input="handleSearch"
          />
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select
            v-model="filterCategory"
            placeholder="选择分类"
            clearable
            style="width: 100%"
            @change="handleFilter"
          >
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="8" :md="6">
          <el-select
            v-model="filterImportance"
            placeholder="重要性筛选"
            clearable
            style="width: 100%"
            @change="handleFilter"
          >
            <el-option label="重要通知" value="1" />
            <el-option label="普通通知" value="0" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <!-- 通知列表 -->
    <div class="notifications-section">
      <div class="section-header">
        <span class="total-count">
          共找到 {{ filteredNotifications.length }} 条通知
        </span>
        <div class="sort-options">
          <el-radio-group v-model="sortOrder" @change="handleSort">
            <el-radio-button label="desc">最新发布</el-radio-button>
            <el-radio-button label="asc">最早发布</el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <el-empty
        v-if="filteredNotifications.length === 0"
        description="暂无通知"
        :image-size="200"
      />
      
      <div v-else class="notification-list">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          class="notification-item"
          :class="{ important: notification.is_important }"
          @click="viewNotificationDetail(notification.id)"
        >
          <div class="notification-badge">
            <el-tag v-if="notification.is_important" type="danger" size="small">
              <el-icon><StarFilled /></el-icon>
              重要
            </el-tag>
            <el-tag v-if="notification.category" type="primary" size="small">
              {{ notification.category }}
            </el-tag>
          </div>
          
          <div class="notification-content">
            <h3 class="notification-title">{{ notification.title }}</h3>
            <p class="notification-summary">{{ notification.content }}</p>
            
            <div class="notification-meta">
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ notification.publisher || '武汉科技大学' }}</span>
              </div>
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>{{ formatTime(notification.created_at) }}</span>
              </div>
              <div class="meta-item">
                <el-icon><View /></el-icon>
                <span>{{ notification.views || 0 }} 次浏览</span>
              </div>
            </div>
          </div>
          
          <div class="notification-action">
            <el-button
              type="primary"
              link
              :icon="ArrowRight"
              @click.stop="viewNotificationDetail(notification.id)"
            >
              查看详情
            </el-button>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredNotifications.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <el-skeleton :rows="5" animated />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Bell,
  Search,
  ArrowRight,
  User,
  Clock,
  View,
  StarFilled
} from '@element-plus/icons-vue'
import { notificationApi, type Notification } from '@/api/notifications'

const router = useRouter()

const notifications = ref<Notification[]>([])
const loading = ref(false)

// 筛选条件
const searchKeyword = ref('')
const filterCategory = ref('')
const filterImportance = ref('')
const sortOrder = ref('desc')
const categories = ref<string[]>([])

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

// 格式化时间
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

// 查看通知详情
function viewNotificationDetail(id: number) {
  router.push(`/notification/${id}`)
}

// 处理搜索
function handleSearch() {
  currentPage.value = 1
}

// 处理筛选
function handleFilter() {
  currentPage.value = 1
}

// 处理排序
function handleSort() {
  // 排序逻辑在计算属性中处理
}

// 处理分页大小变化
function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1
}

// 处理当前页变化
function handleCurrentChange(page: number) {
  currentPage.value = page
}

// 过滤和排序后的通知列表
const filteredNotifications = computed(() => {
  let filtered = notifications.value

  // 关键词搜索
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(notification =>
      notification.title.toLowerCase().includes(keyword) ||
      (notification.content && notification.content.toLowerCase().includes(keyword))
    )
  }

  // 分类筛选
  if (filterCategory.value) {
    filtered = filtered.filter(notification => 
      notification.category === filterCategory.value
    )
  }

  // 重要性筛选
  if (filterImportance.value !== '') {
    filtered = filtered.filter(notification => 
      notification.is_important.toString() === filterImportance.value
    )
  }

  // 排序
  filtered = [...filtered].sort((a, b) => {
    const dateA = new Date(a.created_at).getTime()
    const dateB = new Date(b.created_at).getTime()
    return sortOrder.value === 'desc' ? dateB - dateA : dateA - dateB
  })

  return filtered
})

// 分页后的数据
const paginatedNotifications = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredNotifications.value.slice(start, end)
})

// 加载通知列表
async function loadNotifications() {
  loading.value = true
  try {
    const data = await notificationApi.getList()
    notifications.value = data || []
    
    // 提取分类列表
    categories.value = [...new Set(data.map(item => item.category).filter(Boolean))] as string[]
  } catch (error) {
    console.error('加载通知列表失败:', error)
    // 使用演示数据
    notifications.value = [
      {
        id: 1,
        title: '关于2025-2026学年第一学期选课工作的通知',
        content: '2025-2026学年第一学期选课工作即将开始，请各学院及时通知学生做好选课准备。',
        category: '教务通知',
        is_important: 1,
        publisher: '武汉科技大学教务处',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        views: 0
      },
      {
        id: 2,
        title: '关于2025年秋季学期开学及疫情防控要求的通知',
        content: '2025年秋季学期将于9月2日正式开学，请全体师生按照疫情防控要求做好返校准备。',
        category: '疫情防控',
        is_important: 1,
        publisher: '武汉科技大学办公室',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        updated_at: new Date(Date.now() - 86400000).toISOString(),
        views: 0
      }
    ]
    categories.value = ['教务通知', '疫情防控']
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadNotifications()
})
</script>

<style scoped>
.notifications-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  color: #303133;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-subtitle {
  font-size: 18px;
  color: #606266;
  margin: 0;
}

/* 筛选条件 */
.filter-section {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* 通知列表 */
.notifications-section {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.total-count {
  font-size: 16px;
  color: #606266;
  font-weight: 500;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 通知项 */
.notification-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  padding: 24px;
  background: #f5f7fa;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
}

.notification-item:hover {
  background: #e0e7ff;
  border-color: #409eff;
  transform: translateY(-2px);
}

.notification-item.important {
  background: #fee2e2;
  border-color: #fecaca;
}

.notification-item.important:hover {
  background: #fecaca;
  border-color: #fca5a5;
}

.notification-badge {
  display: flex;
  gap: 8px;
  margin-right: 16px;
  flex-shrink: 0;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.notification-summary {
  font-size: 14px;
  color: #606266;
  margin: 0 0 16px 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.notification-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
}

.meta-item .el-icon {
  font-size: 14px;
}

.notification-action {
  margin-left: 16px;
  flex-shrink: 0;
}

/* 分页 */
.pagination-section {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

/* 加载状态 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* 响应式 */
@media (max-width: 768px) {
  .notifications-container {
    padding: 16px;
  }

  .page-title {
    font-size: 28px;
  }

  .notifications-section {
    padding: 24px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .notification-item {
    flex-direction: column;
    padding: 20px;
  }

  .notification-badge {
    margin-right: 0;
    margin-bottom: 12px;
  }

  .notification-meta {
    gap: 12px;
  }

  .notification-action {
    margin-left: 0;
    margin-top: 16px;
    width: 100%;
    text-align: center;
  }
}
</style>