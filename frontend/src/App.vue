<template>
  <el-config-provider :locale="zhCn">
    <component :is="currentLayout">
      <router-view />
    </component>
  </el-config-provider>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { useUserStore } from '@/store/user'
import Layout from '@/components/Layout.vue'

const route = useRoute()
const userStore = useUserStore()

// 登录页面不使用布局组件
const currentLayout = computed(() => 
  route.path === '/login' || route.path === '/admin/login' ? 'div' : Layout
)

onMounted(() => {
  // 从 sessionStorage 初始化用户状态 (关闭浏览器后自动清除)
  const storedUser = sessionStorage.getItem('userInfo')
  const storedToken = sessionStorage.getItem('token')
  if (storedUser) {
    userStore.setUserInfo(JSON.parse(storedUser))
  }
  if (storedToken) {
    userStore.setToken(storedToken)
  }
})
</script>

<style>
#app {
  width: 100%;
  height: 100vh;
}
</style>
