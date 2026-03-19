<template>
  <div class="campus-container">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="title">校园服务</span>
        </div>
      </template>

      <div class="campus-grid">
        <!-- 空教室查询 -->
        <div class="campus-item" @click="navigateToEmptyClassroom">
          <el-icon size="48" color="#409eff"><School /></el-icon>
          <h3>空教室查询</h3>
          <p>实时查看空闲教室</p>
        </div>

        <!-- 成绩查询/上传 -->
        <div class="campus-item" @click="navigateToGrades">
          <el-icon size="48" color="#67c23a"><Document /></el-icon>
          <h3>{{ currentUser?.role === 'teacher' ? '成绩上传' : '成绩查询' }}</h3>
          <p>{{ currentUser?.role === 'teacher' ? '上传学生考试成绩' : '查看各科考试成绩' }}</p>
        </div>

        <!-- 图书馆 -->
        <div class="campus-item" @click="navigateToLibrary">
          <el-icon size="48" color="#e6a23c"><Reading /></el-icon>
          <h3>图书馆</h3>
          <p>馆藏书籍与座位查询</p>
        </div>

        <!-- 课程评价 -->
        <div class="campus-item" @click="navigateToEvaluations">
          <el-icon size="48" color="#909399"><Document /></el-icon>
          <h3>课程评价</h3>
          <p>{{ currentUser?.role === 'teacher' ? '查看课程评价' : '评价我的课程' }}</p>
        </div>

        <!-- 学生选课 -->
        <div class="campus-item" @click="navigateToCourseSelection">
          <el-icon size="48" color="#f56c6c"><List /></el-icon>
          <h3>学生选课</h3>
          <p>{{ currentUser?.role === 'teacher' ? '课程管理' : '选择课程' }}</p>
        </div>
      </div>
    </el-card>

    <!-- 空教室查询对话框 -->
    <el-dialog v-model="emptyClassroomVisible" title="空教室查询" width="80%" top="5vh">
      <el-form :inline="true" class="search-form" :model="classroomQueryForm">
        <el-form-item label="星期">
          <el-select v-model="classroomQueryForm.day_of_week" placeholder="请选择星期" style="width: 120px">
            <el-option
              v-for="day in weekdays"
              :key="day.value"
              :label="day.label"
              :value="day.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="节次">
          <el-select v-model="classroomQueryForm.period" placeholder="请选择节次" style="width: 140px">
            <el-option
              v-for="period in periods"
              :key="period.value"
              :label="`${period.label} (${period.time})`"
              :value="period.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="周次">
          <el-input-number
            v-model="classroomQueryForm.week"
            :min="1"
            :max="18"
            style="width: 120px"
          />
        </el-form-item>

        <el-form-item label="学期">
          <el-select v-model="classroomQueryForm.semester" placeholder="请选择学期" style="width: 180px">
            <el-option label="2024-2025-2" value="2024-2025-2" />
          </el-select>
        </el-form-item>

        <el-form-item label="教学楼">
          <el-select v-model="classroomQueryForm.building" placeholder="全部" clearable style="width: 120px">
            <el-option
              v-for="building in buildings"
              :key="building"
              :label="building"
              :value="building"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="教室类型">
          <el-select v-model="classroomQueryForm.room_type" placeholder="全部" clearable style="width: 120px">
            <el-option label="普通" value="普通" />
            <el-option label="多媒体" value="多媒体" />
            <el-option label="实验室" value="实验室" />
          </el-select>
        </el-form-item>

        <el-form-item label="最小容量">
          <el-input-number
            v-model="classroomQueryForm.min_capacity"
            :min="0"
            :step="5"
            style="width: 120px"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :icon="Search" @click="handleClassroomSearch" :loading="classroomLoading">
            查询
          </el-button>
          <el-button :icon="Refresh" @click="handleClassroomReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-alert type="info" :closable="false" v-if="!classroomLoading && emptyClassrooms.length > 0">
        共找到 {{ emptyClassrooms.length }} 间空闲教室
      </el-alert>

      <el-empty v-if="!classroomLoading && emptyClassrooms.length === 0" description="未找到符合条件的空闲教室" style="margin: 40px 0;" />

      <div v-loading="classroomLoading" class="classroom-list" v-if="emptyClassrooms.length > 0">
        <div
          v-for="classroom in emptyClassrooms"
          :key="classroom.id"
          class="classroom-item"
          @click="handleClassroomClick(classroom)"
        >
          <div class="classroom-icon">
            <el-icon size="32"><Monitor /></el-icon>
          </div>
          <div class="classroom-info">
            <div class="classroom-name">
              {{ classroom.building }}{{ classroom.room_number }}
              <el-tag :type="getRoomTypeTagType(classroom.room_type)" size="small">
                {{ classroom.room_type }}
              </el-tag>
            </div>
            <div class="classroom-details">
              <el-icon><User /></el-icon>
              容量: {{ classroom.capacity }}人
              <span v-if="classroom.equipment" class="equipment">
                <el-icon><Setting /></el-icon>
                {{ classroom.equipment }}
              </span>
            </div>
            <div class="classroom-floor">
              <el-icon><OfficeBuilding /></el-icon>
              {{ classroom.floor }}楼
            </div>
          </div>
          <div class="classroom-actions">
            <el-button type="primary" size="small" @click.stop="handleClassroomClick(classroom)">
              查看详情
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 成绩管理对话框 -->
    <el-dialog v-model="gradesVisible" :title="currentUser?.role === 'teacher' ? '成绩上传' : '成绩查询'" width="80%" top="5vh">
      <!-- 学生视图 -->
      <div v-if="currentUser?.role === 'student'">
        <el-form :inline="true" class="search-form">
          <el-form-item label="学期">
            <el-select v-model="gradeQuerySemester" placeholder="请选择学期" clearable>
              <el-option label="2024-2025-1" value="2024-2025-1" />
              <el-option label="2024-2025-2" value="2024-2025-2" />
            </el-select>
          </el-form-item>
          <el-form-item label="课程名称">
            <el-input v-model="courseNameSearch" placeholder="输入课程名称搜索" clearable style="width: 200px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="loadMyGrades">查询</el-button>
          </el-form-item>
        </el-form>

        <el-alert v-if="myGrades.length > 0" :closable="false">
          平均绩点: {{ myGrades[0]?.gpa || 0 }}
        </el-alert>

        <el-table v-loading="gradesLoading" :data="myGrades" stripe style="margin-top: 20px;">
          <el-table-column prop="semester" label="学期" width="120" />
          <el-table-column prop="course_code" label="课程代码" width="120" />
          <el-table-column prop="course_name" label="课程名称" min-width="200" />
          <el-table-column prop="credits" label="学分" width="80" />
          <el-table-column prop="score" label="成绩" width="100">
            <template #default="{ row }">
              <el-tag :type="getScoreType(row.score)">{{ row.score }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="grade_point" label="绩点" width="80" />
          <el-table-column prop="grade_level" label="等级" width="80" />
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <el-tag v-if="row.is_makeup" type="warning">补考</el-tag>
              <el-tag v-else type="success">正常</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 教师视图 -->
      <div v-if="currentUser?.role === 'teacher'" v-loading="gradesLoading">
        <el-alert title="教师成绩上传功能" type="info" :closable="false" style="margin-bottom: 20px;">
          请选择课程和学期，录入学生成绩
        </el-alert>

        <el-form :inline="true" class="search-form">
          <el-form-item label="学期">
            <el-select v-model="teacherGradeForm.semester" placeholder="请选择学期">
              <el-option label="2024-2025-1" value="2024-2025-1" />
              <el-option label="2024-2025-2" value="2024-2025-2" />
            </el-select>
          </el-form-item>
          <el-form-item label="课程名称">
            <el-input v-model="teacherCourseNameSearch" placeholder="输入课程名称搜索" clearable style="width: 200px" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="loadTeacherCourses">查询课程</el-button>
          </el-form-item>
        </el-form>

        <!-- 课程列表 -->
        <div v-if="teacherCourses.length > 0" style="margin-top: 20px;">
          <h3 style="margin-bottom: 16px;">我的授课课程</h3>
          <el-card
            v-for="course in teacherCourses"
            :key="course.id"
            shadow="hover"
            style="margin-bottom: 16px; cursor: pointer;"
            @click="selectCourse(course)"
          >
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <strong>{{ course.course_name }}</strong>
                <el-tag style="margin-left: 10px;">{{ course.course_code }}</el-tag>
                <el-tag type="info" style="margin-left: 10px;">{{ course.credits }}学分</el-tag>
                <div style="margin-top: 8px; color: #909399;">学期: {{ course.semester }}</div>
              </div>
              <el-button type="primary" size="small">录入成绩</el-button>
            </div>
          </el-card>
        </div>

        <!-- 学生成绩录入 -->
        <el-dialog
          v-model="gradeUploadVisible"
          title="成绩录入"
          width="70%"
          top="5vh"
          :close-on-click-modal="false"
        >
          <el-alert :closable="false" style="margin-bottom: 20px;">
            课程: {{ selectedCourse?.course_name }} ({{ selectedCourse?.course_code }})
          </el-alert>

          <el-table :data="courseStudents" stripe>
            <el-table-column prop="student_number" label="学号" width="120" />
            <el-table-column prop="student_name" label="姓名" width="120" />
            <el-table-column label="成绩" width="150">
              <template #default="{ row, $index }">
                <el-input-number
                  v-model="studentScores[$index]"
                  :min="0"
                  :max="100"
                  :precision="1"
                  style="width: 120px;"
                  placeholder="成绩"
                />
              </template>
            </el-table-column>
            <el-table-column label="等级" width="80">
              <template #default="{ $index }">
                <el-tag :type="getScoreType(studentScores[$index] || 0)">
                  {{ calculateGradeLevel(studentScores[$index] || 0) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button
                  v-if="row.grade_id"
                  type="danger"
                  size="small"
                  @click="deleteGrade(row.grade_id)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <template #footer>
            <el-button @click="gradeUploadVisible = false">取消</el-button>
            <el-button type="primary" :loading="gradesLoading" @click="uploadGrades">
              提交成绩
            </el-button>
          </template>
        </el-dialog>
      </div>
    </el-dialog>

    <!-- 图书馆对话框 -->
    <el-dialog v-model="libraryVisible" title="图书馆" width="80%">
      <el-tabs v-model="libraryTab">
        <el-tab-pane label="书籍检索" name="books">
          <el-alert type="info" :closable="false" v-if="!booksLoading && books.length > 0">
            共找到 {{ books.length }} 本图书
          </el-alert>
          <el-empty v-if="!booksLoading && books.length === 0" description="暂无图书数据" style="margin: 40px 0;" />

          <el-form :inline="true">
            <el-form-item label="关键词">
              <el-input v-model="bookSearchForm.keyword" placeholder="输入书名或作者" clearable />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchBooks">搜索</el-button>
              <el-button @click="loadAllBooks">显示全部</el-button>
            </el-form-item>
          </el-form>
          <el-table v-loading="booksLoading" :data="books" stripe>
            <el-table-column prop="title" label="书名" min-width="200" />
            <el-table-column prop="author" label="作者" width="120" />
            <el-table-column prop="category" label="分类" width="100" />
            <el-table-column prop="publisher" label="出版社" width="120" />
            <el-table-column prop="publish_year" label="出版年份" width="100" />
            <el-table-column prop="location" label="位置" width="120" />
            <el-table-column prop="available_copies" label="可借" width="80">
              <template #default="{ row }">
                {{ row.available_copies }}/{{ row.total_copies }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.available_copies > 0 ? 'success' : 'danger'">
                  {{ row.available_copies > 0 ? '可借' : '已借完' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="座位查询" name="seats">
          <el-form :inline="true" class="search-form">
            <el-form-item label="楼层">
              <el-select v-model="seatSearchForm.floor" placeholder="全部楼层" clearable style="width: 120px" @change="handleSeatFilterChange">
                <el-option
                  v-for="floor in availableFloors"
                  :key="floor"
                  :label="`${floor}楼`"
                  :value="floor"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="区域">
              <el-select v-model="seatSearchForm.area" placeholder="全部区域" clearable style="width: 140px" @change="handleSeatFilterChange">
                <el-option
                  v-for="area in availableAreas"
                  :key="area"
                  :label="area"
                  :value="area"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="类型">
              <el-select v-model="seatSearchForm.seat_type" placeholder="全部类型" clearable style="width: 120px" @change="handleSeatFilterChange">
                <el-option label="普通" value="普通" />
                <el-option label="靠窗" value="靠窗" />
                <el-option label="安静区" value="安静区" />
                <el-option label="电源位" value="电源位" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadSeats">查询</el-button>
              <el-button @click="resetSeatFilter">重置</el-button>
            </el-form-item>
          </el-form>

          <el-alert v-if="!seatsLoading" type="info" :closable="false" style="margin-bottom: 20px;">
            <div class="seat-stats">
              <el-statistic title="总座位" :value="seatStats.total" />
              <el-statistic title="空闲" :value="seatStats.available" style="color: #67c23a;" />
              <el-statistic title="已预约" :value="seatStats.reserved" style="color: #e6a23c;" />
              <el-statistic title="有人" :value="seatStats.occupied" style="color: #f56c6c;" />
            </div>
          </el-alert>

          <div v-loading="seatsLoading" class="seats-grid">
            <div
              v-for="seat in seats"
              :key="seat.id"
              class="seat-item"
              :class="{
                'available': seat.status === 'available',
                'reserved': seat.status === 'reserved',
                'occupied': seat.status === 'occupied'
              }"
              @click="handleSeatClick(seat)"
            >
              <div class="seat-icon">
                <el-icon size="20">
                  <OfficeBuilding v-if="seat.status === 'available'" />
                  <Lock v-else-if="seat.status === 'reserved'" />
                  <User v-else />
                </el-icon>
              </div>
              <div class="seat-info">
                <div class="seat-number">{{ seat.seat_number }}</div>
                <div class="seat-area">{{ seat.floor }}楼 · {{ seat.area }}</div>
                <div class="seat-type">{{ seat.seat_type }}</div>
                <el-tag :type="getSeatStatusType(seat.status)" size="small">
                  {{ getSeatStatusLabel(seat.status) }}
                </el-tag>
              </div>
            </div>
          </div>

          <el-empty v-if="!seatsLoading && seats.length === 0" description="暂无座位数据" style="margin: 40px 0;" />
        </el-tab-pane>
        <el-tab-pane label="我的预约" name="my-reservations">
          <el-alert type="info" :closable="false" v-if="!myReservationsLoading && myReservations.length > 0">
            共 {{ myReservations.length }} 条预约记录
          </el-alert>
          <el-empty v-if="!myReservationsLoading && myReservations.length === 0" description="暂无预约记录" style="margin: 40px 0;" />
          <el-button type="primary" @click="loadMyReservations" :loading="myReservationsLoading" style="margin-bottom: 20px;">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          <el-table v-loading="myReservationsLoading" :data="myReservations" stripe>
            <el-table-column prop="seat_number" label="座位号" width="120" />
            <el-table-column prop="floor" label="楼层" width="80">
              <template #default="{ row }">
                {{ row.floor }}楼
              </template>
            </el-table-column>
            <el-table-column prop="area" label="区域" width="100" />
            <el-table-column label="类型" width="100">
              <template #default="{ row }">
                {{ row.seat_type || '普通' }}
              </template>
            </el-table-column>
            <el-table-column prop="reservation_date" label="预约日期" width="120" />
            <el-table-column prop="start_time" label="开始时间" width="90" />
            <el-table-column prop="end_time" label="结束时间" width="90" />
            <el-table-column prop="status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="getReservationStatusType(row.status)">
                  {{ getReservationStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="check_in_time" label="签到时间" width="160">
              <template #default="{ row }">
                {{ row.check_in_time || '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === 'reserved'"
                  type="success"
                  size="small"
                  @click="checkInFromMyReservations(row)"
                >
                  签到
                </el-button>
                <el-button
                  v-if="row.status === 'reserved'"
                  type="danger"
                  size="small"
                  @click="cancelReservationFromList(row.id)"
                >
                  取消
                </el-button>
                <el-tag v-if="row.status === 'checked_in'" type="success" size="small">已签到</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 课程评价对话框 -->
    <el-dialog v-model="evaluationsVisible" title="课程评价" width="90%">
      <el-tabs v-model="evaluationTab">
        <!-- 学生：我的评价 -->
        <el-tab-pane v-if="currentUser?.role === 'student'" label="我的评价" name="student">
          <el-button type="primary" @click="showSubmitEvaluation" style="margin-bottom: 20px;">
            <el-icon><Document /></el-icon>
            提交新评价
          </el-button>
          <el-button @click="loadMyEvaluations" :loading="evaluationsLoading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>

          <el-table v-loading="evaluationsLoading" :data="myEvaluations" stripe>
            <el-table-column prop="course_name" label="课程名称" width="150" />
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="teacher_name" label="教师" width="100" />
            <el-table-column prop="semester" label="学期" width="100" />
            <el-table-column prop="overall_rating" label="总体评分" width="100">
              <template #default="{ row }">
                <el-rate v-model="row.overall_rating" disabled />
              </template>
            </el-table-column>
            <el-table-column prop="comment" label="评价内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="is_recommended" label="推荐" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_recommended === 1 ? 'success' : 'info'">
                  {{ row.is_recommended === 1 ? '推荐' : '不推荐' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="editEvaluation(row)">修改</el-button>
                <el-button type="danger" size="small" @click="deleteEvaluation(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 教师：课程评价统计 -->
        <el-tab-pane v-if="currentUser?.role === 'teacher'" label="课程评价统计" name="teacher">
          <el-tabs v-model="evaluationCourseStatsTab">
            <el-tab-pane label="评价列表" name="list">
              <el-form :inline="true">
                <el-form-item label="学期">
                  <el-select v-model="evaluationStatsSemester" placeholder="全部学期" clearable style="width: 150px" @change="loadTeacherEvaluationStats">
                    <el-option label="2024-2025-1" value="2024-2025-1" />
                    <el-option label="2024-2025-2" value="2024-2025-2" />
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="loadTeacherEvaluationStats" :loading="evaluationsLoading">查询</el-button>
                </el-form-item>
              </el-form>

              <el-table v-loading="evaluationsLoading" :data="teacherEvaluationStats" stripe>
                <el-table-column prop="course_name" label="课程名称" width="200" />
                <el-table-column prop="semester" label="学期" width="120" />
                <el-table-column prop="total_evaluations" label="评价人数" width="100" />
                <el-table-column label="教学质量" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.teaching_quality" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="课程内容" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.course_content" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="教师态度" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.teacher_attitude" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="课程难度" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.difficulty" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="作业量" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.workload" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="总体评分" width="100">
                  <template #default="{ row }">
                    <el-rate :model-value="row.average_ratings.overall_rating" disabled />
                  </template>
                </el-table-column>
                <el-table-column label="推荐率" width="100">
                  <template #default="{ row }">
                    <el-tag type="success">{{ row.recommendation_rate }}%</el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 选课对话框 -->
    <el-dialog v-model="courseSelectionVisible" title="学生选课" width="90%">
      <el-tabs v-model="courseSelectionTab">
        <!-- 学生：可选课程 -->
        <el-tab-pane v-if="currentUser?.role === 'student'" label="可选课程" name="available">
          <el-form :inline="true" class="search-form">
            <el-form-item label="学期">
              <el-select v-model="courseSelectionSemester" placeholder="请选择学期" style="width: 150px" @change="loadAvailableCourses">
                <el-option label="2024-2025-1" value="2024-2025-1" />
                <el-option label="2024-2025-2" value="2024-2025-2" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程类型">
              <el-select v-model="courseSearchForm.course_type" placeholder="全部类型" clearable style="width: 120px">
                <el-option label="必修" value="必修" />
                <el-option label="选修" value="选修" />
                <el-option label="实践" value="实践" />
              </el-select>
            </el-form-item>
            <el-form-item label="院系">
              <el-input v-model="courseSearchForm.department" placeholder="输入院系" clearable style="width: 150px" />
            </el-form-item>
            <el-form-item label="搜索">
              <el-input v-model="courseSearchForm.search" placeholder="课程名称或代码" clearable style="width: 180px" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadAvailableCourses">查询</el-button>
              <el-button @click="loadAvailableCourses">刷新</el-button>
            </el-form-item>
          </el-form>

          <el-table v-loading="courseSelectionLoading" :data="availableCourses" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" width="200" />
            <el-table-column prop="teacher_name" label="授课教师" width="100" />
            <el-table-column prop="department" label="院系" width="120" />
            <el-table-column prop="course_type" label="类型" width="80">
              <template #default="{ row }">
                <el-tag :type="row.course_type === '必修' ? 'primary' : row.course_type === '选修' ? 'success' : 'info'">
                  {{ row.course_type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="credits" label="学分" width="80" />
            <el-table-column prop="hours" label="学时" width="80" />
            <el-table-column label="选课人数" width="100">
              <template #default="{ row }">
                {{ row.selected_count || 0 }}/{{ row.capacity || 100 }}
              </template>
            </el-table-column>
            <el-table-column label="剩余名额" width="100">
              <template #default="{ row }">
                <el-tag :type="row.remaining_count > 0 ? 'success' : 'danger'">
                  {{ row.remaining_count || 0 }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.is_selected" type="success">已选</el-tag>
                <el-tag v-else type="info">未选</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="!row.is_selected"
                  type="primary"
                  size="small"
                  :disabled="row.remaining_count <= 0"
                  @click="selectCourseForSelection(row)"
                >
                  选课
                </el-button>
                <el-tag v-else type="success" size="small">已选择</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 学生：我的选课 -->
        <el-tab-pane v-if="currentUser?.role === 'student'" label="我的选课" name="selected">
          <el-button @click="loadMySelections" :loading="courseSelectionLoading" style="margin-bottom: 20px;">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>

          <el-table v-loading="courseSelectionLoading" :data="mySelections" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" width="200" />
            <el-table-column prop="teacher_name" label="授课教师" width="100" />
            <el-table-column prop="semester" label="学期" width="120" />
            <el-table-column prop="course_type" label="类型" width="80" />
            <el-table-column prop="credits" label="学分" width="80" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'selected' ? 'success' : 'info'">
                  {{ row.status === 'selected' ? '已选' : '已退选' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="selected_at" label="选课时间" width="180">
              <template #default="{ row }">
                {{ new Date(row.selected_at).toLocaleString('zh-CN') }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === 'selected'"
                  type="danger"
                  size="small"
                  @click="dropCourse(row.id)"
                >
                  退选
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 教师：课程管理 -->
        <el-tab-pane v-if="currentUser?.role === 'teacher'" label="我的课程" name="teacher">
          <el-form :inline="true">
            <el-form-item label="学期">
              <el-select v-model="courseSelectionSemester" placeholder="请选择学期" style="width: 150px" @change="loadTeacherCourseSelections">
                <el-option label="2024-2025-1" value="2024-2025-1" />
                <el-option label="2024-2025-2" value="2024-2025-2" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="loadTeacherCourseSelections">查询</el-button>
            </el-form-item>
          </el-form>

          <el-table v-loading="courseSelectionLoading" :data="availableCourses" stripe>
            <el-table-column prop="course_code" label="课程代码" width="120" />
            <el-table-column prop="course_name" label="课程名称" width="200" />
            <el-table-column prop="course_type" label="类型" width="80">
              <template #default="{ row }">
                <el-tag :type="row.course_type === '必修' ? 'primary' : 'success'">
                  {{ row.course_type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="credits" label="学分" width="80" />
            <el-table-column prop="hours" label="学时" width="80" />
            <el-table-column prop="selection_count" label="选课人数" width="100">
              <template #default="{ row }">
                <el-tag type="info">{{ row.selection_count }}人</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 提交评价对话框 -->
    <el-dialog v-model="submitEvaluationVisible" title="提交课程评价" width="600px">
      <el-form :model="evaluationForm" label-width="120px">
        <el-form-item label="选择课程">
          <el-select v-model="evaluationForm.course_id" placeholder="请选择课程" style="width: 100%">
            <el-option
              v-for="course in myGrades"
              :key="course.course_id"
              :label="`${course.course_name} (${course.course_code})`"
              :value="course.course_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-input v-model="evaluationForm.semester" disabled />
        </el-form-item>
        <el-form-item label="教学质量">
          <el-rate v-model="evaluationForm.teaching_quality" />
          <span class="rate-label">{{ evaluationForm.teaching_quality }}/5</span>
        </el-form-item>
        <el-form-item label="课程内容">
          <el-rate v-model="evaluationForm.course_content" />
          <span class="rate-label">{{ evaluationForm.course_content }}/5</span>
        </el-form-item>
        <el-form-item label="教师态度">
          <el-rate v-model="evaluationForm.teacher_attitude" />
          <span class="rate-label">{{ evaluationForm.teacher_attitude }}/5</span>
        </el-form-item>
        <el-form-item label="课程难度">
          <el-rate v-model="evaluationForm.difficulty" />
          <span class="rate-label">{{ evaluationForm.difficulty }}/5</span>
        </el-form-item>
        <el-form-item label="作业量">
          <el-rate v-model="evaluationForm.workload" />
          <span class="rate-label">{{ evaluationForm.workload }}/5</span>
        </el-form-item>
        <el-form-item label="总体评分">
          <el-rate v-model="evaluationForm.overall_rating" />
          <span class="rate-label">{{ evaluationForm.overall_rating }}/5</span>
        </el-form-item>
        <el-form-item label="推荐该课程">
          <el-switch v-model="evaluationForm.is_recommended" :active-value="1" :inactive-value="0" />
        </el-form-item>
        <el-form-item label="评价内容">
          <el-input v-model="evaluationForm.comment" type="textarea" :rows="4" placeholder="请输入您的评价内容" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="submitEvaluationVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEvaluation">提交评价</el-button>
      </template>
    </el-dialog>

    <!-- 教室详情对话框 -->
    <el-dialog
      v-model="classroomDetailVisible"
      :title="`${selectedClassroom?.building}${selectedClassroom?.room_number} - 教室详情`"
      width="600px"
    >
      <div v-if="selectedClassroom" class="classroom-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="教学楼">{{ selectedClassroom.building }}</el-descriptions-item>
          <el-descriptions-item label="教室号">{{ selectedClassroom.room_number }}</el-descriptions-item>
          <el-descriptions-item label="容量">{{ selectedClassroom.capacity }}人</el-descriptions-item>
          <el-descriptions-item label="类型">
            <el-tag :type="getRoomTypeTagType(selectedClassroom.room_type)">
              {{ selectedClassroom.room_type }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="楼层">{{ selectedClassroom.floor }}楼</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag type="success">可用</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="设备" :span="2">
            {{ selectedClassroom.equipment || '无' }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider>该教室课表</el-divider>

        <el-table :data="classroomScheduleList" stripe v-loading="classroomScheduleLoading" max-height="300">
          <el-table-column prop="day_of_week" label="星期" width="80">
            <template #default="{ row }">
              {{ getWeekdayLabel(row.day_of_week) }}
            </template>
          </el-table-column>
          <el-table-column prop="period" label="节次" width="100">
            <template #default="{ row }">
              第{{ row.period }}节
            </template>
          </el-table-column>
          <el-table-column prop="class_name" label="班级" />
          <el-table-column label="课程">
            <template #default="{ row }">
              {{ row.course?.course_name }}
            </template>
          </el-table-column>
          <el-table-column label="周次" width="120">
            <template #default="{ row }">
              {{ row.week_start }}-{{ row.week_end }}周
            </template>
          </el-table-column>
        </el-table>
      </div>

      <template #footer>
        <el-button @click="classroomDetailVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 座位详情对话框 -->
    <el-dialog v-model="seatDetailVisible" :title="`座位 ${selectedSeat?.seat_number} 详情`" width="500px">
      <div v-if="selectedSeat" class="seat-detail-content">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="座位号">{{ selectedSeat.seat_number }}</el-descriptions-item>
          <el-descriptions-item label="位置">{{ selectedSeat.floor }}楼 · {{ selectedSeat.area }}</el-descriptions-item>
          <el-descriptions-item label="类型">{{ selectedSeat.seat_type }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getSeatStatusType(selectedSeat.status)">
              {{ getSeatStatusLabel(selectedSeat.status) }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 预约表单 -->
        <div v-if="selectedSeat.status === 'available'" class="reservation-form">
          <h4>预约信息</h4>
          <el-form :model="reservationForm" label-width="80px">
            <el-form-item label="预约日期">
              <el-date-picker
                v-model="reservationForm.reservation_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                :disabled-date="disabledDate"
              />
            </el-form-item>
            <el-form-item label="开始时间">
              <el-time-picker
                v-model="reservationForm.start_time"
                placeholder="选择开始时间"
                format="HH:mm"
                value-format="HH:mm"
                style="width: 100%"
              />
            </el-form-item>
            <el-form-item label="结束时间">
              <el-time-picker
                v-model="reservationForm.end_time"
                placeholder="选择结束时间"
                format="HH:mm"
                value-format="HH:mm"
                style="width: 100%"
              />
            </el-form-item>
          </el-form>
        </div>

        <!-- 操作按钮 -->
        <div class="seat-actions">
          <el-button
            v-if="selectedSeat.status === 'available'"
            type="primary"
            :loading="seatReserving"
            @click="reserveSeat"
          >
            立即预约
          </el-button>
          <el-button
            v-else-if="selectedSeat.status === 'reserved' && isMyReservation(selectedSeat.id)"
            type="success"
            @click="checkInSeat"
          >
            签到
          </el-button>
          <el-button
            v-if="selectedSeat.status === 'reserved' && isMyReservation(selectedSeat.id)"
            type="danger"
            @click="showCancelReservationDialog"
          >
            取消预约
          </el-button>
          <el-button @click="seatDetailVisible = false">关闭</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { School, Document, Reading, Bell, Search, Refresh, Monitor, User, Setting, OfficeBuilding, Lock, List } from '@element-plus/icons-vue'
import { campusApi, Grade, Course, StudentWithGrade, GradeUpload, Seat, SeatStats } from '@/api/campus'
import { evaluationApi, CourseEvaluation, CourseEvaluationStats } from '@/api/evaluation'
import { scheduleApi, Classroom, Schedule } from '@/api/schedule'
import { courseSelectionApi, CourseSelection, CourseWithSelectionStatus, CourseManagementRequest } from '@/api/courseSelection'
import { useUserStore } from '@/store/user'
import type { Grade as GradeType } from '@/api/campus'

const userStore = useUserStore()

// 弹窗显示状态
const emptyClassroomVisible = ref(false)
const gradesVisible = ref(false)
const libraryVisible = ref(false)
const evaluationsVisible = ref(false)
const classroomDetailVisible = ref(false)
const gradeUploadVisible = ref(false)
const seatDetailVisible = ref(false)
const myReservationsVisible = ref(false)
const courseSelectionVisible = ref(false)

// 加载状态
const classroomLoading = ref(false)
const gradesLoading = ref(false)
const booksLoading = ref(false)
const evaluationsLoading = ref(false)
const classroomScheduleLoading = ref(false)
const seatsLoading = ref(false)
const seatReserving = ref(false)
const myReservationsLoading = ref(false)
const courseSelectionLoading = ref(false)

// 数据
const emptyClassrooms = ref<Classroom[]>([])
const books = ref<any[]>([])
const selectedClassroom = ref<Classroom | null>(null)
const classroomScheduleList = ref<Schedule[]>([])
const myGrades = ref<GradeType[]>([])
const teacherCourses = ref<Course[]>([])
const courseStudents = ref<StudentWithGrade[]>([])
const selectedCourse = ref<Course | null>(null)
const studentScores = ref<number[]>([])
const gradeQuerySemester = ref('')
const courseNameSearch = ref('')
const teacherCourseNameSearch = ref('')

// 课程评价相关
const myEvaluations = ref<CourseEvaluation[]>([])
const teacherEvaluationStats = ref<CourseEvaluationStats[]>([])
const evaluationTab = ref('student')
const evaluationCourseStatsTab = ref('list')
const evaluationStatsSemester = ref('')
const evaluationForm = ref({
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
})
const submitEvaluationVisible = ref(false)

// 选课相关
const availableCourses = ref<CourseWithSelectionStatus[]>([])
const mySelections = ref<CourseSelection[]>([])
const courseSelectionTab = ref('available')
const courseSelectionSemester = ref('2024-2025-2')
const courseSelectionForm = ref({
  course_id: 0,
  semester: '2024-2025-2'
})
const courseSearchForm = ref({
  course_type: undefined as string | undefined,
  department: undefined as string | undefined,
  search: ''
})

// 座位相关
const seats = ref<any[]>([])
const selectedSeat = ref<any>(null)
const seatStats = ref({ total: 0, available: 0, occupied: 0, reserved: 0 })
const availableFloors = ref<number[]>([])
const availableAreas = ref<string[]>([])
const myReservations = ref<any[]>([])
const seatSearchForm = ref({
  floor: undefined as number | undefined,
  area: undefined as string | undefined,
  seat_type: undefined as string | undefined
})
const reservationForm = ref({
  reservation_date: '',
  start_time: '',
  end_time: ''
})

// 当前用户
const currentUser = computed(() => userStore.userInfo)

// 教师成绩表单
const teacherGradeForm = ref({
  semester: '2024-2025-2'
})

// 基础数据
const weekdays = ref<Array<{ value: number; label: string }>>([])
const periods = ref<Array<{ value: number; label: string; time: string }>>([])
const buildings = ref<string[]>([])

// 搜索表单
const searchForm = ref({
  building: '',
  day: '',
  section: ''
})

const classroomQueryForm = ref({
  day_of_week: 1,
  period: 1,
  week: 1,
  semester: '2024-2025-2',
  building: '',
  room_type: '',
  min_capacity: 0
})

const bookSearchForm = ref({
  keyword: ''
})

const libraryTab = ref('books')
const librarySeats = ref({
  available: 156,
  total: 500
})

// 导航方法
const navigateToEmptyClassroom = async () => {
  emptyClassroomVisible.value = true
  // 加载基础数据
  if (weekdays.value.length === 0) {
    await loadClassroomBaseData()
  }
}

const navigateToGrades = () => {
  gradesVisible.value = true
  if (currentUser.value?.role === 'student') {
    loadMyGrades()
  } else if (currentUser.value?.role === 'teacher') {
    loadTeacherCourses()
  }
}

const navigateToLibrary = () => {
  libraryVisible.value = true
  // 自动加载所有图书
  loadAllBooks()
  // 加载座位相关数据
  loadLibraryBaseData()
  // 加载座位列表
  loadSeats()
}

const navigateToEvaluations = () => {
  evaluationsVisible.value = true
  if (currentUser.value?.role === 'student') {
    loadMyEvaluations()
  } else if (currentUser.value?.role === 'teacher') {
    // 教师登录时，切换到teacher tab
    evaluationTab.value = 'teacher'
  }
}

const navigateToCourseSelection = () => {
  courseSelectionVisible.value = true
  if (currentUser.value?.role === 'student') {
    loadAvailableCourses()
    loadMySelections()
  } else if (currentUser.value?.role === 'teacher') {
    // 教师登录时，切换到teacher tab
    courseSelectionTab.value = 'teacher'
  }
}



// 加载教室查询基础数据
async function loadClassroomBaseData() {
  try {
    const [weekdaysRes, periodsRes, buildingsRes] = await Promise.all([
      scheduleApi.getWeekdays(),
      scheduleApi.getPeriods(),
      scheduleApi.getBuildings()
    ])

    weekdays.value = weekdaysRes.days
    periods.value = periodsRes.periods
    buildings.value = buildingsRes.buildings

    // 设置默认值
    classroomQueryForm.value.day_of_week = getTodayWeekday()
    classroomQueryForm.value.period = getCurrentPeriod()
  } catch (error) {
    ElMessage.error('加载基础数据失败')
  }
}

// 获取今天是星期几（1-7）
function getTodayWeekday(): number {
  const day = new Date().getDay()
  return day === 0 ? 7 : day
}

// 获取当前节次（根据时间估算）
function getCurrentPeriod(): number {
  const hour = new Date().getHours()
  if (hour < 10) return 1
  if (hour < 12) return 2
  if (hour < 16) return 3
  if (hour < 19) return 4
  return 5
}

// 查询空教室
async function handleClassroomSearch() {
  classroomLoading.value = true
  try {
    emptyClassrooms.value = await scheduleApi.getAvailableClassrooms(classroomQueryForm.value)
    ElMessage.success(`找到 ${emptyClassrooms.value.length} 间空闲教室`)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '查询失败')
    emptyClassrooms.value = []
  } finally {
    classroomLoading.value = false
  }
}

// 重置空教室查询条件
function handleClassroomReset() {
  classroomQueryForm.value = {
    day_of_week: getTodayWeekday(),
    period: getCurrentPeriod(),
    week: 1,
    semester: '2024-2025-2',
    building: '',
    room_type: '',
    min_capacity: 0
  }
  emptyClassrooms.value = []
}

// 查看教室详情
async function handleClassroomClick(classroom: Classroom) {
  selectedClassroom.value = classroom
  classroomDetailVisible.value = true
  classroomScheduleLoading.value = true

  try {
    classroomScheduleList.value = await scheduleApi.getClassroomSchedule(
      classroom.id,
      classroomQueryForm.value.semester
    )
  } catch (error) {
    ElMessage.error('加载课表失败')
    classroomScheduleList.value = []
  } finally {
    classroomScheduleLoading.value = false
  }
}

// 查询方法
const searchEmptyClassroom = async () => {
  if (!searchForm.value.building || !searchForm.value.day || !searchForm.value.section) {
    ElMessage.warning('请填写完整的查询条件')
    return
  }

  classroomLoading.value = true
  try {
    const response = await campusApi.getEmptyClassroom(searchForm.value)
    emptyClassrooms.value = response
  } catch (error: any) {
    console.error('查询空教室失败:', error)
    ElMessage.error(error.response?.data?.detail || '查询失败')
  } finally {
    classroomLoading.value = false
  }
}

const loadGrades = async () => {
  // 该方法已废弃，使用loadMyGrades和loadTeacherCourses替代
}

// 学生：查询我的成绩
const loadMyGrades = async () => {
  gradesLoading.value = true
  try {
    const semester = gradeQuerySemester.value || undefined
    myGrades.value = await campusApi.getMyGrades(semester)
    ElMessage.success('加载成绩成功')
  } catch (error: any) {
    console.error('加载成绩失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    gradesLoading.value = false
  }
}

// 教师：查询所授课程
const loadTeacherCourses = async () => {
  gradesLoading.value = true
  try {
    const semester = teacherGradeForm.value.semester || undefined
    const courseName = teacherCourseNameSearch.value || undefined
    teacherCourses.value = await campusApi.getTeacherCourses(semester, courseName)
  } catch (error: any) {
    console.error('加载课程失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    gradesLoading.value = false
  }
}

// 教师：选择课程并加载学生列表
const selectCourse = async (course: Course) => {
  selectedCourse.value = course
  gradeUploadVisible.value = true
  gradesLoading.value = true

  try {
    const semester = teacherGradeForm.value.semester
    courseStudents.value = await campusApi.getCourseStudents(course.id, semester)
    // 初始化成绩数组
    studentScores.value = courseStudents.value.map(student => student.score || 0)
  } catch (error: any) {
    console.error('加载学生列表失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
    gradeUploadVisible.value = false
  } finally {
    gradesLoading.value = false
  }
}

// 教师：上传成绩
const uploadGrades = async () => {
  if (!selectedCourse.value) return

  gradesLoading.value = true
  try {
    const data: GradeUpload = {
      student_ids: courseStudents.value.map(s => s.student_id),
      course_id: selectedCourse.value.id,
      semester: teacherGradeForm.value.semester,
      scores: studentScores.value
    }

    await campusApi.uploadGrades(data)
    ElMessage.success('成绩上传成功')
    gradeUploadVisible.value = false
    // 重新加载课程列表
    await loadTeacherCourses()
  } catch (error: any) {
    console.error('上传成绩失败:', error)
    ElMessage.error(error.response?.data?.detail || '上传失败')
  } finally {
    gradesLoading.value = false
  }
}

// 教师：删除成绩
const deleteGrade = async (gradeId: number) => {
  try {
    await campusApi.deleteGrade(gradeId)
    ElMessage.success('成绩删除成功')
    // 重新加载当前课程的学生列表
    if (selectedCourse.value) {
      await selectCourse(selectedCourse.value)
    }
  } catch (error: any) {
    console.error('删除成绩失败:', error)
    ElMessage.error(error.response?.data?.detail || '删除失败')
  }
}

// 计算等级
const calculateGradeLevel = (score: number): string => {
  if (score >= 90) return 'A'
  if (score >= 80) return 'B'
  if (score >= 70) return 'C'
  if (score >= 60) return 'D'
  return 'F'
}

// 加载所有图书
const loadAllBooks = async () => {
  booksLoading.value = true
  try {
    const response = await campusApi.searchBooks({})
    books.value = response.books || []
  } catch (error: any) {
    console.error('加载图书失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    booksLoading.value = false
  }
}

const searchBooks = async () => {
  booksLoading.value = true
  try {
    const response = await campusApi.searchBooks({
      keyword: bookSearchForm.value.keyword
    })
    books.value = response.books || []
    ElMessage.success(`找到 ${response.total || 0} 本图书`)
  } catch (error: any) {
    console.error('搜索书籍失败:', error)
    ElMessage.error(error.response?.data?.detail || '搜索失败')
  } finally {
    booksLoading.value = false
  }
}

// 图书馆座位相关函数
const loadLibraryBaseData = async () => {
  try {
    const [floorsRes, areasRes] = await Promise.all([
      campusApi.getFloors(),
      campusApi.getAreas()
    ])
    availableFloors.value = floorsRes.floors
    availableAreas.value = areasRes.areas
  } catch (error) {
    console.error('加载基础数据失败:', error)
  }
}

const loadSeats = async () => {
  seatsLoading.value = true
  try {
    const params: any = {}
    if (seatSearchForm.value.floor !== undefined) params.floor = seatSearchForm.value.floor
    if (seatSearchForm.value.area) params.area = seatSearchForm.value.area
    if (seatSearchForm.value.seat_type) params.seat_type = seatSearchForm.value.seat_type

    const response = await campusApi.getSeats(params)
    seats.value = response.seats
    seatStats.value = {
      total: response.total,
      available: response.available,
      occupied: response.occupied,
      reserved: response.reserved
    }
  } catch (error: any) {
    console.error('加载座位失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    seatsLoading.value = false
  }
}

const handleSeatFilterChange = () => {
  loadSeats()
}

const resetSeatFilter = () => {
  seatSearchForm.value = {
    floor: undefined,
    area: undefined,
    seat_type: undefined
  }
  loadSeats()
}

const handleSeatClick = (seat: Seat) => {
  selectedSeat.value = seat
  seatDetailVisible.value = true
  // 如果是可用座位，设置默认预约日期为今天
  if (seat.status === 'available') {
    const today = new Date()
    reservationForm.value.reservation_date = today.toISOString().split('T')[0]
    reservationForm.value.start_time = ''
    reservationForm.value.end_time = ''
  }
}

const reserveSeat = async () => {
  if (!selectedSeat.value) return

  if (!reservationForm.value.reservation_date) {
    ElMessage.warning('请选择预约日期')
    return
  }

  seatReserving.value = true
  try {
    await campusApi.reserveSeat(selectedSeat.value.id, {
      reservation_date: reservationForm.value.reservation_date,
      start_time: reservationForm.value.start_time,
      end_time: reservationForm.value.end_time
    })
    ElMessage.success('预约成功')
    seatDetailVisible.value = false
    await loadSeats()
  } catch (error: any) {
    console.error('预约失败:', error)
    ElMessage.error(error.response?.data?.detail || '预约失败')
  } finally {
    seatReserving.value = false
  }
}

const checkInSeat = async () => {
  if (!selectedSeat.value) return

  try {
    await campusApi.checkInSeat(selectedSeat.value.id)
    ElMessage.success('签到成功')
    seatDetailVisible.value = false
    await loadSeats()
  } catch (error: any) {
    console.error('签到失败:', error)
    ElMessage.error(error.response?.data?.detail || '签到失败')
  }
}

const showCancelReservationDialog = () => {
  ElMessageBox.confirm('确定要取消该预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    if (!selectedSeat.value) return
    await cancelReservation(selectedSeat.id)
  })
}

const cancelReservation = async (seatId: number) => {
  try {
    await loadMyReservations()
    const reservation = myReservations.value.find(r => r.seat_id === seatId && r.status === 'reserved')
    if (!reservation) {
      ElMessage.error('未找到预约记录')
      return
    }

    await campusApi.cancelReservation(reservation.id)
    ElMessage.success('取消预约成功')
    seatDetailVisible.value = false
    await loadSeats()
  } catch (error: any) {
    console.error('取消预约失败:', error)
    ElMessage.error(error.response?.data?.detail || '取消失败')
  }
}

const isMyReservation = (seatId: number) => {
  return myReservations.value.some(r => r.seat_id === seatId && (r.status === 'reserved' || r.status === 'checked_in'))
}

const loadMyReservations = async () => {
  myReservationsLoading.value = true
  try {
    const response = await campusApi.getMyReservations()
    myReservations.value = response.reservations
  } catch (error: any) {
    console.error('加载我的预约失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    myReservationsLoading.value = false
  }
}

const checkInFromMyReservations = async (reservation: any) => {
  try {
    await campusApi.checkInSeat(reservation.seat_id)
    ElMessage.success('签到成功')
    await loadMyReservations()
  } catch (error: any) {
    console.error('签到失败:', error)
    ElMessage.error(error.response?.data?.detail || '签到失败')
  }
}

const cancelReservationFromList = async (reservationId: number) => {
  ElMessageBox.confirm('确定要取消该预约吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await campusApi.cancelReservation(reservationId)
      ElMessage.success('取消预约成功')
      await loadMyReservations()
    } catch (error: any) {
      console.error('取消预约失败:', error)
      ElMessage.error(error.response?.data?.detail || '取消失败')
    }
  })
}

const disabledDate = (time: Date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return time.getTime() < today.getTime()
}

const showMyReservations = async () => {
  myReservationsVisible.value = true
  await loadMyReservations()
}

// 辅助方法
const getSeatStatusType = (status: string): string => {
  const typeMap: Record<string, string> = {
    'available': 'success',
    'occupied': 'danger',
    'reserved': 'warning'
  }
  return typeMap[status] || 'info'
}

const getSeatStatusLabel = (status: string): string => {
  const labelMap: Record<string, string> = {
    'available': '空闲',
    'occupied': '有人',
    'reserved': '已预约'
  }
  return labelMap[status] || status
}

const getReservationStatusType = (status: string): string => {
  const typeMap: Record<string, string> = {
    'reserved': 'warning',
    'checked_in': 'success',
    'cancelled': 'info'
  }
  return typeMap[status] || 'info'
}

const getReservationStatusLabel = (status: string): string => {
  const labelMap: Record<string, string> = {
    'reserved': '已预约',
    'checked_in': '已签到',
    'cancelled': '已取消'
  }
  return labelMap[status] || status
}

// ========== 课程评价相关函数 ==========

const loadMyEvaluations = async () => {
  evaluationsLoading.value = true
  try {
    const response = await evaluationApi.getMyEvaluations()
    myEvaluations.value = response
  } catch (error: any) {
    console.error('加载我的评价失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    evaluationsLoading.value = false
  }
}

const showSubmitEvaluation = async () => {
  // 确保已加载课程列表
  if (myGrades.value.length === 0) {
    await loadMyGrades()
  }
  if (myGrades.value.length === 0) {
    ElMessage.warning('您还没有任何课程成绩，无法评价')
    return
  }
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

const submitEvaluation = async () => {
  if (!evaluationForm.value.course_id) {
    ElMessage.warning('请选择课程')
    return
  }

  try {
    // 检查是否是编辑模式（有_evaluation_id字段）
    const evaluationId = (evaluationForm.value as any)._evaluation_id

    if (evaluationId) {
      // 编辑模式 - 更新评价
      const updateData = {
        teaching_quality: evaluationForm.value.teaching_quality,
        course_content: evaluationForm.value.course_content,
        teacher_attitude: evaluationForm.value.teacher_attitude,
        difficulty: evaluationForm.value.difficulty,
        workload: evaluationForm.value.workload,
        overall_rating: evaluationForm.value.overall_rating,
        comment: evaluationForm.value.comment,
        is_recommended: evaluationForm.value.is_recommended
      }
      await evaluationApi.updateEvaluation(evaluationId, updateData)
      ElMessage.success('评价修改成功')
    } else {
      // 新建模式 - 创建评价
      await evaluationApi.createEvaluation(evaluationForm.value)
      ElMessage.success('评价提交成功')
    }

    submitEvaluationVisible.value = false
    // 重置表单
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
    await loadMyEvaluations()
  } catch (error: any) {
    console.error('提交评价失败:', error)
    ElMessage.error(error.response?.data?.detail || '提交失败')
  }
}

const editEvaluation = async (evaluation: CourseEvaluation) => {
  // 填充表单
  evaluationForm.value = {
    course_id: evaluation.course_id,
    semester: evaluation.semester,
    teaching_quality: evaluation.teaching_quality,
    course_content: evaluation.course_content,
    teacher_attitude: evaluation.teacher_attitude,
    difficulty: evaluation.difficulty,
    workload: evaluation.workload,
    overall_rating: evaluation.overall_rating,
    comment: evaluation.comment,
    is_recommended: evaluation.is_recommended,
    _evaluation_id: evaluation.id // 添加临时字段存储评价ID
  }
  submitEvaluationVisible.value = true
}

const deleteEvaluation = async (evaluationId: number) => {
  ElMessageBox.confirm('确定要删除该评价吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await evaluationApi.deleteEvaluation(evaluationId)
      ElMessage.success('删除成功')
      await loadMyEvaluations()
    } catch (error: any) {
      console.error('删除评价失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  })
}

const loadTeacherEvaluationStats = async () => {
  evaluationsLoading.value = true
  try {
    const response = await evaluationApi.getTeacherCourseStats(evaluationStatsSemester.value || undefined)
    teacherEvaluationStats.value = response
  } catch (error: any) {
    console.error('加载课程评价统计失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    evaluationsLoading.value = false
  }
}

// 选课相关函数
const loadAvailableCourses = async () => {
  courseSelectionLoading.value = true
  try {
    const response = await courseSelectionApi.getAvailableCourses({
      semester: courseSelectionSemester.value,
      ...courseSearchForm.value
    })
    availableCourses.value = response
  } catch (error: any) {
    console.error('加载可选课程失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    courseSelectionLoading.value = false
  }
}

const loadMySelections = async () => {
  courseSelectionLoading.value = true
  try {
    const response = await courseSelectionApi.getMySelections({
      semester: courseSelectionSemester.value
    })
    mySelections.value = response
  } catch (error: any) {
    console.error('加载我的选课失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    courseSelectionLoading.value = false
  }
}

const selectCourseForSelection = async (course: CourseWithSelectionStatus) => {
  try {
    await courseSelectionApi.selectCourse({
      course_id: course.id,
      semester: courseSelectionSemester.value
    })
    ElMessage.success('选课成功')
    await loadAvailableCourses()
    await loadMySelections()
  } catch (error: any) {
    console.error('选课失败:', error)
    ElMessage.error(error.response?.data?.detail || '选课失败')
  }
}

const dropCourse = async (selectionId: number) => {
  ElMessageBox.confirm('确定要退选该课程吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await courseSelectionApi.dropCourse(selectionId)
      ElMessage.success('退选成功')
      await loadAvailableCourses()
      await loadMySelections()
    } catch (error: any) {
      console.error('退选失败:', error)
      ElMessage.error(error.response?.data?.detail || '退选失败')
    }
  })
}

const loadTeacherCourseSelections = async () => {
  courseSelectionLoading.value = true
  try {
    const response = await courseSelectionApi.getTeacherCourses(courseSelectionSemester.value)
    availableCourses.value = response.map(c => ({
      ...c,
      course_code: c.course_code || '',
      course_name: c.course_name,
      is_selected: true,
      selection_status: 'selected'
    }))
  } catch (error: any) {
    console.error('加载教师课程失败:', error)
    ElMessage.error(error.response?.data?.detail || '加载失败')
  } finally {
    courseSelectionLoading.value = false
  }
}

// 辅助方法

// 辅助方法
const getScoreType = (score: number) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'primary'
  if (score >= 70) return 'warning'
  if (score >= 60) return 'info'
  return 'danger'
}

const getRoomTypeTagType = (roomType: string): string => {
  const typeMap: Record<string, string> = {
    '普通': '',
    '多媒体': 'primary',
    '实验室': 'success'
  }
  return typeMap[roomType] || ''
}

const getWeekdayLabel = (day: number): string => {
  const item = weekdays.value.find(w => w.value === day)
  return item?.label || ''
}

// 监听课程评价对话框打开
watch(evaluationsVisible, async (newValue) => {
  if (newValue && currentUser.value?.role === 'teacher') {
    // 等待对话框渲染完成后再加载
    setTimeout(() => {
      // 确保tab已经是teacher
      if (evaluationTab.value === 'teacher') {
        loadTeacherEvaluationStats()
      }
    }, 200)
  }
})

// 监听选课对话框打开
watch(courseSelectionVisible, async (newValue) => {
  if (newValue && currentUser.value?.role === 'teacher') {
    // 等待对话框渲染完成后再加载
    setTimeout(() => {
      // 确保tab已经是teacher
      if (courseSelectionTab.value === 'teacher') {
        loadTeacherCourseSelections()
      }
    }, 200)
  }
})

// 监听评价Tab切换
watch(evaluationTab, (newValue) => {
  if (newValue === 'teacher' && currentUser.value?.role === 'teacher' && evaluationsVisible.value) {
    loadTeacherEvaluationStats()
  }
})

// 监听选课Tab切换
watch(courseSelectionTab, (newValue) => {
  if (newValue === 'teacher' && currentUser.value?.role === 'teacher' && courseSelectionVisible.value) {
    loadTeacherCourseSelections()
  }
})

onMounted(() => {
  // 页面加载时可以预加载一些数据
})
</script>

<style scoped>
.campus-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.campus-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.campus-item {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border: 1px solid #ebeef5;
  border-radius: 12px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.campus-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #409eff;
}

.campus-item h3 {
  margin: 15px 0 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.campus-item p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.search-form {
  margin-bottom: 20px;
}

.seat-info {
  display: flex;
  justify-content: space-around;
  padding: 40px 0;
  background: #f5f7fa;
  border-radius: 8px;
  margin-top: 20px;
}

.classroom-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
  padding: 10px 0;
}

.classroom-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.classroom-item:hover {
  border-color: #409eff;
  background-color: #f5f7fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.classroom-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.classroom-info {
  flex: 1;
  min-width: 0;
}

.classroom-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.classroom-details {
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.classroom-details .equipment {
  display: flex;
  align-items: center;
  gap: 4px;
}

.classroom-floor {
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.classroom-actions {
  flex-shrink: 0;
}

.classroom-detail {
  padding: 10px 0;
}

/* 座位统计样式 */
.seat-stats {
  display: flex;
  gap: 30px;
  justify-content: center;
  padding: 10px 0;
}

/* 座位网格 - 紧凑布局 */
.seats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
  padding: 10px 0;
}

/* 座位项 */
.seat-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 8px 12px;
  border: 2px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
  min-height: 60px;
  gap: 8px;
}

.seat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.seat-item.available {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e6fffa 100%);
}

.seat-item.reserved {
  border-color: #e6a23c;
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
}

.seat-item.occupied {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
}

.seat-icon {
  margin-bottom: 0;
  flex-shrink: 0;
}

.seat-info {
  text-align: left;
  flex: 1;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  flex-wrap: wrap;
}

.seat-number {
  font-weight: bold;
  font-size: 13px;
  color: #303133;
  margin-bottom: 0;
  flex-shrink: 0;
}

.seat-area {
  font-size: 11px;
  color: #606266;
  margin-bottom: 0;
  flex-shrink: 0;
}

.seat-type {
  font-size: 10px;
  color: #909399;
  margin-bottom: 0;
  flex-shrink: 0;
}

/* 座位详情 */
.seat-detail-content {
  padding: 10px 0;
}

.reservation-form {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
}

.reservation-form h4 {
  margin-bottom: 15px;
  color: #303133;
}

.seat-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
