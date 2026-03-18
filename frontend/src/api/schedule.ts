import request from './index'

export interface Classroom {
  id: number
  building: string
  room_number: string
  capacity: number
  room_type: string
  equipment?: string
  floor?: number
  is_available: number
  created_at: string
  updated_at: string
}

export interface Course {
  id: number
  course_code: string
  course_name: string
  teacher_name?: string
  department?: string
  credits?: number
  hours?: number
  course_type: string
  created_at: string
  updated_at: string
}

export interface Schedule {
  id: number
  classroom_id: number
  course_id: number
  day_of_week: number
  period: number
  week_start: number
  week_end: number
  semester: string
  class_name?: string
  classroom?: Classroom
  course?: Course
  created_at: string
  updated_at: string
}

export interface ClassroomStatus {
  classroom: Classroom
  is_available: boolean
  occupied_courses?: Schedule[]
}

export const scheduleApi = {
  // 获取所有教室
  getClassrooms: (params?: {
    building?: string
    room_type?: string
    min_capacity?: number
  }) => {
    return request.get<any, Classroom[]>('/classrooms', { params })
  },

  // 获取教室详情
  getClassroom: (id: number) => {
    return request.get<any, Classroom>(`/classrooms/${id}`)
  },

  // 获取教室课表
  getClassroomSchedule: (id: number, semester?: string) => {
    return request.get<any, Schedule[]>(`/classrooms/${id}/schedule`, {
      params: { semester }
    })
  },

  // 获取教室状态
  getClassroomStatus: (
    id: number,
    day_of_week: number,
    period: number,
    week?: number,
    semester?: string
  ) => {
    return request.get<any, ClassroomStatus>(`/classrooms/${id}/status`, {
      params: { day_of_week, period, week, semester }
    })
  },

  // 查询空教室
  getAvailableClassrooms: (params: {
    day_of_week: number
    period: number
    week?: number
    semester?: string
    building?: string
    min_capacity?: number
    room_type?: string
  }) => {
    return request.get<any, Classroom[]>('/available-classrooms', { params })
  },

  // 获取所有教学楼
  getBuildings: () => {
    return request.get<any, { buildings: string[] }>('/buildings')
  },

  // 获取所有节次
  getPeriods: () => {
    return request.get<any, { periods: Array<{ value: number; label: string; time: string }> }>(
      '/periods'
    )
  },

  // 获取所有星期
  getWeekdays: () => {
    return request.get<any, { days: Array<{ value: number; label: string }> }>(
      '/weekdays'
    )
  },

  // 获取所有课程
  getCourses: (params?: {
    department?: string
    course_type?: string
  }) => {
    return request.get<any, Course[]>('/courses', { params })
  },

  // 获取课程详情
  getCourse: (id: number) => {
    return request.get<any, Course>(`/courses/${id}`)
  },

  // 获取课程课表
  getCourseSchedule: (id: number, semester?: string) => {
    return request.get<any, Schedule[]>(`/courses/${id}/schedule`, {
      params: { semester }
    })
  },

  // 获取所有排课
  getSchedules: (params?: {
    semester?: string
    day_of_week?: number
    period?: number
  }) => {
    return request.get<any, Schedule[]>('/schedules', { params })
  }
}
