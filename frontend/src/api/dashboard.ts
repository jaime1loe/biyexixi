import request from './index'

export interface StatisticsOverview {
  question_count: number
  answer_count: number
  ask_count: number
  user_count: number
  knowledge_count: number
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

export interface Activity {
  id: number
  user_id: number
  username: string
  user_role: string
  action_type: string
  target_type?: string
  target_id?: number
  target_name?: string
  details?: string
  created_at: string
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
    return request.get<any, any[]>('/statistics/top-questions', {
      params: { limit }
    })
  },

  getRecentActivities: (limit: number = 10) => {
    return request.get<any, Activity[]>('/activities/recent', {
      params: { limit }
    })
  }
}

// 兼容旧的命名方式
export const dashboardApi = statisticsApi
