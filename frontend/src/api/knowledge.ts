import request from './index'

export interface Knowledge {
  id: number
  title: string
  content: string
  category?: string
  tags?: string
  status?: string
  // 审核相关字段
  uploader_id?: number
  reviewer_id?: number
  review_status?: string  // pending, approved, rejected
  rejection_reason?: string
  // 文件相关字段
  file_path?: string
  file_name?: string
  file_size?: number
  created_at: string
  updated_at?: string
}

export interface KnowledgeCreate {
  title: string
  content: string
  category?: string
  tags?: string
}

export const knowledgeApi = {
  create: (data: KnowledgeCreate) => {
    return request.post<any, Knowledge>('/knowledge/', data)
  },

  upload: (formData: FormData) => {
    return request.post<any, Knowledge>('/knowledge/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 添加分类
  addCategory: (name: string) => {
    const formData = new FormData()
    formData.append('name', name)
    return request.post<any, { success: boolean }>('/knowledge/categories', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // 删除分类
  deleteCategory: (name: string) => {
    return request.delete<any, { success: boolean }>(`/knowledge/categories?name=${encodeURIComponent(name)}`)
  },

  update: (id: number, data: Partial<KnowledgeCreate>) => {
    return request.put<any, Knowledge>(`/knowledge/${id}`, data)
  },

  delete: (id: number) => {
    return request.delete(`/knowledge/${id}`)
  },

  getList: (params: { skip?: number; limit?: number; category?: string }) => {
    return request.get<any, Knowledge[]>('/knowledge/', { params })
  },

  getById: (id: number) => {
    return request.get<any, Knowledge>(`/knowledge/${id}`)
  },

  search: (params: { keyword: string; category?: string }) => {
    return request.get<any, Knowledge[]>('/knowledge/search', { params })
  },

  getCategories: () => {
    return request.get<any, { categories: string[] }>('/knowledge/categories')
  },

  // 下载文件
  download: (id: number, fileName: string) => {
    return request.get(`/knowledge/${id}/download`, {
      responseType: 'blob'
    }).then(response => {
      const url = window.URL.createObjectURL(new Blob([response]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', fileName)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    })
  },

  // 获取待审核列表（管理员）
  getPending: () => {
    return request.get<any, Knowledge[]>('/knowledge/pending')
  },

  // 获取我的文档
  getMyDocuments: () => {
    return request.get<any, Knowledge[]>('/knowledge/my-documents')
  },

  // 审核知识（管理员）
  review: (id: number, action: 'approve' | 'reject', reason?: string) => {
    return request.post<any, { message: string; knowledge: Knowledge }>(`/knowledge/${id}/review`, {
      action,
      reason
    })
  }
}
