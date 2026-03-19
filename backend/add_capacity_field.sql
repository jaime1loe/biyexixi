-- 为课程表添加容量字段
ALTER TABLE courses ADD COLUMN capacity INT DEFAULT 100 COMMENT '课程容量';

-- 更新现有课程容量（如果需要）
-- UPDATE courses SET capacity = 100 WHERE capacity IS NULL;

-- 为课程表添加索引
CREATE INDEX idx_courses_capacity ON courses(capacity);
