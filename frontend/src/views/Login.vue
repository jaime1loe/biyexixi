<template>
  <div class="login-container">
    <!-- 科技装饰元素 -->
    <div class="tech-decoration">
      <span class="tech-element">📚</span>
      <span class="tech-element">💡</span>
      <span class="tech-element">🔬</span>
      <span class="tech-element">🎓</span>
      <span class="tech-element">💻</span>
      <span class="tech-element">🔗</span>
    </div>
    
    <div class="login-box">
      <div class="login-header">
        <div class="logo">
          <el-icon size="48" color="#409eff"><ChatLineSquare /></el-icon>
        </div>
        <h1>高校知识库智能答疑系统</h1>
        <p>基于大模型的智能问答平台</p>
      </div>

      <el-tabs v-model="activeTab" class="login-tabs" stretch>
        <el-tab-pane label="登录" name="login">
          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            label-position="top"
            size="large"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
                clearable
              />
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                show-password
                @keyup.enter="handleLogin"
              />
            </el-form-item>

            <el-form-item label="登录身份" prop="loginRole">
              <el-select
                v-model="loginForm.loginRole"
                placeholder="请选择登录身份"
                style="width: 100%"
              >
                <el-option label="学生" value="student" />
                <el-option label="教师" value="teacher" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <div class="form-options">
                <el-checkbox v-model="rememberMe">记住密码</el-checkbox>
                <el-link type="primary" underline="never">忘记密码?</el-link>
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                @click="handleLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            label-position="top"
            size="large"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="请输入用户名(3-20个字符)"
                :prefix-icon="User"
                clearable
              />
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="请输入密码(6-20个字符)"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>

            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="请再次输入密码"
                :prefix-icon="Lock"
                show-password
                @keyup.enter="handleRegister"
              />
            </el-form-item>

            <el-form-item label="邮箱" prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="请输入邮箱地址"
                :prefix-icon="Message"
                clearable
              />
            </el-form-item>

            <el-form-item label="身份" prop="role">
              <el-select
                v-model="registerForm.role"
                placeholder="请选择身份"
                style="width: 100%"
              >
                <el-option label="学生" value="student" />
                <el-option label="教师" value="teacher" />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-checkbox v-model="agreeTerms">
                我已阅读并同意
                <el-link type="primary" underline="never">《用户协议》</el-link>
                和
                <el-link type="primary" underline="never">《隐私政策》</el-link>
              </el-checkbox>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                @click="handleRegister"
              >
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <div class="login-footer">
        <p>© 2026 高校知识库智能答疑系统 | 毕业设计项目</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock, Message, ChatLineSquare } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { authApi, type LoginRequest, type RegisterRequest } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('login')
const loading = ref(false)
const rememberMe = ref(false)
const agreeTerms = ref(false)

const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()

const loginForm = reactive({
  username: '',
  password: '',
  loginRole: ''
})

const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  role: ''
})

const validateUsername = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入用户名'))
  } else if (value.length < 3 || value.length > 20) {
    callback(new Error('用户名长度为3-20个字符'))
  } else {
    callback()
  }
}

const validatePassword = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入密码'))
  } else if (value.length < 6 || value.length > 20) {
    callback(new Error('密码长度为6-20个字符'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const validateEmail = (rule: any, value: any, callback: any) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!value) {
    callback(new Error('请输入邮箱地址'))
  } else if (!emailRegex.test(value)) {
    callback(new Error('请输入正确的邮箱地址'))
  } else {
    callback()
  }
}

const loginRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  loginRole: [{ required: true, message: '请选择登录身份', trigger: 'change' }]
}

const registerRules: FormRules = {
  username: [{ validator: validateUsername, trigger: 'blur' }],
  password: [{ validator: validatePassword, trigger: 'blur' }],
  confirmPassword: [{ validator: validateConfirmPassword, trigger: 'blur' }],
  email: [{ validator: validateEmail, trigger: 'blur' }],
  role: [{ required: true, message: '请选择身份', trigger: 'change' }]
}

async function handleLogin() {
  if (!loginFormRef.value) return

  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    const loginData: LoginRequest = {
      username: loginForm.username,
      password: loginForm.password
    }

    const response = await authApi.login(loginData)

    // 存储token
    userStore.setToken(response.access_token)

    // 获取用户信息
    try {
      const userInfo = await authApi.getCurrentUser()
      userStore.setUserInfo({
        id: userInfo.id,
        username: userInfo.username,
        role: userInfo.role,
        avatar: userInfo.avatar || '',
        email: userInfo.email || ''
      })

      // 验证用户选择的角色与实际角色是否匹配
      const selectedRole = loginForm.loginRole
      const actualRole = userInfo.role

      if (selectedRole !== actualRole) {
        ElMessage.error(`您选择的身份(${getRoleLabel(selectedRole)})与您的实际身份(${getRoleLabel(actualRole)})不匹配，请重新选择`)
        // 清除token
        userStore.clearUserInfo()
        sessionStorage.removeItem('token')
        return
      }

      // 根据角色跳转不同页面
      ElMessage.success('登录成功!')
      if (selectedRole === 'admin') {
        // 管理员跳转到管理后台
        await router.push('/admin')
      } else {
        // 学生和教师跳转到系统首页
        await router.push('/home')
      }
    } catch (userError: any) {
      console.error('获取用户信息失败:', userError)
      // 获取用户信息失败，但登录成功，使用基本信息继续
      userStore.setUserInfo({
        username: loginData.username,
        role: loginForm.loginRole
      })
      
      // 根据选择的角色跳转
      ElMessage.success('登录成功!')
      if (loginForm.loginRole === 'admin') {
        await router.push('/admin')
      } else {
        await router.push('/home')
      }
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    const errorMessage = error.response?.data?.detail || '登录失败，请检查用户名和密码'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  if (!registerFormRef.value) return

  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    if (!agreeTerms.value) {
      ElMessage.warning('请阅读并同意用户协议和隐私政策')
      return
    }

    loading.value = true

    const registerData: RegisterRequest = {
      username: registerForm.username,
      password: registerForm.password,
      email: registerForm.email,
      role: registerForm.role
    }

    await authApi.register(registerData)

    ElMessage.success('注册成功!请登录')
    activeTab.value = 'login'

    // 清空注册表单
    registerFormRef.value.resetFields()
  } catch (error: any) {
    console.error('注册失败:', error)
    const errorMessage = error.response?.data?.detail || '注册失败，请稍后重试'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

// 获取角色标签
function getRoleLabel(role: string): string {
  const labelMap: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return labelMap[role] || role
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  background-image: url('../../login.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 背景图片遮罩 */
.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
}

/* 科技网格背景 */
.login-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  background-image:
    linear-gradient(rgba(64, 158, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(64, 158, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

/* 浮动科技元素 - 书籍/灯泡/网络节点 */
.tech-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.tech-element {
  position: absolute;
  opacity: 0.15;
  color: #409eff;
  animation: float 6s ease-in-out infinite;
}

.tech-element:nth-child(1) {
  top: 10%;
  left: 10%;
  font-size: 60px;
  animation-delay: 0s;
}

.tech-element:nth-child(2) {
  top: 20%;
  right: 15%;
  font-size: 48px;
  animation-delay: 1s;
}

.tech-element:nth-child(3) {
  bottom: 25%;
  left: 8%;
  font-size: 52px;
  animation-delay: 2s;
}

.tech-element:nth-child(4) {
  bottom: 15%;
  right: 10%;
  font-size: 44px;
  animation-delay: 3s;
}

.tech-element:nth-child(5) {
  top: 40%;
  left: 5%;
  font-size: 36px;
  animation-delay: 4s;
}

.tech-element:nth-child(6) {
  top: 35%;
  right: 5%;
  font-size: 40px;
  animation-delay: 5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

.login-box {
  width: 100%;
  max-width: 480px;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
  z-index: 10;
}

.login-header {
  text-align: center;
  padding: 40px 40px 20px;
  background: rgba(255, 255, 255, 0.6);
}

.logo {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
}

.login-header h1 {
  margin: 0 0 8px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.login-header p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.login-tabs {
  padding: 20px 40px;
  background: rgba(255, 255, 255, 0.6);
}

:deep(.el-tabs__nav-wrap::after) {
  height: 1px;
}

:deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
}

:deep(.el-form-item__label) {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.form-options {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  background: linear-gradient(135deg, #409eff 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid #ebeef5;
  background: rgba(255, 255, 255, 0.6);
}

.login-footer p {
  margin: 0;
  font-size: 12px;
  color: #909399;
}


/* 输入框和下拉框半透明背景 */
:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.6) !important;
}

/* 选择器下拉框半透明背景 */
:deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.6) !important;
}
</style>
