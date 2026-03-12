import request from './index'

export interface EmptyClassroom {
  building: string
  room: string
}

export interface Grade {
  course: string
  score: number
  credit: number
  semester: string
}

export interface Book {
  id: number
  title: string
  author: string
  category: string
  location: string
  available: boolean
}

export const campusApi = {
  // 查询空教室
  getEmptyClassrooms: (params?: { building?: string }) => {
    return request.get('/campus/empty-classrooms', { params })
  },

  // 查询成绩
  getGrades: () => {
    return request.get('/campus/grades')
  },

  // 获取图书馆信息
  getLibraryInfo: () => {
    return request.get('/campus/library/info')
  },

  // 查询图书
  searchBooks: (params?: { keyword?: string; category?: string }) => {
    return request.get('/campus/library/books', { params })
  },

  // 获取图书分类
  getBookCategories: () => {
    return request.get('/campus/library/categories')
  },

  // 获取图书详情
  getBookDetail: (bookId: number) => {
    return request.get(`/campus/library/books/${bookId}`)
  }
}
