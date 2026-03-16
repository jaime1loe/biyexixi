import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { ElMessage } from 'element-plus'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Welcome',
    component: () => import('@/views/Welcome.vue'),
    meta: { title: '欢迎', requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录/注册', requiresAuth: false }
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLogin.vue'),
    meta: { title: '管理员登录', requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { title: '智能问答', requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { title: '问答历史', requiresAuth: true }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/Knowledge.vue'),
    meta: { title: '知识库', requiresAuth: true }
  },
  {
    path: '/evaluations',
    name: 'Evaluations',
    component: () => import('@/views/Evaluations.vue'),
    meta: { title: '学生评价查询', requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '数据统计', requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { title: '我的收藏', requiresAuth: true }
  },
  {
    path: '/campus',
    name: 'Campus',
    component: () => import('@/views/Campus.vue'),
    meta: { title: '校园服务', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { title: '系统设置', requiresAuth: true }
  },
  {
    path: '/notification/:id',
    name: 'NotificationDetail',
    component: () => import('@/views/NotificationDetail.vue'),
    meta: { title: '通知详情', requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('@/views/Notifications.vue'),
    meta: { title: '通知公告', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || '高校知识库智能答疑系统'}`

  // 只从sessionStorage读取token，关闭浏览器后自动失效
  const token = sessionStorage.getItem('token')
  
  const requiresAuth = to.meta.requiresAuth !== false
  const requiresAdmin = to.meta.requiresAdmin === true

  console.log('路由守卫:', { path: to.path, hasToken: !!token, requiresAuth })

  // 如果URL参数中有force=true,强制清除token并跳转到登录页
  if (to.query.force === 'true') {
    console.log('强制清除token,跳转到登录页')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('userInfo')
    // 重定向到登录页,不带force参数
    next({ path: '/login', query: {} })
    return
  }

  // 已登录用户访问登录页面的处理（不包括根路径）
  // 注意：/admin/login 页面不进行自动跳转，允许已登录用户访问以重新进行管理员登录
  if (to.path === '/login' && token) {
    console.log('已登录用户访问登录页，跳转到对应首页')

    // 只从sessionStorage读取用户信息
    const userInfoStr = sessionStorage.getItem('userInfo')
    const userInfo = JSON.parse(userInfoStr || '{}')

    // 检查是否是管理员
    if (userInfo.role === 'admin') {
      // 管理员用户，跳转到管理后台
      next('/admin')
    } else {
      // 普通用户，跳转到首页
      next('/home')
    }
    return
  }

  // 需要认证的页面:没有token则跳转到登录
  if (requiresAuth && !token) {
    console.log('需要认证但无token,跳转到登录页')
    next('/login')
    return
  }

  // 需要管理员权限的页面
  if (requiresAdmin && token) {
    // 只从sessionStorage读取用户信息
    const userInfoStr = sessionStorage.getItem('userInfo')
    const userInfo = JSON.parse(userInfoStr || '{}')
    
    if (userInfo.role !== 'admin') {
      ElMessage.error('您不是管理员，无法访问管理后台')
      next('/home')
      return
    }
  }

  // 管理员不能访问普通用户页面（除了管理后台、欢迎页面和个人中心）
  if (token) {
    // 只从sessionStorage读取用户信息
    const userInfoStr = sessionStorage.getItem('userInfo')
    const userInfo = JSON.parse(userInfoStr || '{}')

    // 如果是管理员，且不是访问管理后台相关页面、欢迎页面或个人中心，则重定向到管理后台
    if (userInfo.role === 'admin' &&
        !to.path.startsWith('/admin') &&
        to.path !== '/admin/login' &&
        to.path !== '/' &&
        to.path !== '/profile') {
      console.log('管理员访问非管理页面，重定向到管理后台')
      next('/admin')
      return
    }
  }

  console.log('允许访问:', to.path)
  next()
})

export default router
