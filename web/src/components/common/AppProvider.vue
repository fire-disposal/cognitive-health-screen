<template>
  <n-config-provider
    wh-full
    :locale="zhCN"
    :date-locale="dateZhCN"
    :theme="appStore.isDark ? darkTheme : undefined"
    :theme-overrides="mergedThemeOverrides"
  >
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <slot></slot>
            <NaiveProviderContent />
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup>
import { defineComponent, h, computed, watch, onMounted } from 'vue'
import {
  zhCN,
  dateZhCN,
  darkTheme,
  useLoadingBar,
  useDialog,
  useMessage,
  useNotification,
} from 'naive-ui'
import { useCssVar } from '@vueuse/core'
import { kebabCase } from 'lodash-es'
import { setupMessage, setupDialog } from '@/utils'
import { naiveThemeOverrides } from '~/settings'
import { themeColorMap } from '~/settings/theme'
import { useAppStore, useUserStore } from '@/store'

const appStore = useAppStore()
const userStore = useUserStore()

// 计算合并后的主题覆盖配置
const mergedThemeOverrides = computed(() => {
  const themeConfig = appStore.theme && themeColorMap[appStore.theme]
  if (!themeConfig) return naiveThemeOverrides

  return {
    ...naiveThemeOverrides,
    common: {
      ...naiveThemeOverrides.common,
      ...themeConfig,
      // 强制更新主题相关变量
      primaryColor: themeConfig.primaryColor,
      primaryColorHover: themeConfig.primaryColorHover,
      primaryColorPressed: themeConfig.primaryColorPressed,
      primaryColorSuppl: themeConfig.primaryColorSuppl,
    }
  }
})

function setupCssVar() {
  // 应用默认主题配置
  const baseCommon = naiveThemeOverrides.common
  for (const key in baseCommon) {
    useCssVar(`--${kebabCase(key)}`, document.documentElement).value = baseCommon[key] || ''
  }

  // 应用当前主题配置
  const themeConfig = appStore.theme && themeColorMap[appStore.theme]
  if (themeConfig) {
    for (const key in themeConfig) {
      const cssVar = `--${kebabCase(key)}`
      const value = themeConfig[key]
      if (value) {
        useCssVar(cssVar, document.documentElement).value = value
        // 设置主题色
        if (key === 'primaryColor') {
          window.localStorage.setItem('__THEME_COLOR__', value)
        }
      }
    }
  }
}

// 挂载naive组件的方法至window, 以便在全局使用
function setupNaiveTools() {
  window.$loadingBar = useLoadingBar()
  window.$notification = useNotification()

  window.$message = setupMessage(useMessage())
  window.$dialog = setupDialog(useDialog())
}

const NaiveProviderContent = defineComponent({
  setup() {
    setupNaiveTools()
    
    onMounted(async () => {
      try {
        // 加载用户信息和主题设置
        await userStore.getUserInfo()
        if (userStore.theme) {
          appStore.setTheme(userStore.theme)
        }
      } catch (error) {
        console.error('Failed to load user theme:', error)
      }
    })

    // 监听主题变化
    watch(() => appStore.theme, () => {
      setupCssVar()
    }, { immediate: true })
  },
  render() {
    return h('div')
  },
})
</script>
