<template>
  <div class="evaluations-container">
    <div class="evaluations-header">
      <h3><el-icon><Document /></el-icon>学生评价查询</h3>
      <div class="header-actions">
        <el-button v-if="isTeacher" type="primary" :icon="Plus" @click="handleAddEvaluation">添加评价</el-button>
        <el-button :icon="Refresh" @click="refreshData">刷新</el-button>
      </div>
    </div>

    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索学生姓名或学号"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-select
            v-model="selectedCourse"
            placeholder="选择课程"
            clearable
            style="width: 100%"
            @change="handleFilterChange"
          >
            <el-option
              v-for="course in courseOptions"
              :key="course.id"
              :label="course.name"
              :value="course.id"
            />
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-select
            v-model="selectedSemester"
            placeholder="选择学期"
            clearable
            style="width: 100%"
            @change="handleFilterChange"
          >
            <el-option
              v-for="semester in semesterOptions"
              :key="semester.value"
              :label="semester.label"
              :value="semester.value"
            />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #409eff;">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.totalStudents }}</div>
                <div class="stat-label">学生总数</div>
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
                <div class="stat-value">{{ stats.averageScore }}</div>
                <div class="stat-label">平均分</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #e6a23c;">
                <el-icon><Trophy /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.excellentCount }}</div>
                <div class="stat-label">优秀(>=90)</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background: #f56c6c;">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.failCount }}</div>
                <div class="stat-label">不及格(<60)</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="evaluations-content">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="所有评价" name="all">
          <el-table
            v-loading="loading"
            :data="evaluationsList"
            style="width: 100%"
            stripe
            @sort-change="handleSortChange"
          >
            <el-table-column prop="student_name" label="学生姓名" width="120" />
            <el-table-column prop="student_id" label="学号" width="120" />
            <el-table-column prop="course_name" label="课程名称" width="200" />
            <el-table-column prop="score" label="分数" width="100" sortable>
              <template #default="{ row }">
                <el-tag :type="getScoreType(row.score)" size="small">
                  {{ row.score }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="semester" label="学期" width="120">
              <template #default="{ row }">
                <span>{{ formatSemester(row.semester) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="evaluation_date" label="评价日期" width="150">
              <template #default="{ row }">
                <span>{{ formatDate(row.evaluation_date) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="teacher_comment" label="评语" min-width="200">
              <template #default="{ row }">
                <el-tooltip :content="row.teacher_comment" placement="top">
                  <div class="comment-cell">{{ truncateComment(row.teacher_comment) }}</div>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button v-if="isTeacher" link type="primary" size="small" @click="handleEdit(row)">
                  编辑
                </el-button>
                <el-button v-if="isTeacher" link type="danger" size="small" @click="handleDelete(row)">
                  删除
                </el-button>
                <el-button link type="info" size="small" @click="handleViewDetails(row)">
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              layout="total, prev, pager, next, jumper"
              @change="loadEvaluations"
            />
          </div>
        </el-tab-pane>

        <el-tab-pane v-if="isTeacher" label="我的评价" name="my-evaluations">
          <el-table
            v-loading="loading"
            :data="myEvaluationsList"
            style="width: 100%"
            stripe
          >
            <el-table-column prop="student_name" label="学生姓名" width="120" />
            <el-table-column prop="student_id" label="学号" width="120" />
            <el-table-column prop="course_name" label="课程名称" width="180" />
            <el-table-column prop="score" label="分数" width="100">
              <template #default="{ row }">
                <el-tag :type="getScoreType(row.score)" size="small">
                  {{ row.score }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="semester" label="学期" width="120">
              <template #default="{ row }">
                <span>{{ formatSemester(row.semester) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" size="small" @click="handleEdit(row)">
                  编辑
                </el-button>
                <el-button link type="danger" size="small" @click="handleDelete(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane v-if="isStudent" label="我的成绩" name="my-scores">
          <el-table
            v-loading="loading"
            :data="myScoresList"
            style="width: 100%"
            stripe
          >
            <el-table-column prop="course_name" label="课程名称" width="200" />
            <el-table-column prop="score" label="分数" width="100">
              <template #default="{ row }">
                <el-tag :type="getScoreType(row.score)" size="small">
                  {{ row.score }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="semester" label="学期" width="120">
              <template #default="{ row }">
                <span>{{ formatSemester(row.semester) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="evaluation_date" label="评价日期" width="150">
              <template #default="{ row }">
                <span>{{ formatDate(row.evaluation_date) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="teacher_comment" label="评语" min-width="200" />
          </el-table>
        </el-tab-pane>

        <el-tab-pane v-if="isTeacher" label="成绩统计" name="statistics">
          <div class="chart-section">
            <el-card shadow="hover" style="margin-bottom: 20px;">
              <template #header>
                <div class="chart-header">
                  <span>成绩分布图</span>
                  <el-select v-model="chartCourse" placeholder="选择课程" style="width: 200px;">
                    <el-option
                      v-for="course in courseOptions"
                      :key="course.id"
                      :label="course.name"
                      :value="course.id"
                    />
                  </el-select>
                </div>
              </template>
              <div id="scoreDistributionChart" style="width: 100%; height: 300px;"></div>
            </el-card>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 添加/编辑评价对话框 -->
    <el-dialog
      v-model="evaluationDialogVisible"
      :title="editingEvaluation ? '编辑评价' : '添加评价'"
      width="600px"
    >
      <el-form
        ref="evaluationFormRef"
        :model="evaluationForm"
        :rules="evaluationRules"
        label-width="100px"
      >
        <el-form-item label="学生" prop="student_id">
          <el-select
            v-model="evaluationForm.student_id"
            placeholder="选择学生"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="student in studentOptions"
              :key="student.id"
              :label="`${student.name} (${student.student_id})`"
              :value="student.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="课程" prop="course_id">
          <el-select
            v-model="evaluationForm.course_id"
            placeholder="选择课程"
            style="width: 100%"
          >
            <el-option
              v-for="course in teacherCourseOptions"
              :key="course.id"
              :label="course.name"
              :value="course.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学期" prop="semester">
          <el-select
            v-model="evaluationForm.semester"
            placeholder="选择学期"
            style="width: 100%"
          >
            <el-option
              v-for="semester in semesterOptions"
              :key="semester.value"
              :label="semester.label"
              :value="semester.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="分数" prop="score">
          <el-input-number
            v-model="evaluationForm.score"
            :min="0"
            :max="100"
            :step="0.5"
            style="width: 100%"
            placeholder="输入0-100之间的分数"
          />
        </el-form-item>
        <el-form-item label="评语" prop="teacher_comment">
          <el-input
            v-model="evaluationForm.teacher_comment"
            type="textarea"
            :rows="4"
            placeholder="请输入对学生的评语..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="evaluationDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitEvaluation" :loading="submitting">
          {{ editingEvaluation ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="评价详情"
      width="500px"
    >
      <div class="detail-content" v-if="currentEvaluation">
        <div class="detail-section">
          <h4>学生信息</h4>
          <div class="detail-row">
            <span class="label">姓名：</span>
            <span class="value">{{ currentEvaluation.student_name }}</span>
          </div>
          <div class="detail-row">
            <span class="label">学号：</span>
            <span class="value">{{ currentEvaluation.student_id }}</span>
          </div>
        </div>
        <el-divider />
        <div class="detail-section">
          <h4>课程信息</h4>
          <div class="detail-row">
            <span class="label">课程名称：</span>
            <span class="value">{{ currentEvaluation.course_name }}</span>
          </div>
          <div class="detail-row">
            <span class="label">学期：</span>
            <span class="value">{{ formatSemester(currentEvaluation.semester) }}</span>
          </div>
        </div>
        <el-divider />
        <div class="detail-section">
          <h4>评价信息</h4>
          <div class="detail-row">
            <span class="label">分数：</span>
            <span class="value">
              <el-tag :type="getScoreType(currentEvaluation.score)" size="small">
                {{ currentEvaluation.score }}
              </el-tag>
            </span>
          </div>
          <div class="detail-row">
            <span class="label">评价日期：</span>
            <span class="value">{{ formatDate(currentEvaluation.evaluation_date) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">评语：</span>
            <div class="value">{{ currentEvaluation.teacher_comment }}</div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Plus, Refresh, Search, User, SuccessFilled,
  Trophy, Warning, Edit, Delete, View
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import * as echarts from 'echarts'

// Interface definitions
interface Evaluation {
  id: number
  student_id: string
  student_name: string
  course_id: number
  course_name: string
  score: number
  semester: string
  evaluation_date: string
  teacher_comment: string
  teacher_id?: number
  teacher_name?: string
}

interface Student {
  id: string
  student_id: string
  name: string
  class_name?: string
}

interface Course {
  id: number
  name: string
  teacher_id?: number
}

interface SemesterOption {
  value: string
  label: string
}

// Reactive data
const userStore = useUserStore()
const activeTab = ref('all')
const searchKeyword = ref('')
const selectedCourse = ref<number>()
const selectedSemester = ref<string>()
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const evaluationDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const editingEvaluation = ref(false)
const submitting = ref(false)
const chartCourse = ref<number>()

const evaluationsList = ref<Evaluation[]>([])
const myEvaluationsList = ref<Evaluation[]>([])
const myScoresList = ref<Evaluation[]>([])
const studentOptions = ref<Student[]>([])
const courseOptions = ref<Course[]>([])
const teacherCourseOptions = ref<Course[]>([])
const semesterOptions = ref<SemesterOption[]>([
  { value: '2024-2025-1', label: '2024-2025学年第一学期' },
  { value: '2024-2025-2', label: '2024-2025学年第二学期' },
  { value: '2025-2026-1', label: '2025-2026学年第一学期' },
  { value: '2025-2026-2', label: '2025-2026学年第二学期' },
])
const evaluationForm = ref({
  student_id: '',
  course_id: undefined as number | undefined,
  semester: '',
  score: 0,
  teacher_comment: ''
})
const currentEvaluation = ref<Evaluation | null>(null)
const evaluationFormRef = ref()

const stats = ref({
  totalStudents: 0,
  averageScore: 0,
  excellentCount: 0,
  failCount: 0,
  totalEvaluations: 0
})

// Computed properties
const userRole = computed(() => userStore.userInfo?.role)
const isTeacher = computed(() => userRole.value === 'teacher')
const isStudent = computed(() => userRole.value === 'student')
const isAdmin = computed(() => userRole.value === 'admin')

// Validation rules
const evaluationRules = {
  student_id: [
    { required: true, message: 'Please select a student', trigger: 'blur' }
  ],
  course_id: [
    { required: true, message: 'Please select a course', trigger: 'blur' }
  ],
  semester: [
    { required: true, message: 'Please select a semester', trigger: 'blur' }
  ],
  score: [
    { required: true, message: 'Please enter a score', trigger: 'blur' },
    { validator: (rule: any, value: number, callback: any) => {
      if (value < 0 || value > 100) {
        callback(new Error('Score must be between 0-100'))
      } else {
        callback()
      }
    }, trigger: 'blur' }
  ],
  teacher_comment: [
    { required: true, message: 'Please enter a comment', trigger: 'blur' },
    { min: 5, message: 'Comment must be at least 5 characters', trigger: 'blur' }
  ]
}

// Mock data initialization
function initMockData() {
  studentOptions.value = [
    { id: 'stu001', student_id: '2024001', name: 'Zhang San', class_name: 'CS Class 1' },
    { id: 'stu002', student_id: '2024002', name: 'Li Si', class_name: 'CS Class 1' },
    { id: 'stu003', student_id: '2024003', name: 'Wang Wu', class_name: 'CS Class 2' },
    { id: 'stu004', student_id: '2024004', name: 'Zhao Liu', class_name: 'SE Class 1' },
    { id: 'stu005', student_id: '2024005', name: 'Qian Qi', class_name: 'SE Class 2' },
  ]

  courseOptions.value = [
    { id: 1, name: 'Data Structures', teacher_id: isTeacher.value ? userStore.userInfo?.id : 1 },
    { id: 2, name: 'Algorithm Design', teacher_id: isTeacher.value ? userStore.userInfo?.id : 2 },
    { id: 3, name: 'Database Systems', teacher_id: isTeacher.value ? userStore.userInfo?.id : 3 },
    { id: 4, name: 'Operating Systems', teacher_id: isTeacher.value ? userStore.userInfo?.id : 4 },
  ]

  teacherCourseOptions.value = courseOptions.value.filter(course => 
    isTeacher.value ? course.teacher_id === userStore.userInfo?.id : true
  )

  const mockEvaluations: Evaluation[] = [
    {
      id: 1,
      student_id: '2024001',
      student_name: 'Zhang San',
      course_id: 1,
      course_name: 'Data Structures',
      score: 85.5,
      semester: '2024-2025-1',
      evaluation_date: '2024-12-20',
      teacher_comment: 'Good performance, master core concepts well.'
    },
    {
      id: 2,
      student_id: '2024002',
      student_name: 'Li Si',
      course_id: 1,
      course_name: 'Data Structures',
      score: 92.0,
      semester: '2024-2025-1',
      evaluation_date: '2024-12-20',
      teacher_comment: 'Excellent student, outstanding algorithm implementation skills.'
    },
    {
      id: 3,
      student_id: '2024003',
      student_name: 'Wang Wu',
      course_id: 2,
      course_name: 'Algorithm Design',
      score: 78.0,
      semester: '2024-2025-1',
      evaluation_date: '2024-12-15',
      teacher_comment: 'Solid foundation, but needs improvement in complex algorithm implementation.'
    },
    {
      id: 4,
      student_id: '2024001',
      student_name: 'Zhang San',
      course_id: 2,
      course_name: 'Algorithm Design',
      score: 88.0,
      semester: '2024-2025-1',
      evaluation_date: '2024-12-15',
      teacher_comment: 'Strong algorithm design skills, able to solve medium difficulty problems.'
    },
    {
      id: 5,
      student_id: '2024004',
      student_name: 'Zhao Liu',
      course_id: 1,
      course_name: 'Data Structures',
      score: 95.0,
      semester: '2024-2025-1',
      evaluation_date: '2024-12-20',
      teacher_comment: 'Very excellent, able to independently complete complex data structure design and implementation.'
    },
  ]

  return mockEvaluations
}

// Load evaluations
async function loadEvaluations() {
  loading.value = true
  try {
    const mockEvaluations = initMockData()
    
    let filteredList = mockEvaluations

    if (isStudent.value) {
      filteredList = filteredList.filter(evalItem => evalItem.student_id === userStore.userInfo?.student_id)
      myScoresList.value = filteredList
    } else if (isTeacher.value) {
      const myEvals = filteredList.filter(evalItem => evalItem.teacher_id === userStore.userInfo?.id)
      myEvaluationsList.value = myEvals
      filteredList = isTeacher.value ? filteredList : mockEvaluations
    }

    if (searchKeyword.value) {
      filteredList = filteredList.filter(evalItem =>
        evalItem.student_name.includes(searchKeyword.value) ||
        evalItem.student_id.includes(searchKeyword.value)
      )
    }

    if (selectedCourse.value) {
      filteredList = filteredList.filter(evalItem => evalItem.course_id === selectedCourse.value)
    }

    if (selectedSemester.value) {
      filteredList = filteredList.filter(evalItem => evalItem.semester === selectedSemester.value)
    }

    total.value = filteredList.length

    const startIndex = (currentPage.value - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    evaluationsList.value = filteredList.slice(startIndex, endIndex)

    updateStats(filteredList)

  } catch (error: any) {
    ElMessage.error('Failed to load evaluation data')
    console.error('Failed to load evaluation data:', error)
  } finally {
    loading.value = false
  }
}

// Update statistics
function updateStats(evaluations: Evaluation[]) {
  if (evaluations.length === 0) {
    stats.value = {
      totalStudents: 0,
      averageScore: 0,
      excellentCount: 0,
      failCount: 0,
      totalEvaluations: 0
    }
    return
  }

  const uniqueStudents = new Set(evaluations.map(e => e.student_id))
  const totalScore = evaluations.reduce((sum, evalItem) => sum + evalItem.score, 0)
  const excellent = evaluations.filter(e => e.score >= 90).length
  const fail = evaluations.filter(e => e.score < 60).length

  stats.value = {
    totalStudents: uniqueStudents.size,
    averageScore: Math.round((totalScore / evaluations.length) * 10) / 10,
    excellentCount: excellent,
    failCount: fail,
    totalEvaluations: evaluations.length
  }
}

// Refresh data
function refreshData() {
  loadEvaluations()
}

// Search handler
function handleSearch() {
  currentPage.value = 1
  loadEvaluations()
}

// Filter change handler
function handleFilterChange() {
  currentPage.value = 1
  loadEvaluations()
}

// Sort change handler
function handleSortChange({ prop, order }: { prop: string, order: string }) {
  if (prop === 'score') {
    evaluationsList.value.sort((a, b) => {
      if (order === 'ascending') return a.score - b.score
      if (order === 'descending') return b.score - a.score
      return 0
    })
  }
}

// Add evaluation
function handleAddEvaluation() {
  editingEvaluation.value = false
  evaluationForm.value = {
    student_id: '',
    course_id: undefined,
    semester: '',
    score: 0,
    teacher_comment: ''
  }
  evaluationDialogVisible.value = true
}

// Edit evaluation
function handleEdit(row: Evaluation) {
  editingEvaluation.value = true
  evaluationForm.value = {
    student_id: row.student_id,
    course_id: row.course_id,
    semester: row.semester,
    score: row.score,
    teacher_comment: row.teacher_comment
  }
  evaluationDialogVisible.value = true
}

// Delete evaluation
async function handleDelete(row: Evaluation) {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete the evaluation for student "${row.student_name}" in "${row.course_name}"?`,
      'Confirm',
      {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    ElMessage.success('Deleted successfully')
    loadEvaluations()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('Failed to delete')
    }
  }
}

// View details
function handleViewDetails(row: Evaluation) {
  currentEvaluation.value = row
  detailDialogVisible.value = true
}

// Submit evaluation form
async function handleSubmitEvaluation() {
  if (!evaluationFormRef.value) return
  
  const valid = await evaluationFormRef.value.validate()
  if (!valid) return

  submitting.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    ElMessage.success(editingEvaluation.value ? 'Evaluation updated successfully' : 'Evaluation added successfully')
    evaluationDialogVisible.value = false
    loadEvaluations()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || 'Submission failed')
  } finally {
    submitting.value = false
  }
}

// Get score type based on score
function getScoreType(score: number): string {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 60) return 'warning'
  return 'danger'
}

// Format semester display
function formatSemester(semester: string): string {
  const semesterMap: Record<string, string> = {
    '2024-2025-1': '2024-2025 First Semester',
    '2024-2025-2': '2024-2025 Second Semester',
    '2025-2026-1': '2025-2026 First Semester',
    '2025-2026-2': '2025-2026 Second Semester',
  }
  return semesterMap[semester] || semester
}

// Format date
function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}-${month}-${day}`
}

// Truncate comment display
function truncateComment(comment: string, maxLength = 50): string {
  if (comment.length <= maxLength) return comment
  return comment.substring(0, maxLength) + '...'
}

// Initialize chart
function initChart() {
  const chartDom = document.getElementById('scoreDistributionChart')
  if (!chartDom) return

  const chart = echarts.init(chartDom)
  
  const scoreRanges = [
    { range: '0-59', label: 'Fail', count: 2 },
    { range: '60-69', label: 'Pass', count: 5 },
    { range: '70-79', label: 'Average', count: 8 },
    { range: '80-89', label: 'Good', count: 12 },
    { range: '90-100', label: 'Excellent', count: 6 },
  ]

  const option = {
    title: {
      text: 'Score Distribution',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: scoreRanges.map(item => item.range),
      name: 'Score Range'
    },
    yAxis: {
      type: 'value',
      name: 'Count'
    },
    series: [
      {
        name: 'Student Count',
        type: 'bar',
        data: scoreRanges.map(item => item.count),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#2378f7' },
              { offset: 0.7, color: '#2378f7' },
              { offset: 1, color: '#83bff6' }
            ])
          }
        }
      }
    ]
  }

  chart.setOption(option)
  
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

onMounted(() => {
  loadEvaluations()
  
  if (isTeacher.value) {
    setTimeout(initChart, 300)
  }
})
</script>

<style scoped>
.evaluations-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.evaluations-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.evaluations-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 6px;
}

.stats-section {
  margin-bottom: 24px;
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

.evaluations-content {
  border-radius: 8px;
  overflow: hidden;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.comment-cell {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.detail-content {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 8px;
}

.detail-section {
  margin-bottom: 16px;
}

.detail-section h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #303133;
}

.detail-row {
  display: flex;
  margin-bottom: 10px;
  align-items: flex-start;
}

.detail-row .label {
  width: 100px;
  font-weight: 500;
  color: #606266;
}

.detail-row .value {
  flex: 1;
  color: #303133;
  word-break: break-word;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>