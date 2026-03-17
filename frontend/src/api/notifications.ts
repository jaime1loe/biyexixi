import request from './index'

export interface Notification {
  id: number
  title: string
  content?: string
  detail_content?: string
  category?: string
  is_important: number
  file_path?: string
  created_at: string
  updated_at: string
  published_at?: string
  schedule_time?: string
  status?: string
  publisher?: string
  views?: number
}

export interface NotificationCreate {
  title: string
  content?: string
  detail_content?: string
  category?: string
  is_important?: number
  publisher?: string
  schedule_time?: string
  status?: string
}

export interface NotificationUpdate {
  title?: string
  content?: string
  detail_content?: string
  category?: string
  is_important?: number
  publisher?: string
  schedule_time?: string
  status?: string
}

export const notificationApi = {
  // 创建通知（无需附件时使用JSON）
  create: (data: NotificationCreate) => {
    return request.post<any, Notification>('/notifications/', data)
  },

  // 创建通知（带附件）
  createWithFile: (data: NotificationCreate, file: File) => {
    const formData = new FormData()
    formData.append('notification_json', JSON.stringify(data))
    formData.append('file', file)
    return request.post<any, Notification>('/notifications/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 更新通知
  update: (id: number, data: NotificationUpdate) => {
    return request.put<any, Notification>(`/notifications/${id}/`, data)
  },

  // 更新通知（带附件）
  updateWithFile: (id: number, data: NotificationUpdate, file: File) => {
    const formData = new FormData()
    formData.append('notification_update', JSON.stringify(data))
    formData.append('file', file)
    return request.post<any, Notification>(`/notifications/${id}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 获取通知列表
  getList: (params?: { skip?: number; limit?: number; category?: string; is_important?: boolean; status?: string; include_scheduled?: boolean }) => {
    return request.get<any, Notification[]>('/notifications/', { params })
  },

  // 获取通知详情
  getDetail: (id: number) => {
    return request.get<any, Notification>(`/notifications/${id}/`)
  },

  // 删除通知
  remove: (id: number) => {
    return request.delete(`/notifications/${id}/`)
  },

  // 下载附件
  download: (id: number) => {
    return request.get(`/notifications/${id}/download`, { responseType: 'blob' })
  },

  // 获取分类列表
  getCategories: () => {
    return request.get('/notifications/categories/list')
  },

  // 获取待定时发布的通知列表
  getScheduledList: () => {
    return request.get('/notifications/scheduled/list')
  }
}
