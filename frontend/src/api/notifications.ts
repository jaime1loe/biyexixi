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
  publisher?: string
  views?: number
}

export interface NotificationCreate {
  title: string
  content?: string
  category?: string
  is_important?: number
}

export const notificationApi = {
  // 创建通知
  create: (data: NotificationCreate) => {
    return request.post<any, Notification>('/notifications', data)
  },

  // 获取通知列表
  getList: (params?: { skip?: number; limit?: number; category?: string; is_important?: boolean }) => {
    return request.get<any, Notification[]>('/notifications', { params })
  },

  // 获取通知详情
  getDetail: (id: number) => {
    return request.get<any, Notification>(`/notifications/${id}`)
  },

  // 删除通知
  remove: (id: number) => {
    return request.delete(`/notifications/${id}`)
  },

  // 下载附件
  download: (id: number) => {
    return request.get(`/notifications/${id}/download`, { responseType: 'blob' })
  },

  // 获取分类列表
  getCategories: () => {
    return request.get('/notifications/categories/list')
  }
}
