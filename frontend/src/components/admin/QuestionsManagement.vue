<template>
  <div class="questions-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">问答管理</span>
          <el-button type="primary" @click="exportQuestions">
            <el-icon><Download /></el-icon>
            导出CSV
          </el-button>
        </div>
      </template>

      <el-form :inline="true" :model="searchForm">
        <el-form-item label="分类">
          <el-select v-model="searchForm.category" placeholder="全部" clearable>
            <el-option label="学术问题" value="academic" />
            <el-option label="生活问题" value="life" />
            <el-option label="就业问题" value="career" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="搜索问题内容"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchQuestions">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table v-loading="loading" :data="questions" stripe style="margin-top: 20px">
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
        <el-table-column prop="ask_count" label="提问次数" width="100" />
        <el-table-column prop="answer_count" label="回答次数" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
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
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="loadQuestions"
        @current-change="loadQuestions"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import { chatApi } from '@/api/chat'

const loading = ref(false)
const questions = ref<any[]>([])
const searchForm = ref({
  category: '',
  keyword: ''
})
const pagination = ref({
  page: 1,
  size: 20,
  total: 0
})

const loadQuestions = async () => {
  loading.value = true
  try {
    const params: any = {
      skip: (pagination.value.page - 1) * pagination.value.size,
      limit: pagination.value.size
    }
    // 只有当 category 不为空时才添加
    if (searchForm.value.category) {
      params.category = searchForm.value.category
    }
    const response = await chatApi.getQuestions(params)
    questions.value = response
    pagination.value.total = response.length
  } catch (error: any) {
    console.error('加载问答失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    loading.value = false
  }
}

const searchQuestions = () => {
  pagination.value.page = 1
  loadQuestions()
}

const resetSearch = () => {
  searchForm.value = {
    category: '',
    keyword: ''
  }
  pagination.value.page = 1
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

const exportQuestions = () => {
  ElMessage.info('导出功能开发中')
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

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.questions-management {
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