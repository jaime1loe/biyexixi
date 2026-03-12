import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

request.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // 处理401未授权错误 - 只显示错误信息，不自动跳转
    if (error.response?.status === 401) {
      console.log('检测到401错误，显示错误信息但不跳转')
      ElMessage.error('认证失败：' + (error.response?.data?.detail || '请检查登录状态'))
    }
    
    ElMessage.error(error.response?.data?.detail || error.response?.data?.message || '请求失败')
    return Promise.reject(error)
  }
)

export default request
