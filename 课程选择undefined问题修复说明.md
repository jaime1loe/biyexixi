# 课程选择下拉框显示 undefined 的问题修复说明

## 问题描述
在课程评价功能中，"选择课程"下拉框显示的都是 `undefined`，无法正常显示课程名称和代码。

## 问题原因
后端服务器仍在运行旧版本的代码，没有加载最新的修改。由于 Python 的模块缓存机制，即使修改了源代码，运行中的服务器也不会自动更新。

## 解决方案

### 方案1：重启后端服务器（推荐）
这是最彻底的解决方案，可以确保所有最新代码都被加载。

**步骤：**
1. 停止当前运行的后端服务器
2. 清理 Python 缓存（可选，但推荐）：
   ```bash
   cd d:/毕业设计/backend
   del /s /q __pycache__
   ```
3. 重新启动后端服务器：
   ```bash
   python main.py
   ```

**验证：**
重启后，访问 `/api/grades/student/my` 端点，应该返回包含 `course_code` 和 `course_name` 字段的数据，而不是 `course: null`。

### 方案2：临时前端修复（不推荐）
如果暂时无法重启后端，可以在前端添加一个临时修复，处理 `course` 字段为 `null` 的情况。

**修改文件：** `frontend/src/views/Campus.vue`

在 `showSubmitEvaluation` 函数中，为课程列表添加额外的处理：

```typescript
const showSubmitEvaluation = async () => {
  // 确保已加载课程列表
  if (myGrades.value.length === 0) {
    await loadMyGrades()
  }
  if (myGrades.value.length === 0) {
    ElMessage.warning('您还没有任何课程成绩，无法评价')
    return
  }
  
  // 临时修复：如果 course_name 或 course_code 为 undefined，尝试从其他字段获取
  const processedGrades = myGrades.value.map(grade => ({
    ...grade,
    // 如果 course_name 是 undefined，显示 course_id
    course_name: grade.course_name || grade.course?.course_name || `课程ID: ${grade.course_id}`,
    course_code: grade.course_code || grade.course?.course_code || 'N/A',
    course_id: grade.course_id  // 确保使用正确的字段
  }))
  
  myGrades.value = processedGrades
  
  // 重置表单为新建模式
  evaluationForm.value = {
    course_id: 0,
    semester: '2024-2025-2',
    teaching_quality: 5,
    course_content: 5,
    teacher_attitude: 5,
    difficulty: 5,
    workload: 5,
    overall_rating: 5,
    comment: '',
    is_recommended: 1
  }
  submitEvaluationVisible.value = true
}
```

同时，更新下拉框的显示逻辑：

```vue
<el-form-item label="选择课程">
  <el-select v-model="evaluationForm.course_id" placeholder="请选择课程" style="width: 100%">
    <el-option
      v-for="course in myGrades"
      :key="course.course_id"
      :label="`${course.course_name || '未知课程'} (${course.course_code || 'N/A'})`"
      :value="course.course_id"
    />
  </el-select>
</el-form-item>
```

## 验证步骤

### 后端API验证
使用以下Python脚本验证后端是否返回正确的数据：

```python
import requests
import json

# 登录
login_data = {"username": "student1", "password": "123456"}
response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
token = response.json().get("access_token")

# 获取成绩
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/grades/student/my", headers=headers)
grades = response.json()

# 检查第一条记录
if grades:
    print("第一条成绩记录:")
    print(json.dumps(grades[0], indent=2, ensure_ascii=False))
    
    # 验证关键字段
    if 'course_code' in grades[0] and 'course_name' in grades[0]:
        print("\n✓ API 返回数据正确，包含 course_code 和 course_name")
    else:
        print("\n✗ API 返回数据不正确，需要重启后端服务器")
```

### 前端界面验证
1. 使用学生账号（student1）登录
2. 进入"校园服务" -> "课程评价"
3. 点击"提交新评价"
4. 检查"选择课程"下拉框：
   - **正确状态**：显示课程名称和代码，如 "计算机学院专业课程1 (01001)"
   - **错误状态**：显示 "undefined undefined" 或类似的错误文本

## 已完成的修复

### 后端修复（需要重启后端才能生效）
- 文件：`backend/app/routers/grades.py`
- 修改内容：
  1. 移除了 `response_model` 参数，避免 Pydantic 自动序列化导致的问题
  2. 直接构建字典返回，确保包含 `course_code` 和 `course_name` 字段
  3. 添加了调试日志，便于排查问题

### 数据验证
- 已通过直接测试验证，数据查询逻辑正确
- 可以成功获取课程信息并构建正确的响应数据

## 推荐操作顺序

1. **立即操作**：重启后端服务器
2. **验证**：使用上述验证脚本确认 API 返回正确数据
3. **测试**：通过前端界面验证课程选择下拉框正常显示
4. **完成**：提交评价并验证功能正常

## 注意事项

- 如果重启后端后仍然显示 `undefined`，请检查：
  - 后端服务器是否真的已重启
  - 是否清理了 `__pycache__` 目录
  - 浏览器是否使用了缓存的旧数据（尝试刷新页面或清除缓存）
  
- 临时前端修复只是权宜之计，根本解决方案还是重启后端服务器

## 相关文件

- `backend/app/routers/grades.py` - 成绩查询API（已修改）
- `frontend/src/views/Campus.vue` - 课程评价UI组件（可能需要临时修复）
- `backend/direct_test_grades.py` - 数据验证脚本（已测试通过）
