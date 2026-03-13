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

  function setUserInfo(info: UserInfo) {
    userInfo.value = info
    // 使用 localStorage 确保登录状态持久化
    localStorage.setItem('userInfo', JSON.stringify(info))
    sessionStorage.setItem('userInfo', JSON.stringify(info)) // 同时存储到sessionStorage
  }

  function setToken(newToken: string) {
    token.value = newToken
    // 使用 localStorage 确保登录状态持久化
    localStorage.setItem('token', newToken)
    sessionStorage.setItem('token', newToken) // 同时存储到sessionStorage
  }

  function logout() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
    sessionStorage.removeItem('userInfo')
    sessionStorage.removeItem('token')
  }

  function initFromStorage() {
    // 优先从sessionStorage读取，如果没有则从localStorage读取
    let storedUser = sessionStorage.getItem('userInfo')
    let storedToken = sessionStorage.getItem('token')
    
    if (!storedUser) storedUser = localStorage.getItem('userInfo')
    if (!storedToken) storedToken = localStorage.getItem('token')
    
    if (storedUser) userInfo.value = JSON.parse(storedUser)
    if (storedToken) token.value = storedToken
  }

  initFromStorage()

  return { userInfo, token, setUserInfo, setToken, logout }
})
