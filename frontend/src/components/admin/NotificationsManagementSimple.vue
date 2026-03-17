<template>
  <div class="notifications-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>通知管理</span>
          <el-button type="primary" :icon="Plus" @click="showCreateDialog = true">
            发布通知
          </el-button>
        </div>
      </template>

      <div v-loading="loading">
        <el-empty v-if="!loading && notifications.length === 0" description="暂无通知" />

        <el-table v-else :data="notifications" stripe>
          <el-table-column type="index" label="#" width="60" />
          <el-table-column prop="title" label="标题" min-width="200" />
          <el-table-column label="分类" width="120">
            <template #default="{ row }">
              <el-tag v-if="row.category" size="small">{{ row.category }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="publisher" label="发布单位" width="150" />
          <el-table-column prop="views" label="浏览" width="80" />
          <el-table-column label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button link type="primary" size="small" @click="editNotification(row)">
                编辑
              </el-button>
              <el-button link type="danger" size="small" @click="deleteNotification(row.id)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingId ? '编辑通知' : '发布通知'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入通知标题" />
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="form.category" placeholder="请输入分类" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.content" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="详细内容">
          <el-input v-model="form.detail_content" type="textarea" :rows="5" />
        </el-form-item>
        <el-form-item label="发布单位">
          <el-input v-model="form.publisher" placeholder="请输入发布单位" />
        </el-form-item>
        <el-form-item label="重要性">
          <el-switch
            v-model="form.is_important"
            :active-value="1"
            :inactive-value="0"
            active-text="重要"
            inactive-text="普通"
          />
        </el-form-item>
        <el-form-item label="定时发布">
          <el-date-picker
            v-model="form.schedule_time"
            type="datetime"
            placeholder="选择定时发布时间（留空则立即发布）"
            value-format="YYYY-MM-DDTHH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">
          {{ editingId ? '保存' : '发布' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { notificationApi, type Notification, type NotificationCreate } from '@/api/notifications'

const loading = ref(false)
const submitting = ref(false)
const notifications = ref<Notification[]>([])
const showCreateDialog = ref(false)
const editingId = ref<number | null>(null)

const form = reactive<NotificationCreate>({
  title: '',
  content: '',
  detail_content: '',
  category: '',
  publisher: '',
  is_important: 0,
  status: 'published'
})

// 加载通知列表
async function loadNotifications() {
  loading.value = true
  try {
    console.log('正在加载通知...')
    const data = await notificationApi.getList({ include_scheduled: true })
    console.log('通知数据:', data)
    notifications.value = data || []
    console.log('通知数量:', notifications.value.length)
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载通知失败')
  } finally {
    loading.value = false
  }
}

// 编辑通知
function editNotification(notification: Notification) {
  editingId.value = notification.id
  Object.assign(form, {
    title: notification.title,
    content: notification.content || '',
    detail_content: notification.detail_content || '',
    category: notification.category || '',
    publisher: notification.publisher || '',
    is_important: notification.is_important,
    status: notification.status || 'published',
    schedule_time: notification.schedule_time || undefined
  })
  showCreateDialog.value = true
}

// 提交表单
async function submitForm() {
  if (!form.title || !form.content) {
    ElMessage.warning('请填写标题和摘要')
    return
  }

  submitting.value = true
  try {
    console.log('提交表单:', form)

    if (editingId.value) {
      // 更新
      await notificationApi.update(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      // 创建
      await notificationApi.create(form)
      ElMessage.success('发布成功')
    }

    showCreateDialog.value = false
    resetForm()
    loadNotifications()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('操作失败')
  } finally {
    submitting.value = false
  }
}

// 删除通知
async function deleteNotification(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除这条通知吗？', '确认', {
      type: 'warning'
    })

    await notificationApi.remove(id)
    ElMessage.success('删除成功')
    loadNotifications()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 重置表单
function resetForm() {
  editingId.value = null
  Object.assign(form, {
    title: '',
    content: '',
    detail_content: '',
    category: '',
    publisher: '',
    is_important: 0,
    status: 'published',
    schedule_time: undefined
  })
}

// 格式化日期
function formatDate(dateStr: string): string {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 获取状态类型
function getStatusType(status: string): string {
  const types: Record<string, string> = {
    published: 'success',
    scheduled: 'warning',
    draft: 'info'
  }
  return types[status] || 'info'
}

// 获取状态文本
function getStatusText(status: string): string {
  const texts: Record<string, string> = {
    published: '已发布',
    scheduled: '待定时',
    draft: '草稿'
  }
  return texts[status] || '未知'
}

onMounted(() => {
  console.log('组件已挂载')
  loadNotifications()
})
</script>

<style scoped>
.notifications-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
