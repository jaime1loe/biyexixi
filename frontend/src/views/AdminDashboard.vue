<template>
  <div class="admin-dashboard">
    <!-- 侧边栏 -->
    <div class="admin-sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <el-icon size="32" color="#f56c6c"><Setting /></el-icon>
          <span class="logo-text">管理后台</span>
        </div>
      </div>
      
      <el-menu
        :default-active="activeTab"
        class="admin-menu"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#ff7875"
        @select="handleTabChange"
      >
        <el-sub-menu index="questions">
          <template #title>
            <el-icon><ChatDotRound /></el-icon>
            <span>问答管理</span>
          </template>
          <el-menu-item index="questions-list">问题列表</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="users">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="users-list">用户列表</el-menu-item>
          <el-menu-item index="roles">角色管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="knowledge">
          <template #title>
            <el-icon><Files /></el-icon>
            <span>知识库管理</span>
          </template>
          <el-menu-item index="knowledge-list">文档列表</el-menu-item>
          <el-menu-item index="knowledge-review">审核管理</el-menu-item>
        </el-sub-menu>
        
        <el-menu-item index="notifications">
          <el-icon><Bell /></el-icon>
          <span>通知管理</span>
        </el-menu-item>
        
        <el-menu-item index="settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </div>

    <!-- 主内容区 -->
    <div class="admin-main">
      <!-- 内容区域 -->
      <div class="admin-content">
        <div style="text-align: right; margin-bottom: 16px;">
          <el-button type="danger" @click="logout">退出登录</el-button>
        </div>
        <!-- 问题列表 -->
        <div v-if="activeTab === 'questions-list'" class="tab-content">
          <QuestionsManagement />
        </div>

        <!-- 用户列表 -->
        <div v-else-if="activeTab === 'users-list'" class="tab-content">
          <UsersManagement />
        </div>

        <!-- 角色管理/信息审核 -->
        <div v-else-if="activeTab === 'roles'" class="tab-content">
          <ProfileChangeReview />
        </div>

        <!-- 知识库列表 -->
        <div v-else-if="activeTab === 'knowledge-list'" class="tab-content">
          <KnowledgeManagement />
        </div>

        <!-- 其他功能 -->
        <div v-else class="tab-content">
          <el-alert
            :title="`${currentTabName} 功能开发中`"
            type="info"
            :closable="false"
            center
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Setting, ChatDotRound, User, Files, Bell } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import QuestionsManagement from '@/components/admin/QuestionsManagement.vue'
import UsersManagement from '@/components/admin/UsersManagement.vue'
import KnowledgeManagement from '@/components/admin/KnowledgeManagement.vue'
import ProfileChangeReview from '@/components/admin/ProfileChangeReview.vue'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('questions-list')

const currentTabName = computed(() => {
  const tabMap: Record<string, string> = {
    'questions-list': '问题列表',
    'users-list': '用户列表',
    'profile-change-review': '信息审核',
    'roles': '角色管理',
    'knowledge-list': '文档列表',
    'knowledge-review': '审核管理',
    'notifications': '通知管理',
    'settings': '系统设置'
  }
  return tabMap[activeTab.value] || '管理后台'
})

function handleTabChange(tab: string) {
  activeTab.value = tab
}

function logout() {
  userStore.logout()
  // 清除管理员登录标记
  sessionStorage.removeItem('isAdminLogin')
  ElMessage.success('已退出管理员登录')
  router.push('/')
}

onMounted(() => {
  // 检查是否为管理员
  if (userStore.userInfo?.role !== 'admin') {
    ElMessage.error('您不是管理员，无法访问管理后台')
    // 清除可能的错误标记
    sessionStorage.removeItem('isAdminLogin')
    router.push('/home')
    return
  }

  // 设置管理员登录标记
  sessionStorage.setItem('isAdminLogin', 'true')
})
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

.admin-sidebar {
  width: 240px;
  background: #001529;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #002140;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
}

.admin-menu {
  border: none;
  height: calc(100vh - 80px);
  overflow-y: auto;
}

.admin-menu .el-menu-item,
.admin-menu .el-sub-menu__title {
  height: 48px;
  line-height: 48px;
}

.admin-menu .el-menu-item:hover,
.admin-menu .el-sub-menu__title:hover {
  background-color: #1890ff !important;
}

.admin-menu .el-menu-item.is-active {
  background-color: #1890ff !important;
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.admin-header {
  background: #fff;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f5f5;
}

.username {
  font-weight: 500;
  color: #333;
}

.admin-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 滚动条样式 */
.admin-menu::-webkit-scrollbar,
.admin-content::-webkit-scrollbar {
  width: 6px;
}

.admin-menu::-webkit-scrollbar-track,
.admin-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.admin-menu::-webkit-scrollbar-thumb,
.admin-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.admin-menu::-webkit-scrollbar-thumb:hover,
.admin-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    width: 200px;
  }
  
  .admin-header {
    padding: 0 16px;
  }
  
  .admin-content {
    padding: 16px;
  }
}

/* 数据概览样式 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.charts-section {
  margin-top: 24px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.chart-placeholder p {
  margin-top: 12px;
  font-size: 14px;
}

.tab-content {
  padding: 0;
}

/* 移动端适配 */
@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
}
</style>