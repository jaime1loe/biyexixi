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
    // 使用 sessionStorage 而不是 localStorage,关闭浏览器后自动清除
    sessionStorage.setItem('userInfo', JSON.stringify(info))
  }

  function setToken(newToken: string) {
    token.value = newToken
    // 使用 sessionStorage 而不是 localStorage,关闭浏览器后自动清除
    sessionStorage.setItem('token', newToken)
  }

  function logout() {
    userInfo.value = null
    token.value = ''
    sessionStorage.removeItem('userInfo')
    sessionStorage.removeItem('token')
  }

  function initFromStorage() {
    // 只从 sessionStorage 读取,不再从 localStorage 读取
    const storedUser = sessionStorage.getItem('userInfo')
    const storedToken = sessionStorage.getItem('token')
    if (storedUser) userInfo.value = JSON.parse(storedUser)
    if (storedToken) token.value = storedToken
  }

  initFromStorage()

  return { userInfo, token, setUserInfo, setToken, logout }
})
