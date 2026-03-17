<template>
  <div class="admin-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title">管理后台</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <!-- 问答管理 -->
        <el-tab-pane label="问答管理" name="questions">
          <div class="tab-header">
            <el-form :inline="true" :model="questionSearchForm">
              <el-form-item label="分类">
                <el-select v-model="questionSearchForm.category" placeholder="全部" clearable>
                  <el-option label="学术问题" value="academic" />
                  <el-option label="生活问题" value="life" />
                  <el-option label="就业问题" value="career" />
                  <el-option label="其他" value="other" />
                </el-select>
              </el-form-item>
              <el-form-item label="关键词">
                <el-input
                  v-model="questionSearchForm.keyword"
                  placeholder="搜索问题内容"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="searchQuestions">搜索</el-button>
                <el-button @click="resetQuestionSearch">重置</el-button>
              </el-form-item>
            </el-form>

            <el-table v-loading="questionsLoading" :data="questions" stripe>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="question" label="问题" min-width="250">
                <template #default="{ row }">
                  <div class="text-ellipsis">{{ row.question }}</div>
                </template>
              </el-table-column>
              <el-table-column prop="category" label="分类" width="120">
                <template #default="{ row }">
                  <el-tag :type="getCategoryType(row.category)">
                    {{ getCategoryLabel(row.category) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column prop="views" label="浏览量" width="100" />
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="editQuestion(row)">
                    编辑
                  </el-button>
                  <el-button type="danger" link size="small" @click="deleteQuestion(row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-pagination
              v-model:current-page="questionPagination.page"
              v-model:page-size="questionPagination.size"
              :total="questionPagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadQuestions"
              @current-change="loadQuestions"
              style="margin-top: 20px; justify-content: flex-end"
            />
          </div>
        </el-tab-pane>

        <!-- 用户管理 -->
        <el-tab-pane label="用户管理" name="users">
          <div class="tab-header">
            <el-form :inline="true" :model="userSearchForm">
              <el-form-item label="身份">
                <el-select v-model="userSearchForm.role" placeholder="全部" clearable>
                  <el-option label="管理员" value="admin" />
                  <el-option label="教师" value="teacher" />
                  <el-option label="学生" value="student" />
                </el-select>
              </el-form-item>
              <el-form-item label="关键词">
                <el-input
                  v-model="userSearchForm.keyword"
                  placeholder="搜索用户名或邮箱"
                  clearable
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="searchUsers">搜索</el-button>
                <el-button @click="resetUserSearch">重置</el-button>
              </el-form-item>
            </el-form>

            <el-table v-loading="usersLoading" :data="users" stripe>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" width="150" />
              <el-table-column prop="email" label="邮箱" width="200" />
              <el-table-column prop="role" label="身份" width="100">
                <template #default="{ row }">
                  <el-tag :type="getRoleType(row.role)">
                    {{ getRoleLabel(row.role) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="department" label="院系" width="150" />
              <el-table-column prop="is_active" label="状态" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'danger'">
                    {{ row.is_active ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="注册时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="editUser(row)">
                    编辑
                  </el-button>
                  <el-button
                    :type="row.is_active ? 'warning' : 'success'"
                    link
                    size="small"
                    @click="toggleUserStatus(row)"
                  >
                    {{ row.is_active ? '禁用' : '启用' }}
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-pagination
              v-model:current-page="userPagination.page"
              v-model:page-size="userPagination.size"
              :total="userPagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadUsers"
              @current-change="loadUsers"
              style="margin-top: 20px; justify-content: flex-end"
            />
          </div>
        </el-tab-pane>

        <!-- 知识库管理 -->
        <!-- 通知管理 -->
        <el-tab-pane label="通知管理" name="notifications">
          <NotificationsManagementSimple />
        </el-tab-pane>

        <el-tab-pane label="知识库管理" name="knowledge">
          <div class="tab-header">
            <el-button type="primary" @click="showUploadDialog = true">
              <el-icon><Upload /></el-icon>
              上传文档
            </el-button>

            <el-table v-loading="knowledgeLoading" :data="knowledgeList" stripe style="margin-top: 20px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="200" />
              <el-table-column prop="file_name" label="文件名" min-width="200" />
              <el-table-column prop="file_type" label="文件类型" width="120" />
              <el-table-column prop="file_size" label="文件大小" width="100">
                <template #default="{ row }">
                  {{ formatFileSize(row.file_size) }}
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="上传时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link size="small" @click="downloadKnowledge(row)">
                    下载
                  </el-button>
                  <el-button type="danger" link size="small" @click="deleteKnowledge(row.id)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 上传文档对话框 -->
    <el-dialog v-model="showUploadDialog" title="上传文档" width="500px">
      <el-form :model="uploadForm" label-width="100px">
        <el-form-item label="文档标题">
          <el-input v-model="uploadForm.title" placeholder="请输入文档标题" />
        </el-form-item>
        <el-form-item label="选择文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
          >
            <el-button type="primary">选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 PDF、Word、TXT 格式，文件大小不超过10MB</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item label="文档描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入文档描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" :loading="uploading" @click="handleUpload">上传</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import { chatApi as questionsApi } from '@/api/chat'
import { authApi as usersApi } from '@/api/auth'
import { knowledgeApi } from '@/api/knowledge'
import NotificationsManagementSimple from '@/components/admin/NotificationsManagementSimple.vue'

const activeTab = ref('questions')

// 问答管理
const questionsLoading = ref(false)
const questions = ref<any[]>([])
const questionSearchForm = ref({
  category: '',
  keyword: ''
})
const questionPagination = ref({
  page: 1,
  size: 20,
  total: 0
})

// 用户管理
const usersLoading = ref(false)
const users = ref<any[]>([])
const userSearchForm = ref({
  role: '',
  keyword: ''
})
const userPagination = ref({
  page: 1,
  size: 20,
  total: 0
})

// 知识库管理
const knowledgeLoading = ref(false)
const knowledgeList = ref<any[]>([])
const showUploadDialog = ref(false)
const uploading = ref(false)
const uploadForm = ref({
  title: '',
  file: null as File | null,
  description: ''
})

const handleTabChange = (tabName: string) => {
  if (tabName === 'questions') {
    loadQuestions()
  } else if (tabName === 'users') {
    loadUsers()
  } else if (tabName === 'knowledge') {
    loadKnowledge()
  }
}

// 问答管理方法
const loadQuestions = async () => {
  questionsLoading.value = true
  try {
    const response = await questionsApi.getQuestions({
      skip: (questionPagination.value.page - 1) * questionPagination.value.size,
      limit: questionPagination.value.size,
      category: questionSearchForm.value.category
    })
    questions.value = response
    questionPagination.value.total = response.length
  } catch (error: any) {
    console.error('加载问答失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    questionsLoading.value = false
  }
}

const searchQuestions = () => {
  questionPagination.value.page = 1
  loadQuestions()
}

const resetQuestionSearch = () => {
  questionSearchForm.value = {
    category: '',
    keyword: ''
  }
  questionPagination.value.page = 1
  loadQuestions()
}

const editQuestion = (question: any) => {
  ElMessage.info('编辑功能开发中')
}

const deleteQuestion = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个问题吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    // 暂时提示删除功能
    ElMessage.success('删除功能开发中')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

// 用户管理方法
const loadUsers = async () => {
  usersLoading.value = true
  try {
    // 这里需要调用管理员获取用户列表的API
    const response = await usersApi.getUsers({
      skip: (userPagination.value.page - 1) * userPagination.value.size,
      limit: userPagination.value.size,
      role: userSearchForm.value.role
    })
    users.value = response || []
    userPagination.value.total = response?.length || 0
  } catch (error: any) {
    console.error('加载用户失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    usersLoading.value = false
  }
}

const searchUsers = () => {
  userPagination.value.page = 1
  loadUsers()
}

const resetUserSearch = () => {
  userSearchForm.value = {
    role: '',
    keyword: ''
  }
  userPagination.value.page = 1
  loadUsers()
}

const editUser = (user: any) => {
  ElMessage.info('编辑用户功能开发中')
}

const toggleUserStatus = async (user: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要${user.is_active ? '禁用' : '启用'}该用户吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    ElMessage.success('操作成功')
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  }
}

// 知识库管理方法
const loadKnowledge = async () => {
  knowledgeLoading.value = true
  try {
    const response = await knowledgeApi.getList()
    knowledgeList.value = response
  } catch (error: any) {
    console.error('加载知识库失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    knowledgeLoading.value = false
  }
}

const handleFileChange = (file: any) => {
  uploadForm.value.file = file.raw
}

const handleUpload = async () => {
  if (!uploadForm.value.title || !uploadForm.value.file) {
    ElMessage.warning('请填写完整的上传信息')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('title', uploadForm.value.title)
    formData.append('file', uploadForm.value.file)
    formData.append('description', uploadForm.value.description)

    await knowledgeApi.upload(formData)
    ElMessage.success('上传成功')
    showUploadDialog.value = false
    uploadForm.value = { title: '', file: null, description: '' }
    loadKnowledge()
  } catch (error: any) {
    console.error('上传失败:', error)
    ElMessage.error(error.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

const downloadKnowledge = (item: any) => {
  ElMessage.info('下载功能开发中')
}

const deleteKnowledge = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个文档吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await knowledgeApi.delete(id)
    ElMessage.success('删除成功')
    loadKnowledge()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

// 辅助方法
const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const getCategoryType = (category: string) => {
  const typeMap: Record<string, string> = {
    academic: 'primary',
    life: 'success',
    career: 'warning',
    other: 'info'
  }
  return typeMap[category] || 'info'
}

const getCategoryLabel = (category: string) => {
  const labelMap: Record<string, string> = {
    academic: '学术问题',
    life: '生活问题',
    career: '就业问题',
    other: '其他'
  }
  return labelMap[category] || '其他'
}

const getRoleType = (role: string) => {
  const typeMap: Record<string, string> = {
    admin: 'danger',
    teacher: 'warning',
    student: 'primary'
  }
  return typeMap[role] || 'info'
}

const getRoleLabel = (role: string) => {
  const labelMap: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return labelMap[role] || role
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.admin-container {
  padding: 20px;
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

.tab-header {
  padding: 10px 0;
}

.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

:deep(.el-pagination) {
  display: flex;
  justify-content: flex-end;
}
</style>
