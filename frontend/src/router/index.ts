import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录/注册', requiresAuth: false }
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
    meta: { title: '知识库管理', requiresAuth: true }
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
    component: () => import('@/views/Admin.vue'),
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

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || '高校知识库智能答疑系统'}`

  // 优先从sessionStorage读取token，如果没有则从localStorage读取
  let token = sessionStorage.getItem('token')
  if (!token) token = localStorage.getItem('token')
  
  const requiresAuth = to.meta.requiresAuth !== false
  const requiresAdmin = to.meta.requiresAdmin === true

  console.log('路由守卫:', { path: to.path, hasToken: !!token, requiresAuth })

  // 如果URL参数中有force=true,强制清除token并跳转到登录页
  if (to.query.force === 'true') {
    console.log('强制清除token,跳转到登录页')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('userInfo')
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    // 重定向到登录页,不带force参数
    next({ path: '/login', query: {} })
    return
  }

  // 登录页处理:如果有token,跳转到首页
  if (to.path === '/login' && token) {
    console.log('已登录,跳转到首页')
    next('/home')
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
    // 优先从sessionStorage读取用户信息，如果没有则从localStorage读取
    let userInfoStr = sessionStorage.getItem('userInfo')
    if (!userInfoStr) userInfoStr = localStorage.getItem('userInfo')
    const userInfo = JSON.parse(userInfoStr || '{}')
    
    if (userInfo.role !== 'admin') {
      next('/home')
      return
    }
  }

  console.log('允许访问:', to.path)
  next()
})

export default router
