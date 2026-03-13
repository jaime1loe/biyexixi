/**
 * 通知工具
 * 用于管理系统桌面通知
 */

// 通知管理器类
class NotificationManager {
  private enabled: boolean = false
  private soundEnabled: boolean = true
  private dndMode: boolean = false
  private dndStart: string = '22:00'
  private dndEnd: string = '08:00'
  private notificationTypes: string[] = ['answer', 'system']

  /**
   * 检查通知权限
   */
  private async checkPermission(): Promise<boolean> {
    if (!('Notification' in window)) {
      return false
    }

    if (Notification.permission === 'granted') {
      return true
    }

    if (Notification.permission !== 'denied') {
      const permission = await Notification.requestPermission()
      return permission === 'granted'
    }

    return false
  }

  /**
   * 检查是否在免打扰时段
   */
  private isInDndMode(): boolean {
    if (!this.dndMode) return false

    const now = new Date()
    const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`

    if (this.dndStart <= this.dndEnd) {
      // 不跨天
      return currentTime >= this.dndStart && currentTime <= this.dndEnd
    } else {
      // 跨天
      return currentTime >= this.dndStart || currentTime <= this.dndEnd
    }
  }

  /**
   * 检查通知类型是否允许
   */
  private isTypeAllowed(type: string): boolean {
    return this.notificationTypes.includes(type)
  }

  /**
   * 显示通知
   */
  async show(options: {
    title: string
    body: string
    type?: 'answer' | 'recommend' | 'system' | 'update'
    icon?: string
    onClick?: () => void
  }) {
    // 检查通知是否启用
    if (!this.enabled) return

    // 检查通知权限
    if (!(await this.checkPermission())) return

    // 检查免打扰模式
    if (this.isInDndMode()) return

    // 检查通知类型
    if (options.type && !this.isTypeAllowed(options.type)) return

    // 创建通知
    const notification = new Notification(options.title, {
      body: options.body,
      icon: options.icon || '/favicon.ico',
      requireInteraction: false
    })

    // 点击事件
    if (options.onClick) {
      notification.onclick = () => {
        options.onClick?.()
        notification.close()
      }
    }

    // 播放声音
    if (this.soundEnabled) {
      const { sound } = await import('@/utils/sound')
      sound.playNotificationSound()
    }

    // 自动关闭
    setTimeout(() => {
      notification.close()
    }, 5000)
  }

  /**
   * 设置通知开关
   */
  setEnabled(enabled: boolean) {
    this.enabled = enabled
  }

  /**
   * 设置声音开关
   */
  setSoundEnabled(enabled: boolean) {
    this.soundEnabled = enabled
  }

  /**
   * 设置免打扰模式
   */
  setDndMode(enabled: boolean, start?: string, end?: string) {
    this.dndMode = enabled
    if (start) this.dndStart = start
    if (end) this.dndEnd = end
  }

  /**
   * 设置通知类型
   */
  setNotificationTypes(types: string[]) {
    this.notificationTypes = types
  }

  /**
   * 获取通知状态
   */
  getStatus() {
    return {
      enabled: this.enabled,
      soundEnabled: this.soundEnabled,
      dndMode: this.dndMode,
      dndStart: this.dndStart,
      dndEnd: this.dndEnd,
      notificationTypes: this.notificationTypes
    }
  }

  /**
   * 设置通知状态
   */
  setStatus(status: {
    enabled?: boolean
    soundEnabled?: boolean
    dndMode?: boolean
    dndStart?: string
    dndEnd?: string
    notificationTypes?: string[]
  }) {
    if (status.enabled !== undefined) this.enabled = status.enabled
    if (status.soundEnabled !== undefined) this.soundEnabled = status.soundEnabled
    if (status.dndMode !== undefined) this.dndMode = status.dndMode
    if (status.dndStart !== undefined) this.dndStart = status.dndStart
    if (status.dndEnd !== undefined) this.dndEnd = status.dndEnd
    if (status.notificationTypes !== undefined) this.notificationTypes = status.notificationTypes
  }
}

// 创建单例实例
const notificationManager = new NotificationManager()

// 导出单例和便捷方法
export const notification = notificationManager
export const showNotification = (options: {
  title: string
  body: string
  type?: 'answer' | 'recommend' | 'system' | 'update'
  icon?: string
  onClick?: () => void
}) => notificationManager.show(options)
export const setNotificationEnabled = (enabled: boolean) => notificationManager.setEnabled(enabled)
export const setNotificationSoundEnabled = (enabled: boolean) => notificationManager.setSoundEnabled(enabled)
export const setNotificationDndMode = (enabled: boolean, start?: string, end?: string) =>
  notificationManager.setDndMode(enabled, start, end)
export const setNotificationTypes = (types: string[]) => notificationManager.setNotificationTypes(types)
export const getNotificationStatus = () => notificationManager.getStatus()
export const setNotificationStatus = (status: Parameters<typeof notificationManager.setStatus>[0]) =>
  notificationManager.setStatus(status)

export default notification
