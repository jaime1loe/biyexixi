import request from './index'

// ========== 课程评价相关类型定义 ==========

export interface CourseEvaluation {
  id: number
  student_id: number
  student_name: string
  course_id: number
  course_name: string
  course_code: string
  teacher_id: number
  teacher_name: string
  semester: string
  teaching_quality: number
  course_content: number
  teacher_attitude: number
  difficulty: number
  workload: number
  overall_rating: number
  comment: string
  is_recommended: number
  created_at: string
}

export interface CourseEvaluationStats {
  course_id: number
  course_name: string
  teacher_name: string
  semester: string
  total_evaluations: number
  average_ratings: {
    teaching_quality: number
    course_content: number
    teacher_attitude: number
    difficulty: number
    workload: number
    overall_rating: number
  }
  recommendation_rate: number
}

export interface CourseEvaluationCreate {
  course_id: number
  semester: string
  teaching_quality: number
  course_content: number
  teacher_attitude: number
  difficulty: number
  workload: number
  overall_rating: number
  comment: string
  is_recommended: number
}

export interface CourseEvaluationUpdate {
  teaching_quality?: number
  course_content?: number
  teacher_attitude?: number
  difficulty?: number
  workload?: number
  overall_rating?: number
  comment?: string
  is_recommended?: number
}

// ========== 课程评价API ==========

export const evaluationApi = {
  // 学生：提交课程评价
  createEvaluation: (data: CourseEvaluationCreate) => {
    return request.post<any, CourseEvaluation>('/evaluations', data)
  },

  // 学生：查询自己的评价
  getMyEvaluations: (semester?: string) => {
    return request.get<any, CourseEvaluation[]>('/evaluations/my-evaluations', {
      params: { semester }
    })
  },

  // 教师/学生：查询指定课程的评价
  getCourseEvaluations: (courseId: number, semester?: string) => {
    return request.get<any, CourseEvaluation[]>(`/evaluations/course/${courseId}`, {
      params: { semester }
    })
  },

  // 教师：查询自己课程的评价统计
  getTeacherCourseStats: (semester?: string) => {
    return request.get<any, CourseEvaluationStats[]>('/evaluations/teacher/my-courses-stats', {
      params: { semester }
    })
  },

  // 学生：修改评价
  updateEvaluation: (evaluationId: number, data: CourseEvaluationUpdate) => {
    return request.put<any, CourseEvaluation>(`/evaluations/${evaluationId}`, data)
  },

  // 学生：删除评价
  deleteEvaluation: (evaluationId: number) => {
    return request.delete(`/evaluations/${evaluationId}`)
  }
}
