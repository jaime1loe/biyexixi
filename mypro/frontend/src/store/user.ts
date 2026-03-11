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
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function logout() {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('userInfo')
    localStorage.removeItem('token')
  }

  function initFromStorage() {
    const storedUser = localStorage.getItem('userInfo')
    const storedToken = localStorage.getItem('token')
    if (storedUser) userInfo.value = JSON.parse(storedUser)
    if (storedToken) token.value = storedToken
  }

  initFromStorage()

  return { userInfo, token, setUserInfo, setToken, logout }
})
