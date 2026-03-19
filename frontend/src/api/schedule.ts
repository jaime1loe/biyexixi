import request from './index'
import type { AxiosResponse } from 'axios'

// 教室相关
export interface Classroom {
  id: number
  building: string
  room_number: string
  capacity: number
  room_type: string
  equipment: string
  floor: number
  is_available: number
  created_at: string
  updated_at: string
}

// 课程相关
export interface Course {
  id: number
  course_code: string
  course_name: string
  credits: number
  hours: number
  teacher_name?: string
  department: string
  course_type: string
  capacity: number
}

// 排课相关
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

export interface ScheduleCreate {
  classroom_id: number
  course_id: number
  day_of_week: number
  period: number
  week_start: number
  week_end: number
  semester: string
  class_name?: string
}

export interface ScheduleUpdate {
  classroom_id?: number
  course_id?: number
  day_of_week?: number
  period?: number
  week_start?: number
  week_end?: number
  semester?: string
  class_name?: string
}

export interface Period {
  value: number
  label: string
  time: string
}

export interface Weekday {
  value: number
  label: string
}

// 获取所有教室
export const getClassrooms = (params?: {
  building?: string
  room_type?: string
  min_capacity?: number
}): Promise<AxiosResponse<Classroom[]>> => {
  return request.get('/classrooms', { params })
}

// 获取教室详情
export const getClassroom = (classroomId: number): Promise<AxiosResponse<Classroom>> => {
  return request.get(`/classrooms/${classroomId}`)
}

// 获取教室课表
export const getClassroomSchedule = (
  classroomId: number,
  semester?: string
): Promise<AxiosResponse<Schedule[]>> => {
  return request.get(`/classrooms/${classroomId}/schedule`, {
    params: { semester }
  })
}

// 获取教室状态
export const getClassroomStatus = (
  classroomId: number,
  dayOfWeek: number,
  period: number,
  week: number = 1,
  semester?: string
): Promise<AxiosResponse<any>> => {
  return request.get(`/classrooms/${classroomId}/status`, {
    params: {
      day_of_week: dayOfWeek,
      period,
      week,
      semester
    }
  })
}

// 获取空闲教室
export const getAvailableClassrooms = (params: {
  day_of_week: number
  period: number
  week?: number
  semester?: string
  building?: string
  min_capacity?: number
  room_type?: string
}): Promise<AxiosResponse<Classroom[]>> => {
  return request.get('/available-classrooms', { params })
}

// 获取所有课程
export const getCourses = (params?: {
  department?: string
  course_type?: string
}): Promise<AxiosResponse<Course[]>> => {
  return request.get('/courses', { params })
}

// 获取课程详情
export const getCourse = (courseId: number): Promise<AxiosResponse<Course>> => {
  return request.get(`/courses/${courseId}`)
}

// 获取课程课表
export const getCourseSchedule = (
  courseId: number,
  semester?: string
): Promise<AxiosResponse<Schedule[]>> => {
  return request.get(`/courses/${courseId}/schedule`, {
    params: { semester }
  })
}

// 获取所有排课
export const getSchedules = (params?: {
  semester?: string
  day_of_week?: number
  period?: number
}): Promise<AxiosResponse<Schedule[]>> => {
  return request.get('/schedules', { params })
}

// 创建排课
export const createSchedule = (data: ScheduleCreate): Promise<AxiosResponse<Schedule>> => {
  return request.post('/schedules', data)
}

// 更新排课
export const updateSchedule = (
  scheduleId: number,
  data: ScheduleUpdate
): Promise<AxiosResponse<Schedule>> => {
  return request.put(`/schedules/${scheduleId}`, data)
}

// 删除排课
export const deleteSchedule = (scheduleId: number): Promise<AxiosResponse<void>> => {
  return request.delete(`/schedules/${scheduleId}`)
}

// 获取所有教学楼
export const getBuildings = (): Promise<AxiosResponse<{ buildings: string[] }>> => {
  return request.get('/buildings')
}

// 获取所有节次
export const getPeriods = (): Promise<AxiosResponse<{ periods: Period[] }>> => {
  return request.get('/periods')
}

// 获取所有星期
export const getWeekdays = (): Promise<AxiosResponse<{ days: Weekday[] }>> => {
  return request.get('/weekdays')
}
