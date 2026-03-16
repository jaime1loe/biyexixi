<template>
  <div class="profile-change-review">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">信息修改审核</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <!-- 待审核 -->
        <el-tab-pane label="待审核" name="pending">
          <el-table :data="pendingRequests" stripe v-loading="loading">
            <el-table-column prop="id" label="申请ID" width="80" />
            <el-table-column prop="user_id" label="用户ID" width="100" />
            <el-table-column label="修改内容" min-width="300">
              <template #default="{ row }">
                <div class="change-content">
                  <div v-if="row.real_name" class="change-item">
                    <span class="change-label">真实姓名:</span>
                    <span>{{ row.real_name }}</span>
                  </div>
                  <div v-if="row.email" class="change-item">
                    <span class="change-label">邮箱:</span>
                    <span>{{ row.email }}</span>
                  </div>
                  <div v-if="row.phone" class="change-item">
                    <span class="change-label">手机号:</span>
                    <span>{{ row.phone }}</span>
                  </div>
                  <div v-if="row.department" class="change-item">
                    <span class="change-label">院系:</span>
                    <span>{{ row.department }}</span>
                  </div>
                  <div v-if="row.major" class="change-item">
                    <span class="change-label">专业:</span>
                    <span>{{ row.major }}</span>
                  </div>
                  <div v-if="row.bio" class="change-item">
                    <span class="change-label">个人简介:</span>
                    <span>{{ row.bio }}</span>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="reason" label="修改原因" width="150" show-overflow-tooltip />
            <el-table-column prop="created_at" label="申请时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="success" size="small" @click="handleApprove(row)">
                  通过
                </el-button>
                <el-button type="danger" size="small" @click="handleReject(row)">
                  拒绝
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!loading && pendingRequests.length === 0" description="暂无待审核申请" />
        </el-tab-pane>

        <!-- 已审核 -->
        <el-tab-pane label="已审核" name="reviewed">
          <el-table :data="reviewedRequests" stripe v-loading="loading">
            <el-table-column prop="id" label="申请ID" width="80" />
            <el-table-column prop="user_id" label="用户ID" width="100" />
            <el-table-column prop="reason" label="修改原因" width="150" show-overflow-tooltip />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="admin_comment" label="审核意见" min-width="150" show-overflow-tooltip />
            <el-table-column prop="reviewed_at" label="审核时间" width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.reviewed_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewDetail(row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="!loading && reviewedRequests.length === 0" description="暂无已审核申请" />
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 审核对话框 -->
    <el-dialog v-model="reviewDialogVisible" :title="reviewDialogTitle" width="600px">
      <el-form :model="reviewForm" label-width="100px">
        <el-form-item label="修改原因">
          <el-input v-model="currentRequest.reason" disabled />
        </el-form-item>
        <el-form-item label="修改内容">
          <div class="change-content">
            <div v-if="currentRequest.real_name" class="change-item">
              <span class="change-label">真实姓名:</span>
              <span>{{ currentRequest.real_name }}</span>
            </div>
            <div v-if="currentRequest.email" class="change-item">
              <span class="change-label">邮箱:</span>
              <span>{{ currentRequest.email }}</span>
            </div>
            <div v-if="currentRequest.phone" class="change-item">
              <span class="change-label">手机号:</span>
              <span>{{ currentRequest.phone }}</span>
            </div>
            <div v-if="currentRequest.department" class="change-item">
              <span class="change-label">院系:</span>
              <span>{{ currentRequest.department }}</span>
            </div>
            <div v-if="currentRequest.major" class="change-item">
              <span class="change-label">专业:</span>
              <span>{{ currentRequest.major }}</span>
            </div>
            <div v-if="currentRequest.bio" class="change-item">
              <span class="change-label">个人简介:</span>
              <span>{{ currentRequest.bio }}</span>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="审核意见">
          <el-input
            v-model="reviewForm.admin_comment"
            type="textarea"
            :rows="3"
            placeholder="请输入审核意见"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReview" :loading="reviewing">
          确认
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="申请详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="申请ID">{{ currentRequest.id }}</el-descriptions-item>
        <el-descriptions-item label="用户ID">{{ currentRequest.user_id }}</el-descriptions-item>
        <el-descriptions-item label="修改原因">{{ currentRequest.reason }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">
          {{ currentRequest.real_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">
          {{ currentRequest.email || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="手机号">
          {{ currentRequest.phone || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="院系">
          {{ currentRequest.department || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="专业">
          {{ currentRequest.major || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="个人简介">
          {{ currentRequest.bio || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentRequest.status)">
            {{ getStatusLabel(currentRequest.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="审核意见">
          {{ currentRequest.admin_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="申请时间">
          {{ formatDateTime(currentRequest.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item label="审核时间">
          {{ formatDateTime(currentRequest.reviewed_at) || '-' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { profileChangesApi } from '@/api/profileChanges'

const activeTab = ref('pending')
const loading = ref(false)
const reviewing = ref(false)
const reviewDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const reviewDialogTitle = ref('')

const pendingRequests = ref<any[]>([])
const reviewedRequests = ref<any[]>([])
const currentRequest = reactive<any>({})

const reviewForm = reactive({
  status: '',
  admin_comment: ''
})

const loadPendingRequests = async () => {
  loading.value = true
  try {
    // 调用API获取待审核申请
    const data = await profileChangesApi.getPending()
    pendingRequests.value = data || []
  } catch (error) {
    console.error('加载待审核申请失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const loadReviewedRequests = async () => {
  loading.value = true
  try {
    // 调用API获取已审核申请
    const data = await profileChangesApi.getAll({ skip: 0, limit: 100 })
    // 过滤出已审核的申请
    reviewedRequests.value = data.filter((r: any) => r.status !== 'pending') || []
  } catch (error) {
    console.error('加载已审核申请失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleApprove = (row: any) => {
  Object.assign(currentRequest, row)
  reviewForm.status = 'approved'
  reviewForm.admin_comment = '审核通过'
  reviewDialogTitle.value = '通过申请'
  reviewDialogVisible.value = true
}

const handleReject = (row: any) => {
  Object.assign(currentRequest, row)
  reviewForm.status = 'rejected'
  reviewForm.admin_comment = ''
  reviewDialogTitle.value = '拒绝申请'
  reviewDialogVisible.value = true
}

const confirmReview = async () => {
  if (reviewForm.status === 'rejected' && !reviewForm.admin_comment) {
    ElMessage.warning('拒绝申请必须填写审核意见')
    return
  }

  reviewing.value = true
  try {
    // 调用API审核
    await profileChangesApi.review(currentRequest.id, {
      status: reviewForm.status,
      admin_comment: reviewForm.admin_comment
    })

    ElMessage.success(reviewForm.status === 'approved' ? '审核通过' : '已拒绝申请')
    reviewDialogVisible.value = false

    // 重新加载数据
    loadPendingRequests()
    loadReviewedRequests()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    reviewing.value = false
  }
}

const viewDetail = (row: any) => {
  Object.assign(currentRequest, row)
  detailDialogVisible.value = true
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labelMap: Record<string, string> = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝'
  }
  return labelMap[status] || status
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadPendingRequests()
  loadReviewedRequests()
})
</script>

<style scoped>
.profile-change-review {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.change-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.change-item {
  display: flex;
  gap: 8px;
}

.change-label {
  font-weight: 500;
  color: #606266;
  min-width: 80px;
}
</style>
