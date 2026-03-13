import request from './index'

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
  email?: string
  real_name?: string
  student_id?: string
  role: string
}

export interface UserInfo {
  id: number
  username: string
  real_name?: string
  student_id?: string
  email?: string
  role: string
  avatar?: string
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login: (data: LoginRequest) => {
    return request.post<any, AuthResponse>('/auth/login', data)
  },

  register: (data: RegisterRequest) => {
    return request.post<any, UserInfo>('/auth/register', data)
  },

  getCurrentUser: () => {
    return request.get<any, UserInfo>('/auth/me')
  },

  updateCurrentUser: (data: Partial<UserInfo>) => {
    return request.put<any, UserInfo>('/auth/me', data)
  },

  getUsers: (params?: { skip?: number; limit?: number; role?: string }) => {
    return request.get<any, UserInfo[]>('/auth/users', { params })
  }
}
