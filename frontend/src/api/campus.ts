import request from './index'

export interface EmptyClassroom {
  building: string
  room: string
}

export interface Grade {
  id?: number
  student_id?: number
  course_id?: number
  semester: string
  course_code: string
  course_name: string
  credits: number
  score: number
  grade_point: number
  grade_level: string
  is_makeup: boolean
  gpa?: number
  course?: {
    id: number
    course_code: string
    course_name: string
    credits?: number
  }
}

export interface GradeUpload {
  student_ids: number[]
  course_id: number
  semester: string
  scores: number[]
}

export interface Course {
  id: number
  course_code: string
  course_name: string
  semester: string
  credits: number
  student_count?: number
}

export interface StudentWithGrade {
  student_id: number
  student_name: string
  student_number?: string
  score?: number
  grade_level?: string
  is_makeup: boolean
  grade_id?: number
}

export interface Book {
  id: number
  title: string
  author: string
  publisher: string
  publish_year: number
  isbn: string
  category: string
  location: string
  total_copies: number
  available_copies: number
  status: string
  language: string
  pages: number
  price: number
  description?: string
}

export interface Seat {
  id: number
  seat_number: string
  floor: number
  area: string
  seat_type: string
  status: string
  is_available: boolean
}

export interface SeatReservation {
  id: number
  seat_id: number
  seat_number: string
  floor: number
  area: string
  reservation_date: string
  start_time: string
  end_time: string
  status: string
  check_in_time: string
  check_out_time: string
  created_at: string
}

export interface SeatStats {
  total: number
  available: number
  occupied: number
  reserved: number
}

export const campusApi = {
  // 查询空教室
  getEmptyClassrooms: (params?: { building?: string }) => {
    return request.get('/campus/empty-classrooms', { params })
  },

  // 学生：查询我的成绩
  getMyGrades: (semester?: string, course_name?: string) => {
    return request.get<any, Grade[]>('/grades/student/my', { params: { semester, course_name } })
  },

  // 教师：获取所授课程列表
  getTeacherCourses: (semester?: string, course_name?: string) => {
    return request.get<any, Course[]>('/grades/teacher/courses', { params: { semester, course_name } })
  },

  // 教师：获取课程学生列表
  getCourseStudents: (course_id: number, semester: string) => {
    return request.get<any, StudentWithGrade[]>(`/grades/teacher/course/${course_id}/students`, {
      params: { semester }
    })
  },

  // 教师：上传学生成绩
  uploadGrades: (data: GradeUpload) => {
    return request.post<any, any>('/grades/teacher/upload', data)
  },

  // 教师：更新学生成绩
  updateGrade: (grade_id: number, data: { score?: number; is_makeup?: boolean }) => {
    return request.put<any, any>(`/grades/teacher/grade/${grade_id}`, data)
  },

  // 教师：删除学生成绩
  deleteGrade: (grade_id: number) => {
    return request.delete<any, any>(`/grades/teacher/grade/${grade_id}`)
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
  },

  // ===== 座位相关 =====

  // 获取楼层列表
  getFloors: () => {
    return request.get<any, { floors: number[] }>('/campus/library/floors')
  },

  // 获取区域列表
  getAreas: () => {
    return request.get<any, { areas: string[] }>('/campus/library/areas')
  },

  // 查询座位
  getSeats: (params?: { floor?: number; area?: string; seat_type?: string }) => {
    return request.get<any, { seats: Seat[]; total: number; available: number; occupied: number; reserved: number }>('/campus/library/seats', { params })
  },

  // 预约座位
  reserveSeat: (seatId: number, data: { reservation_date: string; start_time: string; end_time: string }) => {
    return request.post(`/campus/library/seats/${seatId}/reserve`, data)
  },

  // 座位签到
  checkInSeat: (seatId: number) => {
    return request.post(`/campus/library/seats/${seatId}/checkin`)
  },

  // 取消预约
  cancelReservation: (reservationId: number) => {
    return request.delete(`/campus/library/reservations/${reservationId}`)
  },

  // 获取我的预约
  getMyReservations: () => {
    return request.get<any, { reservations: SeatReservation[] }>('/campus/library/my-reservations')
  }
}
