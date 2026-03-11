import request from './index'

export interface Favorite {
  id: number
  user_id: number
  question_id: number
  question?: any
  created_at: string
}

export interface FavoriteCreate {
  question_id: number
}

export const favoritesApi = {
  // 收藏问题
  add: (data: FavoriteCreate) => {
    return request.post<any, Favorite>('/favorites', data)
  },

  // 取消收藏
  remove: (favoriteId: number) => {
    return request.delete(`/favorites/${favoriteId}`)
  },

  // 获取我的收藏列表
  getList: (params?: { skip?: number; limit?: number }) => {
    return request.get<any, Favorite[]>('/favorites', { params })
  },

  // 检查是否已收藏
  check: (questionId: number) => {
    return request.get(`/favorites/check/${questionId}`)
  }
}
