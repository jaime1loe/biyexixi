<template>
  <div class="history-container">
    <div class="history-header">
      <h3><el-icon><Clock /></el-icon>问答历史</h3>
      <el-button type="primary" :icon="Download" @click="handleExport">导出记录</el-button>
    </div>

    <div class="history-filter">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索问题关键词"
        :prefix-icon="Search"
        style="width: 300px"
        @input="handleSearch"
      />
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        @change="handleSearch"
      />
    </div>

    <div class="history-list">
      <div v-loading="loading">
        <div
          v-for="item in filteredHistory"
          :key="item.id"
          class="history-item"
        >
          <div class="item-header">
            <div class="question">
              <el-icon><ChatDotRound /></el-icon>
              <span>{{ item.question }}</span>
            </div>
            <div class="item-actions">
              <el-tag v-if="item.category" size="small">{{ item.category }}</el-tag>
              <el-button link type="primary" :icon="View" @click="handleView(item)">查看</el-button>
            </div>
          </div>
          <div class="item-content">
            <div class="answer">{{ item.answer || '等待回答...' }}</div>
            <div class="item-footer">
              <span class="time">{{ formatTime(item.created_at) }}</span>
            </div>
          </div>
        </div>

        <el-empty v-if="!loading && filteredHistory.length === 0" description="暂无历史记录" />
      </div>
    </div>

    <div class="history-pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Download, Search, ChatDotRound, View, Delete } from '@element-plus/icons-vue'
import { chatApi, Question } from '@/api/chat'

interface HistoryItem {
  id: number
  question: string
  answer?: string
  created_at: string
  category?: string
}

const searchKeyword = ref('')
const dateRange = ref<[Date, Date] | null>(null)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const historyList = ref<HistoryItem[]>([])

const filteredHistory = computed(() => {
  let result = historyList.value

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(item =>
      item.question.toLowerCase().includes(keyword) ||
      (item.answer && item.answer.toLowerCase().includes(keyword))
    )
  }

  if (dateRange.value) {
    const [start, end] = dateRange.value
    result = result.filter(item => {
      const time = new Date(item.created_at).getTime()
      return time >= start.getTime() && time <= end.getTime()
    })
  }

  return result
})

async function loadHistory() {
  loading.value = true
  try {
    const data = await chatApi.getMyQuestions({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    historyList.value = data
    total.value = data.length
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '加载历史记录失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
}

function handlePageChange() {
  loadHistory()
}

function handleView(item: HistoryItem) {
  ElMessageBox.alert(item.answer || '暂无回答', item.question, {
    confirmButtonText: '关闭'
  })
}

async function handleDelete(item: HistoryItem) {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.success('删除功能需要后端支持')
  } catch {
    // 用户取消
  }
}

function handleExport() {
  ElMessage.success('导出功能开发中...')
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
  loadHistory()
})
</script>

<style scoped>
.history-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.history-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.history-filter {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.history-list {
  margin-bottom: 20px;
}

.history-item {
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  transition: all 0.3s;
  background: #fafafa;
}

.history-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.question {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.item-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.item-content {
  margin-left: 28px;
}

.answer {
  padding: 12px;
  background: #fff;
  border-radius: 6px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 8px;
}

.item-footer {
  display: flex;
  justify-content: flex-end;
}

.time {
  font-size: 12px;
  color: #909399;
}

.history-pagination {
  display: flex;
  justify-content: center;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}
</style>
