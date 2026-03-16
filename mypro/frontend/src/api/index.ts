import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

request.interceptors.request.use(
  (config) => {
    // 只从sessionStorage读取token，关闭浏览器后自动失效
    const token = sessionStorage.getItem('token')
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('请求携带token:', token.substring(0, 20) + '...')
    } else {
      console.log('请求未携带token，用户可能未登录')
    }
    
    console.log('请求配置:', config.method?.toUpperCase(), config.url)
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
    // 检查是否需要抑制错误消息显示
    const suppressError = error.config?.suppressErrorMessage

    // 处理401未授权错误 - 只显示错误信息，不自动跳转
    if (error.response?.status === 401) {
      console.log('检测到401错误，显示错误信息但不跳转')
      if (!suppressError) {
        ElMessage.error('认证失败：' + (error.response?.data?.detail || '请检查登录状态'))
      }
      return Promise.reject(error)
    }

    // 如果设置了 suppressErrorMessage 标记，则不显示错误消息
    if (!suppressError) {
      ElMessage.error(error.response?.data?.detail || error.response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
