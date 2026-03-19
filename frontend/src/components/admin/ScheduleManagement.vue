<template>
  <div class="schedule-management">
    <div class="page-header">
      <h2>排课管理</h2>
      <el-button type="primary" @click="showAddDialog">新增排课</el-button>
    </div>

    <!-- 筛选区域 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="学期">
          <el-select v-model="filterForm.semester" placeholder="选择学期">
            <el-option label="2024-2025-1" value="2024-2025-1" />
            <el-option label="2024-2025-2" value="2024-2025-2" />
            <el-option label="2025-2026-1" value="2025-2026-1" />
            <el-option label="2025-2026-2" value="2025-2026-2" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadSchedules">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 列表 -->
    <el-table :data="schedules" v-loading="loading" border stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="course.course_code" label="课程代码" width="150" />
      <el-table-column prop="course.course_name" label="课程名称" width="200" />
      <el-table-column prop="classroom.building" label="教学楼" width="100" />
      <el-table-column prop="classroom.room_number" label="教室号" width="100" />
      <el-table-column label="星期" width="100">
        <template #default="{ row }">{{ weekdayMap[row.day_of_week] }}</template>
      </el-table-column>
      <el-table-column prop="period" label="节次" width="80" />
      <el-table-column label="周次" width="120">
        <template #default="{ row }">{{ row.week_start }}-{{ row.week_end }}周</template>
      </el-table-column>
      <el-table-column prop="semester" label="学期" width="120" />
      <el-table-column prop="class_name" label="班级" width="120" />
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑排课' : '新增排课'"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="学期" prop="semester">
          <el-select v-model="form.semester" placeholder="选择学期">
            <el-option label="2024-2025-1" value="2024-2025-1" />
            <el-option label="2024-2025-2" value="2024-2025-2" />
            <el-option label="2025-2026-1" value="2025-2026-1" />
            <el-option label="2025-2026-2" value="2025-2026-2" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程" prop="course_id">
          <el-select v-model="form.course_id" placeholder="选择课程" filterable>
            <el-option
              v-for="course in courses"
              :key="course.id"
              :label="`${course.course_code} - ${course.course_name}`"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="教室" prop="classroom_id">
          <el-select v-model="form.classroom_id" placeholder="选择教室" filterable>
            <el-option
              v-for="classroom in classrooms"
              :key="classroom.id"
              :label="`${classroom.building}${classroom.room_number} (容量${classroom.capacity}人)`"
              :value="classroom.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="星期" prop="day_of_week">
          <el-select v-model="form.day_of_week" placeholder="选择星期">
            <el-option label="周一" :value="1" />
            <el-option label="周二" :value="2" />
            <el-option label="周三" :value="3" />
            <el-option label="周四" :value="4" />
            <el-option label="周五" :value="5" />
            <el-option label="周六" :value="6" />
            <el-option label="周日" :value="7" />
          </el-select>
        </el-form-item>
        <el-form-item label="节次" prop="period">
          <el-select v-model="form.period" placeholder="选择节次">
            <el-option label="第1节" :value="1" />
            <el-option label="第2节" :value="2" />
            <el-option label="第3节" :value="3" />
            <el-option label="第4节" :value="4" />
            <el-option label="第5节" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="起始周" prop="week_start">
          <el-input-number v-model="form.week_start" :min="1" :max="25" />
        </el-form-item>
        <el-form-item label="结束周" prop="week_end">
          <el-input-number v-model="form.week_end" :min="1" :max="25" />
        </el-form-item>
        <el-form-item label="班级" prop="class_name">
          <el-input v-model="form.class_name" placeholder="如: 计科2101" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import * as scheduleApi from '@/api/schedule'
import * as courseApi from '@/api/course'

const loading = ref(false)
const submitting = ref(false)
const schedules = ref<any[]>([])
const courses = ref<any[]>([])
const classrooms = ref<any[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()

const filterForm = ref({
  semester: '2024-2025-2'
})

const form = ref({
  course_id: undefined as number | undefined,
  classroom_id: undefined as number | undefined,
  day_of_week: undefined as number | undefined,
  period: undefined as number | undefined,
  week_start: 1,
  week_end: 18,
  semester: '2024-2025-2',
  class_name: ''
})

const weekdayMap: Record<number, string> = {
  1: '周一',
  2: '周二',
  3: '周三',
  4: '周四',
  5: '周五',
  6: '周六',
  7: '周日'
}

const rules = {
  course_id: [{ required: true, message: '请选择课程', trigger: 'change' }],
  classroom_id: [{ required: true, message: '请选择教室', trigger: 'change' }],
  day_of_week: [{ required: true, message: '请选择星期', trigger: 'change' }],
  period: [{ required: true, message: '请选择节次', trigger: 'change' }],
  semester: [{ required: true, message: '请选择学期', trigger: 'change' }]
}

const loadSchedules = async () => {
  try {
    loading.value = true
    const response = await scheduleApi.getSchedules({ semester: filterForm.value.semester })
    schedules.value = Array.isArray(response) ? response : []
  } catch (error: any) {
    console.error('加载排课失败:', error)
    schedules.value = []
    ElMessage.error('加载排课失败')
  } finally {
    loading.value = false
  }
}

const loadCourses = async () => {
  try {
    const response = await scheduleApi.getCourses()
    courses.value = Array.isArray(response) ? response : []
  } catch (error: any) {
    console.error('加载课程列表失败:', error)
    courses.value = []
  }
}

const loadClassrooms = async () => {
  try {
    const response = await scheduleApi.getClassrooms()
    classrooms.value = Array.isArray(response) ? response : []
  } catch (error: any) {
    console.error('加载教室列表失败:', error)
    classrooms.value = []
  }
}

const showAddDialog = () => {
  isEdit.value = false
  editingId.value = null
  form.value = {
    course_id: undefined,
    classroom_id: undefined,
    day_of_week: undefined,
    period: undefined,
    week_start: 1,
    week_end: 18,
    semester: filterForm.value.semester,
    class_name: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  isEdit.value = true
  editingId.value = row.id
  form.value = {
    course_id: row.course_id,
    classroom_id: row.classroom_id,
    day_of_week: row.day_of_week,
    period: row.period,
    week_start: row.week_start,
    week_end: row.week_end,
    semester: row.semester,
    class_name: row.class_name || ''
  }
  dialogVisible.value = true
}

const handleDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条排课记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await scheduleApi.deleteSchedule(row.id)
    ElMessage.success('删除成功')
    loadSchedules()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (isEdit.value) {
      await scheduleApi.updateSchedule(editingId.value!, form.value)
      ElMessage.success('更新成功')
    } else {
      await scheduleApi.createSchedule(form.value)
      ElMessage.success('创建成功')
    }

    dialogVisible.value = false
    loadSchedules()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('提交失败')
    }
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}

const resetFilter = () => {
  filterForm.value = {
    semester: '2024-2025-2'
  }
  loadSchedules()
}

onMounted(() => {
  loadSchedules()
  loadCourses()
  loadClassrooms()
})
</script>

<style scoped>
.schedule-management {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.filter-card {
  margin-bottom: 16px;
}

.filter-form {
  margin: 0;
}
</style>
