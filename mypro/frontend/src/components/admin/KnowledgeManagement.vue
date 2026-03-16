<template>
  <div class="knowledge-management">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card primary">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalDocs }}</div>
              <div class="stat-label">文档总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card success">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><SuccessFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.approved }}</div>
              <div class="stat-label">已审核通过</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card warning">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.pending }}</div>
              <div class="stat-label">待审核</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card danger">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><CircleClose /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.rejected }}</div>
              <div class="stat-label">已拒绝</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 标签页 -->
    <el-card class="content-card">
      <template #header>
        <div class="card-header">
          <span class="title">知识库管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="showUploadDialog = true">
              <el-icon><Upload /></el-icon>
              上传文档
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab" type="border-card">
        <!-- 待审核文件 -->
        <el-tab-pane label="待审核文件" name="pending">
          <el-table v-loading="loading" :data="pendingList" stripe>
            <el-table-column prop="title" label="文档名称" min-width="200">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <el-icon color="#409eff"><Document /></el-icon>
                  {{ row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="uploader_name" label="上传者" width="120" />
            <el-table-column prop="created_at" label="上传时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="审核操作" width="280" fixed="right">
              <template #default="{ row }">
                <el-button type="success" size="small" @click="handleApprove(row)">通过</el-button>
                <el-button type="danger" size="small" @click="handleReject(row)">拒绝</el-button>
                <el-button link type="primary" :icon="View" size="small" @click="handleView(row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 文档列表 -->
        <el-tab-pane label="文档列表" name="list">
          <div class="filter-bar">
            <el-select
              v-model="selectedCategoryFilter"
              placeholder="筛选文档种类"
              clearable
              style="width: 200px; margin-right: 12px;"
              @change="handleFilterChange"
            >
              <el-option label="全部" value="" />
              <el-option
                v-for="cat in categories"
                :key="cat.name"
                :label="cat.name"
                :value="cat.name"
              />
            </el-select>
            <el-date-picker
              v-model="uploadTimeRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              style="width: 300px;"
              @change="handleFilterChange"
            />
          </div>
          
          <el-table v-loading="loading" :data="documentList" stripe style="margin-top: 16px;">
            <el-table-column prop="title" label="文档名称" min-width="200">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <el-icon color="#409eff"><Document /></el-icon>
                  {{ row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="uploader_name" label="上传者" width="120" />
            <el-table-column prop="review_status" label="审核状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getReviewStatusType(row.review_status)">
                  {{ getReviewStatusText(row.review_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="上传时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="View" size="small" @click="handleView(row)">查看</el-button>
                <el-button link type="danger" :icon="Delete" size="small" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              layout="total, prev, pager, next, jumper"
              @change="loadDocuments"
            />
          </div>
        </el-tab-pane>

        <!-- 分类管理 -->
        <el-tab-pane label="分类管理" name="category">
          <div class="category-list">
            <el-tag
              v-for="category in categories"
              :key="category.name"
              closable
              size="large"
              @close="handleDeleteCategory(category.name)"
            >
              {{ category.name }} ({{ category.count }})
            </el-tag>
            <el-input
              v-if="showInput"
              v-model="newCategory"
              size="small"
              style="width: 120px;"
              @blur="handleAddCategory"
              @keyup.enter="handleAddCategory"
            />
            <el-button
              v-else
              size="small"
              :icon="Plus"
              @click="showInput = true"
            >
              添加分类
            </el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 上传文档对话框 -->
    <el-dialog v-model="showUploadDialog" title="上传文档" width="500px">
      <el-upload
        drag
        action="/api"
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".txt,.doc,.docx,.pdf"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 .txt .doc .docx .pdf 格式,文件大小不超过 10MB
          </div>
        </template>
      </el-upload>

      <el-form v-if="uploadFile" style="margin-top: 20px;">
        <el-form-item label="选择分类">
          <el-select v-model="selectedCategory" placeholder="请选择分类" style="width: 100%;">
            <el-option
              v-for="cat in categories"
              :key="cat.name"
              :label="cat.name"
              :value="cat.name"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmUpload" :loading="uploading">
          开始上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 查看文档对话框 -->
    <el-dialog v-model="viewDialogVisible" title="查看文档" width="800px">
      <div class="view-dialog" v-if="currentDoc">
        <div class="doc-header">
          <h3>{{ currentDoc.title }}</h3>
          <div class="doc-meta">
            <el-tag size="small">{{ currentDoc.category || '未分类' }}</el-tag>
            <span class="upload-time">上传时间：{{ formatTime(currentDoc.created_at) }}</span>
          </div>
        </div>
        <div class="doc-content">
          <pre>{{ currentDoc.content }}</pre>
        </div>
        <div class="doc-footer" v-if="currentDoc.file_name">
          <el-divider>附件信息</el-divider>
          <div class="file-info">
            <el-icon><Document /></el-icon>
            <span>{{ currentDoc.file_name }}</span>
            <span class="file-size">{{ formatFileSize(currentDoc.file_size) }}</span>
            <el-button
              type="primary"
              size="small"
              @click="handleDownloadFile"
              style="margin-left: 12px"
            >
              下载文件
            </el-button>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 拒绝原因对话框 -->
    <el-dialog v-model="rejectDialogVisible" title="填写拒绝原因" width="500px">
      <el-input
        v-model="rejectReason"
        type="textarea"
        :rows="4"
        placeholder="请输入拒绝原因..."
      />
      <template #footer>
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmReject">确认拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Document, Upload, View, Delete, SuccessFilled, Clock, CircleClose,
  Plus, UploadFilled
} from '@element-plus/icons-vue'
import { knowledgeApi } from '@/api/knowledge'

const activeTab = ref('pending')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const showUploadDialog = ref(false)
const viewDialogVisible = ref(false)
const rejectDialogVisible = ref(false)
const uploading = ref(false)
const uploadFile = ref<File | null>(null)
const selectedCategory = ref('')
const selectedCategoryFilter = ref('')
const uploadTimeRange = ref<[Date, Date] | null>(null)
const showInput = ref(false)
const newCategory = ref('')
const loading = ref(false)
const currentDoc = ref<any>(null)
const pendingDoc = ref<any>(null)
const rejectReason = ref('')

const categories = ref<Array<{ name: string; count: number }>>([])
const documentList = ref<any[]>([])
const pendingList = ref<any[]>([])

const stats = ref({
  totalDocs: 0,
  approved: 0,
  pending: 0,
  rejected: 0
})

const reviewStatusMap = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已拒绝'
}

// 加载统计数据
async function loadStats() {
  try {
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    const pendingDocs = await knowledgeApi.getPending()

    stats.value = {
      totalDocs: allDocs.length,
      approved: allDocs.filter(doc => doc.review_status === 'approved').length,
      pending: pendingDocs.length,
      rejected: allDocs.filter(doc => doc.review_status === 'rejected').length
    }
  } catch (error: any) {
    console.error('加载统计数据失败', error)
  }
}

async function loadCategories() {
  try {
    const data = await knowledgeApi.getCategories()
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    const categoryCountMap: Record<string, number> = {}
    allDocs.forEach(doc => {
      if (doc.category) {
        categoryCountMap[doc.category] = (categoryCountMap[doc.category] || 0) + 1
      }
    })

    categories.value = data.categories.map(cat => ({
      name: cat,
      count: categoryCountMap[cat] || 0
    }))
  } catch (error: any) {
    ElMessage.error('加载分类失败')
  }
}

async function loadDocuments() {
  loading.value = true
  try {
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    let filteredDocs = allDocs

    if (selectedCategoryFilter.value) {
      filteredDocs = filteredDocs.filter(doc => doc.category === selectedCategoryFilter.value)
    }

    if (uploadTimeRange.value && uploadTimeRange.value.length === 2) {
      const [startDate, endDate] = uploadTimeRange.value
      const startTime = new Date(startDate).setHours(0, 0, 0, 0)
      const endTime = new Date(endDate).setHours(23, 59, 59, 999)
      filteredDocs = filteredDocs.filter(doc => {
        const docTime = new Date(doc.created_at).getTime()
        return docTime >= startTime && docTime <= endTime
      })
    }

    total.value = filteredDocs.length
    const startIndex = (currentPage.value - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    documentList.value = filteredDocs.slice(startIndex, endIndex)

    await loadStats()
  } catch (error: any) {
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

async function loadPendingList() {
  loading.value = true
  try {
    const data = await knowledgeApi.getPending()
    pendingList.value = data
    await loadStats()
  } catch (error: any) {
    ElMessage.error('加载待审核列表失败')
  } finally {
    loading.value = false
  }
}

function handleFileChange(file: any) {
  uploadFile.value = file.raw
}

async function handleConfirmUpload() {
  if (!uploadFile.value) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  uploading.value = true
  try {
    const content = await readFileContent(uploadFile.value)
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    formData.append('title', uploadFile.value.name.replace(/\.[^/.]+$/, ''))
    formData.append('content', content)
    if (selectedCategory.value) {
      formData.append('category', selectedCategory.value)
    }

    await knowledgeApi.upload(formData)
    ElMessage.success('文档上传成功')
    showUploadDialog.value = false
    loadDocuments()
    loadCategories()
    loadStats()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '文档上传失败')
  } finally {
    uploading.value = false
  }
}

async function readFileContent(file: File): Promise<string> {
  const fileName = file.name.toLowerCase()

  if (fileName.endsWith('.doc') || fileName.endsWith('.docx') || fileName.endsWith('.pdf')) {
    return `[这是 ${file.name} 文件，文件已保存到服务器，可以下载查看完整内容]`
  }

  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string || ''
      const hasGarbledChars = /[\uFFFD\u00A0\u200B\uFEFF]/.test(text) ||
                             (/[\x00-\x08\x0B\x0C\x0E-\x1F]/.test(text))

      if (hasGarbledChars) {
        const gbkReader = new FileReader()
        gbkReader.onload = (event) => {
          resolve(event.target?.result as string || text)
        }
        gbkReader.onerror = () => resolve(text)
        gbkReader.readAsText(file, 'GBK')
      } else {
        resolve(text)
      }
    }
    reader.onerror = () => reject(new Error('读取文件失败'))
    reader.readAsText(file, 'UTF-8')
  })
}

async function handleView(row: any) {
  try {
    const data = await knowledgeApi.getById(row.id)
    currentDoc.value = data
    viewDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error('加载文档详情失败')
  }
}

async function handleDownloadFile() {
  if (!currentDoc.value || !currentDoc.value.file_name) return

  try {
    await knowledgeApi.download(currentDoc.value.id, currentDoc.value.file_name)
    ElMessage.success('文件下载中...')
  } catch (error: any) {
    ElMessage.error('文件下载失败')
  }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm(`确定要删除文档"${row.title}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await knowledgeApi.delete(row.id)
    ElMessage.success('删除成功')
    loadDocuments()
    loadStats()
    loadCategories()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

async function handleApprove(row: any) {
  try {
    await ElMessageBox.confirm(`确定要通过"${row.title}"的审核吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    await knowledgeApi.review(row.id, 'approve')
    ElMessage.success('审核通过')
    await loadPendingList()
    await loadDocuments()
    await loadStats()
    await loadCategories()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '审核失败')
    }
  }
}

function handleReject(row: any) {
  pendingDoc.value = row
  rejectReason.value = ''
  rejectDialogVisible.value = true
}

async function handleConfirmReject() {
  if (!rejectReason.value.trim()) {
    ElMessage.warning('请填写拒绝原因')
    return
  }

  try {
    await knowledgeApi.review(pendingDoc.value!.id, 'reject', rejectReason.value.trim())
    ElMessage.success('已拒绝')
    rejectDialogVisible.value = false
    await loadPendingList()
    await loadDocuments()
    await loadStats()
    await loadCategories()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '拒绝失败')
  }
}

async function handleAddCategory() {
  if (newCategory.value.trim()) {
    try {
      await knowledgeApi.addCategory(newCategory.value.trim())
      ElMessage.success('分类添加成功')
      newCategory.value = ''
      showInput.value = false
      await loadCategories()
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '添加分类失败')
    }
  }
}

async function handleDeleteCategory(name: string) {
  try {
    await ElMessageBox.confirm(`确定要删除分类"${name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await knowledgeApi.deleteCategory(name)
    ElMessage.success('分类删除成功')
    await loadCategories()
    await loadDocuments()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除分类失败')
    }
  }
}

function getReviewStatusText(status?: string): string {
  return status ? reviewStatusMap[status as keyof typeof reviewStatusMap] || status : '未知'
}

function getReviewStatusType(status?: string): any {
  const typeMap: Record<string, any> = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger'
  }
  return typeMap[status || ''] || 'info'
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

function handleFilterChange() {
  currentPage.value = 1
  loadDocuments()
}

onMounted(() => {
  loadCategories()
  loadDocuments()
  loadPendingList()
  loadStats()
})

watch(activeTab, (newTab) => {
  if (newTab === 'pending') {
    loadPendingList()
  } else if (newTab === 'list') {
    loadDocuments()
  }
})
</script>

<style scoped>
.knowledge-management {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.primary {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: #fff;
}

.stat-card.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: #fff;
}

.stat-card.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #f0c78a 100%);
  color: #fff;
}

.stat-card.danger {
  background: linear-gradient(135deg, #f56c6c 0%, #f89898 100%);
  color: #fff;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
  margin-top: 4px;
}

.content-card {
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 20px;
}

.category-list .el-tag {
  padding: 12px 20px;
  font-size: 14px;
}

.view-dialog {
  max-height: 70vh;
  overflow-y: auto;
}

.doc-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.doc-header h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  color: #303133;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #909399;
}

.upload-time {
  font-size: 13px;
}

.doc-content {
  padding: 20px 0;
  max-height: 50vh;
  overflow-y: auto;
}

.doc-content pre {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
  margin: 0;
}

.doc-footer {
  margin-top: 20px;
  padding-top: 16px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.file-size {
  margin-left: auto;
  font-size: 12px;
  color: #909399;
}
</style>