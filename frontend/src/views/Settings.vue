<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span class="title">课程设置</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" type="border-card">
        <!-- 课程管理 -->
        <el-tab-pane label="课程管理" name="courses">
          <CourseManagement />
        </el-tab-pane>

        <!-- 排课管理 -->
        <el-tab-pane label="排课管理" name="schedules">
          <div class="coming-soon">
            <el-empty description="排课管理功能开发中" />
          </div>
        </el-tab-pane>

        <!-- 教师管理 -->
        <el-tab-pane label="教师管理" name="teachers">
          <div class="teacher-list">
            <h3>教师列表</h3>
            <el-table :data="teachers" stripe v-loading="teachersLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="username" label="用户名" width="150" />
              <el-table-column prop="real_name" label="真实姓名" width="150" />
              <el-table-column prop="department" label="院系" width="150" />
              <el-table-column label="操作" width="200">
                <template #default="{ row }">
                  <el-button type="primary" size="small" :icon="Edit">编辑</el-button>
                  <el-button type="danger" size="small" :icon="Delete">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Edit, Delete } from '@element-plus/icons-vue'
import {
  courseManagementApi,
  Teacher,
  CourseManagementResponse
} from '@/api/courseSelection'

// 当前标签页
const activeTab = ref('courses')

// 教师
const teachers = ref<Teacher[]>([])
const teachersLoading = ref(false)

// 加载教师列表
const loadTeachers = async () => {
  teachersLoading.value = true
  try {
    teachers.value = await courseManagementApi.getTeachers()
  } catch (error: any) {
    console.error('加载教师列表失败:', error)
  } finally {
    teachersLoading.value = false
  }
}

onMounted(() => {
  loadTeachers()
})
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.settings-card {
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

.teacher-list {
  padding: 20px 0;
}

.teacher-list h3 {
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
}

.coming-soon {
  padding: 60px 0;
  text-align: center;
}
</style>
