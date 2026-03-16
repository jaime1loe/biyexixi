<template>
  <div class="users-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="title">用户列表</span>
        </div>
      </template>

      <!-- 用户列表 -->
      <div>
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="身份">
            <el-select v-model="searchForm.role" placeholder="全部" clearable>
              <el-option label="管理员" value="admin" />
              <el-option label="教师" value="teacher" />
              <el-option label="学生" value="student" />
            </el-select>
          </el-form-item>
          <el-form-item label="关键词">
            <el-input
              v-model="searchForm.keyword"
              placeholder="搜索用户名或邮箱"
              clearable
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchUsers">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>

        <el-table v-loading="loading" :data="users" stripe style="margin-top: 20px">
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="role" label="身份" width="100">
            <template #default="{ row }">
              <el-tag :type="getRoleType(row.role)">
                {{ getRoleLabel(row.role) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="department" label="院系" width="150" />
          <el-table-column prop="is_active" label="状态" width="80">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'">
                {{ row.is_active ? '正常' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="注册时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" link size="small" @click="editUser(row)">
                编辑
              </el-button>
              <el-button
                :type="row.is_active ? 'warning' : 'success'"
                link
                size="small"
                @click="toggleUserStatus(row)"
              >
                {{ row.is_active ? '禁用' : '启用' }}
              </el-button>
              <el-button type="danger" link size="small" @click="resetPassword(row)">
                重置密码
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadUsers"
          @current-change="loadUsers"
          style="margin-top: 20px; justify-content: flex-end"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { authApi } from '@/api/auth'

// 用户列表相关
const loading = ref(false)
const users = ref<any[]>([])
const searchForm = ref({
  role: '',
  keyword: ''
})
const pagination = ref({
  page: 1,
  size: 20,
  total: 0
})

const loadUsers = async () => {
  loading.value = true
  try {
    const params: any = {
      skip: (pagination.value.page - 1) * pagination.value.size,
      limit: pagination.value.size
    }
    if (searchForm.value.role) {
      params.role = searchForm.value.role
    }
    const response = await authApi.getUsers(params)
    users.value = response || []
    pagination.value.total = response?.length || 0
  } catch (error: any) {
    console.error('加载用户失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    loading.value = false
  }
}

const searchUsers = () => {
  pagination.value.page = 1
  loadUsers()
}

const resetSearch = () => {
  searchForm.value = {
    role: '',
    keyword: ''
  }
  pagination.value.page = 1
  loadUsers()
}

const editUser = (_user: any) => {
  ElMessage.info('编辑用户功能开发中')
}

const toggleUserStatus = async (user: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要${user.is_active ? '禁用' : '启用'}该用户吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    ElMessage.success('操作成功')
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('操作失败:', error)
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  }
}

const resetPassword = async (user: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要重置用户 ${user.username} 的密码吗？新密码将发送到用户邮箱。`,
      '重置密码',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    ElMessage.success('密码重置功能开发中')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('重置密码失败:', error)
      ElMessage.error(error.response?.data?.detail || '重置失败')
    }
  }
}

const getRoleType = (role: string) => {
  const typeMap: Record<string, string> = {
    admin: 'danger',
    teacher: 'warning',
    student: 'primary'
  }
  return typeMap[role] || 'info'
}

const getRoleLabel = (role: string) => {
  const labelMap: Record<string, string> = {
    admin: '管理员',
    teacher: '教师',
    student: '学生'
  }
  return labelMap[role] || role
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-management {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-pagination) {
  display: flex;
  justify-content: flex-end;
}
</style>