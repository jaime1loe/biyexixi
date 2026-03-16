<template>
  <el-container class="layout-container">
    <el-header>
      <div class="header-content">
        <h1 class="system-title">高效智能问答系统</h1>
        <div class="header-actions">
          <el-dropdown @command="handleMenuCommand">
            <el-button type="primary" class="home-menu-btn">
              <el-icon><Menu /></el-icon>
              首页功能
              <el-icon><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="/home">
                  <el-icon><HomeFilled /></el-icon>
                  首页
                </el-dropdown-item>
                <el-dropdown-item command="/chat">
                  <el-icon><ChatDotRound /></el-icon>
                  智能问答
                </el-dropdown-item>
                <el-dropdown-item command="/history">
                  <el-icon><Clock /></el-icon>
                  问答历史
                </el-dropdown-item>
                <el-dropdown-item command="/knowledge">
                  <el-icon><Document /></el-icon>
                  知识库管理
                </el-dropdown-item>
                <!-- 老师功能：学生评价查询 -->
                <el-dropdown-item v-if="isTeacher" command="/evaluations">
                  <el-icon><EditPen /></el-icon>
                  学生评价查询
                </el-dropdown-item>
                <el-dropdown-item command="/favorites">
                  <el-icon><Star /></el-icon>
                  我的收藏
                </el-dropdown-item>
                <el-dropdown-item command="/campus">
                  <el-icon><School /></el-icon>
                  校园服务
                </el-dropdown-item>
                <el-dropdown-item command="/dashboard">
                  <el-icon><DataAnalysis /></el-icon>
                  数据统计
                </el-dropdown-item>
                <el-dropdown-item v-if="isAdmin" command="/admin">
                  <el-icon><Management /></el-icon>
                  管理后台
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-dropdown @command="handleUserCommand">
            <div class="user-dropdown">
              <el-avatar :size="36" :src="userInfo?.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span>{{ userInfo?.username || '用户' }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><UserFilled /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  系统设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  ArrowDown,
  UserFilled,
  Setting,
  SwitchButton,
  Menu,
  HomeFilled,
  ChatDotRound,
  Clock,
  Document,
  Star,
  School,
  DataAnalysis,
  Management,
  EditPen,
  Trophy
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const isAdmin = computed(() => userInfo.value?.role === 'admin')
const isTeacher = computed(() => userInfo.value?.role === 'teacher')
const isStudent = computed(() => userInfo.value?.role === 'student')

function handleMenuCommand(path: string) {
  router.push(path)
}

async function handleUserCommand(command: string) {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      try {
        await ElMessageBox.confirm('确定要退出登录吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/')
      } catch {
        // 用户取消
      }
      break
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 21, 41, 0.15);
  display: flex;
  align-items: center;
  padding: 0 40px;
  height: 70px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.system-title {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.home-menu-btn {
  background-color: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #fff;
  font-size: 16px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
}

.home-menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 20px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.user-dropdown .el-avatar {
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.user-dropdown span {
  font-weight: 500;
  font-size: 15px;
}

.el-main {
  background-color: #f5f7fa;
  padding: 0;
  height: calc(100vh - 70px);
  overflow-y: auto;
}
</style>
