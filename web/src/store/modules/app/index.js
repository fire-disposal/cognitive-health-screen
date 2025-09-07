import { defineStore } from 'pinia'
import { themeColorMap } from '~/settings/theme'
import { useDark } from '@vueuse/core'
import { lStorage } from '@/utils'

const THEME_KEY = 'app-theme'
const isDark = useDark()

// 从localStorage获取保存的主题设置
const savedTheme = lStorage.get(THEME_KEY)

export const useAppStore = defineStore('app', {
  state() {
    return {
      reloadFlag: true,
      collapsed: false,
      fullScreen: true,
      /** keepAlive路由的key，重新赋值可重置keepAlive */
      aliveKeys: {},
      isDark,
      theme: savedTheme || 'blue',
    }
  },
  actions: {
    async reloadPage() {
      $loadingBar.start()
      this.reloadFlag = false
      await nextTick()
      this.reloadFlag = true

      setTimeout(() => {
        document.documentElement.scrollTo({ left: 0, top: 0 })
        $loadingBar.finish()
      }, 100)
    },
    switchCollapsed() {
      this.collapsed = !this.collapsed
    },
    setCollapsed(collapsed) {
      this.collapsed = collapsed
    },
    setFullScreen(fullScreen) {
      this.fullScreen = fullScreen
    },
    setAliveKeys(key, val) {
      this.aliveKeys[key] = val
    },
    /** 设置暗黑模式 */
    setDark(isDark) {
      this.isDark = isDark
    },
    /** 切换/关闭 暗黑模式 */
    toggleDark() {
      this.isDark = !this.isDark
    },
    /** 设置用户主题 */
    setTheme(themeName) {
      if (themeName && themeColorMap[themeName]) {
        this.theme = themeName
        // 保存到localStorage
        lStorage.set(THEME_KEY, themeName)
        
        // 应用主题配置
        const themeConfig = themeColorMap[themeName]
        const naiveTheme = {
          common: {
            ...themeConfig,
            // 确保所有主题相关的CSS变量被正确设置
            '--primary-color': themeConfig.primaryColor,
            '--primary-color-hover': themeConfig.primaryColorHover,
            '--primary-color-pressed': themeConfig.primaryColorPressed,
            '--primary-color-suppl': themeConfig.primaryColorSuppl,
            '--text-color': themeConfig.textColor
          }
        }
        
        // 应用到naive-ui
        window.$naive?.setTheme(naiveTheme)
        
        // 更新根元素CSS变量
        const root = document.documentElement
        Object.entries(themeConfig).forEach(([key, value]) => {
          const cssVar = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`
          root.style.setProperty(cssVar, value)
        })
        
        // 触发主题更新事件
        window.dispatchEvent(new CustomEvent('theme-change', { detail: { theme: themeName } }))
      }
    },
    // 已移除LOGO类型相关方法，彻底去除LOGO切换与状态
  },
})
