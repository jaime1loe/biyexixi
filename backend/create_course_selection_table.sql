-- 创建选课表
CREATE TABLE IF NOT EXISTS course_selections (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '选课ID',
    student_id INT NOT NULL COMMENT '学生ID',
    course_id INT NOT NULL COMMENT '课程ID',
    semester VARCHAR(20) NOT NULL COMMENT '学期：2024-2025-1',
    status VARCHAR(20) DEFAULT 'selected' COMMENT '状态：selected=已选, dropped=退选, completed=已完成',
    selected_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '选课时间',
    dropped_at DATETIME COMMENT '退选时间',
    INDEX idx_student_id (student_id),
    INDEX idx_course_id (course_id),
    INDEX idx_semester (semester),
    INDEX idx_student_semester (student_id, semester),
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='选课表';
