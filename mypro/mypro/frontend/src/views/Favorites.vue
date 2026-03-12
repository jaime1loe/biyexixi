<template>
  <div class="favorites-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title">我的收藏</span>
          <el-button type="primary" size="small" @click="loadFavorites">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <div v-loading="loading">
        <el-empty v-if="favorites.length === 0 && !loading" description="暂无收藏的问题" />

        <el-table v-else :data="favorites" stripe style="width: 100%">
          <el-table-column prop="question" label="问题" min-width="300">
            <template #default="{ row }">
              <div class="question-text">{{ row.question }}</div>
            </template>
          </el-table-column>

          <el-table-column prop="answer" label="回答" min-width="400">
            <template #default="{ row }">
              <div class="answer-text">{{ row.answer }}</div>
            </template>
          </el-table-column>

          <el-table-column prop="created_at" label="收藏时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" link size="small" @click="viewDetail(row)">
                查看详情
              </el-button>
              <el-button type="danger" link size="small" @click="handleRemove(row.id)">
                取消收藏
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 查看详情对话框 -->
    <el-dialog v-model="dialogVisible" title="问题详情" width="60%">
      <div v-if="currentFavorite" class="detail-content">
        <div class="detail-item">
          <span class="label">问题：</span>
          <span class="value">{{ currentFavorite.question }}</span>
        </div>
        <el-divider />
        <div class="detail-item">
          <span class="label">回答：</span>
          <div class="value answer-content">{{ currentFavorite.answer }}</div>
        </div>
        <el-divider />
        <div class="detail-item">
          <span class="label">收藏时间：</span>
          <span class="value">{{ formatDate(currentFavorite.created_at) }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { favoritesApi } from '@/api/favorites'
import type { FavoriteResponse } from '@/api/favorites'

const router = useRouter()
const loading = ref(false)
const favorites = ref<FavoriteResponse[]>([])
const dialogVisible = ref(false)
const currentFavorite = ref<FavoriteResponse | null>(null)

const loadFavorites = async () => {
  loading.value = true
  try {
    const response = await favoritesApi.getAll()
    favorites.value = response
  } catch (error: any) {
    console.error('加载收藏失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载收藏失败')
  } finally {
    loading.value = false
  }
}

const viewDetail = (favorite: FavoriteResponse) => {
  currentFavorite.value = favorite
  dialogVisible.value = true
}

const handleRemove = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏这个问题吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await favoritesApi.remove(id)
    ElMessage.success('已取消收藏')
    await loadFavorites()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('取消收藏失败:', error)
      ElMessage.error(error.response?.data?.detail || '取消收藏失败')
    }
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.favorites-container {
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

.question-text {
  font-weight: 500;
  color: #303133;
}

.answer-text {
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.detail-content {
  padding: 10px 0;
}

.detail-item {
  margin-bottom: 20px;
}

.detail-item .label {
  font-weight: 600;
  color: #303133;
  margin-right: 10px;
}

.detail-item .value {
  color: #606266;
  line-height: 1.6;
}

.answer-content {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
