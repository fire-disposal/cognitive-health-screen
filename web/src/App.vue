<template>
  <AppProvider>
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </AppProvider>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore, useUserStore } from '@/store'
import AppProvider from '@/components/common/AppProvider.vue'
import { lStorage } from '@/utils'

const appStore = useAppStore()
const userStore = useUserStore()

onMounted(() => {
  // 从本地存储恢复主题设置
  const savedTheme = lStorage.get('app-theme')
  if (savedTheme) {
    appStore.setTheme(savedTheme)
  }
})
</script>

<style>
:root {
  transition: all 0.3s; /* 添加过渡效果 */
}
</style>
