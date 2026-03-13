<template>
  <div class="i18n-demo">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ t('settings.title') }}</span>
        </div>
      </template>

      <div class="demo-section">
        <h3>{{ t('settings.language') }}</h3>
        <el-radio-group v-model="locale" @change="handleLanguageChange">
          <el-radio value="zh-CN">简体中文</el-radio>
          <el-radio value="en-US">English</el-radio>
        </el-radio-group>
      </div>

      <div class="demo-section">
        <h3>{{ t('appearance.theme') }}</h3>
        <p>{{ t('appearance.light') }}</p>
        <p>{{ t('appearance.dark') }}</p>
        <p>{{ t('appearance.auto') }}</p>
      </div>

      <div class="demo-section">
        <h3>{{ t('common.confirm') }}</h3>
        <el-button type="primary">{{ t('common.confirm') }}</el-button>
        <el-button>{{ t('common.cancel') }}</el-button>
      </div>

      <div class="demo-section">
        <h3>动态翻译</h3>
        <p>当前语言: {{ locale }}</p>
        <p>{{ t('common.loading') }}</p>
        <p>{{ t('common.success') }}</p>
        <p>{{ t('common.error') }}</p>
        <p>{{ t('common.warning') }}</p>
        <p>{{ t('common.info') }}</p>
      </div>

      <div class="demo-section">
        <h3>带默认值的翻译</h3>
        <p>{{ t('unknown.key', '这是默认值') }}</p>
        <p>{{ t('unknown.key2', '这是另一个默认值') }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from '@/i18n/composable'

const { t, locale, setLocale } = useI18n()

const handleLanguageChange = (lang: 'zh-CN' | 'en-US') => {
  setLocale(lang)
  console.log('语言已切换到:', lang)
}
</script>

<style scoped>
.i18n-demo {
  padding: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

.demo-section {
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #ebeef5;
}

.demo-section:last-child {
  border-bottom: none;
}

.demo-section h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #303133;
}

.demo-section p {
  margin: 8px 0;
  color: #606266;
}

.demo-section .el-button {
  margin-right: 8px;
}
</style>
