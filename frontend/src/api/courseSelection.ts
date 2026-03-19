import request from './index'

// ========== 选课相关类型定义 ==========

export interface CourseSelection {
  id: number
  student_id: number
  course_id: number
  course_code: string
  course_name: string
  teacher_id?: number
  teacher_name: string
  semester: string
  status: string
  selected_at: string
  dropped_at?: string | null
  course_type?: string
  credits?: number
  hours?: number
  department?: string
}

export interface CourseWithSelectionStatus {
  id: number
  course_code: string
  course_name: string
  teacher_id?: number
  teacher_name?: string
  department?: string
  credits?: number
  hours?: number
  course_type?: string
  capacity?: number
  selected_count?: number
  remaining_count?: number
  is_selected: boolean
  selection_status?: string | null
}

export interface CourseSelectionCreate {
  course_id: number
  semester: string
}

export interface CourseManagementRequest {
  course_name: string
  course_code: string
  teacher_id: number
  department?: string
  credits?: number
  hours?: number
  course_type: string
}

export interface CourseManagementResponse {
  id: number
  course_code: string
  course_name: string
  teacher_id: number
  teacher_name: string
  department?: string
  credits?: number
  hours?: number
  course_type: string
  selection_count?: number
  created_at?: string
  updated_at?: string
}

export interface CourseStudent {
  student_id: number
  student_name: string
  student_number?: string
  department?: string
  major?: string
  class_name?: string
  selected_at: string
  selection_id: number
}

export interface TeacherCourseSelection {
  course_id: number
  course_code: string
  course_name: string
  course_type: string
  credits?: number
  hours?: number
  department?: string
  selection_count: number
  semester: string
}

export interface Teacher {
  id: number
  username: string
  real_name?: string
  department?: string
}

// ========== 选课API ==========

export const courseSelectionApi = {
  // 学生：查询可选课程
  getAvailableCourses: (params?: {
    semester?: string
    course_type?: string
    department?: string
    search?: string
  }) => {
    return request.get<CourseWithSelectionStatus[]>('/course-selection/available', { params })
  },

  // 学生：查询我的选课
  getMySelections: (params?: {
    semester?: string
    status?: string
  }) => {
    return request.get<CourseSelection[]>('/course-selection/my-courses', { params })
  },

  // 学生：选课
  selectCourse: (data: CourseSelectionCreate) => {
    return request.post<CourseSelection>('/course-selection/select', data)
  },

  // 学生：退选
  dropCourse: (selectionId: number) => {
    return request.delete(`/course-selection/${selectionId}`)
  },

  // 教师：查看课程选课学生
  getCourseStudents: (courseId: number, semester?: string) => {
    return request.get<CourseStudent[]>(`/course-selection/teacher/${courseId}/students`, {
      params: { semester }
    })
  },

  // 教师：查看自己的课程及选课情况
  getTeacherCourses: (semester?: string) => {
    return request.get<TeacherCourseSelection[]>('/course-selection/teacher/my-courses', {
      params: { semester }
    })
  }
}

// ========== 课程管理API ==========

export const courseManagementApi = {
  // 管理员：开设课程
  createCourse: (data: CourseManagementRequest) => {
    return request.post<CourseManagementResponse>('/course-management', data)
  },

  // 查询所有课程
  getAllCourses: (params?: {
    semester?: string
    course_type?: string
    department?: string
    teacher_id?: number
    search?: string
    skip?: number
    limit?: number
  }) => {
    return request.get<{ total: number; courses: CourseManagementResponse[] }>('/course-management', {
      params
    })
  },

  // 查询课程详情
  getCourseDetail: (courseId: number, semester?: string) => {
    return request.get<CourseManagementResponse>(`/course-management/${courseId}`, {
      params: { semester }
    })
  },

  // 更新课程信息
  updateCourse: (courseId: number, data: CourseManagementRequest) => {
    return request.put<CourseManagementResponse>(`/course-management/${courseId}`, data)
  },

  // 删除课程
  deleteCourse: (courseId: number) => {
    return request.delete(`/course-management/${courseId}`)
  },

  // 获取教师列表
  getTeachers: () => {
    return request.get<Teacher[]>('/course-management/teachers/list')
  }
}
