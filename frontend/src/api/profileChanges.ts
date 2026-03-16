import request from './index'

export const profileChangesApi = {
  // 提交信息修改申请
  submit: (data: any) => {
    return request.post('/profile-changes/submit', data)
  },

  // 获取我的修改申请记录
  getMyRequests: () => {
    return request.get('/profile-changes/my-requests', {
      suppressErrorMessage: true  // 抑制错误消息显示
    })
  },

  // 获取待审核的申请（管理员）
  getPending: () => {
    return request.get('/profile-changes/pending')
  },

  // 获取所有申请（管理员）
  getAll: (params?: any) => {
    return request.get('/profile-changes/all', { params })
  },

  // 审核申请（管理员）
  review: (id: number, data: any) => {
    return request.post(`/profile-changes/review/${id}`, data)
  },

  // 删除修改申请
  deleteRequest: (id: number) => {
    return request.delete(`/profile-changes/${id}`)
  }
}
