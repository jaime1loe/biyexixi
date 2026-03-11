import request from './index'

export interface StatisticsOverview {
  total_questions: number
  total_users: number
  total_knowledge: number
  avg_rating: number
  today_questions: number
  today_users: number
  week_questions: number
}

export interface DailyStatistics {
  date: string
  question_count: number
  user_count: number
  avg_rating: number
}

export interface CategoryStatistics {
  categories: Array<{ category: string; count: number }>
}

export const statisticsApi = {
  getOverview: () => {
    return request.get<any, StatisticsOverview>('/statistics/overview')
  },

  getDaily: (days: number = 7) => {
    return request.get<any, DailyStatistics[]>('/statistics/daily', {
      params: { days }
    })
  },

  getCategoryStats: () => {
    return request.get<any, CategoryStatistics>('/statistics/category')
  },

  getTopQuestions: (limit: number = 10) => {
    return request.get<any, any[]>('/statistics/top-questions', {
      params: { limit }
    })
  },

  getPopularQuestions: (limit: number = 8) => {
    return request.get<any, any[]>('/statistics/popular-questions', {
      params: { limit }
    })
  }
}

// 兼容旧的命名方式
export const dashboardApi = statisticsApi
