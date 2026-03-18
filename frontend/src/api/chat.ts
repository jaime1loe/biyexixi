import request from './index'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

export interface QuestionRequest {
  question: string
  category?: string
}

export interface Question {
  id: number
  user_id: number
  question: string
  answer?: string
  category?: string
  created_at: string
  updated_at?: string
}

export interface FeedbackRequest {
  question_id: number
  rating: number
  comment?: string
}

export const chatApi = {
  sendMessage: (data: QuestionRequest) => {
    return request.post<any, Question>('/questions/', data)
  },

  getMyQuestions: (params: { skip?: number; limit?: number }) => {
    return request.get<any, Question[]>('/questions/my', { params })
  },

  getQuestions: (params: { skip?: number; limit?: number; category?: string }) => {
    return request.get<any, Question[]>('/questions/', { params })
  },

  getQuestion: (id: number) => {
    return request.get<any, Question>(`/questions/${id}`)
  },

  submitFeedback: (data: FeedbackRequest) => {
    return request.post('/feedback/', data)
  },

  // 导出CSV
  exportCSV: () => {
    return request.get('/questions/export/csv', { responseType: 'blob' })
  },

  // 导出Excel
  exportExcel: () => {
    return request.get('/questions/export/excel', { responseType: 'blob' })
  }
}

