<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h3><el-icon><DataAnalysis /></el-icon>数据统计看板</h3>
      <div class="header-actions">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          size="default"
          @change="handleDateChange"
        />
        <el-button type="primary" :icon="Refresh" @click="handleRefresh">刷新</el-button>
      </div>
    </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <div class="stat-card primary">
          <div class="stat-icon">
            <el-icon><ChatDotRound /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.totalQuestions }}</div>
            <div class="stat-label">总提问数</div>
            <div class="stat-trend" :class="{ up: stats.todayQuestions > 0 }">
              <el-icon v-if="stats.todayQuestions > 0"><CaretTop /></el-icon>
              <el-icon v-else><CaretBottom /></el-icon>
              今日新增 {{ stats.todayQuestions }}
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card success">
          <div class="stat-icon">
            <el-icon><DocumentCopy /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.totalAnswers }}</div>
            <div class="stat-label">总回答数</div>
            <div class="stat-trend up">
              <el-icon><CaretTop /></el-icon>
              回答率 98.5%
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card warning">
          <div class="stat-icon">
            <el-icon><Star /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.avgRating }}</div>
            <div class="stat-label">平均评分</div>
            <div class="stat-trend up">
              <el-icon><CaretTop /></el-icon>
              满意率 92.3%
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card info">
          <div class="stat-icon">
            <el-icon><User /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">128</div>
            <div class="stat-label">活跃用户</div>
            <div class="stat-trend up">
              <el-icon><CaretTop /></el-icon>
              环比 +12.5%
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><TrendCharts /></el-icon>提问趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <div class="bar-chart">
              <div
                v-for="(item, index) in trendData"
                :key="index"
                class="bar-item"
              >
                <div
                  class="bar"
                  :style="{ height: `${item.value * 2}px`, background: item.color }"
                ></div>
                <div class="bar-label">{{ item.label }}</div>
                <div class="bar-value">{{ item.value }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><PieChart /></el-icon>问题分类</span>
            </div>
          </template>
          <div class="pie-chart" v-loading="loading">
            <div class="pie-legend" v-if="categoryData.length > 0">
              <div
                v-for="(item, index) in categoryData"
                :key="index"
                class="legend-item"
              >
                <div class="legend-color" :style="{ background: item.color }"></div>
                <span class="legend-label">{{ item.name }}</span>
                <span class="legend-value">{{ item.value }}%</span>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="bottom-row">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><Trophy /></el-icon>热门问题 TOP 5</span>
            </div>
          </template>
          <div class="hot-list">
            <div
              v-for="(item, index) in stats.popularQuestions"
              :key="index"
              class="hot-item"
            >
              <div class="hot-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</div>
              <div class="hot-content">
                <div class="hot-question">{{ item.question }}</div>
                <div class="hot-count">提问 {{ item.count }} 次</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span><el-icon><Clock /></el-icon>最近活动</span>
            </div>
          </template>
          <div class="activity-list">
            <div
              v-for="(item, index) in stats.recentActivity"
              :key="index"
              class="activity-item"
            >
              <div class="activity-icon">
                <el-icon v-if="item.action.includes('提问')"><ChatDotRound /></el-icon>
                <el-icon v-else-if="item.action.includes('评分')"><Star /></el-icon>
                <el-icon v-else><Document /></el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-text">{{ item.action }}</div>
                <div class="activity-time">{{ item.time }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  DataAnalysis,
  Refresh,
  ChatDotRound,
  DocumentCopy,
  Star,
  User,
  TrendCharts,
  PieChart,
  Trophy,
  Clock,
  CaretTop,
  CaretBottom
} from '@element-plus/icons-vue'
import { statisticsApi, StatisticsOverview, DailyStatistics, CategoryStatistics } from '@/api/dashboard'

interface DashboardStats {
  totalQuestions: number
  totalAnswers: number
  avgRating: number
  todayQuestions: number
  popularQuestions: Array<{ question: string; count: number }>
  recentActivity: Array<{ time: string; action: string }>
}

const dateRange = ref<[Date, Date] | null>(null)
const loading = ref(false)

const stats = ref<DashboardStats>({
  totalQuestions: 0,
  totalAnswers: 0,
  avgRating: 0,
  todayQuestions: 0,
  popularQuestions: [],
  recentActivity: []
})

const overview = ref<StatisticsOverview>({
  question_count: 0,
  answer_count: 0,
  ask_count: 0,
  user_count: 0,
  knowledge_count: 0,
  avg_rating: 0,
  today_questions: 0,
  today_users: 0,
  week_questions: 0
})

const dailyStats = ref<DailyStatistics[]>([])

const categoryStats = ref<CategoryStatistics>({ categories: [] })

const trendData = ref<Array<{ label: string; value: number; color: string }>>([])

const categoryData = ref<Array<{ name: string; value: number; color: string }>>([])

const categoryColors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399', '#9c27b0', '#ff9800']

async function loadOverview() {
  loading.value = true
  try {
    const data = await statisticsApi.getOverview()
    overview.value = data
    stats.value.totalQuestions = data.question_count
    stats.value.totalAnswers = data.answer_count
    stats.value.avgRating = data.avg_rating
    stats.value.todayQuestions = data.today_questions
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '数据加载失败')
  } finally {
    loading.value = false
  }
}

async function loadDailyStats() {
  try {
    const data = await statisticsApi.getDaily(7)
    dailyStats.value = data
    trendData.value = data.map((item, index) => ({
      label: getWeekDay(item.date),
      value: item.question_count,
      color: isWeekend(index) ? '#67c23a' : '#409eff'
    }))
  } catch (error) {
    console.error('加载每日统计失败:', error)
  }
}

async function loadCategoryStats() {
  try {
    const data = await statisticsApi.getCategoryStats()
    categoryStats.value = data
    const total = data.categories.reduce((sum, item) => sum + item.count, 0)
    categoryData.value = data.categories.map((item, index) => ({
      name: item.category,
      value: total > 0 ? Math.round((item.count / total) * 100) : 0,
      color: categoryColors[index % categoryColors.length]
    }))
  } catch (error) {
    console.error('加载分类统计失败:', error)
  }
}

async function loadTopQuestions() {
  try {
    const data = await statisticsApi.getTopQuestions(5)
    stats.value.popularQuestions = data.map(item => ({
      question: item.question,
      count: item.ask_count || 1
    }))
  } catch (error) {
    console.error('加载热门问题失败:', error)
  }
}

async function loadStats() {
  await Promise.all([
    loadOverview(),
    loadDailyStats(),
    loadCategoryStats(),
    loadTopQuestions()
  ])
}

function handleRefresh() {
  loadStats()
  ElMessage.success('数据已刷新')
}

function handleDateChange() {
  loadStats()
}

function getWeekDay(dateStr: string): string {
  const date = new Date(dateStr)
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return days[date.getDay()]
}

function isWeekend(index: number): boolean {
  // 简单判断：最后两个是周末
  return index >= 5
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.dashboard-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  padding: 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.success {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.stat-card.warning {
  background: linear-gradient(135deg, #e6a23c 0%, #f0c78a 100%);
}

.stat-card.info {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
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

.stat-content {
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

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  margin-top: 8px;
  opacity: 0.85;
}

.stat-trend.up {
  color: #67c23a;
}

.stat-trend:not(.up) {
  color: #f56c6c;
}

.charts-row {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.chart-container {
  height: 280px;
  padding: 20px 0;
}

.bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 100%;
  padding: 0 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 60px;
}

.bar {
  width: 30px;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
}

.bar:hover {
  opacity: 0.8;
  transform: scaleY(1.05);
}

.bar-label {
  font-size: 12px;
  color: #909399;
}

.bar-value {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.pie-chart {
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pie-legend {
  width: 100%;
  padding: 0 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f5f7fa;
}

.legend-item:last-child {
  border-bottom: none;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-label {
  flex: 1;
  margin-left: 12px;
  color: #606266;
}

.legend-value {
  font-weight: 500;
  color: #303133;
}

.hot-list {
  padding: 10px 0;
}

.hot-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f7fa;
}

.hot-item:last-child {
  border-bottom: none;
}

.hot-rank {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #fff;
  font-size: 14px;
}

.hot-rank.rank-1 {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
}

.hot-rank.rank-2 {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
}

.hot-rank.rank-3 {
  background: linear-gradient(135deg, #cd7f32 0%, #daa06d 100%);
}

.hot-rank:not(.rank-1):not(.rank-2):not(.rank-3) {
  background: #e4e7ed;
  color: #909399;
}

.hot-content {
  flex: 1;
}

.hot-question {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.hot-count {
  font-size: 12px;
  color: #909399;
}

.activity-list {
  padding: 10px 0;
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f5f7fa;
}

.activity-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #909399;
}
</style>
