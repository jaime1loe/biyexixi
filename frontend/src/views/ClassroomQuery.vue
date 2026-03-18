<template>
  <div class="classroom-query-container">
    <div class="page-header">
      <h2><el-icon><School /></el-icon>空教室查询</h2>
      <p class="subtitle">查询指定时间段内的空闲教室</p>
    </div>

    <!-- 查询条件 -->
    <el-card shadow="hover" class="filter-card">
      <el-form :inline="true" :model="queryForm" label-width="80px">
        <el-form-item label="星期">
          <el-select v-model="queryForm.day_of_week" placeholder="请选择星期" style="width: 120px">
            <el-option
              v-for="day in weekdays"
              :key="day.value"
              :label="day.label"
              :value="day.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="节次">
          <el-select v-model="queryForm.period" placeholder="请选择节次" style="width: 140px">
            <el-option
              v-for="period in periods"
              :key="period.value"
              :label="`${period.label} (${period.time})`"
              :value="period.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="周次">
          <el-input-number
            v-model="queryForm.week"
            :min="1"
            :max="18"
            style="width: 120px"
          />
        </el-form-item>

        <el-form-item label="学期">
          <el-select v-model="queryForm.semester" placeholder="请选择学期" style="width: 180px">
            <el-option label="2024-2025-2" value="2024-2025-2" />
          </el-select>
        </el-form-item>

        <el-form-item label="教学楼">
          <el-select v-model="queryForm.building" placeholder="全部" clearable style="width: 120px">
            <el-option
              v-for="building in buildings"
              :key="building"
              :label="building"
              :value="building"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="教室类型">
          <el-select v-model="queryForm.room_type" placeholder="全部" clearable style="width: 120px">
            <el-option label="普通" value="普通" />
            <el-option label="多媒体" value="多媒体" />
            <el-option label="实验室" value="实验室" />
          </el-select>
        </el-form-item>

        <el-form-item label="最小容量">
          <el-input-number
            v-model="queryForm.min_capacity"
            :min="0"
            :step="5"
            style="width: 120px"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleSearch" :loading="loading">
            查询
          </el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 查询结果 -->
    <el-card shadow="hover" class="result-card">
      <template #header>
        <div class="card-header">
          <span><el-icon><List /></el-icon>查询结果</span>
          <el-tag type="success" v-if="!loading && classrooms.length > 0">
            共 {{ classrooms.length }} 间空闲教室
          </el-tag>
        </div>
      </template>

      <el-empty v-if="!loading && classrooms.length === 0" description="未找到符合条件的空闲教室" />

      <div v-loading="loading" class="classroom-list">
        <div
          v-for="classroom in classrooms"
          :key="classroom.id"
          class="classroom-item"
          @click="handleClassroomClick(classroom)"
        >
          <div class="classroom-icon">
            <el-icon size="32"><Monitor /></el-icon>
          </div>
          <div class="classroom-info">
            <div class="classroom-name">
              {{ classroom.building }}{{ classroom.room_number }}
              <el-tag :type="getRoomTypeTagType(classroom.room_type)" size="small">
                {{ classroom.room_type }}
              </el-tag>
            </div>
            <div class="classroom-details">
              <el-icon><User /></el-icon>
              容量: {{ classroom.capacity }}人
              <span v-if="classroom.equipment" class="equipment">
                <el-icon><Setting /></el-icon>
                {{ classroom.equipment }}
              </span>
            </div>
            <div class="classroom-floor">
              <el-icon><OfficeBuilding /></el-icon>
              {{ classroom.floor }}楼
            </div>
          </div>
          <div class="classroom-actions">
            <el-button type="primary" size="small" @click.stop="handleClassroomClick(classroom)">
              查看详情
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 教室详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`${selectedClassroom?.building}${selectedClassroom?.room_number} - 教室详情`"
      width="600px"
    >
      <div v-if="selectedClassroom" class="classroom-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="教学楼">{{ selectedClassroom.building }}</el-descriptions-item>
          <el-descriptions-item label="教室号">{{ selectedClassroom.room_number }}</el-descriptions-item>
          <el-descriptions-item label="容量">{{ selectedClassroom.capacity }}人</el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag :type="getRoomTypeTagType(selectedClassroom.room_type)">
              {{ selectedClassroom.room_type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="楼层">{{ selectedClassroom.floor }}楼</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag type="success">可用</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="设备" :span="2">
            {{ selectedClassroom.equipment || '无' }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>该教室课表</el-divider>

        <el-table :data="scheduleList" stripe v-loading="scheduleLoading" max-height="300">
          <el-table-column prop="day_of_week" label="星期" width="80">
            <template #default="{ row }">
              {{ getWeekdayLabel(row.day_of_week) }}
            </template>
          </el-table-column>
          <el-table-column prop="period" label="节次" width="100">
            <template #default="{ row }">
              第{{ row.period }}节
            </template>
          </el-table-column>
          <el-table-column prop="class_name" label="班级" />
          <el-table-column label="课程">
            <template #default="{ row }">
              {{ row.course?.course_name }}
            </template>
          </el-table-column>
          <el-table-column label="周次" width="120">
            <template #default="{ row }">
              {{ row.week_start }}-{{ row.week_end }}周
            </template>
          </el-table-column>
        </el-table>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  School,
  Search,
  Refresh,
  List,
  Monitor,
  User,
  Setting,
  OfficeBuilding
} from '@element-plus/icons-vue'
import { scheduleApi, Classroom, Schedule } from '@/api/schedule'

const weekdays = ref<Array<{ value: number; label: string }>>([])
const periods = ref<Array<{ value: number; label: string; time: string }>>([])
const buildings = ref<string[]>([])

const queryForm = ref({
  day_of_week: 1,
  period: 1,
  week: 1,
  semester: '2024-2025-2',
  building: '',
  room_type: '',
  min_capacity: 0
})

const classrooms = ref<Classroom[]>([])
const loading = ref(false)

const detailDialogVisible = ref(false)
const selectedClassroom = ref<Classroom | null>(null)
const scheduleList = ref<Schedule[]>([])
const scheduleLoading = ref(false)

// 加载基础数据
async function loadBaseData() {
  try {
    const [weekdaysRes, periodsRes, buildingsRes] = await Promise.all([
      scheduleApi.getWeekdays(),
      scheduleApi.getPeriods(),
      scheduleApi.getBuildings()
    ])

    weekdays.value = weekdaysRes.days
    periods.value = periodsRes.periods
    buildings.value = buildingsRes.buildings

    // 设置默认值
    queryForm.value.day_of_week = getTodayWeekday()
    queryForm.value.period = getCurrentPeriod()
  } catch (error) {
    ElMessage.error('加载基础数据失败')
  }
}

// 获取今天是星期几（1-7）
function getTodayWeekday(): number {
  const day = new Date().getDay()
  return day === 0 ? 7 : day
}

// 获取当前节次（根据时间估算）
function getCurrentPeriod(): number {
  const hour = new Date().getHours()
  if (hour < 10) return 1
  if (hour < 12) return 2
  if (hour < 16) return 3
  if (hour < 19) return 4
  return 5
}

// 查询空教室
async function handleSearch() {
  loading.value = true
  try {
    classrooms.value = await scheduleApi.getAvailableClassrooms(queryForm.value)
    ElMessage.success(`找到 ${classrooms.value.length} 间空闲教室`)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '查询失败')
    classrooms.value = []
  } finally {
    loading.value = false
  }
}

// 重置查询条件
function handleReset() {
  queryForm.value = {
    day_of_week: getTodayWeekday(),
    period: getCurrentPeriod(),
    week: 1,
    semester: '2024-2025-2',
    building: '',
    room_type: '',
    min_capacity: 0
  }
  classrooms.value = []
}

// 查看教室详情
async function handleClassroomClick(classroom: Classroom) {
  selectedClassroom.value = classroom
  detailDialogVisible.value = true
  scheduleLoading.value = true

  try {
    scheduleList.value = await scheduleApi.getClassroomSchedule(
      classroom.id,
      queryForm.value.semester
    )
  } catch (error) {
    ElMessage.error('加载课表失败')
    scheduleList.value = []
  } finally {
    scheduleLoading.value = false
  }
}

// 获取教室类型标签颜色
function getRoomTypeTagType(roomType: string): string {
  const typeMap: Record<string, string> = {
    '普通': '',
    '多媒体': 'primary',
    '实验室': 'success'
  }
  return typeMap[roomType] || ''
}

// 获取星期标签
function getWeekdayLabel(day: number): string {
  const item = weekdays.value.find(w => w.value === day)
  return item?.label || ''
}

onMounted(() => {
  loadBaseData()
})
</script>

<style scoped>
.classroom-query-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.filter-card {
  margin-bottom: 20px;
}

.result-card {
  min-height: 400px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-header span {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.classroom-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
  padding: 10px 0;
}

.classroom-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.classroom-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.classroom-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.classroom-info {
  flex: 1;
  min-width: 0;
}

.classroom-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.classroom-details {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.classroom-details .equipment {
  display: flex;
  align-items: center;
  gap: 4px;
}

.classroom-floor {
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.classroom-actions {
  flex-shrink: 0;
}

.classroom-detail {
  padding: 10px 0;
}
</style>
