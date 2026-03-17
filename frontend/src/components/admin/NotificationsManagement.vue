<template>
  <div class="notifications-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2 class="page-title">
        <el-icon><Bell /></el-icon>
        通知管理
      </h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">
        发布通知
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon published">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.published }}</div>
          <div class="stat-label">已发布</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon scheduled">
          <el-icon><Timer /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.scheduled }}</div>
          <div class="stat-label">待定时</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon important">
          <el-icon><StarFilled /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.important }}</div>
          <div class="stat-label">重要通知</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon total">
          <el-icon><Files /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">全部通知</div>
        </div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索通知标题..."
            clearable
            :prefix-icon="Search"
            @input="handleSearch"
          />
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-select
            v-model="filterStatus"
            placeholder="选择状态"
            clearable
            style="width: 100%"
            @change="handleFilter"
          >
            <el-option label="已发布" value="published" />
            <el-option label="待定时" value="scheduled" />
            <el-option label="草稿" value="draft" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="6">
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
        <el-col :xs="24" :sm="6">
          <el-select
            v-model="filterImportance"
            placeholder="重要性"
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
      <el-table
        :data="filteredNotifications"
        v-loading="loading"
        stripe
        @sort-change="handleSort"
      >
        <el-table-column type="index" label="#" width="60" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="分类" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.category" type="primary" size="small">
              {{ row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'published'" type="success" size="small">
              已发布
            </el-tag>
            <el-tag v-else-if="row.status === 'scheduled'" type="warning" size="small">
              待定时
            </el-tag>
            <el-tag v-else type="info" size="small">
              草稿
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="定时发布" width="160">
          <template #default="{ row }">
            <span v-if="row.schedule_time">
              {{ formatDateTime(row.schedule_time) }}
            </span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="重要" width="80">
          <template #default="{ row }">
            <el-icon v-if="row.is_important" :size="18" color="#f56c6c">
              <StarFilled />
            </el-icon>
          </template>
        </el-table-column>
        <el-table-column prop="publisher" label="发布单位" width="150" show-overflow-tooltip />
        <el-table-column prop="views" label="浏览" width="80" sortable />
        <el-table-column label="发布时间" width="160" sortable="custom">
          <template #default="{ row }">
            {{ formatDateTime(row.published_at || row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              :icon="Edit"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="row.status === 'scheduled'"
              link
              type="success"
              size="small"
              :icon="Check"
              @click="handlePublishNow(row)"
            >
              立即发布
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 创建/编辑通知对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '发布通知' : '编辑通知'"
      width="700px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
        label-position="left"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="formData.title"
            placeholder="请输入通知标题"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select
            v-model="formData.category"
            placeholder="选择或输入分类"
            filterable
            allow-create
            style="width: 100%"
          >
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="摘要" prop="content">
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="3"
            placeholder="请输入通知摘要"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="详细内容">
          <el-input
            v-model="formData.detail_content"
            type="textarea"
            :rows="8"
            placeholder="请输入通知详细内容"
            maxlength="5000"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="发布单位" prop="publisher">
          <el-input
            v-model="formData.publisher"
            placeholder="请输入发布单位"
            maxlength="100"
          />
        </el-form-item>
        <el-form-item label="重要性">
          <el-switch
            v-model="formData.is_important"
            :active-value="1"
            :inactive-value="0"
            active-text="重要"
            inactive-text="普通"
          />
        </el-form-item>
        <el-form-item label="定时发布">
          <el-date-picker
            v-model="scheduleDate"
            type="datetime"
            placeholder="选择定时发布时间（留空则立即发布）"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DDTHH:mm:ss"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="附件">
          <el-upload
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
            :show-file-list="true"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.txt,.zip,.rar"
          >
            <el-button :icon="Upload">选择附件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持上传文档和压缩包，单个文件不超过10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          {{ dialogMode === 'create' ? '发布' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  Bell,
  Plus,
  Edit,
  Delete,
  Search,
  Document,
  Timer,
  StarFilled,
  Files,
  Check,
  Upload
} from '@element-plus/icons-vue'
import { notificationApi, type Notification, type NotificationCreate, type NotificationUpdate } from '@/api/notifications'

// 数据
const loading = ref(false)
const submitLoading = ref(false)
const notifications = ref<Notification[]>([])
const categories = ref<string[]>([])

// 筛选条件
const searchKeyword = ref('')
const filterStatus = ref('')
const filterCategory = ref('')
const filterImportance = ref('')

// 统计数据
const stats = reactive({
  published: 0,
  scheduled: 0,
  important: 0,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const dialogMode = ref<'create' | 'edit'>('create')
const currentNotificationId = ref<number | null>(null)
const formRef = ref<FormInstance>()
const scheduleDate = ref<string>('')
const selectedFile = ref<File | null>(null)

// 表单数据
const formData = reactive<NotificationCreate>({
  title: '',
  content: '',
  detail_content: '',
  category: '',
  publisher: '',
  is_important: 0,
  status: 'published'
})

// 表单验证规则
const formRules: FormRules = {
  title: [
    { required: true, message: '请输入通知标题', trigger: 'blur' },
    { min: 1, max: 200, message: '标题长度在 1 到 200 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入通知摘要', trigger: 'blur' }
  ]
}

// 格式化日期时间
function formatDateTime(timestamp: string): string {
  if (!timestamp) return '-'
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 禁用过去的日期
function disabledDate(time: Date) {
  return time.getTime() < Date.now() - 8.64e7 // 不能选今天之前
}

// 过滤后的通知列表
const filteredNotifications = computed(() => {
  let filtered = notifications.value

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(notification =>
      notification.title.toLowerCase().includes(keyword) ||
      (notification.content && notification.content.toLowerCase().includes(keyword))
    )
  }

  if (filterStatus.value) {
    filtered = filtered.filter(notification => notification.status === filterStatus.value)
  }

  if (filterCategory.value) {
    filtered = filtered.filter(notification => notification.category === filterCategory.value)
  }

  if (filterImportance.value !== '') {
    filtered = filtered.filter(notification =>
      notification.is_important.toString() === filterImportance.value
    )
  }

  return filtered
})

// 加载通知列表
async function loadNotifications() {
  loading.value = true
  try {
    console.log('开始加载通知列表...')
    const data = await notificationApi.getList({ include_scheduled: true })
    console.log('通知列表数据:', data)
    notifications.value = data || []

    // 计算统计数据
    stats.total = notifications.value.length
    stats.published = notifications.value.filter(n => n.status === 'published').length
    stats.scheduled = notifications.value.filter(n => n.status === 'scheduled').length
    stats.important = notifications.value.filter(n => n.is_important).length

    // 提取分类列表
    categories.value = [...new Set(data.map(item => item.category).filter(Boolean))] as string[]
    console.log('统计数据:', stats)
    console.log('分类列表:', categories.value)
  } catch (error) {
    console.error('加载通知列表失败:', error)
    ElMessage.error('加载通知列表失败')
  } finally {
    loading.value = false
  }
}

// 处理搜索
function handleSearch() {
  // 搜索逻辑在计算属性中处理
}

// 处理筛选
function handleFilter() {
  // 筛选逻辑在计算属性中处理
}

// 处理排序
function handleSort({ prop, order }: any) {
  if (prop === 'published_at' && order) {
    notifications.value.sort((a, b) => {
      const dateA = new Date(a.published_at || a.created_at).getTime()
      const dateB = new Date(b.published_at || b.created_at).getTime()
      return order === 'ascending' ? dateA - dateB : dateB - dateA
    })
  }
}

// 创建通知
function handleCreate() {
  dialogMode.value = 'create'
  currentNotificationId.value = null
  Object.assign(formData, {
    title: '',
    content: '',
    detail_content: '',
    category: '',
    publisher: '',
    is_important: 0,
    status: 'published'
  })
  scheduleDate.value = ''
  selectedFile.value = null
  dialogVisible.value = true
}

// 编辑通知
function handleEdit(notification: Notification) {
  dialogMode.value = 'edit'
  currentNotificationId.value = notification.id
  Object.assign(formData, {
    title: notification.title,
    content: notification.content || '',
    detail_content: notification.detail_content || '',
    category: notification.category || '',
    publisher: notification.publisher || '',
    is_important: notification.is_important,
    status: notification.status || 'published'
  })
  scheduleDate.value = notification.schedule_time || ''
  selectedFile.value = null
  dialogVisible.value = true
}

// 提交表单
async function handleSubmit() {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const submitData: NotificationCreate = {
        ...formData,
        schedule_time: scheduleDate.value || undefined
      }

      if (dialogMode.value === 'create') {
        // 如果有附件，使用带文件上传的API
        if (selectedFile.value) {
          await notificationApi.createWithFile(submitData, selectedFile.value)
        } else {
          await notificationApi.create(submitData)
        }
        ElMessage.success('通知发布成功')
      } else {
        const updateData: NotificationUpdate = {
          ...submitData
        }
        // 如果有附件，使用带文件上传的API
        if (selectedFile.value) {
          await notificationApi.updateWithFile(currentNotificationId.value!, updateData, selectedFile.value)
        } else {
          await notificationApi.update(currentNotificationId.value!, updateData)
        }
        ElMessage.success('通知更新成功')
      }

      dialogVisible.value = false
      loadNotifications()
    } catch (error) {
      console.error('提交失败:', error)
      ElMessage.error(dialogMode.value === 'create' ? '发布失败' : '更新失败')
    } finally {
      submitLoading.value = false
    }
  })
}

// 文件选择
function handleFileChange(file: any) {
  selectedFile.value = file.raw
  if (file.size > 10 * 1024 * 1024) {
    ElMessage.warning('文件大小不能超过10MB')
    selectedFile.value = null
  }
}

// 立即发布
async function handlePublishNow(notification: Notification) {
  try {
    await ElMessageBox.confirm('确定要立即发布此通知吗？', '确认', {
      type: 'warning'
    })

    await notificationApi.update(notification.id, {
      status: 'published',
      schedule_time: undefined
    })

    ElMessage.success('已立即发布')
    loadNotifications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('立即发布失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

// 删除通知
async function handleDelete(notification: Notification) {
  try {
    await ElMessageBox.confirm(
      `确定要删除通知"${notification.title}"吗？此操作不可恢复！`,
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '删除',
        cancelButtonText: '取消'
      }
    )

    await notificationApi.remove(notification.id)
    ElMessage.success('删除成功')
    loadNotifications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadNotifications()
})
</script>

<style scoped>
.notifications-management {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.stat-icon.published {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: #fff;
}

.stat-icon.scheduled {
  background: linear-gradient(135deg, #e6a23c 0%, #f0c78a 100%);
  color: #fff;
}

.stat-icon.important {
  background: linear-gradient(135deg, #f56c6c 0%, #f89898 100%);
  color: #fff;
}

.stat-icon.total {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

/* 筛选条件 */
.filter-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

/* 通知列表 */
.notifications-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.text-muted {
  color: #c0c4cc;
}

/* 响应式 */
@media (max-width: 768px) {
  .notifications-management {
    padding: 12px;
  }

  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }

  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .stat-card {
    padding: 16px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>
