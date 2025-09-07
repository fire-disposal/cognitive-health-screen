<template>
  <router-link h-60 f-c-c to="/">
    <img
      src="/logo/type1.svg"
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
    <div
      v-show="!appStore.collapsed"
      style="font-size: 13px; color: #555; font-weight: 500; max-width: 180px; line-height: 1.4; margin-top: 2px;"
    >
      数字孪生驱动的认知障碍居家健康监测系统
    </div>
  </router-link>
</template>

<script setup>
import { useAppStore } from '@/store'
const title = import.meta.env.VITE_TITLE
const appStore = useAppStore()
</script>
