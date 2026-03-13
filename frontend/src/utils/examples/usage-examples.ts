/**
 * 系统设置功能使用示例
 *
 * 本文件展示如何在项目中使用系统设置相关的工具函数
 */

// ==================== 1. 声音工具使用示例 ====================

import { sound, playNotificationSound, playSuccessSound, playErrorSound } from '@/utils/sound'

// 示例1: 在消息组件中播放通知音
function onReceiveMessage() {
  if (sound.isEnabled()) {
    playNotificationSound()
  }
}

// 示例2: 在表单提交后播放提示音
async function handleFormSubmit() {
  try {
    await submitData()
    playSuccessSound()
    ElMessage.success('提交成功')
  } catch (error) {
    playErrorSound()
    ElMessage.error('提交失败')
  }
}

// 示例3: 在设置页面切换声音开关
function toggleSound(enabled: boolean) {
  sound.setEnabled(enabled)
  if (enabled) {
    playNotificationSound() // 播放测试音
  }
}

// ==================== 2. 通知工具使用示例 ====================

import {
  notification,
  showNotification,
  setNotificationEnabled,
  setNotificationSoundEnabled,
  setNotificationDndMode,
  setNotificationTypes
} from '@/utils/notification'

// 示例1: 收到新回复时显示通知
function onNewReply(reply: any) {
  notification.show({
    title: '新回复',
    body: `${reply.author}: ${reply.content}`,
    type: 'answer',
    onClick: () => {
      // 点击通知跳转到详情页
      router.push(`/questions/${reply.questionId}`)
    }
  })
}

// 示例2: 收到系统公告时显示通知
function onSystemAnnouncement(announcement: any) {
  showNotification({
    title: '系统公告',
    body: announcement.content,
    type: 'system',
    icon: '/logo.png'
  })
}

// 示例3: AI 回复完成时显示通知
function onAIResponse(response: any) {
  notification.show({
    title: 'AI 回复已完成',
    body: response.summary,
    type: 'answer'
  })
}

// 示例4: 批量设置通知配置
function configureNotification(settings: any) {
  setNotificationEnabled(settings.enabled)
  setNotificationSoundEnabled(settings.sound)
  setNotificationDndMode(settings.dndMode, settings.dndStart, settings.dndEnd)
  setNotificationTypes(settings.types)
}

// ==================== 3. 在 Vue 组件中使用 ====================

import { ref, onMounted } from 'vue'
import { notification, sound } from '@/utils/notification'
import { sound as soundManager } from '@/utils/sound'

export default {
  setup() {
    // 示例1: 聊天组件
    const messages = ref([])

    function sendMessage(content: string) {
      // 发送消息
      chatApi.send(content)

      // 播放发送音
      sound.playSuccessSound()
    }

    function onMessageReceived(message: any) {
      messages.value.push(message)

      // 播放接收音
      if (soundManager.isEnabled()) {
        sound.playNotificationSound()
      }

      // 显示通知（如果不在聊天页面）
      if (!isChatPageActive()) {
        notification.show({
          title: '新消息',
          body: `${message.sender}: ${message.content}`,
          type: 'answer',
          onClick: () => {
            scrollToMessage(message.id)
          }
        })
      }
    }

    // 示例2: 问答组件
    const question = ref(null)

    async function submitAnswer(content: string) {
      try {
        await answerApi.create({
          questionId: question.value.id,
          content
        })

        // 播放成功音
        playSuccessSound()
        ElMessage.success('回答提交成功')

        // 重新加载数据
        await loadQuestion()
      } catch (error) {
        // 播放错误音
        playErrorSound()
        ElMessage.error('提交失败')
      }
    }

    // 示例3: 知识库上传组件
    async function uploadDocument(file: File) {
      try {
        await knowledgeApi.upload(file)

        // 播放成功音
        playSuccessSound()
        ElMessage.success('文档上传成功')

        // 显示通知
        notification.show({
          title: '上传完成',
          body: `文档 ${file.name} 已成功上传`,
          type: 'system'
        })
      } catch (error) {
        // 播放错误音
        playErrorSound()
        ElMessage.error('上传失败')
      }
    }

    // 示例4: 监听新通知
    onMounted(() => {
      // 监听 WebSocket 消息
      ws.on('message', (data) => {
        switch (data.type) {
          case 'reply':
            onNewReply(data.reply)
            break
          case 'announcement':
            onSystemAnnouncement(data.announcement)
            break
          case 'ai_response':
            onAIResponse(data.response)
            break
        }
      })
    })

    return {
      messages,
      sendMessage,
      submitAnswer,
      uploadDocument
    }
  }
}

// ==================== 4. 在 API 调用中使用 ====================

import api from '@/api'

// 统一的 API 调用包装器
async function apiCall<T>(
  fn: () => Promise<T>,
  options?: {
    successMessage?: string
    errorMessage?: string
    showNotification?: boolean
  }
): Promise<T> {
  try {
    const result = await fn()

    // 播放成功音
    playSuccessSound()

    // 显示成功消息
    if (options?.successMessage) {
      ElMessage.success(options.successMessage)
    }

    // 显示通知
    if (options?.showNotification) {
      notification.show({
        title: '操作成功',
        body: options.successMessage || '操作已完成',
        type: 'system'
      })
    }

    return result
  } catch (error) {
    // 播放错误音
    playErrorSound()

    // 显示错误消息
    ElMessage.error(options?.errorMessage || '操作失败')

    throw error
  }
}

// 使用示例
async function createQuestion(question: any) {
  await apiCall(
    () => api.questions.create(question),
    {
      successMessage: '问题发布成功',
      errorMessage: '问题发布失败',
      showNotification: true
    }
  )
}

// ==================== 5. 在 Pinia Store 中使用 ====================

import { defineStore } from 'pinia'
import { notification, sound } from '@/utils/notification'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    enabled: true,
    sound: true,
    types: ['answer', 'system']
  }),

  actions: {
    init() {
      // 从 localStorage 加载设置
      const settings = JSON.parse(localStorage.getItem('settings') || '{}')
      if (settings.notification) {
        this.enabled = settings.notification.desktop
        this.sound = settings.notification.sound
        this.types = settings.notification.types

        // 同步到通知管理器
        notification.setEnabled(this.enabled)
        notification.setSoundEnabled(this.sound)
        notification.setNotificationTypes(this.types)
      }
    },

    showReplyNotification(reply: any) {
      if (!this.enabled) return

      notification.show({
        title: '新回复',
        body: `${reply.author}: ${reply.content}`,
        type: this.types.includes('answer') ? 'answer' : 'system'
      })
    },

    toggleSound(enabled: boolean) {
      this.sound = enabled
      sound.setEnabled(enabled)
      notification.setSoundEnabled(enabled)
    }
  }
})

// ==================== 6. 在路由守卫中使用 ====================

import { createRouter, createWebHistory } from 'vue-router'
import { notification, sound } from '@/utils/notification'

const router = createRouter({
  history: createWebHistory(),
  routes: [...]
})

// 导航前守卫
router.beforeEach((to, from, next) => {
  // 播放页面切换音（可选）
  if (from.name && sound.isEnabled()) {
    sound.playSuccessSound()
  }

  next()
})

// 导航后守卫
router.afterEach((to, from) => {
  // 如果有未读通知，显示通知
  if (to.meta.showUnreadNotification) {
    notification.show({
      title: '新消息',
      body: '您有未读的消息',
      type: 'answer',
      onClick: () => {
        router.push('/messages')
      }
    })
  }
})

// ==================== 7. 在 WebSocket 监听中使用 ====================

import { notification, sound } from '@/utils/notification'
import { sound as soundManager } from '@/utils/sound'

class WebSocketManager {
  private ws: WebSocket | null = null

  connect(url: string) {
    this.ws = new WebSocket(url)

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      switch (data.type) {
        case 'new_reply':
          // 播放声音
          if (soundManager.isEnabled()) {
            playNotificationSound()
          }

          // 显示通知
          notification.show({
            title: '新回复',
            body: data.content,
            type: 'answer',
            onClick: () => {
              router.push(`/questions/${data.questionId}`)
            }
          })

          // 刷新数据
          refreshQuestions()
          break

        case 'new_announcement':
          // 显示系统公告
          notification.show({
            title: '系统公告',
            body: data.content,
            type: 'system'
          })
          break

        case 'ai_response':
          // AI 回复完成
          notification.show({
            title: 'AI 回复完成',
            body: data.summary,
            type: 'answer'
          })
          break
      }
    }
  }
}

export default new WebSocketManager()
