import request from './index'
import type { AxiosResponse } from 'axios'

export interface Course {
  id: number
  course_code: string
  course_name: string
  credits: number
  hours: number
  teacher_name?: string
  teacher_id?: number
  department: string
  course_type: string
  capacity: number
}

export interface CourseCreate {
  course_code: string
  course_name: string
  teacher_id?: number
  department: string
  credits: number
  hours: number
  course_type: string
  capacity: number
}

export interface CourseUpdate {
  course_code?: string
  course_name?: string
  teacher_id?: number
  department?: string
  credits?: number
  hours?: number
  course_type?: string
  capacity?: number
}

export interface Teacher {
  id: number
  username: string
  real_name?: string
}

// 获取所有课程
export const getCourses = (params?: {
  department?: string
  course_type?: string
  search?: string
  skip?: number
  limit?: number
}): Promise<AxiosResponse<any>> => {
  return request.get('/course-management', { params })
}

// 获取课程详情
export const getCourse = (courseId: number, semester?: string): Promise<AxiosResponse<Course>> => {
  return request.get(`/course-management/${courseId}`, {
    params: { semester }
  })
}

// 创建课程
export const createCourse = (data: CourseCreate): Promise<AxiosResponse<Course>> => {
  return request.post('/course-management', data)
}

// 更新课程
export const updateCourse = (
  courseId: number,
  data: CourseUpdate
): Promise<AxiosResponse<Course>> => {
  return request.put(`/course-management/${courseId}`, data)
}

// 删除课程
export const deleteCourse = (courseId: number): Promise<AxiosResponse<void>> => {
  return request.delete(`/course-management/${courseId}`)
}

// 获取教师列表
export const getTeachers = (): Promise<AxiosResponse<Teacher[]>> => {
  return request.get('/course-management/teachers/list')
}
