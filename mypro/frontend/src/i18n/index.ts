/**
 * 简单的国际化配置
 */

// 语言类型
export type Language = 'zh-CN' | 'en-US'

// 翻译字典
export const messages: Record<Language, Record<string, string>> = {
  'zh-CN': {
    // 通用
    'common.confirm': '确定',
    'common.cancel': '取消',
    'common.save': '保存',
    'common.delete': '删除',
    'common.edit': '编辑',
    'common.search': '搜索',
    'common.loading': '加载中...',
    'common.success': '成功',
    'common.error': '错误',
    'common.warning': '警告',
    'common.info': '提示',

    // 导航
    'nav.home': '首页',
    'nav.questions': '问答',
    'nav.knowledge': '知识库',
    'nav.chat': '聊天',
    'nav.settings': '设置',
    'nav.logout': '退出登录',

    // 登录
    'login.title': '登录',
    'login.username': '用户名',
    'login.password': '密码',
    'login.remember': '记住我',
    'login.loginBtn': '登录',
    'login.success': '登录成功',
    'login.failed': '登录失败',

    // 系统设置
    'settings.title': '系统设置',
    'settings.appearance': '外观设置',
    'settings.language': '语言设置',
    'settings.notification': '通知设置',
    'settings.privacy': '隐私设置',
    'settings.advanced': '高级设置',
    'settings.about': '关于',
    'settings.saveAll': '保存所有设置',
    'settings.resetAll': '重置为默认',

    // 外观设置
    'appearance.theme': '主题模式',
    'appearance.light': '浅色',
    'appearance.dark': '深色',
    'appearance.auto': '跟随系统',
    'appearance.primaryColor': '主题颜色',
    'appearance.fontSize': '字体大小',
    'appearance.scale': '界面缩放',

    // 语言设置
    'language.interface': '界面语言',
    'language.ai': 'AI回复语言',
    'language.auto': '自动检测',

    // 通知设置
    'notification.desktop': '桌面通知',
    'notification.sound': '声音提醒',
    'notification.types': '消息通知类型',
    'notification.answer': '收到新回复',
    'notification.recommend': '推荐内容',
    'notification.system': '系统公告',
    'notification.update': '功能更新',
    'notification.dndMode': '免打扰时段',
    'notification.enabled': '开启',
    'notification.disabled': '关闭',

    // 隐私设置
    'privacy.publicProfile': '公开资料',
    'privacy.showOnline': '显示在线状态',
    'privacy.history': '历史记录可见性',
    'privacy.dataSharing': '数据共享',
    'privacy.private': '仅自己可见',
    'privacy.friends': '好友可见',
    'privacy.public': '公开',
    'privacy.allow': '允许',
    'privacy.disallow': '不允许',

    // 高级设置
    'advanced.autoReply': '自动回复',
    'advanced.quickReplies': '快捷回复短语',
    'advanced.clearCache': '清空缓存',
    'advanced.exportData': '导出数据',
    'advanced.deleteAccount': '删除账户',
    'advanced.danger': '危险区域',

    // 消息提示
    'msg.themeChanged': '主题已切换',
    'msg.colorUpdated': '主题颜色已更新',
    'msg.fontSizeSet': '字体大小已设置',
    'msg.interfaceScaled': '界面已缩放',
    'msg.languageChanged': '语言已切换',
    'msg.aiLanguageUpdated': 'AI回复语言设置已更新',
    'msg.notificationEnabled': '桌面通知已开启',
    'msg.notificationDisabled': '桌面通知已关闭',
    'msg.soundEnabled': '声音提醒已开启',
    'msg.soundDisabled': '声音提醒已关闭',
    'msg.notificationTypesUpdated': '通知类型已更新',
    'msg.dndEnabled': '免打扰模式已开启',
    'msg.dndDisabled': '免打扰模式已关闭',
    'msg.settingsSaved': '所有设置已保存',
    'msg.settingsReset': '已重置为默认设置',
    'msg.cacheCleared': '缓存已清空',
    'msg.dataExported': '数据导出成功',
  },

  'en-US': {
    // Common
    'common.confirm': 'Confirm',
    'common.cancel': 'Cancel',
    'common.save': 'Save',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.search': 'Search',
    'common.loading': 'Loading...',
    'common.success': 'Success',
    'common.error': 'Error',
    'common.warning': 'Warning',
    'common.info': 'Info',

    // Navigation
    'nav.home': 'Home',
    'nav.questions': 'Questions',
    'nav.knowledge': 'Knowledge',
    'nav.chat': 'Chat',
    'nav.settings': 'Settings',
    'nav.logout': 'Logout',

    // Login
    'login.title': 'Login',
    'login.username': 'Username',
    'login.password': 'Password',
    'login.remember': 'Remember me',
    'login.loginBtn': 'Login',
    'login.success': 'Login successful',
    'login.failed': 'Login failed',

    // Settings
    'settings.title': 'System Settings',
    'settings.appearance': 'Appearance',
    'settings.language': 'Language',
    'settings.notification': 'Notification',
    'settings.privacy': 'Privacy',
    'settings.advanced': 'Advanced',
    'settings.about': 'About',
    'settings.saveAll': 'Save All Settings',
    'settings.resetAll': 'Reset to Default',

    // Appearance
    'appearance.theme': 'Theme',
    'appearance.light': 'Light',
    'appearance.dark': 'Dark',
    'appearance.auto': 'Auto',
    'appearance.primaryColor': 'Primary Color',
    'appearance.fontSize': 'Font Size',
    'appearance.scale': 'Interface Scale',

    // Language
    'language.interface': 'Interface Language',
    'language.ai': 'AI Response Language',
    'language.auto': 'Auto Detect',

    // Notification
    'notification.desktop': 'Desktop Notification',
    'notification.sound': 'Sound Alert',
    'notification.types': 'Notification Types',
    'notification.answer': 'New Replies',
    'notification.recommend': 'Recommendations',
    'notification.system': 'System Announcements',
    'notification.update': 'Feature Updates',
    'notification.dndMode': 'Do Not Disturb',
    'notification.enabled': 'Enabled',
    'notification.disabled': 'Disabled',

    // Privacy
    'privacy.publicProfile': 'Public Profile',
    'privacy.showOnline': 'Show Online Status',
    'privacy.history': 'History Visibility',
    'privacy.dataSharing': 'Data Sharing',
    'privacy.private': 'Private',
    'privacy.friends': 'Friends Only',
    'privacy.public': 'Public',
    'privacy.allow': 'Allow',
    'privacy.disallow': 'Disallow',

    // Advanced
    'advanced.autoReply': 'Auto Reply',
    'advanced.quickReplies': 'Quick Replies',
    'advanced.clearCache': 'Clear Cache',
    'advanced.exportData': 'Export Data',
    'advanced.deleteAccount': 'Delete Account',
    'advanced.danger': 'Danger Zone',

    // Messages
    'msg.themeChanged': 'Theme changed to',
    'msg.colorUpdated': 'Theme color updated',
    'msg.fontSizeSet': 'Font size set to',
    'msg.interfaceScaled': 'Interface scaled to',
    'msg.languageChanged': 'Language changed',
    'msg.aiLanguageUpdated': 'AI language settings updated',
    'msg.notificationEnabled': 'Desktop notification enabled',
    'msg.notificationDisabled': 'Desktop notification disabled',
    'msg.soundEnabled': 'Sound alert enabled',
    'msg.soundDisabled': 'Sound alert disabled',
    'msg.notificationTypesUpdated': 'Notification types updated',
    'msg.dndEnabled': 'Do not disturb mode enabled',
    'msg.dndDisabled': 'Do not disturb mode disabled',
    'msg.settingsSaved': 'All settings saved',
    'msg.settingsReset': 'Reset to default settings',
    'msg.cacheCleared': 'Cache cleared',
    'msg.dataExported': 'Data exported successfully',
  }
}

// 当前语言
let currentLanguage: Language = 'zh-CN'

// 初始化语言
export function initLanguage() {
  const saved = localStorage.getItem('settings')
  if (saved) {
    try {
      const settings = JSON.parse(saved)
      if (settings.language?.current) {
        currentLanguage = settings.language.current
      }
    } catch (e) {
      console.warn('Failed to load language settings:', e)
    }
  }
  return currentLanguage
}

// 设置语言
export function setLanguage(lang: Language) {
  currentLanguage = lang
  localStorage.setItem('language', lang)

  // 更新 HTML lang 属性
  document.documentElement.lang = lang
}

// 获取翻译
export function t(key: string, fallback?: string): string {
  return messages[currentLanguage]?.[key] || fallback || key
}

// 获取当前语言
export function getCurrentLanguage(): Language {
  return currentLanguage
}

// 支持的语言列表
export const supportedLanguages: { label: string; value: Language }[] = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
]
