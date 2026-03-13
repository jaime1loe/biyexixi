# 国际化（i18n）使用指南

## 概述

本项目提供了一个简单的国际化系统，支持中文和英文切换。

## 功能特性

- ✅ 支持中文（简体）和英文
- ✅ 自动保存语言设置到 localStorage
- ✅ 页面加载时自动应用保存的语言
- ✅ 支持自定义事件通知其他组件语言已更改
- ✅ 提供 Vue 3 Composition API 支持

## 基本使用

### 1. 在 TypeScript/JavaScript 中使用

```typescript
import { t, setLanguage, getCurrentLanguage } from '@/i18n'

// 获取翻译
const title = t('settings.title') // "系统设置" 或 "System Settings"

// 设置语言
setLanguage('en-US') // 切换到英文

// 获取当前语言
const currentLang = getCurrentLanguage() // "en-US"
```

### 2. 在 Vue 组件中使用（组合式 API）

```vue
<script setup lang="ts">
import { useI18n } from '@/i18n/composable'

const { t, locale, setLocale } = useI18n()

// 使用翻译
const title = t('settings.title')

// 监听语言变化
watch(locale, (newLang) => {
  console.log('语言已切换到:', newLang)
})

// 手动切换语言
const handleLanguageChange = (lang: 'zh-CN' | 'en-US') => {
  setLocale(lang)
}
</script>

<template>
  <div>
    <h1>{{ t('settings.title') }}</h1>
    <p>{{ t('common.loading') }}</p>
  </div>
</template>
```

### 3. 在 Vue 组件中使用（选项式 API）

```vue
<script lang="ts">
import { defineComponent } from 'vue'
import { t } from '@/i18n'

export default defineComponent({
  methods: {
    t
  }
})
</script>

<template>
  <div>
    <h1>{{ t('settings.title') }}</h1>
  </div>
</template>
```

### 4. 监听语言变化

```typescript
// 监听语言变化事件
window.addEventListener('languageChanged', (e: any) => {
  const newLang = e.detail.lang
  console.log('语言已切换到:', newLang)

  // 重新加载数据
  loadData()
})

// 清理监听器
const cleanup = () => {
  window.removeEventListener('languageChanged', handleLanguageChange)
}
```

## 翻译文件结构

翻译文件位于 `src/i18n/index.ts`，结构如下：

```typescript
export const messages: Record<Language, Record<string, string>> = {
  'zh-CN': {
    // 中文翻译
    'key1': '翻译1',
    'key2': '翻译2',
  },
  'en-US': {
    // 英文翻译
    'key1': 'Translation 1',
    'key2': 'Translation 2',
  }
}
```

## 添加新的翻译

### 1. 在翻译文件中添加键值对

```typescript
export const messages: Record<Language, Record<string, string>> = {
  'zh-CN': {
    // ... 现有翻译
    'my.new.key': '我的新翻译',
  },
  'en-US': {
    // ... 现有翻译
    'my.new.key': 'My New Translation',
  }
}
```

### 2. 在组件中使用

```vue
<template>
  <div>{{ t('my.new.key') }}</div>
</template>
```

## 翻译键命名规范

建议使用点号分隔的层级结构：

```
模块.功能.具体内容

示例：
- common.confirm
- settings.title
- appearance.theme
- notification.desktop
```

### 现有翻译模块

#### 通用（common）
- common.confirm - 确定
- common.cancel - 取消
- common.save - 保存
- common.delete - 删除

#### 导航（nav）
- nav.home - 首页
- nav.questions - 问答
- nav.knowledge - 知识库
- nav.chat - 聊天
- nav.settings - 设置

#### 系统设置（settings）
- settings.title - 系统设置
- settings.appearance - 外观设置
- settings.language - 语言设置

#### 外观设置（appearance）
- appearance.theme - 主题模式
- appearance.primaryColor - 主题颜色
- appearance.fontSize - 字体大小
- appearance.scale - 界面缩放

#### 通知设置（notification）
- notification.desktop - 桌面通知
- notification.sound - 声音提醒
- notification.types - 消息通知类型

#### 隐私设置（privacy）
- privacy.publicProfile - 公开资料
- privacy.showOnline - 显示在线状态
- privacy.history - 历史记录可见性

#### 高级设置（advanced）
- advanced.autoReply - 自动回复
- advanced.quickReplies - 快捷回复短语
- advanced.clearCache - 清空缓存

#### 消息（msg）
- msg.themeChanged - 主题已切换
- msg.settingsSaved - 所有设置已保存
- msg.cacheCleared - 缓存已清空

## 高级用法

### 1. 带默认值的翻译

```typescript
// 如果找不到翻译，使用默认值
const text = t('my.unknown.key', '默认文本')
```

### 2. 动态翻译键

```typescript
const modules = ['appearance', 'language', 'notification']

modules.forEach(module => {
  const title = t(`settings.${module}`)
  console.log(title)
})
```

### 3. 条件翻译

```typescript
const getMessage = () => {
  if (error.value) {
    return t('common.error')
  } else if (loading.value) {
    return t('common.loading')
  } else {
    return t('common.success')
  }
}
```

## 在系统设置中使用

系统设置页面已集成语言切换功能：

```vue
<el-radio-group v-model="language.current" @change="handleLanguageChange">
  <el-radio label="zh-CN">简体中文</el-radio>
  <el-radio label="en-US">English</el-radio>
</el-radio-group>
```

切换语言后：
1. 界面语言立即更新
2. 设置保存到 localStorage
3. 触发 `languageChanged` 事件
4. 其他组件可以监听此事件并更新界面

## 最佳实践

### 1. 翻译键命名

✅ 推荐：
```typescript
'nav.home'
'settings.appearance.theme'
'msg.themeChanged'
```

❌ 不推荐：
```typescript
'首页'
'外观主题'
'主题切换'
```

### 2. 翻译完整句子

✅ 推荐：
```typescript
'msg.settingsSaved': '所有设置已保存'
```

❌ 不推荐：
```typescript
'msg.all': '所有'
'msg.settings': '设置'
'msg.saved': '已保存'
// 然后拼接: t('msg.all') + t('msg.settings') + t('msg.saved')
```

### 3. 使用组合式函数

在 Vue 组件中，推荐使用 `useI18n()`：

```vue
<script setup lang="ts">
import { useI18n } from '@/i18n/composable'

const { t, locale } = useI18n()
</script>
```

### 4. 监听语言变化

如果需要在语言切换时重新加载数据：

```typescript
import { onMounted, onUnmounted } from 'vue'

const handleLanguageChange = () => {
  loadData()
}

onMounted(() => {
  window.addEventListener('languageChanged', handleLanguageChange)
})

onUnmounted(() => {
  window.removeEventListener('languageChanged', handleLanguageChange)
})
```

## 注意事项

### 1. 翻译键必须存在于两种语言

如果某个键只存在于一种语言，另一种语言会显示键名本身。

### 2. 大小写敏感

翻译键是大小写敏感的：
```typescript
t('common.confirm')  // ✅ 正确
t('Common.Confirm')  // ❌ 错误
```

### 3. 缓存问题

切换语言后，某些数据可能需要重新加载。建议监听 `languageChanged` 事件并重新获取数据。

### 4. 第三方库

Element Plus 等第三方库需要单独配置国际化：

```typescript
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'

app.use(ElementPlus, {
  locale: language === 'zh-CN' ? zhCn : en
})
```

## API 参考

### t(key: string, fallback?: string): string

获取翻译文本。

**参数：**
- `key`: 翻译键
- `fallback`: 可选，当找不到翻译时使用的默认值

**返回：** 翻译后的文本

**示例：**
```typescript
t('common.confirm') // "确定"
t('unknown.key', '默认值') // "默认值"
```

### setLanguage(lang: Language): void

设置当前语言。

**参数：**
- `lang`: 语言代码 ('zh-CN' | 'en-US')

**示例：**
```typescript
setLanguage('en-US')
```

### getCurrentLanguage(): Language

获取当前语言。

**返回：** 当前语言代码

**示例：**
```typescript
const lang = getCurrentLanguage() // "zh-CN"
```

### useI18n()

Vue 3 组合式函数。

**返回：**
- `t`: 翻译函数
- `locale`: 当前语言（响应式）
- `setLocale`: 设置语言函数

**示例：**
```typescript
const { t, locale, setLocale } = useI18n()
```

## 未来改进

- [ ] 添加更多语言支持
- [ ] 支持复数形式
- [ ] 支持日期和数字格式化
- [ ] 支持 Vue I18n 完整功能
- [ ] 添加翻译管理工具
- [ ] 支持从外部文件加载翻译

## 更新日志

### v1.0.0 (2026-03-12)
- 实现基础国际化系统
- 支持中文（简体）和英文
- 提供组合式 API `useI18n()`
- 系统设置页面集成语言切换
- 支持语言变化事件通知
