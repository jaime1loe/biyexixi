<template>
  <div class="course-management">
    <div class="page-header">
      <h2>课程管理</h2>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        开设课程
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="学期">
          <el-select v-model="searchForm.semester" placeholder="全部学期" clearable style="width: 150px" @change="loadCourses">
            <el-option label="2024-2025-1" value="2024-2025-1" />
            <el-option label="2024-2025-2" value="2024-2025-2" />
          </el-select>
        </el-form-item>
        <el-form-item label="课程类型">
          <el-select v-model="searchForm.course_type" placeholder="全部类型" clearable style="width: 120px">
            <el-option label="必修" value="必修" />
            <el-option label="选修" value="选修" />
            <el-option label="实践" value="实践" />
          </el-select>
        </el-form-item>
        <el-form-item label="院系">
          <el-input v-model="searchForm.department" placeholder="输入院系" clearable style="width: 150px" />
        </el-form-item>
        <el-form-item label="搜索">
          <el-input v-model="searchForm.search" placeholder="课程名称或代码" clearable style="width: 180px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="Search" @click="loadCourses">查询</el-button>
          <el-button :icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 课程列表 -->
    <el-card class="table-card">
      <el-table v-loading="loading" :data="courses" stripe>
        <el-table-column prop="course_code" label="课程代码" width="120" />
        <el-table-column prop="course_name" label="课程名称" width="200" />
        <el-table-column prop="teacher_name" label="授课教师" width="100" />
        <el-table-column prop="department" label="院系" width="120" />
        <el-table-column prop="course_type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.course_type === '必修' ? 'primary' : 'success'">
              {{ row.course_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="credits" label="学分" width="80" />
        <el-table-column prop="hours" label="学时" width="80" />
        <el-table-column prop="capacity" label="容量" width="80" />
        <el-table-column prop="selection_count" label="选课人数" width="100">
          <template #default="{ row }">
            <el-tag type="info">{{ row.selection_count || 0 }}人</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" :icon="Edit" @click="showEditDialog(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" :icon="Delete" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="loadCourses"
          @size-change="loadCourses"
        />
      </div>
    </el-card>

    <!-- 创建/编辑课程对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="courseForm" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="课程代码" prop="course_code">
          <el-input v-model="courseForm.course_code" placeholder="请输入课程代码" />
        </el-form-item>
        <el-form-item label="课程名称" prop="course_name">
          <el-input v-model="courseForm.course_name" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="授课教师" prop="teacher_id">
          <el-select v-model="courseForm.teacher_id" placeholder="请选择教师" style="width: 100%">
            <el-option
              v-for="teacher in teachers"
              :key="teacher.id"
              :label="`${teacher.real_name} (${teacher.username})`"
              :value="teacher.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="开课院系" prop="department">
          <el-input v-model="courseForm.department" placeholder="请输入开课院系" />
        </el-form-item>
        <el-form-item label="课程类型" prop="course_type">
          <el-radio-group v-model="courseForm.course_type">
            <el-radio value="必修">必修</el-radio>
            <el-radio value="选修">选修</el-radio>
            <el-radio value="实践">实践</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学分" prop="credits">
          <el-input-number
            v-model="courseForm.credits"
            :min="0"
            :max="10"
            :precision="1"
            :step="0.5"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="学时" prop="hours">
          <el-input-number
            v-model="courseForm.hours"
            :min="0"
            :max="200"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="课程容量" prop="capacity">
          <el-input-number
            v-model="courseForm.capacity"
            :min="1"
            :max="500"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
import {
  courseManagementApi,
  CourseManagementRequest,
  CourseManagementResponse,
  Teacher
} from '@/api/courseSelection'

// 数据
const courses = ref<CourseManagementResponse[]>([])
const teachers = ref<Teacher[]>([])
const loading = ref(false)

// 搜索表单
const searchForm = ref({
  semester: '',
  course_type: '',
  department: '',
  search: ''
})

// 分页
const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('开设课程')
const isEdit = ref(false)
const formRef = ref()

// 课程表单
const courseForm = ref<CourseManagementRequest>({
  course_code: '',
  course_name: '',
  teacher_id: 0,
  department: '',
  credits: 3,
  hours: 48,
  course_type: '必修'
})

// 表单验证规则
const formRules = {
  course_code: [
    { required: true, message: '请输入课程代码', trigger: 'blur' }
  ],
  course_name: [
    { required: true, message: '请输入课程名称', trigger: 'blur' }
  ],
  teacher_id: [
    { required: true, message: '请选择授课教师', trigger: 'change' }
  ],
  department: [
    { required: true, message: '请输入开课院系', trigger: 'blur' }
  ],
  course_type: [
    { required: true, message: '请选择课程类型', trigger: 'change' }
  ],
  credits: [
    { required: true, message: '请输入学分', trigger: 'blur' }
  ],
  hours: [
    { required: true, message: '请输入学时', trigger: 'blur' }
  ]
}

// 加载课程列表
const loadCourses = async () => {
  loading.value = true
  try {
    const response = await courseManagementApi.getAllCourses({
      ...searchForm.value,
      skip: (pagination.value.page - 1) * pagination.value.pageSize,
      limit: pagination.value.pageSize
    })
    courses.value = response.courses
    pagination.value.total = response.total
  } catch (error: any) {
    console.error('加载课程失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    loading.value = false
  }
}

// 加载教师列表
const loadTeachers = async () => {
  try {
    teachers.value = await courseManagementApi.getTeachers()
  } catch (error: any) {
    console.error('加载教师列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  }
}

// 显示创建对话框
const showCreateDialog = () => {
  isEdit.value = false
  dialogTitle.value = '开设课程'
  courseForm.value = {
    course_code: '',
    course_name: '',
    teacher_id: 0,
    department: '',
    credits: 3,
    hours: 48,
    course_type: '必修'
  }
  dialogVisible.value = true
}

// 显示编辑对话框
const showEditDialog = (course: CourseManagementResponse) => {
  isEdit.value = true
  dialogTitle.value = '编辑课程'
  courseForm.value = {
    course_code: course.course_code,
    course_name: course.course_name,
    teacher_id: course.teacher_id,
    department: course.department || '',
    credits: course.credits || 3,
    hours: course.hours || 48,
    course_type: course.course_type || '必修'
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch {
    ElMessage.warning('请填写完整信息')
    return
  }

  loading.value = true
  try {
    if (isEdit.value) {
      const courseId = courses.value.find(c =>
        c.course_code === courseForm.value.course_code
      )?.id
      if (courseId) {
        await courseManagementApi.updateCourse(courseId, courseForm.value)
        ElMessage.success('课程更新成功')
      }
    } else {
      await courseManagementApi.createCourse(courseForm.value)
      ElMessage.success('课程开设成功')
    }
    dialogVisible.value = false
    await loadCourses()
  } catch (error: any) {
    console.error('提交课程失败:', error)
    ElMessage.error(error.response?.data?.detail || '提交失败')
  } finally {
    loading.value = false
  }
}

// 删除课程
const handleDelete = (course: CourseManagementResponse) => {
  ElMessageBox.confirm(
    `确定要删除课程 "${course.course_name}" 吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      await courseManagementApi.deleteCourse(course.id)
      ElMessage.success('课程删除成功')
      await loadCourses()
    } catch (error: any) {
      console.error('删除课程失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {
    // 用户取消
  })
}

// 重置搜索
const handleReset = () => {
  searchForm.value = {
    semester: '',
    course_type: '',
    department: '',
    search: ''
  }
  pagination.value.page = 1
  loadCourses()
}

onMounted(() => {
  loadCourses()
  loadTeachers()
})
</script>

<style scoped>
.course-management {
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
  font-size: 24px;
  font-weight: 600;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
