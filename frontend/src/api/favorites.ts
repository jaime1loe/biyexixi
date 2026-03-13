import request from './index'

export interface FavoriteResponse {
  id: number
  user_id: number
  question_id: number
  question?: string
  answer?: string
  created_at: string
}

export interface FavoriteCreate {
  question_id: number
}

export const favoritesApi = {
  // 收藏问题
  add: (data: FavoriteCreate) => {
    return request.post<any, FavoriteResponse>('/favorites/', data)
  },

  // 取消收藏
  remove: (favoriteId: number) => {
    return request.delete(`/favorites/${favoriteId}`)
  },

  // 获取我的收藏列表
  getList: (params?: { skip?: number; limit?: number }) => {
    return request.get<any, FavoriteResponse[]>('/favorites/', { params })
  },

  // 检查是否已收藏
  check: (questionId: number) => {
    return request.get(`/favorites/check/${questionId}`)
  },

  // 获取我的收藏列表（兼容旧版本）
  getAll: () => {
    return request.get<any, FavoriteResponse[]>('/favorites/')
  }
}
