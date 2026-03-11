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
              <div class="stat-icon" style="background: #409eff;">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">24</div>
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
                <div class="stat-value">20</div>
                <div class="stat-label">已处理</div>
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
                <div class="stat-value">3</div>
                <div class="stat-label">处理中</div>
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
                <div class="stat-value">1</div>
                <div class="stat-label">失败</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="knowledge-content">
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="文档列表" name="list">
          <el-table v-loading="loading" :data="documentList" style="width: 100%" stripe>
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
                <el-button link type="primary" :icon="View" size="small">查看</el-button>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
const uploading = ref(false)
const uploadFile = ref<File | null>(null)
const selectedCategory = ref('')
const showInput = ref(false)
const newCategory = ref('')
const loading = ref(false)

const statusMap = {
  pending: '待处理',
  processing: '处理中',
  completed: '已完成',
  failed: '失败'
}

const categories = ref<Array<{ name: string; count: number }>>([])

const documentList = ref<KnowledgeDoc[]>([])

async function loadCategories() {
  try {
    const data = await knowledgeApi.getCategories()
    // 获取每个分类的知识数量
    categories.value = data.categories.map(cat => ({
      name: cat,
      count: 0 // 这里可以单独调用API获取数量，暂时设为0
    }))
  } catch (error: any) {
    ElMessage.error('加载分类失败')
  }
}

async function loadDocuments() {
  loading.value = true
  try {
    const data = await knowledgeApi.getList({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    documentList.value = data.map((item, index) => ({
      ...item,
      uploadTime: item.created_at,
      status: 'completed'
    }))
    total.value = data.length
  } catch (error: any) {
    ElMessage.error('加载文档列表失败')
  } finally {
    loading.value = false
  }
}

function handleUpload() {
  if (userStore.userInfo?.role !== 'admin') {
    ElMessage.warning('只有管理员可以上传文档')
    return
  }
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
    const formData = new FormData()
    formData.append('file', uploadFile.value)
    formData.append('title', uploadFile.value.name)
    formData.append('content', '') // 需要添加内容字段
    if (selectedCategory.value) {
      formData.append('category', selectedCategory.value)
    }

    await knowledgeApi.upload(formData)
    ElMessage.success('文档上传成功，正在处理中...')
    uploadDialogVisible.value = false
    loadDocuments()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '文档上传失败')
  } finally {
    uploading.value = false
  }
}

async function handleDelete(row: KnowledgeDoc) {
  if (userStore.userInfo?.role !== 'admin') {
    ElMessage.warning('只有管理员可以删除文档')
    return
  }
  try {
    await ElMessageBox.confirm(`确定要删除文档"${row.title}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await knowledgeApi.delete(row.id)
    ElMessage.success('删除成功')
    loadDocuments()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function handleAddCategory() {
  if (newCategory.value.trim()) {
    ElMessage.success('分类功能需要后端支持')
    newCategory.value = ''
    showInput.value = false
  }
}

function handleDeleteCategory(name: string) {
  ElMessage.success('分类删除功能需要后端支持')
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

onMounted(() => {
  loadCategories()
  loadDocuments()
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
</style>
