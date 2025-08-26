<template>
  <router-link h-60 f-c-c to="/">
    <img
      :src="getCurrentLogo()"
      style="width: 36px; height: 36px;"
      object-fit="contain"
    />
    <h2
      v-show="!appStore.collapsed"
      ml-2
      mr-8
      max-w-150
      flex-shrink-0
      text-16
      font-bold
      style="color: var(--primary-color)"
    >
      {{ title }}
    </h2>
  </router-link>
</template>

<script setup>
import { useAppStore } from '@/store'
import { logoTypeMap } from '~/settings/theme'
const title = import.meta.env.VITE_TITLE
const appStore = useAppStore()

const getCurrentLogo = () => {
  return appStore.logoType && logoTypeMap[appStore.logoType]?.icon || logoTypeMap.type1.icon
}
</script>
