<template>
  <div class="profile-container">
    <!-- 基本信息 -->
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span class="title">基本信息</span>
          <el-button type="primary" size="small" @click="handleEdit" v-if="!isEditing">
            <el-icon><Edit /></el-icon>
            修改
          </el-button>
        </div>
      </template>

      <!-- 头像和基本信息 -->
      <div class="profile-header">
        <el-avatar :size="100" :src="userInfo.avatar">
          <el-icon><User /></el-icon>
        </el-avatar>
        <div class="user-info">
          <h3>{{ userInfo.realName || userInfo.username }}</h3>
          <el-tag :type="getRoleType(userInfo.role)">{{ getRoleLabel(userInfo.role) }}</el-tag>
        </div>
      </div>

      <!-- 查看模式：只显示信息 -->
      <div v-if="!isEditing" class="info-display">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户名">{{ userInfo.username }}</el-descriptions-item>
          <el-descriptions-item label="真实姓名">{{ userInfo.realName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="学号/工号">{{ userInfo.studentId || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ userInfo.email || '-' }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ userInfo.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="院系">{{ userInfo.department || '-' }}</el-descriptions-item>
          <el-descriptions-item label="专业" :span="2">{{ userInfo.major || '-' }}</el-descriptions-item>
          <el-descriptions-item label="个人简介" :span="2">
            {{ userInfo.bio || '-' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 编辑模式：显示表单 -->
      <div v-else class="edit-form">
        <el-form
          ref="profileFormRef"
          :model="editForm"
          :rules="editRules"
          label-width="100px"
        >
          <el-form-item label="真实姓名" prop="realName">
            <el-input v-model="editForm.realName" placeholder="请输入真实姓名" />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input v-model="editForm.email" placeholder="请输入邮箱" />
          </el-form-item>

          <el-form-item label="手机号" prop="phone">
            <el-input v-model="editForm.phone" placeholder="请输入手机号" />
          </el-form-item>

          <el-form-item label="院系" prop="department">
            <el-input v-model="editForm.department" placeholder="请输入院系" />
          </el-form-item>

          <el-form-item label="专业" prop="major">
            <el-input v-model="editForm.major" placeholder="请输入专业" />
          </el-form-item>

          <el-form-item label="个人简介" prop="bio">
            <el-input
              v-model="editForm.bio"
              type="textarea"
              :rows="3"
              placeholder="请输入个人简介"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="修改原因" prop="reason" required>
            <el-input
              v-model="editForm.reason"
              type="textarea"
              :rows="2"
              placeholder="请说明修改原因（必填）"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSubmit" :loading="submitting">
              提交修改
            </el-button>
            <el-button @click="handleCancel">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <!-- 修改申请记录 -->
    <el-card class="requests-card">
      <template #header>
        <div class="card-header">
          <span class="title">修改申请记录</span>
        </div>
      </template>

      <el-empty v-if="changeRequests.length === 0" description="暂无修改申请记录" />

      <el-timeline v-else>
        <el-timeline-item
          v-for="request in changeRequests"
          :key="request.id"
          :timestamp="formatDateTime(request.created_at)"
          placement="top"
        >
          <el-card>
            <div class="request-content">
              <div class="request-header">
                <el-tag :type="getStatusType(request.status)">
                  {{ getStatusLabel(request.status) }}
                </el-tag>
                <span class="request-reason">{{ request.reason }}</span>
              </div>
              <div v-if="request.admin_comment" class="request-comment">
                <el-text type="info" size="small">管理员意见: {{ request.admin_comment }}</el-text>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 修改密码 -->
    <el-card class="password-card">
      <template #header>
        <div class="card-header">
          <span class="title">修改密码</span>
        </div>
      </template>

      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码(至少6位)"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleChangePassword">
            修改密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 账户统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span class="title">账户统计</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <el-icon class="stat-icon" color="#409EFF"><ChatDotRound /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalQuestions }}</div>
              <div class="stat-label">总提问数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon class="stat-icon" color="#67C23A"><DocumentChecked /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalAnswers }}</div>
              <div class="stat-label">获得回答</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon class="stat-icon" color="#E6A23C"><Star /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalRatings }}</div>
              <div class="stat-label">评价次数</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <el-icon class="stat-icon" color="#F56C6C"><Calendar /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.daysActive }}</div>
              <div class="stat-label">活跃天数</div>
            </div>
          </div>
        </el-col>
        </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import { User, ChatDotRound, DocumentChecked, Star, Calendar, Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { authApi } from '@/api/auth'
import { profileChangesApi } from '@/api/profileChanges'

const userStore = useUserStore()

// 编辑状态
const isEditing = ref(false)
const submitting = ref(false)

// 用户信息（显示用）
const userInfo = reactive({
  username: '',
  realName: '',
  role: 'student',
  studentId: '',
  email: '',
  phone: '',
  department: '',
  major: '',
  bio: '',
  avatar: ''
})

// 编辑表单
const editForm = reactive({
  realName: '',
  email: '',
  phone: '',
  department: '',
  major: '',
  bio: '',
  reason: ''
})

// 修改密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 账户统计
const stats = reactive({
  totalQuestions: 0,
  totalAnswers: 0,
  totalRatings: 0,
  daysActive: 0
})

// 修改申请记录
const changeRequests = ref<any[]>([])

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

// 编辑表单验证规则
const editRules = {
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请输入修改原因', trigger: 'blur' }
  ]
}

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: any) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 获取角色类型
const getRoleType = (role: string) => {
  const typeMap: Record<string, string> = {
    'student': 'success',
    'teacher': 'primary',
    'admin': 'danger'
  }
  return typeMap[role] || 'info'
}

// 获取角色标签
const getRoleLabel = (role: string) => {
  const labelMap: Record<string, string> = {
    'student': '学生',
    'teacher': '教师',
    'admin': '管理员'
  }
  return labelMap[role] || role
}

// 加载用户信息
const loadUserInfo = async () => {
  try {
    // 从后端API获取用户信息
    const data = await authApi.getCurrentUser()
    userInfo.username = data.username
    userInfo.realName = data.real_name || ''
    userInfo.role = data.role || 'student'
    userInfo.email = data.email || ''
    userInfo.avatar = data.avatar || ''
    userInfo.studentId = data.student_id || ''
    userInfo.phone = data.phone || ''
    userInfo.department = data.department || ''
    userInfo.major = data.major || ''
    userInfo.bio = data.bio || ''

    // 更新本地存储
    const userData = {
      id: data.id,
      username: data.username,
      role: data.role,
      realName: data.real_name || '',
      email: data.email || '',
      avatar: data.avatar || '',
      studentId: data.student_id || '',
      phone: data.phone || '',
      department: data.department || '',
      major: data.major || '',
      bio: data.bio || ''
    }
    sessionStorage.setItem('userInfo', JSON.stringify(userData))
    userStore.setUserInfo(userData)

    // 加载统计数据
    stats.totalQuestions = 45
    stats.totalAnswers = 42
    stats.totalRatings = 38
    stats.daysActive = 15

    // 加载修改申请记录
    loadChangeRequests()
  } catch (error) {
    console.error('加载用户信息失败:', error)
    // 从sessionStorage读取
    const userData = sessionStorage.getItem('userInfo')
    if (userData) {
      const user = JSON.parse(userData)
      userInfo.username = user.username
      userInfo.realName = user.realName || ''
      userInfo.role = user.role || 'student'
      userInfo.email = user.email || ''
      userInfo.avatar = user.avatar || ''
      userInfo.studentId = user.studentId || ''
      userInfo.phone = user.phone || ''
      userInfo.department = user.department || ''
      userInfo.major = user.major || ''
      userInfo.bio = user.bio || ''
    }
  }
}

// 加载修改申请记录
const loadChangeRequests = async () => {
  try {
    const data = await profileChangesApi.getMyRequests()
    changeRequests.value = data
  } catch (error) {
    console.error('加载修改申请记录失败:', error)
  }
}

// 点击修改按钮
const handleEdit = () => {
  // 初始化编辑表单
  editForm.realName = userInfo.realName
  editForm.email = userInfo.email
  editForm.phone = userInfo.phone
  editForm.department = userInfo.department
  editForm.major = userInfo.major
  editForm.bio = userInfo.bio
  editForm.reason = ''
  isEditing.value = true
}

// 取消编辑
const handleCancel = () => {
  isEditing.value = false
  editFormRef.value?.resetFields()
}

// 提交修改申请
const handleSubmit = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // 提交修改申请
        await profileChangesApi.submit(editForm)

        ElMessage.success('申请提交成功，请等待管理员审核')

        // 退出编辑模式
        isEditing.value = false
        editFormRef.value?.resetFields()

        // 重新加载用户信息
        await loadUserInfo()
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '提交申请失败，请重试')
      } finally {
        submitting.value = false
      }
    }
  })
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const labelMap: Record<string, string> = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝'
  }
  return labelMap[status] || status
}

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // TODO: 调用后端API修改密码
        await new Promise(resolve => setTimeout(resolve, 1000))

        ElMessage.success('密码修改成功,请重新登录')

        // 清空表单
        passwordFormRef.value.resetFields()

        // 3秒后跳转到登录页
        setTimeout(() => {
          sessionStorage.removeItem('token')
          sessionStorage.removeItem('userInfo')
          window.location.href = '/login'
        }, 3000)
      } catch (error) {
        ElMessage.error('密码修改失败,请重试')
      }
    }
  })
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.profile-card,
.password-card,
.stats-card,
.requests-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.user-info {
  flex: 1;
}

.user-info h3 {
  margin: 0 0 10px 0;
  font-size: 24px;
  color: #303133;
}

.info-display {
  padding: 0 20px;
}

.edit-form {
  padding: 0 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-item:hover {
  background: #e6f7ff;
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 36px;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.request-content {
  padding: 10px;
}

.request-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.request-reason {
  flex: 1;
  color: #303133;
  font-weight: 500;
}

.request-comment {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #ebeef5;
}
</style>
