<template>
  <div class="campus-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title">校园服务</span>
        </div>
      </template>

      <div class="campus-grid">
        <!-- 空教室查询 -->
        <div class="campus-item" @click="navigateToEmptyClassroom">
          <el-icon size="48" color="#409eff"><School /></el-icon>
          <h3>空教室查询</h3>
          <p>实时查看空闲教室</p>
        </div>

        <!-- 成绩查询 -->
        <div class="campus-item" @click="navigateToGrades">
          <el-icon size="48" color="#67c23a"><Document /></el-icon>
          <h3>成绩查询</h3>
          <p>查看各科考试成绩</p>
        </div>

        <!-- 图书馆 -->
        <div class="campus-item" @click="navigateToLibrary">
          <el-icon size="48" color="#e6a23c"><Reading /></el-icon>
          <h3>图书馆</h3>
          <p>馆藏书籍与座位查询</p>
        </div>

        <!-- 通知公告 -->
        <div class="campus-item" @click="navigateToNotifications">
          <el-icon size="48" color="#f56c6c"><Bell /></el-icon>
          <h3>通知公告</h3>
          <p>查看学校最新通知</p>
        </div>
      </div>
    </el-card>

    <!-- 空教室查询对话框 -->
    <el-dialog v-model="emptyClassroomVisible" title="空教室查询" width="70%">
      <el-form :inline="true" class="search-form">
        <el-form-item label="教学楼">
          <el-select v-model="searchForm.building" placeholder="请选择教学楼">
            <el-option label="第一教学楼" value="A" />
            <el-option label="第二教学楼" value="B" />
            <el-option label="第三教学楼" value="C" />
            <el-option label="综合楼" value="D" />
          </el-select>
        </el-form-item>
        <el-form-item label="星期">
          <el-select v-model="searchForm.day" placeholder="请选择星期">
            <el-option label="周一" value="1" />
            <el-option label="周二" value="2" />
            <el-option label="周三" value="3" />
            <el-option label="周四" value="4" />
            <el-option label="周五" value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="节次">
          <el-select v-model="searchForm.section" placeholder="请选择节次">
            <el-option label="第1-2节" value="1-2" />
            <el-option label="第3-4节" value="3-4" />
            <el-option label="第5-6节" value="5-6" />
            <el-option label="第7-8节" value="7-8" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchEmptyClassroom">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table v-loading="classroomLoading" :data="emptyClassrooms" stripe>
        <el-table-column prop="room_number" label="教室号" width="120" />
        <el-table-column prop="building" label="教学楼" width="120" />
        <el-table-column prop="capacity" label="容量" width="100" />
        <el-table-column prop="equipment" label="设备" />
        <el-table-column label="状态" width="100">
          <template #default>
            <el-tag type="success">空闲</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 成绩查询对话框 -->
    <el-dialog v-model="gradesVisible" title="成绩查询" width="80%">
      <el-table v-loading="gradesLoading" :data="grades" stripe>
        <el-table-column prop="semester" label="学期" width="120" />
        <el-table-column prop="course_name" label="课程名称" min-width="200" />
        <el-table-column prop="credit" label="学分" width="80" />
        <el-table-column prop="score" label="成绩" width="100">
          <template #default="{ row }">
            <el-tag :type="getScoreType(row.score)">{{ row.score }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="gpa" label="绩点" width="80" />
        <el-table-column prop="remark" label="备注" />
      </el-table>
    </el-dialog>

    <!-- 图书馆对话框 -->
    <el-dialog v-model="libraryVisible" title="图书馆" width="80%">
      <el-tabs v-model="libraryTab">
        <el-tab-pane label="书籍检索" name="books">
          <el-form :inline="true">
            <el-form-item label="关键词">
              <el-input v-model="bookSearchForm.keyword" placeholder="输入书名或作者" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchBooks">搜索</el-button>
            </el-form-item>
          </el-form>
          <el-table v-loading="booksLoading" :data="books" stripe>
            <el-table-column prop="title" label="书名" min-width="200" />
            <el-table-column prop="author" label="作者" width="120" />
            <el-table-column prop="isbn" label="ISBN" width="150" />
            <el-table-column prop="location" label="位置" width="150" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === '可借' ? 'success' : 'danger'">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="座位查询" name="seats">
          <el-alert title="图书馆座位实时查询功能" type="info" :closable="false" />
          <div class="seat-info">
            <el-statistic title="剩余座位" :value="librarySeats.available" />
            <el-statistic title="总座位" :value="librarySeats.total" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 通知公告对话框 -->
    <el-dialog v-model="notificationsVisible" title="通知公告" width="70%">
      <el-table v-loading="notificationsLoading" :data="notifications" stripe>
        <el-table-column prop="title" label="标题" min-width="250">
          <template #default="{ row }">
            <el-link type="primary" @click="viewNotification(row)">{{ row.title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getNotificationType(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_date" label="发布日期" width="180" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { School, Document, Reading, Bell } from '@element-plus/icons-vue'
import { campusApi } from '@/api/campus'
import { notificationsApi } from '@/api/notifications'

// 弹窗显示状态
const emptyClassroomVisible = ref(false)
const gradesVisible = ref(false)
const libraryVisible = ref(false)
const notificationsVisible = ref(false)

// 加载状态
const classroomLoading = ref(false)
const gradesLoading = ref(false)
const booksLoading = ref(false)
const notificationsLoading = ref(false)

// 数据
const emptyClassrooms = ref<any[]>([])
const grades = ref<any[]>([])
const books = ref<any[]>([])
const notifications = ref<any[]>([])

// 搜索表单
const searchForm = ref({
  building: '',
  day: '',
  section: ''
})

const bookSearchForm = ref({
  keyword: ''
})

const libraryTab = ref('books')
const librarySeats = ref({
  available: 156,
  total: 500
})

// 导航方法
const navigateToEmptyClassroom = () => {
  emptyClassroomVisible.value = true
}

const navigateToGrades = () => {
  gradesVisible.value = true
  loadGrades()
}

const navigateToLibrary = () => {
  libraryVisible.value = true
}

const navigateToNotifications = () => {
  notificationsVisible.value = true
  loadNotifications()
}

// 查询方法
const searchEmptyClassroom = async () => {
  if (!searchForm.value.building || !searchForm.value.day || !searchForm.value.section) {
    ElMessage.warning('请填写完整的查询条件')
    return
  }

  classroomLoading.value = true
  try {
    const response = await campusApi.getEmptyClassroom(searchForm.value)
    emptyClassrooms.value = response
  } catch (error: any) {
    console.error('查询空教室失败:', error)
    ElMessage.error(error.response?.data?.detail || '查询失败')
  } finally {
    classroomLoading.value = false
  }
}

const loadGrades = async () => {
  gradesLoading.value = true
  try {
    const response = await campusApi.getGrades()
    grades.value = response
  } catch (error: any) {
    console.error('加载成绩失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    gradesLoading.value = false
  }
}

const searchBooks = async () => {
  if (!bookSearchForm.value.keyword) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  booksLoading.value = true
  try {
    const response = await campusApi.searchBooks(bookSearchForm.value.keyword)
    books.value = response
  } catch (error: any) {
    console.error('搜索书籍失败:', error)
    ElMessage.error(error.response?.data?.detail || '搜索失败')
  } finally {
    booksLoading.value = false
  }
}

const loadNotifications = async () => {
  notificationsLoading.value = true
  try {
    const response = await notificationsApi.getAll()
    notifications.value = response
  } catch (error: any) {
    console.error('加载通知失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    notificationsLoading.value = false
  }
}

const viewNotification = (notification: any) => {
  ElMessage.info(notification.content || '暂无详细内容')
}

// 辅助方法
const getScoreType = (score: number) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  if (score >= 60) return 'info'
  return 'danger'
}

const getNotificationType = (type: string) => {
  const typeMap: Record<string, string> = {
    '通知': 'info',
    '公告': 'primary',
    '紧急': 'danger',
    '活动': 'success'
  }
  return typeMap[type] || 'info'
}

onMounted(() => {
  // 页面加载时可以预加载一些数据
})
</script>

<style scoped>
.campus-container {
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

.campus-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.campus-item {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border: 1px solid #ebeef5;
  border-radius: 12px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.campus-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.campus-item h3 {
  margin: 15px 0 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.campus-item p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.search-form {
  margin-bottom: 20px;
}

.seat-info {
  display: flex;
  justify-content: space-around;
  padding: 40px 0;
  background: #f5f7fa;
  border-radius: 8px;
  margin-top: 20px;
}
</style>
