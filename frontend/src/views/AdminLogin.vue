<template>
  <div class="admin-login-container">
    <div class="admin-login-box">
      <div class="admin-login-header">
        <div class="admin-logo">
          <el-icon size="48" color="#f56c6c"><Setting /></el-icon>
        </div>
        <h1>管理员后台登录</h1>
        <p>高校知识库智能答疑系统 - 管理后台</p>
      </div>

      <el-form
        ref="adminLoginFormRef"
        :model="adminLoginForm"
        :rules="adminLoginRules"
        label-position="top"
        size="large"
        class="admin-login-form"
      >
        <el-form-item label="管理员账号" prop="username">
          <el-input
            v-model="adminLoginForm.username"
            placeholder="请输入管理员账号"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item label="管理员密码" prop="password">
          <el-input
            v-model="adminLoginForm.password"
            type="password"
            placeholder="请输入管理员密码"
            :prefix-icon="Lock"
            show-password
            @keyup.enter="handleAdminLogin"
          />
        </el-form-item>

        <el-form-item>
          <div class="admin-form-options">
            <el-checkbox v-model="rememberMe">记住密码</el-checkbox>
            <el-link type="primary" underline="never" @click="gotoNormalLogin">
              返回普通用户登录
            </el-link>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button
            type="danger"
            class="admin-login-button"
            :loading="loading"
            @click="handleAdminLogin"
          >
            管理员登录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="admin-login-footer">
        <p><el-icon><Warning /></el-icon> 仅限管理员账号登录</p>
        <p>© 2026 高校知识库智能答疑系统 | 管理员后台</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock, Setting, Warning } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { authApi } from '@/api/auth'
import type { LoginRequest } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const rememberMe = ref(false)
const adminLoginFormRef = ref<FormInstance>()

const adminLoginForm = reactive({
  username: '',
  password: ''
})

const adminLoginRules: FormRules = {
  username: [
    { required: true, message: '请输入管理员账号', trigger: 'blur' },
    { min: 3, max: 20, message: '账号长度为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入管理员密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20个字符', trigger: 'blur' }
  ]
}

async function handleAdminLogin() {
  if (!adminLoginFormRef.value) return

  try {
    const valid = await adminLoginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    const loginData: LoginRequest = {
      username: adminLoginForm.username,
      password: adminLoginForm.password
    }

    const response = await authApi.login(loginData)

    // 先存储token
    userStore.setToken(response.access_token)

    // 验证用户角色是否为管理员
    try {
      const userInfo = await authApi.getCurrentUser()
      
      // 检查角色是否为管理员
      if (userInfo.role !== 'admin') {
        ElMessage.error('您不是管理员，无法登录管理后台')
        // 清除token
        userStore.clearUserInfo()
        sessionStorage.removeItem('token')
        localStorage.removeItem('token')
        return
      }

      // 存储管理员用户信息
      userStore.setUserInfo({
        id: userInfo.id,
        username: userInfo.username,
        role: userInfo.role,
        avatar: userInfo.avatar || '',
        email: userInfo.email || '',
        real_name: userInfo.real_name || ''
      })

      // 管理员登录成功，跳转到管理后台
      ElMessage.success('管理员登录成功!')
      
      // 设置管理员登录标记
      sessionStorage.setItem('isAdminLogin', 'true')
      
      await router.push('/admin')
    } catch (userError: any) {
      console.error('获取用户信息失败:', userError)
      ElMessage.error('获取用户信息失败，请重新登录')
      // 清除token
      userStore.clearUserInfo()
      sessionStorage.removeItem('token')
      localStorage.removeItem('token')
    }
  } catch (error: any) {
    console.error('管理员登录失败:', error)
    const errorMessage = error.response?.data?.detail || '登录失败，请检查账号和密码'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

function gotoNormalLogin() {
  router.push('/login')
}
</script>

<style scoped>
.admin-login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5222d 0%, #cf1322 100%);
  padding: 20px;
}

.admin-login-box {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(245, 34, 45, 0.3);
  overflow: hidden;
}

.admin-login-header {
  text-align: center;
  padding: 40px 40px 20px;
  background: linear-gradient(135deg, #fff1f0 0%, #ffffff 100%);
  border-bottom: 1px solid #ffccc7;
}

.admin-logo {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.admin-login-header h1 {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 600;
  color: #f5222d;
}

.admin-login-header p {
  margin: 0;
  font-size: 14px;
  color: #a8071a;
  font-weight: 500;
}

.admin-login-form {
  padding: 30px 40px;
}

:deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 500;
  color: #595959;
}

.admin-form-options {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #f5222d 0%, #cf1322 100%);
  border: none;
  transition: all 0.3s;
}

.admin-login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(245, 34, 45, 0.4);
}

.admin-login-button:active {
  transform: translateY(0);
}

.admin-login-footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid #ffccc7;
  background: #fff2e8;
}

.admin-login-footer p {
  margin: 8px 0;
  font-size: 12px;
  color: #a8071a;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.admin-login-footer p:first-child {
  font-weight: 500;
}
</style>