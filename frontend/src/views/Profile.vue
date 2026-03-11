<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span class="title">个人中心</span>
        </div>
      </template>

      <!-- 头像和基本信息 -->
      <div class="profile-header">
        <el-avatar :size="100" :src="userInfo.avatar" @click="handleAvatarClick">
          <el-icon><User /></el-icon>
        </el-avatar>
        <div class="avatar-tip">
          <el-text type="info" size="small">点击更换头像</el-text>
        </div>
      </div>

      <!-- 用户信息表单 -->
      <el-form
        ref="profileFormRef"
        :model="userInfo"
        :rules="rules"
        label-width="100px"
        class="profile-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userInfo.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="userInfo.realName" placeholder="请输入真实姓名" />
        </el-form-item>

        <el-form-item label="用户身份" prop="role">
          <el-select v-model="userInfo.role" placeholder="请选择身份" disabled>
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item label="学号/工号" prop="studentId">
          <el-input v-model="userInfo.studentId" placeholder="请输入学号或工号" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userInfo.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="院系" prop="department">
          <el-input v-model="userInfo.department" placeholder="请输入院系" />
        </el-form-item>

        <el-form-item label="专业" prop="major">
          <el-input v-model="userInfo.major" placeholder="请输入专业" />
        </el-form-item>

        <el-form-item label="个人简介" prop="bio">
          <el-input
            v-model="userInfo.bio"
            type="textarea"
            :rows="3"
            placeholder="请输入个人简介"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="saving">
            保存修改
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
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
          <el-button type="primary" @click="handleChangePassword" :loading="changingPassword">
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

    <!-- 头像上传对话框 -->
    <el-dialog v-model="avatarDialogVisible" title="上传头像" width="400px">
      <el-upload
        class="avatar-uploader"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload"
        :on-success="handleAvatarSuccess"
        :http-request="uploadAvatar"
        accept="image/*"
      >
        <img v-if="tempAvatar" :src="tempAvatar" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
      <div class="upload-tip">
        <el-text type="info" size="small">支持 JPG、PNG 格式,大小不超过 2MB</el-text>
      </div>
      <template #footer>
        <el-button @click="avatarDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAvatar">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance, type UploadRequestOptions } from 'element-plus'
import { User, ChatDotRound, DocumentChecked, Star, Calendar, Plus } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()

// 用户信息
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

// 状态
const saving = ref(false)
const changingPassword = ref(false)
const avatarDialogVisible = ref(false)
const tempAvatar = ref('')

// 表单引用
const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

// 验证规则
const rules = {
  realName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
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

// 加载用户信息
const loadUserInfo = () => {
  // TODO: 从后端API获取用户信息
  const userData = localStorage.getItem('userInfo')
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

  // 加载统计数据
  stats.totalQuestions = 45
  stats.totalAnswers = 42
  stats.totalRatings = 38
  stats.daysActive = 15
}

// 保存用户信息
const handleSave = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        // TODO: 调用后端API保存用户信息
        await new Promise(resolve => setTimeout(resolve, 1000))

        // 更新本地存储
        const userData = JSON.parse(localStorage.getItem('userInfo') || '{}')
        Object.assign(userData, userInfo)
        localStorage.setItem('userInfo', JSON.stringify(userData))

        // 同时更新 userStore
        const storedUser = JSON.parse(localStorage.getItem('userInfo') || '{}')
        userStore.setUserInfo(storedUser)

        ElMessage.success('保存成功')
      } catch (error) {
        ElMessage.error('保存失败,请重试')
      } finally {
        saving.value = false
      }
    }
  })
}

// 重置表单
const handleReset = () => {
  loadUserInfo()
  profileFormRef.value?.resetFields()
  ElMessage.info('已重置为原始信息')
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPassword.value = true
      try {
        // TODO: 调用后端API修改密码
        await new Promise(resolve => setTimeout(resolve, 1000))

        ElMessage.success('密码修改成功,请重新登录')

        // 清空表单
        passwordFormRef.value.resetFields()

        // 3秒后跳转到登录页
        setTimeout(() => {
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }, 3000)
      } catch (error) {
        ElMessage.error('密码修改失败,请重试')
      } finally {
        changingPassword.value = false
      }
    }
  })
}

// 点击头像
const handleAvatarClick = () => {
  avatarDialogVisible.value = true
  tempAvatar.value = userInfo.avatar
}

// 头像上传前验证
const beforeAvatarUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 自定义上传
const uploadAvatar = async (options: UploadRequestOptions) => {
  const reader = new FileReader()
  reader.readAsDataURL(options.file)
  reader.onload = () => {
    tempAvatar.value = reader.result as string
  }
}

// 头像上传成功
const handleAvatarSuccess = () => {
  ElMessage.success('头像上传成功')
}

// 确认更换头像
const confirmAvatar = () => {
  userInfo.avatar = tempAvatar.value
  avatarDialogVisible.value = false

  // 保存到本地存储
  const userData = JSON.parse(localStorage.getItem('userInfo') || '{}')
  userData.avatar = userInfo.avatar
  localStorage.setItem('userInfo', JSON.stringify(userData))

  // 同时更新 userStore
  userStore.setUserInfo(userData)

  // TODO: 调用后端API保存头像
  ElMessage.success('头像更换成功')
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
.stats-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.avatar-tip {
  margin-top: 10px;
}

.profile-form {
  max-width: 600px;
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

/* 头像上传样式 */
.avatar-uploader {
  display: flex;
  justify-content: center;
}

.avatar-uploader :deep(.el-upload) {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.avatar-uploader :deep(.el-upload:hover) {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 200px;
  height: 200px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  text-align: center;
  margin-top: 10px;
}
</style>
