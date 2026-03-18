-- 创建课程评价表
CREATE TABLE IF NOT EXISTS course_evaluations (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评价ID',
    student_id INT NOT NULL COMMENT '学生ID',
    course_id INT NOT NULL COMMENT '课程ID',
    teacher_id INT NOT NULL COMMENT '教师ID',
    semester VARCHAR(20) NOT NULL COMMENT '学期：2024-2025-1',

    -- 评价维度（1-5分）
    teaching_quality INT COMMENT '教学质量 1-5',
    course_content INT COMMENT '课程内容 1-5',
    teacher_attitude INT COMMENT '教师态度 1-5',
    difficulty INT COMMENT '课程难度 1-5',
    workload INT COMMENT '作业量 1-5',

    -- 总体评分（1-5分）
    overall_rating FLOAT COMMENT '总体评分 1-5',

    -- 文字评价
    comment TEXT COMMENT '评价内容',

    -- 推荐
    is_recommended INT DEFAULT 0 COMMENT '是否推荐：1=推荐, 0=不推荐',

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '评价时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    INDEX idx_student_id (student_id),
    INDEX idx_course_id (course_id),
    INDEX idx_teacher_id (teacher_id),
    INDEX idx_semester (semester),
    UNIQUE KEY uk_student_course_semester (student_id, course_id, semester),

    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程评价表';

-- 添加evaluations关系到courses表（如果需要）
ALTER TABLE courses ADD INDEX idx_teacher_id (teacher_id);
