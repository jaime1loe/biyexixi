/**
 * 声音播放工具
 * 用于播放系统通知音
 */

// 声音播放器类
class SoundPlayer {
  private audioContext: AudioContext | null = null
  private enabled: boolean = true

  /**
   * 初始化音频上下文
   */
  private initAudioContext() {
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    }
    return this.audioContext
  }

  /**
   * 播放通知音（使用 Web Audio API 生成简单提示音）
   */
  playNotificationSound() {
    if (!this.enabled) return

    try {
      const ctx = this.initAudioContext()
      const oscillator = ctx.createOscillator()
      const gainNode = ctx.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      oscillator.frequency.value = 800
      oscillator.type = 'sine'

      gainNode.gain.setValueAtTime(0.3, ctx.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5)

      oscillator.start(ctx.currentTime)
      oscillator.stop(ctx.currentTime + 0.5)
    } catch (error) {
      console.warn('播放声音失败:', error)
    }
  }

  /**
   * 播放成功提示音
   */
  playSuccessSound() {
    if (!this.enabled) return

    try {
      const ctx = this.initAudioContext()
      const oscillator = ctx.createOscillator()
      const gainNode = ctx.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      oscillator.frequency.value = 1200
      oscillator.type = 'sine'

      gainNode.gain.setValueAtTime(0.2, ctx.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3)

      oscillator.start(ctx.currentTime)
      oscillator.stop(ctx.currentTime + 0.3)
    } catch (error) {
      console.warn('播放声音失败:', error)
    }
  }

  /**
   * 播放错误提示音
   */
  playErrorSound() {
    if (!this.enabled) return

    try {
      const ctx = this.initAudioContext()
      const oscillator = ctx.createOscillator()
      const gainNode = ctx.createGain()

      oscillator.connect(gainNode)
      gainNode.connect(ctx.destination)

      oscillator.frequency.value = 300
      oscillator.type = 'sawtooth'

      gainNode.gain.setValueAtTime(0.2, ctx.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4)

      oscillator.start(ctx.currentTime)
      oscillator.stop(ctx.currentTime + 0.4)
    } catch (error) {
      console.warn('播放声音失败:', error)
    }
  }

  /**
   * 设置声音开关
   */
  setEnabled(enabled: boolean) {
    this.enabled = enabled
  }

  /**
   * 获取声音状态
   */
  isEnabled(): boolean {
    return this.enabled
  }
}

// 创建单例实例
const soundPlayer = new SoundPlayer()

// 导出单例和便捷方法
export const sound = soundPlayer
export const playNotificationSound = () => soundPlayer.playNotificationSound()
export const playSuccessSound = () => soundPlayer.playSuccessSound()
export const playErrorSound = () => soundPlayer.playErrorSound()
export const setSoundEnabled = (enabled: boolean) => soundPlayer.setEnabled(enabled)
export const isSoundEnabled = () => soundPlayer.isEnabled()

export default sound
