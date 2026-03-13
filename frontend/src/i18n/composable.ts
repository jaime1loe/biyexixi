/**
 * 国际化组合式函数
 * 用于在 Vue 组件中使用国际化功能
 */

import { ref, watch } from 'vue'
import { t, setLanguage, getCurrentLanguage, Language } from './index'

export function useI18n() {
  // 当前语言
  const currentLanguage = ref<Language>(getCurrentLanguage())

  // 监听语言变化事件
  const onLanguageChange = () => {
    window.addEventListener('languageChanged', (e: any) => {
      currentLanguage.value = e.detail.lang
    })
  }

  // 获取翻译
  const translate = (key: string, fallback?: string) => {
    return t(key, fallback)
  }

  // 设置语言
  const changeLanguage = (lang: Language) => {
    setLanguage(lang)
    currentLanguage.value = lang
  }

  // 初始化监听
  onLanguageChange()

  return {
    t: translate,
    locale: currentLanguage,
    setLocale: changeLanguage
  }
}
