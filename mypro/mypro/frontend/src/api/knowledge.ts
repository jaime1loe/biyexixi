import request from './index'

export interface Knowledge {
  id: number
  title: string
  content: string
  category?: string
  tags?: string
  file_path?: string
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
  }
}
