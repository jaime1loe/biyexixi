import { defineStore } from 'pinia'
import { ref } from 'vue'

interface UserInfo {
  id?: number
  username: string
  role: string
  avatar?: string
  realName?: string
  email?: string
  phone?: string
  studentId?: string
  department?: string
  major?: string
  bio?: string
}

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string>('')
  const isAdminLogin = ref<boolean>(false)

  function setUserInfo(info: UserInfo) {
    userInfo.value = info
    // 检查是否是管理员登录
    if (info.role === 'admin') {
      isAdminLogin.value = true
      sessionStorage.setItem('isAdminLogin', 'true')
    } else {
      isAdminLogin.value = false
      sessionStorage.removeItem('isAdminLogin')
    }
    
    // 只使用 sessionStorage，关闭浏览器后自动失效
    sessionStorage.setItem('userInfo', JSON.stringify(info))
  }

  function setToken(newToken: string) {
    token.value = newToken
    // 只使用 sessionStorage，关闭浏览器后自动失效
    sessionStorage.setItem('token', newToken)
  }

  function logout() {
    userInfo.value = null
    token.value = ''
    isAdminLogin.value = false
    sessionStorage.removeItem('userInfo')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('isAdminLogin')
  }

  function clearUserInfo() {
    userInfo.value = null
    token.value = ''
    isAdminLogin.value = false
    sessionStorage.removeItem('userInfo')
    sessionStorage.removeItem('token')
    sessionStorage.removeItem('isAdminLogin')
  }

  function initFromStorage() {
    // 只从sessionStorage读取，关闭浏览器后自动失效
    const storedUser = sessionStorage.getItem('userInfo')
    const storedToken = sessionStorage.getItem('token')
    
    if (storedUser) {
      userInfo.value = JSON.parse(storedUser)
      // 检查是否是管理员
      if (userInfo.value?.role === 'admin') {
        isAdminLogin.value = sessionStorage.getItem('isAdminLogin') === 'true'
      }
    }
    if (storedToken) token.value = storedToken
  }

  initFromStorage()

  return { 
    userInfo, 
    token, 
    isAdminLogin,
    setUserInfo, 
    setToken, 
    logout, 
    clearUserInfo 
  }
})
