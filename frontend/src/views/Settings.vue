<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <span class="title">系统设置</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" type="border-card">
        <!-- 外观设置 -->
        <el-tab-pane label="外观设置" name="appearance">
          <div class="setting-section">
            <h3>主题模式</h3>
            <el-radio-group v-model="appearance.theme" @change="handleThemeChange">
              <el-radio-button value="light">
                <el-icon><Sunny /></el-icon>
                浅色
              </el-radio-button>
              <el-radio-button value="dark">
                <el-icon><Moon /></el-icon>
                深色
              </el-radio-button>
              <el-radio-button value="auto">
                <el-icon><Monitor /></el-icon>
                跟随系统
              </el-radio-button>
            </el-radio-group>
          </div>

          <div class="setting-section">
            <h3>主题颜色</h3>
            <div class="color-picker-wrapper">
              <el-color-picker
                v-model="appearance.primaryColor"
                :predefine="predefineColors"
                @change="handleColorChange"
              />
              <span class="color-value">{{ appearance.primaryColor }}</span>
            </div>
          </div>

          <div class="setting-section">
            <h3>字体大小</h3>
            <el-slider
              v-model="appearance.fontSize"
              :min="12"
              :max="20"
              :step="1"
              show-stops
              @change="handleFontSizeChange"
            />
            <el-text type="info" size="small">当前: {{ appearance.fontSize }}px</el-text>
          </div>

          <div class="setting-section">
            <h3>界面缩放</h3>
            <el-select v-model="appearance.scale" @change="handleScaleChange">
              <el-option label="75%" :value="0.75" />
              <el-option label="90%" :value="0.9" />
              <el-option label="100%" :value="1" />
              <el-option label="110%" :value="1.1" />
              <el-option label="125%" :value="1.25" />
            </el-select>
          </div>
        </el-tab-pane>

        <!-- 语言设置 -->
        <el-tab-pane label="语言设置" name="language">
          <div class="setting-section">
            <h3>界面语言</h3>
            <el-radio-group v-model="language.current" @change="handleLanguageChange">
              <el-radio value="zh-CN">简体中文</el-radio>
              <el-radio value="en-US">English</el-radio>
            </el-radio-group>
          </div>

          <div class="setting-section">
            <h3>AI回复语言</h3>
            <el-radio-group v-model="language.aiLanguage" @change="handleAiLanguageChange">
              <el-radio value="auto">自动检测</el-radio>
              <el-radio value="zh-CN">简体中文</el-radio>
              <el-radio value="en-US">English</el-radio>
            </el-radio-group>
          </div>
        </el-tab-pane>

        <!-- 通知设置 -->
        <el-tab-pane label="通知设置" name="notification">
          <div class="setting-section">
            <h3>桌面通知</h3>
            <el-switch
              v-model="notification.desktop"
              active-text="开启"
              inactive-text="关闭"
              @change="handleDesktopNotificationChange"
            />
          </div>

          <div class="setting-section">
            <h3>声音提醒</h3>
            <el-switch
              v-model="notification.sound"
              active-text="开启"
              inactive-text="关闭"
              @change="handleSoundChange"
            />
          </div>

          <div class="setting-section">
            <h3>消息通知类型</h3>
            <el-checkbox-group v-model="notification.types" @change="handleNotificationTypesChange">
              <el-checkbox value="answer">收到新回复</el-checkbox>
              <el-checkbox value="recommend">推荐内容</el-checkbox>
              <el-checkbox value="system">系统公告</el-checkbox>
              <el-checkbox value="update">功能更新</el-checkbox>
            </el-checkbox-group>
          </div>

          <div class="setting-section">
            <h3>免打扰时段</h3>
            <el-switch
              v-model="notification.dndMode"
              active-text="开启"
              inactive-text="关闭"
              @change="handleDndModeChange"
            />
            <div v-if="notification.dndMode" class="dnd-time">
              <el-time-picker
                v-model="notification.dndStart"
                placeholder="开始时间"
                format="HH:mm"
                value-format="HH:mm"
              />
              <span class="time-separator">至</span>
              <el-time-picker
                v-model="notification.dndEnd"
                placeholder="结束时间"
                format="HH:mm"
                value-format="HH:mm"
              />
            </div>
          </div>
        </el-tab-pane>

        <!-- 隐私设置 -->
        <el-tab-pane label="隐私设置" name="privacy">
          <div class="setting-section">
            <h3>公开资料</h3>
            <el-switch
              v-model="privacy.publicProfile"
              active-text="公开"
              inactive-text="私密"
              @change="handlePublicProfileChange"
            />
            <p class="setting-desc">开启后其他用户可以查看你的基本信息</p>
          </div>

          <div class="setting-section">
            <h3>显示在线状态</h3>
            <el-switch
              v-model="privacy.showOnline"
              active-text="显示"
              inactive-text="隐藏"
              @change="handleShowOnlineChange"
            />
          </div>

          <div class="setting-section">
            <h3>历史记录可见性</h3>
            <el-radio-group v-model="privacy.historyVisibility" @change="handleHistoryVisibilityChange">
              <el-radio value="private">仅自己可见</el-radio>
              <el-radio value="friends">好友可见</el-radio>
              <el-radio value="public">公开</el-radio>
            </el-radio-group>
          </div>

          <div class="setting-section">
            <h3>数据共享</h3>
            <el-switch
              v-model="privacy.dataSharing"
              active-text="允许"
              inactive-text="不允许"
              @change="handleDataSharingChange"
            />
            <p class="setting-desc">允许匿名数据用于改进服务</p>
          </div>
        </el-tab-pane>

        <!-- 高级设置 -->
        <el-tab-pane label="高级设置" name="advanced">
          <div class="setting-section">
            <h3>自动回复</h3>
            <el-switch
              v-model="advanced.autoReply"
              active-text="开启"
              inactive-text="关闭"
              @change="handleAutoReplyChange"
            />
          </div>

          <div class="setting-section">
            <h3>快捷回复短语</h3>
            <div class="quick-replies">
              <el-tag
                v-for="(reply, index) in advanced.quickReplies"
                :key="index"
                closable
                @close="removeQuickReply(index)"
                class="reply-tag"
              >
                {{ reply }}
              </el-tag>
              <el-input
                v-if="showReplyInput"
                ref="replyInputRef"
                v-model="newReply"
                size="small"
                style="width: 200px"
                @blur="addQuickReply"
                @keyup.enter="addQuickReply"
              />
              <el-button
                v-else
                size="small"
                :icon="Plus"
                @click="handleAddReplyClick"
              >
                添加快捷回复
              </el-button>
            </div>
          </div>

          <div class="setting-section">
            <h3>清空缓存</h3>
            <el-button type="danger" @click="handleClearCache">
              清空所有缓存
            </el-button>
            <p class="setting-desc">缓存大小: {{ formatBytes(cacheSize) }}</p>
          </div>

          <div class="setting-section">
            <h3>导出数据</h3>
            <el-button @click="handleExportData">
              导出我的数据
            </el-button>
            <p class="setting-desc">导出问答历史和设置</p>
          </div>

          <div class="setting-section danger-zone">
            <h3 class="danger-title">危险区域</h3>
            <el-button type="danger" @click="handleDeleteAccount">
              删除账户
            </el-button>
            <p class="setting-desc warning">此操作不可逆,请谨慎操作</p>
          </div>
        </el-tab-pane>

        <!-- 关于 -->
        <el-tab-pane label="关于" name="about">
          <div class="about-section">
            <div class="logo-section">
              <el-icon :size="60" color="#409EFF"><ChatDotRound /></el-icon>
              <h2>高校知识库在线答疑系统</h2>
              <p class="version">版本 v1.0.0</p>
            </div>

            <el-divider />

            <div class="info-list">
              <div class="info-item">
                <span class="info-label">项目名称:</span>
                <span class="info-value">基于大模型智能体的高校知识库在线答疑系统</span>
              </div>
              <div class="info-item">
                <span class="info-label">开发团队:</span>
                <span class="info-value">李佳敏、刘佳欣、欧阳格</span>
              </div>
              <div class="info-item">
                <span class="info-label">技术栈:</span>
                <span class="info-value">Vue3 + SpringBoot + Python + LangChain</span>
              </div>
              <div class="info-item">
                <span class="info-label">最后更新:</span>
                <span class="info-value">2026年3月10日</span>
              </div>
            </div>

            <el-divider />

            <div class="link-section">
              <h3>相关链接</h3>
              <div class="links">
                <el-button link type="primary" @click="openLink('https://github.com')">
                  <el-icon><Link /></el-icon>
                  项目仓库
                </el-button>
                <el-button link type="primary" @click="openLink('https://docs.example.com')">
                  <el-icon><Document /></el-icon>
                  使用文档
                </el-button>
                <el-button link type="primary" @click="openLink('mailto:support@example.com')">
                  <el-icon><Message /></el-icon>
                  联系我们
                </el-button>
              </div>
            </div>

            <el-divider />

            <div class="footer">
              <p>© 2026 高校知识库在线答疑系统. All rights reserved.</p>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>

      <div class="save-bar">
        <el-button type="primary" @click="handleSaveAll" :loading="saving">
          保存所有设置
        </el-button>
        <el-button @click="handleResetAll">
          重置为默认
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Sunny,
  Moon,
  Monitor,
  ChatDotRound,
  Link,
  Document,
  Message,
  Plus
} from '@element-plus/icons-vue'
import { sound } from '@/utils/sound'
import { notification as notificationManager } from '@/utils/notification'
import { t, setLanguage, getCurrentLanguage, initLanguage } from '@/i18n'

// 当前标签页
const activeTab = ref('appearance')

// 外观设置
const appearance = reactive({
  theme: 'light',
  primaryColor: '#1890FF',
  fontSize: 14,
  scale: 1
})

// 语言设置
const language = reactive({
  current: 'zh-CN',
  aiLanguage: 'auto'
})

// 通知设置
const notification = reactive({
  desktop: false,
  sound: true,
  types: ['answer', 'system'],
  dndMode: false,
  dndStart: '22:00',
  dndEnd: '08:00'
})

// 隐私设置
const privacy = reactive({
  publicProfile: false,
  showOnline: true,
  historyVisibility: 'private',
  dataSharing: false
})

// 高级设置
const advanced = reactive({
  autoReply: false,
  quickReplies: ['好的', '收到', '谢谢', '需要帮助吗?']
})

// 缓存大小
const cacheSize = ref(1024 * 500) // 500KB

// 状态
const saving = ref(false)
const showReplyInput = ref(false)
const newReply = ref('')
const replyInputRef = ref()

// 预定义颜色
const predefineColors = [
  '#409EFF',
  '#67C23A',
  '#E6A23C',
  '#F56C6C',
  '#909399',
  '#1890FF',
  '#2F54EB',
  '#722ED1',
  '#EB2F96',
  '#FA541C'
]

// 加载设置
const loadSettings = () => {
  const savedSettings = localStorage.getItem('settings')
  if (savedSettings) {
    const settings = JSON.parse(savedSettings)

    // 加载外观设置
    if (settings.appearance) {
      Object.assign(appearance, settings.appearance)
      // 应用保存的主题
      applyTheme(appearance.theme)
      // 应用保存的主题颜色
      if (appearance.primaryColor) {
        document.documentElement.style.setProperty('--el-color-primary', appearance.primaryColor)
      }
      // 应用保存的字体大小
      if (appearance.fontSize) {
        document.documentElement.style.setProperty('--el-font-size-base', `${appearance.fontSize}px`)
      }
      // 应用保存的缩放
      if (appearance.scale) {
        handleScaleChange(appearance.scale)
      }
    }

    // 加载语言设置
    if (settings.language) {
      Object.assign(language, settings.language)
    }

    // 加载通知设置
    if (settings.notification) {
      Object.assign(notification, settings.notification)
    }

    // 加载隐私设置
    if (settings.privacy) {
      Object.assign(privacy, settings.privacy)
    }

    // 加载高级设置
    if (settings.advanced) {
      Object.assign(advanced, settings.advanced)
    }
  }
}

// 保存设置
const saveSettings = () => {
  const settings = {
    appearance: { ...appearance },
    language: { ...language },
    notification: { ...notification },
    privacy: { ...privacy },
    advanced: { ...advanced }
  }
  localStorage.setItem('settings', JSON.stringify(settings))

  // 同步通知设置到通知管理器
  notificationManager.setEnabled(notification.desktop)
  notificationManager.setSoundEnabled(notification.sound)
  notificationManager.setNotificationTypes(notification.types)
  notificationManager.setDndMode(notification.dndMode, notification.dndStart, notification.dndEnd)
}

// 应用主题
const applyTheme = (theme: string) => {
  const html = document.documentElement

  // 移除所有主题类
  html.classList.remove('light', 'dark')

  if (theme === 'auto') {
    // 跟随系统主题
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    html.classList.add(prefersDark ? 'dark' : 'light')
  } else {
    html.classList.add(theme)
  }

  // 设置 CSS 变量
  if (theme === 'dark' || (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.style.setProperty('--el-bg-color', '#1a1a1a')
    document.documentElement.style.setProperty('--el-text-color-primary', '#e5e5e5')
    document.documentElement.style.setProperty('--el-text-color-regular', '#bfbfbf')
    document.documentElement.style.setProperty('--el-border-color', '#434343')
    document.documentElement.style.setProperty('--el-bg-color-page', '#121212')
  } else {
    document.documentElement.style.setProperty('--el-bg-color', '#ffffff')
    document.documentElement.style.setProperty('--el-text-color-primary', '#303133')
    document.documentElement.style.setProperty('--el-text-color-regular', '#606266')
    document.documentElement.style.setProperty('--el-border-color', '#dcdfe6')
    document.documentElement.style.setProperty('--el-bg-color-page', '#f5f7fa')
  }
}

// 主题变更
const handleThemeChange = (value: string) => {
  applyTheme(value)
  ElMessage.success(`已切换到${value === 'light' ? '浅色' : value === 'dark' ? '深色' : '跟随系统'}主题`)
}

// 颜色变更
const handleColorChange = (color: string) => {
  document.documentElement.style.setProperty('--el-color-primary', color)
  ElMessage.success('主题颜色已更新')
}

// 字体大小变更
const handleFontSizeChange = (size: number) => {
  document.documentElement.style.setProperty('--el-font-size-base', `${size}px`)
  ElMessage.success(`字体大小已设置为 ${size}px`)
}

// 缩放变更
const handleScaleChange = (scale: number) => {
  // 使用 CSS 变量 + rem 单位的方式
  // 这样所有使用 rem 单位的元素都会自动缩放
  document.documentElement.style.setProperty('--scale-factor', scale.toString())
  document.documentElement.style.fontSize = `${scale * 16}px`

  ElMessage.success(`界面已缩放至 ${scale * 100}%`)
}

// 语言变更
const handleLanguageChange = (lang: string) => {
  setLanguage(lang as 'zh-CN' | 'en-US')
  const langName = lang === 'zh-CN' ? '简体中文' : 'English'
  ElMessage.success(`已切换为${langName}`)

  // 触发自定义事件，通知其他组件语言已更改
  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }))
}

// AI语言变更
const handleAiLanguageChange = (lang: string) => {
  ElMessage.success('AI回复语言设置已更新')

  // 保存到 localStorage（通过 saveSettings）
  // 触发自定义事件
  window.dispatchEvent(new CustomEvent('aiLanguageChanged', { detail: { lang } }))
}

// 通知设置变更
const handleDesktopNotificationChange = async (value: boolean) => {
  if (value) {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      if (permission === 'granted') {
        notificationManager.setEnabled(true)
        ElMessage.success('桌面通知已开启')
        // 发送测试通知
        notificationManager.show({
          title: '通知已开启',
          body: '您已成功开启桌面通知功能',
          type: 'system'
        })
      } else {
        notification.desktop = false
        notificationManager.setEnabled(false)
        ElMessage.warning('浏览器未授权通知权限')
      }
    } else {
      notification.desktop = false
      notificationManager.setEnabled(false)
      ElMessage.error('您的浏览器不支持桌面通知')
    }
  } else {
    notificationManager.setEnabled(false)
    ElMessage.success('桌面通知已关闭')
  }
}

const handleSoundChange = (value: boolean) => {
  if (value) {
    sound.playNotificationSound()
  }
  sound.setEnabled(value)
  notificationManager.setSoundEnabled(value)
  ElMessage.success(`声音提醒已${value ? '开启' : '关闭'}`)
}

const handleNotificationTypesChange = (types: string[]) => {
  notificationManager.setNotificationTypes(types)
  ElMessage.success('通知类型已更新')
}

const handleDndModeChange = (value: boolean) => {
  notificationManager.setDndMode(value, notification.dndStart, notification.dndEnd)
  ElMessage.success(`免打扰模式已${value ? '开启' : '关闭'}`)
}

// 隐私设置变更
const handlePublicProfileChange = (value: boolean) => {
  ElMessage.success(`资料可见性已设置为${value ? '公开' : '私密'}`)
}

const handleShowOnlineChange = (value: boolean) => {
  ElMessage.success(`在线状态已${value ? '显示' : '隐藏'}`)
}

const handleHistoryVisibilityChange = (value: string) => {
  const map: Record<string, string> = {
    private: '仅自己可见',
    friends: '好友可见',
    public: '公开'
  }
  ElMessage.success(`历史记录${map[value]}`)
}

const handleDataSharingChange = (value: boolean) => {
  ElMessage.success(`数据共享已${value ? '开启' : '关闭'}`)
}

// 高级设置变更
const handleAutoReplyChange = (value: boolean) => {
  ElMessage.success(`自动回复已${value ? '开启' : '关闭'}`)
}

// 快捷回复
const handleAddReplyClick = async () => {
  showReplyInput.value = true
  await nextTick()
  replyInputRef.value?.focus()
}

const addQuickReply = () => {
  if (newReply.value.trim()) {
    advanced.quickReplies.push(newReply.value.trim())
    newReply.value = ''
    showReplyInput.value = false
  } else {
    showReplyInput.value = false
  }
}

const removeQuickReply = (index: number) => {
  advanced.quickReplies.splice(index, 1)
}

// 清空缓存
const handleClearCache = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有缓存吗?此操作不可恢复。',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 清空 localStorage 中的缓存（保留用户信息和设置）
    const user = localStorage.getItem('user')
    const settings = localStorage.getItem('settings')

    localStorage.clear()

    // 恢复必要的数据
    if (user) localStorage.setItem('user', user)
    if (settings) localStorage.setItem('settings', settings)

    // 清空 sessionStorage
    sessionStorage.clear()

    // 清空所有 indexedDB 数据库（可选）
    try {
      const databases = await indexedDB.databases()
      for (const database of databases) {
        if (database.name) {
          indexedDB.deleteDatabase(database.name)
        }
      }
    } catch (e) {
      console.warn('清理 indexedDB 失败:', e)
    }

    cacheSize.value = 0
    ElMessage.success('缓存已清空')
  } catch {
    // 用户取消
  }
}

// 导出数据
const handleExportData = () => {
  const data = {
    user: JSON.parse(localStorage.getItem('user') || '{}'),
    settings: localStorage.getItem('settings'),
    exportTime: new Date().toISOString()
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `export_${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)

  ElMessage.success('数据导出成功')
}

// 删除账户
const handleDeleteAccount = async () => {
  try {
    await ElMessageBox.prompt('请输入 "DELETE" 确认删除账户', '危险操作', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      inputPattern: /^DELETE$/,
      inputErrorMessage: '请输入 DELETE 确认操作',
      type: 'error'
    })

    // TODO: 调用后端API删除账户
    ElMessage.success('账户删除请求已提交')

    setTimeout(() => {
      localStorage.clear()
      window.location.href = '/login'
    }, 2000)
  } catch {
    // 用户取消或输入错误
  }
}

// 保存所有设置
const handleSaveAll = async () => {
  saving.value = true
  try {
    // TODO: 调用后端API保存设置
    await new Promise(resolve => setTimeout(resolve, 500))
    saveSettings()
    ElMessage.success('所有设置已保存')
  } catch (error) {
    ElMessage.error('保存失败,请重试')
  } finally {
    saving.value = false
  }
}

// 重置所有设置
const handleResetAll = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要重置所有设置为默认值吗?',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // 重置为默认值
    Object.assign(appearance, {
      theme: 'light',
      primaryColor: '#1890FF',
      fontSize: 14,
      scale: 1
    })
    Object.assign(language, {
      current: 'zh-CN',
      aiLanguage: 'auto'
    })
    Object.assign(notification, {
      desktop: false,
      sound: true,
      types: ['answer', 'system'],
      dndMode: false,
      dndStart: '22:00',
      dndEnd: '08:00'
    })
    Object.assign(privacy, {
      publicProfile: false,
      showOnline: true,
      historyVisibility: 'private',
      dataSharing: false
    })
    Object.assign(advanced, {
      autoReply: false,
      quickReplies: ['好的', '收到', '谢谢', '需要帮助吗?']
    })

    // 应用重置后的设置
    applyTheme(appearance.theme)
    handleScaleChange(appearance.scale)
    saveSettings()
    ElMessage.success('已重置为默认设置')
  } catch {
    // 用户取消
  }
}

// 打开链接
const openLink = (url: string) => {
  window.open(url, '_blank')
}

// 格式化字节
const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

onMounted(() => {
  // 初始化语言
  initLanguage()
  loadSettings()
  // 初始化主题
  applyTheme(appearance.theme)
  // 初始化声音设置
  sound.setEnabled(notification.sound)
  // 初始化通知设置
  notificationManager.setEnabled(notification.desktop)
  notificationManager.setSoundEnabled(notification.sound)
  notificationManager.setNotificationTypes(notification.types)
  notificationManager.setDndMode(notification.dndMode, notification.dndStart, notification.dndEnd)
  // 监听系统主题变化
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (appearance.theme === 'auto') {
      applyTheme('auto')
    }
  })
})
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.setting-section {
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
}

.setting-section:last-child {
  border-bottom: none;
}

.setting-section h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.setting-desc {
  margin: 10px 0 0 0;
  font-size: 13px;
  color: #909399;
}

.setting-desc.warning {
  color: #f56c6c;
}

/* 颜色选择器 */
.color-picker-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}

.color-value {
  font-family: monospace;
  color: #606266;
}

/* 免打扰时间 */
.dnd-time {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.time-separator {
  color: #909399;
}

/* 快捷回复 */
.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.reply-tag {
  margin: 0;
}

/* 危险区域 */
.danger-zone {
  padding: 20px;
  background: #fef0f0;
  border-radius: 4px;
  border: 1px solid #fbc4c4;
}

.danger-title {
  color: #f56c6c;
  margin-bottom: 15px;
}

/* 关于页面 */
.about-section {
  padding: 20px 0;
}

.logo-section {
  text-align: center;
  padding: 30px 0;
}

.logo-section h2 {
  margin: 15px 0 5px 0;
  color: #303133;
}

.version {
  color: #909399;
  font-size: 14px;
}

.info-list {
  max-width: 600px;
  margin: 0 auto;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-label {
  font-weight: 500;
  color: #606266;
}

.info-value {
  color: #303133;
}

.link-section h3 {
  margin-bottom: 15px;
  color: #303133;
}

.links {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.links .el-icon {
  margin-right: 5px;
}

.footer {
  text-align: center;
  padding: 20px 0;
  color: #909399;
  font-size: 13px;
}

/* 保存栏 */
.save-bar {
  display: flex;
  justify-content: center;
  gap: 15px;
  padding: 20px 0;
  border-top: 1px solid #ebeef5;
  margin-top: 20px;
}
</style>
