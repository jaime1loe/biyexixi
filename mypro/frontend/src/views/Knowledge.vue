<template>
  <div class="knowledge-container">
    <div class="knowledge-header">
      <h3><el-icon><Document /></el-icon>知识库管理</h3>
      <el-button type="primary" :icon="Upload" @click="handleUpload">上传文档</el-button>
    </div>

    <div class="knowledge-stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #909399;">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.totalDocs }}</div>
                <div class="stat-label">文档总数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #67c23a;">
                <el-icon><SuccessFilled /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.completed }}</div>
                <div class="stat-label">{{ isAdmin ? '已处理' : '已通过' }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #e6a23c;">
                <el-icon><Loading /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.processing }}</div>
                <div class="stat-label">{{ isAdmin ? '待处理' : '待审核' }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #f56c6c;">
                <el-icon><CircleClose /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.failed }}</div>
                <div class="stat-label">{{ isAdmin ? '已拒绝' : '失败' }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="knowledge-content">
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 管理员专属：待审核文件 -->
        <el-tab-pane v-if="isAdmin" label="待审核文件" name="pending">
          <el-table v-loading="loading" :data="pendingList" style="width: 100%" stripe>
            <el-table-column prop="title" label="文档名称" min-width="200">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <el-icon color="#409eff"><Document /></el-icon>
                  {{ row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" />
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
          <el-table v-loading="loading" :data="documentList" style="width: 100%; margin-top: 16px;" stripe>
            <el-table-column prop="title" label="文档名称" min-width="200">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <el-icon color="#409eff"><Document /></el-icon>
                  {{ row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" />
            <el-table-column prop="uploadTime" label="上传时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.uploadTime) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="View" size="small" @click="handleView(row)">查看</el-button>
                <!-- 管理员可以删除任意文档，教师/学生只能删除已被拒绝的文档 -->
                <el-button
                  v-if="isAdmin || (row.review_status === 'rejected')"
                  link
                  type="danger"
                  :icon="Delete"
                  size="small"
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
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

        <!-- 学生/教师专属：我的文档 -->
        <el-tab-pane v-if="!isAdmin" label="我的文档" name="my-documents">
          <el-table v-loading="loading" :data="myDocumentsList" style="width: 100%" stripe>
            <el-table-column prop="title" label="文档名称" min-width="200">
              <template #default="{ row }">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <el-icon color="#409eff"><Document /></el-icon>
                  {{ row.title }}
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120" />
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
            <el-table-column prop="rejection_reason" label="拒绝原因" min-width="200">
              <template #default="{ row }">
                <span style="color: #f56c6c;">{{ row.rejection_reason || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" :icon="View" size="small" @click="handleView(row)">查看</el-button>
                <el-button v-if="row.review_status === 'rejected'" link type="danger" :icon="Delete" size="small" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane v-if="isAdmin" label="分类管理" name="category">
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
    </div>

    <el-dialog v-model="uploadDialogVisible" title="上传文档" width="500px">
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
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmUpload" :loading="uploading">
          开始上传
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="viewDialogVisible" title="查看文档" width="800px">
      <div class="view-dialog" v-if="currentDoc">
        <div class="doc-header">
          <h3>{{ currentDoc.title }}</h3>
          <div class="doc-meta">
            <el-tag size="small">{{ currentDoc.category || '未分类' }}</el-tag>
            <span class="upload-time">上传时间：{{ formatTime(currentDoc.uploadTime) }}</span>
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
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Upload, View, Delete, SuccessFilled, Loading, CircleClose, Plus, UploadFilled } from '@element-plus/icons-vue'
import { knowledgeApi, Knowledge } from '@/api/knowledge'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

interface KnowledgeDoc extends Knowledge {
  uploadTime: string
  status: string
}

const activeTab = ref('list')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const uploadDialogVisible = ref(false)
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
const currentDoc = ref<KnowledgeDoc | null>(null)
const pendingDoc = ref<Knowledge | null>(null)
const rejectReason = ref('')

// 记录本次登录时初始的统计数（用于计算本次处理数量）
const initialStats = ref({
  approved: 0,
  rejected: 0
})

const statusMap = {
  pending: '待处理',
  processing: '处理中',
  completed: '已完成',
  failed: '失败'
}

const reviewStatusMap = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已拒绝'
}

const categories = ref<Array<{ name: string; count: number }>>([])

const documentList = ref<KnowledgeDoc[]>([])
const pendingList = ref<Knowledge[]>([])
const myDocumentsList = ref<Knowledge[]>([])

// 判断是否为管理员
const isAdmin = computed(() => userStore.userInfo?.role === 'admin')

// 统计数据
const stats = ref({
  totalDocs: 0,
  completed: 0,
  processing: 0,
  failed: 0,
  totalProcessed: 0
})

// 加载统计数据（管理员统计所有文档，学生/老师统计自己的文档）
async function loadStats() {
  try {
    // 管理员和学生/老师都获取知识库中所有已审核通过的文档
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    if (isAdmin.value) {
      // 管理员：获取待审核列表
      const pendingDocs = await knowledgeApi.getPending()

      // 计算统计数据
      const totalApproved = allDocs.filter(doc => doc.review_status === 'approved').length
      const totalRejected = allDocs.filter(doc => doc.review_status === 'rejected').length
      const totalPending = pendingDocs.length
      const thisSessionApproved = totalApproved - initialStats.value.approved
      const thisSessionRejected = totalRejected - initialStats.value.rejected

      stats.value = {
        totalDocs: totalApproved, // 文档总数（已审核通过）
        completed: thisSessionApproved, // 本次登录后通过的文档数
        processing: totalPending, // 当前等待审核的文档数
        failed: thisSessionRejected, // 本次登录后拒绝的文档数
        totalProcessed: 0
      }
    } else {
      // 学生/老师：统计自己上传的文档
      const myDocs = await knowledgeApi.getMyDocuments()
      stats.value = {
        totalDocs: allDocs.filter(doc => doc.review_status === 'approved').length, // 知识库中所有已审核通过的文档数
        completed: myDocs.filter(doc => doc.review_status === 'approved').length, // 审核通过的文档数
        processing: myDocs.filter(doc => doc.review_status === 'pending').length, // 等待审核的文档数
        failed: myDocs.filter(doc => doc.review_status === 'rejected').length, // 被拒绝的文档数
        totalProcessed: 0
      }
    }
  } catch (error: any) {
    console.error('加载统计数据失败', error)
  }
}

// 初始化管理员统计（记录登录时的初始值）
async function initAdminStats() {
  if (!isAdmin.value) return

  try {
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    // 记录登录时已通过和已拒绝的数量
    initialStats.value = {
      approved: allDocs.filter(doc => doc.review_status === 'approved').length,
      rejected: allDocs.filter(doc => doc.review_status === 'rejected').length
    }
  } catch (error: any) {
    console.error('初始化统计失败', error)
  }
}

async function loadCategories() {
  try {
    const data = await knowledgeApi.getCategories()
    // 获取所有文档以统计每个分类的数量
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    // 统计每个分类的文档数量
    const categoryCountMap: Record<string, number> = {}
    allDocs.forEach(doc => {
      if (doc.category) {
        categoryCountMap[doc.category] = (categoryCountMap[doc.category] || 0) + 1
      }
    })

    // 更新分类列表及其数量
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
    // 获取所有文档
    const allDocs = await knowledgeApi.getList({
      skip: 0,
      limit: 10000
    })

    let filteredDocs = allDocs

    // 按分类筛选
    if (selectedCategoryFilter.value) {
      filteredDocs = filteredDocs.filter(doc => doc.category === selectedCategoryFilter.value)
    }

    // 按上传时间筛选
    if (uploadTimeRange.value && uploadTimeRange.value.length === 2) {
      const [startDate, endDate] = uploadTimeRange.value
      const startTime = new Date(startDate).setHours(0, 0, 0, 0)
      const endTime = new Date(endDate).setHours(23, 59, 59, 999)
      filteredDocs = filteredDocs.filter(doc => {
        const docTime = new Date(doc.created_at).getTime()
        return docTime >= startTime && docTime <= endTime
      })
    }

    // 更新总数
    total.value = filteredDocs.length

    // 分页处理
    const startIndex = (currentPage.value - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    const paginatedDocs = filteredDocs.slice(startIndex, endIndex)

    documentList.value = paginatedDocs.map((item, index) => ({
      ...item,
      uploadTime: item.created_at,
      status: item.status || 'completed'
    }))

    // 加载所有文档以获取准确的统计数据
    await loadStats()
  } catch (error: any) {
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

function handleUpload() {
  uploadDialogVisible.value = true
  uploadFile.value = null
  selectedCategory.value = ''
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
    // 读取文件内容作为文本
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
    uploadDialogVisible.value = false
    // 重新加载数据
    loadDocuments()
    loadCategories() // 更新分类数量
    loadStats() // 重新加载统计数据
    if (!isAdmin.value) {
      loadMyDocuments() // 学生/老师也更新我的文档列表
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '文档上传失败')
  } finally {
    uploading.value = false
  }
}

// 读取文件内容（支持多种编码）
async function readFileContent(file: File): Promise<string> {
  const fileName = file.name.toLowerCase()

  // 对于二进制文件（doc, docx, pdf），返回提示信息
  if (fileName.endsWith('.doc') || fileName.endsWith('.docx') || fileName.endsWith('.pdf')) {
    return `[这是 ${file.name} 文件，文件已保存到服务器，可以下载查看完整内容]`
  }

  // 对于文本文件，尝试多种编码读取
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      const text = e.target?.result as string || ''

      // 检测是否包含乱码字符
      const hasGarbledChars = /[\uFFFD\u00A0\u200B\uFEFF]/.test(text) ||
                             (/[\x00-\x08\x0B\x0C\x0E-\x1F]/.test(text))

      if (hasGarbledChars) {
        // 如果检测到乱码，尝试使用 GBK 编码读取
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

    // 首先尝试 UTF-8 编码
    reader.readAsText(file, 'UTF-8')
  })
}

async function handleView(row: KnowledgeDoc) {
  try {
    const data = await knowledgeApi.getById(row.id)
    currentDoc.value = {
      ...data,
      uploadTime: row.uploadTime,
      status: row.status
    }
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

async function handleDelete(row: KnowledgeDoc) {
  // 管理员可以删除任意文档
  // 教师/学生只能删除自己上传的已被拒绝的文档
  if (userStore.userInfo?.role !== 'admin') {
    if (row.review_status !== 'rejected') {
      ElMessage.warning('只能删除已被拒绝的文档')
      return
    }
  }
  try {
    await ElMessageBox.confirm(`确定要删除文档"${row.title}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await knowledgeApi.delete(row.id)
    ElMessage.success('删除成功')
    // 根据当前标签页重新加载数据
    if (activeTab.value === 'my-documents') {
      loadMyDocuments()
    } else {
      loadDocuments()
    }
    loadStats() // 更新统计数据
    loadCategories() // 更新分类数量
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

async function handleAddCategory() {
  if (newCategory.value.trim()) {
    try {
      await knowledgeApi.addCategory(newCategory.value.trim())
      ElMessage.success('分类添加成功')
      newCategory.value = ''
      showInput.value = false
      await loadCategories() // 更新分类列表和数量
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
    await loadCategories() // 更新分类列表和数量
    await loadDocuments() // 更新文档列表
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除分类失败')
    }
  }
}

// 加载待审核列表（管理员）
async function loadPendingList() {
  loading.value = true
  try {
    const data = await knowledgeApi.getPending()
    pendingList.value = data
  } catch (error: any) {
    ElMessage.error('加载待审核列表失败')
  } finally {
    loading.value = false
  }
}

// 加载我的文档（学生/教师）
async function loadMyDocuments() {
  loading.value = true
  try {
    const data = await knowledgeApi.getMyDocuments()
    myDocumentsList.value = data
    // 学生/老师加载数据时也更新统计
    await loadStats()
  } catch (error: any) {
    ElMessage.error('加载我的文档失败')
  } finally {
    loading.value = false
  }
}

// 审核通过
async function handleApprove(row: Knowledge) {
  try {
    await ElMessageBox.confirm(`确定要通过"${row.title}"的审核吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info'
    })
    await knowledgeApi.review(row.id, 'approve')
    ElMessage.success('审核通过')
    await loadPendingList()
    await loadDocuments() // 更新文档列表
    await loadStats() // 更新统计数据
    await loadCategories() // 更新分类数量
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '审核失败')
    }
  }
}

// 审核拒绝
function handleReject(row: Knowledge) {
  pendingDoc.value = row
  rejectReason.value = ''
  rejectDialogVisible.value = true
}

// 确认拒绝
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
    await loadDocuments() // 更新文档列表
    await loadStats() // 更新统计数据
    await loadCategories() // 更新分类数量
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '拒绝失败')
  }
}

// 获取审核状态文本
function getReviewStatusText(status?: string): string {
  return status ? reviewStatusMap[status as keyof typeof reviewStatusMap] || status : '未知'
}

// 获取审核状态类型
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

// 筛选条件变化处理
function handleFilterChange() {
  currentPage.value = 1
  loadDocuments()
}

onMounted(() => {
  // 管理员：初始化统计（记录登录时的初始值）
  if (isAdmin.value) {
    initAdminStats().then(() => {
      loadStats()
    })
  }

  loadCategories()
  loadDocuments()

  // 根据角色加载不同的列表
  if (isAdmin.value) {
    loadPendingList()
  } else {
    loadMyDocuments()
  }

  // 监听标签页切换
  watch(activeTab, (newTab) => {
    if (isAdmin.value) {
      if (newTab === 'pending') {
        loadPendingList()
      } else if (newTab === 'list') {
        loadDocuments()
      }
    } else {
      if (newTab === 'my-documents') {
        loadMyDocuments()
      } else if (newTab === 'list') {
        loadDocuments()
      }
    }
  })
})
</script>

<style scoped>
.knowledge-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.knowledge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.knowledge-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.knowledge-stats {
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.knowledge-content {
  border-radius: 8px;
  overflow: hidden;
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

.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
</style>
